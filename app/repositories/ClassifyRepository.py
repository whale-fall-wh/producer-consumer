# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 3:39 下午 
# @Author : wangHua
# @File : ClassifyRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import Classify


class ClassifyRepository(BaseRepository):
    def init_model(self) -> Type[Classify]:
        return Classify
