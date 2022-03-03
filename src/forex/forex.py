#import MetaTrader5 as mt5
from src.db import ForexMongo
from .login import Login


class ForexRobot(ForexMongo, Login):
    def __init__(self, *args, **kwargs):
        account = kwargs.get('account')

        strategy = kwargs.get('strategy')
        indicator = kwargs.get('indicator')
