# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities.SiteConfigEntity import SiteConfigEntity
import re
import html
from common import replace_multi, str2int, str2float
from app.translates import get_translate_by_locale
from utils.Logger import Logger


class ProductElement(BaseElement):

    def __init__(self, content: bytes, site_config: SiteConfigEntity):
        self.site_config = site_config
        self.translate = get_translate_by_locale(self.site_config.key)
        if self.translate is None:
            self.translate = get_translate_by_locale('en')
            Logger().warning('未获取到翻译器，已使用en翻译，请及时配置')
        BaseElement.__init__(self, content)

    def get_element_title(self) -> [str, None]:
        elements = self.html.xpath(self.site_config.product_title_xpath)
        return ''.join(elements).strip()

    def get_element_price(self) -> str:
        elements = self.html.xpath(self.site_config.product_price_xpath)
        return ''.join(elements).strip()

    def get_element_rating(self) -> float:
        elements = self.html.xpath(self.site_config.product_rating_xpath)
        if elements:
            return self.__deal_with_rating(elements[0].strip())

        return 0

    def get_element_classify_rank(self):
        product_str = self.__get_product_detail_str()
        if not product_str:
            return {}

        matches = []
        for classify_rank_config in self.site_config.product_classify_rank:
            matches = re.findall(self.__deal_re_pattern(classify_rank_config), product_str)
            if matches:
                break
        if not matches:
            return {}
        ranks_tmp = [rank.strip() for rank in matches[0].strip().split('     ')]
        ranks = []
        for rank in ranks_tmp:
            if rank:
                ranks.append(rank)

        return self.__deal_with_rank(ranks)

    def get_element_available_date(self):
        product_str = self.__get_product_detail_str()
        if not product_str:
            return None

        matches = []
        for product_available_date in self.site_config.product_available_date:
            matches = re.findall(self.__deal_re_pattern(product_available_date), product_str)
            if matches:
                break
        if not matches:
            return None

        available_date = ''.join(matches[0].replace(':', '').strip().split('   ')[:1]).strip()
        available_date = self.translate.available_date(available_date)
        if available_date:
            return available_date.strftime('%Y-%m-%d')

        return None

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
        product_html = re.sub("<\s*a[^>]*>[^<]*<\s*/\s*a\s*>", "", product_html)
        product_html = re.sub("<[^>]*?>", "", product_html, flags=re.S)
        product_html = product_html.replace('\n', '     ').replace('\xa0', ' ').replace('\xc2', ' ')

        return '---start---' + product_html + '---end---'

    @staticmethod
    def __deal_re_pattern(classify_rank_config):
        return classify_rank_config[1: len(classify_rank_config)-2]

    def __deal_with_rank(self, ranks: list):
        splits = self.site_config.product_rank_split
        replace = self.site_config.product_rank_replace
        if type(splits) == str:
            splits = [splits]
        rs = dict()
        for rank in ranks:
            for split in splits:
                item = rank.split(split)
                if len(item) == 2:
                    rank_num = str2int(replace_multi(item[0], replace, ''))
                    if rank_num:
                        rs[item[1].replace('(', '').replace(')', '').strip()] = rank_num
                    break

        return rs

    def __deal_with_rating(self, rating):

        rating = replace_multi(rating, self.site_config.product_rating_split, '').strip()
        return str2float(rating, 1)
