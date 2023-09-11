from openxlab.types.command_type import *
from openxlab.model.commands.download import Download
from openxlab.model.commands.wget import Wget
from openxlab.model.commands.upload import Upload
from openxlab.model.commands.init import Init
from openxlab.model.commands.create import Create
from openxlab.model.commands.list import List
from openxlab.model.commands.visibility import Visibility
from openxlab.model.commands.remove import Remove
from openxlab.model.commands.inference import Inference


class Model(BaseCommand):
    """model"""

    sub_command_list = [Upload, Download, Init, Create, List, Visibility, Remove, Inference, Wget]

    def get_name(self) -> str:
        return "model"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--foo",
            type=str,
            help=(
                "this is an argument for test"
            ),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        pass
