import logging
import os
import datetime
from utils.Singleton import singleton


@singleton
class Logger:

    def __init__(self):
        self.log_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/'
        self.log_filename = self.log_dir_path + datetime.date.today().strftime('%Y-%m-%d') + '.log'

        self.logger = logging.getLogger(self.log_filename)

        self.logger.setLevel(logging.DEBUG)

        # 输出DEBUG级别日志到控制台
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)

        # 输出INFO级别日志到文件
        th = logging.FileHandler(self.log_filename, encoding='utf-8')
        th.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        th.setLevel(logging.INFO)
        self.logger.addHandler(th)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.logger, key)(*args, **kwargs)
        return not_find

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

    def set_format(self, color):
        # 30黑 31红 32绿 33黄 34蓝 35紫 36青 37白
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % '[%(asctime)s] - [%(levelname)s] - %(message)s')
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)


if __name__ == '__main__':
    Logger().debug('aaa')
    Logger().info('aaa')
    Logger().warning('aaa')
    Logger().error('aaa')
    Logger().critical('aaa')
