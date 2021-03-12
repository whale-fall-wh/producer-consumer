# !/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.Http import Http
from lxml import etree
from utils.Logger import Logger
import os
from utils.BDApi import ImgApi


class Captcha:
    """amazon验证码"""
    params = {'amzn': '', 'amzn-r': '', 'field-keywords': '', }
    url = ''
    img_url = ''
    img_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/storage/imgs/{}'

    def __init__(self, base_url: str, html: str, http: Http):
        self.http = http
        self.html = etree.HTML(html)
        self.base_url = base_url
        self.get_params()
        self.get_url()
        self.response = self.validate()

    def get_url(self):
        """
        地址可以从form表单获取
        :return:
        """
        self.url = self.base_url + '/errors/validateCaptcha'

    def get_params(self):
        amzn_element = self.html.xpath("//input[@name='amzn']/@value")
        if amzn_element:
            self.params['amzn'] = amzn_element[0]
        img_url = self.html.xpath("//img[contains(@src, 'captcha')]/@src")
        if img_url:
            self.img_url = img_url[0]
            path = self.save_img()
            self.params['field-keywords'] = ImgApi(path=path).code
            Logger().debug("图片地址: {}， 识别出的验证码：{}".format(path, self.params['field-keywords']))

    def validate(self):
        rs = self.http.get(self.url, params=self.params)
        Logger().debug(rs.cookies)

        return rs

    def save_img(self):
        # 保存图片，可以抽出来，封装
        html = self.http.get(self.img_url)
        img_name = self.img_path.format(str(hash(self.img_url)) + '.jpg')
        with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
            file.write(html.content)
            file.flush()

        return img_name
