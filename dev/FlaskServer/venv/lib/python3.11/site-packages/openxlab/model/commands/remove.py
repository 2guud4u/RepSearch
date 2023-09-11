"""
remove repository
"""
from openxlab.types.command_type import *
from openxlab.model import remove


class Remove(BaseCommand):
    """Remove the model repository."""

    def get_name(self) -> str:
        return "remove"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.usage = 'openxlab model remove [-h] -r MODEL_REPO {help} ...\n' \
                       'Example:\n' \
                       '> openxlab model remove --model-repo=username/model_repo_name'
        parser.add_argument('-r', '--model-repo', required=True,
                            help='The name of model repository.[required]')

    def take_action(self, parsed_args: Namespace) -> int:
        remove(parsed_args.model_repo)
        return 0
