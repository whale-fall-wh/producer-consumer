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
