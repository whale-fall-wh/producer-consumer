import threading
from BaseJob import BaseJob


class BaseConsumer(threading.Thread, BaseJob):
    def __init__(self):
        BaseJob.__init__(self)
        threading.Thread.__init__(self)


