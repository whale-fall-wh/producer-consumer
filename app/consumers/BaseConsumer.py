# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import threading
from app.BaseJob import BaseJob
from abc import ABCMeta, abstractmethod
from utils import Logger


class BaseConsumer(threading.Thread, BaseJob, metaclass=ABCMeta):
    # 多线程抓取
    threading_num = 1

    def __init__(self):
        BaseJob.__init__(self)
        threading.Thread.__init__(self)

    @abstractmethod
    def run_job(self):
        pass

    def run(self):
        Logger().debug('{} 开启 {} 个线程'.format(self.__class__.__name__, self.threading_num))
        for i in range(self.threading_num):
            t = threading.Thread(target=self.run_job)
            t.start()
