# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/23 5:51 下午 
# @Author : wangHua
# @File : ProductItemDailyDataRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItemDailyData as CurrentModel
from utils.Singleton import singleton


@singleton
class ProductItemDailyDataRepository(BaseRepository):
    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel
