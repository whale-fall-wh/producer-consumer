# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 3:10 下午 
# @Author : wangHua
# @File : ProductReviewItemElement.py 
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity
from app.translates import get_translate_by_locale
from utils import Logger
from common import replace_multi, str2int, str2float


class ProductReviewItemElement(BaseElement):
    """
    评论详情元素
    """
    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config
        self.translate = get_translate_by_locale(self.site_config.key)
        if self.translate is None:
            self.translate = get_translate_by_locale('en')
            Logger().warning('未获取到 {} 翻译器，已使用en翻译，请及时配置'.format(self.site_config.key))
        BaseElement.__init__(self, content)

    def get_element_title(self):
        elements = self.html.xpath(self.site_config.product_review_title_xpath)

        return ''.join(elements).strip()

    def get_element_uuid(self):
        elements = self.html.xpath(self.site_config.product_review_uuid_xpath)

        return elements[0].strip() if elements else None

    def get_element_username(self):
        elements = self.html.xpath(self.site_config.product_review_username_xpath)

        return ''.join(elements).strip()

    def get_element_date(self):
        elements = self.html.xpath(self.site_config.product_review_date_xpath)

        review_date = elements[0].strip() if elements else None

        return self.__deal_with_date(review_date, self.site_config.product_review_data_split)

    def get_element_rating(self):
        elements = self.html.xpath(self.site_config.product_review_rating_xpath)

        return self.__deal_with_rating(''.join(elements).strip())

    def get_element_helpers(self):
        elements = self.html.xpath(self.site_config.product_review_helpful_xpath)

        return self.__deal_with_helpers(elements)

    def get_element_content(self):
        elements = self.html.xpath(self.site_config.product_review_content_xpath)

        return ''.join(elements).strip()

    def get_element_detail_link(self):
        elements = self.html.xpath(self.site_config.product_review_detail_link_xpath)

        return ''.join(elements).strip()

    @staticmethod
    def __deal_with_helpers(elements: list):
        if not elements:
            return 0
        helper_str = replace_multi(''.join(elements).strip(), [",", "."], '').split(' ')[0]

        return str2int(helper_str, 1)

    def __deal_with_rating(self, rating):

        rating = replace_multi(rating, self.site_config.product_rating_split, '').strip()
        return str2float(rating, 1)

    def get_attr_color_size(self):
        attr = dict()
        attr_str = []
        elements = self.html.xpath(self.site_config.product_review_color_size_xpath)
        for element in elements:
            item = element.split(':')
            if len(item) >= 2:
                attr[item[0].strip()] = item[1].strip()
                attr_str.append(item[1].strip())
        color = attr.get(self.site_config.product_review_color_name, '')
        size = attr.get(self.site_config.product_review_size_name, '')

        return '|'.join(attr_str), color, size

    def __deal_with_date(self, review_date, configs):
        if type(configs) == list:
            for config in configs:
                rs = self.__deal_with_date(review_date, config)
                if rs:
                    return rs

        if not configs:
            return None

        review_date = ''.join(review_date.split(configs)[-1:])
        review_date = self.translate.available_date(review_date)
        if review_date:
            return review_date.strftime('%Y-%m-%d')

        return None


if __name__ == '__main__':
    a = []
    print(''.join(a[-1:]))
