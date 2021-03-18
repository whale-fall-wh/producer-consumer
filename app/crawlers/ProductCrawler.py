# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.Logger import Logger
from utils.Http import Http
import requests
from app.crawlers.elements.ProductElement import ProductElement
from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.exceptions.CrawlErrorException import CrawlErrorException
from app.entities.ProductJobEntity import ProductJobEntity
from app.repositories.ProductItemRepository import ProductItemRepository


class ProductCrawler(BaseAmazonCrawler):

    def __init__(self, job_entity: ProductJobEntity, http: Http):
        self.product_item_repository = ProductItemRepository()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.job_entity = job_entity
        self.product_item = self.product_item_repository.show(self.job_entity.product_item_id)
        self.product = self.product_item.product

        if self.product_item and self.product_item.product and self.product_item.site:
            self.url = self.base_url.format(self.product_item.site.domain, self.product.asin)
            BaseAmazonCrawler.__init__(self, http=http, site=self.product_item.site)

    def run(self):
        try:
            Logger().debug('开始抓取{}产品，地址 {}'.format(self.product.asin, self.url))
            rs = self.get(url=self.url)
            product_element = ProductElement(content=rs.content, site_config=self.site_config_entity)
            title = product_element.title
            if title:
                Logger().info(product_element.get_all_element())
            else:
                raise CrawlErrorException('页面请求异常, 地址 {}'.format(self.url))
        except requests.exceptions.RequestException:
            raise CrawlErrorException(self.url + '超时')
