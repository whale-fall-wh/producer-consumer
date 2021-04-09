# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 4:08 下午 
# @Author : wangHua
# @File : ClassifyJobEntity.py 
# @Software: PyCharm

from app.entities.BaseJobEntity import BaseJobEntity
from app.enums import RedisListKeyEnum


class ClassifyJobEntity(BaseJobEntity):

    product_item_id = 0

    def set_job_type(self):
        return ''

