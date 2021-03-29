# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random


def sleep_random():
    random_time = random.randint(3, 10)
    time.sleep(random_time)


def sleep(secs: float):
    time.sleep(secs)


def replace_multi(string: str, search, replace: str):
    if type(search) == list:
        for search_item in search:
            string = replace_multi(string, search_item, replace)
        return string

    return string.replace(search, replace)


def str2int(s, default=0):
    try:
        return int(s)
    except:
        return default


def str2float(s, d=1, default=0.0) -> float:
    try:
        s = float(s)
        return round(s, d)
    except:
        return default
