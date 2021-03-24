# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/23 3:59 下午 
# @Author : wangHua
# @File : ProductTypeRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ProductType as CurrentModel
from utils.Singleton import singleton


@singleton
class ProductTypeRepository(BaseRepository):

    def init_model(self):
        return CurrentModel
