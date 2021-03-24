# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 5:51 下午 
# @Author : wangHua
# @File : ProductItemDailyRankRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItemDailyRank as CurrentModel
from utils.Singleton import singleton
from typing import Type


@singleton
class ProductItemDailyRankRepository(BaseRepository):
    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel
