# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 5:21 下午 
# @Author : wangHua
# @File : SiteConfigEntity.py 
# @Software: PyCharm

from .BaseEntity import BaseEntity


class SiteConfigEntity(BaseEntity):
    key = ''
    error_500 = '//input[@name="cs_503_search"]'     # 503异常页面也会有id=g，要先判断是否页面异常，再判断not_found
    page_not_found = '//*[@id="g"]'     # 这个如果有其他页面也在使用id=g就有异常了，就会被判定成not_found
    validate_captcha = '//form[@action="/errors/validateCaptcha"]'

    product_title_xpath = '//*[@id="productTitle"]/text()'
    product_price_xpath = '//*[@id="priceblock_ourprice"]/text()'
    product_rating_xpath = '//*[@id="acrPopover"]/@title'
    product_detail_xpath = [
        '//*[@id="prodDetails"]',
        '//*[@id="detailBulletsWrapper_feature_div"]',
        '//*[@id="productDetails_detailBullets_sections1"]',
        '//*[@id="productDetails_db_sections"]'
    ]

    product_classify_rank = []
    product_rank_replace = []
    product_available_date = []
    product_rank_split = None
    product_rating_split = None
    product_available_date_format = None
    product_available_date_locale = None
    product_price_unit = ''

    product_review_list_xpath = '//div[@id="cm_cr-review_list"]/div[@data-hook="review"]'
    product_review_title_xpath = '//*[@data-hook="review-title"]//text()'   # 只筛选本站点的，其他国家的先排除
    product_review_uuid_xpath = '//@id'
    product_review_username_xpath = '//*[@class="a-profile-name"]/text()'
    product_review_date_xpath = '//span[@data-hook="review-date"]/text()'
    product_review_rating_xpath = '//i[contains(@data-hook,"review-star-rating")]//text()'
    product_review_content_xpath = '//span[@data-hook="review-body"]//text()'
    product_review_color_size_xpath = '//a[@data-hook="format-strip"]/text()'
    product_review_helpful_xpath = '//*[@data-hook="helpful-vote-statement"]//text()'
    product_review_detail_link_xpath = '//*[@data-hook="review-title"]/@href'

    product_review_color_name = None
    product_review_size_name = None
    product_review_data_split = None

    shop_asin_xpath = '//div[@data-asin]/@data-asin'

    has_en_translate = False

    def to_object(self, data: dict):
        # TODO: 通过映射关系来实现
        self.key = data.get('product', {}).get('available_date_locale', '')
        self.product_classify_rank = data.get('product', {}).get('classify_rank', [])
        self.product_available_date = data.get('product', {}).get('available_date', [])
        self.product_rank_split = data.get('product', {}).get('rank_split', [])
        self.product_rank_replace = data.get('product', {}).get('rank_replace', [])
        self.product_available_date_format = data.get('product', {}).get('rank_split', [])
        self.product_available_date_locale = data.get('product', {}).get('rank_split', '')
        self.has_en_translate = data.get('has_en_translate', '')
        self.product_rating_split = data.get('product', {}).get('rating_split', [])
        self.product_price_unit = data.get('product', {}).get('unit', '')
        self.product_review_color_name = data.get('review', {}).get('color_name', '')
        self.product_review_size_name = data.get('review', {}).get('size_name', '')
        self.product_review_data_split = data.get('review', {}).get('date', {}).get('split', '')

        return self
