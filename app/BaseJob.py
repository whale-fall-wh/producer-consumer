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


# 用redis队列实现，也可以用rabbitMQ实现更复杂的场景
class BaseJob(metaclass=ABCMeta):
    base_key = config('REDIS_PREFIX', 'cpa:') + 'job:{}'

    def __init__(self):
        self.job_key = self.set_job_key()

    @abstractmethod
    def set_job_key(self) -> str:
        pass

    @staticmethod
    def __get_job_key(job_key: str):
        return BaseJob.base_key.format(job_key)

    def get_job_obj(self) -> dict:
        """
        获取任务
        :return: 任务字典
        """
        while True:
            job_str = Redis().db.lpop(self.__get_job_key(self.job_key))
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

    @classmethod
    def set_job_by_key(cls, job_key, job_entity: BaseJobEntity):
        """可以再优化一下，挪到其他地方"""
        return Redis().db.rpush(cls.__get_job_key(job_key), json.dumps(job_entity.to_dict()))
