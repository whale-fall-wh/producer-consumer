# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 4:05 下午
# @Author : wangHua
# @Software: PyCharm

import schedule
import re
import time
from app import consumers, producers


class Producer:
    """
    生产任务
    """
    def __init__(self):
        # 所有的生产者类(继承BaseProducer)
        self.producers = producers.producers

    def start(self):
        for producer in self.producers:
            producer()
        while True:
            schedule.run_pending()
            time.sleep(1)


class Consumer:
    """
    消费任务--多线程，继承多线程类，一个job一个线程
    """
    def __init__(self):
        # 所有的消费者类(继承Thread、BaseConsumer)
        self.consumers = consumers.consumer

    def start(self):
        for consumer in self.consumers:
            t = consumer()
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    Consumer().start()  # 多线程启动消费者
    Producer().start()
