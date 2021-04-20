# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 3:24 下午 
# @Author : wangHua
# @File : YoutubeSearchDownloadConsumer.py 
# @Software: PyCharm


from app.jobs.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
import youtube_dl
from app.proxies import get_proxy_engine
from app.entities import YoutubeSearchDownloadJobEntity, YoutubePlaylistEntity
from app.services import YoutubeVideoService


class YoutubeVideoDownloadConsumer(BaseConsumer):
    ydl_opts = {
        'noplaylist': 'True',
        '--default-search': 'ytsearch'
    }

    def __init__(self):
        self.youtubeVideoService = YoutubeVideoService()
        BaseConsumer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_SEARCH_DOWNLOAD_JOB

    def run_job(self, job_dict: dict):
        proxyEngine = get_proxy_engine('local_proxy')
        jobEntity = YoutubeSearchDownloadJobEntity.instance(job_dict)
        if jobEntity.keyword is None:
            return
        self.ydl_opts['proxy'] = proxyEngine.get_proxy_ip() if proxyEngine else None

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch{jobEntity.count}:{jobEntity.keyword}",
                download=False
            )
        playlistEntity = YoutubePlaylistEntity.instance(result)
        for videoEntity in playlistEntity.videos:
            self.youtubeVideoService.save_by_entity(videoEntity)
