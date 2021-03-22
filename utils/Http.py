# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:20 下午
# @Author : wangHua
# @Software: PyCharm

import requests
from utils.Logger import Logger


class Http(object):
    """简单封装"""
    default_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    def __init__(self):
        self.http = requests.session()
        self.http.headers = self.default_header

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=(10, 20), allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):

        return self.http.request(method, url,
                                 params, data, headers, cookies, files,
                                 auth, timeout, allow_redirects, proxies,
                                 hooks, stream, verify, cert, json)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.http, key)(*args, **kwargs)

        return not_find

    def set_proxy(self, proxy=None):
        self.http.proxies = proxy
        Logger().debug(self.http.proxies)

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
