# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities.SiteConfigEntity import SiteConfigEntity
import re
import html


class ProductElement(BaseElement):

    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config

        BaseElement.__init__(self, content)

    def get_element_title(self) -> [str, None]:
        elements = self.html.xpath(self.site_config.product_title_xpath)
        return ''.join(elements).strip()

    def get_element_price(self) -> str:
        elements = self.html.xpath(self.site_config.product_price_xpath)
        return ''.join(elements).strip()

    def get_element_rating(self) -> str:
        elements = self.html.xpath(self.site_config.product_rating_xpath)
        return ''.join(elements).strip()

    def get_element_classify_rank(self):
        product_str = self.__get_product_detail_str()
        if not product_str:
            return {}

        matches = []
        for classify_rank_config in self.site_config.product_classify_rank:
            matches = re.findall(self.deal_re_pattern(classify_rank_config), product_str)
            if matches:
                break
        if not matches:
            return {}

        ranks_tmp = [rank.strip() for rank in matches[0].strip().split('   ')]
        ranks = []
        for rank in ranks_tmp:
            if rank:
                ranks.append(rank)

        return ranks

    def get_element_available_date(self):
        return ''

    def get_element_feature_rate(self):
        # 异步接口
        return {}

    def __get_product_detail(self):
        # 可能返回假数据，测试用本地IP是空，用代理正常返回数据
        for xpath in self.site_config.product_detail_xpath:
            element = self.html.xpath(xpath)
            if element:
                return self.get_html(element[0])

        return ''

    def __get_product_detail_str(self):
        # 取出html各种标签，实体等
        product_html = self.__get_product_detail()
        if not product_html:
            return product_html

        product_html = html.unescape(product_html)

        product_html = re.sub('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', "", product_html)
        product_html = re.sub("<\s*style[^>]*>[^<]*<\s*/\s*style\s*>", "", product_html)
        product_html = re.sub("<[^>]*?>", "", product_html, flags=re.S)
        product_html = product_html.replace('\n', '     ').replace('\xa0', ' ').replace('\xc2', ' ')

        return '---start---' + product_html + '---end---'

    @staticmethod
    def deal_re_pattern(classify_rank_config):
        return classify_rank_config[1: len(classify_rank_config)-2]
