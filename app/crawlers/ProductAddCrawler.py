# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/26 4:00 下午 
# @Author : wangHua
# @File : ProductAddCrawler.py 
# @Software: PyCharm

from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from utils import Http
from app.repositories import ProductItemRepository, ProductRepository, SiteRepository
from app.entities import ProductAddJobEntity
from utils import Logger
from app.crawlers.elements import ProductElement
from app.exceptions import CrawlErrorException, NotFoundException
import requests


class ProductAddCrawler(BaseAmazonCrawler):

    """
    可以在asin被添加时，插入对应的队列相关任务
    """

    def __init__(self, jobEntity: ProductAddJobEntity, http: Http):
        self.productItemRepository = ProductItemRepository()
        self.productRepository = ProductRepository()
        self.siteRepository = SiteRepository()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.jobEntity = jobEntity
        self.product = self.productRepository.show(self.jobEntity.product_id)
        self.site = self.siteRepository.show(self.jobEntity.site_id)
        self.productItem = None
        if self.product and self.site:
            self.url = self.base_url.format(self.site.domain, self.product.asin)
            BaseAmazonCrawler.__init__(self, http=http, site=self.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'
            Logger().debug('新增asin{}开始抓取，地址 {}'.format(self.product.asin, self.url))
            rs = self.get(url=self.url)
            product_element = ProductElement(content=rs.content, site_config=self.site_config_entity)
            title = getattr(product_element, 'title')
            if title:
                self.productItem = self.productItemRepository.update_or_create({
                    'product_id': self.product.id,
                    'site_id': self.site.id
                })
            else:
                raise CrawlErrorException('页面请求异常, 地址 {}'.format(self.url))
        except requests.exceptions.RequestException:
            raise CrawlErrorException('product ' + self.url + '请求异常')
        except NotFoundException:
            pass
