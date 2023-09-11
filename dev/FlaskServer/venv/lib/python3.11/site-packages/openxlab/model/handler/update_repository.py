"""
update repository
"""
import re

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token
from openxlab.model.common.bury import bury_data


@bury_data()
def visibility(model_repo, private) -> None:
    """
    update repository visibility private -> public
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        client.update_repository(repository, private)
        print(f"repository:{repository} visibility update to public successfully.")
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
