# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import Product as CurrentModel, ProductType
from utils.Singleton import singleton


@singleton
class ProductRepository(BaseRepository):

    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def getProductsByType(self, product_types: [int, list]):
        with self.db.auto_commit_db():
            query = self.db.session.query(self.model)
            if type(product_types) == list:
                query = query.filter(self.model.types.any(ProductType.id.in_(product_types)))
            else:
                query = query.filter(self.model.types.any(ProductType.id == product_types))

            return query.all()


if __name__ == '__main__':
    product = ProductRepository().show(796)
    print(product.__dict__)
