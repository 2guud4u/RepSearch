"""
upload model file|meta file|log file|readme file-cli
"""
from openxlab.types.command_type import *
from openxlab.model import upload


class Upload(BaseCommand):
    """Upload model-related files."""

    def get_name(self) -> str:
        return "upload"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.usage = 'openxlab model upload [-h] -r MODEL_REPO [-ft FILE_TYPE] -s SOURCE [-t TARGET] {help} ...\n' \
                       'Example:\n' \
                       '> openxlab model upload -r username/model_repo_name -s metafile.yaml'
        parser.add_argument('-r', '--model-repo', required=True,
                            help='The name of model repository.[required]')
        parser.add_argument('-ft', '--file-type', type=str, default='metafile', required=False,
                            help='Upload file type, metafile/other, default metafile.')
        parser.add_argument('-s', '--source', type=str, required=True,
                            help='The path of the file to be uploaded. [required]')
        parser.add_argument('-t', '--target', type=str, required=False,
                            help='The path where the uploaded file is stored or the name of the replaced file.')

    def take_action(self, parsed_args: Namespace) -> int:
        upload(parsed_args.model_repo, parsed_args.file_type, parsed_args.source, parsed_args.target)
        return 0
