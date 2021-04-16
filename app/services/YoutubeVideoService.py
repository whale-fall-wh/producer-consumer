# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 10:45 上午 
# @Author : wangHua
# @File : YoutubeVideoService.py 
# @Software: PyCharm

from app.repositories import *
from app.entities import YoutubeVideoEntity


class YoutubeVideoService(object):

    def __init__(self):
        self.youtubeVideoRepository = YoutubeVideoRepository()
        self.youtubeUploaderRepository = YoutubeUploaderRepository()
        self.youtubeVideoFormatRepository = YoutubeVideoFormatRepository()
        self.youtubeVideoThumbnailRepository = YoutubeVideoThumbnailRepository()

    def save_by_entity(self, entity: YoutubeVideoEntity):
        uploader = self.youtubeUploaderRepository.save_by_entity(entity.upload_entity)
        video = self.youtubeVideoRepository.save_by_entity(entity)
        uploader.videos.append(video)
        for formatEntity in entity.formats:
            videoFormat = self.youtubeVideoFormatRepository.save_by_entity(formatEntity)
            video.video_formats.append(videoFormat)
        for thumbnailEntity in entity.thumbnails:
            thumbnail = self.youtubeVideoThumbnailRepository.save_by_entity(thumbnailEntity)
            video.video_thumbnails.append(thumbnail)

        return video
