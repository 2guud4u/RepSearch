import json
import sys
from typing import Dict
from urllib.parse import quote

import requests

from openxlab.dataset.constants import computed_url
from openxlab.dataset.exception import *


class XlabDatasetAPI(object):
    """This class contains the interaction between client & odl serverend.

    This class is being instantiate from client.py
    Strongly recommend that openxlab provide a general method to handle contextinfo.

    """

    def __init__(self, host, cookie):
        self.host = host
        self.odl_cookie = cookie

    def get_dataset_files(self, dataset_name: str, payload: dict = None):
        header_dict = {"accept": "application/json"}
        data = {"recursive": True}

        if payload:
            data.update(payload)

        resp = requests.get(
            url=f"{self.host}/datasets/api/v2/datasets/{dataset_name}/r/main",
            params=data,
            headers=header_dict,
            cookies=self.odl_cookie,
        )

        if resp.status_code != 200:
            print(f"{OpenDataLabError(resp.status_code, resp.text)}")
            sys.exit(-1)
        result_dict = resp.json()['data']

        # no content
        if not result_dict['list']:
            print(
                f"{OpenDataLabError(404, 'path not found, please check download path and try again')}"
            )
            sys.exit(-1)
        return result_dict

    def get_dataset_download_urls(self, dataset_id: int, dataset_dict: Dict):
        resp = requests.get(
            url=f"{self.host}/datasets/resolve/{dataset_id}/main/{dataset_dict['name']}",
            headers={"accept": "application/json"},
            cookies=self.odl_cookie,
            allow_redirects=False,
        )
        if resp.status_code != 302:
            print(f"{OpenDataLabError(resp.status_code, resp.text)}")
            sys.exit(-1)
        return resp.headers['Location']

    def get_dataset_info(self, dataset_name: str):
        header_dict = {
            "accept": "application/json",
        }
        parsed_dataset_name = quote(dataset_name.replace("/", ","))
        resp = requests.get(
            url=f"{self.host}{computed_url}datasets/{parsed_dataset_name}",
            headers=header_dict,
            cookies=self.odl_cookie,
        )

        if resp.status_code != 200:
            print(f"{OpenDataLabError(resp.status_code, resp.text)}")
            sys.exit(-1)

        data = resp.json()['data']
        if data['id'] == 0:
            print(f"No dataset:{dataset_name}")
            sys.exit(-1)
        return data

    def pre_object_upload(self, dataset: str, branch: str, file_path: str, req: dict) -> dict:
        resp = requests.post(
            url=f"{self.host}{computed_url}preUpload/{dataset}/{branch}{file_path}",
            data=json.dumps(req),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
            cookies=self.odl_cookie,
        )
        if resp.status_code != 200:
            print(f"{OpenDataLabError(resp.status_code, resp.text)}")
            sys.exit(-1)
        resp_json = resp.json()
        data = resp_json['data']
        return data

    def post_object_upload(self, dataset: str, branch: str, file_path: str, req: dict) -> dict:
        resp = requests.post(
            url=f"{self.host}{computed_url}postUpload/{dataset}/{branch}/{file_path}",
            data=json.dumps(req),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
            cookies=self.odl_cookie,
        )
        if resp.status_code != 200:
            print(f"{OpenDataLabError(resp.status_code, resp.text)}")
            sys.exit(-1)
        resp_json = resp.json()
        data = resp_json["data"]
        return data

    def create_dataset(self, req: dict):
        resp = requests.post(
            url=f"{self.host}/datasets/api/v2/datasets",
            data=json.dumps(req),
            headers={"Content-Type": "application/json", "accept": "application/json"},
            cookies=self.odl_cookie,
        )
        if resp.status_code != 200:
            print(f"While creating {req['name']} encounter error: {OpenDataLabError(resp.text)}")
            sys.exit(-1)
        resp_json = resp.json()
        data = resp_json['data']
        return data

    def commit_dataset(self, req: list):
        dataset_name = req[0]
        parsed_dataset_name = quote(dataset_name.replace("/", ","))

        resp = requests.post(
            url=f"{self.host}/datasets/api/v2/datasets/{parsed_dataset_name}/commit",
            data=json.dumps(req[1]),
            headers={"Content-Type": "application/json", "accept": "application/json"},
            cookies=self.odl_cookie,
        )

        if resp.status_code != 200:
            print(f"While committing {req[0]} encounter error: {OpenDataLabError(resp.text)}")
            sys.exit(-1)
        return

    def delete_repo(self, dataset_repo_name: str):
        """delete repo api"""
        resp = requests.delete(
            url=f"{self.host}{computed_url}datasets/{dataset_repo_name}",
            cookies=self.odl_cookie,
        )

        if resp.status_code != 200:
            print(
                f"While deleting {dataset_repo_name} encounter error: {OpenDataLabError(resp.text)}"
            )
            sys.exit(-1)
        return
