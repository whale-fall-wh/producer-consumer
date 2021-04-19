# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 2:54 下午 
# @Author : wangHua
# @File : YoutubePlaylistDownloadProducer.py 
# @Software: PyCharm

from app.jobs.producers import BaseProducer
from app.enums import RedisListKeyEnum
from app.entities import YoutubePlaylistDownloadJobEntity


class YoutubePlaylistDownloadProducer(BaseProducer):
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_PLAYLIST_DOWNLOAD_JOB

    def _schedule(self):
        self.schedule.every(3).hours.do(self.start)

    def start(self):
        entity = YoutubePlaylistDownloadJobEntity.instance(
            {}
        )
        self.set_job(entity)
