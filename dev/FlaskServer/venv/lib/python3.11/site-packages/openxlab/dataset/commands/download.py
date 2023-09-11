from openxlab.dataset.handler.download_dataset_repository import dataset_download
from openxlab.types.command_type import *


class Download(BaseCommand):
    """This command is designed to handle single file
    or subset download of a given dataset.

    """

    def get_name(self) -> str:
        return "download"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            # "--dataset_repo_name",
            # "-n",
            "--dataset-repo-name",
            type=str,
            # required=True,
            help=("The dataset repo you want to download file from."),
        )
        parser.add_argument(
            "--source-path",
            "-s",
            type=str,
            required=True,
            help=("The relative path of the file you want to download."),
        )
        parser.add_argument(
            "--destination-path",
            "-d",
            type=str,
            required=False,
            help=("The target path you want to store the file."),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_download(
            dataset_repo_name=parsed_args.dataset_repo_name,
            source_path=parsed_args.source_path,
            destination_path=parsed_args.destination_path,
        )

        return 0
