# !/usr/bin/env python
# -*- coding: utf-8 -*-

from producers.BaseProducer import BaseProducer


class ProductProducer(BaseProducer):
    job_key = 'product_asin'    # 注意和消费者对应，可以抽出一个文件单独存放类
    every = 1*60             # 每隔秒数投放任务

    def __init__(self):
        BaseProducer.__init__(self)

    def start(self):
        # mysql 获取asin，并塞进redis队列
        asin_map = [
            'B01NAWKYZ0',
            'B07214SKYV',
            'B072JMFRKQ',
            'B078NLCPYW',
            'B07BWPNMCB',
            'B075DGQWZT',
            'B077JYGQZ1',
            'B071WPR3FC',
            'B07TWPMZFF',
            'B07TYPP711',
            'B085Q2NVN8',
            'B074PLWQY3',
            'B077JYR2M2'
        ]
        for asin_str in asin_map:
            self.set_job(asin_str)

