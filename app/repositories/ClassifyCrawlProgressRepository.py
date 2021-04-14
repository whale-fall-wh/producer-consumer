# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 11:16 上午 
# @Author : wangHua
# @File : ClassifyCrawlProgressRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ClassifyCrawlProgress as CurrentModel, ProductItemKeyword, ShopItem
from typing import Type
from utils.Singleton import singleton


@singleton
class ClassifyCrawlProgressRepository(BaseRepository):
    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def find_by_model(self, model):
        if isinstance(model, ProductItemKeyword):
            model_name = 'App\Models\ProductItemKeyword'
        elif isinstance(model, ShopItem):
            model_name = 'App\Models\ShopItem'
        else:
            return None

        with self.db.auto_commit_db():
            classifyCrawlProgress = self.db.session.query(
                CurrentModel
            ).filter_by(model=model_name, model_id=model.id).first()

        return classifyCrawlProgress

    @staticmethod
    def add_finished(progress: CurrentModel, num=1):
        if progress:
            progress.update({'finished': progress.finished+num})

    @staticmethod
    def add_total(progress: CurrentModel, num=1):
        if progress:
            progress.update({'total': progress.total+num})
