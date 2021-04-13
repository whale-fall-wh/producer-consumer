# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 5:12 下午 
# @Author : wangHua
# @File : ProductClassifyElement.py 
# @Software: PyCharm

from app.crawlers.elements.ProductDetailElement import ProductDetailElement


class ProductClassifyElement(ProductDetailElement):

    def get_element_classify_rank(self):
        rs = list()
        productDetail = self._get_product_detail_element()
        if productDetail is None:
            return []
        classifies = productDetail.xpath('//a[contains(@href,"gp/bestsellers")]')
        for classify in classifies:
            classify_url = ''.join(classify.xpath('./@href[1]'))
            classify_name = ''.join(classify.xpath('./text()[1]'))
            url = ''.join(classify_url.split('/ref=')[:1])
            url_id = ''.join(url.split('/')[-1:])
            if url != '/gp/bestsellers' and url_id.isnumeric():
                rs_item = dict()
                rs_item['name'] = classify_name
                rs_item['url'] = url
                rs_item['url_id'] = url_id
                rs.append(rs_item)

        return rs
