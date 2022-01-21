import MetaTrader5 as mt5
from src.utils import logs


class Login:
    def __init__(self, account):
        self._account = account
        self.login()

    def login(self):
        try:
            authorized = mt5.login(
                    username=self._account.get('username'),
                    password=self._account.get('password'))
        except Exception as ex:
            logs('warning', ex)

        return authorized
