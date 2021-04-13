# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 2:05 下午 
# @Author : wangHua
# @File : KeywordProducer.py 
# @Software: PyCharm

from app.producers.BaseProducer import BaseProducer
from app.enums import RedisListKeyEnum
from app.repositories import KeywordRepository
from app.entities import KeywordJobEntity


class KeywordProducer(BaseProducer):
    """
    测试生成任务，实际应该在web段查询的时候新增一条记录，并插入队列
    """
    ignore = True

    def __init__(self):
        self.keywordRepository = KeywordRepository()
        BaseProducer.__init__(self)

    def _schedule(self):
        pass

    def start(self):
        keywords = self.keywordRepository.all()
        for keyword in keywords:
            jobEntity = KeywordJobEntity.instance({
                'site_id': 1,
                'site_name': '',
                'keyword_id': keyword.id,
                'keyword_name': keyword.name,
                'max_num': 100
            })
            self.set_job(jobEntity)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.keyword_crawl_job
