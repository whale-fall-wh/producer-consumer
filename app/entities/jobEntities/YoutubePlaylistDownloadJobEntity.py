# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 2:55 下午 
# @Author : wangHua
# @File : YoutubePlaylistDownloadJobEntity.py 
# @Software: PyCharm

from .BaseJobEntity import BaseJobEntity


class YoutubePlaylistDownloadJobEntity(BaseJobEntity):
    url = 'https://www.youtube.com/playlist'
