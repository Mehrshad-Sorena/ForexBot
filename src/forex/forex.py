from src.utils import GetData, bestExtremeFinder
from src.strategy import sikimi
from src.db import ForexMongo
import MetaTrader5 as mt5
from .login import Login


class ForexRobot(Login, GetData):
    """
    Forex Robot
    """
    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.get('strategy')
        self.indicator = kwargs.get('indicator')

    def run(self):
        if self.strategy == 'sikimi':
            symbol_data_5M, money, sym = self.getGenetic(
                    mt5.TIMEFRAME_M5, 0, 200)
            symbol_data_15M, money, sym = self.getGenetic(
                    mt5.TIMEFRAME_M15, 0, 6000)
            symbol_data_1H, money, sym = self.getGenetic(
                    mt5.TIMEFRAME_H1, 0, 2000)
            symbol_data_4H, money, sym = self.getGenetic(
                    mt5.TIMEFRAME_H4, 0, 360)
            symbol_data_1D, money, sym = self.getGenetic(
                    mt5.TIMEFRAME_D1, 0, 60)
            exterm_point_pred = self.extremePointsIchimoko(
                    mt5.TIMEFRAME_M5, 0, 200)

            y3 = symbol_data_5M['AUDCAD_i']['high']
            y4 = symbol_data_5M['AUDCAD_i']['low']

            sikimi_strategy_result = sikimi(
                    y3, y4, symbol_data_5M, symbol_data_15M, symbol_data_1D,
                    symbol_data_1H, symbol_data_4H, exterm_point_pred)

            return sikimi_strategy_result
