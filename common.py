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
        try:
            if not s:
                return 0
            if '-' == s[0]:
                return 0 - str2int(s[1:])
            elif s[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                num = 0
                for i in range(len(s)):
                    if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        num = num * 10 + int(s[i])
                    else:
                        return num
            else:
                return 0
        except:
            return 0


if __name__ == '__main__':
    str2int('')
