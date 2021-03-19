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
