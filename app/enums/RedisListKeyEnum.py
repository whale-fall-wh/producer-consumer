# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 2:56 下午 
# @Author : wangHua
# @File : RedisListKeyEnum.py 
# @Software: PyCharm

from app.enums.BaseEnum import BaseEnum


class RedisListKeyEnum(BaseEnum):

    # 添加新的Asin时创建的asin
    product_add_crawl_job = 'product_add_crawl_job'

    product_crawl_job = 'product_crawl_job'

    product_review_crawl_job = 'product_review_crawl_job'

    shop_crawl_job = 'shop_crawl_job'
