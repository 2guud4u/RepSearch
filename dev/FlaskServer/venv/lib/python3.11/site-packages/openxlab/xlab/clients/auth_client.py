import requests as requests

from openxlab.xlab.common.response_dto import ReturnDto


def http_common_header():
    header_dict = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    return header_dict


def valid_response_dto(response_dto, path, payload):
    if response_dto.msg_code != '10000':
        raise ValueError(f"call {path} error, message: {response_dto.msg}")
    response_data = response_dto.data
    if response_data is None or len(response_data) == 0:
        raise ValueError(f"call {path} error, message: {response_dto.msg}")
    if response_data['msgCode'] != '10000':
        raise ValueError(f"call {path} error, message: {response_data['msg']}")
    return response_data['data']


class AuthClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def http_post_response_dto(self, path, payload):
        headers = http_common_header()
        response = requests.post(f"{self.endpoint}{path}", json=payload, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        response_dto = ReturnDto.from_camel_case(response_dict)
        return response_dto

    def auth(self, ak):
        if len(ak) == 0:
            raise ValueError("access key must not be empty")
        path = "auth"
        payload = {"ak": ak}
        response_dto = self.http_post_response_dto(path, payload)
        auth_dict = valid_response_dto(response_dto, path, payload)
        return auth_dict['nonce'], auth_dict['algorithm']

    def get_jwt(self, ak, d):
        if len(ak) == 0 or len(d) == 0:
            raise ValueError("access key and d must not be empty")
        path = "getJwt"
        payload = {"ak": ak, "d": d}
        response_dto = self.http_post_response_dto(path, payload)
        jwt_dict = valid_response_dto(response_dto, path, payload)
        return jwt_dict

    def refresh_jwt(self, ak, refresh_token):
        if len(ak) == 0 or len(refresh_token) == 0:
            raise ValueError("access key and refresh_token must not be empty")
        path = "refreshJwt"
        payload = {"ak": ak, "refresh_token": refresh_token}
        response_dto = self.http_post_response_dto(path, payload)
        jwt_dict = valid_response_dto(response_dto, path, payload)
        return jwt_dict


