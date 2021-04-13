# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 3:22 下午 
# @Author : wangHua
# @File : ProductClassifyRepository.py 
# @Software: PyCharm

from app.repositories.BaseRepository import BaseRepository
from app.models import ProductClassify as CurrentModel
from typing import Type
from utils.Singleton import singleton
from sqlalchemy import func


@singleton
class ProductClassifyRepository(BaseRepository):
    def init_model(self) -> Type[CurrentModel]:
        return CurrentModel

    def update_or_create_node(self, attributes: dict, data: dict):
        with self.db.auto_commit_db():
            model = self.db.session.query(CurrentModel).filter_by(**attributes).first()
            if model is not None:
                if type(data) == dict and data:
                    for k, v in data.items():
                        setattr(model, k, v)
            else:
                aggregate,  = self.db.session.query(func.max(CurrentModel._rgt)).first()
                data['_lft'] = aggregate+1 if aggregate else 1
                data['_rgt'] = aggregate+2 if aggregate else 2
                if type(data) == dict:
                    attributes.update(data)
                model = CurrentModel(**attributes)
                self.db.session.add(model)

        return model

    def update_or_create_children(self, parentNode: CurrentModel, attributes: dict, data: dict):
        attributes['parent_id'] = parentNode.id
        sql = 'update `product_classifies` set `_lft` = case when `_lft` >= {_rgt} then `_lft` + 2 else `_lft` end,' \
              ' `_rgt` = case when `_rgt` >= {_rgt} then `_rgt` + 2 else `_rgt` end' \
              ' where (`_lft` >= {_rgt} or `_rgt` >= {_rgt})'.format(**{'_rgt': parentNode._rgt})
        with self.db.auto_commit_db():
            model = self.db.session.query(CurrentModel).filter_by(**attributes).first()
            if model is not None:
                if type(data) == dict and data:
                    for k, v in data.items():
                        setattr(model, k, v)
            else:
                data['_lft'] = parentNode._rgt
                data['_rgt'] = parentNode._rgt + 1
                if type(data) == dict:
                    attributes.update(data)
                self.db.session.execute(sql)
                model = CurrentModel(**attributes)
                self.db.session.add(model)

        return model


if __name__ == '__main__':
    re = ProductClassifyRepository()
    node = re.update_or_create_node({'name': 'test_node'}, {'url': 'aaa'})
    child = re.update_or_create_children(node, {'name': 'test_children'}, {})
    last_child = re.update_or_create_children(child, {'name': 'test_children'}, {})
