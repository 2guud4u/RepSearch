"""
setting model repository visibility-cli
"""
from openxlab.types.command_type import *
from openxlab.model import visibility


class Visibility(BaseCommand):
    """visibility"""

    def get_name(self) -> str:
        return "visibility"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-r', '--model-repo', required=True,
                            help='model repository address. format:username/repository.')
        parser.add_argument('-prt', '--private', type=bool, default=False, required=False,
                            help='set repository visibility.')

    def take_action(self, parsed_args: Namespace) -> int:
        private = False
        visibility(parsed_args.model_repo, private)
        return 0
