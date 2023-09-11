""" 
query to get the information of dataset repository
"""
from rich import box
from rich.console import Console
from rich.table import Table

from openxlab.dataset.commands.utility import ContextInfo


def dataset_info(dataset_repo_name: str):
    ctx = ContextInfo()
    client = ctx.get_client()

    info_data = client.get_api().get_dataset_info(dataset_name=dataset_repo_name)
    info_data_result = _reformat_info_data(info_data)
    console = Console()
    table = Table(show_header=True, header_style='bold cyan', box=box.ASCII2)
    table.add_column("Field", width=20, justify='full', overflow='fold')
    table.add_column("Content", width=120, justify='full', overflow='fold')

    for key in info_data_result.keys():
        val = info_data_result[key]
        val = "" if not val else val
        table.add_row(key, val, end_section=True)

    console.print(table)

    return info_data_result


def _format_types(info_data, type_name):
    types_str = ""
    if type_name in info_data['attrs'].keys():
        types_list = info_data['attrs'][type_name]
        if types_list and len(types_list) > 0:
            types_str = ", ".join([x['name']['en'] for x in types_list])

    return types_str


def _reformat_info_data(info_data):
    publisher_str = _format_types(info_data, 'publisher')
    media_types_str = _format_types(info_data, 'mediaTypes')
    label_types_str = _format_types(info_data, 'labelTypes')
    task_types_str = _format_types(info_data, 'taskTypes')
    if info_data['introduction']:
        data_introduction = info_data['introduction']['en']
    else:
        data_introduction = ""
    introduction_str = ""
    if data_introduction and len(data_introduction) > 0:
        introduction_str = data_introduction[:97] + '...'

    info_data_result = {
        'Name': info_data['name'],
        'Introduction': introduction_str,
        'Author': publisher_str,
        'Data Type': media_types_str,
        'Label Type': label_types_str,
        'Task Type': task_types_str,
    }

    return info_data_result
