"""
model repository init-cli
"""
from openxlab.types.command_type import *
from openxlab.model.handler.download_file import download_metafile_template


class Init(BaseCommand):
    """Initialize the generated metafile.yaml file."""

    def get_name(self) -> str:
        return "init"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.usage = 'openxlab model init [OPTIONS]\n' \
                       'Example:\n' \
                       '> openxlab model init --path=\'/local/to/path\''
        parser.add_argument('-p', '--path',
                            help='The path where the generated files are stored.')

    def take_action(self, parsed_args: Namespace) -> int:
        download_metafile_template(parsed_args.path)
        return 0
