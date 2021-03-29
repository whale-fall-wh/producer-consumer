# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.Redis import Redis
from abc import ABCMeta, abstractmethod
import common
import json
from app.entities.BaseJobEntity import BaseJobEntity
from decouple import config


class BaseJob(metaclass=ABCMeta):

    def __init__(self):
        self.job_key = self.set_job_key()
        self.base_key = config('REDIS_PREFIX', 'cpa:') + 'job:{}'
        self.redis = Redis().db

    @abstractmethod
    def set_job_key(self) -> str:
        pass

    def __get_job_key(self, job_key: str):
        return self.base_key.format(job_key)

    def get_job_obj(self) -> dict:
        """
        获取任务
        :return: 任务字典
        """
        while True:
            job_str = self.redis.lpop(self.__get_job_key(self.job_key))
            if job_str:
                return json.loads(job_str)
            common.sleep(10)

    def set_job(self, job_entity: BaseJobEntity):
        return self.set_job_by_key(self.job_key, job_entity)

    def set_error_job(self, job_entity: BaseJobEntity):
        if job_entity.retry_time >= 3:
            return False
        job_entity.retry_time += 1

        return self.set_job_by_key(self.job_key, job_entity)

    def set_job_by_key(self, job_key, job_entity: BaseJobEntity):
        return self.redis.rpush(self.__get_job_key(job_key), json.dumps(job_entity.to_dict()))
