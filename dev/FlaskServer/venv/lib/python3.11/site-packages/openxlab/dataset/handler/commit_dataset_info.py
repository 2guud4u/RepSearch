""" 
commit message of change of dataset repository
"""
from openxlab.dataset.commands.utility import ContextInfo


def dataset_commit(dataset_repo_name: str, commit_name: str):
    ctx = ContextInfo()
    client = ctx.get_client()

    req_data_list = [f"{dataset_repo_name}", {"msg": f"{commit_name}"}]
    client.get_api().commit_dataset(req=req_data_list)
