# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 9:31 下午 
# @Author : wangHua
# @File : CaptchaElement.py 
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity
import settings


class AmazonExceptionElement(BaseElement):
    """
    亚马逊各种异常元素
    """

    def __init__(self, content: bytes, site_config_entity: SiteConfigEntity):
        self.site_config_entity = site_config_entity
        BaseElement.__init__(self, content)

    def need_validate(self) -> bool:
        element = self.html.xpath(self.site_config_entity.validate_captcha)

        return bool(element)

    def not_found(self) -> bool:
        element = self.html.xpath(self.site_config_entity.page_not_found)
        if element:
            path = settings.STORAGE_PATH
            with open(path + '/logs/not_found.html', 'w') as f:
                f.write(self.get_html(self.html))

        return bool(element)

    def error_500(self):
        error = self.html.xpath(self.site_config_entity.error_500)
        not_found = self.html.xpath(self.site_config_entity.page_not_found)

        return bool(error) and bool(not_found)
