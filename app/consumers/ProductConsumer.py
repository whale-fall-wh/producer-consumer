# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm


from app.crawlers.ProductCrawler import ProductCrawler
from utils import Logger, Http
from app.proxies import get_proxy_engine
import common
from app.consumers import BaseConsumer
from app.exceptions import NotFoundException, CrawlErrorException
from app.enums import RedisListKeyEnum
from app.entities import ProductJobEntity
import requests


class ProductConsumer(BaseConsumer):
    """
    抓取产品信息
    """

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_crawl_job

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                job_entity = ProductJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        # product 反扒比较苛刻，这边用了随机IP的代理
                        http.set_proxy(proxy_engine.get_proxy())
                    ProductCrawler(job_entity, http)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(job_entity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                except requests.exceptions.ProxyError:
                    # 代理异常
                    Logger().error('代理异常')
                common.sleep_random()
