# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 9:31 下午 
# @Author : wangHua
# @File : CaptchaElement.py 
# @Software: PyCharm

from .BaseElement import BaseElement
from app.entities.SiteConfigEntity import SiteConfigEntity


class AmazonExceptionElement(BaseElement):

    def __init__(self, content: bytes, site_config_entity: SiteConfigEntity):
        self.site_config_entity = site_config_entity
        BaseElement.__init__(self, content)

    def need_validate(self) -> bool:
        element = self.html.xpath(self.site_config_entity.validate_captcha)

        return bool(element)

    def not_found(self) -> bool:
        element = self.html.xpath(self.site_config_entity.page_not_found)

        return bool(element)
