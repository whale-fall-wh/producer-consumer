# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm
from abc import ABCMeta, abstractmethod

from app.BaseJob import BaseJob
import schedule


class BaseProducer(BaseJob, metaclass=ABCMeta):
    every = 1 * 60 * 60 * 24

    def __init__(self):
        BaseJob.__init__(self)
        schedule.every(self.every).seconds.do(self.start)

    @abstractmethod
    def start(self):
        pass
