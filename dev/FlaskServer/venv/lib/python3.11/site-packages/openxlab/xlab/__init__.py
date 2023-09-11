

from openxlab.config import version as config_version
from openxlab.types.command_type import *

from openxlab.xlab.commands.config_command import Config


class Version(BaseCommand):
    """Get Openxlab Version"""
    
    def get_name(self) -> str:
        return "version"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("OpenXLab %s" % config_version.version)
        return 0
    
