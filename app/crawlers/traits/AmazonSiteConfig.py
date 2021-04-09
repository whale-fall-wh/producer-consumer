# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 1:32 下午 
# @Author : wangHua
# @File : AmazonSiteConfig.py
# @Software: PyCharm

from app.models import Site
from app.entities import SiteConfigEntity
from app.repositories import SiteRepository


class AmazonSiteConfig(object):

    def __init__(self, site: Site):
        self.site = site
        self.site_config_entity = SiteConfigEntity.instance(self.init_site_config(site))
        if self.site_config_entity.has_en_translate and site.short_name != 'us':
            siteEn = SiteRepository().get_by_short_name('us')
            if siteEn:
                self.site_config_entity = SiteConfigEntity.instance(siteEn.__dict__)

    @staticmethod
    def init_site_config(site: Site):
        if site.site_config and type(site.site_config.config) == dict:
            return site.site_config.config
        else:
            return {}
