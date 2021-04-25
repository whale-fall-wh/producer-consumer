# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 2:51 下午 
# @Author : wangHua
# @File : YoutubePlaylistDownloadConsumer.py 
# @Software: PyCharm


from app.jobs.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
import youtube_dl
from app.proxies import get_proxy_engine
from app.entities import YoutubePlaylistDownloadJobEntity, YoutubePlaylistEntity
from app.services import YoutubeVideoService


class YoutubePlaylistDownloadConsumer(BaseConsumer):
    ydl_opts = {
    }

    def __init__(self):
        self.youtubeVideoService = YoutubeVideoService()
        super(YoutubePlaylistDownloadConsumer, self).__init__()

    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_PLAYLIST_DOWNLOAD_JOB

    def run_job(self, job_dict: dict):
        proxyEngine = get_proxy_engine('local_proxy')
        jobEntity = YoutubePlaylistDownloadJobEntity.instance(job_dict)
        self.ydl_opts['proxy'] = proxyEngine.get_proxy_ip() if proxyEngine else None
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(
                jobEntity.url,
                download=False
            )

        playlistEntity = YoutubePlaylistEntity.instance(result)
        for videoEntity in playlistEntity.videos:
            self.youtubeVideoService.save_by_entity(videoEntity)


