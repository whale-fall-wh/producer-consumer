# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from app.consumers.BaseConsumer import BaseConsumer

consumers = LoadModules(__path__, BaseConsumer).modules
