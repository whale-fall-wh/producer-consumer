# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from .BaseCrawlerException import BaseCrawlException


class CrawlErrorException(BaseCrawlException):
    """爬虫抓取失败异常"""
    pass
