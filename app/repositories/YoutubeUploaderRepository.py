# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:16 上午 
# @Author : wangHua
# @File : YoutubeUploaderRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import YoutubeUploader
from app.entities import YoutubeUploaderEntity
from utils.Singleton import singleton


@singleton
class YoutubeUploaderRepository(BaseRepository):
    def init_model(self):
        return YoutubeUploader

    def save_by_entity(self, entity: YoutubeUploaderEntity):
        return self.init_model().update_or_create(entity.only(['uploader_id']), entity.besides(['uploader_id']))
