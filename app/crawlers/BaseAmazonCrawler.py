# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from .elements import AmazonExceptionElement
from app.exceptions import NotFoundException, CrawlErrorException
from utils.Http import Http
from app.crawlers.Captcha import Captcha
from abc import ABCMeta, abstractmethod
from app.models import Site
from .traits.AmazonSiteConfig import AmazonSiteConfig
from utils import Logger


class BaseAmazonCrawler(AmazonSiteConfig, metaclass=ABCMeta):
    """抓取亚马逊网站基类"""

    @abstractmethod     # 抽象方法，子类必须实现，类似interface
    def run(self):
        pass

    def __init__(self, http: Http, site: Site):
        self.http = http
        AmazonSiteConfig.__init__(self, site)

        self.run()

    # TODO: 使用装饰器来做请求异常处理。
    def request(self, method, url: str, request_time=1, **kwargs):
        rs = self.http.request(method=method, url=url, **kwargs)
        exception = AmazonExceptionElement(content=rs.content, site_config_entity=self.site_config_entity)
        if exception.error_500():
            raise CrawlErrorException('{} 500+ error'.format(url))
        if exception.not_found():
            raise NotFoundException('{} not_found'.format(url))

        if exception.need_validate() and request_time <= 3:
            Captcha(self.site.domain, http=self.http, html=rs.text)
            Logger().info("尝试第{}次重试".format(request_time))
            rs = self.request(method=method, url=url, request_time=request_time+1, **kwargs)

        return rs

    def get(self, url: str, **kwargs):
        return self.request(method='GET', url=url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request(method='POST', url=url, **kwargs)
