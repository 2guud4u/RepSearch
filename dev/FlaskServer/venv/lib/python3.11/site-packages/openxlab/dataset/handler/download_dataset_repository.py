""" 
download specific file/files according to source_path(single file/relative path) of dataset repository
"""
import os

from tqdm import tqdm

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.constants import FILE_THRESHOLD
from openxlab.dataset.io import downloader


def dataset_download(dataset_repo_name: str, source_path: str, destination_path=""):
    if not destination_path:
        destination_path = os.getcwd()

    ctx = ContextInfo()
    client = ctx.get_client()

    # parse dataset_name
    parsed_ds_name = dataset_repo_name.replace("/", ",")
    # huggingface use underscores when loading/downloading datasets
    parsed_save_path = dataset_repo_name.replace("/", "___")

    get_payload = {"prefix": source_path}
    data_dict = client.get_api().get_dataset_files(
        dataset_name=parsed_ds_name, payload=get_payload
    )
    info_dataset_id = data_dict['list'][0]['dataset_id']

    object_info_list = []
    for info in data_dict['list']:
        curr_dict = {}
        curr_dict['size'] = info['size']
        curr_dict['name'] = info['path'][1:]
        # without destination path upload file,file has prefix with '//'
        if info['path'].startswith('//'):
            curr_dict['name'] = info['path'][2:]
        object_info_list.append(curr_dict)

    with tqdm(total=len(object_info_list)) as pbar:
        for idx in range(len(object_info_list)):
            # exist already
            print(f" Downloading No.{idx+1} of total {len(object_info_list)} files")
            if os.path.exists(
                (os.path.join(destination_path, parsed_save_path, object_info_list[idx]['name']))
            ):
                print(f"target already exists, jumping to next !")
                pbar.update(1)
                continue

            # big file download
            if object_info_list[idx]['size'] > FILE_THRESHOLD:
                download_url = client.get_api().get_dataset_download_urls(
                    info_dataset_id, object_info_list[idx]
                )
                downloader.BigFileDownloader(
                    url=download_url,
                    filename=object_info_list[idx]['name'],
                    download_dir=os.path.join(destination_path, parsed_save_path),
                    file_size=object_info_list[idx]['size'],
                    blocks_num=1,
                ).start()
                pbar.update(1)

            # small file download
            else:
                download_url = client.get_api().get_dataset_download_urls(
                    info_dataset_id, object_info_list[idx]
                )
                downloader.SmallFileDownload(
                    url=download_url,
                    filename=object_info_list[idx]['name'],
                    download_dir=os.path.join(destination_path, parsed_save_path),
                )._single_thread_download()
                pbar.update(1)

    print(f"\nDownload Complete!")
