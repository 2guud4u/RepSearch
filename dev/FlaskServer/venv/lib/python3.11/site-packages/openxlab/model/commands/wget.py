"""
download model file|meta file|log file|readme file-cli
"""
from openxlab.types.command_type import *
from openxlab.model import wget


class Wget(BaseCommand):
    """Download model weight files."""

    def get_name(self) -> str:
        return "wget"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.usage = "openxlab model wget [-h] -r MODEL_REPO -f FILE [-p PATH] [-o] {help} ...\n" \
                       'Example:\n' \
                       '> openxlab model wget --url={url}' \
                       '  --output=/path/to/local/folder/\n' \
                       '  --overwrite=True'
        parser.add_argument('-u', '--url', required=True,
                            help='model remote download url.')
        parser.add_argument('-op', '--output', required=False,
                            help='setting download path.')
        parser.add_argument('-o', '--overwrite', default=False, type=bool,
                            help='force overwriting local files.')

    def take_action(self, parsed_args: Namespace) -> int:
        wget(parsed_args.url, path=parsed_args.output, overwrite=parsed_args.overwrite)
        return 0
