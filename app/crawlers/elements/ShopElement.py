# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 11:13 上午 
# @Author : wangHua
# @File : ShopElement.py 
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity


class ShopElement(BaseElement):
    """
    产品页面元素
    """

    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config
        BaseElement.__init__(self, content)

    def get_element_asin(self):
        asin = self.html.xpath(self.site_config.shop_asin_xpath)

        return asin
