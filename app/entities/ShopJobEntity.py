# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 10:42 上午 
# @Author : wangHua
# @File : ShopJobEntity.py 
# @Software: PyCharm

from app.entities.BaseJobEntity import BaseJobEntity


class ShopJobEntity(BaseJobEntity):
    shop_item_id = 0
    shop_asin = ''
    shop_id = 0
    site_id = 0
    site_name = ''
    page = 1
    crawl_classify = False

    def set_job_type(self):
        return 'shop_job'
