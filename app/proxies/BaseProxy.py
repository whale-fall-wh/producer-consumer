# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from utils.Logger import Logger


class BaseProxy(metaclass=ABCMeta):

    proxy_engine = ''

    def __init__(self):
        Logger().info('启用代理插件：{}'.format(self.proxy_engine))
        self.proxy_ip = self.get_proxy()

    @abstractmethod
    def get_proxy(self):
        pass
