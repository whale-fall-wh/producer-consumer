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


class ShopConsumer(BaseConsumer):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                  ',application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

    def __init__(self):
        self.productItemRepository = ProductItemRepository()
        BaseConsumer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.shop_crawl_job

    def run_job(self):
        Logger().info('shop_consumer start')
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
