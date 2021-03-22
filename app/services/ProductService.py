# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 3:00 下午 
# @Author : wangHua
# @File : ProductService.py 
# @Software: PyCharm

from app.repositories import *
from utils.Singleton import singleton
from app.models import ProductItem
from time import strftime


@singleton
class ProductService(object):
    product_repository = ProductRepository()
    classify_repository = ClassifyRepository()
    product_item_daily_rank_repository = ProductItemDailyRankRepository()

    def update_product_item_daily_rank(self, product_item: ProductItem, ranks: dict):
        if ranks:
            for classify_name, rank in ranks.items():
                classify = self.classify_repository.update_or_create({'name': classify_name})
                classify = self.product_item_daily_rank_repository.model.update_or_create(
                    {'date': strftime('%Y-%m-%d'), 'classify_id': classify.id, 'product_item_id': product_item.id},
                    {'rank': rank}
                )
                product_item.daily_ranks.append(classify)
