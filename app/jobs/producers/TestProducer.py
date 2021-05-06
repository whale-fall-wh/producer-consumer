# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/17 3:59 下午 
# @Author : wangHua
# @File : TestProducer.py 
# @Software: PyCharm

from app.jobs.producers import BaseProducer
from app.enums import RedisListKeyEnum
from app.entities import YoutubeSearchDownloadJobEntity


class TestProducer(BaseProducer):
    def set_job_key(self) -> str:
        return RedisListKeyEnum.YOUTUBE_SEARCH_DOWNLOAD_JOB

    def _schedule(self):
        pass

    def start(self):
        entity = YoutubeSearchDownloadJobEntity.instance(
            {'keyword': 'husky', 'count': 20}
        )
        self.set_job(entity)
