# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 5:51 下午 
# @Author : wangHua
# @File : ProductItemDailyRankRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ProductItemDailyRank


class ProductItemDailyRankRepository(BaseRepository):
    def init_model(self):
        return ProductItemDailyRank
