# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 1:28 下午 
# @Author : wangHua
# @File : YoutubeVideoDownloadProducer.py
# @Software: PyCharm

from app.producers.BaseProducer import BaseProducer
from app.enums import RedisListKeyEnum
from app.entities import YoutubeVideoDownloadJobEntity
from utils import Http, Logger
from app.proxies import get_proxy_engine
import re


class YoutubeVideoDownloadProducer(BaseProducer):
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_VIDEO_DOWNLOAD_JOB

    def _schedule(self):
        self.schedule.every(10).minutes.do(self.start)

    def start(self):
        try:
            http = Http()
            http.set_proxy(get_proxy_engine('local_proxy').get_proxy())
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/70.0.3538.77 Safari/537.36'}
            http.set_headers(headers)
            url = r"https://www.youtube.com/playlist"
            html = http.request('GET', url, headers=headers).text
            videoIds = re.findall('"videoId":"([A-Za-z0-9_-]{11})","thumbnail"', html)
            for videoId in videoIds:
                entity = YoutubeVideoDownloadJobEntity.instance(
                    {'video_url': 'https://www.youtube.com/watch?v={}'.format(videoId)}
                )
                self.set_job(entity)
        except Exception as e:
            Logger().error("YoutubeVideoDownloadProducer 异常: {}".format(str(e)))
