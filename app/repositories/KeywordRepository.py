# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 10:08 上午 
# @Author : wangHua
# @File : KeywordRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import ProductItemKeyword


class KeywordRepository(BaseRepository):
    def init_model(self):
        return ProductItemKeyword

