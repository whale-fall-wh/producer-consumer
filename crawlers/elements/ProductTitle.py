# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree


def get_title(text: str):
    """
    获取product标题
    :param text:
    :return:
    """
    html = etree.HTML(text)
    rs = html.xpath('//*[@id="productTitle"]/text()')
    if len(rs):
        title = rs[0].strip()
    else:
        title = None

    return title

