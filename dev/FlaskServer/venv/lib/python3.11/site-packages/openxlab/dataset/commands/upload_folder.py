from openxlab.dataset.handler.upload_dataset_folder import dataset_upload_folder
from openxlab.types.command_type import *


class UploadFolder(BaseCommand):
    """Upload resources from local to remote"""

    def get_name(self) -> str:
        return "upload-folder"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset-repo-name",
            # "-n",
            # type=str,
            # required=True,
            help=("The dataset repo you want upload files."),
        )
        parser.add_argument(
            "--source-path",
            "-s",
            type=str,
            required=True,
            help=("The path of the file you want to upload."),
        )
        parser.add_argument(
            "--destination-path",
            "-d",
            type=str,
            # required=True,
            help=("The target path you want upload files."),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_upload_folder(
            dataset_repo_name=parsed_args.dataset_repo_name,
            source_path=parsed_args.source_path,
            destination_path=parsed_args.destination_path,
        )

        return 0
