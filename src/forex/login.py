#import MetaTrader5 as mt5
from src.utils import logs


class Login:
    def login(self, account):
        try:
            authorized = mt5.login(
                    username=account.get('username'),
                    password=account.get('password'))
        except Exception as ex:
            logs('warning', ex)

        return authorized
