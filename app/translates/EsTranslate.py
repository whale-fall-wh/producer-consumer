# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/22 1:17 下午 
# @Author : wangHua
# @File : DeTranslate.py 
# @Software: PyCharm

from app.translates.BaseTranslate import BaseTranslate


class UkTranslate(BaseTranslate):
    key = 'es'

    def _init_locale(self):
        return 'es_ES'

    def pre_handle(self, time_str: str):
        return time_str.replace(' de ', ' ')
