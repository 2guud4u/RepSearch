"""
创建模型仓库
"""
import logging
import os
import re
from tqdm import tqdm
import requests

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token
from openxlab.model.common.meta_file_util import MetafileParser
from openxlab.model.common.bury import bury_data


@bury_data("create_model")
def create(model_repo, private=False) -> None:
    """
    create model repository
    usage: cli & sdk
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        # parse & check metafile.yml
        print("Current directory:", os.getcwd())

        meta_parser = MetafileParser("metafile.yaml")
        meta_data = meta_parser.parse_and_validate()
        client.create_repository(repository, private, meta_data)
        print(f"repository:{repository} created successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        return


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


def _parse_check():
    pass
