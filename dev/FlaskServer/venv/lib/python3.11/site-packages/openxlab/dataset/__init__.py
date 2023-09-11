from openxlab.config import version as config_version
from openxlab.dataset.commands.commit import Commit
from openxlab.dataset.commands.create import Create
from openxlab.dataset.commands.download import Download

# from openxlab.dataset.commands.download import Download
from openxlab.dataset.commands.get import Get
from openxlab.dataset.commands.info import Info
from openxlab.dataset.commands.ls import Ls
from openxlab.dataset.commands.remove import Remove
from openxlab.dataset.commands.upload_file import UploadFile
from openxlab.dataset.commands.upload_folder import UploadFolder
from openxlab.dataset.handler.commit_dataset_info import dataset_commit
from openxlab.dataset.handler.create_dataset_repository import dataset_create_repo
from openxlab.dataset.handler.download_dataset_repository import dataset_download
from openxlab.dataset.handler.get_dataset_repository import dataset_get
from openxlab.dataset.handler.list_dataset_repository import dataset_list
from openxlab.dataset.handler.query_dataset_repository import dataset_info
from openxlab.dataset.handler.remove_dataset_repository import dataset_remove_repo
from openxlab.dataset.handler.upload_dataset_file import dataset_upload_file
from openxlab.dataset.handler.upload_dataset_folder import dataset_upload_folder
from openxlab.types.command_type import *


def help():
    print("help")


class Dataset(BaseCommand):
    """Dataset Demo"""

    sub_command_list = [
        Get,
        Create,
        UploadFile,
        UploadFolder,
        Info,
        Ls,
        Commit,
        Download,
        Remove,
    ]

    def get_name(self) -> str:
        return "dataset"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--test",
            help=(" This argument is a test argument"),
        )
