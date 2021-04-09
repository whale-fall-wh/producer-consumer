# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/8 5:05 下午
# @Author : wangHua
# @Software: PyCharm

import logging
from logging.handlers import TimedRotatingFileHandler
import settings
from utils.Singleton import ThreadSafeSingleton
from decouple import config


class Logger(metaclass=ThreadSafeSingleton):
    """
    日志-控制台打印所有日志，文件记录info级别以上日志
    """
    def __init__(self):
        # 日志输出目录、文件
        self.log_filename = settings.STORAGE_PATH + '/logs/logs'
        self.logger = logging.getLogger(self.log_filename)
        self.logger.setLevel(logging.DEBUG)

        # 输出DEBUG级别日志到控制台
        self.sh = logging.StreamHandler()
        self.sh.setLevel(config('CONSOLE_LOG_LEVEL', logging.DEBUG))

        # 输出INFO级别日志到文件
        self.tfh = TimedRotatingFileHandler(self.log_filename, when='midnight', backupCount=10, encoding='utf-8')
        self.tfh.suffix = '%Y-%m-%d'
        self.tfh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        self.tfh.setLevel(config('FILE_LOG_LEVEL', logging.INFO))
        self.logger.addHandler(self.tfh)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.logger, key)(*args, **kwargs)
        return not_find

    def set_format(self, color):
        # 30黑 31红 32绿 33黄 34蓝 35紫 36青 37白
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % '[%(asctime)s] - [%(levelname)s] - %(message)s')
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)

    def debug(self, message):
        self.set_format('\033[0;37m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.set_format('\033[0;36m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.set_format('\033[0;33m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.set_format('\033[0;31m%s\033[0m')
        self.logger.error(message)

    def critical(self, message):
        self.set_format('\033[0;35m%s\033[0m')
        self.logger.critical(message)


if __name__ == '__main__':
    logger = Logger()
    logger.debug('1')
    logger.info('2')
    # logger.warning('3')
    # logger.error('4')
    # logger.critical('5')

