# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 10:15 上午
# @Author : wangHua
# @Software: PyCharm


from abc import ABCMeta


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

    def to_dict(self):
        return self.__dict__

    def to_string(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()
