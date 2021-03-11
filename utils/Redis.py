# !/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from decouple import config
from utils.Singleton import singleton


@singleton
class Redis:
    config = dict()
    db = None

    def __init__(self):
        self.__init_config()
        Redis.pool = redis.ConnectionPool(**self.config)
        self.db = redis.Redis(connection_pool=Redis.pool)

    def __init_config(self):
        self.config['host'] = config('REDIS_HOST', '127.0.0.1')
        self.config['port'] = config('REDIS_PORT', 6379)
        self.config['db'] = config('REDIS_DB_INDEX', 0)
        self.config['decode_responses'] = True
        if config('REDIS_PASSWORD', ''):
            self.config['password'] = config('REDIS_PASSWORD')

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.db, key)(*args, **kwargs)
        return not_find


if __name__ == '__main__':
    redis = Redis()
    redis.lpush('test', 'aaa')
    print(redis.rpop('test'))
