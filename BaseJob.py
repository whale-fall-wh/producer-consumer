# !/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.Redis import Redis


class BaseJob(object):
    job_key = None
    base_key = 'job:{}'

    def __init__(self):
        self.redis = Redis().db

    def get_job_key(self):
        return self.base_key.format(self.job_key)

    def get_job(self):
        return self.redis.rpop(self.get_job_key())

    def set_job(self, job):
        return self.redis.lpush(self.get_job_key(), job)
