# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:05 下午
# @Author : wangHua
# @Software: PyCharm


import redis
from settings import REDIS_CONFIG
from utils.Singleton import singleton


@singleton
class Redis:
    db = None

    def __init__(self):
        Redis.pool = redis.ConnectionPool(**REDIS_CONFIG)
        self.db = redis.Redis(connection_pool=Redis.pool)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.db, key)(*args, **kwargs)
        return not_find


if __name__ == '__main__':
    redis = Redis()
    redis.lpush('test', 'aaa')
    print(redis.rpop('test'))
