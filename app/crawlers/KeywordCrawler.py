# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 10:02 上午 
# @Author : wangHua
# @File : KeywordCrawler.py
# @Software: PyCharm

from .BaseAmazonCrawler import BaseAmazonCrawler
from utils import Http, Logger
from app.entities import KeywordJobEntity, ProductClassifyJobEntity
from app.enums import ProductTypeEnum, RedisListKeyEnum
from app.repositories import ProductItemRepository, KeywordRepository, SiteRepository
from .elements import SearchElement
from app.models import ProductItem, Product, ProductTypeProductRelation
from app.BaseJob import BaseJob
from app.exceptions import CrawlErrorException
import requests


class KeywordCrawler(BaseAmazonCrawler):
    """
    keyword在被添加的时候，redis相关队列插入任务即可触发抓取
    """
    # ignore = True
    def __init__(self, jobEntity: KeywordJobEntity, http: Http):
        self.asin_list = 0
        self.jobEntity = jobEntity
        self.crawl_next_page = True
        self.siteRepository = SiteRepository()
        self.productItemRepository = ProductItemRepository()
        self.keywordRepository = KeywordRepository()
        self.keyword = self.keywordRepository.show(self.jobEntity.keyword_id)
        self.base_url = '{}/s?k={}&page={}'
        site = self.siteRepository.show(self.jobEntity.site_id)
        if site and self.keyword:
            self.url = self.base_url.format(site.domain, self.keyword.name, self.jobEntity.page)
            BaseAmazonCrawler.__init__(self, http=http, site=site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'
            Logger().debug('开始抓取{}关键字，地址 {}'.format(self.keyword.name, self.url))
            rs = self.get(url=self.url)
            shopElement = SearchElement(content=rs.content, site_config=self.site_config_entity)
            if not shopElement.check_page(self.keyword.name):
                raise CrawlErrorException("search页面抓取异常")
            all_asin_list = getattr(shopElement, 'asin', [])
            asin_list = list(filter(lambda x: x, all_asin_list))
            for asin in asin_list:
                productItem = self.save_asin(asin)
                newJobEntity = ProductClassifyJobEntity.instance({
                    'product_item_id': productItem.id,
                    'keyword_id': self.keyword.id
                })
                BaseJob.set_job_by_key(RedisListKeyEnum.product_classify_crawl_job, newJobEntity)
                self.jobEntity.current_num += 1
                if self.jobEntity.current_num >= self.jobEntity.max_num:
                    break
            self.asin_list = len(asin_list)
            self.crawl_next_page = self.check_next_page()
        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('classify ' + self.url + ' 请求异常, ' + str(e))

    def save_asin(self, asin: str):
        product = Product.update_or_create({'asin': asin})
        ProductTypeProductRelation.update_or_create({
            'product_id': product.id,
            'product_type_id': ProductTypeEnum.TYPE_ID_SEARCH
        })
        return ProductItem.update_or_create({'product_id': product.id, 'site_id': self.site.id})

    def check_next_page(self):
        """
        翻页：当前页有数据并且抓取的数量小于总抓取数
        :return:
        """
        return self.asin_list and self.jobEntity.current_num < self.jobEntity.max_num
