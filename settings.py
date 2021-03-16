# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

from decouple import config
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STORAGE_PATH = PROJECT_PATH + '/storage'

DATABASE_CONFIG = {
    'username': config('DB_USERNAME', 'root'),
    'password': config('DB_PASSWORD', '123456'),
    'host': config('DB_HOST', '127.0.0.1'),
    'port': config('DB_PORT', 3306),
    'database': config('DB_DATABASE', ''),
}

CONNECTION_STR = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(**DATABASE_CONFIG)

REDIS_CONFIG = {
    'host': config('REDIS_HOST', '127.0.0.1'),
    'port': config('REDIS_PORT', 6379),
    'db': config('REDIS_DB_INDEX', 0),
    'decode_responses': True
}
if config('REDIS_PASSWORD', ''):
    REDIS_CONFIG['password'] = config('REDIS_PASSWORD')
