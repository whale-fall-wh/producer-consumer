# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 10:59 上午 
# @Author : wangHua
# @File : ShopRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import Shop


class ShopRepository(BaseRepository):

    def init_model(self):
        return Shop
