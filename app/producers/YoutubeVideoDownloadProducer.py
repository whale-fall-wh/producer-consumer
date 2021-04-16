# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 1:28 下午 
# @Author : wangHua
# @File : YoutubeVideoDownloadProducer.py
# @Software: PyCharm

from app.producers.BaseProducer import BaseProducer
from app.enums import RedisListKeyEnum
from app.entities import YoutubeVideoDownloadJobEntity


test_url = 'https://www.youtube.com/watch?v=BaW_jenozKc'


class YoutubeVideoDownloadProducer(BaseProducer):
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_VIDEO_DOWNLOAD_JOB

    def _schedule(self):
        pass

    def start(self):
        entity = YoutubeVideoDownloadJobEntity.instance({'video_url': test_url})
        self.set_job(entity)
