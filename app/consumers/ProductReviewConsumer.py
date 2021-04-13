# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 1:11 下午 
# @Author : wangHua
# @File : ProductReviewConsumer.py 
# @Software: PyCharm

from app.consumers import BaseConsumer
from app.enums import RedisListKeyEnum
from utils import Logger, Http
from app.proxies import get_proxy_engine
from app.entities import ProductReviewJobEntity
import common
from app.exceptions import CrawlErrorException, NotFoundException
from app.crawlers import ProductReviewCrawler
import requests


class ProductReviewConsumer(BaseConsumer):
    """
    住区评论信息
    """
    threading_num = 1

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_review_crawl_job

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = ProductReviewJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawl = ProductReviewCrawler(jobEntity, http)
                    if crawl.crawl_next_page:
                        jobEntity.page += 1
                        self.set_job(jobEntity)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(jobEntity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                except requests.exceptions.ProxyError:
                    # 代理异常
                    Logger().error('代理异常')
                except Exception as e:
                    self.set_error_job(jobEntity)
                    Logger().error('其他异常, -' + str(e))
                common.sleep_random()
