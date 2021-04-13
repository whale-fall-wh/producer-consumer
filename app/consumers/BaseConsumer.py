# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import threading
from app.BaseJob import BaseJob
from abc import ABCMeta, abstractmethod
from utils import Logger


class BaseConsumer(threading.Thread, BaseJob, metaclass=ABCMeta):
    # 多线程抓取
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

    def __init__(self):
        BaseJob.__init__(self)
        threading.Thread.__init__(self)

    @abstractmethod
    def run_job(self):
        pass

    def run(self):
        Logger().debug('{} 开启 {} 个线程'.format(self.__class__.__name__, self.threading_num))
        for i in range(self.threading_num):
            t = threading.Thread(target=self.run_job)
            t.start()
