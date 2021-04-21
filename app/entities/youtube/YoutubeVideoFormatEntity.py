# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 3:26 下午 
# @Author : wangHua
# @File : YoutubeVideoFormatEntity.py
# @Software: PyCharm

from app.entities.BaseEntity import BaseEntity


class YoutubeVideoFormatEntity(BaseEntity):
    video_id = ''
    format_id = ''
    asr = 0
    filesize = 0
    format_note = ''
    fps = 0
    height = 0
    width = 0
    quality = 0
    ext = ''
