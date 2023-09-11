""" 
create new dataset repository 
"""

from rich import print as rprint

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.types.command_type import *


def dataset_create_repo(dataset_repo_name: str):
    ctx = ContextInfo()
    client = ctx.get_client()

    req_data_dict = {"name": f"{dataset_repo_name}", "displayname": f"{dataset_repo_name}"}

    resp_data_dict = client.get_api().create_dataset(req=req_data_dict)

    rprint(f"Dataset named: [blue]{resp_data_dict['name']}[/blue] create success!")
