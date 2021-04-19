# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:14 上午 
# @Author : wangHua
# @File : YoutubeVideoRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import YoutubeVideo
from app.entities import YoutubeVideoEntity
from utils.Singleton import singleton


@singleton
class YoutubeVideoRepository(BaseRepository):
    def init_model(self):
        return YoutubeVideo

    def save_by_entity(self, entity: YoutubeVideoEntity, resource_id=None):
        data = entity.only(['title', 'title', 'description', 'upload_date', 'uploader_id', 'url', 'channel_id',
                            'duration', 'view_count', 'average_rating', 'age_limit', 'like_count', 'dislike_count'])
        if resource_id is not None:
            data['resource_id'] = resource_id
        return self.init_model().update_or_create(
            entity.only(['video_id']),
            data
        )
