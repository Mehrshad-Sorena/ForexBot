from .forex.forex import ForexRobot
from src.db import ForexMongo


class Runner(ForexRobot, ForexMongo):
    def __init__(self, *args, **kwargs):
        pass
