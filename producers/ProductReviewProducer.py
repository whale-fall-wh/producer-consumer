# !/usr/bin/env python
# -*- coding: utf-8 -*-

from producers.BaseProducer import BaseProducer
import schedule


class ProductReviewProducer(BaseProducer):
    job_key = 'product_review_asin'  # 注意和消费者对应

    def __init__(self):
        schedule.every(2).seconds.do(self.start)
        BaseProducer.__init__(self)

    def start(self):
        pass
