# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 10:31 上午 
# @Author : wangHua
# @File : SearchElement.py 
# @Software: PyCharm

from .BaseElement import BaseElement
from app.entities import SiteConfigEntity


class SearchElement(BaseElement):
    """
    产品页面元素
    """
    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config
        BaseElement.__init__(self, content)

    def get_element_asin(self):
        return self.html.xpath(self.site_config.keyword_asin_xpath)

    def check_page(self, keyword: str):
        xpath = "//span[contains(text(), '{}')]".format(keyword)

        return self.html.xpath(xpath)
