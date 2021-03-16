# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.Logger import Logger
from utils.Http import Http
import requests
from app.crawlers.elements.ProductTitle import get_title
from app.crawlers.BaseAmazonSpider import BaseAmazonSpider
from app.exceptions.SpiderErrorException import SpiderErrorException
from app.entities.ProductJobEntity import ProductJobEntity
from app.repositories.ProductItemRepository import ProductItemRepository


class ProductCrawler(BaseAmazonSpider):

    def __init__(self, job_entity: ProductJobEntity, http: Http):
        self.product_item_repository = ProductItemRepository()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.job_entity = job_entity
        self.product_item = self.product_item_repository.show(self.job_entity.product_item_id)
        self.product = self.product_item.product
        self.site = self.product_item.site

        if self.product_item and self.product_item.product and self.product_item.site:
            self.url = self.base_url.format(self.site.domain, self.product.asin)
            BaseAmazonSpider.__init__(self, http=http)

    def run(self):
        try:
            Logger().debug('开始抓取{}产品，地址 {}'.format(self.product.asin, self.url))
            rs = self.get(url=self.url)
            title = get_title(rs.text)
            if title:
                Logger().info(title)
            else:
                Logger().error(self.product.asin + '抓取失败，' + '地址 ' + self.url)
        except requests.exceptions.RequestException:
            raise SpiderErrorException(self.url + '超时')
