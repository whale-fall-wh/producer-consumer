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
import time
from app.models import ProductItemCrawlDate
from app.BaseJob import BaseJob
from app.enums import RedisListKeyEnum


class ProductClassifyCrawler(BaseAmazonCrawler):

    def __init__(self, jobEntity: ProductClassifyJobEntity, http: Http):
        self.classifyCrawlProgressRepository = ClassifyCrawlProgressRepository()
        self.productItemRepository = ProductItemRepository()
        self.keywordRepository = KeywordRepository()
        self.base_url = '{}/dp/{}'   # 亚马逊产品地址
        self.jobEntity = jobEntity
        self.productItem = self.productItemRepository.show(jobEntity.product_item_id)
        if self.productItem and self.productItem.site and self.productItem.product:
            self.url = self.base_url.format(self.productItem.site.domain, self.productItem.product.asin)
            BaseAmazonCrawler.__init__(self, http=http, site=self.productItem.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '?language=en_US'
            if self.is_crawl():
                self.update_crawl_progress()
                Logger().info("地址{}今日已抓取".format(self.url))
                return

            Logger().debug('开始抓取{}产品分类，地址 {}'.format(self.productItem.product.asin, self.url))
            rs = self.get(url=self.url)
            element = ProductClassifyElement(rs.content, self.site_config_entity)
            urls = element.get_element('classify_rank', {})
            if urls:
                for urlObj in urls:
                    url = urlObj.get('url', '')
                    if url:
                        url = self.site.domain + url
                        newJobEntity = ClassifyTreeCrawlJobEntity.instance({
                            'url': url,
                            'url_id': urlObj.get('url_id', ''),
                            'name': urlObj.get('name', ''),
                            'product_id': self.productItem.product.id,
                            'site_id': self.site.id,
                            'product_item_id': self.productItem.id
                        })
                        BaseJob.set_job_by_key(RedisListKeyEnum.classify_tree_crawl_job, newJobEntity)

            self.update_crawl_date()
            self.update_crawl_progress()
        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('classify ' + self.url + ' 请求异常, ' + str(e))

    def is_crawl(self):
        all_crawl_date = self.productItem.all_crawl_date
        if all_crawl_date and all_crawl_date.classify_crawl_date and\
                all_crawl_date.classify_crawl_date.strftime("%Y-%m-%d") \
                >= time.strftime("%Y-%m-%d", time.localtime(time.time() - 10 * 30 * 24 * 60 * 60)):
            return True
        return False

    def update_crawl_progress(self):
        if self.jobEntity.keyword_id:
            keyword = self.keywordRepository.show(self.jobEntity.keyword_id)
            progress = self.classifyCrawlProgressRepository.find_by_model(keyword)
            self.classifyCrawlProgressRepository.add_finished(progress)

    def update_crawl_date(self):
        ProductItemCrawlDate.update_or_create(
            {'product_item_id': self.productItem.id}, {'classify_crawl_date': time.strftime("%Y-%m-%d",
                                                                                            time.localtime())}
        )
