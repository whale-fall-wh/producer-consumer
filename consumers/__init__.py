from utils.LoadModules import LoadModules
from consumers.BaseConsumer import BaseConsumer

consumer = LoadModules(__path__, BaseConsumer).yield_module()
