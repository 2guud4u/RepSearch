""" 
delete dataset repository for user
"""
from rich import print as rprint

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.types.command_type import *


def dataset_remove_repo(dataset_repo_name: str):
    ctx = ContextInfo()
    client = ctx.get_client()
    parsed_ds_name = dataset_repo_name.replace("/", ",")
    rprint(f"Removing dataset repository [red]{dataset_repo_name}[/red]...")
    client.get_api().delete_repo(parsed_ds_name)
    rprint(f"Dataset repository [blue]{dataset_repo_name}[/blue] removed successfully!")
