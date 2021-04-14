# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 4:54 下午 
# @Author : wangHua
# @File : ProductClassifyCrawler.py 
# @Software: PyCharm

from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.entities import ProductClassifyJobEntity, ClassifyTreeCrawlJobEntity
from utils import Http, Logger
from app.repositories import ProductItemRepository, KeywordRepository, ClassifyCrawlProgressRepository
from app.exceptions import CrawlErrorException
import requests
from app.crawlers.elements import ProductClassifyElement
from app.services import ProductService


class ProductClassifyCrawler(BaseAmazonCrawler):

    def __init__(self, jobEntity: ProductClassifyJobEntity, http: Http):
        self.productItemRepository = ProductItemRepository()
        self.productService = ProductService()
        self.keywordRepository = KeywordRepository()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.jobEntity = jobEntity
        self.keyword = self.keywordRepository.show(self.jobEntity.keyword_id) if self.jobEntity.keyword_id else None
        self.productItem = self.productItemRepository.show(jobEntity.product_item_id)
        if self.productItem and self.productItem.site and self.productItem.product:
            self.url = self.base_url.format(self.productItem.site.domain, self.productItem.product.asin)
            BaseAmazonCrawler.__init__(self, http=http, site=self.productItem.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'
            if self.productService.is_crawl(self.productItem):
                self.productService.update_keyword_crawl_progress(self.keyword)
                Logger().info("地址{}今日已抓取".format(self.url))
                return

            Logger().debug('开始抓取{}产品分类，地址 {}'.format(self.productItem.product.asin, self.url))
            rs = self.get(url=self.url)
            element = ProductClassifyElement(rs.content, self.site_config_entity)
            self.productService.crawl_product_classify_job(element, self.productItem)

            self.productService.update_keyword_crawl_progress(self.keyword)
        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('classify ' + self.url + ' 请求异常, ' + str(e))
