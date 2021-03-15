from utils.LoadModules import LoadModules
from app.producers.BaseProducer import BaseProducer

producers = LoadModules(__path__, BaseProducer).modules
