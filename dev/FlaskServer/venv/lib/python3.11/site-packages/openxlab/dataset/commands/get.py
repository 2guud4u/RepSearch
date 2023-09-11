from openxlab.dataset.handler.get_dataset_repository import dataset_get
from openxlab.types.command_type import *


class Get(BaseCommand):
    """Get a whole dataset"""

    def get_name(self) -> str:
        return "get"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset-repo-name",
            type=str,
        )
        parser.add_argument(
            "--destination-path",
            "-d",
            type=str,
            # required = True
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_get(parsed_args.dataset_repo_name, parsed_args.destination_path)

        return 0
