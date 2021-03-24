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


@singleton
class ProductService(object):
    productRepository = ProductRepository()
    classifyRepository = ClassifyRepository()
    productItemDailyRankRepository = ProductItemDailyRankRepository()
    productItemReviewRepository = ProductItemReviewRepository()
    productItemRepository = ProductItemRepository()
    productItemDailyDataRepository = ProductItemDailyDataRepository()

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
        if product_item.site.name == '美亚':
            product_item.product.update({
                'review_date': review_date,
                'reviews': reviews
            })
