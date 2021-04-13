# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 2:49 下午 
# @Author : wangHua
# @File : ProductReviewCrawler.py 
# @Software: PyCharm

from app.crawlers.BaseAmazonCrawler import BaseAmazonCrawler
from app.repositories import ProductItemRepository, ProductRepository, ProductItemReviewRepository
from app.services import ProductService
from app.entities import ProductReviewJobEntity
from utils import Http, Logger
from app.crawlers.elements import ProductReviewListElement, ProductReviewItemElement
import requests
from app.exceptions import CrawlErrorException
import time


class ProductReviewCrawler(BaseAmazonCrawler):

    """
    抓取、保存产品评论数据
    评论可以直接用get请求html或者用post请求review接口
    """

    def __init__(self, job_entity: ProductReviewJobEntity, http: Http):
        self.crawl_next_page = True
        self.crawl_date = None
        self.review_count = 0
        self.base_url = "{}/product-reviews/{}?reviewerType=all_reviews&pageNumber={}&sortBy=recent"
        self.productItemReviewRepository = ProductItemReviewRepository()
        self.productItemRepository = ProductItemRepository()
        self.productRepository = ProductRepository()
        self.productService = ProductService()
        self.job_entity = job_entity
        self.productItem = self.productItemRepository.show(self.job_entity.product_item_id)
        if self.productItem and self.productItem.product and self.productItem.site:
            self.product = self.productItem.product
            if self.productItem.crawl_date:
                self.crawl_date = self.productItem.crawl_date.strftime('%Y-%m-%d')
            self.url = self.base_url.format(self.productItem.site.domain, self.product.asin, self.job_entity.page)
            BaseAmazonCrawler.__init__(self, http=http, site=self.productItem.site)

    def run(self):
        try:
            if self.site_config_entity.has_en_translate:
                self.url = self.url + '&language=en_US'
            Logger().debug('开始抓取 {} - {}站 - 第{}页 评论，地址 {}'.format(self.product.asin,
                                                                  self.site.name,
                                                                  self.job_entity.page,
                                                                  self.url)
                           )
            rs = self.get(url=self.url)
            review_list_element = ProductReviewListElement(content=rs.content, site_config=self.site_config_entity)
            review_list = getattr(review_list_element, 'review_list')
            if review_list:
                Logger().debug('reviews element ' + review_list.__str__())
                for review_item in review_list:
                    item_content = review_list_element.get_content(review_item)
                    review_item_element = ProductReviewItemElement(item_content, self.site_config_entity)
                    if getattr(review_item_element, 'uuid') and getattr(review_item_element, 'title'):
                        data = review_item_element.get_all_element()
                        data['attr'], data['color'], data['size'] = review_item_element.get_attr_color_size()
                        if data['date'] and self.crawl_date and (self.crawl_date > data['date']) \
                                and self.job_entity.type == 'new':
                            self.crawl_next_page = False
                        self.review_count += 1
                        self.save(data)
                self.productService.update_product_item_daily_data(self.productItem)

            self.crawl_next_page = self.check_next_page() and self.crawl_next_page
            if not self.crawl_next_page:
                self.productItem.update({'crawl_date': time.strftime('%Y-%m-%d')})

        except requests.exceptions.RequestException as e:
            raise CrawlErrorException('review ' + self.url + ' 请求异常, ' + str(e))

    def check_next_page(self):
        return self.review_count >= 10

    def save(self, data: dict):
        if data:
            not_empty_list = filter(lambda x_y: x_y[1] is not None, data.items())
            data = {key: value for key, value in not_empty_list}
            data['product_item_id'] = self.productItem.id
            data['product_id'] = self.product.id
            data['site_id'] = self.productItem.site_id
            data['is_processed'] = 1
            self.productItemReviewRepository.update_or_create({'uuid': data['uuid']}, data)
