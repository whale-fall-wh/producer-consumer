# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 1:38 下午 
# @Author : wangHua
# @File : ClassifyTreeCrawler.py 
# @Software: PyCharm

from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.entities import ClassifyTreeCrawlJobEntity
from utils import Http, Logger
from app.repositories import ProductItemRepository, ProductClassifyRepository
from app.exceptions import CrawlErrorException
import requests
from app.crawlers.elements import ClassifyTreeElement
from app.models import ProductClassify, ProductClassifyProductItemRelation


class ClassifyTreeCrawler(BaseAmazonCrawler):

    def __init__(self, jobEntity: ClassifyTreeCrawlJobEntity, http: Http):
        self.productItemRepository = ProductItemRepository()
        self.productClassifyRepository = ProductClassifyRepository()
        self.jobEntity = jobEntity
        self.url = jobEntity.url
        self.productItem = self.productItemRepository.show(jobEntity.product_item_id)

        if self.productItem and self.productItem.product and self.productItem.site:
            BaseAmazonCrawler.__init__(self, http=http, site=self.productItem.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'

            Logger().debug('开始抓取分类数信息，地址 {}'.format(self.url))
            rs = self.get(self.url)
            element = ClassifyTreeElement(rs.content, self.site.site_config)
            trees = element.crawl_classify_tree(self.jobEntity.url, self.jobEntity.name)
            self.store_tree(trees)

        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('classify tree ' + self.url + ' 请求异常, ' + str(e))

    def store_tree(self, trees, parentProductClassify: ProductClassify = None):
        for tree in trees:
            items = tree.pop('items', [])
            if parentProductClassify:
                url_id = tree.get('url_id', '')
                if url_id:
                    classify = self.productClassifyRepository.update_or_create_children(
                        parentProductClassify,
                        {'url_id': url_id},
                        tree
                    )
                    if tree.get('name', ''):
                        self.sync_product_item(classify.id)
                else:
                    classify = None
            else:
                classify = self.productClassifyRepository.update_or_create_node(
                    {'classify_name': tree.get('classify_name', '')},
                    tree
                )
            if items and classify is not None:
                self.store_tree(items, classify)

    def sync_product_item(self, classify_id):
        ProductClassifyProductItemRelation.update_or_create({
            'product_item_id': self.productItem.id,
            'product_classify_id': classify_id
        })
