# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils import Logger
from utils.Http import Http
import requests
from app.crawlers.elements import ProductElement
from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.exceptions import CrawlErrorException
from app.entities import ProductJobEntity
from app.repositories import ProductItemRepository, ProductRepository
from app.services import ProductService
from copy import deepcopy


class ProductCrawler(BaseAmazonCrawler):

    def __init__(self, job_entity: ProductJobEntity, http: Http):
        self.product_item_repository = ProductItemRepository()
        self.product_repository = ProductRepository()
        self.product_service = ProductService()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.job_entity = job_entity
        self.product_item = self.product_item_repository.show(self.job_entity.product_item_id)

        if self.product_item and self.product_item.product and self.product_item.site:
            self.product = self.product_item.product
            self.url = self.base_url.format(self.product_item.site.domain, self.product.asin)
            BaseAmazonCrawler.__init__(self, http=http, site=self.product_item.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'
            Logger().debug('开始抓取{}产品，地址 {}'.format(self.product.asin, self.url))
            rs = self.get(url=self.url)
            product_element = ProductElement(content=rs.content, site_config=self.site_config_entity)
            title = getattr(product_element, 'title')
            if title:
                data = product_element.get_all_element()
                no_empty_data = dict()
                for k, v in data.items():
                    if v:
                        no_empty_data[k] = v
                self.save_data(no_empty_data)
            else:
                raise CrawlErrorException('页面请求异常, 地址 {}'.format(self.url))
        except requests.exceptions.RequestException:
            raise CrawlErrorException('product ' + self.url + '请求异常')

    def save_data(self, no_empty_data: dict):
        rating = no_empty_data.get('rating', 0.0)
        available_date = no_empty_data.get('available_date', None)
        price = no_empty_data.get('price', '')
        feature_rate = no_empty_data.get('feature_rate', {})
        classify_rank = no_empty_data.get('classify_rank', {})
        product_dict = {}
        if rating:
            product_dict['rating'] = rating
        if available_date:
            product_dict['available_date'] = available_date
        if self.product:
            self.product_repository.update_by_id(self.product.id, product_dict)
        if self.product_item:
            product_item_dict = deepcopy(product_dict)
            if price:
                product_item_dict['price'] = price
            if feature_rate:
                product_item_dict['feature_rate'] = feature_rate
            if classify_rank:
                product_item_dict['classify_rank'] = self.handle_ranks_dict(classify_rank)
            self.product_item.update(product_item_dict)

        self.product_service.update_product_item_daily_data(self.product_item)
        self.product_service.update_product_item_daily_rank(self.product_item, ranks=classify_rank)

    @staticmethod
    def handle_ranks_dict(classify_rank: dict):
        if classify_rank:
            return ["{} in {}".format(rank, name) for name, rank in classify_rank.items()]
        else:
            return []
