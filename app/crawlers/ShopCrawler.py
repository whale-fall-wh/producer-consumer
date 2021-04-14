# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 10:44 上午 
# @Author : wangHua
# @File : ShopCrawler.py 
# @Software: PyCharm

from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.entities import ShopJobEntity, ProductJobEntity, ProductReviewJobEntity
from utils import Http, Logger
from app.repositories import ShopItemRepository, ProductRepository
from .elements import ShopElement
import requests
from app.models import Product, ProductTypeProductRelation, ProductItem
from app.exceptions import CrawlErrorException
from app.enums import ProductTypeEnum, RedisListKeyEnum
from app.BaseJob import BaseJob
from app.services import ProductService


class ShopCrawler(BaseAmazonCrawler):

    def __init__(self, jobEntity: ShopJobEntity, http: Http):
        self.base_url = '{}/s?me={}&page={}'   # 亚马逊产品地址
        self.asin_list = 0
        self.crawl_next_page = True
        self.jobEntity = jobEntity
        self.shopItemRepository = ShopItemRepository()
        self.productService = ProductService()
        self.productRepository = ProductRepository()
        self.shopItem = self.shopItemRepository.show(self.jobEntity.shop_item_id)
        if self.shopItem:
            self.shop = self.shopItem.shop
            if self.shopItem.site and self.shop:
                self.url = self.base_url.format(self.shopItem.site.domain, self.shop.asin, self.jobEntity.page)
                BaseAmazonCrawler.__init__(self, http=http, site=self.shopItem.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '&language=en_US'
            Logger().debug('开始抓取{}店铺产品，地址 {}'.format(self.shop.asin, self.url))
            rs = self.get(url=self.url)
            shopElement = ShopElement(content=rs.content, site_config=self.site_config_entity)
            all_asin_list = getattr(shopElement, 'asin', [])
            asin_list = list(filter(lambda x: x, all_asin_list))
            for asin in asin_list:
                product = self.productRepository.update_or_create({'asin': asin})
                productItem = self.save(product)
                self.crawl_product_job(productItem)
            self.asin_list = len(asin_list)
            self.productService.add_shop_progress_total(self.shopItem, self.asin_list)
            self.crawl_next_page = self.check_next_page()
        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('shop ' + self.url + ' 请求异常, ' + str(e))

    def check_next_page(self):
        return self.asin_list >= 16

    def save(self, product: Product):
        ProductTypeProductRelation.update_or_create({
            'product_id': product.id,
            'product_type_id': ProductTypeEnum.TYPE_ID_SHOP
        })

        return ProductItem.update_or_create({'product_id': product.id, 'site_id': self.site.id},
                                            {'shop_item_id': self.shopItem.id})

    def crawl_product_job(self, productItem: ProductItem):
        data = {
            'product_asin': productItem.product.asin,
            'product_id': productItem.product.id,
            'site_id': productItem.site.id,
            'site_name': productItem.site.name,
            'product_item_id': productItem.id,
            'shop_item_id': self.jobEntity.shop_item_id,
            'crawl_classify': self.jobEntity.crawl_classify
        }

        BaseJob.set_job_by_key(RedisListKeyEnum.product_crawl_job, ProductJobEntity.instance(data))
        BaseJob.set_job_by_key(RedisListKeyEnum.product_review_crawl_job, ProductReviewJobEntity.instance(data))
