# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 4:11 下午 
# @Author : wangHua
# @File : ResourceRepository.py 
# @Software: PyCharm

from .BaseRepository import BaseRepository
from app.models import Resource


class ResourceRepository(BaseRepository):

    def init_model(self):
        return Resource

    def save(self, path, url='', resource_type=1):
        return self.init_model().update_or_create({'path': path}, {'url': url, 'resource_type': resource_type})

    def get_resource(self, resource_id):
        return self.show(resource_id)
