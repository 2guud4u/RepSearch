""" 
get the list of dataset repository
"""
from rich import box
from rich.console import Console
from rich.table import Table

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.exception import *
from openxlab.dataset.utils import bytes2human


def dataset_list(dataset_repo_name: str):
    ctx = ContextInfo()
    client = ctx.get_client()

    parsed_ds_name = dataset_repo_name.replace("/", ",")
    data_dict = client.get_api().get_dataset_files(dataset_name=parsed_ds_name)
    object_info_dict = {}
    total_size = 0
    for info in data_dict['list']:
        object_info_dict[info['path']] = bytes2human(info['size'])
        total_size += info['size']
    if len(object_info_dict) == 0:
        raise OdlAccessDeniedError()

    sorted_object_info_dict = dict(
        sorted(object_info_dict.items(), key=lambda x: x[0], reverse=True)
    )

    console = Console()
    table = Table(show_header=True, header_style='bold cyan', box=box.ASCII2)  # ROUNDED
    table.add_column("File Name", min_width=20, justify='left')
    table.add_column("Size", width=12, justify='left')

    print(f"Total Size: {bytes2human(total_size)}")
    for key, val in sorted_object_info_dict.items():
        table.add_row(key, val, end_section=True)
    console.print(table)

    return sorted_object_info_dict
