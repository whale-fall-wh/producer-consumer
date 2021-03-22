# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:20 下午
# @Author : wangHua
# @Software: PyCharm

import requests
from decouple import config
from utils.Logger import Logger
from functools import wraps
from app import proxies as proxy_pgk
from app.proxies.BaseProxy import BaseProxy


class Proxy:
    """代理"""
    proxy_engine = config('PROXY_ENGINE', '')

    @staticmethod
    def get_proxy_engine(proxy_engine) -> [BaseProxy, None]:
        for proxy_class in proxy_pgk.proxies:
            if proxy_class.proxy_engine == proxy_engine:
                return proxy_class()

        return None

    @staticmethod
    def log_proxy(f):
        @wraps(f)
        def log(*k, **kw):
            r = f(*k, **kw)
            Logger().debug(r)

        return log


class ErrorHttp:
    def __init__(self):
        self.need_change_proxy = False
        self.continue_error_time = 0

    def error_time_increase(self):
        self.continue_error_time += 1
        if self.continue_error_time >= 3:
            self.need_change_proxy = True

    def init_error_info(self):
        self.continue_error_time = 0
        self.need_change_proxy = False


class Http(ErrorHttp):
    """简单封装"""
    default_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    def __init__(self, use_proxy: bool = True, is_http2: bool = False):
        ErrorHttp.__init__(self)
        self.is_http2 = is_http2
        self.http = requests.session()
        self.http.headers = self.default_header
        self.use_proxy = use_proxy
        self.proxy_engine = Proxy.get_proxy_engine(Proxy.proxy_engine)
        self.set_proxy()

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=(10, 20), allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):

        self.auto_change_proxy()
        return self.http.request(method, url,
                                 params, data, headers, cookies, files,
                                 auth, timeout, allow_redirects, proxies,
                                 hooks, stream, verify, cert, json)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.http, key)(*args, **kwargs)

        return not_find

    @Proxy.log_proxy
    def auto_change_proxy(self):
        if self.proxy_engine and self.proxy_engine.get_every_request:
            self.http.proxies = self.proxy_engine.get_proxy()

        return self.http.proxies

    @Proxy.log_proxy
    def set_proxy(self):
        if self.use_proxy and self.proxy_engine:
            self.http.proxies = self.proxy_engine.get_proxy()

        return self.http.proxies

    def set_headers(self, headers: dict):
        self.http.headers = headers

    def add_header(self, key: str, value: str):
        self.http.headers[key] = value


if __name__ == '__main__':
    try:
        re = Http().request("GET", 'https://www.amazon.com')
        print(re.text)
    except requests.exceptions.RequestException:
        print(111)
