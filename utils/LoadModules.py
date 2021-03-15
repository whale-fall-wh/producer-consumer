import pkgutil
import inspect


class LoadModules:

    def __init__(self, path, base_model):
        self.modules = list()
        for loader, name, is_pkg in pkgutil.walk_packages(path):
            module = loader.find_module(name).load_module(name)
            for name_, value in inspect.getmembers(module):
                if inspect.isclass(value) and issubclass(value, base_model) and not getattr(value, 'ignore', False) \
                        and value is not base_model:
                    self.modules.append(value)
