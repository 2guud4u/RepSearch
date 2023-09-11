from argparse import ArgumentParser
from argparse import Namespace

from openxlab.dataset.handler.remove_dataset_repository import dataset_remove_repo
from openxlab.types.command_type import *


class Remove(BaseCommand):
    """ "Delete repository for user"""

    def get_name(self) -> str:
        return "remove"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--dataset-repo-name", help="The dataset repo you want to delete")

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_remove_repo(parsed_args.dataset_repo_name)

        return 0
