# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 4:05 下午
# @Author : wangHua
# @Software: PyCharm

import schedule
import time
from app.jobs import producers, consumers
import argparse
from utils import db


class Argparse(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._add_arguments()
        self.args = self.parser.parse_args()
        self.p = Producer()
        self.s = Consumer()

    def _add_arguments(self):
        self.parser.add_argument('-run', help='RUN！！！', action='store_true')
        self.parser.add_argument('-run-all-producer', help='立刻运行所有的producer', action='store_true')
        self.parser.add_argument('-run-producer', help='立刻运行指定producer', dest='producer_class_name', choices=[
            producer_class.__name__ for producer_class in producers.producers
        ])
        self.parser.add_argument('-run-consumer', help='运行指定consumer', dest='consumer_class_name', choices=[
            consumer_class.__name__ for consumer_class in consumers.consumers
        ])
        self.parser.add_argument('-migrate', help='创建表', action='store_true')

    def run(self):
        if self.args.producer_class_name:
            self.p.run_by_class_name(self.args.producer_class_name)
        elif self.args.consumer_class_name:
            self.s.run_by_class_name(self.args.consumer_class_name)
        elif self.args.run_all_producer:
            self.p.run_all()
        elif self.args.migrate:
            db.create_all()
        else:
            self.s.start()
            self.p.start()


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

    def run_all(self):
        for producer in self.producers:
            producer().start()

    def run_by_class_name(self, class_name):
        for producer in self.producers:
            if producer.__name__ == class_name:
                producer().start()


class Consumer:
    """
    消费任务--多线程，继承多线程类，一个job一个线程
    """
    def __init__(self):
        # 所有的消费者类(继承Thread、BaseConsumer)
        self.consumers = consumers.consumers

    def start(self):
        for consumer in self.consumers:
            t = consumer()
            t.setDaemon(True)
            t.start()

    def run_by_class_name(self, consumer_class_name):
        for consumer in self.consumers:
            if consumer.__name__ == consumer_class_name:
                t = consumer()
                t.setDaemon(False)
                t.start()


if __name__ == '__main__':
    Argparse().run()
