import getpass

from openxlab.types.command_type import *
from openxlab.xlab.handler.user_config import clear_dataset_json
from openxlab.xlab.handler.user_config import get_dataset_path
from openxlab.xlab.handler.user_login import login
from openxlab.xlab.handler.user_token import *


class Login(BaseCommand):
    """Login Openxlab"""

    def get_name(self) -> str:
        return "login"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-r', '--relogin', required=False,  action='store_true',
                            help='force relogin via new AK, SK')

    def take_action(self, parsed_args: Namespace):
        re_login = parsed_args.relogin
        if os.path.exists(get_config_path()) and re_login is False:
            print("AK and SK have been configured. You can use the --relogin parameter to force a re-login.")
            return
        print("openxlab: You can find your Access key & Secrete Key in your browser here: "
              "https://sso.openxlab.org.cn/usercenter?tab=secret")
        # clear dataset.json if re_login
        if os.path.exists(get_dataset_path()) and re_login is True:
            clear_dataset_json()
        ak = input("openxlab: Paste your Access Key here: ")
        sk = getpass.getpass("openxlab: Paste your Secrete Key here: ")
        login(ak, sk, re_login)




