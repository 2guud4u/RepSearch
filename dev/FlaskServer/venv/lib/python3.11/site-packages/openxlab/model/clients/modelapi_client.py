import requests

from openxlab.xlab.handler.user_token import get_jwt
from openxlab.utils.id_util import generate_unique_id
import json
import base64
import os



class ModelApiClient(object):
    def __init__(self, endpoint, token):
        self.token = token
        self.endpoint = endpoint

    def get_inference_result(self, payload):
        """
        get inference result
        """
        result = self.http_post_response_dto(payload)
        return result

    def http_post_response_dto(self, payload):
        headers = self.http_common_header()
        data = {'texts': payload['texts']}
        if payload['args'] is not None:
            data['args'] = payload['args']
        print(f'payload:{payload}')
        response = requests.post(self.endpoint, files=payload["files"], data=data,
                                 headers=headers)
        response.raise_for_status()
        result = Result(payload, response.content, response.headers['Content-Type'])
        return result

    def http_common_header(self):
        try:
            jwt = get_jwt()
        except ValueError as e:
            print(f"warning: {e}")
            return
        header_dict = {
            "Authorization": jwt
        }
        return header_dict


class Result(object):
    def __init__(self, payload, original, content_type):
        self.payload = payload
        self.original = original
        self.content_type = content_type

    def tojson(self):
        return json.loads(self.original)

    @property
    def predictions(self):
        if 'application/json' not in self.content_type:
            return None
        data = json.loads(self.original)
        if type(data) == dict:
            return data['predictions']
        else:
            for item in data:
                if 'visualization' in item:
                    del item['visualization']
        return data

    @property
    def visualization(self):
        data = json.loads(self.original)
        if 'application/json' not in self.content_type:
            return None
        if type(data) == dict:
            return data['visualization']
        else:
            visualization_list = [item["visualization"] for item in data]
            return visualization_list

    def save_base64_images(self, output_dir=None):
        output_file_list = []
        visualization = self.visualization
        if not visualization:
            return visualization

        input_files = self.payload['files']
        if len(input_files) != len(visualization):
            raise ValueError('input files length is not match output visualization length')

        if output_dir is not None:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = os.getcwd()

        for i, item in enumerate(visualization):
            image_data_arr = item.split(',')
            if len(image_data_arr) == 2:
                image_data = image_data_arr[1]
            else:
                image_data = image_data_arr[0]
            base_name = os.path.basename(input_files[i][1][0])
            file_name_without_extension, extension = os.path.splitext(base_name)
            filename = f"{file_name_without_extension}_visual_{generate_unique_id(6)}{extension}"
            file_path = os.path.join(output_dir, filename)

            image_bytes = base64.b64decode(image_data)

            with open(file_path, "wb") as file:
                file.write(image_bytes)
            output_file_list.append(file_path)
        return output_file_list


