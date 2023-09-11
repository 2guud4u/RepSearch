import requests

from openxlab.model.common.constants import paths
from openxlab.model.common.response_dto import ReturnDto


class UploadServiceClient(object):
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def get_upload_signature(self, repository_id, uid, model, model_info):
        payload = {"tag": "file", "key": "model-center", "type": 0, "fileType": "file/pth",
                   "fileName": model_info['objectName'],
                   "data": {"repositoryId": repository_id, "modelId": model_info['modelId'],
                            "modelName": model_info['modelName'], "weightName": model_info['weightName'],
                            "uid": uid}}
        response_dto = self.http_post_response_dto("", payload)
        if response_dto.msg_code != '10000':
            raise ValueError(f"Get upload signature error:{response_dto.msg}, traceId:{response_dto.trace_id}")
        if response_dto.data['msgCode'] != '10000':
            raise ValueError(f"Get upload signature error:{response_dto.data['msg']}, "
                             f"traceId:{response_dto.data['traceId']}")
        return response_dto.data['data']

    def http_post_response_dto(self, path, payload):
        headers = self.http_common_header()
        print(f"headers:{headers}, body:{payload}")
        response = requests.post(f"{self.endpoint}{path}", json=payload, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        response_dto = ReturnDto.from_camel_case(response_dict)
        return response_dto

    def http_common_header(self):
        header_dict = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "id": "597091",
            "Authorization": f"Bearer {self.token}"
        }
        return header_dict


