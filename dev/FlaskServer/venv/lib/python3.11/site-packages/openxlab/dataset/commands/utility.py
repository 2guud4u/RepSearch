from distutils.command.config import config
from functools import wraps
import json
import sys
from typing import Any
from typing import Callable
from typing import TypeVar

import requests

from openxlab.dataset.client.client import Client
from openxlab.dataset.client.uaa import get_odl_token
from openxlab.dataset.commands.config import config as client_config
from openxlab.dataset.constants import endpoint
from openxlab.dataset.exception import *
from openxlab.dataset.exception import OpenDataLabError
from openxlab.xlab.handler.user_config import get_config


_Callable = TypeVar("_Callable", bound=Callable[..., None])


class ContextInfo:
    """This class contains command context."""

    def __init__(self):
        self.credent = get_config(need_force=True)
        self.ak = self.credent.ak
        self.sk = self.credent.sk
        self.url = endpoint
        self.config = client_config
        self.conf_file = client_config._get_config_filepath()
        self._conf_content = self.check_config()
        # print(self._conf_content)
        if "ssouid" not in self._conf_content:
            config_json = self.odl_auth()
            self.update_config(config_json)
            self._conf_content = self.check_config()
        odl_cookie = self._conf_content
        self.cookie = odl_cookie
        self.check_ret = 0

    def odl_auth(self):
        code, sso_uid = get_odl_token(self.ak, self.sk)
        data = {
            "code": code,
            "redirect": "",
        }
        data = json.dumps(data)

        resp = requests.post(
            f"{self.url}/datasets/api/v2/users/auth",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise OdlAuthError(resp.status_code, resp.text)

        odl_token = resp.json()["data"]["token"]
        config_json = {'opendatalab_session': odl_token, 'ssouid': sso_uid}
        return config_json

    def get_client(self) -> Client:
        return Client(host=self.url, odl_cookie=self.cookie)

    def get_content(self):
        return self._conf_content

    def set_content(self, content: dict) -> None:
        for key, value in content.items():
            self._conf_content[key] = value

            if key == 'user.token' and not content[key]:
                self.cookie = content[key]

    def get_config_content(self):
        try:
            with open(self.conf_file, 'r') as f:
                config_content = json.load(f)
        except json.decoder.JSONDecodeError:
            config_content = {}

        return config_content

    def check_config(self):
        res = self.get_config_content()
        if not res:
            init_config_dict = {
                'opendatalab_session': '',
            }
            result = init_config_dict
            with open(self.conf_file, 'w') as f:
                json.dump(init_config_dict, f, indent=4, sort_keys=True, separators=(',', ':'))
        else:
            result = res

        return result

    def update_config(self, content: dict) -> None:
        res = self.get_config_content()
        if res:
            self.set_content(content)
            with open(self.conf_file, 'w') as f:
                f.seek(0)
                json.dump(self._conf_content, f, indent=4, sort_keys=True, separators=(',', ':'))

    def clean_config(self):
        res = self.get_config_content()
        if not res:
            self.check_config()
        else:
            with open(self.conf_file, "w") as f:
                if 'user.token' in res.keys():
                    res['user.token'] = ''
                if 'user.email' in res.keys():
                    res['user.email'] = ''
                f.seek(0)
                json.dump(res, f, indent=4, sort_keys=True, separators=(',', ':'))

        return res


def exception_handler(func: _Callable) -> _Callable:
    """Decorator for CLI functions to catch custom exceptions.

    Arguments:
        func: The CLI function needs to be decorated.

    Returns:
        The CLI function with exception catching procedure.

    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            func(*args, **kwargs)
        except OpenDataLabError as err:
            if err.STATUS_CODE == 401:
                print(f"Error: authentication failure, please login!")
                pass
            elif err.STATUS_CODE == 403:
                print(f"Unable to access. Please visit the dataset homepage!")
                pass
            elif err.STATUS_CODE == 404:
                print(f"Data not exists!")
                pass
            elif err.STATUS_CODE == 412:
                print(f"Access with cdn error!")
                pass
            elif err.STATUS_CODE == 500:
                print(f"Internal server occurs!")
                pass
            else:
                print(f"Error occurs!!!")

            sys.exit(1)

    return wrapper  # type: ignore[return-value]
