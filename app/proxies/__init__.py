# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : wangHua
# @Software: PyCharm

from utils.LoadModules import LoadModules
from app.proxies.BaseProxy import BaseProxy


proxies = LoadModules(__path__, BaseProxy).modules
