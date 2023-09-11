import os


# 默认的配置路径
DEFAULT_CONFIG_DIR = os.path.join(
    os.path.expanduser("~"), ".openxlab"
)

 # 默认配置文件名称
DEFAULT_CLI_CONFIG_FILE_NAME = "config.json" 

DEFAULT_CLI_TOKEN_FILE_NAME = "token.json"

DEFAULT_CLI_DATASET_FILE_NAME = "dataset.json"

AK_ENV_NAME = "OPENXLAB_AK"
SK_ENV_NAME = "OPENXLAB_SK"

OPENXLAB_ENV_VALUE_PREFIX = "OPENXLAB_"
