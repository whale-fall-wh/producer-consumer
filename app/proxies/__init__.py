# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from app.proxies.BaseProxy import BaseProxy
from decouple import config


proxies = LoadModules(__path__, BaseProxy).modules


def get_proxy_engine(proxy_engine=config('PROXY_ENGINE', '')) -> [BaseProxy, None]:
    """
    获取代理引擎
    :param proxy_engine: 通过传参数，可以设置想要使用的代理，放在队列中，并在合适的位置调用，可以动态的变更代理
    :return:
    """
    for proxy_class in proxies:
        if proxy_class.proxy_engine == proxy_engine:
            return proxy_class()

    return None
