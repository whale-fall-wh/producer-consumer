import requests
from fake_useragent import UserAgent
from decouple import config
from utils.Logger import Logger


class Proxy:
    proxy = None

    def __init__(self):
        proxy_type = config('PROXY_TYPE')
        if proxy_type == 'tps':     # 隧道代理，或者直接是代理服务器IP
            self.proxy = {
                'http': config('PROXY_SERVER_URL'),
                'https': config('PROXY_SERVER_URL')
            }
        Logger().debug(self.proxy)


class Http:
    http = None
    headers = dict()

    def __init__(self):
        # self.headers['user-agent'] = UserAgent(verify_ssl=False).random
        self.headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
                                     '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        self.http = requests.session()
        self.http.headers = self.headers
        # self.http.proxies = Proxy().proxy

    def get(self, url, **kwargs):
        return self.http.get(url=url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.http.post(url=url, data=data, json=json, **kwargs)

    def put(self, url, data, **kwargs):
        return self.http.put(url=url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.http.delete(url=url, **kwargs)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.http, key)(*args, **kwargs)
        return not_find

    def set_headers(self, headers: dict):
        self.headers = headers

    def add_header(self, key: str, value: str):
        self.headers[key] = value
