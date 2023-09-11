import json

from openxlab.config import const
from openxlab.utils.env_util import *
from openxlab.utils.file import *


def get_config_path() -> str:
    return os.path.join(get_config_dir(), get_config_file_name())


def get_token_path() -> str:
    return os.path.join(get_config_dir(), get_token_file_name())

def get_dataset_path() -> str:
    return os.path.join(get_config_dir(), get_dataset_file_name())


def get_config_dir() -> str:
    return const.DEFAULT_CONFIG_DIR


def get_token_file_name() -> str:
    return const.DEFAULT_CLI_TOKEN_FILE_NAME


def get_config_file_name() -> str:
    return const.DEFAULT_CLI_CONFIG_FILE_NAME

def get_dataset_file_name() -> str:
    return const.DEFAULT_CLI_DATASET_FILE_NAME


def get_config(ak=None, sk=None, need_force = False):
    """ @need_force: utilized to check user's ak, if not, ask user to login"""
    if ak is not None and sk is not None:
        return UserConfig(ak, sk)
    if not os.path.exists(get_config_path()):
        ak_env_value = get_env(const.AK_ENV_NAME)
        sk_env_value = get_env(const.SK_ENV_NAME)
        if ak_env_value is not None and sk_env_value is not None:
            return UserConfig(ak_env_value, sk_env_value)
        # need login
        if need_force is True and not ak_env_value:
            raise Exception(
                "Please login openxlab and config ak/sk, try \"openxlab login\" and refer to https://openxlab.org.cn/docs/developers/%E9%89%B4%E6%9D%83%E7%AE%A1%E7%90%86.html"
            )
        return None
    config_json = get_file_content(get_config_path())
    config_dict = json.loads(config_json)
    return UserConfig(config_dict['ak'], config_dict['sk'])

def clear_dataset_json():
    """clear the content in dataset.json file"""
    try:
        with open(get_dataset_path(), 'w') as f:
            f.truncate(0)
    except Exception as e:
        raise (e)

class UserConfig(object):
    def __init__(self, ak, sk):
        if ak is None or sk is None:
            raise ValueError("ak and sk must not be empty")
        self.ak = ak
        self.sk = sk

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def store_to_local(self):
        if not os.path.exists(get_config_dir()):
            os.makedirs(get_config_dir(), mode=0o700)
        config_json = self.to_json()
        set_env(const.AK_ENV_NAME, self.ak)
        set_env(const.SK_ENV_NAME, self.sk)
        with open(get_config_path(), mode="w", encoding='utf-8') as f:
            f.write(config_json)
