# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import functools
import threading


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


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


# 线程安全单利类
class ThreadSafeSingleton(type):
    _instances = {}

    @synchronized
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
