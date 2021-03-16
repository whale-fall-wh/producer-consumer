# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 3:34 下午 
# @Author : wangHua
# @File : SiteRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import Site
from utils.Singleton import singleton


@singleton
class SiteRepository(BaseRepository):

    def init_model(self) -> Type[Site]:
        return Site
