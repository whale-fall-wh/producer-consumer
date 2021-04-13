# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 10:36 上午 
# @Author : wangHua
# @File : ShopConsumer.py 
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
from utils import Logger, Http
from app.proxies import get_proxy_engine
from app.exceptions import NotFoundException, CrawlErrorException
import common
from app.entities import ShopJobEntity, ProductJobEntity, ProductReviewJobEntity
from app.crawlers import ShopCrawler
from app.repositories import ProductItemRepository
import requests


class ShopConsumer(BaseConsumer):

    def __init__(self):
        self.productItemRepository = ProductItemRepository()
        BaseConsumer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.shop_crawl_job

    def run_job(self):
        http = Http()
        http.set_headers(self.headers)
        proxy_engine = get_proxy_engine()
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = ShopJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawl = ShopCrawler(jobEntity, http)
                    if crawl.crawl_next_page:
                        jobEntity.page += 1
                        self.set_job(jobEntity)
                    else:
                        self.crawl_shop_product(jobEntity)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(jobEntity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                except requests.exceptions.ProxyError:
                    # 代理异常
                    Logger().error('代理异常')
                common.sleep_random()

    def crawl_shop_product(self, jobEntity: ShopJobEntity):
        productItems = self.productItemRepository.get_by_shop_item_id(jobEntity.shop_item_id)
        for productItem in productItems:
            if productItem.product and productItem.site:
                data = {
                    'product_asin': productItem.product.asin,
                    'product_id': productItem.product.id,
                    'site_id': productItem.site.id,
                    'site_name': productItem.site.name,
                    'product_item_id': productItem.id,
                }
                self.set_job_by_key(RedisListKeyEnum.product_crawl_job, ProductJobEntity.instance(data))
                self.set_job_by_key(RedisListKeyEnum.product_review_crawl_job, ProductReviewJobEntity.instance(data))
