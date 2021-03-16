# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.producers import BaseProducer
from utils.Logger import Logger
from app.repositories.ProductRepository import ProductRepository
from app.entities.ProductJobEntity import ProductJobEntity
from app.enums.RedisListKeyEnum import RedisListKeyEnum


class ProductProducer(BaseProducer):
    every = 1*60             # 每隔秒数投放任务

    def __init__(self):
        self.job_count = 0
        self.productRepository = ProductRepository()
        BaseProducer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_crawl_job

    def start(self):
        products = self.productRepository.all()
        for product in products:
            for product_item in product.product_items:
                if product_item.site:
                    # 没有传对象，直接存了ID，取出任务后，需要使用id再获取到对象再操作
                    entity = ProductJobEntity.instance({
                        'product_id': product.id,
                        'product_asin': product.asin,
                        'site_id': product_item.site.id,
                        'product_item_id': product_item.id
                    })
                    self.set_job(entity)
                    self.job_count += 1
        Logger().info('product 开始投放任务, 本次添加{}个任务' .format(self.job_count))


if __name__ == '__main__':
    ProductProducer().start()
