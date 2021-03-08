import requests
from utils.Proxy import Proxy
from utils.Header import Header


class Http:
    http = None

    def __init__(self):
        self.http = requests.session()
        self.http.headers = Header.get_header()
        # self.http.proxies = Proxy.get_proxy()

    def get(self, url, **kwargs):
        return self.http.get(url=url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.http.post(url=url, data=data, json=json, **kwargs)
