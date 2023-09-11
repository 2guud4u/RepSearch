from argparse import Namespace

from openxlab.types.command_type import BaseCommand
from openxlab.xlab.handler import user_token


class Token(BaseCommand):
    """Print token"""

    def get_name(self) -> str:
        return "token"

    def take_action(self, parsed_args: Namespace):
        print(user_token.get_jwt())
