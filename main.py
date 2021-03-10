# !/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
import consumers
import producers


class Producer:
    """
    生产任务
    """
    def __init__(self):
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
        self.consumers = consumers.consumer

    def start(self):
        for consumer in self.consumers:
            t = consumer()
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    Consumer().start()
    Producer().start()
