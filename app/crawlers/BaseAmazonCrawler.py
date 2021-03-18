# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from .elements.AmazonExceptionElement import AmazonExceptionElement
from app.exceptions.NotFoundException import NotFoundException
from utils.Http import Http
from app.crawlers.Captcha import Captcha
from abc import ABCMeta, abstractmethod
from app.models import Site
from app.entities.SiteConfigEntity import SiteConfigEntity


class BaseAmazonCrawler(metaclass=ABCMeta):
    """抓取亚马逊网站基类"""

    @abstractmethod     # 抽象方法，子类必须实现，类似interface
    def run(self):
        pass

    def __init__(self, http: Http, site: Site):
        # 是否需要验证码
        self.need_captcha_flag = False
        self.http = http
        self.site = site
        self.site_config_entity = SiteConfigEntity.instance(self.init_site_config())
        self.run()

    def init_site_config(self):
        if self.site.site_config and type(self.site.site_config.config) == dict:
            return self.site.site_config.config
        else:
            return {}

    # TODO: 使用装饰器来做请求异常处理。验证码可以做三次尝试
    def request(self, method, url: str, **kwargs):

        rs = self.http.request(method=method, url=url, **kwargs)
        exception = AmazonExceptionElement(content=rs.content, site_config_entity=self.site_config_entity)
        if exception.not_found():
            raise NotFoundException('{} not_found'.format(url))

        self.need_captcha_flag = exception.need_validate()
        if self.need_captcha_flag:
            Captcha('https://www.amazon.com', http=self.http, html=rs.text)
            rs = self.http.request(method=method, url=url, **kwargs)

        return rs

    def get(self, url: str, **kwargs):
        return self.request(method='GET', url=url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request(method='GET', url=url, **kwargs)
