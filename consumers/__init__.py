import pkgutil
import inspect
from consumers.BaseConsumer import BaseConsumer

# 获取所有类
consumer = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for name_, value in inspect.getmembers(module):
        globals()[name_] = value
        if inspect.isclass(value) and issubclass(value, BaseConsumer) and not getattr(value, 'ignore', False)\
                and value is not BaseConsumer:
            consumer.append(value)
