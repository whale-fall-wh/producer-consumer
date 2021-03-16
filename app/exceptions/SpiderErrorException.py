# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.Logger import Logger


class SpiderErrorException(Exception):
    """爬虫抓取失败异常"""

    def __init__(self, msg=''):
        if msg:
            Logger().warning(msg)
