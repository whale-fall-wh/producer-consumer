# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 10:02 上午 
# @Author : wangHua
# @File : YoutubeVideoDownloadConsumer.py
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
import youtube_dl
from settings import STORAGE_PATH
from app.proxies import get_proxy_engine
from app.entities import YoutubeVideoDownloadJobEntity, YoutubeVideoEntity
from utils import Logger
from app.services import YoutubeVideoService


class YoutubeVideoDownloadConsumer(BaseConsumer):
    ydl_opts = {
        'outtmpl': '{}%(extractor)s/%(id)s.%(ext)s'.format(STORAGE_PATH + '/videos/')
    }

    def __init__(self):
        self.youtubeVideoService = YoutubeVideoService()
        BaseConsumer.__init__(self)
    
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_VIDEO_DOWNLOAD_JOB

    def run_job(self):
        proxyEngine = get_proxy_engine('local_proxy')
        while True:
            try:
                job_dict = self.get_job_obj()
                if job_dict:
                    jobEntity = YoutubeVideoDownloadJobEntity.instance(job_dict)
                    self.ydl_opts['proxy'] = proxyEngine.get_proxy_ip() if proxyEngine else None
                    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                        result = ydl.extract_info(jobEntity.video_url)
                    videoEntity = YoutubeVideoEntity.instance(result)
                    video = self.youtubeVideoService.save_by_entity(videoEntity)
            except Exception as e:
                Logger().error('YouTubeConsumer - {}'.format(str(e)))
