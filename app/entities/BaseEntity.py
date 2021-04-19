# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 10:15 上午
# @Author : wangHua
# @Software: PyCharm


from abc import ABCMeta
from copy import deepcopy


class BaseEntity(metaclass=ABCMeta):

    def __init__(self):
        pass

    @classmethod
    def instance(cls, data: dict):
        return cls().to_object(data=data)

    def to_object(self, data: dict):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

        return self

    def only(self, keys: list) -> dict:
        data = self.to_dict()

        return {key: value for key, value in data.items() if key in keys}

    def besides(self, keys: list) -> dict:
        data = deepcopy(self).to_dict()
        [data.pop(k) for k in keys]

        return data

    def to_dict(self):
        return self.__dict__

    def to_string(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()
