from openxlab.dataset.handler.commit_dataset_info import dataset_commit
from openxlab.types.command_type import *


class Commit(BaseCommand):
    """Commit local changes"""

    def get_name(self) -> str:
        return "commit"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset-repo-name",
            type=str,
        )
        parser.add_argument("--commit-message", "-m", type=str, required=True)

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_commit(
            dataset_repo_name=parsed_args.dataset_repo_name, commit_name=parsed_args.commit_message
        )

        return 0
