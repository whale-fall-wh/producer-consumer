# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:17 上午 
# @Author : wangHua
# @File : YoutubeVideoFormatRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import YoutubeVideoFormat
from app.entities import YoutubeVideoFormatEntity
from utils.Singleton import singleton


@singleton
class YoutubeVideoFormatRepository(BaseRepository):

    def init_model(self):
        return YoutubeVideoFormat

    def save_by_entity(self, entity: YoutubeVideoFormatEntity):
        return self.init_model().update_or_create(
            entity.only(['video_id', 'format_id']),
            entity.besides(['video_id', 'format_id'])
        )
