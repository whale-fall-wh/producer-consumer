# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/19 10:54 上午 
# @Author : wangHua
# @File : ItTranslate.py 
# @Software: PyCharm

from app.translates.BaseTranslate import BaseTranslate


class ItTranslate(BaseTranslate):
    key = 'it'

    def _init_locale(self):
        return 'it_IT'
