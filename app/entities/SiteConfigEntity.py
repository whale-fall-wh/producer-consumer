# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 5:21 下午 
# @Author : wangHua
# @File : SiteConfigEntity.py 
# @Software: PyCharm

from .BaseEntity import BaseEntity


class SiteConfigEntity(BaseEntity):
    key = ''
    page_not_found = '//*[@id="g"]'     # 这个如果有其他页面也在使用id=g就有异常了，就会被判定成not_found
    validate_captcha = '//form[@action="/errors/validateCaptcha"]'

    product_title_xpath = '//*[@id="productTitle"]/text()'
    product_price_xpath = '//*[@id="priceblock_ourprice"]/text()'
    product_rating_xpath = '//span[@data-hook="rating-out-of-text"]/text()'
    product_detail_xpath = [
        '//*[@id="prodDetails"]',
        '//*[@id="detailBulletsWrapper_feature_div"]',
        '//*[@id="productDetails_detailBullets_sections1"]',
        '//*[@id="productDetails_db_sections"]'
    ]

    product_classify_rank = []
    product_available_date = []
    product_rank_split = None
    product_available_date_format = None
    product_available_date_locale = None

    has_en_translate = False

    def to_object(self, data: dict):
        # TODO: 通过映射关系来实现
        self.key = data.get('product', {}).get('available_date_locale', '')
        self.product_classify_rank = data.get('product', {}).get('classify_rank', [])
        self.product_available_date = data.get('product', {}).get('available_date', [])
        self.product_rank_split = data.get('product', {}).get('rank_split', [])
        self.product_available_date_format = data.get('product', {}).get('rank_split', [])
        self.product_available_date_locale = data.get('product', {}).get('rank_split', '')
        self.has_en_translate = data.get('product', {}).get('has_en_translate', '')

        return self
