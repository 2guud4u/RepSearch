import hashlib
import io
import multiprocessing
import os
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from urllib.parse import urljoin

import requests
from rich import print as rprint
from tqdm import tqdm

from openxlab.dataset.utility.concurrency import concurrent_submit
from openxlab.types.command_type import *


# buf_size = 128 kb chunksize
def calculate_file_sha256(file_path: str, buf_size: int = 131072):
    if not Path(file_path).is_file():
        raise Exception(f"file {file_path} does not exist")
    sha256_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha256_obj.update(data)

    return sha256_obj.hexdigest()


class FileInfo:
    def __init__(self, client, abs_path: str, rel_path: Optional[str] = None):
        self.abs_path = abs_path
        self.rel_path = rel_path
        self.sha256: Optional[str] = None
        self.size: Optional[int] = None
        self.pre_upload: Optional[Dict] = None
        self.upload_process: Optional[List[Dict]] = []
        self.dataset: Optional[str] = None
        self.branch: Optional[str] = None
        self.sink_path: Optional[str] = None
        self.upload_id: Optional[str] = None
        self.client = client

    def get_size(self):
        self.size = os.stat(self.abs_path).st_size

    def get_pre_upload_info(self, dataset, branch, sink_path: Optional[str] = None):
        self.dataset = dataset
        self.branch = branch

        if self.size is None:
            self.get_size()
        if self.sha256 is None:
            self.sha256 = calculate_file_sha256(self.abs_path)
        if self.rel_path is None:
            self.rel_path = os.path.split(self.abs_path)[-1]

        if self.sink_path is None:
            self.sink_path = self.rel_path if sink_path is None else sink_path
        req_dict = {"size": self.size, "sha256": self.sha256}
        self.pre_upload = self.client.pre_object_upload(
            self.dataset, self.branch, self.sink_path, req_dict
        )
        if not self.pre_upload["exists"]:
            self.upload_id = self.pre_upload["id"]

    def put_part(self, part_number: int):
        if self.upload_id is None:
            raise Exception(f"no upload id info")

        part_number_list = [part["number"] for part in self.pre_upload["parts"]]
        if part_number not in part_number_list:
            raise Exception(f"the part number does not exist")

        part = [part for part in self.pre_upload["parts"] if part["number"] == part_number][0]
        part_put_url = part["putUrl"]
        part_size = self.pre_upload["partSize"]
        if part["number"] == 0:
            data = Path(self.abs_path).open("rb")
        else:
            offset = (part_number - 1) * part_size
            read_size = min(self.size - offset, part_size)
            with open(self.abs_path, "rb") as f:
                f.seek(offset)
                data = io.BufferedReader(io.BytesIO(f.read(read_size)))

        put_resp = requests.put(url=part_put_url, data=data)
        data.close()

        if put_resp.status_code != 200:
            raise Exception(
                f"put failed, status_code = {put_resp.status_code}, text = {put_resp.text}"
            )
        etag = put_resp.headers['Etag']
        part_submit_dict = {"number": part_number, "etag": etag}
        self.upload_process.append(part_submit_dict)

    def get_post_upload_info(self):
        if not self.upload_process or len(self.upload_process) != len(self.pre_upload["parts"]):
            raise Exception("no upload task or upload does not finish")

        post_req = {"id": self.upload_id, "parts": self.upload_process}
        post_resp = self.client.post_object_upload(
            self.dataset, self.branch, self.sink_path, post_req
        )
        if post_resp["sha256"] != self.sha256:
            raise Exception(f"file sha256 mismatch!")


def put_file_part(file: FileInfo, part_number: int):
    if file.upload_id is None:
        raise Exception(f"no upload id info")

    part_number_list = [part["number"] for part in file.pre_upload["parts"]]
    if part_number not in part_number_list:
        raise Exception(f"the part number does not exist")

    part = [part for part in file.pre_upload["parts"] if part["number"] == part_number][0]
    part_put_url = part["putUrl"]
    part_size = file.pre_upload["partSize"]
    if part["number"] == 0:
        data = Path(file.abs_path).open("rb")
    else:
        offset = (part_number - 1) * part_size
        read_size = min(file.size - offset, part_size)
        with open(file.abs_path, "rb") as f:
            f.seek(offset)
            data = io.BufferedReader(io.BytesIO(f.read(read_size)))

    put_resp = requests.put(url=part_put_url, data=data)
    data.close()

    if put_resp.status_code != 200:
        raise Exception(
            f"put failed, status_code = {put_resp.status_code}, text = {put_resp.text}"
        )
    etag = put_resp.headers['Etag']
    part_submit_dict = {"number": part_number, "etag": etag}
    file.upload_process.append(part_submit_dict)


