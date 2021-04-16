# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 2:56 下午 
# @Author : wangHua
# @File : RedisListKeyEnum.py 
# @Software: PyCharm

from app.enums.BaseEnum import BaseEnum


class RedisListKeyEnum(BaseEnum):

    YOUTUBE_VIDEO_DOWNLOAD_JOB = 'youtube_video_download_job'
    YOUTUBE_VIDEO_LIST_DOWNLOAD_JOB = 'youtube_video_list_download_job'
