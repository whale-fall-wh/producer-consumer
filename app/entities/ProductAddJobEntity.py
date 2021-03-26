# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/26 4:03 下午 
# @Author : wangHua
# @File : ProductAddJobEntity.py 
# @Software: PyCharm

from app.entities.BaseJobEntity import BaseJobEntity


class ProductAddJobEntity(BaseJobEntity):
    product_asin = ''
    product_id = ''
    site_id = 0
    site_name = ''

    def set_job_type(self):
        return 'product_add_job'
