from app.proxies.BaseProxy import BaseProxy
import os
import random
from utils.Logger import Logger
import settings


class LuminatiStaticEngine(BaseProxy):

    proxy_engine = 'luminati_static'

    def __init__(self):
        self.ip_file = settings.STORAGE_PATH + '/proxies/ips-static.txt'
        BaseProxy.__init__(self)

    def get_proxy(self):
        print(self.ip_file)
        ip = ''
        if os.path.exists(self.ip_file):
            with open(self.ip_file, 'r') as f:
                ips = f.readlines()
                ip = random.choice(ips)
        else:
            Logger().warning('代理IP文件不存在，请去官方网站下载，并放在指定位置 {}'.format(self.ip_file))

        return self.format_proxy(ip)

    def __str__(self):
        return self.proxy_ip

    @staticmethod
    def format_proxy(ip):
        if ip:
            ip, port, username, password = ip.strip().replace("\n", '').split(':')
            return "http://{}:{}@{}:{}".format(username, password, ip, port)

        return ip
