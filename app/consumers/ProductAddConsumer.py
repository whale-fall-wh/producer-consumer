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
from app.entities import ProductJobEntity, ProductAddJobEntity, ProductReviewJobEntity
from app.crawlers import ProductAddCrawler
import common
import requests


class ProductAddConsumer(BaseConsumer):
    threading_num = 1
    """
    添加新的asin时，插入对应的任务，该消费者会判断某个站点中的产品是否存在，如果存在，则添加对应站点的asin数据，并产生新的任务
    """
    # ignore = True     # 忽略该消费者

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_add_crawl_job

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = ProductAddJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawler = ProductAddCrawler(jobEntity, http)
                    if crawler.productItem:
                        job_dict['product_item_id'] = crawler.productItem.id
                        # self.set_job_by_key(RedisListKeyEnum.product_crawl_job, ProductJobEntity.instance(job_dict))
                        self.set_job_by_key(RedisListKeyEnum.product_review_crawl_job,
                                            ProductReviewJobEntity.instance(job_dict))
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(jobEntity)
                except requests.exceptions.ProxyError:
                    # 代理异常
                    Logger().error('代理异常')
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                except Exception as e:
                    self.set_error_job(jobEntity)
                    Logger().error('其他异常, -' + str(e))
                common.sleep_random()
