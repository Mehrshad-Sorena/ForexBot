import MetaTrader5 as mt5
from .login import Login


class ForexRobot(Login):
    def __init__(self, *args, **kwargs):
        account = kwargs.get('account')
        Login.__init__(self, account)

        strategy = kwargs.get('strategy')
        indicator = kwargs.get('indicator')
