# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent
from decouple import config
from utils.Logger import Logger
import proxies


class Proxy:
    """代理"""
    proxy_engine = config('PROXY_ENGINE', '')
    proxy = None
    proxy_class = None

    def __init__(self):
        self.proxy_class = self.__init_proxy_class()
        if self.proxy_class:
            self.proxy = {
                'http': self.proxy_class.proxy_ip,
                'https': self.proxy_class.proxy_ip
            }

        Logger().debug(self.proxy)

    def __init_proxy_class(self):
        for proxy_class in proxies.proxies:
            if proxy_class.proxy_engine == self.proxy_engine:
                return proxy_class()

        return None


class Http:
    """简单封装"""
    http = None
    headers = dict()

    def __init__(self, is_proxy=True):
        # self.headers['user-agent'] = UserAgent(verify_ssl=False).random
        self.headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
                                     '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        self.http = requests.session()
        self.http.headers = self.headers
        if is_proxy:
            self.http.proxies = Proxy().proxy

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


if __name__ == '__main__':
    re = Http().get('https://www.amazon.com')
    print(re.text)
