# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.producers import BaseProducer
from utils.Logger import Logger


class ProductReviewProducer(BaseProducer):
    every = 60   # 调度间隔，单位秒

    def __init__(self):
        BaseProducer.__init__(self)

    def start(self):
        Logger().debug(self.__class__)

    def set_job_key(self) -> str:
        return 'product_review_asin'
