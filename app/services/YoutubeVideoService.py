# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:45 上午 
# @Author : wangHua
# @File : YoutubeVideoService.py 
# @Software: PyCharm

from app.repositories import *
from app.entities import YoutubeVideoEntity
from settings import PROJECT_PATH, VIDEO_PATH
from utils import Logger


class YoutubeVideoService(object):

    def __init__(self):
        self.youtubeVideoRepository = YoutubeVideoRepository()
        self.youtubeUploaderRepository = YoutubeUploaderRepository()
        self.youtubeVideoFormatRepository = YoutubeVideoFormatRepository()
        self.youtubeVideoThumbnailRepository = YoutubeVideoThumbnailRepository()
        self.resourceRepository = ResourceRepository()

    def save_by_entity(self, entity: YoutubeVideoEntity, save_resource=False):
        Logger().info('{} 正在入库'.format(entity.video_id))
        uploader = self.youtubeUploaderRepository.save_by_entity(entity.upload_entity)
        resource_id = None
        if save_resource:
            resource_id = self.save_resource(entity)
        video = self.youtubeVideoRepository.save_by_entity(entity, resource_id)

        uploader.videos.append(video)
        for formatEntity in entity.formats:
            videoFormat = self.youtubeVideoFormatRepository.save_by_entity(
                formatEntity,
                resource_id=resource_id if save_resource and formatEntity.format_id == entity.format_id else None
            )
            video.video_formats.append(videoFormat)
        for thumbnailEntity in entity.thumbnails:
            thumbnail = self.youtubeVideoThumbnailRepository.save_by_entity(thumbnailEntity)
            video.video_thumbnails.append(thumbnail)

        return video

    def save_resource(self, entity: YoutubeVideoEntity):
        video_path = '{video_path}/{extractor}/{id}/{format}-{format_note}.{ext}'.format(**{
            'video_path': VIDEO_PATH,
            'extractor': entity.extractor,
            'id': entity.video_id,
            'format': entity.format_id,
            'format_note': entity.format_note,
            'ext': entity.ext
        }).replace(PROJECT_PATH, '')
        resource = self.resourceRepository.save(video_path)
        return resource.id
