# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.producers import BaseProducer
from utils import Logger
from app.enums import RedisListKeyEnum, ProductTypeEnum
from app.repositories import ProductRepository, ProductTypeRepository
from app.entities import ProductReviewJobEntity as CurrentJobEntity
from progress.bar import Bar


class ProductReviewProducer(BaseProducer):

    def __init__(self):
        self.job_count = 0
        self.productRepository = ProductRepository()
        self.productTypeRepository = ProductTypeRepository()
        BaseProducer.__init__(self)

    def start(self):
        # 这边只会产出cpa、shop类型的产品，search类型的可以不抓取
        products = self.productRepository.getProductsByType([ProductTypeEnum.TYPE_ID_CPA])
        with Bar('product-review-producer...', max=len(products), fill='#', suffix='%(percent)d%%') as bar:
            for product in products:
                for product_item in product.product_items:
                    if product_item.site:
                        # 没有传对象，直接存了ID，取出任务后，需要使用id再获取到对象再操作,消费队列通过product_item_id获取，其他参数可有可无
                        entity = CurrentJobEntity.instance({
                            'product_id': product.id,
                            'product_asin': product.asin,
                            'site_id': product_item.site.id,
                            'product_item_id': product_item.id,
                            'page': 1
                        })
                        self.set_job(entity)
                        self.job_count += 1
                bar.next()

        Logger().info('product-review 开始投放任务,{}个产品, 共添加{}个任务'.format(len(products), self.job_count))

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_review_crawl_job

    def _schedule(self):
        # 每天凌晨执行任务
        self.schedule.every().day.at('00:00').do(self.start)
