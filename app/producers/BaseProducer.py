# !/usr/bin/env python
# -*- coding: utf-8 -*-

from app.BaseJob import BaseJob
import schedule


class BaseProducer(BaseJob):
    every = 1 * 60 * 60 * 24

    def __init__(self):
        BaseJob.__init__(self)
        schedule.every(self.every).seconds.do(self.start)

    def start(self):
        pass
