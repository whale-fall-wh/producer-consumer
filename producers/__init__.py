import inspect
import pkgutil
from producers.BaseProducer import BaseProducer

# 获取所有类
producers = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for name_, value in inspect.getmembers(module):
        globals()[name_] = value
        if inspect.isclass(value) and issubclass(value, BaseProducer) and not getattr(value, 'ignore', False)\
                and value is not BaseProducer:
            producers.append(value)
