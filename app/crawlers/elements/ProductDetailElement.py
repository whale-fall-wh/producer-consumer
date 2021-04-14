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
        self.product_detail_element = None
        BaseElement.__init__(self, content)

    def _get_product_detail_element(self):
        if self.product_detail_element is not None:
            return self.product_detail_element
        for xpath in self.siteConfig.product_detail_xpath:
            element = self.html.xpath(xpath)
            if element:
                self.product_detail_element = element[0]

                return self.product_detail_element

        return None
