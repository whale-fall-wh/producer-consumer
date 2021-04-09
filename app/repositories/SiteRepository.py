# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 3:34 下午 
# @Author : wangHua
# @File : SiteRepository.py 
# @Software: PyCharm

from typing import Type
from app.repositories.BaseRepository import BaseRepository
from app.models import Site as CurrentModel
from utils.Singleton import singleton


@singleton
class SiteRepository(BaseRepository):

    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def get_by_short_name(self, short_name: str):
        with self.db.auto_commit_db():
            site = self.db.session.query(CurrentModel).filter_by(short_name=short_name).first()

        return site
