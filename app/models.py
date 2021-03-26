# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.DB import db
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


product_type_product_relations = Table(
    "product_type_product_relations",
    db.Model.metadata,
    db.Column("product_id", db.BigInt(unsigned=True), db.ForeignKey("products.id"), nullable=False, primary_key=True),
    db.Column("product_type_id", db.BigInt(unsigned=True), db.ForeignKey("product_types.id"),
              nullable=False, primary_key=True),
)


class Brand(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "brands"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class Category(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "categories"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class Classify(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'classifies'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ClassifyCrawlProgress(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "classify_crawl_progresses"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    model_id = db.Column(db.BigInt(unsigned=True), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Integer, default=0)
    finished = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class Product(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "products"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), default='')
    asin = db.Column(db.String(255), unique=True, nullable=False)
    img = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    reviews = db.Column(db.Integer, default=0)
    rating_change = db.Column(db.Float, default=0.0)
    reviews_change = db.Column(db.Integer, default=0)
    review_date = db.Column(db.Date, nullable=True)
    available_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # 一对多关系 目标类中必须要存在product属性
    product_items = relationship('ProductItem', back_populates="product")
    product_type_relations = relationship("ProductTypeProductRelation", back_populates="product")
    types = relationship("ProductType", secondary=product_type_product_relations, backref='products')


class ProductItem(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "product_items"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    product_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('products.id'))
    site_id = db.Column(db.BigInt(unsigned=True),  db.ForeignKey('sites.id'))
    rating = db.Column(db.Float, default=0.0)
    reviews = db.Column(db.Integer, default=0)
    rating_change = db.Column(db.Float, default=0.0)
    reviews_change = db.Column(db.Integer, default=0)
    price = db.Column(db.String(255), default='')
    review_date = db.Column(db.Date, nullable=True)
    available_date = db.Column(db.Date, nullable=True)
    questions = db.Column(db.Integer, default=0)
    answers = db.Column(db.Integer, default=0)
    classify_rank = db.Column(db.JSON, nullable=True)
    feature_rate = db.Column(db.JSON, nullable=True)
    crawl_date = db.Column(db.Date, nullable=True)
    shop_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('shop_items.id'))
    img = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    product = relationship('Product', back_populates="product_items")
    site = relationship('Site', back_populates="product_items")
    daily_ranks = relationship('ProductItemDailyRank', back_populates="product_item")
    product_item_reviews = relationship('ProductItemReview', back_populates="product_item")


class ProductItemCrawlDate(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "product_item_crawl_dates"

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    product_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_items.id'))
    classify_crawl_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ProductItemDailyData(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_item_daily_data'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    product_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_items.id'))
    product_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('products.id'))
    rating = db.Column(db.Float, default=0.0)
    reviews = db.Column(db.Integer, default=0)
    helpers = db.Column(db.Integer, default=0)
    price = db.Column(db.String(255), default='')
    questions = db.Column(db.Integer, default=0)
    answers = db.Column(db.Integer, default=0)
    classify_rank = db.Column(db.JSON, nullable=True)
    feature_rate = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ProductItemDailyRank(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_item_daily_ranks'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=True)
    product_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_items.id'))
    classify_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('classifies.id'))
    rank = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    product_item = relationship('ProductItem', back_populates="daily_ranks")


class ProductItemKeyword(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_item_keywords'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ProductItemReview(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_item_reviews'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(32), unique=True)
    product_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_items.id'))
    product_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('products.id'))
    site_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('sites.id'))
    username = db.Column(db.String(255), nullable=True)
    title = db.Column(db.Text, nullable=True)
    attr = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, default=0)
    color = db.Column(db.String(255), nullable=True)
    size = db.Column(db.String(255), nullable=True)
    helpers = db.Column(db.Integer, default=0)
    detail_link = db.Column(db.String(255), default='')
    content = db.Column(db.Text, default='')
    is_processed = db.Column(db.Integer, default=1)
    date = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    product_item = relationship('ProductItem', back_populates="product_item_reviews")


class ProductType(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_types'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    product_relations = relationship("ProductTypeProductRelation", back_populates="product_type")

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class ProductTypeProductRelation(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'product_type_product_relations'

    product_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('products.id'), primary_key=True)
    product_type_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('product_types.id'), primary_key=True)

    product = relationship('Product', back_populates="product_type_relations")
    product_type = relationship('ProductType', back_populates="product_relations")


class Shop(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'shops'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    asin = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    shop_items = relationship('ShopItem', back_populates="shop")


class ShopItem(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'shop_items'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    shop_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('shops.id'))
    site_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('sites.id'))

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    shop = relationship('Shop', back_populates="shop_items")
    site = relationship('Site', back_populates="shop_items")


class ShopItemDetail(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'shop_item_details'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    shop_item_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('shop_items.id'))
    little_goods_trend = db.Column(db.JSON, nullable=True)
    high_rate_goods_trend = db.Column(db.JSON, nullable=True)
    review_trend = db.Column(db.JSON, nullable=True)
    rate_trend = db.Column(db.JSON, nullable=True)
    little_goods_num = db.Column(db.Integer, default=0)
    high_rate_goods_num = db.Column(db.Integer, default=0)
    review_num = db.Column(db.Integer, default=0)
    rate = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class Site(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'sites'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), default='')
    short_name = db.Column(db.String(255), default='')
    domain = db.Column(db.String(255), default='')
    status = db.Column(db.String(3), default='On')  # On Off
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # 一对多关系 目标类中必须要存在product属性
    product_items = relationship('ProductItem', back_populates="site")
    shop_items = relationship('ShopItems', back_populates="site")
    site_config = relationship('SiteConfig', backref="site", uselist=False)


class SiteConfig(BaseModel):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'site_configs'

    id = db.Column(db.BigInt(unsigned=True), primary_key=True, autoincrement=True)
    site_id = db.Column(db.BigInt(unsigned=True), db.ForeignKey('sites.id'))
    config = db.Column(db.JSON, nullable=True)


if __name__ == '__main__':
    # # 一对多关系模型
    # with db.auto_commit_db():
    #     rs = db.session.query(Product).filter().first()
    #     print(rs.product_items)
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

    # # 多对多关联查询
    # with db.auto_commit_db():
    #     cpa = db.session.query(ProductType).filter(ProductType.id == 1).first()
    #     print(cpa.name)
    #     products = db.session.query(Product).filter(Product.types.contains(cpa)).count()
    #     print(products)

    db.create_all()
