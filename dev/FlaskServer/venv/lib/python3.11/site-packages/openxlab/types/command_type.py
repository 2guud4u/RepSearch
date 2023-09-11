from argparse import ArgumentParser
from argparse import Namespace
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union


class BaseCommand:
    """Base class for commands.
    """
    sub_command_list = []

    def __init__(self) -> None:
        pass
        
    def get_name():
        """define command name"""
        pass
        
    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments required for each command.

        Args:
            parser:
                `ArgumentParser` object to add arguments
        """
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        """Define action if the command is called.

        Args:
            parsed_args:
                `Namespace` object including arguments specified by user.

        Returns:
            Running status of the action.
            0 if this method finishes normally, otherwise 1.
        """

        raise NotImplementedError