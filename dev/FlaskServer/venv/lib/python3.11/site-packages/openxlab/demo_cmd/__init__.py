from openxlab.config import version as config_version
from openxlab.types.command_type import *


def help():
    print("help")


class Upload(BaseCommand):
    """upload"""

    def get_name(self) -> str:
        return "upload"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("upload something")
        return 0


class Demo(BaseCommand):
    """demo"""

    sub_command_list = [Upload]

    def get_name(self) -> str:
        return "demo"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--directions",
            type=str,
            nargs="+",
            choices=("minimize", "maximize"),
            help=(
                "Directions of optimization, if there are multiple objectives."
                " This argument is deprecated. Please create a study in advance."
            ),
        )

    # def take_action(self, parsed_args: Namespace) -> int:
    #     help()
    #     return 0
