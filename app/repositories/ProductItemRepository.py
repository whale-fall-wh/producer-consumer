# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 3:32 下午 
# @Author : wangHua
# @File : ProductItemRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItem as CurrentModel
from utils import singleton


@singleton
class ProductItemRepository(BaseRepository):

    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def get_by_shop_item_id(self, shop_item_id):
        with self.db.auto_commit_db():
            productItems = self.db.session.query(self.model).filter_by(shop_item_id=shop_item_id).all()

        return productItems
