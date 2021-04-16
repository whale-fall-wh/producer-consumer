# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from app.entities.BaseEntity import BaseEntity


class BaseJobEntity(BaseEntity, metaclass=ABCMeta):
    def __init__(self):
        self.retry_time = 0
        BaseEntity.__init__(self)
