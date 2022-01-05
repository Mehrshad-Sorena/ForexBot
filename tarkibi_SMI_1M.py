from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
#import matplotlib.pyplot as plt
import numpy as np
from find_flat import *
from three_flat_find import *
from cross_TsKs_Buy_signal import *
from exit_signal_TsKs import *
from chiko_signal import *
from log_get_data import *
import math
from divergence import *
from cross_macd import *
import schedule
import time
import os
from datetime import date
import datetime
import pytz
import threading
import concurrent.futures
import logging
import csv
from Genetic_MACD_buysell_algo_onebyone import *
from multiprocessing import Process
import threading
from Accounts import *
from UTC_Time import *
from SMA_Signal_Cross import *
import logging

#from ta import add_all_ta_features
#from ind.utils import dropna
#from ind.trend import MACD
#symbol_data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
#symbol_data_ichi,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)


def trade_strategy_SMI_1M():
	max_allow_score = 20
	#print(ind.version)
#python -m pip install -U --force-reinstall pip

#class symbol_data:
#	def __init__(self, name, open_candle, close_candle, high_candel, low_candle, volume_candle, time_candle):
#		self.name = name
#		self.open_candle = open_candle
#		self.close_candle = close_candle
#		self.high_candel = high_candel
#		self.low_candle = low_candle
#		self.volume_candle = volume_candle
#		self.time_candle = time_candle

	hour,minute,second,day = time_func()

	log_name = 'Logs/main_bot/bot_log_'+day+'-'+str(hour)+'-'+str(minute)+'-'+str(second)+'.log'
	
	logging.basicConfig(filename=log_name, level=logging.DEBUG)

	#logging.debug('This message should go to the log file')
	#logging.info('So should this')
	#logging.warning('And this, too')
	#logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
	

	#print('Loading Data 1 .............')
	logging.info('Loading Data 1 .............')

	

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)
	#print(my_money)
	logging.info('my_money= %f'%my_money)

	#print('Start Checking .............')
	logging.info('Start Checking .............')

	#print("money",my_money)
#print("symbol = ",symbols.name)

	#symbol_data = symbol_daind.append(symbol_data_local, ignore_index = True)	

#print(type(MACD(symbol_data['EURUSD']['open'],26,12,9,False) ))

	magic = time.time_ns()

	for sym in symbols:

		if (my_money == 0): break

		if (sym.name == 'RUBRUR'):continue
		if (sym.name == 'EURDKK_i'): continue
		if (sym.name == 'USDDKK_i'): continue
		if (sym.name == 'USDTRY_i'): continue
		if (sym.name == 'EURTRY_i'): continue
		if (sym.name == '_DJI'):continue
		if (sym.name == '_DXY'):continue
		if (sym.name == 'BTCUSD_i'):continue
		if (sym.name == 'ETHUSD_i'):continue
		if (sym.name == 'LTCUSD_i'):continue
		if (sym.name == 'XBNUSD_i'):continue
		if (sym.name == 'XRPUSD_i'):continue
		if (sym.name == 'DAX30_i'):continue
		if (sym.name == 'RUBRUR'):continue
		if (sym.name == 'FTSE100_i'):continue
		if (sym.name == 'IBEX35_i'):continue
		if (sym.name == 'NIKK225_i'):continue
		if (sym.name == 'SPX500_i'):continue
		if (sym.name == 'ASX200_i'):continue
		if (sym.name == 'CAC40_i'):continue
		if (sym.name == 'HSI50_i'):continue
		if (sym.name == 'NG_i'):continue
		if (sym.name == 'NQ100_i'):continue
		if (sym.name == 'STOXX50_i'):continue
		if (sym.name == 'BRN_i'):continue
		if (sym.name == 'WTI_i'):continue
		if (sym.name == 'USDHKD'):continue
		if (sym.name == 'USDRUB_i'):continue
		if (sym.name == 'USDRUB'):continue

		logging.info('***********************************************************************************************************************')
		logging.info('***********************************************************************************************************************')
		logging.info('***********************************************************************************************************************')
		logging.debug('                                           %s' %sym.name)
		#print('***********************************************************************************************************************')
		#print('***********************************************************************************************************************')
		#print('***********************************************************************************************************************')
		#print('                                           ', sym.name,'                                                               ')

		symbol_data_5M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M5,1000,sym.name)
		symbol_data_1M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M1,1000,sym.name)
		symbol_data_30M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M30,1000,sym.name)
		symbol_data_1H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H1,300,sym.name)
		#symbol_data_4H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H4,300,sym.name)
		symbol_data_15M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M15,1000,sym.name)
		symbol_data_1D,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_D1,300,sym.name)

		vol_traded_max = (my_money/100) * 0.1

		symbol_data_vol,my_money,symbols_vol = log_get_data(mt5.TIMEFRAME_M1,10)

		vol_traded = 0

		flag_same_sell_1M = ''
		flag_same_buy_1M = ''

		flag_same_sell_5M = ''
		flag_same_buy_5M = ''

		flag_same_sell_15M = ''
		flag_same_buy_15M = ''

		flag_same_sell_5M15M = ''
		flag_same_buy_5M15M = ''

		flag_same_sell_15M30M = ''
		flag_same_buy_15M30M = ''

		flag_same_sell_5M1H = ''
		flag_same_buy_5M1H = ''

		for sym_vol in symbols_vol:
			positions = mt5.positions_get(symbol=sym_vol.name)
			#print(positions)
			if positions == None:
				print("No positions on ",sym_vol.name,", error code={}".format(mt5.last_error()))
			elif len(positions)>0:
				for position in positions:
					type_position = position[5]
					vol_position = position[9]
					symbol_position = position[16]
					comment_position = position[17]

					vol_traded += vol_position

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '15M1H gen SMI')):
						#print('same sell')
						flag_same_sell_15M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '15M1H gen SMI')):
						#print('same buy')
						flag_same_buy_15M = 'same_buy'

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '15M30M gen SMI')):
						#print('same sell')
						flag_same_sell_15M30M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '15M30M gen SMI')):
						#print('same buy')
						flag_same_buy_15M30M = 'same_buy'

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M1H gen SMI')):
						#print('same sell')
						flag_same_sell_5M1H = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M1H gen SMI')):
						#print('same buy')
						flag_same_buy_5M1H = 'same_buy'

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M30M gen SMI')):
						#print('same sell')
						flag_same_sell_5M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M30M gen SMI')):
						#print('same buy')
						flag_same_buy_15M30M = 'same_buy'

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M15M gen SMI')):
						#print('same sell')
						flag_same_sell_5M15M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M15M gen SMI')):
						#print('same buy')
						flag_same_buy_5M15M = 'same_buy'

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '1M gen SMI')):
						#print('same sell')
						flag_same_sell_1M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '1M gen SMI')):
						#print('same buy')
						flag_same_buy_1M = 'same_buy'


					          
						


		#print(sym.name)
		if (vol_traded >= vol_traded_max): 
			#print('No Money')
			logging.warning('No Money')
			break

		#print(sym.name)
