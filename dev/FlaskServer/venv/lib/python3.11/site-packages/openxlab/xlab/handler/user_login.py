import os

from openxlab.xlab.handler.user_config import UserConfig, get_config_path
from openxlab.xlab.handler.user_token import get_token_via_api


def login(ak, sk, re_login=False):
    if os.path.exists(get_config_path()) and re_login is False:
        raise ValueError("AK and SK have been configured. You can set re_login as true to force a re-login.")
    get_token_via_api(ak, sk)
    user_config = UserConfig(ak, sk)
    user_config.store_to_local()

