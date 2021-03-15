# !/usr/bin/env python
# -*- coding: utf-8 -*-

from app.crawlers.ProductSpider import ProductCrawler
from utils.Logger import Logger
from utils.Http import Http
import common
from app.consumers import BaseConsumer
from app.exceptions.SpiderErrorException import SpiderErrorException


class ProductConsumer(BaseConsumer):
    # ignore = True     # 忽略该消费者
    job_key = 'product_asin'

    def __init__(self):
        self.http = None
        BaseConsumer.__init__(self)

    def _check_proxy(self):
        if self.http.continue_error_time >= 3:
            self.http.continue_error_time = 0
            self.http.set_proxy()

    def run(self):
        Logger().info('product_consumer start')
        # 要保持所有http请求在一个会话中，所以这边带参数传，对代理有要求，IP尽量少变化，变化后，http会话就没有意义了
        self.http = Http()

        while True:
            job_dict = self.get_job_obj()
            # 检查是否需要切换代理，连续三次请求失败，则需要切换代理
            self._check_proxy()
            if job_dict:
                try:
                    asin_str = self.get_job(job_dict)
                    ProductCrawler(asin_str, self.http)
                    self.http.init_error_info()
                except SpiderErrorException:
                    # 爬虫失败异常，http 连续失败次数+1
                    self.http.error_time_increase()
                    self.set_error_job(job_dict)

                common.sleep_random()


if __name__ == '__main__':
    t = ProductConsumer()
    t.setDaemon(False)  # 非守护进程，主线程结束任务之后，会等待线程结束，注意任务是死循环
    t.start()
