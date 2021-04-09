# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from .elements.AmazonExceptionElement import AmazonExceptionElement
from app.exceptions import NotFoundException, CrawlErrorException
from utils.Http import Http
from app.crawlers.Captcha import Captcha
from abc import ABCMeta, abstractmethod
from app.models import Site
from .traits.AmazonSiteConfig import AmazonSiteConfig


class BaseAmazonCrawler(AmazonSiteConfig, metaclass=ABCMeta):
    """抓取亚马逊网站基类"""

    @abstractmethod     # 抽象方法，子类必须实现，类似interface
    def run(self):
        pass

    def __init__(self, http: Http, site: Site):
        # 是否需要验证码
        self.need_captcha_flag = False
        self.http = http
        AmazonSiteConfig.__init__(self, site)

        self.run()

    # TODO: 使用装饰器来做请求异常处理。验证码可以做三次尝试
    def request(self, method, url: str, **kwargs):

        rs = self.http.request(method=method, url=url, **kwargs)
        exception = AmazonExceptionElement(content=rs.content, site_config_entity=self.site_config_entity)
        if exception.error_500():
            raise CrawlErrorException('{} 500+ error'.format(url))
        if exception.not_found():
            raise NotFoundException('{} not_found'.format(url))

        self.need_captcha_flag = exception.need_validate()
        if self.need_captcha_flag:
            Captcha(self.site.domain, http=self.http, html=rs.text)
            rs = self.http.request(method=method, url=url, **kwargs)

        return rs

    def get(self, url: str, **kwargs):
        return self.request(method='GET', url=url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request(method='GET', url=url, **kwargs)
