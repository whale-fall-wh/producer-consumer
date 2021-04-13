# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/30 9:31 上午 
# @Author : wangHua
# @File : KeywordConsumer.py 
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
from app.entities import KeywordJobEntity
from utils import Http, Logger
from app.proxies import get_proxy_engine
from app.crawlers import KeywordCrawler
import common
from app.exceptions import NotFoundException, CrawlErrorException
import requests


class KeywordConsumer(BaseConsumer):
    # ignore = True
    threading_num = 1

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = KeywordJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    crawl = KeywordCrawler(jobEntity, http)
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

    def set_job_key(self) -> str:
        return RedisListKeyEnum.keyword_crawl_job
