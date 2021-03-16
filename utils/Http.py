# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:20 下午
# @Author : wangHua
# @Software: PyCharm

import requests
from decouple import config
from utils.Logger import Logger
from app import proxies as proxy_pgk


class Proxy:
    """代理"""
    proxy_engine = config('PROXY_ENGINE', '')

    def __init__(self):
        self.proxy_class = self.__init_proxy_class()
        if self.proxy_class and self.proxy_class.proxy_ip:
            self.proxy = {
                'http': self.proxy_class.proxy_ip,
                'https': self.proxy_class.proxy_ip
            }
            Logger().debug('已经获取到的代理: {}'.format(self.proxy.__str__()))
        else:
            self.proxy = None
            Logger().warning('未获取到的代理')

    def __init_proxy_class(self):
        for proxy_class in proxy_pgk.proxies:
            if proxy_class.proxy_engine == self.proxy_engine:
                return proxy_class()

        return None


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
    default_header = {}

    def __init__(self, use_proxy=True):
        ErrorHttp.__init__(self)
        self.http = requests.session()
        self.http.headers = self.default_header
        self.http.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' \
                                          ' (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        self.use_proxy = use_proxy
        self.set_proxy()

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=(10, 30), allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):

        return self.http.request(method, url,
                                 params, data, headers, cookies, files,
                                 auth, timeout, allow_redirects, proxies,
                                 hooks, stream, verify, cert, json)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.http, key)(*args, **kwargs)

        return not_find

    def set_proxy(self):
        if self.use_proxy:
            self.http.proxies = Proxy().proxy

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
