from rich import print as rprint

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.handler.create_dataset_repository import dataset_create_repo
from openxlab.types.command_type import *


class Create(BaseCommand):
    """Create a dataset repo"""

    def get_name(self) -> str:
        return "create"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset-repo-name",
            # "-n",
            # required=True,
            help=('Desired dataset name'),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_create_repo(parsed_args.dataset_repo_name)

        return 0
