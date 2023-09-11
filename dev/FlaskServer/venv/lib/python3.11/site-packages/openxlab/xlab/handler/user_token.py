import base64
import hmac

from openxlab.utils.time_util import *
from openxlab.xlab.clients.auth_client import AuthClient
from openxlab.xlab.handler.user_config import *


# TODO
AUTH_CLIENT = AuthClient("https://openapi.openxlab.org.cn/api/v1/sso-be/api/v1/open/")
# AUTH_CLIENT = AuthClient("https://staging.openxlab.org.cn/api/v1/sso-be/api/v1/open/")


def calculate_d(sk, nonce, algorithm):
    if len(sk) == 0 or len(nonce) == 0 or len(algorithm) == 0:
        raise ValueError("sk, nonce and algorith must not be empty")
    try:
        hmac_key = bytearray(sk.encode('utf-8'))
        hmac_obj = hmac.new(
            hmac_key,
            nonce.encode('utf-8'),
            algorithm[4:] if algorithm.startswith("Hmac") else algorithm,
        )
        raw_hmac = hmac_obj.digest()
        return base64.b64encode(raw_hmac).decode('utf-8')
    except KeyError as e:
        raise ValueError("Unsupported hash type: %s" % algorithm) from e
    except Exception as e:
        raise ValueError("Error signing nonce: %s" % str(e)) from e


def get_jwt(ak=None, sk=None):
    return get_token(ak, sk).jwt


def get_token(ak=None, sk=None):
    local_user_token = get_token_from_local()
    if local_user_token is None:
        return get_token_via_api(ak, sk)
    user_token_expiration_datetime = get_datetime_from_formatted_str(local_user_token.expiration)
    now = get_current_time()
    if user_token_expiration_datetime <= now:
        return refresh_token(ak, sk)
    return local_user_token


def get_token_from_local():
    if not os.path.exists(get_token_path()):
        return None
    token_json = get_file_content(get_token_path())
    token_dict = json.loads(token_json)
    return UserToken(**token_dict)


def get_token_via_api(ak=None, sk=None):
    user_config = get_config(ak, sk)
    if user_config is None:
        raise ValueError(
            "Local config must not be empty before get token via api. "
            "Please use the 'openxlab config' command to set the config"
        )
    nonce, algorithm = AUTH_CLIENT.auth(user_config.ak)
    d = calculate_d(user_config.sk, nonce, algorithm)
    jwt_dict = AUTH_CLIENT.get_jwt(user_config.ak, d)
    jwt_dict['refresh_time'] = get_current_formatted_time()
    user_token = UserToken(**jwt_dict)
    # user_token.store_to_local()
    return user_token


def refresh_token(ak=None, sk=None):
    user_config = get_config(ak, sk)
    if user_config is None:
        raise ValueError(
            "Local config must not be empty before refresh token. "
            "Please use the 'openxlab config' command to set the config"
        )
    local_user_token = get_token_from_local()
    if local_user_token is None:
        raise ValueError("local token must not be empty before refresh token")
    refresh_expiration_datetime = get_datetime_from_formatted_str(
        local_user_token.refresh_expiration
    )
    now = get_current_time()
    if refresh_expiration_datetime <= now:
        return get_token_via_api(ak, sk)
    refresh_jwt_dict = AUTH_CLIENT.refresh_jwt(user_config.ak, local_user_token.refresh_token)
    refresh_jwt_dict['refresh_time'] = get_current_formatted_time()
    user_token = UserToken(**refresh_jwt_dict)
    # user_token.store_to_local()
    return user_token


class UserToken(object):
    def __init__(self, jwt, expiration, sso_uid, refresh_time, refresh_token, refresh_expiration):
        self.jwt = jwt
        self.expiration = expiration
        self.sso_uid = sso_uid
        self.refresh_time = refresh_time
        self.refresh_token = refresh_token
        self.refresh_expiration = refresh_expiration

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def store_to_local(self):
        if not os.path.exists(get_config_dir()):
            os.makedirs(get_config_dir(), mode=0o700)
        token_json = self.to_json()
        with open(get_token_path(), mode="w", encoding='utf-8') as f:
            f.write(token_json)
