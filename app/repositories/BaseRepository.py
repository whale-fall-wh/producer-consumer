# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 1:01 下午
# @Author : wangHua
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from utils.DB import db


class BaseRepository(metaclass=ABCMeta):
    """
    对model的进一步封装，model中只有属性和关系，repository是一些操作对象
    """
    def __init__(self):
        self.db = db
        self.model = self.init_model()

    @abstractmethod
    def init_model(self):
        pass

    def paginate(self):
        pass

    def show(self, model_id: int):
        with self.db.auto_commit_db():
            model = self.db.session.query(self.model).filter(self.model.id == model_id).first()

        return model

    def all(self) -> list:
        with self.db.auto_commit_db():
            return self.db.session.query(self.model).filter().all()

    def store(self):
        pass

    def destroy(self):
        pass

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.model, key)(*args, **kwargs)

        return not_find
