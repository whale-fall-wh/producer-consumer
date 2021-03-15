from utils.LoadModules import LoadModules
from app.consumers.BaseConsumer import BaseConsumer

consumer = LoadModules(__path__, BaseConsumer).modules
