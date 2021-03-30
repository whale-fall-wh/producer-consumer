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


class ProductReviewConsumer(BaseConsumer):
    """
    住区评论信息
    """
    threading_num = 3

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

    def set_job_key(self) -> str:
        return RedisListKeyEnum.product_review_crawl_job

    def run_job(self):
        Logger().info('product_review_consumer start')
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                job_entity = ProductReviewJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawl = ProductReviewCrawler(job_entity, http)
                    if crawl.crawl_next_page:
                        job_entity.page += 1
                        self.set_job(job_entity)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(job_entity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                common.sleep_random()
