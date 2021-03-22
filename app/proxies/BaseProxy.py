# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from utils.Logger import Logger


class BaseProxy(metaclass=ABCMeta):

    proxy_engine = ''

    get_every_request = False

    def __init__(self):
        Logger().info('启用代理插件：{}'.format(self.proxy_engine))

    @abstractmethod
    def get_proxy(self):
        pass
