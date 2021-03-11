# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度API
"""
import base64
import requests
from decouple import config
from utils.Logger import Logger
from utils.Redis import Redis


class ImgApi:
    """
    百度通用文字识别
    """
    access_token = ''
    code = ''

    def __init__(self, path):
        self.client_id = config('BAIDU_CLIENT_ID', '')
        self.client_secret = config('BAIDU_CLIENT_SECRET', '')

        if not (self.client_id and self.client_secret):
            Logger().warning('百度API配置异常，部分功能将不可使用')
            return

        self.http = requests.Session()
        # 二进制方式打开图片文件
        with open(path, 'rb') as f:
            image = base64.b64encode(f.read()).decode('UTF8')
            self.params = {"image": image, "language_type": "ENG"}
        self.get_token()
        self.get_code()

    def __init_config(self):
        pass

    def get_code(self):
        try:
            api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = self.http.post(api_url.format(self.access_token), data=self.params, headers=headers)
            Logger().debug(response.json())
            if response and response.json().get('words_result_num'):
                self.code = response.json().get('words_result')[0].get('words')
            else:
                Logger().error(response.json())
        except:
            Logger().error('百度识别验证码异常')

    def get_token(self):
        try:
            # 百度的access_token 有效市场为30天，可配置缓存，避免重复调用
            self.access_token = Redis().db.get('baidu_api:access_token')
            if self.access_token:
                return
        except:
            pass
        try:
            token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={' \
                        '}&client_secret={} '
            response = self.http.get(token_url.format(self.client_id, self.client_secret))
            if response:
                self.access_token = response.json().get('access_token')
                Redis().db.set('baidu_api:access_token', self.access_token, 24*60*60)   # 一天有效，30天内都行
                Logger().debug(self.access_token)
        except:
            return None


if __name__ == '__main__':
    code = ImgApi('/Users/wanghua/PycharmProjects/amazon/imgs/1.jpg').code
    Logger().debug(code)
