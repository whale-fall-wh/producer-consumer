# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 9:50 上午 
# @Author : wangHua
# @File : ClassifyProductJobEntity.py 
# @Software: PyCharm

from .BaseJobEntity import BaseJobEntity


class ClassifyProductJobEntity(BaseJobEntity):

    site_id = 0
    site_name = ''
    keyword_id = 0
    keyword = ''
    page = 1
    current_num = 0
    max_num = 2

    def set_job_type(self):
        return 'crawl-classify'
