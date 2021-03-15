# !/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.Redis import Redis
import common
import json


class BaseJob(object):
    job_key = None
    __job_name_key = 'job'
    __retry_name_key = 'retry_time'

    def __init__(self):
        self.base_key = 'job:{}'
        self.redis = Redis().db

    def __get_job_key(self):
        return self.base_key.format(self.job_key)

    def get_job(self, job_dict: dict):
        return job_dict.get(self.__job_name_key)

    def get_job_obj(self):
        """
        获取任务
        :return: 任务字典
        """
        job_str = self.redis.lpop(self.__get_job_key())
        if job_str:
            return json.loads(job_str)
        else:
            common.sleep(5)
            self.get_job_obj()

    def set_job(self, job):
        job_dict = {self.__job_name_key: job, self.__retry_name_key: 0}

        return self.redis.rpush(self.__get_job_key(), json.dumps(job_dict))

    def set_error_job(self, job_dict: dict):
        job_dict['retry_time'] = job_dict.get(self.__retry_name_key) + 1

        return self.redis.rpush(self.__get_job_key(), json.dumps(job_dict))
