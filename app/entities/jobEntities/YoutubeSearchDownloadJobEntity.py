# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 3:24 下午 
# @Author : wangHua
# @File : YoutubeSearchDownloadJobEntity.py 
# @Software: PyCharm


from .BaseJobEntity import BaseJobEntity


class YoutubeSearchDownloadJobEntity(BaseJobEntity):
    keyword = None
    count = 10
