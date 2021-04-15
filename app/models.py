# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils import db
from sqlalchemy import func, Table
from sqlalchemy.orm import relationship


class BaseModel(db.Model):
    __abstract__ = True

    def __repr__(self):
        return self.__dict__.__str__()

    def update(self, attributes: dict):
        with db.auto_commit_db():
            if attributes:
                for k, v in attributes.items():
                    setattr(self, k, v)

    @classmethod
    def create(cls, attributes):
        with db.auto_commit_db():
            model = cls(**attributes)
            db.session.add(model)

        return model

    @classmethod
    def update_by_id(cls, model_id: int, data: dict):
        with db.auto_commit_db():
            return db.session.query(cls).filter(cls.id == model_id).update(data)

    @classmethod
    def update_or_create(cls, attributes: dict, values: dict = None):
        with db.auto_commit_db():
            model = db.session.query(cls).filter_by(**attributes).first()
            if model is not None:
                if type(values) == dict:
                    for k, v in values.items():
                        setattr(model, k, v)
            else:
                if type(values) == dict:
                    attributes.update(values)
                model = cls(**attributes)
                db.session.add(model)

            return model

    def delete(self):
        with db.auto_commit_db():
            db.session.delete(self)


if __name__ == '__main__':
    db.create_all()
