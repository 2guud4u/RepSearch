import json
import sys

import requests

from openxlab.dataset.constants import odl_clientId
from openxlab.dataset.constants import uaa_url_prefix
from openxlab.xlab.handler.user_token import get_jwt
from openxlab.xlab.handler.user_token import get_token
from openxlab.xlab.handler.user_token import get_token_from_local


api_auth = "/api/v1/internal/auth"
clientId = odl_clientId
auth_url = uaa_url_prefix + api_auth



def get_auth_code(sso_uid):
    result = None
    if sso_uid:
        client_id = {'clientId': clientId}
        data = json.dumps(client_id)
        resp = requests.post(url=auth_url,
                             data=data,
                             headers={
                                 "Content-Type": "application/json",
                                 "Cookie": f"ssouid={sso_uid}",
                             }
                             )
        if resp.status_code == 200:
            result = resp.json()['data']['code']
    return result


def get_odl_token(ak, sk):
    status = get_jwt(ak, sk)
    token = get_token()
    sso_uid = token.sso_uid
    if sso_uid:
        auth_code = get_auth_code(sso_uid=sso_uid)

    if not auth_code:
        print(f"Error: Auth failure")
        sys.exit(1)
    return auth_code, sso_uid
