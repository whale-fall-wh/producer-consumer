# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/19 10:55 上午
# @Author : wangHua
# @File : BaseTranslate.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
import locale
import datetime


class BaseTranslate(metaclass=ABCMeta):

    def __init__(self):
        self.locale = self._init_locale()
        self.time_format = self._init_format()

    @abstractmethod
    def _init_locale(self):
        pass

    def _init_format(self):
        # https://www.runoob.com/python/att-time-strftime.html
        # 可以在子类重写，以满足其他格式
        return [
            "%d. %B %Y",  # 18. October 2019
            "%d %B %Y",  # 18 October 2019
            "%d %B, %Y",  # 18 October, 2019
            '%B %d, %Y',  # October 18, 2019
            "%d. %b %Y",  # 18. October 2019
            "%d %b %Y",  # 18 October 2019
            "%d %b, %Y",  # 18 October, 2019
            '%b %d, %Y'  # October 18, 2019
        ]

    @staticmethod
    def get_time_from_locale_format(time_str: str, time_format, time_locale):
        try:
            locale.setlocale(locale.LC_ALL, time_locale)
            format_time = datetime.datetime.strptime(time_str, time_format)
            locale.resetlocale()

            return format_time
        except:
            return None

    def available_date(self, time_str):
        if type(self.time_format) == str:
            return self.get_time_from_locale_format(time_str, self.time_format, self.locale)
        elif type(self.time_format) == list:
            for time_format_item in self.time_format:
                rs = self.get_time_from_locale_format(time_str, time_format_item, self.locale)
                if rs is not None:
                    return rs

        return None
