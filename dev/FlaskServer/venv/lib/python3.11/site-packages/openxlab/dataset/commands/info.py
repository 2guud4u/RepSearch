from openxlab.dataset.handler.query_dataset_repository import dataset_info
from openxlab.types.command_type import *


class Info(BaseCommand):
    """Get info of a dataset"""

    def get_name(self) -> str:
        return "info"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset-repo-name",
            type=str,
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_info(parsed_args.dataset_repo_name)
