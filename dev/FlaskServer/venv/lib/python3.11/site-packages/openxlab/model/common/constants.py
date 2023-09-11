"""
model module constant define
"""
import os

model_openapi_url_prefix_dev = "https://dev.openxlab.org.cn/api/v1"
model_openapi_url_prefix_staging = "https://staging.openxlab.org.cn/api/v1"
model_openapi_url_prefix_prod = "https://openapi.openxlab.org.cn/api/v1"
model_url_prefix_dev = "http://10.1.100.130:10019"
model_cache_path = os.path.join(os.path.expanduser("~"), '.cache', 'model')
# temp token
token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1OTcwOTEiLCJyb2wiOiJST0xFX0FETUlOIiwiaXNzIjoiT3BlblhMYWIiLCJpYXQiOjE2ODE5Njg4NzMsInBob25lIjoiIiwiYWsiOiI2cHFnOXprNmRteG9rZ2JnbHZvayIsImVtYWlsIjoiZG9uZ3hpYW96aHVhbmdAcGpsYWIub3JnLmNuIiwiZXhwIjoxNzEzNTA0ODczfQ.eFl8ZH9tDp-pcjY3wz6PeNBarJwhVx90qQ3h82Qvpf0hrcrdrQSBcI8AmEk2TZFpeViC6HBtXRxxGp2YLK1XkA"
endpoint = model_openapi_url_prefix_prod
paths = {
    'file_download_path': '/model-center/api/v1/cli/repository/getFileDownloadUrl',
    'meta_file_template_download_path': '/model-center/api/v1/cli/repository/getMetafileTemplateUrl',
    'create_repository_path': '/model-center/api/v1/cli/repository/createModelRepository',
    'update_repository_path': '/model-center/api/v1/cli/repository/updateRepositoryBaseInfo',
    'delete_repository_path': '/model-center/api/v1/cli/repository/deleteRepository',
    'query_models_path': '/model-center/api/v1/cli/repository/getRepositoryModelList',
    'update_upload_status_path': '/model-center/api/v1/cli/repository/updateFileUploadStatus',
    'query_model_repo_info_path': '/model-center/api/v1/cli/repository/queryModelRepoInfo',
    'get_upload_signature': "/upload-service/api/v1/getUploadSignature",
    'bury_upload': "/data-bury/api/v1/bury/collect",
}
# oss_endpoint = 'https://openmmlab-open.oss-cn-shanghai.aliyuncs.com'
oss_endpoint = 'https://oss-cn-shanghai.aliyuncs.com'
oss_bucket_domain_dev = 'openmmlab-open.oss-cn-shanghai.aliyuncs.com'
oss_bucket_domain_staging = 'openmmlab-open.oss-cn-shanghai.aliyuncs.com'
oss_bucket_domain_prod = 'xlab-model-center.oss-cn-shanghai.aliyuncs.com'
oss_bucket_domain = oss_bucket_domain_prod
default_metafile_template_name = 'metafile.yaml'
river_pass_url_dev = 'http://106.14.134.80:10006/getFile'
river_pass_url_staging = 'http://riverpass.staging.openxlab.org.cn/getFile'
river_pass_url_prod = 'http://riverpass.openxlab.org.cn/getFile'
river_pass_url = river_pass_url_prod
