# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 3:03 下午 
# @Author : wangHua
# @File : ProductReviewListElement.py
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity


class ProductReviewListElement(BaseElement):
    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config
        BaseElement.__init__(self, content)

    def get_element_review_list(self):
        return self.html.xpath(self.site_config.product_review_list_xpath)
