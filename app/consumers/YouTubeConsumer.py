# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/15 10:02 上午 
# @Author : wangHua
# @File : YouTubeConsumer.py
# @Software: PyCharm

from app.consumers.BaseConsumer import BaseConsumer
from app.enums import RedisListKeyEnum
import youtube_dl
from settings import STORAGE_PATH


class YouTubeConsumer(BaseConsumer):
    ydl_opts = {
        'proxy': 'http://localhost:1081',
        'outtmpl': '{}%(extractor)s/%(author)s-%(title)s.%(ext)s'.format(STORAGE_PATH + '/videos/')
    }

    def set_job_key(self) -> str:
        return RedisListKeyEnum.youtube_crawl_job

    def run_job(self):

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=ltZZ3M2zQRw'])
