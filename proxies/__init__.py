from utils.LoadModules import LoadModules
from .BaseProxy import BaseProxy
from utils.Logger import Logger


load_module = LoadModules(__path__, BaseProxy)
Logger().debug('所有有效的代理插件：' + [proxy.proxy_engine for proxy in load_module.modules].__str__())
proxies = load_module.yield_module()
