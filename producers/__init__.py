from utils.LoadModules import LoadModules
from producers.BaseProducer import BaseProducer

producers = LoadModules(__path__, BaseProducer).yield_module()
