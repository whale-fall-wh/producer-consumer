# !/usr/bin/env python
# -*- coding: utf-8 -*-

from producers.BaseProducer import BaseProducer
from utils.Logger import Logger


class ProductReviewProducer(BaseProducer):
    job_key = 'product_review_asin'  # 注意和消费者对应
    every = 60   # 调度间隔，单位秒

    def __init__(self):
        BaseProducer.__init__(self)

    def start(self):
        Logger().debug(self.__class__)