#g = float("{:.2f}".format(x))

		
		#****************************** Data_Buy 1M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_1M_buy = line
					data_macd_1M_buy['tp'] = float(data_macd_1M_buy['tp'])
					data_macd_1M_buy['tp'] = (data_macd_1M_buy['tp']/3)*2

					data_macd_1M_buy['st'] = float(data_macd_1M_buy['st'])
					data_macd_1M_buy['macd_fast'] = float(data_macd_1M_buy['macd_fast'])
					data_macd_1M_buy['macd_slow'] = float(data_macd_1M_buy['macd_slow'])
					data_macd_1M_buy['macd_signal'] = float(data_macd_1M_buy['macd_signal'])
					data_macd_1M_buy['diff_minus'] = float(data_macd_1M_buy['diff_minus'])
					data_macd_1M_buy['diff_plus'] = float(data_macd_1M_buy['diff_plus'])
					data_macd_1M_buy['score'] = (float(data_macd_1M_buy['score']))

		except:
			#continue

			data_macd_1M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)

				macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1M_buy)))

				data_macd_1M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2) ,'score': 100}

			except:
				#print('Cant calc MACD 1M BUY')
				logging.warning('Cant calc MACD 1M BUY')
				continue
				data_macd_1M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0 ,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 1M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1M_sell = line
					data_macd_1M_sell['tp'] = float(data_macd_1M_sell['tp'])
					data_macd_1M_sell['tp'] = (data_macd_1M_sell['tp']/3)*2

					data_macd_1M_sell['st'] = float(data_macd_1M_sell['st'])
					data_macd_1M_sell['macd_fast'] = float(data_macd_1M_sell['macd_fast'])
					data_macd_1M_sell['macd_slow'] = float(data_macd_1M_sell['macd_slow'])
					data_macd_1M_sell['macd_signal'] = float(data_macd_1M_sell['macd_signal'])
					data_macd_1M_sell['diff_minus'] = float(data_macd_1M_sell['diff_minus'])
					data_macd_1M_sell['diff_plus'] = float(data_macd_1M_sell['diff_plus'])
					data_macd_1M_sell['score'] = (float(data_macd_1M_sell['score']))

		except:
			#continue
			data_macd_1M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)

				macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1M_sell)))

				data_macd_1M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2),'score': 100}

			except:
				#print('Cant calc MACD 1M SELL')
				logging.warning('Cant calc MACD 1M SELL')
				data_macd_1M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 5M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_5M_buy = line
					data_macd_5M_buy['tp'] = float(data_macd_5M_buy['tp'])
					data_macd_5M_buy['tp'] = (data_macd_5M_buy['tp']/3)*2

					data_macd_5M_buy['st'] = float(data_macd_5M_buy['st'])
					data_macd_5M_buy['macd_fast'] = float(data_macd_5M_buy['macd_fast'])
					data_macd_5M_buy['macd_slow'] = float(data_macd_5M_buy['macd_slow'])
					data_macd_5M_buy['macd_signal'] = float(data_macd_5M_buy['macd_signal'])
					data_macd_5M_buy['diff_minus'] = float(data_macd_5M_buy['diff_minus'])
					data_macd_5M_buy['diff_plus'] = float(data_macd_5M_buy['diff_plus'])
					data_macd_5M_buy['score'] = (float(data_macd_5M_buy['score']) / 2)

					if(data_macd_5M_buy['score'] < max_allow_score):
						data_macd_5M_buy['score'] = data_macd_5M_buy['score']/10

		except:
			#continue

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			try:
				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_buy)))

				data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			except:
				#print('Cant calc MACD 5M Buy')
				logging.warning('Cant calc MACD 5M Buy')
				data_macd_5M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 5M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M_sell = line
					data_macd_5M_sell['tp'] = float(data_macd_30M_sell['tp'])
					data_macd_5M_sell['tp'] = (data_macd_30M_sell['tp']/3)*2

					data_macd_5M_sell['st'] = float(data_macd_30M_sell['st'])
					data_macd_5M_sell['macd_fast'] = float(data_macd_5M_sell['macd_fast'])
					data_macd_5M_sell['macd_slow'] = float(data_macd_5M_sell['macd_slow'])
					data_macd_5M_sell['macd_signal'] = float(data_macd_5M_sell['macd_signal'])
					data_macd_5M_sell['diff_minus'] = float(data_macd_5M_sell['diff_minus'])
					data_macd_5M_sell['diff_plus'] = float(data_macd_5M_sell['diff_plus'])
					data_macd_5M_sell['score'] = (float(data_macd_5M_sell['score']) / 2)

					if(data_macd_5M_sell['score'] < max_allow_score):
						data_macd_5M_sell['score'] = data_macd_5M_sell['score']/10

		except:
			#continue
			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_sell)))

				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

			except:
				#print('Cant calc MACD 5M SELL')
				logging.warning('Cant calc MACD 5M SELL')
				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Buy 30M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_30M_buy = line
					data_macd_30M_buy['tp'] = float(data_macd_30M_buy['tp'])
					data_macd_30M_buy['tp'] = (data_macd_30M_buy['tp']/3)*2

					data_macd_30M_buy['st'] = float(data_macd_30M_buy['st'])
					data_macd_30M_buy['macd_fast'] = float(data_macd_30M_buy['macd_fast'])
					data_macd_30M_buy['macd_slow'] = float(data_macd_30M_buy['macd_slow'])
					data_macd_30M_buy['macd_signal'] = float(data_macd_30M_buy['macd_signal'])
					data_macd_30M_buy['diff_minus'] = float(data_macd_30M_buy['diff_minus'])
					data_macd_30M_buy['diff_plus'] = float(data_macd_30M_buy['diff_plus'])
					data_macd_30M_buy['score'] = (float(data_macd_30M_buy['score']) / 2)

		except:
			#continue

			data_macd_30M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			try:
				macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

				macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_buy)))

				data_macd_30M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			except:
				#print('Cant calc MACD 30M Buy')
				logging.warning('Cant calc MACD 30M Buy')
				data_macd_30M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 30M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_30M_sell = line
					data_macd_30M_sell['tp'] = float(data_macd_30M_sell['tp'])
					data_macd_30M_sell['tp'] = (data_macd_30M_sell['tp']/3)*2

					data_macd_30M_sell['st'] = float(data_macd_30M_sell['st'])
					data_macd_30M_sell['macd_fast'] = float(data_macd_30M_sell['macd_fast'])
					data_macd_30M_sell['macd_slow'] = float(data_macd_30M_sell['macd_slow'])
					data_macd_30M_sell['macd_signal'] = float(data_macd_30M_sell['macd_signal'])
					data_macd_30M_sell['diff_minus'] = float(data_macd_30M_sell['diff_minus'])
					data_macd_30M_sell['diff_plus'] = float(data_macd_30M_sell['diff_plus'])
					data_macd_30M_sell['score'] = (float(data_macd_30M_sell['score']) / 2)

					if(data_macd_30M_sell['score'] < max_allow_score):
						data_macd_30M_sell['score'] = data_macd_30M_sell['score']/10

		except:
			#continue
			data_macd_30M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

				macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_sell)))

				data_macd_30M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

			except:
				#print('Cant calc MACD 30M SELL')
				logging.warning('Cant calc MACD 30M SELL')
				data_macd_30M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Buy 15M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_15M_buy = line
					data_macd_15M_buy['tp'] = float(data_macd_15M_buy['tp'])
					data_macd_15M_buy['tp'] = (data_macd_15M_buy['tp']/3)*2

					data_macd_15M_buy['st'] = float(data_macd_15M_buy['st'])
					data_macd_15M_buy['macd_fast'] = float(data_macd_15M_buy['macd_fast'])
					data_macd_15M_buy['macd_slow'] = float(data_macd_15M_buy['macd_slow'])
					data_macd_15M_buy['macd_signal'] = float(data_macd_15M_buy['macd_signal'])
					data_macd_15M_buy['diff_minus'] = float(data_macd_15M_buy['diff_minus'])
					data_macd_15M_buy['diff_plus'] = float(data_macd_15M_buy['diff_plus'])
					data_macd_15M_buy['score'] = (float(data_macd_15M_buy['score']))

		except:
			#continue

			data_macd_15M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)

				macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_15M_buy)))

				data_macd_15M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2) ,'score': 160}

			except:
				#print('Cant calc MACD 15M BUY')
				logging.warning('Cant calc MACD 15M BUY')
				data_macd_15M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 15M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_15M_sell = line
					data_macd_15M_sell['tp'] = float(data_macd_15M_sell['tp'])
					data_macd_15M_sell['tp'] = (data_macd_15M_sell['tp']/3)*2

					data_macd_15M_sell['st'] = float(data_macd_15M_sell['st'])
					data_macd_15M_sell['macd_fast'] = float(data_macd_15M_sell['macd_fast'])
					data_macd_15M_sell['macd_slow'] = float(data_macd_15M_sell['macd_slow'])
					data_macd_15M_sell['macd_signal'] = float(data_macd_15M_sell['macd_signal'])
					data_macd_15M_sell['diff_minus'] = float(data_macd_15M_sell['diff_minus'])
					data_macd_15M_sell['diff_plus'] = float(data_macd_15M_sell['diff_plus'])
					data_macd_15M_sell['score'] = (float(data_macd_15M_sell['score']))

		except:
			#continue
			data_macd_15M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)

				macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_15M_sell)))

				data_macd_15M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2),'score': 160}

			except:
				#print('Cant calc MACD 15M SELL')
				logging.warning('Cant calc MACD 15M SELL')
				data_macd_15M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 1H MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_1H_buy = line
					data_macd_1H_buy['tp'] = float(data_macd_1H_buy['tp'])
					data_macd_1H_buy['tp'] = (data_macd_1H_buy['tp']/3)*2

					data_macd_1H_buy['st'] = float(data_macd_1H_buy['st'])
					data_macd_1H_buy['macd_fast'] = float(data_macd_1H_buy['macd_fast'])
					data_macd_1H_buy['macd_slow'] = float(data_macd_1H_buy['macd_slow'])
					data_macd_1H_buy['macd_signal'] = float(data_macd_1H_buy['macd_signal'])
					data_macd_1H_buy['diff_minus'] = float(data_macd_1H_buy['diff_minus'])
					data_macd_1H_buy['diff_plus'] = float(data_macd_1H_buy['diff_plus'])
					data_macd_1H_buy['score'] = (float(data_macd_1H_buy['score']) / 2)

					if(data_macd_1H_buy['score'] < max_allow_score):
						data_macd_1H_buy['score'] = data_macd_1H_buy['score']/10

		except:
			#continue

			data_macd_1H_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			try:
				macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)

				macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1H_buy)))

				data_macd_1H_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			except:
				#print('Cant calc MACD 1H BUY')
				logging.warning('Cant calc MACD 1H BUY')
				data_macd_1H_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 1H MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1H_sell = line
					data_macd_1H_sell['tp'] = float(data_macd_1H_sell['tp'])
					data_macd_1H_sell['tp'] = (data_macd_1H_sell['tp']/3)*2

					data_macd_1H_sell['st'] = float(data_macd_1H_sell['st'])
					data_macd_1H_sell['macd_fast'] = float(data_macd_1H_sell['macd_fast'])
					data_macd_1H_sell['macd_slow'] = float(data_macd_1H_sell['macd_slow'])
					data_macd_1H_sell['macd_signal'] = float(data_macd_1H_sell['macd_signal'])
					data_macd_1H_sell['diff_minus'] = float(data_macd_1H_sell['diff_minus'])
					data_macd_1H_sell['diff_plus'] = float(data_macd_1H_sell['diff_plus'])
					data_macd_1H_sell['score'] = (float(data_macd_1H_sell['score']) / 2)

					if(data_macd_1H_sell['score'] < max_allow_score):
						data_macd_1H_sell['score'] = data_macd_1H_sell['score']/10

		except:
			#continue
			data_macd_1H_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

				macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1H_sell)))

				data_macd_1H_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

			except:
				#print('Cant calc MACD 1H SELL')
				logging.warning('Cant calc MACD 1H SELL')
				data_macd_1H_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 1D MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_1D_buy = line
					data_macd_1D_buy['tp'] = float(data_macd_1D_buy['tp'])
					data_macd_1D_buy['tp'] = (data_macd_1D_buy['tp']/3)*2

					data_macd_1D_buy['st'] = float(data_macd_1D_buy['st'])
					data_macd_1D_buy['macd_fast'] = float(data_macd_1D_buy['macd_fast'])
					data_macd_1D_buy['macd_slow'] = float(data_macd_1D_buy['macd_slow'])
					data_macd_1D_buy['macd_signal'] = float(data_macd_1D_buy['macd_signal'])
					data_macd_1D_buy['diff_minus'] = float(data_macd_1D_buy['diff_minus'])
					data_macd_1D_buy['diff_plus'] = float(data_macd_1D_buy['diff_plus'])
					data_macd_1D_buy['score'] = (float(data_macd_1D_buy['score']) / 2)

					if(data_macd_1D_buy['score'] < max_allow_score):
						data_macd_1D_buy['score'] = data_macd_1D_buy['score']/10

		except:
			#continue

			data_macd_1D_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			try:
				macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

				macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1D_buy)))

				data_macd_1D_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			except:
				#print('Cant calc MACD 1D BUY')
				logging.warning('Cant calc MACD 1D BUY')
				data_macd_1D_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 1D MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1D_sell = line
					data_macd_1D_sell['tp'] = float(data_macd_1D_sell['tp'])
					data_macd_1D_sell['tp'] = (data_macd_1D_sell['tp']/3)*2

					data_macd_1D_sell['st'] = float(data_macd_1D_sell['st'])
					data_macd_1D_sell['macd_fast'] = float(data_macd_1D_sell['macd_fast'])
					data_macd_1D_sell['macd_slow'] = float(data_macd_1D_sell['macd_slow'])
					data_macd_1D_sell['macd_signal'] = float(data_macd_1D_sell['macd_signal'])
					data_macd_1D_sell['diff_minus'] = float(data_macd_1D_sell['diff_minus'])
					data_macd_1D_sell['diff_plus'] = float(data_macd_1D_sell['diff_plus'])
					data_macd_1D_sell['score'] = (float(data_macd_1D_sell['score']) / 2)

					if(data_macd_1D_sell['score'] < max_allow_score):
						data_macd_1D_sell['score'] = data_macd_1D_sell['score']/10

		except:
			#continue
			data_macd_1D_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_1D_sell = ind.macd(symbol_data_1D[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

				macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1D_sell)))

				data_macd_1D_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

			except:
				#print('Cant calc MACD 1D SELL')
				logging.warning('Cant calc MACD 1D SELL')
				data_macd_1D_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************


		#******************************//////////////////////***********************************************************
		#print('////////////////////////////////////////////')
		#print('Loading Data 2 .............')

		logging.debug('////////////////////////////////////////////')
		logging.debug('Loading Data 2 .............')

		symbol_data_5M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M5,1000,sym.name)
		symbol_data_1M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M1,1000,sym.name)
		symbol_data_30M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M30,1000,sym.name)
		symbol_data_1H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H1,300,sym.name)
		symbol_data_4H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H4,300,sym.name)
		symbol_data_15M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M15,1000,sym.name)
		symbol_data_1D,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_D1,300,sym.name)

		#print('Start Calculate .............')
		logging.debug('Start Calculate .............')


		#****************************************** Res_Buy_Protection_Sell ***************************************************************

		i = 0
		j = 0

		resist_buy = {}
		protect_sell = {}

		resist_buy_final = {}
		protect_sell_final = {}


		resist_buy_final_1D = {}
		protect_sell_final_1D = {}


		resist_buy_final_4H = {}
		protect_sell_final_4H = {}

		resist_buy_final_1H = {}
		protect_sell_final_1H = {}

		resist_buy_final_30M = {}
		protect_sell_final_30M = {}

		resist_buy_final_1M = {}
		protect_sell_final_1M = {}

		resist_buy_final_5M = {}
		protect_sell_final_5M = {}

		resist_buy_final_15M = {}
		protect_sell_final_15M = {}

		try:
			with open("Res_Buy_Protection_Sell/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (((symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 1)] + symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 2)])/2) < resist_buy[i]):
							resist_buy_final_1D[j] = resist_buy[i]
							resist_buy_final[j] = resist_buy[i]

							j += 1

						if (((symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 1)] + symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 2)])/2) < resist_buy[i]):
							resist_buy_final_1D[j] = resist_buy[i]
							resist_buy_final[j] = resist_buy[i]

							j += 1

						if (((symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 1)] + symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 2)])/2) < protect_sell[i]):
							protect_sell_final_1D[j] = protect_sell[i]
							protect_sell_final[j] = protect_sell[i]

							j += 1

						if (((symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 1)] + symbol_data_1D[sym.name]['open'][(len(symbol_data_1D[sym.name]['open']) - 2)])/2) < protect_sell[i]):
							protect_sell_final_1D[j] = protect_sell[i]
							protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 1D')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 1D')

		#print(resist_buy)

		resist_buy = {}
		protect_sell = {}

		try:
			with open("Res_Buy_Protection_Sell/4H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (((symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 1)] + symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 2)])/2) < resist_buy[i]):
							resist_buy_final_4H[j] = resist_buy[i]
							resist_buy_final[j] = resist_buy[i]

							j += 1

						if (((symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 1)] + symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 2)])/2) < resist_buy[i]):
							resist_buy_final_4H[j] = resist_buy[i]
							resist_buy_final[j] = resist_buy[i]

							j += 1

						if (((symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 1)] + symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 2)])/2) < protect_sell[i]):
							protect_sell_final_4H[j] = protect_sell[i]
							protect_sell_final[j] = protect_sell[i]

							j += 1

						if (((symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 1)] + symbol_data_4H[sym.name]['open'][(len(symbol_data_4H[sym.name]['open']) - 2)])/2) < protect_sell[i]):
							protect_sell_final_4H[j] = protect_sell[i]
							protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 4H')


		resist_buy = {}
		protect_sell = {}


		try:
			with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_1H[sym.name]['HLC/3'][(len(symbol_data_1H[sym.name]['high'])-1)] + symbol_data_1H[sym.name]['HLC/3'][(len(symbol_data_1H[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['low'])-1)] + symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (price_ask < resist_buy[i]):
							resist_buy_final_1H[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_ask < resist_buy[i]):
							resist_buy_final_1H[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_1H[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_1H[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 1H')


		resist_buy = {}
		protect_sell = {}


		try:
			with open("Res_Buy_Protection_Sell/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_30M[sym.name]['HLC/3'][(len(symbol_data_30M[sym.name]['high'])-1)] + symbol_data_30M[sym.name]['HLC/3'][(len(symbol_data_30M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_30M[sym.name]['high'][(len(symbol_data_30M[sym.name]['low'])-1)] + symbol_data_30M[sym.name]['high'][(len(symbol_data_30M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (price_ask < resist_buy[i]):
							resist_buy_final_30M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_ask < resist_buy[i]):
							resist_buy_final_30M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_30M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_30M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 30M')


		#*************************************** 1M ******************************************************
		resist_buy = {}
		protect_sell = {}

		try:
			with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_1M[sym.name]['HLC/3'][(len(symbol_data_1M[sym.name]['high'])-1)] + symbol_data_1M[sym.name]['HLC/3'][(len(symbol_data_1M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_1M[sym.name]['high'][(len(symbol_data_1M[sym.name]['low'])-1)] + symbol_data_1M[sym.name]['high'][(len(symbol_data_1M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (price_ask < resist_buy[i]):
							resist_buy_final_1M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_ask < resist_buy[i]):
							resist_buy_final_1M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_1M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_1M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 1M')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#************************* 5M ************************************************************************************
		resist_buy = {}
		protect_sell = {}

		try:
			with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_5M[sym.name]['HLC/3'][(len(symbol_data_5M[sym.name]['HLC/3'])-1)] + symbol_data_5M[sym.name]['HLC/3'][(len(symbol_data_5M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_5M[sym.name]['high'][(len(symbol_data_5M[sym.name]['low'])-1)] + symbol_data_5M[sym.name]['high'][(len(symbol_data_5M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (price_ask < resist_buy[i]):
							resist_buy_final_5M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_ask < resist_buy[i]):
							resist_buy_final_5M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_5M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_5M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************** 15M ******************************************************************
		resist_buy = {}
		protect_sell = {}

		try:
			with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_15M[sym.name]['HLC/3'][(len(symbol_data_15M[sym.name]['HLC/3'])-1)] + symbol_data_15M[sym.name]['HLC/3'][(len(symbol_data_15M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_15M[sym.name]['high'][(len(symbol_data_15M[sym.name]['low'])-1)] + symbol_data_15M[sym.name]['high'][(len(symbol_data_15M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):
					for l in line.values():

						resist_buy[i] = float(l)
						protect_sell[i] = float(l)

						if (price_ask < resist_buy[i]):
							resist_buy_final_15M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_ask < resist_buy[i]):
							resist_buy_final_15M[j] = resist_buy[i]
							#resist_buy_final[j] = resist_buy[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_15M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						if (price_bid < protect_sell[i]):
							protect_sell_final_15M[j] = protect_sell[i]
							#protect_sell_final[j] = protect_sell[i]

							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Buy_Protection_Sell 4H')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell 15M')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////



		resist_buy_find = 100000000000
		protect_sell_find = 100000000000

		resist_buy_find_1D = 100000000000
		protect_sell_find_1D = 100000000000

		resist_buy_find_4H = 100000000000
		protect_sell_find_4H = 100000000000

		resist_buy_find_1H = 100000000000
		protect_sell_find_1H = 100000000000


		resist_buy_find_1M = 100000000000
		protect_sell_find_1M = 100000000000

		resist_buy_find_5M = 100000000000
		protect_sell_find_5M = 100000000000

		resist_buy_find_15M = 100000000000
		protect_sell_find_15M = 100000000000

		resist_buy_find_30M = 100000000000
		protect_sell_find_30M = 100000000000

		try:
			if (len(resist_buy_final.values()) > 1):
				resist_buy_find = min(resist_buy_final.values())
			else:
				resist_buy_find = resist_buy_final.values()

			if (len(protect_sell_final.values()) > 1):
				protect_sell_find = min(protect_sell_final.values())
			else:
				protect_sell_find = protect_sell_final.values()


			if (len(resist_buy_final_1D.values()) > 1):
				resist_buy_find_1D = min(resist_buy_final_1D.values())
			else:
				resist_buy_find_1D = resist_buy_final_1D.values()

			if (len(protect_sell_final_1D.values()) > 1):	
				protect_sell_find_1D = min(protect_sell_final_1D.values())
			else:
				protect_sell_find_1D = protect_sell_final_1D.values()


			if (len(resist_buy_final_4H.values()) > 1):
				resist_buy_find_4H = min(resist_buy_final_4H.values())
			else:
				resist_buy_find_4H = resist_buy_final_4H.values()

			if (len(protect_sell_final_4H.values()) > 1):
				protect_sell_find_4H = min(protect_sell_final_4H.values())
			else:
				protect_sell_find_4H = protect_sell_final_4H.values()


			if (len(resist_buy_final_1H.values()) > 1):
				resist_buy_find_1H = min(resist_buy_final_1H.values())
			else:
				resist_buy_find_1H = resist_buy_final_1H.values()

			if (len(protect_sell_final_1H.values()) > 1):
				protect_sell_find_1H = min(protect_sell_final_1H.values())
			else:
				protect_sell_find_1H = protect_sell_final_1H.values()


			if (len(resist_buy_final_30M.values()) > 1):
				resist_buy_find_30M = min(resist_buy_final_30M.values())
			else:
				resist_buy_find_30M = resist_buy_final_30M.values()

			if (len(protect_sell_final_30M.values()) > 1):
				protect_sell_find_30M = min(protect_sell_final_30M.values())
			else:
				protect_sell_find_30M = protect_sell_final_30M.values()

			if (len(resist_buy_final_1M.values()) > 1):
				resist_buy_find_1M = min(resist_buy_final_1M.values())
				resist_buy_find_1M = min(resist_buy_find_1M,resist_buy_find_4H,resist_buy_find_1D)
			else:
				resist_buy_find_1M = resist_buy_final_1M.values()
				resist_buy_find_1M = min(resist_buy_find_1M,resist_buy_find_4H,resist_buy_find_1D)

			if (len(protect_sell_final_1M.values()) > 1):
				protect_sell_find_1M = min(protect_sell_final_1M.values())
				protect_sell_find_1M = min(protect_sell_find_1M,protect_sell_find_4H,protect_sell_find_1D)
			else:
				protect_sell_find_1M = protect_sell_final_1M.values()
				protect_sell_find_1M = min(protect_sell_find_1M,protect_sell_find_4H,protect_sell_find_1D)


			if (len(resist_buy_final_5M.values()) > 1):
				resist_buy_find_5M = min(resist_buy_final_5M.values())
				resist_buy_find_5M = min(resist_buy_find_5M,resist_buy_find_4H,resist_buy_find_1D)
			else:
				resist_buy_find_5M = resist_buy_final_5M.values()
				resist_buy_find_5M = min(resist_buy_find_5M,resist_buy_find_4H,resist_buy_find_1D)


			if (len(protect_sell_final_5M.values()) > 1):
				protect_sell_find_5M = min(protect_sell_final_5M.values())
				protect_sell_find_5M = min(protect_sell_find_5M,protect_sell_find_4H,protect_sell_find_1D)
			else:
				protect_sell_find_5M = protect_sell_final_5M.values()
				protect_sell_find_5M = min(protect_sell_find_5M,protect_sell_find_4H,protect_sell_find_1D)


			if (len(resist_buy_final_15M.values()) > 1):
				resist_buy_find_15M = min(resist_buy_final_15M.values())
				resist_buy_find_15M = min(resist_buy_find_15M,resist_buy_find_4H,resist_buy_find_1D)
			else:
				resist_buy_find_15M = resist_buy_final_15M.values()
				resist_buy_find_15M = min(resist_buy_find_15M,resist_buy_find_4H,resist_buy_find_1D)

			if (len(protect_sell_final_15M.values()) > 1):
				protect_sell_find_15M = min(protect_sell_final_15M.values())
				protect_sell_find_15M = min(protect_sell_find_15M,protect_sell_find_4H,protect_sell_find_1D)
			else:
				protect_sell_find_15M = protect_sell_final_15M.values()
				protect_sell_find_15M = min(protect_sell_find_15M,protect_sell_find_4H,protect_sell_find_1D)
		except:
			#print('some thing wrongt Res_Buy_Protection_Sell')
			logging.warning('some thing wrongt Res_Buy_Protection_Sell')

		#print('')
		#print('****** Calc Resist Buy and Protect Sell ********')
		#print('')

		logging.debug('')
		logging.debug('****** Calc Resist Buy and Protect Sell ********')
		logging.debug('')

		#print('resist_buy_find = ',resist_buy_find)
		#print('protect_sell_find = ',protect_sell_find)

		logging.debug('resist_buy_find = %f'%resist_buy_find)
		logging.debug('protect_sell_find = %f'%protect_sell_find)

		#print('resist_buy_find_1D = ',resist_buy_find_1D)
		#print('protect_sell_find_1D = ',protect_sell_find_1D)

		logging.debug('resist_buy_find_1D = %f'%resist_buy_find_1D)
		logging.debug('protect_sell_find_1D = %f'%protect_sell_find_1D)

		#print('resist_buy_find_4H = ',resist_buy_find_4H)
		#print('protect_sell_find_4H = ',protect_sell_find_4H)

		#logging.debug('resist_buy_find_4H = %f'%resist_buy_find_4H)
		#logging.debug('protect_sell_find_4H = %f'%protect_sell_find_4H)

		#logging.debug('resist_buy_find_1H = %f'%resist_buy_find_1H)
		#logging.debug('protect_sell_find_1H = %f'%protect_sell_find_1H)


		#logging.debug('resist_buy_find_30M = %f'%resist_buy_find_30M)
		#logging.debug('protect_sell_find_30M = %f'%protect_sell_find_30M)

		#print('////////////////////////////////////////////')
		logging.debug('////////////////////////////////////////////')
		logging.debug('')

		#print('')
		

		#*************************************************************************************************************
		#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#***************************** Res_Sell_Protection_Buy ***************************************************************************

		i = 0
		j = 0

		protect_buy = {}
		resist_sell = {}

		protect_buy_final = {}
		resist_sell_final = {}

		protect_buy_final_1D = {}
		resist_sell_final_1D = {}

		protect_buy_final_4H = {}
		resist_sell_final_4H = {}

		protect_buy_final_1H = {}
		resist_sell_final_1H = {}

		protect_buy_final_30M = {}
		resist_sell_final_30M = {}

		protect_buy_final_1M = {}
		resist_sell_final_1M = {}

		protect_buy_final_5M = {}
		resist_sell_final_5M = {}

		protect_buy_final_15M = {}
		resist_sell_final_15M = {}

		try:
			with open("Res_Sell_Protection_Buy/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_bid = mt5.symbol_info_tick(sym.name).bid
				price_ask = mt5.symbol_info_tick(sym.name).ask

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (((symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 1)] + symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 2)])/2) > protect_buy[i]):
							protect_buy_final_1D[j] = protect_buy[i]
							protect_buy_final[j] = protect_buy[i]
							j += 1

						if (((symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 1)] + symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 2)])/2) > protect_buy[i]):
							protect_buy_final_1D[j] = protect_buy[i]
							protect_buy_final[j] = protect_buy[i]
							j += 1

						if (((symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 1)] + symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 2)])/2) > resist_sell[i]):
							resist_sell_final_1D[j] = resist_sell[i]
							resist_sell_final[j] = resist_sell[i]
							j += 1

						if (((symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 1)] + symbol_data_1D[sym.name]['close'][(len(symbol_data_1D[sym.name]['close']) - 2)])/2) > resist_sell[i]):
							resist_sell_final_1D[j] = resist_sell[i]
							resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 1D')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 1D')

		protect_buy = {}
		resist_sell = {}

		try:
			with open("Res_Sell_Protection_Buy/4H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_bid = mt5.symbol_info_tick(sym.name).bid
				price_ask = mt5.symbol_info_tick(sym.name).ask

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (((symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 1)] + symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 2)])/2) > protect_buy[i]):
							protect_buy_final_4H[j] = protect_buy[i]
							protect_buy_final[j] = protect_buy[i]
							j += 1

						if (((symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 1)] + symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 2)])/2) > protect_buy[i]):
							protect_buy_final_4H[j] = protect_buy[i]
							protect_buy_final[j] = protect_buy[i]
							j += 1

						if (((symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 1)] + symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 2)])/2) > resist_sell[i]):
							resist_sell_final_4H[j] = resist_sell[i]
							resist_sell_final[j] = resist_sell[i]
							j += 1

						if (((symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 1)] + symbol_data_4H[sym.name]['close'][(len(symbol_data_4H[sym.name]['close']) - 2)])/2) > resist_sell[i]):
							resist_sell_final_4H[j] = resist_sell[i]
							resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 4H')

		protect_buy = {}
		resist_sell = {}


		try:
			with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_1H[sym.name]['HLC/3'][(len(symbol_data_1H[sym.name]['high'])-1)] + symbol_data_1H[sym.name]['HLC/3'][(len(symbol_data_1H[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low'])-1)] + symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (price_bid > protect_buy[i]):
							protect_buy_final_1H[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_bid > protect_buy[i]):
							protect_buy_final_1H[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_1H[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_1H[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 1H')

		protect_buy = {}
		resist_sell = {}


		try:
			with open("Res_Sell_Protection_Buy/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_30M[sym.name]['HLC/3'][(len(symbol_data_30M[sym.name]['high'])-1)] + symbol_data_30M[sym.name]['HLC/3'][(len(symbol_data_30M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_30M[sym.name]['low'][(len(symbol_data_30M[sym.name]['low'])-1)] + symbol_data_30M[sym.name]['low'][(len(symbol_data_30M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (price_bid > protect_buy[i]):
							protect_buy_final_30M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_bid > protect_buy[i]):
							protect_buy_final_30M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_30M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_30M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 30M')

		#******************************************* 1M **********************************************************

		protect_buy = {}
		resist_sell = {}

		try:
			with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_1M[sym.name]['HLC/3'][(len(symbol_data_1M[sym.name]['high'])-1)] + symbol_data_1M[sym.name]['HLC/3'][(len(symbol_data_1M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_1M[sym.name]['low'][(len(symbol_data_1M[sym.name]['low'])-1)] + symbol_data_1M[sym.name]['low'][(len(symbol_data_1M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (price_bid > protect_buy[i]):
							protect_buy_final_1M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_bid > protect_buy[i]):
							protect_buy_final_1M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_1M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_1M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 1M')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////

		#****************************************** 5M **********************************************************

		protect_buy = {}
		resist_sell = {}

		try:
			with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_5M[sym.name]['HLC/3'][(len(symbol_data_5M[sym.name]['high'])-1)] + symbol_data_5M[sym.name]['HLC/3'][(len(symbol_data_5M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_5M[sym.name]['low'][(len(symbol_data_5M[sym.name]['low'])-1)] + symbol_data_5M[sym.name]['low'][(len(symbol_data_5M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (price_bid > protect_buy[i]):
							protect_buy_final_5M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_bid > protect_buy[i]):
							protect_buy_final_5M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_5M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_5M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////

		#****************************************** 15M *********************************************************

		protect_buy = {}
		resist_sell = {}

		try:
			with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				price_ask = (symbol_data_15M[sym.name]['HLC/3'][(len(symbol_data_15M[sym.name]['high'])-1)] + symbol_data_15M[sym.name]['HLC/3'][(len(symbol_data_15M[sym.name]['high'])-2)])/2
				price_bid = (symbol_data_15M[sym.name]['low'][(len(symbol_data_15M[sym.name]['low'])-1)] + symbol_data_15M[sym.name]['low'][(len(symbol_data_15M[sym.name]['low'])-2)])/2

				for line in csv.DictReader(myfile):

					for l in line.values():

						protect_buy[i] = float(l)
						resist_sell[i] = float(l)

						if (price_bid > protect_buy[i]):
							protect_buy_final_15M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_bid > protect_buy[i]):
							protect_buy_final_15M[j] = protect_buy[i]
							#protect_buy_final[j] = protect_buy[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_15M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						if (price_ask > resist_sell[i]):
							resist_sell_final_15M[j] = resist_sell[i]
							#resist_sell_final[j] = resist_sell[i]
							j += 1

						i += 1

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy 4H')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy 15M')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////

		protect_buy_find = -100000000000
		resist_sell_find = -100000000000

		protect_buy_find_1D = -100000000000
		resist_sell_find_1D = -100000000000

		protect_buy_find_4H = -100000000000
		resist_sell_find_4H = -100000000000

		protect_buy_find_1H = -100000000000
		resist_sell_find_1H = -100000000000

		protect_buy_find_30M = -100000000000
		resist_sell_find_30M = -100000000000

		protect_buy_find_1M = -100000000000
		resist_sell_find_1M = -100000000000

		protect_buy_find_5M = -100000000000
		resist_sell_find_5M = -100000000000

		protect_buy_find_15M = -100000000000
		resist_sell_find_15M = -100000000000

		try:
			if (len(protect_buy_final.values()) > 1):
				protect_buy_find = max(protect_buy_final.values())
			else:
				protect_buy_find = protect_buy_final.values()

			if (len(resist_sell_final.values()) > 1):
				resist_sell_find = max(resist_sell_final.values())
			else:
				resist_sell_find = resist_sell_final.values()


			if (len(protect_buy_final_1D.values()) > 1):
				protect_buy_find_1D = max(protect_buy_final_1D.values())
			else:
				protect_buy_find_1D = protect_buy_final_1D.values()

			if (len(resist_sell_final_1D.values()) > 1):
				resist_sell_find_1D = max(resist_sell_final_1D.values())
			else:
				resist_sell_find_1D = max(resist_sell_final_1D.values())


			if (len(protect_buy_final_4H.values()) > 1):
				protect_buy_find_4H = max(protect_buy_final_4H.values())
			else:
				protect_buy_find_4H = protect_buy_final_4H.values()

			if (len(resist_sell_final_4H.values()) > 1):
				resist_sell_find_4H = max(resist_sell_final_4H.values())
			else:
				resist_sell_find_4H = resist_sell_final_4H.values()


			if (len(protect_buy_final_1H.values()) > 1):
				protect_buy_find_1H = max(protect_buy_final_1H.values())
			else:
				protect_buy_find_1H = protect_buy_final_1H.values()

			if (len(resist_sell_final_1H.values()) > 1):
				resist_sell_find_1H = max(resist_sell_final_1H.values())
			else:
				resist_sell_find_1H = resist_sell_final_1H.values()


			if (len(protect_buy_final_30M.values()) > 1):
				protect_buy_find_30M = max(protect_buy_final_30M.values())
			else:
				protect_buy_find_30M = protect_buy_final_30M.values()

			if (len(resist_sell_final_30M.values()) > 1):
				resist_sell_find_30M = max(resist_sell_final_30M.values())
			else:
				resist_sell_find_30M = resist_sell_final_30M.values()


			if (len(protect_buy_final_1M.values()) > 1):
				protect_buy_find_1M = max(protect_buy_final_1M.values())
				protect_buy_find_1M = max(protect_buy_find_1M,protect_buy_find_4H,protect_buy_find_1D)
			else:
				protect_buy_find_1M = protect_buy_final_1M.values()
				protect_buy_find_1M = max(protect_buy_find_1M,protect_buy_find_4H,protect_buy_find_1D)

			if (len(resist_sell_final_1M.values()) > 1):
				resist_sell_find_1M = max(resist_sell_final_1M.values())
				resist_sell_find_1M = max(resist_sell_find_1M,resist_sell_find_4h,resist_sell_find_1D)
			else:
				resist_sell_find_1M = resist_sell_final_1M.values()
				resist_sell_find_1M = max(resist_sell_find_1M,resist_sell_find_4h,resist_sell_find_1D)


			if (len(protect_buy_final_5M.values()) > 1):
				protect_buy_find_5M = max(protect_buy_final_5M.values())
				protect_buy_find_5M = max(protect_buy_find_5M,protect_buy_find_4H,protect_buy_find_1D)
			else:
				protect_buy_find_5M = protect_buy_final_5M.values()
				protect_buy_find_5M = max(protect_buy_find_5M,protect_buy_find_4H,protect_buy_find_1D)


			if (len(resist_sell_final_5M.values()) > 1):
				resist_sell_find_5M = max(resist_sell_final_5M.values())
				resist_sell_find_5M = max(resist_sell_find_5M,resist_sell_find_4h,resist_sell_find_1D)
			else:
				resist_sell_find_5M = resist_sell_final_5M.values()
				resist_sell_find_5M = max(resist_sell_find_5M,resist_sell_find_4h,resist_sell_find_1D)


			if (len(protect_buy_final_15M.values()) > 1):
				protect_buy_find_15M = max(protect_buy_final_15M.values())
				protect_buy_find_15M = max(protect_buy_find_15M,protect_buy_find_4H,protect_buy_find_1D)
			else:
				protect_buy_find_15M = protect_buy_final_15M.values()
				protect_buy_find_15M = max(protect_buy_find_15M,protect_buy_find_4H,protect_buy_find_1D)

			if (len(resist_sell_final_15M.values()) > 1):
				resist_sell_find_15M = max(resist_sell_final_15M.values())
				resist_sell_find_15M = max(resist_sell_find_15M,resist_sell_find_4h,resist_sell_find_1D)
			else:
				resist_sell_find_15M = resist_sell_final_15M.values()
				resist_sell_find_15M = max(resist_sell_find_15M,resist_sell_find_4h,resist_sell_find_1D)

		except:
			#print('some thing wrongt Res_Sell_Protection_Buy')
			logging.warning('some thing wrongt Res_Sell_Protection_Buy')

		#print('')
		#print('****** Calc Resist Sell and Protect Buy ********')
		#print('')

		logging.debug('')
		logging.debug('****** Calc Resist Sell and Protect Buy ********')
		logging.debug('')


		#print('protect_buy_find = ',protect_buy_find)
		#print('resist_sell_find = ',resist_sell_find)

		logging.debug('protect_buy_find = %f'%protect_buy_find)
		logging.debug('resist_sell_find = %f'%resist_sell_find)

		#print('protect_buy_find_1D = ',protect_buy_find_1D)
		#print('resist_sell_find_1D = ',resist_sell_find_1D)

		logging.debug('protect_buy_find_1D = %f'%protect_buy_find_1D)
		logging.debug('resist_sell_find_1D = %f'%resist_sell_find_1D)

		#print('protect_buy_find_4H = ',protect_buy_find_4H)
		#print('resist_sell_find_4H = ',resist_sell_find_4H)

		#logging.debug('protect_buy_find_4H = %f'%protect_buy_find_4H)
		#logging.debug('resist_sell_find_4H = %f'%resist_sell_find_4H)


		#logging.debug('protect_buy_find_1H = %f'%protect_buy_find_1H)
		#logging.debug('resist_sell_find_1H = %f'%resist_sell_find_1H)


		#logging.debug('protect_buy_find_30M = %f'%protect_buy_find_30M)
		#logging.debug('resist_sell_find_30M = %f'%resist_sell_find_30M)

		#print('////////////////////////////////////////////')
		#print('')

		logging.debug('////////////////////////////////////////////')
		logging.debug('')

		#price_bid = mt5.symbol_info_tick(sym.name).bid
		#price_ask = mt5.symbol_info_tick(sym.name).ask
		#print('resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3 = ',((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3))
		#print('(((price_ask-protect_buy_find)/protect_buy_find) * 100) = ',(((price_ask-protect_buy_find)/protect_buy_find) * 100))
		#print('')
		#print('resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3 = ',((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))
		#print('(((protect_buy_find-price_ask)/price_ask) * 100) = ',(((protect_sell_find-price_bid)/price_bid) * 100))
		#print('')

		#*************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


		try:

			# *******************++++++++++++ MACD Buy 1D************************************************************

			macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

			macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]
			macdh_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[1]]
			macds_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[2]]
			MACD_signal_cross_1D_buy = cross_macd(macd_1D_buy,macds_1D_buy,macdh_1D_buy,sym.name,data_macd_1D_buy['diff_minus'],(data_macd_1D_sell['diff_plus']/100))

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1D Buy Macd Wrong!!')
			logging.warning('1D Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 1D************************************************************

			macd_all_1D_sell = ind.macd(symbol_data_1D[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

			macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]
			macdh_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[1]]
			macds_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[2]]
			MACD_signal_cross_1D_sell = cross_macd(macd_1D_sell,macds_1D_sell,macdh_1D_sell,sym.name,(data_macd_1D_buy['diff_minus']/100),data_macd_1D_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1D Sell Macd Wrong!!')
			logging.warning('1D Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		try:

			# *******************++++++++++++ MACD Buy 1D************************************************************

			macd_all_4H_buy = ind.macd(symbol_data_4H[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

			macd_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[0]]
			macdh_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[1]]
			macds_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[2]]
			MACD_signal_cross_4H_buy = cross_macd(macd_4H_buy,macds_4H_buy,macdh_4H_buy,sym.name,data_macd_1D_buy['diff_minus'],(data_macd_1D_sell['diff_plus']/100))

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1D Buy Macd Wrong!!')
			logging.warning('4H Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 1D************************************************************

			macd_all_4H_sell = ind.macd(symbol_data_4H[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

			macd_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[0]]
			macdh_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[1]]
			macds_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[2]]
			MACD_signal_cross_4H_sell = cross_macd(macd_4H_sell,macds_4H_sell,macdh_4H_sell,sym.name,(data_macd_1D_buy['diff_minus']/100),data_macd_1D_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1D Sell Macd Wrong!!')
			logging.warning('4H Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		try:

			# *******************++++++++++++ MACD Buy 1H************************************************************

			macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)

			macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]
			macdh_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[1]]
			macds_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[2]]
			MACD_signal_cross_1H_buy = cross_macd(macd_1H_buy,macds_1H_buy,macdh_1H_buy,sym.name,data_macd_1H_buy['diff_minus'],data_macd_1H_sell['diff_plus']/100)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1H Buy Macd Wrong!!')
			logging.warning('1H Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 1H************************************************************

			macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

			macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]
			macdh_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[1]]
			macds_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[2]]
			MACD_signal_cross_1H_sell = cross_macd(macd_1H_sell,macds_1H_sell,macdh_1H_sell,sym.name,data_macd_1H_buy['diff_minus']/100,data_macd_1H_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1H Sell Macd Wrong!!')
			logging.warning('1H Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



		try:

			# *******************++++++++++++ MACD Buy 15M************************************************************

			macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)

			macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]
			macdh_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[1]]
			macds_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[2]]
			MACD_signal_cross_15M_buy = cross_macd(macd_15M_buy,macds_15M_buy,macdh_15M_buy,sym.name,data_macd_15M_buy['diff_minus'],data_macd_15M_sell['diff_plus']/100)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('15M Buy Macd Wrong!!')
			logging.warning('15M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 15M************************************************************

			macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)

			macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]
			macdh_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[1]]
			macds_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[2]]
			MACD_signal_cross_15M_sell = cross_macd(macd_15M_sell,macds_15M_sell,macdh_15M_sell,sym.name,data_macd_15M_buy['diff_minus']/100,data_macd_15M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('15M Sell Macd Wrong!!')
			logging.warning('15M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#///////////////////////////////////////////////***********************-----------+++++++///////////////////////////////////////////

		try:

			# *******************++++++++++++ MACD Buy 30M************************************************************

			macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

			macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]
			macdh_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[1]]
			macds_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[2]]
			MACD_signal_cross_30M_buy = cross_macd(macd_30M_buy,macds_30M_buy,macdh_30M_buy,sym.name,data_macd_30M_buy['diff_minus'],data_macd_30M_sell['diff_plus']/100)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('30M Buy Macd Wrong!!')
			logging.warning('30M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 5M************************************************************

			macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

			macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]
			macdh_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[1]]
			macds_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[2]]
			MACD_signal_cross_30M_sell = cross_macd(macd_30M_sell,macds_30M_sell,macdh_30M_sell,sym.name,data_macd_30M_buy['diff_minus']/100,data_macd_30M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('30M Sell Macd Wrong!!')
			logging.warning('30M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



		try:

			# *******************++++++++++++ MACD Buy 5M************************************************************

			macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

			macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
			macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
			macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
			MACD_signal_cross_5M_buy = cross_macd(macd_5M_buy,macds_5M_buy,macdh_5M_buy,sym.name,data_macd_5M_buy['diff_minus'],data_macd_5M_sell['diff_plus']/100)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('5M Buy Macd Wrong!!')
			logging.warning('5M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 5M************************************************************

			macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

			macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
			macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
			macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
			MACD_signal_cross_5M_sell = cross_macd(macd_5M_sell,macds_5M_sell,macdh_5M_sell,sym.name,data_macd_5M_buy['diff_minus']/100,data_macd_5M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('5M Sell Macd Wrong!!')
			logging.warning('5M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



		try:

			# *******************++++++++++++ MACD Buy 1M************************************************************

			macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)

			macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]
			macdh_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[1]]
			macds_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[2]]
			MACD_signal_cross_1M_buy = cross_macd(macd_1M_buy,macds_1M_buy,macdh_1M_buy,sym.name,data_macd_1M_buy['diff_minus'],data_macd_1M_sell['diff_plus']/100)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1M Buy Macd Wrong!!')
			logging.warning('1M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 1M************************************************************

			macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)

			macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]
			macdh_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[1]]
			macds_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[2]]
			MACD_signal_cross_1M_sell = cross_macd(macd_1M_sell,macds_1M_sell,macdh_1M_sell,sym.name,data_macd_1M_buy['diff_minus']/100,data_macd_1M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1M Sell Macd Wrong!!')
			logging.warning('1M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#///////////////////////////////////////////////***********************-----------+++++++///////////////////////////////////////////


		#***************************************** ichimokou ******************************************************************************

		try:
			# *******************++++++++++++ TSKS 30M************************************************************
			ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
			SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
			tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]]
			kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]]
			chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

			TsKs_signal_cross_30M = {}
			TsKs_signal_cross_30M = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('30M Buy TsKs Wrong!!')
			logging.warning('30M Buy TsKs Wrong!!')


		try:
			# *******************++++++++++++ TSKS 1D************************************************************
			ichi_1D = ind.ichimoku(high=symbol_data_1D[sym.name]['high'],low=symbol_data_1D[sym.name]['low'],close=symbol_data_1D[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_1D = ichi_1D[0][ichi_1D[0].columns[0]]
			SPANB_1D = ichi_1D[0][ichi_1D[0].columns[1]]
			tenkan_1D = ichi_1D[0][ichi_1D[0].columns[2]]
			kijun_1D = ichi_1D[0][ichi_1D[0].columns[3]]
			chikospan_1D = ichi_1D[0][ichi_1D[0].columns[4]]

			TsKs_signal_cross_1D = {}
			TsKs_signal_cross_1D = cross_TsKs_Buy_signal(tenkan_1D,kijun_1D,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1D Buy TsKs Wrong!!')
			logging.warning('1D Buy TsKs Wrong!!')


		try:
			# *******************++++++++++++ TSKS 1H************************************************************
			ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
			SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
			tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]]
			kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]]
			chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

			TsKs_signal_cross_1H = {}
			TsKs_signal_cross_1H = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1H Buy TsKs Wrong!!')
			logging.warning('1H Buy TsKs Wrong!!')


		try:
			# *******************++++++++++++ TSKS 4H************************************************************
			ichi_4H = ind.ichimoku(high=symbol_data_4H[sym.name]['high'],low=symbol_data_4H[sym.name]['low'],close=symbol_data_4H[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_4H = ichi_4H[0][ichi_4H[0].columns[0]]
			SPANB_4H = ichi_4H[0][ichi_4H[0].columns[1]]
			tenkan_4H = ichi_4H[0][ichi_4H[0].columns[2]]
			kijun_4H = ichi_4H[0][ichi_4H[0].columns[3]]
			chikospan_4H = ichi_4H[0][ichi_4H[0].columns[4]]


			TsKs_signal_cross_4H = {}
			TsKs_signal_cross_4H = cross_TsKs_Buy_signal(tenkan_4H,kijun_4H,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('4H Buy TsKs Wrong!!')
			logging.warning('4H Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS 15M************************************************************

			ichi_15M = ind.ichimoku(high=symbol_data_15M[sym.name]['high'],low=symbol_data_15M[sym.name]['low'],close=symbol_data_15M[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_15M = ichi_15M[0][ichi_15M[0].columns[0]]
			SPANB_15M = ichi_15M[0][ichi_15M[0].columns[1]]
			tenkan_15M = ichi_15M[0][ichi_15M[0].columns[2]]
			kijun_15M = ichi_15M[0][ichi_15M[0].columns[3]]
			chikospan_15M = ichi_15M[0][ichi_15M[0].columns[4]]

			

			TsKs_signal_cross_15M = {}

			TsKs_signal_cross_15M = cross_TsKs_Buy_signal(tenkan_15M,kijun_15M,sym.name)
		except:
			#print('15M Buy TsKs Wrong!!')
			logging.warning('15M Buy TsKs Wrong!!')


		try:
			# *******************++++++++++++ TSKS 5M************************************************************
			ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			TsKs_signal_cross_5M = {}
			TsKs_signal_cross_5M = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('5M Buy TsKs Wrong!!')
			logging.warning('5M Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS 1M************************************************************

			ichi_1M = ind.ichimoku(high=symbol_data_1M[sym.name]['high'],low=symbol_data_1M[sym.name]['low'],close=symbol_data_1M[sym.name]['close'],
                    tenkan=9,kijun=26,snkou=52)
			SPANA_1M = ichi_1M[0][ichi_1M[0].columns[0]]
			SPANB_1M = ichi_1M[0][ichi_1M[0].columns[1]]
			tenkan_1M = ichi_1M[0][ichi_1M[0].columns[2]]
			kijun_1M = ichi_1M[0][ichi_1M[0].columns[3]]
			chikospan_1M = ichi_1M[0][ichi_1M[0].columns[4]]

			TsKs_signal_cross_1M = {}

			TsKs_signal_cross_1M = cross_TsKs_Buy_signal(tenkan_1M,kijun_1M,sym.name)

			#print('tenkan = ',tenkan_5M)

			#print('tsks signal = ',TsKs_signal_cross_5M)


			#print(sym.name)
			#print('spana = ',SPANA_5M)


			#*********************---------------------*************/////////////*************************************************

		except:
			#print('1M Buy TsKs Wrong!!')
			logging.warning('1M Buy TsKs Wrong!!')


		


		signal = 0
		flag_cross_1M_buy = ''
		flag_cross_5M_buy = ''
		flag_cross_15M_buy = ''
		flag_cross_5M15M_buy = ''
		flag_cross_15M30M_buy = ''
		flag_cross_5M1H_buy = ''

		flag_cross_1M_sell = ''
		flag_cross_5M_sell = ''
		flag_cross_15M_sell = ''
		flag_cross_5M15M_sell = ''
		flag_cross_15M30M_sell = ''
		flag_cross_5M1H_sell = ''

		flag_hightouch_1D = ''
		flag_lowtouch_1D = ''
		flag_hightouch_4H = ''
		flag_lowtouch_4H = ''

		flag_hightouch_1H = ''
		flag_lowtouch_1H = ''

		flag_hightouch_1M = ''
		flag_lowtouch_1M = ''
		flag_hightouch_5M = ''
		flag_lowtouch_5M = ''
		flag_hightouch_15M = ''
		flag_lowtouch_15M = ''


		#print('')
		#print('')
		#print('***** Top Low Touceh Cheking *****')
		#print('')


		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('****** Signal Checking ********')
		logging.debug('')

		#print('get signal!!!')

		coef_1M = 0.1
		coef_5M = 0.1
		coef_15M = 0.1

		if (sym.name == 'XAUUSD_i'):
			coef_1M = 0.01
			coef_5M = 0.1
			coef_15M = 0.1



		#****************--------------------++++++++++++++++++++++++***** 1M SELL ***********************************************************++++++++++++++++++++++

		try:
			if (((abs(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]-protect_sell_find_15M)/symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_15M-resist_sell_find_15M)/resist_sell_find_15M) * 100)*coef_15M)):
				
				if (protect_sell_find_15M < resist_sell_find_15M): continue
				
				if ((macds_15M_sell[len(symbol_data_15M[sym.name]['low'])-1] <= macd_15M_sell[len(symbol_data_15M[sym.name]['low'])-1])):
					
					if (chikospan_15M[(len(symbol_data_15M[sym.name]['low'])-1-26)] > symbol_data_15M[sym.name]['high'][(len(symbol_data_15M[sym.name]['low'])-1)]):
						
						if (macds_30M_sell[len(symbol_data_30M[sym.name]['low'])-1] <= macd_30M_sell[len(symbol_data_30M[sym.name]['low'])-1]):
							
							if (chikospan_30M[len(symbol_data_30M[sym.name]['low'])-1-26] > symbol_data_30M[sym.name]['high'][len(symbol_data_30M[sym.name]['low'])-1]):
								
								if (tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1] >= kijun_15M[len(symbol_data_15M[sym.name]['low'])-1]):
									
									if (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1]):
										
										if ((symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANA_15M[len(symbol_data_15M[sym.name]['low'])-1]) & (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANB_15M[len(symbol_data_15M[sym.name]['low'])-1])):
											
											flag_cross_15M30M_sell = 'sell'

											if (flag_same_sell_15M30M == 'same_sell'):
												flag_cross_15M30M_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_15M_sell['tp'] = max(resist_sell_find_15M,(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]*0.998))

												data_macd_15M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_15M[sym.name]['high'][len(symbol_data_15M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_15M_sell['tp'] = resist_sell_find_15M * 1.0004

												data_macd_15M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 15M30M: ',sym.name)
											logging.debug('sell finished 15M30M: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_15M30M_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_15M30M_sell = 'failed_sell'
		except:
			logging.warning('signal problem 15M30M SELL MACD!!!')

		

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************************************** 5M1H SELL *****************************************************************************

		try:
			if (((abs(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]-protect_sell_find_5M)/symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_5M-resist_sell_find_5M)/resist_sell_find_5M) * 100)*coef_5M)):
				
				if (protect_sell_find_5M < resist_sell_find_5M): continue
				
				if ((macds_5M_sell[len(symbol_data_5M[sym.name]['low'])-1] <= macd_5M_sell[len(symbol_data_5M[sym.name]['low'])-1])):
					
					if (chikospan_5M[(len(symbol_data_5M[sym.name]['low'])-1-26)] > symbol_data_5M[sym.name]['high'][(len(symbol_data_5M[sym.name]['low'])-1)]):
						
						if (macds_1H_sell[len(symbol_data_1H[sym.name]['low'])-1] <= macd_1H_sell[len(symbol_data_1H[sym.name]['low'])-1]):
							
							if (chikospan_1H[len(symbol_data_1H[sym.name]['low'])-1-26] > symbol_data_1H[sym.name]['high'][len(symbol_data_1H[sym.name]['low'])-1]):
								
								if (tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1] >= kijun_5M[len(symbol_data_5M[sym.name]['low'])-1]):
									
									if (symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1]):
										
										if ((symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= SPANA_5M[len(symbol_data_5M[sym.name]['low'])-1]) & (symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= SPANB_5M[len(symbol_data_5M[sym.name]['low'])-1])):
											
											flag_cross_5M1H_sell = 'sell'

											if (flag_same_sell_5M1H == 'same_sell'):
												flag_cross_5M1H_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_5M_sell['tp'] = max(resist_sell_find_5M,(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]*0.998))

												data_macd_5M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_5M[sym.name]['high'][len(symbol_data_5M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_5M_sell['tp'] = resist_sell_find_5M * 1.0004

												data_macd_5M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 5M1H: ',sym.name)
											logging.debug('sell finished 5M1H: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_5M1H_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_5M1H_sell = 'failed_sell'
		except:
			logging.warning('signal problem 5M1H SELL MACD!!!')


		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************************************** 5M30M SELL *****************************************************************************

		try:
			if (((abs(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]-protect_sell_find_5M)/symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_5M-resist_sell_find_5M)/resist_sell_find_5M) * 100)*coef_5M)):
				
				if (protect_sell_find_5M < resist_sell_find_5M): continue
				
				if ((macds_5M_sell[len(symbol_data_5M[sym.name]['low'])-1] <= macd_5M_sell[len(symbol_data_5M[sym.name]['low'])-1])):
					
					if (chikospan_5M[(len(symbol_data_5M[sym.name]['low'])-1-26)] > symbol_data_5M[sym.name]['high'][(len(symbol_data_5M[sym.name]['low'])-1)]):
						
						if (macds_30M_sell[len(symbol_data_30M[sym.name]['low'])-1] <= macd_30M_sell[len(symbol_data_30M[sym.name]['low'])-1]):
							
							if (chikospan_30M[len(symbol_data_30M[sym.name]['low'])-1-26] > symbol_data_30M[sym.name]['high'][len(symbol_data_30M[sym.name]['low'])-1]):
								
								if (tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1] >= kijun_5M[len(symbol_data_5M[sym.name]['low'])-1]):
									
									if (symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1]):
										
										if ((symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= SPANA_5M[len(symbol_data_5M[sym.name]['low'])-1]) & (symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= SPANB_5M[len(symbol_data_5M[sym.name]['low'])-1])):
											
											flag_cross_5M_sell = 'sell'

											if (flag_same_sell_5M == 'same_sell'):
												flag_cross_5M_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_5M_sell['tp'] = max(resist_sell_find_5M,(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]*0.998))

												data_macd_5M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_5M[sym.name]['high'][len(symbol_data_5M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_5M_sell['tp'] = resist_sell_find_5M * 1.0004

												data_macd_5M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 5M30M: ',sym.name)
											logging.debug('sell finished 5M30M: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_5M_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_5M_sell = 'failed_sell'
		except:
			logging.warning('signal problem 5M30M SELL MACD!!!')


		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************************************** 5M15M SELL *****************************************************************************

		#try:
		if True:
			if (((abs(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]-protect_sell_find_5M)/symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_5M-resist_sell_find_5M)/resist_sell_find_5M) * 100)*coef_5M)):
				
				if (protect_sell_find_5M < resist_sell_find_5M): continue
				
				if ((macds_5M_sell[len(symbol_data_5M[sym.name]['low'])-1] <= macd_5M_sell[len(symbol_data_5M[sym.name]['low'])-1])):
					
					if (chikospan_5M[(len(symbol_data_5M[sym.name]['low'])-1-26)] > symbol_data_5M[sym.name]['high'][(len(symbol_data_5M[sym.name]['low'])-1)]):
						
						if (macds_15M_sell[len(symbol_data_15M[sym.name]['low'])-1] <= macd_15M_sell[len(symbol_data_15M[sym.name]['low'])-1]):
							
							if (chikospan_15M[len(symbol_data_15M[sym.name]['low'])-1-26] > symbol_data_15M[sym.name]['high'][len(symbol_data_15M[sym.name]['low'])-1]):
								
								if (tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1] >= kijun_5M[len(symbol_data_5M[sym.name]['low'])-1]):
									
									if (symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= tenkan_5M[len(symbol_data_5M[sym.name]['low'])-1]):
										
										if ((symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1] >= SPANA_5M[len(symbol_data_5M[sym.name]['low'])-1]) & (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANB_15M[len(symbol_data_15M[sym.name]['low'])-1])):
											
											flag_cross_5M15M_sell = 'sell'

											if (flag_same_sell_5M15M == 'same_sell'):
												flag_cross_5M15M_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_5M_sell['tp'] = max(resist_sell_find_5M,(symbol_data_5M[sym.name]['low'][len(symbol_data_5M[sym.name]['low'])-1]*0.998))

												data_macd_5M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_5M[sym.name]['high'][len(symbol_data_5M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_5M_sell['tp'] = resist_sell_find_5M * 1.0004

												data_macd_5M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 5M15M: ',sym.name)
											logging.debug('sell finished 5M15M: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_5M15M_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_5M15M_sell = 'failed_sell'
		#except:
		else:
			logging.warning('signal problem 5M15M SELL MACD!!!')


		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************************************** 15M1H SELL *****************************************************************************

		try:
			if (((abs(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]-protect_sell_find_15M)/symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_15M-resist_sell_find_15M)/resist_sell_find_15M) * 100)*coef_15M)):
				
				if (protect_sell_find_15M < resist_sell_find_15M): continue
				
				if ((macds_15M_sell[len(symbol_data_15M[sym.name]['low'])-1] <= macd_15M_sell[len(symbol_data_15M[sym.name]['low'])-1])):
					
					if (chikospan_15M[(len(symbol_data_15M[sym.name]['low'])-1-26)] > symbol_data_15M[sym.name]['high'][(len(symbol_data_15M[sym.name]['low'])-1)]):
						
						if (macds_1H_sell[len(symbol_data_1H[sym.name]['low'])-1] <= macd_1H_sell[len(symbol_data_1H[sym.name]['low'])-1]):
							
							if (chikospan_1H[len(symbol_data_1H[sym.name]['low'])-1-26] > symbol_data_1H[sym.name]['high'][len(symbol_data_1H[sym.name]['low'])-1]):
								
								if (tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1] >= kijun_15M[len(symbol_data_15M[sym.name]['low'])-1]):
									
									if (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1]):
										
										if ((symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANA_15M[len(symbol_data_15M[sym.name]['low'])-1]) & (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANB_15M[len(symbol_data_15M[sym.name]['low'])-1])):
											
											flag_cross_15M_sell = 'sell'

											if (flag_same_sell_15M == 'same_sell'):
												flag_cross_15M_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_15M_sell['tp'] = max(resist_sell_find_15M,(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]*0.998))

												data_macd_15M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_15M[sym.name]['high'][len(symbol_data_15M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_15M_sell['tp'] = resist_sell_find_15M * 1.0004

												data_macd_15M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 15M1H: ',sym.name)
											logging.debug('sell finished 15M1H: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_15M_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_15M_sell = 'failed_sell'
		except:
			logging.warning('signal problem 15M1H SELL MACD!!!')


		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#**************************************************************** 5M30M SELL *****************************************************************************
		try:
			if (((abs(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]-protect_sell_find_15M)/symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]) * 100) < ((((protect_sell_find_15M-resist_sell_find_15M)/resist_sell_find_15M) * 100)*coef_15M)):
				
				if (protect_sell_find_15M < resist_sell_find_15M): continue
				
				if ((macds_15M_sell[len(symbol_data_15M[sym.name]['low'])-1] <= macd_15M_sell[len(symbol_data_15M[sym.name]['low'])-1])):
					
					if (chikospan_15M[(len(symbol_data_15M[sym.name]['low'])-1-26)] > symbol_data_15M[sym.name]['high'][(len(symbol_data_15M[sym.name]['low'])-1)]):
						
						if (macds_30M_sell[len(symbol_data_30M[sym.name]['low'])-1] <= macd_30M_sell[len(symbol_data_30M[sym.name]['low'])-1]):
							
							if (chikospan_30M[len(symbol_data_30M[sym.name]['low'])-1-26] > symbol_data_30M[sym.name]['high'][len(symbol_data_30M[sym.name]['low'])-1]):
								
								if (tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1] >= kijun_15M[len(symbol_data_15M[sym.name]['low'])-1]):
									
									if (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= tenkan_15M[len(symbol_data_15M[sym.name]['low'])-1]):
										
										if ((symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANA_15M[len(symbol_data_15M[sym.name]['low'])-1]) & (symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1] >= SPANB_15M[len(symbol_data_15M[sym.name]['low'])-1])):
											
											flag_cross_15M30M_sell = 'sell'

											if (flag_same_sell_15M30M == 'same_sell'):
												flag_cross_15M30M_sell = 'same_sell'

											if (sym.name == 'XAUUSD_i'):
												data_macd_15M_sell['tp'] = max(resist_sell_find_15M,(symbol_data_15M[sym.name]['low'][len(symbol_data_15M[sym.name]['low'])-1]*0.998))

												data_macd_15M_sell['st'] = min(protect_sell_find_4H * 1.001, (symbol_data_15M[sym.name]['high'][len(symbol_data_15M[sym.name]['low'])-1]*1.004))
											else:
												data_macd_15M_sell['tp'] = resist_sell_find_15M * 1.0004

												data_macd_15M_sell['st'] = protect_sell_find_4H * 1.001


											print('sell finished 15M30M: ',sym.name)
											logging.debug('sell finished 15M30M: %s'%sym.name)

											#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 994)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(MACD_signal_cross_15M_buy['index']/2)+500))):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

											#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= 294)):
											#	flag_cross_15M30M_sell = 'failed_sell'

																	

											if (macds_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)] >= macd_1D_buy[(len(symbol_data_1D[sym.name]['low']) - 1)]):
												flag_cross_15M30M_sell = 'failed_sell'

											if (macds_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)] > macd_4H_buy[(len(symbol_data_4H[sym.name]['low']) - 1)]):
												flag_cross_15M30M_sell = 'failed_sell'
		except:
			logging.warning('signal problem 15M30M SELL MACD!!!')


		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#******************************* Top Low Touch Check ********************************************************************************

		#************************************************ 1M Top Low Touched ************************************************************

		if (flag_cross_1M_buy == 'buy'):

			try:
				touch_counter = len(symbol_data_1M[sym.name]['high']) - 1

				while touch_counter > (len(symbol_data_1M[sym.name]['high']) - 1 - 300):
					if ((symbol_data_1M[sym.name]['high'][touch_counter] >= (resist_buy_find_1M * 0.9998))):
						flag_hightouch_1M = 'high_toched'

					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')

		logging.debug('')

		if (flag_cross_1M_sell == 'sell'):

			try:
				touch_counter = len(symbol_data_1M[sym.name]['low']) - 1

				while touch_counter > (len(symbol_data_1M[sym.name]['low']) - 1 - 300):
					if ((symbol_data_1M[sym.name]['low'][touch_counter] <= (resist_sell_find_1M * 1.0002))):
						flag_lowtouch_1M = 'low_toched'

					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')

		#************************************************ 5M Top Low Touched ************************************************************

		if ((flag_cross_5M_buy == 'buy') | (flag_cross_5M15M_buy == 'buy') | (flag_cross_5M1H_buy == 'buy')):
			try:
				touch_counter = len(symbol_data_5M[sym.name]['high'])- 1

				while touch_counter > (len(symbol_data_5M[sym.name]['high']) - 1 - 60):
					if ((symbol_data_5M[sym.name]['high'][touch_counter] >= (resist_buy_find_5M * 0.9998))):
						flag_hightouch_5M = 'high_toched'
						flag_hightouch_5M = 'high_toched'
						flag_hightouch_5M = 'high_toched'
	
					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')


		if ((flag_cross_5M_sell == 'sell') | (flag_cross_5M15M_sell == 'sell') | (flag_cross_5M1H_sell == 'sell')):
			try:
				touch_counter = len(symbol_data_5M[sym.name]['low']) - 1
	
				while touch_counter > (len(symbol_data_5M[sym.name]['low']) - 1 - 20):
					if ((symbol_data_5M[sym.name]['low'][touch_counter] <= (resist_sell_find_5M * 1.0002))):
						flag_lowtouch_5M = 'low_toched'
						flag_lowtouch_5M = 'low_toched'
						flag_lowtouch_5M = 'low_toched'
	
					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')

		#************************************************ 15M Top Low Touched ************************************************************

		if ((flag_cross_15M_buy == 'buy') | (flag_cross_15M30M_buy == 'buy')):
			try:
				touch_counter = len(symbol_data_15M[sym.name]['high']) - 1
	
				while touch_counter > (len(symbol_data_15M[sym.name]['high']) - 1 - 40):
					if ((symbol_data_15M[sym.name]['high'][touch_counter] >= (resist_buy_find_15M * 0.9998))):
						flag_hightouch_15M = 'high_toched'
						flag_hightouch_15M = 'high_toched'
						#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
	
					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')


		if ((flag_cross_15M_sell == 'sell') | (flag_cross_15M30M_sell == 'sell')):
			try:
				touch_counter = len(symbol_data_15M[sym.name]['low']) - 1
	
				while touch_counter > (len(symbol_data_15M[sym.name]['low']) - 1 - 40):
					if ((symbol_data_15M[sym.name]['low'][touch_counter] <= (resist_sell_find_15M * 1.0002))):
						flag_lowtouch_15M = 'low_toched'
						flag_lowtouch_15M = 'low_toched'
	
					touch_counter -= 1

			except:
				#print('No Data')
				logging.warning('No Data')



		logging.debug('')

		#************************************************ 1H Top Low Touched ************************************************************

		try:
			touch_counter = len(symbol_data_1H[sym.name]['high']) - 1

			while touch_counter > (len(symbol_data_1H[sym.name]['high']) - 1 - 10):
				if ((symbol_data_1H[sym.name]['high'][touch_counter] >= (resist_buy_find_1H * 0.9998))):
					flag_hightouch_1H = 'high_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 1H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 1H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if ((symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 3)] <= (protect_buy_find_1H))
					| (symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 2)] <= (protect_buy_find_1H))
					| (symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 1)] <= (protect_buy_find_1H))):
					flag_hightouch_1H = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if (#(symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['high']) - 3)] >= (resist_buy_find_4H * 0.9996))
					#| (symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['high']) - 2)] >= (resist_buy_find_4H * 0.9996))
					(symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['high']) - 1)] >= (resist_buy_find_1H * 0.9998))):
					flag_hightouch_1H = 'high_toched'
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')



		try:
			touch_counter = len(symbol_data_1H[sym.name]['low']) - 1

			while touch_counter > (len(symbol_data_1H[sym.name]['low']) - 1 - 10):
				if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
					flag_lowtouch_1H = 'low_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if ((symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['low']) - 3)] >= (protect_sell_find_1H)) 
					| (symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['low']) - 2)] >= (protect_sell_find_1H))
					| (symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['low']) - 1)] >= (protect_sell_find_1H))):
					flag_lowtouch_1H = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
					#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
					(symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 1)] <= (resist_sell_find_1H * 1.0002))):
					flag_lowtouch_1H = 'low_toched'
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')


		logging.debug('')

		#************************************************ 4H Top Low Touched ************************************************************

		try:
			touch_counter = len(symbol_data_4H[sym.name]['high']) - 1

			while touch_counter > (len(symbol_data_4H[sym.name]['high']) - 1 - 6):
				if ((symbol_data_4H[sym.name]['high'][touch_counter] >= (resist_buy_find_4H * 0.9998))):
					flag_hightouch_4H = 'high_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if ((symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (protect_buy_find_4H))
					| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (protect_buy_find_4H))
					| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 1)] <= (protect_buy_find_4H))):
					flag_hightouch_4H = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if (#(symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['high']) - 3)] >= (resist_buy_find_4H * 0.9996))
					#| (symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['high']) - 2)] >= (resist_buy_find_4H * 0.9996))
					(symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['high']) - 1)] >= (resist_buy_find_4H * 0.9998))):
					flag_hightouch_4H = 'high_toched'
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')



		try:
			touch_counter = len(symbol_data_4H[sym.name]['low']) - 1

			while touch_counter > (len(symbol_data_4H[sym.name]['low']) - 1 - 6):
				if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
					flag_lowtouch_4H = 'low_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if ((symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['low']) - 3)] >= (protect_sell_find_4H)) 
					| (symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['low']) - 2)] >= (protect_sell_find_4H))
					| (symbol_data_4H[sym.name]['high'][(len(symbol_data_4H[sym.name]['low']) - 1)] >= (protect_sell_find_4H))):
					flag_lowtouch_4H = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
					#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
					(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 1)] <= (resist_sell_find_4H * 1.0002))):
					flag_lowtouch_4H = 'low_toched'
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')


		logging.debug('')
		#************************************************ 1D Top Low Touched ************************************************************

		try:
			touch_counter = len(symbol_data_1D[sym.name]['high']) - 1

			while touch_counter > (len(symbol_data_1D[sym.name]['high']) - 1 - 3):
				if ((symbol_data_1D[sym.name]['high'][touch_counter] >= (resist_buy_find_1D * 0.9998))):
					flag_hightouch_1D = 'high_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


				if ((symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (protect_buy_find_1D))
					| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (protect_buy_find_1D)) 
					| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 1)] <= (protect_buy_find_1D))):
					flag_hightouch_1D = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				if (#(symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['high']) - 3)] >= (resist_buy_find_1D * 0.9984))
					#| (symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['high']) - 2)] >= (resist_buy_find_1D * 0.9984)) 
					(symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['high']) - 1)] >= (resist_buy_find_1D * 0.9998))):
					flag_hightouch_1D = 'high_toched'
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')

		#print('')
		#print('')
		logging.debug('')



		try:
			touch_counter = len(symbol_data_1D[sym.name]['low']) - 1

			while touch_counter > (len(symbol_data_1D[sym.name]['low']) - 1 - 3):
				if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
					flag_lowtouch_1D = 'low_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


				if ((symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['low']) - 3)] >= (protect_sell_find_1D))
				 | (symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['low']) - 2)] >= (protect_sell_find_1D))
				 | (symbol_data_1D[sym.name]['high'][(len(symbol_data_1D[sym.name]['low']) - 1)] >= (protect_sell_find_1D))):
					flag_lowtouch_1D = ''
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


				if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
				 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
				 (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 1)] <= (resist_sell_find_1D * 1.0002))):
					flag_lowtouch_1D = 'low_toched'
					#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
					#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

				touch_counter -= 1

		except:
			#print('No Data')
			logging.warning('No Data')


		if ((flag_hightouch_1M == 'high_toched') | (flag_hightouch_1H == 'high_toched') | (flag_hightouch_4H == 'high_toched')):
			flag_cross_1M_buy = 'failed_buy'

		if ((flag_hightouch_5M == 'high_toched') | (flag_hightouch_1H == 'high_toched') | (flag_hightouch_4H == 'high_toched')):
			flag_cross_5M_buy = 'failed_buy'
			flag_cross_5M15M_buy = 'failed_buy'
			flag_cross_5M1H_buy = 'failed_buy'

		if ((flag_hightouch_15M == 'high_toched') | (flag_hightouch_1H == 'high_toched') | (flag_hightouch_4H == 'high_toched')):
			flag_cross_15M_buy = 'failed_buy'
			flag_cross_15M30M_buy = 'failed_buy'

		if ((flag_lowtouch_1M == 'low_toched') | (flag_lowtouch_1H == 'low_toched') | (flag_lowtouch_4H == 'low_toched')):
			flag_cross_1M_sell = 'failed_sell'

		if ((flag_lowtouch_5M == 'low_toched') | (flag_lowtouch_1H == 'low_toched') | (flag_lowtouch_4H == 'low_toched')):
			flag_cross_5M_sell = 'failed_sell'
			flag_cross_5M15M_sell = 'failed_sell'
			flag_cross_5M1H_sell = 'failed_sell'

		if ((flag_lowtouch_15M == 'low_toched') | (flag_lowtouch_1H == 'low_toched') | (flag_lowtouch_4H == 'low_toched')):
			flag_cross_15M_sell = 'failed_sell'
			flag_cross_15M30M_sell = 'failed_sell'



		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#flag_cross_1M = 'buy'
		#flag_cross_5M = 'buy'
		#flag_cross_15M = 'buy'
		#flag_cross_5M15M = 'buy'
		#flag_cross_15M30M = 'buy'
		#flag_cross_5M1H = 'buy'
		#print('////////////////////////////////////////////')
		#print('')
		#print('')
		#print('******* Signals ***********')

		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('')
		logging.debug('******* Signals ***********')


		#print('flag_cross_1M = ',flag_cross_1M)
		#print('flag_cross_5M = ',flag_cross_5M)
		#print('flag_cross_15M = ',flag_cross_15M)
		#print('flag_cross_5M15M = ',flag_cross_5M15M)
		#print('flag_cross_15M30M = ',flag_cross_15M30M)
		#print('flag_cross_5M1H = ',flag_cross_5M1H)

		logging.debug('flag_cross_1M_buy = %s'%flag_cross_1M_buy)
		logging.debug('flag_cross_1M_sell = %s'%flag_cross_1M_sell)
		logging.debug('flag_cross_5M_buy = %s'%flag_cross_5M_buy)
		logging.debug('flag_cross_5M_sell = %s'%flag_cross_5M_sell)
		logging.debug('flag_cross_15M_buy = %s'%flag_cross_15M_buy)
		logging.debug('flag_cross_15M_sell = %s'%flag_cross_15M_sell)
		logging.debug('flag_cross_5M15M_buy = %s'%flag_cross_5M15M_buy)
		logging.debug('flag_cross_5M15M_sell = %s'%flag_cross_5M15M_sell)
		logging.debug('flag_cross_15M30M_buy = %s'%flag_cross_15M30M_buy)
		logging.debug('flag_cross_15M30M_sell = %s'%flag_cross_15M30M_sell)
		logging.debug('flag_cross_5M1H_buy = %s'%flag_cross_5M1H_buy)
		logging.debug('flag_cross_5M1H_sell = %s'%flag_cross_5M1H_sell)


		#print('')
		#print('////////////////////////////////////////////')
		#print('')
		#print('****** SELL OR BUY Doing ***********')
		#print('')

		logging.debug('')
		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('****** SELL OR BUY Doing ***********')
		logging.debug('')


		

		#************************************** 15M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 15M ********************************************************')

			if (flag_cross_15M_buy == 'buy'):


				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '15M1H gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue
									
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 0) & ((comment_position == '1M gen SMI') | (comment_position == '5M gen SMI'))):

									tp_buy = (tp_position + ((((abs(data_macd_15M_buy['tp'])) - spred) * price)/100))
									sp_buy = ((abs(data_macd_15M_buy['st'])) - (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','buy')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_buy,
    										"tp": tp_buy,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 15M 1H Trade MACD')
								logging.warning('request failed 15M 1H Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 15M 1H Trade MACD!!!')
											logging.warning('send Done 15M 1H Trade MACD!!!')
											#continue

							except:
								#print('modify error 15M 1H')
								logging.warning('modify error 15M 1H')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							

						#vol_traded_max = (my_money/100) * 0.06
					#continue

						if (flag_cross_15M_buy == 'buy'):
							comment = '15M1H gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_15M_buy == 'buy'):
								tp_buy = ((abs(data_macd_15M_buy['tp'])) - (((spred) * abs(data_macd_15M_buy['tp']))/100))#(price + ((((abs(data_macd_15M_buy['tp'])) - spred) * price)/100))
								sp_buy = ((abs(data_macd_15M_buy['st'])) - (((spred + 0.05) * abs(data_macd_15M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_15M_buy['score'] * my_money)/1000000))
							

							if (tp_buy <= (price)): 
								print('tp low 15',tp_buy,(price * 1.0002),data_macd_15M_buy['tp'],sym.name)
								break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max):
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							
							
							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 15M Trade MACD')
							logging.warning('request failed 15M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 15M 1H Trade MACD!!!')
										logging.warning('send Done 15M 1H Trade MACD!!!')
						except:
							#print('some thing wrong send 15M 1H Trade MACD')
							logging.warning('some thing wrong send 15M 1H Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_15M_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '15M1H gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 1) & ((comment_position == '1M gen SMI') | (comment_position == '5M gen SMI'))):

									tp_sell = (tp_position - ((((abs(data_macd_15M_sell['tp'])) - spred) * price)/100))
									sp_sell = ((abs(data_macd_15M_sell['st'])) + (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','sell')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_sell,
    										"tp": tp_sell,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 15M 1H Trade MACD')
								logging.warning('request failed 15M 1H Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 15M 1H Trade MACD!!!')
											logging.warning('send Done 15M 1H Trade MACD!!!')
											#continue

							except:
								#print('modify error 15M 1H')
								logging.warning('modify error 15M 1H')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							

						##vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_15M_sell == 'sell'):
							comment = '15M1H gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_15M_sell == 'sell'):
								tp_sell = ((abs(data_macd_15M_sell['tp'])) + (((spred) * abs(data_macd_15M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_15M_sell['st'])) + (((spred + 0.05) * abs(data_macd_15M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_15M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max):
								lot = 0 
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 15M15M 1H Trade MACD')
							logging.warning('request failed 15M15M 1H Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 15M 1H Trade MACD!!!')
										logging.warning('send Done 15M 1H Trade MACD!!!')
						except:
							#print('some thing wrong send 15M 1H Trade MACD')
							logging.warning('some thing wrong send 15M 1H Trade MACD')
							continue
		except:
			#print('cant Play 15M 1H Trade MACD!!!')
			logging.warning('cant Play 15M 1H Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 15M 30M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 15M ********************************************************')

			if (flag_cross_15M30M_buy == 'buy'):

				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((symbol_position == symbol_position) & (type_position == 0) & (comment_position == '15M30M gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 0) & ((comment_position == '1M gen SMI') | (comment_position == '5M gen SMI'))):

									tp_buy = (tp_position + ((((abs(data_macd_15M_buy['tp'])) - spred) * price)/100))
									sp_buy = ((abs(data_macd_15M_buy['st'])) - (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','buy')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_buy,
    										"tp": tp_buy,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 15M 30M Trade MACD')
								logging.warning('request failed 15M 30M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 15M 30M Trade MACD!!!')
											logging.warning('send Done 15M 30M Trade MACD!!!')
											#continue

							except:
								#print('modify error 15M 30M')
								logging.warning('modify error 15M 30M')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							

						#vol_traded_max = (my_money/100) * 0.6
					#continue

						if (flag_cross_15M30M_buy == 'buy'):
							comment = '15M30M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_15M30M_buy == 'buy'):
								tp_buy = ((abs(data_macd_15M_buy['tp'])) - (((spred) * abs(data_macd_15M_buy['tp']))/100))
								sp_buy = ((abs(data_macd_15M_buy['st'])) - (((spred + 0.05) * abs(data_macd_15M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_15M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): 
								print('tp low 15M30M',tp_buy,(price * 1.0002),data_macd_15M_buy['tp'],sym.name)
								break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								continue

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 15M30M Trade MACD')
							logging.warning('request failed 15M30M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 15M30M Trade MACD!!!')
										logging.warning('send Done 15M30M Trade MACD!!!')
						except:
							#print('some thing wrong send 15M30M Trade MACD')
							logging.warning('some thing wrong send 15M30M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_15M30M_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '15M30M gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 1) & ((comment_position == '1M gen SMI') | (comment_position == '5M gen SMI'))):

									tp_sell = (tp_position - ((((abs(data_macd_15M_sell['tp'])) - spred) * price)/100))
									sp_sell = ((abs(data_macd_15M_sell['st'])) + (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','sell')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_sell,
    										"tp": tp_sell,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 15M 30M Trade MACD')
								logging.warning('request failed 15M 30M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 15M 30M Trade MACD!!!')
											logging.warning('send Done 15M 30M Trade MACD!!!')
											#continue

							except:
								#print('modify error 15M 30M')
								logging.warning('modify error 15M 30M')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							

						#vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_15M30M_sell == 'sell'):
							comment = '15M30M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_15M30M_sell == 'sell'):
								tp_sell = ((abs(data_macd_15M_sell['tp'])) + (((spred) * abs(data_macd_15M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_15M_sell['st'])) + (((spred + 0.05) * abs(data_macd_15M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_15M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 15M 30M Trade MACD')
							logging.warning('request failed 15M 30M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 15M 30M Trade MACD!!!')
										logging.warning('send Done 15M 30M Trade MACD!!!')
						except:
							#print('some thing wrong send 15M 30M Trade MACD')
							logging.warning('some thing wrong send 15M 30M Trade MACD')
							continue
		except:
			#print('cant Play 15M 30M Trade MACD!!!')
			logging.warning('cant Play 15M 30M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 5M 1H *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 5M ********************************************************')

			if (flag_cross_5M1H_buy == 'buy'):

				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M1H gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 0) & (comment_position == '1M gen SMI')):

									tp_buy = (tp_position + ((((abs(data_macd_5M_buy['tp'])) - spred) * price)/100))
									sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','buy')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_buy,
    										"tp": tp_buy,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M1H Trade MACD')
								logging.warning('request failed 5M1H Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M1H Trade MACD!!!')
											logging.warning('send Done 5M1H Trade MACD!!!')
											#continue
							except:
								#print('modify error')
								logging.warning('modify error')

							

						#vol_traded_max = (my_money/100) * 0.6
					#continue

						if (flag_cross_5M1H_buy == 'buy'):
							comment = '5M1H gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_5M1H_buy == 'buy'):
								tp_buy = ((abs(data_macd_5M_buy['tp'])) - (((spred) * abs(data_macd_5M_buy['tp']))/100))
								sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.05) * abs(data_macd_5M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M1H Trade MACD')
							logging.warning('request failed 5M1H Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M1H Trade MACD!!!')
										logging.warning('send Done 5M1H Trade MACD!!!')
						except:
							#print('some thing wrong send 5M1H Trade MACD')
							logging.warning('some thing wrong send 5M1H Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_5M1H_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M1H gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 1) & (comment_position == '1M gen SMI')):

									tp_sell = (tp_position - ((((abs(data_macd_5M_sell['tp'])) - spred) * price)/100))
									sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','sell')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_sell,
    										"tp": tp_sell,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M1H Trade MACD')
								logging.warning('request failed 5M1H Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M1H Trade MACD!!!')
											logging.warning('send Done 5M1H Trade MACD!!!')
											#continue

							except:
								#print('modify error 5M 1H')
								logging.warning('modify error 5M 1H')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							if ((type_position == 1) & (comment_position == '5M1H gen SMI')):
								#print('same sell')
								logging.warning('same sell')
								continue

						#vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_5M1H_sell == 'sell'):
							comment = '5M1H gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_5M1H_sell == 'sell'):
								tp_sell = ((abs(data_macd_5M_sell['tp'])) + (((spred) * abs(data_macd_5M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.05) * abs(data_macd_5M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M 1H Trade MACD')
							logging.warning('request failed 5M 1H Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M 1H Trade MACD!!!')
										logging.warning('send Done 5M 1H Trade MACD!!!')
						except:
							#print('some thing wrong send 5M 1H Trade MACD')
							logging.warning('some thing wrong send 5M 1H Trade MACD')
							continue
		except:
			#print('cant Play 5M 1H Trade MACD!!!')
			logging.warning('cant Play 5M 1H Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 5M 30M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 5M ********************************************************')

			if (flag_cross_5M_buy == 'buy'):


				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M30M gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 0) & (comment_position == '1M gen SMI')):

									tp_buy = (tp_position + ((((abs(data_macd_5M_buy['tp'])) - spred) * price)/100))
									sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','buy')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_buy,
    										"tp": tp_buy,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M 30M Trade MACD')
								logging.warning('request failed 5M 30M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M 30M Trade MACD!!!')
											logging.warning('send Done 5M 30M Trade MACD!!!')
											#continue
							except:
								#print('modify error')
								logging.warning('modify error')

							

						#vol_traded_max = (my_money/100) * 0.6
					#continue

						if (flag_cross_5M_buy == 'buy'):
							comment = '5M30M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_5M_buy == 'buy'):
								tp_buy = ((abs(data_macd_5M_buy['tp'])) - (((spred) * abs(data_macd_5M_buy['tp']))/100))
								sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.05) * abs(data_macd_5M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M 30M Trade MACD')
							logging.warning('request failed 5M 30M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M 30M Trade MACD!!!')
										logging.warning('send Done 5M 30M Trade MACD!!!')
						except:
							#print('some thing wrong send 5M 30M Trade MACD')
							logging.warning('some thing wrong send 5M 30M Trade MACD')
							#continue

			account_count = 1000


			if (flag_cross_5M_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M30M gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 1) & (comment_position == '1M gen SMI')):

									tp_sell = (tp_position - ((((abs(data_macd_5M_sell['tp'])) - spred) * price)/100))
									sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','sell')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_sell,
    										"tp": tp_sell,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M 30M Trade MACD')
								logging.warning('request failed 5M 30M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M 30M Trade MACD!!!')
											logging.warning('send Done 5M 30M Trade MACD!!!')
											#continue

							except:
								#print('modify error 5M 30M')
								logging.warning('modify error 5M 30M')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							if ((type_position == 1) & (comment_position == '5M30M gen SMI')):
								print('same sell')
								logging.warning('same sell')
								continue

						#vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_5M_sell == 'sell'):
							comment = '5M30M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_5M_sell == 'sell'):
								tp_sell = ((abs(data_macd_5M_sell['tp'])) + (((spred) * abs(data_macd_5M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.05) * abs(data_macd_5M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M 30M Trade MACD')
							logging.warning('request failed 5M 30M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M 30M Trade MACD!!!')
										logging.warning('send Done 5M 30M Trade MACD!!!')

						except:
							#print('some thing wrong send 5M 30M Trade MACD')
							logging.warning('some thing wrong send 5M 30M Trade MACD')
							continue
		except:
			#print('cant Play 5M 30M Trade MACD!!!')
			logging.warning('cant Play 5M 30M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************

		#************************************** 5M 15M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 5M ********************************************************')

			if (flag_cross_5M15M_buy == 'buy'):

				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M15M gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue

					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 0) & (comment_position == '1M gen SMI')):

									tp_buy = (tp_position + ((((abs(data_macd_5M_buy['tp'])) - spred) * price)/100))
									sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','buy')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_buy,
    										"tp": tp_buy,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M 15M Trade MACD')
								logging.warning('request failed 5M 15M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M 15M Trade MACD!!!')
											logging.warning('send Done 5M 15M Trade MACD!!!')
											#continue
							except:
								#print('modify error')
								logging.warning('modify error')

							

						#vol_traded_max = (my_money/100) * 0.6
					#continue

						if (flag_cross_5M15M_buy == 'buy'):
							comment = '5M15M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_5M15M_buy == 'buy'):
								tp_buy = ((abs(data_macd_5M_buy['tp'])) - (((spred) * abs(data_macd_5M_buy['tp']))/100))
								sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.05) * abs(data_macd_5M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): 
								print('tp low 5',tp_buy,(price * 1.0002),data_macd_5M_buy['tp'])
								break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M15M Trade MACD')
							logging.warning('request failed 5M15M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M15M Trade MACD!!!')
										logging.warning('send Done 5M15M Trade MACD!!!')
						except:
							#print('some thing wrong send 5M15M Trade MACD')
							logging.warning('some thing wrong send 5M15M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_5M15M_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]
								tp_position = position[12]
								sl_position = position[11]
								price_open_position = position[10]
								ticket_position = position[0]
								price_current_position = position[13]
								ID_position = position[18]
								profit_position = position[15]
								magic_position = position[6]

								symbol_position = position[16]

								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M15M gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue
					
							#print("Total positions on ",sym.name,' = ',len(positions))

							try:

								if ((type_position == 1) & (comment_position == '1M gen SMI')):

									tp_sell = (tp_position - ((((abs(data_macd_5M_sell['tp'])) - spred) * price)/100))
									sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.03) * price)/100))

									if True:
										print(sym.name,': ','sell')
										request = {
											"action": mt5.TRADE_ACTION_SLTP,
    										"symbol": sym.name,
    										"position": ID_position,
    										"sl": sp_sell,
    										"tp": tp_sell,
    										"magic": magic_position,
    										"type_time": mt5.ORDER_TIME_GTC,
    										"type_filling": mt5.ORDER_FILLING_FOK
    										}
									else:
										print('//////////////////////////////////////tp<buy*****************************************************')
										request = {}

									result = mt5.order_send(request)
									# check the execution result
									print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
							except:
								#print('request failed 5M15M Trade MACD')
								logging.warning('request failed 5M15M Trade MACD')
							try:
								if result.retcode != mt5.TRADE_RETCODE_DONE:
									print("2. order_send failed, retcode={}".format(result.retcode))
									# request the result as a dictionary and display it element by element
									result_dict=result._asdict()
									for field in result_dict.keys():
										print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
										if field=="request":
											traderequest_dict=result_dict[field]._asdict()
											for tradereq_filed in traderequest_dict:
												print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
										else:
											#print('send Done 5M15M Trade MACD!!!')
											logging.warning('send Done 5M15M Trade MACD!!!')

											#continue

							except:
								#print('modify error 5M15M')
								logging.warning('modify error 5M15M')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							

						#vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_5M15M_sell == 'sell'):
							comment = '5M15M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_5M15M_sell == 'sell'):
								tp_sell = ((abs(data_macd_5M_sell['tp'])) + (((spred) * abs(data_macd_5M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.05) * abs(data_macd_5M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 5M15M Trade MACD')
							logging.warning('request failed 5M15M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 5M15M Trade MACD!!!')
										logging.warning('send Done 5M15M Trade MACD!!!')
						except:
							#print('some thing wrong send 5M15M Trade MACD')
							logging.warning('some thing wrong send 5M15M Trade MACD')
							continue
		except:
			#print('cant Play 5M15M Trade MACD!!!')
			logging.warning('cant Play 5M15M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 1M 5M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()

		try:
			#print('**************************************** MACD Trade Signal 1M ********************************************************')

			if (flag_cross_1M_buy == 'buy'):

				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]

								symbol_position = position[16]
					
								print("Total positions on ",sym.name,' = ',len(positions))
								if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '1M gen SMI')):
									#print('same buy')
									logging.warning('same buy')
									continue

						#vol_traded_max = (my_money/100) * 0.6
					#continue

						if (flag_cross_1M_buy == 'buy'):
							comment = '1M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.045):
								#print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue	

							if (flag_cross_1M_buy == 'buy'):
								tp_buy = ((abs(data_macd_1M_buy['tp'])) - (((spred) * abs(data_macd_1M_buy['tp']))/100))
								sp_buy = ((abs(data_macd_1M_buy['st'])) - (((spred + 0.05) * abs(data_macd_1M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_1M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','buy')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_BUY,
    									"price": price,
    									"sl": sp_buy,
    									"tp": tp_buy,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
   		 								}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
							# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 1M Trade MACD')
							logging.warning('request failed 1M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        							# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 1M Trade MACD!!!')
										logging.warning('some thing wrong send 1M Trade MACD')
						except:
							#print('some thing wrong send 1M Trade MACD')
							logging.warning('some thing wrong send 1M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_1M_sell == 'sell'):
				
					


					
					while account_count <= 1000:

						my_money = log_multi_account(1000)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
								comment_position = position[17]

								symbol_position = position[16]
					
								print("Total positions on ",sym.name,' = ',len(positions))
								if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '1M gen SMI')):
									#print('same sell')
									logging.warning('same sell')
									continue

						#vol_traded_max = (my_money/100) * 0.6
								
					#continue
						if (flag_cross_1M_sell == 'sell'):
							comment = '1M gen SMI'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.045):
								print("spred = ", spred)
								logging.warning("spred = %f"%spred)
								continue

							
							if (flag_cross_1M_sell == 'sell'):
								tp_sell = ((abs(data_macd_1M_sell['tp'])) + (((spred) * abs(data_macd_1M_sell['tp']))/100))
								sp_sell = ((abs(data_macd_1M_sell['st'])) + (((spred + 0.05) * abs(data_macd_1M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_1M_sell['score'] * my_money)/1000000))

							if (tp_sell >= (price)): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 0.09):
								lot = 0.09

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								lot = 0
								#print('No Money')
								logging.warning('No Money')
								break

							if True:#(tp_buy > price):
								if True:
									print(sym.name,': ','sell')
									request = {
										"action": mt5.TRADE_ACTION_DEAL,
    									"symbol": sym.name,
    									"volume": lot,
    									"type": mt5.ORDER_TYPE_SELL,
    									"price": price,
    									"sl": sp_sell,
    									"tp": tp_sell,
    									"deviation": deviation,
    									"magic": magic,
    									"comment": comment,
    									"type_time": mt5.ORDER_TIME_GTC,
    									"type_filling": mt5.ORDER_FILLING_FOK
    									}
								else:
									print('//////////////////////////////////////tp<buy*****************************************************')
									request = {}

								result = mt5.order_send(request)
								# check the execution result
								print("1. order_send(): by {} {} lots at {} with deviation={} points".format(sym.name,lot,price,deviation));
						except:
							#print('request failed 1M Trade MACD')
							logging.warning('request failed 1M Trade MACD')
						try:
							if result.retcode != mt5.TRADE_RETCODE_DONE:
								print("2. order_send failed, retcode={}".format(result.retcode))
								# request the result as a dictionary and display it element by element
								result_dict=result._asdict()
								for field in result_dict.keys():
									print("   {}={}".format(field,result_dict[field]))
        						# if this is a trading request structure, display it element by element as well
									if field=="request":
										traderequest_dict=result_dict[field]._asdict()
										for tradereq_filed in traderequest_dict:
											print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
									else:
										#print('send Done 1M Trade MACD!!!')
										logging.warning('send Done 1M Trade MACD!!!')
						except:
							#print('some thing wrong send 1M Trade MACD')
							logging.warning('some thing wrong send 1M Trade MACD')
							continue
		except:
			#print('cant Play 1M Trade MACD!!!')
			logging.warning('cant Play 1M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************
		#print('////////////////////////////////////////////')
		#print('')
		#print('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		#print('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		#print('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		#print('')
		#print('')
		#print('')

		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('')
		logging.debug('')
		logging.debug('')



		

#trade_strategy_tarkibi(20,2)
trade_strategy_SMI_1M()
