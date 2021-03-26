# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 4:55 下午 
# @Author : wangHua
# @File : BaseElement.py 
# @Software: PyCharm

from lxml import etree
from app.exceptions import CrawlErrorException


class BaseElement(object):

    def __init__(self, content: bytes):
        self._get_element_prefix = 'get_element_'
        self.html = etree.HTML(content)
        if self.html is None:
            raise CrawlErrorException('html 解析异常')

        self.__render_all_element()

    def __render_all_element(self):
        for attr in self.__yield_all_element_function():
            k = attr.replace(self._get_element_prefix, '')
            v = getattr(self, attr)()
            setattr(self, k, v)

    def get_all_element(self):
        rs = dict()
        for attr in self.__yield_all_element_function():
            k = attr.replace(self._get_element_prefix, '')
            rs[k] = getattr(self, k)

        return rs

    def __yield_all_element_function(self):
        for attr in dir(self):
            if attr.startswith(self._get_element_prefix):
                yield attr

    @staticmethod
    def get_html(element) -> str:
        return etree.tostring(element).decode("utf-8")

    @staticmethod
    def get_content(element) -> bytes:
        return etree.tostring(element)
