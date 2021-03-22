# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm


from app.crawlers.ProductCrawler import ProductCrawler
from utils.Logger import Logger
from utils.Http import Http
from app.proxies import get_proxy_engine
import common
from app.consumers import BaseConsumer
from app.exceptions.CrawlErrorException import CrawlErrorException
from app.exceptions.NotFoundException import NotFoundException
from app.enums.RedisListKeyEnum import RedisListKeyEnum
from app.entities.ProductJobEntity import ProductJobEntity


class ProductConsumer(BaseConsumer):
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
        return RedisListKeyEnum.product_crawl_job

    def run(self):
        Logger().info('product_consumer start')
        # 要保持所有http请求在一个会话中，所以这边带参数传，对代理有要求，IP尽量少变化，变化后，http会话就没有意义了
        self.http = Http()
        self.proxy_engine = get_proxy_engine()
        self.http.set_headers(self.headers)
        while True:
            job_dict = self.get_job_obj()
            if job_dict:
                job_entity = ProductJobEntity.instance(job_dict)
                try:
                    if self.proxy_engine:
                        # product 反扒比较苛刻，这边用了随机IP的代理
                        self.http.set_proxy(self.proxy_engine.get_proxy())
                    ProductCrawler(job_entity, self.http)
                except CrawlErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.set_error_job(job_entity)
                except NotFoundException:
                    # 页面不存在，不做处理
                    pass
                common.sleep_random()


if __name__ == '__main__':
    t = ProductConsumer()
    t.setDaemon(False)  # 非守护进程，主线程结束任务之后，会等待线程结束，注意任务是死循环
    t.start()
