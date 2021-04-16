# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:18 上午 
# @Author : wangHua
# @File : YoutubeVideoThumbnailRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import YoutubeVideoThumbnail
from app.entities import YoutubeVideoThumbnailEntity
from utils.Singleton import singleton


@singleton
class YoutubeVideoThumbnailRepository(BaseRepository):
    def init_model(self):
        return YoutubeVideoThumbnail

    def save_by_entity(self, entity: YoutubeVideoThumbnailEntity):
        return self.init_model().update_or_create(
            entity.only(['video_id', 'thumbnail_id']),
            entity.besides(['video_id', 'thumbnail_id'])
        )
