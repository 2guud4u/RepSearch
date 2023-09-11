"""
模型推理功能
"""

import base64
import os
import re
import json

import requests

from openxlab.model.clients.modelapi_client import ModelApiClient
from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token


class Inference:
    def __init__(self, model_repo):
        self.model_repo = model_repo
        # self.device = 'cpu' if device is None else 'gpu'

    def inference(self, input, **args):
        """
        model inference
        """
        try:
            # split params
            username, repository = _split_repo(self.model_repo)
            client = OpenapiClient(endpoint, token)

            model_repo_info = client.query_model_repo_info(username, repository)
            model_api_client = ModelApiClient(model_repo_info['inferUrl'], token)
            texts, files = _process_inputs(input)
            payload = {"files": files, "texts": texts}
            if args:
                payload["args"] = json.dumps(args)
            else:
                payload["args"] = None
            # print(f'payload ->{payload}')
            result = model_api_client.get_inference_result(payload)
            # print(f"inference result:{result}.")
            return result
        except ValueError as e:
            print(f"Error: {e}")
            return


def inference(model_repo, input, **args):
    model_infer = Inference(model_repo)
    return model_infer.inference(input, **args)


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


def _process_inputs(inputs):
    texts = []
    files = []
    if isinstance(inputs, list):
        inputs = inputs
    else:
        inputs = [inputs]
    for input_str in inputs:
        if input_str.startswith('http'):
            # if input is a URL
            response = requests.get(input_str)
            input_data = response.content
            files.append(input_data)
            # input_data = base64.b64encode(response.content).decode('utf-8')
        elif os.path.isfile(input_str):
            # if input is a file path
            filename = os.path.basename(input_str)
            files.append(("files", (filename, open(input_str, "rb"))))
            # input_data = base64.b64encode(file_data).decode('utf-8')
        else:
            # if input is just a string
            # input_data = input_str
            texts.append(input_str)
    return texts, files


