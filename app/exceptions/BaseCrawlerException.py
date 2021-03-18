# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/17 12:54 下午 
# @Author : wangHua
# @File : BaseCrawlerException.py
# @Software: PyCharm

from utils.Logger import Logger


class BaseCrawlException(Exception):
    """爬虫抓取失败异常"""

    def __init__(self, msg=''):
        if msg:
            Logger().warning(msg)
