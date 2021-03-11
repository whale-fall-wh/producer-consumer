# !/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from decouple import config
from utils.Singleton import singleton


@singleton
class Redis:
    config = dict()

    def __init__(self):
        self.init_config()
        Redis.pool = redis.ConnectionPool(**self.config)
        self.db = redis.Redis(connection_pool=Redis.pool)

    def init_config(self):
        self.config['host'] = config('REDIS_HOST')
        self.config['port'] = config('REDIS_PORT', 6379)
        self.config['db'] = config('REDIS_DB_INDEX', 0)
        self.config['decode_responses'] = True
        if config('REDIS_PASSWORD'):
            self.config['password'] = config('REDIS_PASSWORD')


if __name__ == '__main__':
    redis = Redis()
    redis.db.lpush('test', 'aaa')
    print(redis.db.rpop('test'))
