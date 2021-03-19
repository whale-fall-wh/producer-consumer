# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/18 4:54 下午 
# @Author : wangHua
# @File : dateTester.py 
# @Software: PyCharm

import locale
import datetime


def func():
    locale.setlocale(locale.LC_ALL, 'it_IT')
    rule = '%d %b %Y'
    format_time = datetime.datetime.strptime("1 set 2020", rule)
    print("formattime -->{}".format(format_time))
    locale.resetlocale()


if __name__ == '__main__':
    func()
