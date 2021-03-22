# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.DB import db
from sqlalchemy import func, Table
from sqlalchemy.orm import relationship


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, attributes):
        with db.auto_commit_db():
            model = cls(**attributes)
            db.session.add(model)

        return model

    @classmethod
    def update(cls, model_id: int, data: dict):
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


class Product(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "products"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    asin = db.Column(db.String(255), unique=True)
    img = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    rating_change = db.Column(db.Float)
    reviews_change = db.Column(db.Integer)
    review_date = db.Column(db.Date)
    available_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # 一对多关系 目标类中必须要存在product属性
    product_items = relationship('ProductItem', back_populates="product")


class ProductItem(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "product_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('products.id'))
    site_id = db.Column(db.BigInt(unsigned=True),  db.ForeignKey('sites.id'))
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    rating_change = db.Column(db.Float)
    reviews_change = db.Column(db.Integer)
    price = db.Column(db.String(255))
    review_date = db.Column(db.Date)
    available_date = db.Column(db.Date)
    questions = db.Column(db.Integer)
    answers = db.Column(db.Integer)
    classify_rank = db.Column(db.JSON)
    feature_rate = db.Column(db.JSON)
    crawl_date = db.Column(db.Date)
    shop_item_id = db.Column(db.BigInt(unsigned=True))
    img = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    product = relationship('Product', back_populates="product_items")
    site = relationship('Site', back_populates="product_items")
    daily_ranks = relationship('ProductItemDailyRank', back_populates="product_item")


class Site(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'sites'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    domain = db.Column(db.String(255))
    status = db.Column(db.String(3))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # 一对多关系 目标类中必须要存在product属性
    product_items = relationship('ProductItem', back_populates="site")
    site_config = relationship('SiteConfig', backref="site", uselist=False)


class SiteConfig(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'site_configs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('sites.id'))
    config = db.Column(db.JSON)


class Classify(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'classifies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ProductItemDailyRank(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_item_daily_ranks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    product_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_items.id'))
    classify_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('classifies.id'))
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    product_item = relationship('ProductItem', back_populates="daily_ranks")


if __name__ == '__main__':
    # 一对多关系模型
    with db.auto_commit_db():
        rs = db.session.query(Product).filter(id==810).first()
        print(rs.product_items)
    #
    # with db.auto_commit_db():
    #     rs = db.session.query(ProductItem).first()
    #     print(rs.product.asin, rs.site.name)
    #
    # # 一对一关系模型
    # with db.auto_commit_db():
    #     rs = db.session.query(Site).first()
    #     print(rs.site_config.config)
    #
    # with db.auto_commit_db():
    #     rs = db.session.query(SiteConfig).first()
    #     print(rs.site.name)
