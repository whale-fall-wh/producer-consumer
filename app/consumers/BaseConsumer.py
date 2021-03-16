# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import threading
from app.BaseJob import BaseJob
from abc import ABCMeta


class BaseConsumer(threading.Thread, BaseJob, metaclass=ABCMeta):
    def __init__(self):
        BaseJob.__init__(self)
        threading.Thread.__init__(self)
