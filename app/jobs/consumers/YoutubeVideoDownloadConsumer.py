# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 10:02 上午 
# @Author : wangHua
# @File : YoutubeVideoDownloadConsumer.py
# @Software: PyCharm

from app.jobs.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
import youtube_dl
from settings import VIDEO_PATH
from app.proxies import get_proxy_engine
from app.entities import YoutubeVideoDownloadJobEntity, YoutubeVideoEntity
from app.services import YoutubeVideoService


class YoutubeVideoDownloadConsumer(BaseConsumer):
    ydl_opts = {
        'outtmpl': '{}/%(extractor)s/%(id)s/%(format_id)s-%(format_note)s.%(ext)s'.format(VIDEO_PATH),
    }

    def __init__(self):
        self.youtubeVideoService = YoutubeVideoService()
        super(YoutubeVideoDownloadConsumer, self).__init__()
    
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_VIDEO_DOWNLOAD_JOB

    def run_job(self, job_dict: dict):
        jobEntity = YoutubeVideoDownloadJobEntity.instance(job_dict)
        proxyEngine = get_proxy_engine('local_proxy')
        self.ydl_opts['proxy'] = proxyEngine.get_proxy_ip() if proxyEngine else None
        if jobEntity.format is not None:
            self.ydl_opts['format'] = jobEntity.format
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(
                jobEntity.video_url,
                download=jobEntity.download
            )
        videoEntity = YoutubeVideoEntity.instance(result)
        self.youtubeVideoService.save_by_entity(videoEntity, save_resource=jobEntity.download)
