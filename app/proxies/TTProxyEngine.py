# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/19 5:11 下午 
# @Author : wangHua
# @File : TTProxyEngine.py 
# @Software: PyCharm

from app.proxies.BaseProxy import BaseProxy
from decouple import config
import hashlib
import requests
import time
from utils.Logger import Logger
import copy


class TTProxy(BaseProxy):
    """
    仅海外可用
    https://ttproxy.com/
    """
    proxy_engine = 'tt_proxy'
    secret = config('PROXY_SECRET', '')
    key = config('PROXY_KEY', '')
    get_every_request = True

    def __init__(self):
        if not self.secret or not self.key:
            Logger().warning('ttproxy 配置异常')
        else:
            self.params = self.__get_params()
            BaseProxy.__init__(self)

    def get_proxy(self):
        try:
            response = requests.get(
                url="https://api.ttproxy.com/v1/obtain",
                params=self.params,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                },
                data="1"
            )

            proxy_ip = response.json().get('data', {}).get('proxies')[0]
            return {
                'http': 'http://{}'.format(proxy_ip),
                'https': 'http://{}'.format(proxy_ip)
            }

        except:
            Logger().warning('ttproxy代理获取失败')
            return None

    def get_white_list(self):
        try:
            params = {
                "license": self.key,
                "time": int(time.time()),
            }
            params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + self.secret).encode('utf-8')). \
                hexdigest()

            response = requests.get(
                url="https://api.ttproxy.com/v1/whitelist/query",
                params=self.params,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                },
                data="1"
            )

            Logger().info(response.json())
        except:
            pass

    def add_white_list(self, ip):
        try:
            params = copy.deepcopy(self.params)
            params['ip'] = ip
            response = requests.get(
                url="https://api.ttproxy.com/v1/whitelist/add",
                params=params,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                },
                data="1"
            )

            Logger().info(response.json())
        except:
            pass

    def __get_params(self):
        params = {
            "license": self.key,
            "time": int(time.time()),
        }
        params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + self.secret).encode('utf-8')). \
            hexdigest()

        return params


if __name__ == '__main__':
    # TTProxy().add_white_list('54.219.185.72')
    # TTProxy().get_white_list()
    print(TTProxy().proxy_ip)
