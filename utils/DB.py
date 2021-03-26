# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/15 5:05 下午
# @Author : wangHua
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from settings import CONNECTION_STR
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Column, Integer, String, Float, Date, TIMESTAMP, DateTime, Text, ForeignKey, JSON


class DB:
    """
    简单封装，初始化，并使用contextmanager简化语法
    参考 https://segmentfault.com/a/1190000016754146、https://blog.csdn.net/weixin_43343144/article/details/103262272
    contextmanager:
    """

    def __init__(self):
        self.engine = create_engine(CONNECTION_STR)
        # model需要继承的基类:
        self.Model = declarative_base()
        # scoped_session 线程安全，不然多线程会异常
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Column = Column
        self.Integer = Integer
        self.BigInt = mysql.BIGINT
        self.String = String
        self.Float = Float
        self.Date = Date
        self.TIMESTAMP = TIMESTAMP
        self.DateTime = DateTime
        self.Text = Text
        self.ForeignKey = ForeignKey
        self.JSON = JSON

    @contextmanager
    def auto_commit_db(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def create_all(self):
        # 简单实现，创建所有的表，
        # TODO: 使用Alembic封装优化数据迁移
        self.Model.metadata.create_all(self.engine)


db = DB()
