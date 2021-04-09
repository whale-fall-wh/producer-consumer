# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/30 9:31 上午 
# @Author : wangHua
# @File : KeywordConsumer.py 
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
from app.entities import ClassifyProductJobEntity
from utils import Http, Logger
from app.proxies import get_proxy_engine
from app.crawlers import ClassifyProductCrawler
import common
from app.exceptions import NotFoundException, CrawlErrorException
import requests


class KeywordConsumer(BaseConsumer):
    threading_num = 1
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

    def run_job(self):
        Logger().info('keyword_consumer start')
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = ClassifyProductJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawl = ClassifyProductCrawler(jobEntity, http)
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
                common.sleep_random()

    def set_job_key(self) -> str:
        return RedisListKeyEnum.keyword_crawl_job
