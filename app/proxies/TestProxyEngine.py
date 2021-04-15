# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 10:08 上午 
# @Author : wangHua
# @File : TestProxyEngine.py 
# @Software: PyCharm

from app.proxies.BaseProxy import BaseProxy


class TestProxyEngine(BaseProxy):
    proxy_engine = 'test_proxy'

    def get_proxy_ip(self):
        return 'http://localhost:1081'
