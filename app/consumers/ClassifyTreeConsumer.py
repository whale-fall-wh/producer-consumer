# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 1:31 下午 
# @Author : wangHua
# @File : ClassifyTreeConsumer.py 
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
from app.entities import ClassifyTreeCrawlJobEntity
from utils import Http, Logger
from app.proxies import get_proxy_engine
from app.crawlers import ClassifyTreeCrawler
import common
from app.exceptions import NotFoundException, CrawlErrorException
import requests


class ClassifyTreeConsumer(BaseConsumer):
    threading_num = 1

    def set_job_key(self) -> str:
        return RedisListKeyEnum.classify_tree_crawl_job

    def run_job(self):
        http = Http()
        proxy_engine = get_proxy_engine()
        http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                jobEntity = ClassifyTreeCrawlJobEntity.instance(job_dict)
                try:
                    if proxy_engine:
                        http.set_proxy(proxy_engine.get_proxy())
                    ClassifyTreeCrawler(jobEntity, http)
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
