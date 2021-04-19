# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:22 上午 
# @Author : wangHua
# @File : YoutubeUploaderEntity.py 
# @Software: PyCharm

from app.entities.BaseEntity import BaseEntity


class YoutubeUploaderEntity(BaseEntity):
    uploader_id = ''
    uploader = ''
    url = ''

    def to_object(self, data: dict):
        super(YoutubeUploaderEntity, self).to_object(data)
        self.url = data.get('uploader_url', '')

        return self
