# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 5:19 下午 
# @Author : wangHua
# @File : ProductDetailElement.py 
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity


class ProductDetailElement(BaseElement):

    def __init__(self, content: bytes, siteConfig: SiteConfigEntity):
        self.siteConfig = siteConfig
        BaseElement.__init__(self, content)

    def _get_product_detail_element(self):
        for xpath in self.siteConfig.product_detail_xpath:
            element = self.html.xpath(xpath)
            if element:
                return element[0]

        return None
