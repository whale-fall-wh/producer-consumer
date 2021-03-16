# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 3:32 下午 
# @Author : wangHua
# @File : ProductItemRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItem
from utils.Singleton import singleton


@singleton
class ProductItemRepository(BaseRepository):

    def init_model(self) -> Type[ProductItem]:
        return ProductItem
