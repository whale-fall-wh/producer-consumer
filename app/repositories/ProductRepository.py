# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import Product
from utils.Singleton import singleton


@singleton
class ProductRepository(BaseRepository):

    def init_model(self) -> Type[Product]:
        return Product


if __name__ == '__main__':
    product = ProductRepository().show(796)
    print(product.__dict__)
