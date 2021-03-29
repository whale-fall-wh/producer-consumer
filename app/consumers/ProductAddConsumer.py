# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/26 1:57 下午 
# @Author : wangHua
# @File : ProductAddConsumer.py 
# @Software: PyCharm

from app.consumers import BaseConsumer
from utils import Logger, Http
from app.proxies import get_proxy_engine
from app.exceptions import NotFoundException, CrawlErrorException
from app.enums import RedisListKeyEnum
from app.entities import ProductJobEntity, ProductAddJobEntity
from app.crawlers import ProductAddCrawler
import common


class ProductAddConsumer(BaseConsumer):
    """
    添加新的asin时，插入对应的任务，该消费者会判断某个站点中的产品是否存在，如果存在，则添加对应站点的asin数据，并产生新的任务
    """
    # ignore = True     # 忽略该消费者
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
        self.http = None
        self.proxy_engine = None
        BaseConsumer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_add_crawl_job

    def run_job(self):
        Logger().info('product_add_consumer start')
        self.http = Http()
        self.proxy_engine = get_proxy_engine()
        self.http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                job_entity = ProductAddJobEntity.instance(job_dict)
                try:
                    if self.proxy_engine:
                        self.http.set_proxy(self.proxy_engine.get_proxy())
                    crawler = ProductAddCrawler(job_entity, self.http)
                    if crawler.productItem:
                        job_dict['product_item_id'] = crawler.productItem.id
                        new_job = ProductJobEntity.instance(job_dict)
                        self.set_job_by_key(RedisListKeyEnum.product_crawl_job, new_job)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(job_entity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                common.sleep_random()
