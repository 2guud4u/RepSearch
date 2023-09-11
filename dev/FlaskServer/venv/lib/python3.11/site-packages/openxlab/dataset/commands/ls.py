from openxlab.dataset.handler.list_dataset_repository import dataset_list
from openxlab.types.command_type import *


class Ls(BaseCommand):
    """List Dataset resources"""

    def get_name(self) -> str:
        return "ls"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--dataset-repo-name", type=str)

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_list(parsed_args.dataset_repo_name)
        return 0
