""" 
upload local folder to dataset repository
"""
from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.io.upload import Uploader


def dataset_upload_folder(dataset_repo_name: str, source_path: str, destination_path=""):
    ctx = ContextInfo()
    client = ctx.get_client().get_api()
    uploader = Uploader(client, dataset_repo_name)
    uploader.upload_folder(source_path, destination_path)
