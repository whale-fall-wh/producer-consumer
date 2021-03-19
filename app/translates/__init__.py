# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/19 10:55 上午 
# @Author : wangHua
# @File : __init__.py 
# @Software: PyCharm

from utils.LoadModules import LoadModules
from .BaseTranslate import BaseTranslate

translates = LoadModules(__path__, BaseTranslate).modules


def get_translate_by_locale(locale):
    for translate_class in translates:
        translate = translate_class()
        if locale == getattr(translate, 'key', ''):
            return translate
    return None
