# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:05 下午
# @Author : wangHua
# @Software: PyCharm


def singleton(cls):
    """
    单例修饰器
    :param cls:
    :return:
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
