# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 2:05 下午 
# @Author : wangHua
# @File : ClassifyTreeElement.py 
# @Software: PyCharm

from app.crawlers.elements.BaseElement import BaseElement
from app.entities import SiteConfigEntity


class ClassifyTreeElement(BaseElement):
    def __init__(self, content: bytes, siteConfig: SiteConfigEntity):
        self.siteConfig = siteConfig
        BaseElement.__init__(self, content)

    def crawl_classify_tree(self, currentUrl, currentName):
        root = self.html.xpath('//*[@id="zg_browseRoot"]/ul')
        if not root:
            return []

        return self._crawl_tree(root[0], currentUrl, currentName)

    def _crawl_tree(self, element, currentUrl, currentName):
        ul = element.xpath('./ul')
        if ul:
            tree = list()
            treeItem = dict()
            a = element.xpath('./li[1]/a')
            if a:
                treeItem['classify_name'] = ''.join(a[0].xpath('./text()'))
                treeItem['url'] = ''.join(''.join(a[0].xpath('./@href')).split('/ref=')[:1])
            else:
                treeItem['classify_name'] = ''.join(element.xpath('./text()'))
                treeItem['url'] = currentUrl
                treeItem['name'] = currentName

            url_id = ''.join(treeItem.get('url').split('/')[-1:])
            if url_id.isnumeric():
                treeItem['url_id'] = url_id
            treeItem['items'] = self._crawl_tree(ul[0], currentUrl, currentName)
            tree.append(treeItem)
            return tree
        else:
            items = list()
            lis = element.xpath('./li')
            for li in lis:
                tmp = dict()
                tmp['classify_name'] = ''.join(li.xpath('./text()'))
                a = li.xpath('./a')
                if a:
                    tmp['url'] = ''.join(''.join(a[0].xpath('./@href')).split('/ref=')[:1])
                else:
                    tmp['url'] = currentUrl
                    tmp['name'] = currentName
                tmp['url_id'] = ''.join(tmp['url'].split('/')[-1:])
                items.append(tmp)
            return items
