# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from utils.Http import Http
from crawlers.Captcha import Captcha
from abc import ABCMeta, abstractmethod


class BaseAmazonSpider(metaclass=ABCMeta):
    """抓取亚马逊网站基类"""

    # 是否需要验证码
    need_captcha_flag = False

    @abstractmethod     # 抽象方法，子类必须实现，类似interface
    def run(self):
        pass

    def __init__(self, http: Http):
        self.http = http
        self.run()

    def check_need_validate(self, html):
        html = etree.HTML(html)
        if html.xpath("//form[@action='/errors/validateCaptcha']"):
            self.need_captcha_flag = True

        return self.need_captcha_flag

    def get(self, url: str, **kwargs):
        rs = self.http.get(url=url, **kwargs)
        if self.check_need_validate(rs.text):
            # 固定的美国，需要改成动态的， 可以
            Captcha('https://www.amazon.com', http=self.http, html=rs.text)
            rs = self.http.get(url=url, **kwargs)

        return rs
