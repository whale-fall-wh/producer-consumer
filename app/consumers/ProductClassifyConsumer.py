# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 4:39 下午 
# @Author : wangHua
# @File : ProductClassifyConsumer.py 
# @Software: PyCharm

import common
import requests
from app.exceptions import NotFoundException, CrawlErrorException
from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
from utils import Http, Logger
from app.proxies import get_proxy_engine
from app.entities import ProductClassifyJobEntity
from app.crawlers import ProductClassifyCrawler


class ProductClassifyConsumer(BaseConsumer):

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_classify_crawl_job

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                job_entity = ProductClassifyJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    ProductClassifyCrawler(job_entity, http)
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
