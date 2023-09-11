"""
Download function for related files in the reality model library
"""
import logging
import re
from tqdm import tqdm
import requests
import os
import hashlib
import sys


from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token, default_metafile_template_name, model_cache_path, \
    river_pass_url
from openxlab.model.common.bury import bury_data

logger = logging.getLogger("openxlab.model")


@bury_data("download_file")
def download(model_repo, model_name, output=None, overwrite=False) -> None:
    """
    download model file|meta file|log filee|readme file
    usage: cli & sdk
    model_repo: username/repository
    model_name: model name
    output: local storage path
    overwrite: whether to overwrite local files
    """
    print(f'model_repo:{model_repo}, model_name:{model_name}, output:{output}, overwrite:{overwrite}')
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        if isinstance(model_name, str):
            model_name = [model_name]
        filepath = None
        models, files = client.get_download_url(username, repository, model_name, filepath)

    except ValueError as e:
        print(f"Error: {e}")
        return
    file_path_download = []
    cache_path = os.path.join(model_cache_path, f'{username}_{repository}')
    for i_name, i_model in models.items() if models is not None else []:
        url = i_model['url']
        file_name = i_model['fileName']
        _hash = i_model['hash']
        file_path = _download_to_local(url, file_name, output, overwrite, cache_path)
        file_path_download.append(file_path)
    for i_name, i_file in files.items() if files is not None else []:
        url = i_file['url']
        file_name = i_file['fileName']
        _hash = i_file['hash']
        file_path = _download_to_local(url, file_name, output, overwrite, cache_path)
        file_path_download.append(file_path)
    print("download model repo:{}, file_name:{}".format(model_repo, file_name))
    return file_path_download


@bury_data("init_metafile")
def download_metafile_template(path=None) -> None:
    """
    download metafile template file
    """
    try:
        # split params
        client = OpenapiClient(endpoint, token)
        url = client.get_metafile_template_download_url()
    except ValueError as e:
        print(f"Error: {e}")
        return
    _download_to_local(url, file_name=default_metafile_template_name, path=path, allow_cache=False)


def download_from_url(url, path=None, overwrite=False):
    filename = os.path.basename(url)
    try:
        river_pass_download_url = river_pass_url + '?url=' + url
        path_file = _download_to_local(river_pass_download_url, file_name=filename, path=path,
                                       overwrite=overwrite, allow_cache=True)
    except Exception as e:
        print(f"use the original path to download")
        # print(f"riverpass info:{e}")
        path_file = _download_to_local(url, file_name=filename, path=path,
                                       overwrite=overwrite, allow_cache=True)

    print(f'success download file: {path_file}')
    return path_file


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


def _download_to_local(url, file_name, path=None, overwrite=False, cache_path=None, allow_cache=None) -> str:
    """
    download file to local with progress_bar
    url: file download url
    file_name: local file name
    path: local path, default current directory
    _hash: file hash
    weight_raw_size: file raw size
    overwrite: whether to overwrite local files
    cache_path: cache path, default is ~/.cache/model
    allow_cache: cache whether is allowed.
    """
    path_file = file_name
    if allow_cache is None:
        allow_cache = sys_allow_cache()
    if path is not None:
        path_file = os.path.join(path, file_name).replace('\\', '/')
    if allow_cache is True:
        if cache_path is None:
            cache_path = model_cache_path
        cache_path_file = os.path.join(cache_path, file_name).replace('\\', '/')
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        elif os.path.exists(cache_path_file) and overwrite is not True:
            clear_and_link(cache_path_file, path_file)
            return path_file

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(cache_path_file if allow_cache else path_file, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if allow_cache is True:
        clear_and_link(cache_path_file, path_file)
    return path_file


def get_file_hash(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as file:
        file_size = file.seek(0, 2)
        if file_size <= 128:  # 如果文件小于等于128字节
            combined_block = file.read(file_size)  # 只读取一次，并将所有数据组合在一起
            hasher.update(combined_block)
        else:  # 否则，读取前64字节和后64字节
            file.seek(0)  # 将文件指针移动到文件开头
            first_block = file.read(64)
            hasher.update(first_block)
            file.seek(-64, 2)  # 将文件指针移动到文件末尾-64处
            last_block = file.read(64)
            hasher.update(last_block)
            combined_block = first_block + last_block
            hasher.update(combined_block)

    return hasher.hexdigest()


def clear_and_link(cache_path_file, path_file):
    if os.path.exists(path_file):
        os.remove(path_file)
    if os.path.islink(path_file):
        os.unlink(path_file)
    os.symlink(cache_path_file, path_file)


def sys_allow_cache():
    """
    win disable cache
    """
    if sys.platform.startswith('win'):
        return False
    else:
        return True
