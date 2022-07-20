from Mt5_Config import accountConfig
from datetime import datetime

try:
	from MetaTrader5 import *
	import MetaTrader5 as mt5
except Exception as ex:
	print('login get data : ',ex)

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

#********* Methodes:

#login()
#getall()
#getone()
#writer()
#readone()
#readall()
#get_symbols()
#get_balance()
#initilizer()

#/////////////////////

class LoginGetData:

	def __init__(self): self.account_name = ''

	def getall(self, timeframe, number):

		symbols = self.get_symbols()
		symbol_data = {}

		for sym in symbols:
			try:
				data = self.getone(timeframe = timeframe, number = number, symbol = sym.name)
				symbol_data[sym.name] = data[sym.name]
				symbol_data['balance'] = data['balance']
				symbol_data['symbols'] = data['symbols']
			except Exception as ex:
				print("Get All Error: ", ex)
		return symbol_data


	def getone(self, timeframe, number, symbol):

		timeframe = self.timeframechecker(timeframe = timeframe)

		self.initilizer()
		self.login()

		account_info = mt5.account_info()

		if account_info != None:
			account_info_dict = mt5.account_info()._asdict()
		else:
			print("failed to connect to trade account %s, error code = " % (self.account_name), mt5.last_error())

		symbols = mt5.symbols_get()
		symbol_data = {}

		try:
			rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, number)
			rates_frame = pd.DataFrame(rates)
			# convert time in seconds into the datetime format
			rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

			symbol_data[symbol] = pd.DataFrame({
												symbol: symbol,
												'open': rates_frame['open'],
												'close': rates_frame['close'],
												'low': rates_frame['low'],
												'high': rates_frame['high'],
												'HL/2': ((rates_frame['high']+rates_frame['low'])/2),
												'HLC/3': ((rates_frame['high']+rates_frame['low']+rates_frame['close'])/3),
												'HLCC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['close'])/4),
												'OHLC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['open'])/4),
												'volume': rates_frame['tick_volume'],
												'time': rates_frame['time']
												})
			symbol_data['balance'] = account_info_dict["balance"]
			symbol_data['symbols'] = symbols
			symbol_data['symbol'] = symbol

		except Exception as ex:
			print("get data one by one Error: ", ex)

		mt5.shutdown()

		return symbol_data

	def writer(self, symbol, timeframe, number):

		data = self.loging.getone(timeframe = timeframe, number = number, symbol = symbol)

		dataset_path = 'dataset/' + timeframe + '/' + symbol + '.csv'
		dataset_path_dir = 'dataset/' + timeframe + '/'

		if not os.path.exists(dataset_path_dir):
			os.makedirs(dataset_path_dir)

		if os.path.exists(dataset_path):
			os.remove(dataset_path)

		data[symbol].to_csv(dataset_path)

	def readone(self, timeframe, symbol, number):

		dataset_path = 'dataset/' + timeframe + '/' + symbol + '.csv'
		
		symbols = symbol
		count=0
		symbol_data_5M = {}
		symbol_data_1H = {}

		if os.path.exists(dataset_path):
			rates_frame = pd.read_csv(dataset_path)
			if timeframe == '5M':
				symbol_data_5M[symbol] = pd.DataFrame({
													symbol: symbol,
													'open': rates_frame['open'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
													'close': rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
													'low': rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
													'high': rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
													'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/2),
													'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/3),
													'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/4),
													'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/4),
													'volume': rates_frame['volume'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
													'time': rates_frame['time'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)
													})
				time_counter = 0
				for ti in symbol_data_5M[symbol]['time']:
					symbol_data_5M[symbol]['time'][time_counter] = datetime.strptime(symbol_data_5M[symbol]['time'][time_counter], "%Y-%m-%d %H:%M:%S")
					time_counter += 1

				return symbol_data_5M
			else:
				rates_frame = pd.read_csv(dataset_path)
				symbol_data_1H[symbol] = pd.DataFrame({
														symbol: symbol,
														'open': rates_frame['open'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
														'close': rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
														'low': rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
														'high': rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
														'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/2),
														'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/3),
														'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/4),
														'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True))/4),
														'volume': rates_frame['volume'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True),
														'time': rates_frame['time'][(len(rates_frame['open'])-number-1):-1].reset_index(drop=True)
														})

				time_counter = 0
				for ti in symbol_data_1H[symbol]['time']:
					symbol_data_1H[symbol]['time'][time_counter] = datetime.strptime(symbol_data_1H[symbol]['time'][time_counter], "%Y-%m-%d %H:%M:%S")
					time_counter += 1

				return symbol_data_1H
		
	def readall(self, symbol, number_5M, number_1H):

		dataset_path_5M = 'dataset/5M/' + symbol + '.csv'
		dataset_path_1H = 'dataset/1H/' + symbol + '.csv'

		symbol_data_5M = {}
		symbol_data_1H = {}

		symbol_data_5M[symbol] = self.readone(timeframe = '5M', symbol = symbol, number = number_5M)

		symbol_data_1H[symbol] = self.readone(timeframe = '1H', symbol = symbol, number = number_1H)

		return symbol_data_5M, symbol_data_1H

		
	def get_symbols(self):

		self.initilizer()
		
		self.login()

		symbols = mt5.symbols_get()

		mt5.shutdown()

		return symbols

	def get_balance(self):

		self.initilizer()
		
		self.login()

		account_info = mt5.account_info()

		if account_info!=None:
			account_info_dict = mt5.account_info()._asdict()

			return account_info_dict["balance"]
		else:
			print("failed to connect to trade account %s, error code =" % (self.account_name), mt5.last_error())

		mt5.shutdown()

	def initilizer(self):

		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()

	def login(self):
		mt5.login(login = accountConfig()[self.account_name]['username'], password = accountConfig()[self.account_name]['password'])

	def timeframechecker(self, timeframe):
		if timeframe == '5M':
			timeframe = mt5.TIMEFRAME_M5
		elif timeframe == '1H':
			timeframe = mt5.TIMEFRAME_H1
		return timeframe

#login=51149098, server="Alpari-MT5-Demo",password="zyowt2zj"
# loging = LogingGetData()
# loging.account_name = 'mehrshadpc'
# loging.initilizer()
# loging.login()
# #print(mt5.TIMEFRAME_H1)

# for sym in loging.get_symbols():
#  	print(sym.name)

# print(loging.get_balance())
# data = loging.getone(timeframe = mt5.TIMEFRAME_M5, number = 500, symbol = 'XAUUSD_i')
# print(data['XAUUSD_i'])

# data = loging.getall(timeframe = mt5.TIMEFRAME_M5, number = 500)
# print(data)