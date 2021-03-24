# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/23 4:45 下午 
# @Author : wangHua
# @File : bar.py 
# @Software: PyCharm
from progress.spinner import Spinner
import time
state = 1
spinner = Spinner('正在')
while state != 'FINISHED':
    # Do some work
    spinner.next()
    time.sleep(0.05)
