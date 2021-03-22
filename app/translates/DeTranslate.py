# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 1:17 下午 
# @Author : wangHua
# @File : DeTranslate.py 
# @Software: PyCharm

from app.translates.BaseTranslate import BaseTranslate


class DeTranslate(BaseTranslate):
    key = 'de'

    def _init_locale(self):
        return 'de_DE'
