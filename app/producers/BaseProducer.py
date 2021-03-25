# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm
from abc import ABCMeta, abstractmethod

from app.BaseJob import BaseJob
import schedule


class BaseProducer(BaseJob, metaclass=ABCMeta):

    def __init__(self):
        BaseJob.__init__(self)
        self.schedule = schedule
        self._schedule()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _schedule(self):
        pass
