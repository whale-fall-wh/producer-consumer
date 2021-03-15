# !/usr/bin/env python
# -*- coding: utf-8 -*-

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
