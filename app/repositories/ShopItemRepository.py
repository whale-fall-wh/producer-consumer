# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 11:00 上午 
# @Author : wangHua
# @File : ShopItemRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ShopItem


class ShopItemRepository(BaseRepository):
    def init_model(self):
        return ShopItem
