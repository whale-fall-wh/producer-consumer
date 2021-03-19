# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/19 10:55 上午 
# @Author : wangHua
# @File : EnTranslate.py 
# @Software: PyCharm

from app.translates.BaseTranslate import BaseTranslate


class EnTranslate(BaseTranslate):
    key = 'en'

    def _init_locale(self):
        return 'en_US'

    def _init_format(self):

        return [
            "%d. %B %Y",    # 18. October 2019
            "%d %B %Y",     # 18 October 2019
            "%d %B, %Y",    # 18 October, 2019
            '%B %d, %Y'     # October 18, 2019
        ]
