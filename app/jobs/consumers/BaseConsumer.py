# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import threading
from app.jobs.BaseJob import BaseJob
from abc import ABCMeta, abstractmethod
from utils import Logger


class BaseConsumer(threading.Thread, BaseJob, metaclass=ABCMeta):
    # 多线程抓取
    threading_num = 1

    def __init__(self):
        BaseJob.__init__(self)
        threading.Thread.__init__(self)

    @abstractmethod
    def run_job(self, job_dict: dict):
        pass

    def run_threading(self):
        while True:
            try:
                job_dict = self.get_job_obj()
                if job_dict:
                    self.start_job(job_dict)
                    self.run_job(job_dict)

                self.finish_job()
            except Exception as e:
                Logger().error('{} - {}'.format(self.__class__.__name__, str(e)))
                self.fail(e)

    def run(self):
        Logger().debug('{} 开启 {} 个线程'.format(self.__class__.__name__, self.threading_num))
        for i in range(self.threading_num):
            t = threading.Thread(target=self.run_threading)
            t.start()

    def start_job(self, job_dict: dict):
        Logger().info("任务：{} 开始，参数：{}".format(self.__class__.__name__, job_dict.__str__()))

    def finish_job(self):
        Logger().info("任务：{} 完成".format(self.__class__.__name__))

    def fail(self, e: Exception):
        Logger().error('{} - {}'.format(self.__class__.__name__, str(e)))
