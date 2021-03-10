# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from utils.Http import Http
from crawlers.Captcha import Captcha


class BaseAmazonSpider:
    is_error = False

    def run(self):
        pass

    def __init__(self, http: Http):
        self.http = http
        self.run()

    def check_need_validate(self, html):
        html = etree.HTML(html)
        if html.xpath("//form[@action='/errors/validateCaptcha']"):
            self.is_error = True

        return self.is_error

    def get(self, url: str, **kwargs):
        rs = self.http.get(url=url, **kwargs)
        if self.check_need_validate(rs.text):
            # 固定的美国，需要改成动态的
            Captcha('https://www.amazon.com', http=self.http, html=rs.text)
            rs = self.http.get(url=url, **kwargs)

        return rs
