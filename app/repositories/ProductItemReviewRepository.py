# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/23 3:59 下午 
# @Author : wangHua
# @File : ProductItemReviewRepository.py
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItemReview as CurrentModel
from utils.Singleton import singleton
from typing import Type


@singleton
class ProductItemReviewRepository(BaseRepository):

    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def get_last_review_date(self, **filter_by):
        with self.db.auto_commit_db():
            last_review = self.db.session.query(self.model)\
                .filter_by(**filter_by).order_by(CurrentModel.date.desc()).first()

        if last_review:
            return last_review.date
        else:
            return None

    def get_review_count(self, **filter_by):
        with self.db.auto_commit_db():
            count = self.db.session.query(self.model).filter_by(**filter_by).count()

        return count
