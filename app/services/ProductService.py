# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 3:00 下午 
# @Author : wangHua
# @File : ProductService.py 
# @Software: PyCharm

from app.repositories import *
from utils.Singleton import singleton
from app.models import *
from time import strftime
from app.crawlers.elements import ProductClassifyElement
from app.entities import ClassifyTreeCrawlJobEntity
from app.BaseJob import BaseJob
from app.enums import RedisListKeyEnum
import time


@singleton
class ProductService(object):
    productRepository = ProductRepository()
    classifyRepository = ClassifyRepository()
    productItemDailyRankRepository = ProductItemDailyRankRepository()
    productItemReviewRepository = ProductItemReviewRepository()
    productItemRepository = ProductItemRepository()
    productItemDailyDataRepository = ProductItemDailyDataRepository()
    keywordRepository = KeywordRepository()
    classifyCrawlProgressRepository = ClassifyCrawlProgressRepository()
    shopItemRepository = ShopItemRepository()

    def update_product_item_daily_rank(self, product_item: ProductItem, ranks: dict):
        if ranks:
            for classify_name, rank in ranks.items():
                classify = self.classifyRepository.update_or_create({'name': classify_name})
                classify = self.productItemDailyRankRepository.model.update_or_create(
                    {'date': strftime('%Y-%m-%d'), 'classify_id': classify.id, 'product_item_id': product_item.id},
                    {'rank': rank}
                )
                product_item.daily_ranks.append(classify)

    def update_product_item_daily_data(self, product_item: ProductItem):
        review_date = self.productItemReviewRepository.get_last_review_date(product_item_id=product_item.id)

        reviews = self.productItemReviewRepository.get_review_count(product_item_id=product_item.id)
        product_item.update({
            'reviews': reviews,
            'review_date': review_date
        })
        self.productItemDailyDataRepository.update_or_create(
            {'date': strftime('%Y-%m-%d'), 'product_item_id': product_item.id},
            {
                'product_id': product_item.product_id,
                'rating': product_item.rating,
                'reviews': product_item.reviews,
                'helpers': 0,
                'questions': product_item.questions,
                'answers': product_item.answers,
                'price': product_item.price,
                'classify_rank': product_item.classify_rank,
                'feature_rate': product_item.feature_rate if product_item.feature_rate else {}
            }
        )
        if product_item.site.short_name == 'us':
            product_item.product.update({
                'review_date': review_date,
                'reviews': reviews
            })

    @staticmethod
    def crawl_product_classify_job(element: ProductClassifyElement, productItem: ProductItem):
        urls = element.get_element('classify_rank', {})
        if urls:
            for urlObj in urls:
                url = urlObj.get('url', '')
                if url:
                    url = productItem.site.domain + url
                    newJobEntity = ClassifyTreeCrawlJobEntity.instance({
                        'url': url,
                        'url_id': urlObj.get('url_id', ''),
                        'name': urlObj.get('name', ''),
                        'product_id': productItem.product.id,
                        'site_id': productItem.site.id,
                        'product_item_id': productItem.id
                    })
                    BaseJob.set_job_by_key(RedisListKeyEnum.classify_tree_crawl_job, newJobEntity)

        ProductItemCrawlDate.update_or_create(
            {'product_item_id': productItem.id}, {'classify_crawl_date': time.strftime("%Y-%m-%d", time.localtime())}
        )

    @staticmethod
    def is_crawl(productItem: ProductItem):
        all_crawl_date = productItem.all_crawl_date
        if all_crawl_date and all_crawl_date.classify_crawl_date and\
                all_crawl_date.classify_crawl_date.strftime("%Y-%m-%d") \
                >= time.strftime("%Y-%m-%d", time.localtime(time.time() - 10 * 30 * 24 * 60 * 60)):
            return True
        return False

    def update_keyword_crawl_progress(self, keyword: ProductItemKeyword):
        if keyword:
            progress = self.classifyCrawlProgressRepository.find_by_model(keyword)
            self.classifyCrawlProgressRepository.add_finished(progress)

    def update_shop_item_crawl_progress(self, shop_item_id):
        if shop_item_id:
            shopItem = self.shopItemRepository.show(shop_item_id)
            progress = self.classifyCrawlProgressRepository.find_by_model(shopItem)
            self.classifyCrawlProgressRepository.add_finished(progress)

    def add_shop_progress_total(self, shopItem: ShopItem, num: int):
        progress = self.classifyCrawlProgressRepository.find_by_model(shopItem)
        self.classifyCrawlProgressRepository.add_total(progress, num)
