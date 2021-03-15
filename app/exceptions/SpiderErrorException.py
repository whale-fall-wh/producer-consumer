from utils.Logger import Logger


class SpiderErrorException(Exception):
    """爬虫抓取失败异常"""

    def __init__(self, msg=''):
        if msg:
            Logger().warning(msg)
