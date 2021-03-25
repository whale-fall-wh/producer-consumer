# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 10:02 上午 
# @Author : wangHua
# @File : ProductReviewJobEntity.py 
# @Software: PyCharm


from app.entities.BaseJobEntity import BaseJobEntity


class ProductReviewJobEntity(BaseJobEntity):
    product_asin = ''
    product_id = 0
    site_id = 0
    site_name = ''
    product_item_id = 0
    page = 1
    type = 'new'

    def set_job_type(self):
        return 'product_review_job'
