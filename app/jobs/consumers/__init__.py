# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from .BaseConsumer import BaseConsumer

consumers = LoadModules(__path__, BaseConsumer).modules
