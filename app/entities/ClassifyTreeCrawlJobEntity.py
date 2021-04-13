# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 10:13 上午 
# @Author : wangHua
# @File : ClassifyTreeCrawlJobEntity.py 
# @Software: PyCharm

from app.entities.BaseJobEntity import BaseJobEntity


class ClassifyTreeCrawlJobEntity(BaseJobEntity):

    url = ''
    url_id = ''
    name = ''
    product_id = 0
    site_id = 0
    product_item_id = 0

    def set_job_type(self):
        return 'classify_tree_crawl_job'
