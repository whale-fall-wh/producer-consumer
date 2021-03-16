# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from app.entities.BaseEntity import BaseEntity


class BaseJobEntity(BaseEntity, metaclass=ABCMeta):
    def __init__(self):
        # 任务类型字段，后续可能设计一个队列中有多个不同的任务，就能简单实现任务优先级，这个字段用来区分不同任务
        self.job_type = self.set_job_type()
        self.retry_time = 0
        BaseEntity.__init__(self)

    @abstractmethod
    def set_job_type(self):
        pass
