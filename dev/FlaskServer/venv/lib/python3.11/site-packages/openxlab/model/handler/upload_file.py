"""
upload or update model file | log file | metafile
"""
import re
import os

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.clients.oss_client import OssClient
from openxlab.model.clients.upload_service_client import UploadServiceClient
from openxlab.model.common.constants import endpoint, token, oss_endpoint
from openxlab.model.common.meta_file_util import MetafileParser
from openxlab.model.common.bury import bury_data


@bury_data("upload_file")
def upload(model_repo, file_type='metafile', source=None, target=None) -> None:
    """
    upload model file | readme file | logfile | meta file
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        """
        cli逻辑：
        metafile-根据metafile全部覆盖上传
        other-指定具体文件上传
        web端逻辑如下：
        1. 查询哪些待上传
        2. 更新上传状态-开始上传
        2. 遍历获取signature
        3. 上传oss
        4. 更新上传状态-上传完成
        """
        if file_type == 'metafile':
            remote_model_list = client.query_models(repository)['models']

            meta_parser = MetafileParser(source)
            meta_data = meta_parser.parse_and_validate()
            meta_file_model_list = meta_data['Models']
            upload_model_list(client, repository, meta_file_model_list, remote_model_list)
        elif file_type == 'other':
            print('other way is designing')
        else:
            raise ValueError("file_type only support metafile/other")
        print(f"file upload successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        return


def _split_repo(model_repo) -> (str, str):
    """
    Split a full repository name into two separate strings: the username and the repository name.
    """
    # username/repository format check
    pattern = r'.+/.+'
    if not re.match(pattern, model_repo):
        raise ValueError("The input string must be in the format 'username/model_repo'")

    values = model_repo.split('/')
    return values[0], values[1]


def upload_model_list(client: OpenapiClient, repository, meta_file_model_list, remote_model_list):
    meta_file_model_need_upload_list = []
    # 筛选出新增的models
    new_models = [m_meta for m_meta in meta_file_model_list
                  if m_meta['Name'] not in [m_remote['name'] for m_remote in remote_model_list]]
    update_models = [m_meta for m_meta in meta_file_model_list for m_remote in remote_model_list
                     if m_meta['Name'] == m_remote['name']]
    # 加上更新的models
    meta_file_model_need_upload_list = new_models + update_models
    file_names = [os.path.basename(m['Weights']) for m in meta_file_model_need_upload_list]
    models_data = client.update_upload_status(repository, file_names, new_models, update_models, 1)
    model_info_list = models_data['objects']
    for model in meta_file_model_need_upload_list:
        model_info_filter_list = list(filter(lambda m: m['modelName'] == model['Name'], model_info_list))
        signature = client.get_upload_signature(models_data['repositoryId'], models_data['uid'], model,
                                                model_info_filter_list[0])
        oss_client = OssClient(oss_endpoint, signature['accessKeyId'], signature['accessKeySecret'],
                               signature['stsToken'],
                               signature['bucket'])
        oss_client.upload_to_oss(model['Weights'], signature['object'], signature['callback'], signature['callbackVar'])
        client.update_upload_status(repository, [os.path.basename(model['Weights'])], upload_status=2)
