# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from app.producers.BaseProducer import BaseProducer

producers = LoadModules(__path__, BaseProducer).modules
