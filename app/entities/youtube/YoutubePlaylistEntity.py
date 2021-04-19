# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 3:04 下午 
# @Author : wangHua
# @File : YoutubePlaylistEntity.py 
# @Software: PyCharm

from app.entities.BaseEntity import BaseEntity
from .YoutubeVideoEntity import YoutubeVideoEntity


class YoutubePlaylistEntity(BaseEntity):
    _type = 'playlist'
    entries = None
    videos = []

    def to_object(self, data: dict):
        super(YoutubePlaylistEntity, self).to_object(data)

        if self.entries and type(self.entries) == list:
            for entry in self.entries:
                self.videos.append(YoutubeVideoEntity.instance(entry))

        return self
