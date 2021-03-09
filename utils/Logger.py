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
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        self.logger.addHandler(sh)

        # 输出INFO级别日志到文件
        th = logging.FileHandler(self.log_filename, encoding='utf-8')
        th.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        th.setLevel(logging.INFO)
        self.logger.addHandler(th)

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            return getattr(self.logger, key)(*args, **kwargs)
        return not_find


if __name__ == '__main__':
    Logger().debug('aaa')
    Logger().info('aaa')
