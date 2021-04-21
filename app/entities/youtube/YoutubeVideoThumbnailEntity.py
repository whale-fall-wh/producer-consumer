# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 9:58 上午 
# @Author : wangHua
# @File : YoutubeVideoThumbnailEntity.py
# @Software: PyCharm

from ..BaseEntity import BaseEntity


class YoutubeVideoThumbnailEntity(BaseEntity):
    video_id = ''
    thumbnail_id = ''
    width = 0
    height = 0

    def to_object(self, data: dict):
        super(YoutubeVideoThumbnailEntity, self).to_object(data)
        self.thumbnail_id = data.get('id', '')

        return self
