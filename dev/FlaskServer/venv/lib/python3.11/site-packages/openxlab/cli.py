from argparse import ArgumentParser
from argparse import Namespace
import inspect
import logging
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

import openxlab
from openxlab.dataset import Dataset
from openxlab.demo_cmd import Demo
from openxlab.model.commands import Model
from openxlab.types.command_type import BaseCommand
from openxlab.xlab import Config
from openxlab.xlab import Version
from openxlab.xlab.commands.login_command import Login
from openxlab.xlab.commands.token_command import Token
from openxlab.xlab.handler.user_token import get_token


# 定义一级子命令
class AllCommand(BaseCommand):
    sub_command_list = [Version, Demo, Config, Dataset, Model, Login, Token]

    def take_action(self, parsed_args: Namespace) -> int:
        return 0


# 递归添加子命令
def _add_sub_commands_recur(
        main_parser: ArgumentParser, parent_parser: ArgumentParser, command_type: BaseCommand
) -> Dict[str, ArgumentParser]:
    subparsers = main_parser.add_subparsers()

    sub_commands = command_type.sub_command_list
    for command_type in sub_commands:
        command = command_type()
        command_name = command.get_name()

        subparser = subparsers.add_parser(
            command_name, parents=[parent_parser], help=inspect.getdoc(command_type)
        )
        command.add_arguments(subparser)

        # 通过是否实现 take_action 判定命令的默认行为
        if issubclass(command_type, BaseCommand) and getattr(BaseCommand, "take_action") is not getattr(command_type,
                                                                                                        "take_action"):
            subparser.set_defaults(handler=command.take_action)
        else:
            def _print_help(args: Namespace) -> None:
                subparser.print_help()

            subparser.set_defaults(handler=_print_help)

        # 递归添加子命令
        _add_sub_commands_recur(subparser, parent_parser, command_type)

    # 添加默认的 help 命令
    def _print_help(args: Namespace) -> None:
        main_parser.print_help()

    subparsers.add_parser("help", help="Show help message and exit.").set_defaults(
        handler=_print_help
    )
    return


def _get_parser(description: str = "") -> ArgumentParser:
    parent_parser = ArgumentParser(add_help=False)

    main_parser = ArgumentParser(description=description, parents=[parent_parser])

    _add_sub_commands_recur(main_parser, parent_parser, AllCommand)

    return main_parser


def _preprocess_argv(argv: List[str]) -> List[str]:
    # Some preprocess is necessary for argv because some subcommand includes space
    # (e.g. optuna study optimize, optuna storage upgrade, ...).
    argv = argv[1:] if len(argv) > 1 else ["help"]

    # No subcommand is found.
    return argv


def main():
    main_parser = _get_parser()
    argv = sys.argv
    preprocessed_argv = _preprocess_argv(argv)
    args = main_parser.parse_args(preprocessed_argv)

    logger = logging.getLogger("openxlab")
    try:
        return args.handler(args)
    except Exception as e:
        logger.exception(e)
        # if args.debug:
        #     logger.exception(e)
        # else:
        #     logger.error(e)
        #     # This code is required to show help for each subcommand.
        #     # NOTE: the first element of `preprocessed_argv` is command name.
        #     command_name_to_subparser[preprocessed_argv[0]].print_help()
        return 1


if __name__ == "__main__":
    main()
