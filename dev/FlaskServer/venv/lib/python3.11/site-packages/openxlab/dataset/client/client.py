from openxlab.dataset.client.api import XlabDatasetAPI


class Client:
    def __init__(self, host:str, odl_cookie:str):
        self.host = host
        self.odl_cookie = odl_cookie
        self.odl_api = None
        
    def get_api(self):
        self.odl_api = XlabDatasetAPI(host=self.host, cookie=self.odl_cookie)
        return self.odl_api