# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
from utils.Logger import Logger


def sleep_random():
    random_time = random.randint(3, 10)
    Logger().debug('随机sleep{}s'.format(random_time))
    time.sleep(random_time)


def sleep(secs: float):
    time.sleep(secs)


def replace_multi(string: str, search, replace: str):
    if type(search) == list:
        for search_item in search:
            string = replace_multi(string, search_item, replace)
        return string

    return string.replace(search, replace)


def str2int(s):
    try:
        return int(s)
    except:
        return 0


def str2float(s, d=1) -> float:
    try:
        s = float(s)
        return round(s, d)
    except:
        return 0.0


if __name__ == '__main__':
    print(str2float('5.5222'))
