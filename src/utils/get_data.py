from .logger import logs
import MetaTrader5 as mt5
import pandas as pd


class GetData:
    def getData(self, frame, number):
        symbols = mt5.symbols_get()
        symbol_data = {}

        for i in symbols:
            try:
                rates = mt5.copy_rates_from_pos(i.name, frame, 0, number)
                rates_frame = pd.DataFrame(rates)
                rates_frame['time'] = pd.to_datetime(
                        rates_frame['time'], unit='s')
                symbol_data[i.name] = {
                        i.name: i.name,
                        'open': rates_frame['open'],
                        'close': rates_frame['close'],
                        'low': rates_frame['low'],
                        'high': rates_frame['high'],
                        'HL/2': (rates_frame['high'] + rates_frame['low']) / 2,
                        'HLC/3': (rates_frame['high'] + rates_frame['low'] +
                                  rates_frame['close']) / 3,
                        'HLCC/4': (rates_frame['high'] + rates_frame['low'] +
                                   rates_frame['close'] + rates_frame['close']
                                   ) / 4,
                        'OHLC/4': (rates_frame['high'] + rates_frame['low'] +
                                   rates_frame['close'] + rates_frame['open']
                                   ) / 4,
                        'volume': rates_frame['tick_volume'],
                        'time': rates_frame['time']
                }
            except Exception as ex:
                logs('warning', ex)

        return symbol_data, self.account_info_dict['balance'], symbols

    def getSymbols(self, frame):
        symbols = mt5.symbols_get()
        return symbols, self.account_info_dict['balance']

    def getOneByOne(self, frame, number, sym_name):
        symbol_data = {}

        try:
            rates = mt5.copy_rates_from_pos(
                    sym_name, frame, 0, number)
            rates_frame = pd.DataFrame(rates)
            rates_frame['time'] = pd.to_datetime(
                    rates_frame['time'], unit='s')
            symbol_data[sym_name] = {
                    sym_name: sym_name,
                    'open': rates_frame['open'],
                    'close': rates_frame['close'],
                    'low': rates_frame['low'],
                    'high': rates_frame['high'],
                    'HL/2': (rates_frame['high'] + rates_frame['low']) / 2,
                    'HLC/3': (rates_frame['high'] + rates_frame['low'] +
                              rates_frame['close']) / 3,
                    'HLCC/4': (rates_frame['high'] + rates_frame['low'] +
                               rates_frame['close'] + rates_frame['close']
                               ) / 4,
                    'OHLC/4': (rates_frame['high'] + rates_frame['low'] +
                               rates_frame['close'] + rates_frame['open']) / 4,
                    'volume': rates_frame['tick_volume'],
                    'time': rates_frame['time']
            }
        except Exception as ex:
            logs('warning', ex)

        return symbol_data, self.account_info_dict['balance']

    def getGenetic(self, frame, number_start, number_end):
        symbols = mt5.symbols_get()
        symbol_data = {}

        for i in symbols:
            try:
                rates = mt5.copy_rates_from_pos(
                        i.name, frame, number_start, number_end)
                rates_frame = pd.DataFrame(rates)
                rates_frame['time'] = pd.to_datetime(
                        rates_frame['time'], unit='s')
                symbol_data[i.name] = {
                        i.name: i.name,
                        'open': rates_frame['open'],
                        'close': rates_frame['close'],
                        'low': rates_frame['low'],
                        'high': rates_frame['high'],
                        'HL/2': (rates_frame['high'] + rates_frame['low']) / 2,
                        'HLC/3': (rates_frame['high'] + rates_frame['low'] +
                                  rates_frame['close']) / 3,
                        'HLCC/4': (rates_frame['high'] + rates_frame['low'] +
                                   rates_frame['close'] + rates_frame['close']
                                   ) / 4,
                        'OHLC/4': (rates_frame['high'] + rates_frame['low'] +
                                   rates_frame['close'] + rates_frame['open']
                                   ) / 4,
                        'volume': rates_frame['tick_volume'],
                        'time': rates_frame['time']
                }
            except Exception as ex:
                logs('warning', ex)

        return symbol_data, self.account_info_dict['balance'], symbols
