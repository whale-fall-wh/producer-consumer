# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 10:08 上午 
# @Author : wangHua
# @File : LocalProxyEngine.py
# @Software: PyCharm

from app.proxies.BaseProxy import BaseProxy


class LocalProxyEngine(BaseProxy):
    proxy_engine = 'local_proxy'

    def get_proxy_ip(self):
        return 'socks5://localhost:1080'
