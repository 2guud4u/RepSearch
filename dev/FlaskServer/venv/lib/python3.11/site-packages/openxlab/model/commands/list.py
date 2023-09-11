"""
get model list of repository-cli
"""
from openxlab.types.command_type import *
from openxlab.model import list


class List(BaseCommand):
    """To view model information and model meta information under the model repository."""

    def get_name(self) -> str:
        return "list"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.usage = 'openxlab model list [-h] -r MODEL_REPO [-i METAFILE] {help} ...\n' \
                       'Example:\n' \
                       '> openxlab model list --model-repo=username/model_repo_name'
        parser.add_argument('-r', '--model-repo', required=True,
                            help='The name of model repository.[required]')
        parser.add_argument('-i', '--metafile', type=bool, required=False,
                            help='View model meta information, default is Fasle.')

    def take_action(self, parsed_args: Namespace) -> int:
        list(parsed_args.model_repo, parsed_args.metafile)
        return 0
