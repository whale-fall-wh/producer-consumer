# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.entities.BaseJobEntity import BaseJobEntity


class ProductJobEntity(BaseJobEntity):
    product_asin = ''
    product_id = 0
    site_id = 0
    site_name = ''
    product_item_id = 0

    def set_job_type(self):
        return 'product_job'
