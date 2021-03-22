# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from app.proxies.BaseProxy import BaseProxy
from decouple import config


proxies = LoadModules(__path__, BaseProxy).modules


def get_proxy_engine(proxy_engine=config('PROXY_ENGINE', '')) -> [BaseProxy, None]:
    for proxy_class in proxies:
        if proxy_class.proxy_engine == proxy_engine:
            return proxy_class()

    return None