def _get_files_in_folder(client, folde_path: str, mts: bool = False) -> List[FileInfo]:
    if not Path(folde_path).is_dir():
        raise Exception(f"path {folde_path} is not a dir or does not exist")
    root_path = os.path.abspath(folde_path)
    res_list = multiprocessing.Manager().list() if mts else []
    for root, _, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_path).replace("\\", "/")
            file_obj = FileInfo(client, file_path, rel_path)
            file_obj.get_size()
            res_list.append(file_obj)
    return res_list


def update_progress(update_value: int, progress: Optional[tqdm] = None):
    if progress:
        progress.update(update_value)


def upload_files_worker(
    task_list: List[Tuple[FileInfo, int, int]], progress: Optional[tqdm] = None
):
    while len(task_list) > 0:
        task = task_list.pop(0)
        file = task[0]
        part_number = task[1]
        part_size = task[2]
        if file.upload_id is None:
            update_progress(file.size, progress)
        else:
            # put_file_part(file, part_number)
            file.put_part(part_number)
            if len(file.pre_upload["parts"]) == len(file.upload_process):
                file.get_post_upload_info()
            update_progress(part_size, progress)


def upload_files(
    task_list: List[Tuple[FileInfo, int, int]], progress: Optional[tqdm] = None, workers: int = 8
):
    concurrent_submit(upload_files_worker, workers, task_list, progress)


def files_to_tasks(
    file_list: List[FileInfo],
    task_list: List[Tuple[FileInfo, int, int]],
    dataset: str,
    branch: str,
    progress: Optional[tqdm] = None,
):
    while len(file_list) > 0:
        file = file_list.pop(0)
        file.get_pre_upload_info(dataset, branch)

        if file.upload_id:
            if len(file.pre_upload["parts"]) == 1:
                task = (file, 0, file.size)
                task_list.append(task)
            else:
                for part in file.pre_upload["parts"]:
                    part_number = part["number"]
                    size = min(
                        file.pre_upload["partSize"],
                        file.size - (part_number - 1) * file.pre_upload["partSize"],
                    )
                    task_list.append((file, part_number, size))
        else:
            task = (file, 0, 0)
            task_list.append(task)
        update_progress(1, progress)


def get_task_list(
    file_list: List[FileInfo],
    dataset: str,
    branch: str,
    progress: Optional[tqdm] = None,
    workers: int = 8,
):
    task_list = []
    concurrent_submit(files_to_tasks, workers, file_list, task_list, dataset, branch, progress)
    return task_list


# 获取dataset id的方法，此处先做测试
def get_dataset_id(client, dataset_repo_name: str):
    dataset_id = str(client.get_dataset_info(dataset_repo_name)["id"])
    return dataset_id


class Uploader:
    def __init__(self, client, dataset_repo_name: str):
        self.dataset = get_dataset_id(client, dataset_repo_name)
        self.branch = "main"  # TODO default to main this version
        self.buffer_size = 128 * 1024  # 128 kb
        self.workers = 8
        self.client = client

    def upload_folder(self, source_path: str, destination_path: str):
        if not destination_path:
            destination_path = "/"

        if not destination_path.endswith("/"):
            destination_path = destination_path + "/"
        file_list = _get_files_in_folder(self.client, source_path)
        for file in file_list:
            file.sink_path = urljoin(destination_path, file.rel_path)

        total_num = len(file_list)
        total_size = sum([file.size for file in file_list])

        with tqdm(total=total_num, ncols=100, desc="Preparing", unit_scale=True) as progress:
            task_list = get_task_list(file_list, self.dataset, self.branch, progress, self.workers)

        with tqdm(total=total_size, ncols=100, desc="Uploading", unit_scale=True) as progress:
            upload_files(task_list, progress, self.workers)
        # rprint("Upload folder successfully!")

    def upload_file(self, source_path: str, destination_path: str):
        if not os.path.isfile(source_path):
            raise Exception(f"{source_path} is not a file or does not exist!")
        if not destination_path:
            destination_path = "/"
        if not destination_path.endswith("/"):
            destination_path = destination_path + "/"

        file_obj = FileInfo(self.client, source_path)
        file_obj.get_size()
        file_obj.sink_path = urljoin(destination_path, os.path.split(source_path)[-1])
        print(urljoin(destination_path, os.path.split(source_path)[-1]))
        print("checking file info...")
        file_list = [file_obj]
        task_list = []

        total_size = file_obj.size
        files_to_tasks(file_list, task_list, self.dataset, self.branch)
        with tqdm(total=total_size, ncols=100, desc="Uploading", unit_scale=True) as progress:
            upload_files(task_list, progress, self.workers)

        # rprint("Upload file successfully!")
