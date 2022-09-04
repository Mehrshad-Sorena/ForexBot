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

#from ta import add_all_ta_features
#from ind.utils import dropna
#from ind.trend import MACD
#symbol_data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
#symbol_data_ichi,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)


def trade_strategy_tarkibi(max_allow_score):
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

	vol_traded = 0


	symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,10)

	for sym in symbols:
		positions = mt5.positions_get(symbol=sym.name)
		#print(positions)
		if positions == None:
			print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
		elif len(positions)>0:
			for position in positions:
				type_position = position[5]
				vol_position = position[9]

				vol_traded += vol_position





	symbol_data_30M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
	symbol_data_1H,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,500)
	symbol_data_1D,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,500)
	symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)
	symbol_data_1M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M1,500)

	vol_traded_max = (my_money/100) * 0.05
	
	#symbol_data_M1,my_money,symbols = log_get_data(mt5.TIMEFRAME_M1,1000)
	#print("money",my_money)
#print("symbol = ",symbols.name)

	#symbol_data = symbol_daind.append(symbol_data_local, ignore_index = True)	

#print(type(MACD(symbol_data['EURUSD']['open'],26,12,9,False) ))

	magic = time.time_ns()

	for sym in symbols:
		if (my_money == 0): break
		if (sym.name == 'EURDKK_i'): continue
		if (sym.name == 'USDTRY_i'): continue
		if (sym.name == 'EURTRY_i'): continue

		if (vol_traded >= vol_traded_max): 
			print('No Money')
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
					data_macd_1M_buy['score'] = (float(data_macd_1M_buy['score']) / 2)

					if(data_macd_1M_buy['score'] < max_allow_score):
						data_macd_1M_buy['score'] = data_macd_1M_buy['score']/10

		except:
			#continue

			data_macd_1M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)

			macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_1M_buy)))

			data_macd_1M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': (((-1) * abs(mean_macd))/2) ,'score': 0}

			

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
					data_macd_1M_sell['score'] = (float(data_macd_1M_sell['score']) / 2)

					if(data_macd_1M_sell['score'] < max_allow_score):
						data_macd_1M_sell['score'] = data_macd_1M_sell['score']/10

		except:
			#continue
			data_macd_1M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)

			macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_1M_sell)))

			data_macd_1M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': (((-1) * abs(mean_macd))/2),'score': 20}

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
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

			macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_buy)))

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 10}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 5M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M_sell = line
					data_macd_5M_sell['tp'] = float(data_macd_5M_sell['tp'])
					data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp']/3)*2

					data_macd_5M_sell['st'] = float(data_macd_5M_sell['st'])
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

			macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

			macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_sell)))

			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 20}

		#******************************//////////////////////***********************************************************
		
		#****************************** Data_Buy 30M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_30M_buy = line
					data_macd_30M_buy['tp'] = float(data_macd_30M_buy['tp'])
					#data_macd_30M_buy['tp'] = (data_macd_30M_buy['tp']/3)*2

					data_macd_30M_buy['st'] = float(data_macd_30M_buy['st'])
					data_macd_30M_buy['macd_fast'] = float(data_macd_30M_buy['macd_fast'])
					data_macd_30M_buy['macd_slow'] = float(data_macd_30M_buy['macd_slow'])
					data_macd_30M_buy['macd_signal'] = float(data_macd_30M_buy['macd_signal'])
					data_macd_30M_buy['diff_minus'] = float(data_macd_30M_buy['diff_minus'])
					data_macd_30M_buy['diff_plus'] = float(data_macd_30M_buy['diff_plus'])
					data_macd_30M_buy['score'] = float(data_macd_30M_buy['score'])

					if(data_macd_30M_buy['score'] < max_allow_score):
						data_macd_30M_buy['score'] = data_macd_30M_buy['score']/10
		except:
			#continue
			data_macd_30M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

			macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_buy)))

			data_macd_30M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 1.5) , 'diff_minus': ((-1) * abs(mean_macd) * 1.5) ,'score': 0}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Sell 30M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_30M_sell = line
					data_macd_30M_sell['tp'] = float(data_macd_30M_sell['tp'])
					#data_macd_30M_sell['tp'] = (data_macd_30M_sell['tp']/3)*2

					data_macd_30M_sell['st'] = float(data_macd_30M_sell['st'])
					data_macd_30M_sell['macd_fast'] = float(data_macd_30M_sell['macd_fast'])
					data_macd_30M_sell['macd_slow'] = float(data_macd_30M_sell['macd_slow'])
					data_macd_30M_sell['macd_signal'] = float(data_macd_30M_sell['macd_signal'])
					data_macd_30M_sell['diff_minus'] = float(data_macd_30M_sell['diff_minus'])
					data_macd_30M_sell['diff_plus'] = float(data_macd_30M_sell['diff_plus'])
					data_macd_30M_sell['score'] = float(data_macd_30M_sell['score'])

					if(data_macd_30M_sell['score'] < max_allow_score):
						data_macd_30M_sell['score'] = data_macd_30M_sell['score']/10
		except:
			#continue
			data_macd_30M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

			macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_sell)))

			data_macd_30M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 1.5) , 'diff_minus': ((-1) * abs(mean_macd) * 1.5),'score': 0}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Buy 1H MACD *******************************************************************

		try:
			with open("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1H_buy = line
					data_macd_1H_buy['tp'] = float(data_macd_1H_buy['tp'])
					#data_macd_1H_buy['tp'] = (data_macd_1H_buy['tp']/3)*2

					data_macd_1H_buy['st'] = float(data_macd_1H_buy['st'])
					data_macd_1H_buy['macd_fast'] = float(data_macd_1H_buy['macd_fast'])
					data_macd_1H_buy['macd_slow'] = float(data_macd_1H_buy['macd_slow'])
					data_macd_1H_buy['macd_signal'] = float(data_macd_1H_buy['macd_signal'])
					data_macd_1H_buy['diff_minus'] = float(data_macd_1H_buy['diff_minus'])
					data_macd_1H_buy['diff_plus'] = float(data_macd_1H_buy['diff_plus'])
					data_macd_1H_buy['score'] = float(data_macd_1H_buy['score'])

					if(data_macd_1H_buy['score'] < max_allow_score):
						data_macd_1H_buy['score'] = data_macd_1H_buy['score']/10


		except:
			#continue
			data_macd_1H_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 1H MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1H_sell = line
					data_macd_1H_sell['tp'] = float(data_macd_1H_sell['tp'])
					#data_macd_1H_sell['tp'] = (data_macd_1H_sell['tp']/3)*2

					data_macd_1H_sell['st'] = float(data_macd_1H_sell['st'])
					data_macd_1H_sell['macd_fast'] = float(data_macd_1H_sell['macd_fast'])
					data_macd_1H_sell['macd_slow'] = float(data_macd_1H_sell['macd_slow'])
					data_macd_1H_sell['macd_signal'] = float(data_macd_1H_sell['macd_signal'])
					data_macd_1H_sell['diff_minus'] = float(data_macd_1H_sell['diff_minus'])
					data_macd_1H_sell['diff_plus'] = float(data_macd_1H_sell['diff_plus'])
					data_macd_1H_sell['score'] = float(data_macd_1H_sell['score'])

					if(data_macd_1H_sell['score'] < max_allow_score):
						data_macd_1H_sell['score'] = data_macd_1H_sell['score']/10


		except:
			#continue
			data_macd_1H_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 1D MACD *******************************************************************

		try:
			with open("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1D_buy = line
					data_macd_1D_buy['tp'] = float(data_macd_1D_buy['tp'])
					#data_macd_30M_buy['tp'] = (data_macd_30M_buy['tp']/3)*2

					data_macd_1D_buy['st'] = float(data_macd_1D_buy['st'])
					data_macd_1D_buy['macd_fast'] = float(data_macd_1D_buy['macd_fast'])
					data_macd_1D_buy['macd_slow'] = float(data_macd_1D_buy['macd_slow'])
					data_macd_1D_buy['macd_signal'] = float(data_macd_1D_buy['macd_signal'])
					data_macd_1D_buy['diff_minus'] = float(data_macd_1D_buy['diff_minus'])
					data_macd_1D_buy['diff_plus'] = float(data_macd_1D_buy['diff_plus'])
					data_macd_1D_buy['score'] = float(data_macd_1D_buy['score'])

					if(data_macd_1D_buy['score'] < max_allow_score):
						data_macd_1D_buy['score'] = data_macd_1D_buy['score']/10
		except:
			#continue
			data_macd_1D_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

			macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(macd_1D_buy))

			data_macd_1D_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': abs(mean_macd) , 'diff_minus': ((-1) * abs(mean_macd)) ,'score': 0}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Sell 1D MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_1D_sell = line
					data_macd_1D_sell['tp'] = float(data_macd_1D_sell['tp'])
					#data_macd_30M_sell['tp'] = (data_macd_30M_sell['tp']/3)*2

					data_macd_1D_sell['st'] = float(data_macd_1D_sell['st'])
					data_macd_1D_sell['macd_fast'] = float(data_macd_1D_sell['macd_fast'])
					data_macd_1D_sell['macd_slow'] = float(data_macd_1D_sell['macd_slow'])
					data_macd_1D_sell['macd_signal'] = float(data_macd_1D_sell['macd_signal'])
					data_macd_1D_sell['diff_minus'] = float(data_macd_1D_sell['diff_minus'])
					data_macd_1D_sell['diff_plus'] = float(data_macd_1D_sell['diff_plus'])
					data_macd_1D_sell['score'] = float(data_macd_1D_sell['score'])

					if(data_macd_1D_sell['score'] < max_allow_score):
						data_macd_1D_sell['score'] = data_macd_1D_sell['score']/10
		except:
			#continue
			data_macd_1D_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_1D_sell = ind.macd(symbol_data_1D[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

			macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(macd_1D_sell))

			data_macd_1D_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': abs(mean_macd) , 'diff_minus': ((-1) * abs(mean_macd)),'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 5M30M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M30M_buy = line
					data_macd_5M30M_buy['tp'] = float(data_macd_5M30M_buy['tp'])
					#data_macd_5M30M_buy['tp'] = (data_macd_5M30M_buy['tp']/3)*2

					data_macd_5M30M_buy['st'] = float(data_macd_5M30M_buy['st'])
					data_macd_5M30M_buy['macd_fast5M'] = float(data_macd_5M30M_buy['macd_fast5M'])
					data_macd_5M30M_buy['macd_slow5M'] = float(data_macd_5M30M_buy['macd_slow5M'])
					data_macd_5M30M_buy['macd_signal5M'] = float(data_macd_5M30M_buy['macd_signal5M'])
					data_macd_5M30M_buy['diff_plus5M'] = float(data_macd_5M30M_buy['diff_plus5M'])
					data_macd_5M30M_buy['diff_minus5M'] = float(data_macd_5M30M_buy['diff_minus5M'])
					data_macd_5M30M_buy['macd_fast30M'] = float(data_macd_5M30M_buy['macd_fast30M'])
					data_macd_5M30M_buy['macd_slow30M'] = float(data_macd_5M30M_buy['macd_slow30M'])
					data_macd_5M30M_buy['macd_signal30M'] = float(data_macd_5M30M_buy['macd_signal30M'])
					data_macd_5M30M_buy['diff_minus30M'] = float(data_macd_5M30M_buy['diff_minus30M'])
					data_macd_5M30M_buy['diff_plus30M'] = float(data_macd_5M30M_buy['diff_plus30M'])
					data_macd_5M30M_buy['score'] = float(data_macd_5M30M_buy['score'])

					if(data_macd_5M30M_buy['score'] < max_allow_score):
						data_macd_5M30M_buy['score'] = data_macd_5M30M_buy['score']/10

		except:
			#continue
			data_macd_5M30M_buy = {'apply_to5M': 'close','apply_to30M': 'close','tp' : 0.02, 'st' : 0.3,
			'macd_fast5M': 8 , 'macd_slow5M': 18, 'macd_signal5M': 6,'macd_fast30M': 8 , 'macd_slow30M': 18, 'macd_signal30M': 6
			,'diff_plus5M':0 , 'diff_minus5M': 0,'diff_plus30M':0 , 'diff_minus30M': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 5M30M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M30M_sell = line
					data_macd_5M30M_sell['tp'] = float(data_macd_5M30M_sell['tp'])
					#data_macd_5M30M_sell['tp'] = (data_macd_5M30M_sell['tp']/3)*2

					data_macd_5M30M_sell['st'] = float(data_macd_5M30M_sell['st'])
					data_macd_5M30M_sell['macd_fast5M'] = float(data_macd_5M30M_sell['macd_fast5M'])
					data_macd_5M30M_sell['macd_slow5M'] = float(data_macd_5M30M_sell['macd_slow5M'])
					data_macd_5M30M_sell['macd_signal5M'] = float(data_macd_5M30M_sell['macd_signal5M'])
					data_macd_5M30M_sell['diff_plus5M'] = float(data_macd_5M30M_sell['diff_plus5M'])
					data_macd_5M30M_sell['diff_minus5M'] = float(data_macd_5M30M_sell['diff_minus5M'])
					data_macd_5M30M_sell['macd_fast30M'] = float(data_macd_5M30M_sell['macd_fast30M'])
					data_macd_5M30M_sell['macd_slow30M'] = float(data_macd_5M30M_sell['macd_slow30M'])
					data_macd_5M30M_sell['macd_signal30M'] = float(data_macd_5M30M_sell['macd_signal30M'])
					data_macd_5M30M_sell['diff_plus30M'] = float(data_macd_5M30M_sell['diff_plus30M'])
					data_macd_5M30M_sell['diff_minus30M'] = float(data_macd_5M30M_sell['diff_minus30M'])
					data_macd_5M30M_sell['score'] = float(data_macd_5M30M_sell['score'])

					if(data_macd_5M30M_sell['score'] < max_allow_score):
						data_macd_5M30M_sell['score'] = data_macd_5M30M_sell['score']/10

		except:
			#continue
			data_macd_5M30M_sell = {'apply_to5M': 'close','apply_to30M': 'close','tp' : 0.02, 'st' : 0.3,
			'macd_fast5M': 8 , 'macd_slow5M': 18, 'macd_signal5M': 6,'macd_fast30M': 8 , 'macd_slow30M': 18, 'macd_signal30M': 6
			,'diff_plus5M':0 , 'diff_minus5M': 0,'diff_plus30M':0 , 'diff_minus30M': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy porro MACD *******************************************************************

		try:
			with open("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_porro_buy = line
					data_macd_porro_buy['tp'] = float(data_macd_porro_buy['tp'])
					#data_macd_porro_buy['tp'] = (data_macd_porro_buy['tp']/3)*2

					data_macd_porro_buy['st'] = float(data_macd_porro_buy['st'])
					data_macd_porro_buy['macd_fast5M'] = float(data_macd_porro_buy['macd_fast5M'])
					data_macd_porro_buy['macd_slow5M'] = float(data_macd_porro_buy['macd_slow5M'])
					data_macd_porro_buy['macd_signal5M'] = float(data_macd_porro_buy['macd_signal5M'])
					data_macd_porro_buy['diff_plus5M'] = float(data_macd_porro_buy['diff_plus5M'])
					data_macd_porro_buy['diff_minus5M'] = float(data_macd_porro_buy['diff_minus5M'])
					data_macd_porro_buy['macd_fast30M'] = float(data_macd_porro_buy['macd_fast30M'])
					data_macd_porro_buy['macd_slow30M'] = float(data_macd_porro_buy['macd_slow30M'])
					data_macd_porro_buy['macd_signal30M'] = float(data_macd_porro_buy['macd_signal30M'])
					data_macd_porro_buy['diff_plus30M'] = float(data_macd_porro_buy['diff_plus30M'])
					data_macd_porro_buy['diff_minus30M'] = float(data_macd_porro_buy['diff_minus30M'])
					data_macd_porro_buy['macd_fast1H'] = float(data_macd_porro_buy['macd_fast1H'])
					data_macd_porro_buy['macd_slow1H'] = float(data_macd_porro_buy['macd_slow1H'])
					data_macd_porro_buy['macd_signal1H'] = float(data_macd_porro_buy['macd_signal1H'])
					data_macd_porro_buy['diff_plus1H'] = float(data_macd_porro_buy['diff_plus1H'])
					data_macd_porro_buy['diff_minus1H'] = float(data_macd_porro_buy['diff_minus1H'])
					data_macd_porro_buy['score'] = float(data_macd_porro_buy['score'])

					if(data_macd_porro_buy['score'] < max_allow_score):
						data_macd_porro_buy['score'] = data_macd_porro_buy['score']/10

		except:
			#continue
			data_macd_porro_buy = {'apply_to5M': 'close','apply_to30M': 'close', 'apply_to1H': 'close','tp' : 0.02, 'st' : 0.3,
			'macd_fast5M': 8 , 'macd_slow5M': 18, 'macd_signal5M': 6,'macd_fast30M': 8 , 'macd_slow30M': 18, 'macd_signal30M': 6,'macd_fast1H': 8 , 'macd_slow1H': 18, 'macd_signal1H': 6
			,'diff_plus5M':0 , 'diff_minus5M': 0,'diff_plus30M':0 , 'diff_minus30M': 0,'diff_plus1H':0 , 'diff_minus1H': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell porro MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_porro_sell = line
					data_macd_porro_sell['tp'] = float(data_macd_porro_sell['tp'])
					#data_macd_porro_sell['tp'] = (data_macd_porro_sell['tp']/3)*2
					
					data_macd_porro_sell['st'] = float(data_macd_porro_sell['st'])
					data_macd_porro_sell['macd_fast5M'] = float(data_macd_porro_sell['macd_fast5M'])
					data_macd_porro_sell['macd_slow5M'] = float(data_macd_porro_sell['macd_slow5M'])
					data_macd_porro_sell['macd_signal5M'] = float(data_macd_porro_sell['macd_signal5M'])
					data_macd_porro_sell['diff_plus5M'] = float(data_macd_porro_sell['diff_plus5M'])
					data_macd_porro_sell['diff_minus5M'] = float(data_macd_porro_sell['diff_minus5M'])
					data_macd_porro_sell['macd_fast30M'] = float(data_macd_porro_sell['macd_fast30M'])
					data_macd_porro_sell['macd_slow30M'] = float(data_macd_porro_sell['macd_slow30M'])
					data_macd_porro_sell['macd_signal30M'] = float(data_macd_porro_sell['macd_signal30M'])
					data_macd_porro_sell['diff_plus30M'] = float(data_macd_porro_sell['diff_plus30M'])
					data_macd_porro_sell['diff_minus30M'] = float(data_macd_porro_sell['diff_minus30M'])
					data_macd_porro_sell['macd_fast1H'] = float(data_macd_porro_sell['macd_fast1H'])
					data_macd_porro_sell['macd_slow1H'] = float(data_macd_porro_sell['macd_slow1H'])
					data_macd_porro_sell['macd_signal1H'] = float(data_macd_porro_sell['macd_signal1H'])
					data_macd_porro_sell['diff_plus1H'] = float(data_macd_porro_sell['diff_plus1H'])
					data_macd_porro_sell['diff_minus1H'] = float(data_macd_porro_sell['diff_minus1H'])
					data_macd_porro_sell['score'] = float(data_macd_porro_sell['score'])

					if(data_macd_porro_sell['score'] < max_allow_score):
						data_macd_porro_sell['score'] = data_macd_porro_sell['score']/10

		except:
			#continue
			data_macd_porro_sell = {'apply_to5M': 'close','apply_to30M': 'close', 'apply_to1H': 'close','tp' : 0.02, 'st' : 0.3,
			'macd_fast5M': 8 , 'macd_slow5M': 18, 'macd_signal5M': 6,'macd_fast30M': 8 , 'macd_slow30M': 18, 'macd_signal30M': 6,'macd_fast1H': 8 , 'macd_slow1H': 18, 'macd_signal1H': 6
			,'diff_plus5M':0 , 'diff_minus5M': 0,'diff_plus30M':0 , 'diff_minus30M': 0,'diff_plus1H':0 , 'diff_minus1H': 0,'score': 0}

		#******************************//////////////////////***********************************************************


		symbol_data_30M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
		symbol_data_H1,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,5)
		symbol_data_1D,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,5)
		symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)
		symbol_data_1M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M1,1)

	#help(ind.macd)
		try:
			# *******************++++++++++++ MACD Buy 30M************************************************************

			macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

			macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]
			macdh_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[1]]
			macds_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[2]]

			MACD_signal_cross_30M_buy = cross_macd(macd_30M_buy,macds_30M_buy,macdh_30M_buy,sym.name,data_macd_30M_buy['diff_minus'],data_macd_30M_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('30M Buy Macd Wrong!!')

		try:

			# *******************++++++++++++ MACD Sell 30M************************************************************

			macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

			macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]
			macdh_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[1]]
			macds_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[2]]

			MACD_signal_cross_30M_sell = cross_macd(macd_30M_sell,macds_30M_sell,macdh_30M_sell,sym.name,data_macd_30M_sell['diff_minus'],data_macd_30M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************
		except:
			print('30M Sell Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Buy 1M************************************************************

			macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)

			macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]
			macdh_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[1]]
			macds_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[2]]
			MACD_signal_cross_1M_buy = cross_macd(macd_1M_buy,macds_1M_buy,macdh_1M_buy,sym.name,data_macd_1M_buy['diff_minus'],data_macd_1M_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 1M************************************************************

			macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)

			macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]
			macdh_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[1]]
			macds_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[2]]
			MACD_signal_cross_1M_sell = cross_macd(macd_1M_sell,macds_1M_sell,macdh_1M_sell,sym.name,data_macd_1M_sell['diff_minus'],data_macd_1M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1M Sell Macd Wrong!!')
			


		try:

			# *******************++++++++++++ MACD Buy 5M************************************************************

			macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

			macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
			macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
			macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
			MACD_signal_cross_5M_buy = cross_macd(macd_5M_buy,macds_5M_buy,macdh_5M_buy,sym.name,data_macd_5M_buy['diff_minus'],data_macd_5M_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 5M************************************************************

			macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

			macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
			macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
			macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
			MACD_signal_cross_5M_sell = cross_macd(macd_5M_sell,macds_5M_sell,macdh_5M_sell,sym.name,data_macd_5M_sell['diff_minus'],data_macd_5M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Sell Macd Wrong!!')
			

		try:
			# *******************++++++++++++ MACD Buy 1H************************************************************

			macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)

			macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]
			macdh_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[1]]
			macds_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[2]]
			MACD_signal_cross_1H_buy = cross_macd(macd_1H_buy,macds_1H_buy,macdh_1H_buy,sym.name,data_macd_1H_buy['diff_minus'],data_macd_1H_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1H Buy Macd Wrong!!')



		try:
			# *******************++++++++++++ MACD Sell 1H ************************************************************

			macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

			macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]
			macdh_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[1]]
			macds_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[2]]
			MACD_signal_cross_1H_sell = cross_macd(macd_1H_sell,macds_1H_sell,macdh_1H_sell,sym.name,data_macd_1H_sell['diff_minus'],data_macd_1H_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************
			#print(macd_5M)
			#print(len(macd_5M))
		except:
			print('1H Sell Macd Wrong!!')


		
		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		try:
			# *******************++++++++++++ MACD Buy 1D************************************************************

			macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

			macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]
			macdh_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[1]]
			macds_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[2]]
			MACD_signal_cross_1D_buy = cross_macd(macd_1D_buy,macds_1D_buy,macdh_1D_buy,sym.name,data_macd_1D_buy['diff_minus'],data_macd_1D_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1D Buy Macd Wrong!!')



		try:
			# *******************++++++++++++ MACD Sell 1D ************************************************************

			macd_all_1D_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

			macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]
			macdh_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[1]]
			macds_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[2]]
			MACD_signal_cross_1D_sell = cross_macd(macd_1D_sell,macds_1D_sell,macdh_1D_sell,sym.name,data_macd_1D_sell['diff_minus'],data_macd_1D_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************
			#print(macd_5M)
			#print(len(macd_5M))
		except:
			print('1D Sell Macd Wrong!!')
		
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#macd = macd.dropna() # delete nan values


#print("macd = ",macd[macd.columns[0]])#macd
#print("macd = ",macd[macd.columns[1]])#histogram
#print("macd = ",macd[macd.columns[2]])#signal

		#ma = ind.sma(symbol_data[sym.name]['close'],length=3)

		#rsi = ind.rsi(symbol_data[sym.name]['close'],length=14)


		#ichi = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
		#tenkan=21,kijun=25,snkou=52)

		#SPANA = ichi[0][ichi[0].columns[0]]
		#SPANB = ichi[0][ichi[0].columns[1]]
		#tenkan = ichi[0][ichi[0].columns[2]]
		#kijun = ichi[0][ichi[0].columns[3]]
		#chikospan = ichi[0][ichi[0].columns[4]]
		#chikospan_30M = chikospan
		#kijun_30M = kijun
		#tenkan_30M = tenkan

		#chiko_sig_30M[sym.name] = chiko_signal(chikospan,tenkan,kijun,sym.name)

		#TK_KS_signal = cross_TsKs_Buy_signal(tenkan,kijun,sym.name)

		#TK_KS_signal_exit = exit_signal_TsKs(tenkan,kijun,sym.name)

		#ichi = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
		#tenkan=9,kijun=28,snkou=52)

		#SPANA_5M = ichi[0][ichi[0].columns[0]]
		#SPANB_5M = ichi[0][ichi[0].columns[1]]
		#tenkan_5M = ichi[0][ichi[0].columns[2]]
		#kijun_5M = ichi[0][ichi[0].columns[3]]
		#chikospan_5M = ichi[0][ichi[0].columns[4]]


		#chiko_sig_5M[sym.name] = chiko_signal(chikospan_5M,tenkan_5M,kijun_5M,sym.name)

		#TK_KS_signal_5M = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

		#TK_KS_signal_exit_5M = exit_signal_TsKs(tenkan_5M,kijun_5M,sym.name)

		


		signal = 0
		flag_cross_30M = ''
		flag_cross_5M = ''
		flag_cross_1M = ''
		flag_cross_1H = ''
		flag_cross_porro = ''
		flag_cross_5M30M = ''

		#print('get signal!!!')

		try:
			#print(sym.name)

			if (((MACD_signal_cross_30M_buy['signal'] == 'buya') & True#(TsKs_signal_cross_30M_buy['signal'] == 'buy') 
				& (MACD_signal_cross_30M_buy['index']>=997) 
				& ((macd_30M_buy[len(macd_30M_buy)-1]<=data_macd_30M_buy['diff_minus']) & (macds_30M_buy[len(macd_30M_buy)-1]<=data_macd_30M_buy['diff_minus']) ))):
				if ((macd_1D_buy[len(macd_1D_buy)-1] <= (data_macd_1D_buy['diff_minus']/2)) & (macds_1D_buy[len(macd_30M_buy)-1] <= (data_macd_1D_buy['diff_minus']/2))):
					if ((macd_1D_buy[len(macd_1D_buy)-1] >= macd_1D_buy[len(macd_1D_buy)-5]) & (macds_1D_buy[len(macds_1D_buy)-1] >= macds_1D_buy[len(macds_1D_buy)-5])
						| ((macd_1D_buy[len(macd_1D_buy)-1] >= macd_1D_buy[len(macd_1D_buy)-5]) & (macds_1D_buy[len(macds_1D_buy)-1] <= macds_1D_buy[len(macds_1D_buy)-5])) ):

						if (((MACD_signal_cross_1M_buy['signal'] == 'buy')) & (MACD_signal_cross_1M_buy['index'] >= 967)):
							if (((MACD_signal_cross_5M_buy['signal'] == 'buy')) & (MACD_signal_cross_5M_buy['index'] >= 987)):
								flag_cross_30M = 'buy'

						if ((((MACD_signal_cross_1D_buy['signal'] == 'sell') | (MACD_signal_cross_1D_buy['signal'] == 'faild_sell')) & (MACD_signal_cross_1D_buy['index'] > 493))):
							flag_cross_30M = 'failed'
						
		except:
			print('signal problem 30M BUY MACD!!!')

		try:

			if (((MACD_signal_cross_30M_sell['signal'] == 'sella') & True#(TsKs_signal_cross_30M_sell['signal'] == 'sell')
				& (MACD_signal_cross_30M_sell['index']>=997) 
				& ((macd_30M_sell[len(macd_30M_sell)-1]>=data_macd_30M_sell['diff_plus']) & (macds_30M_sell[len(macd_30M_sell)-1]>=data_macd_30M_sell['diff_plus']) ))):
				if ((macd_1D_sell[len(macd_1D_sell)-1] >= (data_macd_1D_sell['diff_plus']/2)) & (macds_1D_sell[len(macd_1D_sell)-1] >= (data_macd_1D_sell['diff_plus']/2))):
					if ((macd_1D_sell[len(macd_1D_sell)-1] <= macd_1D_sell[len(macd_1D_sell)-2]) & (macds_1D_sell[len(macds_1D_sell)-1] <= macds_1D_sell[len(macds_1D_sell)-2])
						| ((macd_1D_sell[len(macd_1D_sell)-1] <= macd_1D_sell[len(macd_1D_sell)-2]) & (macds_1D_sell[len(macds_1D_sell)-1] >= macds_1D_sell[len(macds_1D_sell)-2])) ):

						if (((MACD_signal_cross_1M_sell['signal'] == 'sell')) & (MACD_signal_cross_1M_sell['index'] >= 967)):
							if(((MACD_signal_cross_5M_sell['signal'] == 'sell')) & (MACD_signal_cross_5M_sell['index'] >= 987)):
								flag_cross_30M = 'sell'

						if ((((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] > 493))):
							flag_cross_30M = 'failed'
						
		except:
			print('signal problem 30M SELL MACD!!!')

		#************************************************** 1M Signal Buy ***************************************************************************

		try:

			if (((MACD_signal_cross_1M_buy['signal'] == 'buya') & True#(TsKs_signal_cross_5M_buy['signal'] == 'buy')  
				& (MACD_signal_cross_1M_buy['index'] >= 996) 
				#& (TsKs_signal_cross_5M_buy['index'] >= 960)
				& ((macd_1M_buy[len(macd_1M_buy)-1] <= (data_macd_1M_buy['diff_plus']/2)) & (macds_1M_buy[len(macd_1M_buy)-1] <= (data_macd_1M_buy['diff_plus']/2)) ))):
				print('buy 1')
				print('macd30 buy = ',macd_30M_buy[len(macd_30M_buy)-1])
				print('macds30 buy = ',macds_30M_buy[len(macd_30M_buy)-1])
				print('diff30 = ',data_macd_30M_buy['diff_minus'])
				if ((macd_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_minus']/2)) & (macds_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_minus']/2))):
					print('macd30 diff minus pass')
					if ((macd_30M_buy[len(macd_30M_buy)-1] >= macd_30M_buy[len(macd_30M_buy)-5]) & (macds_30M_buy[len(macd_30M_buy)-1] >= macds_30M_buy[len(macd_30M_buy)-5])
						| ((macd_30M_buy[len(macd_30M_buy)-1] >= macd_30M_buy[len(macd_30M_buy)-5]) & (macds_30M_buy[len(macd_30M_buy)-1] <= macds_30M_buy[len(macd_30M_buy)-5])) ):
						print('macd30 buy= ', MACD_signal_cross_30M_buy)
						if ((((MACD_signal_cross_30M_buy['signal'] == 'sell') | (MACD_signal_cross_30M_buy['signal'] == 'faild_sell')) & (MACD_signal_cross_30M_buy['index']<=968))
							| (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index']>968)) ):
							print('buy')
							flag_cross_1M = 'buy'
		except:
			print('signal problem 1M BUY MACD!!!')

		#*************************************** 1M Signal Sell *******************************************************************************************

		try:

			if (((MACD_signal_cross_1M_sell['signal'] == 'sella') & True#(TsKs_signal_cross_5M_sell['signal'] == 'sell')
				& (MACD_signal_cross_1M_sell['index'] >= 996) 
				#& (TsKs_signal_cross_5M_sell['index'] >= 960)
				& ((macd_1M_sell[len(macd_1M_sell)-1] >= (data_macd_1M_sell['diff_minus']/2)) & (macds_1M_sell[len(macd_1M_sell)-1] >= (data_macd_1M_sell['diff_minus']/2)) ))):
				print('sell 1')
				print('macd30 sell = ',macd_30M_sell[len(macd_30M_sell)-1])
				print('macds30 sell = ',macds_30M_sell[len(macd_30M_sell)-1])
				print('diff30 = ',data_macd_30M_sell['diff_plus'])
				if ((macd_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_plus']/2)) & (macds_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_plus']/2))):
					print('macd30 sell= ',MACD_signal_cross_30M_sell)
					if ((macd_30M_sell[len(macd_30M_sell)-1] <= macd_30M_sell[len(macd_30M_sell)-5]) & (macds_30M_sell[len(macds_30M_sell)-1] <= macds_30M_buy[len(macds_30M_sell)-5])
						| ((macd_30M_sell[len(macd_30M_sell)-1] <= macd_30M_sell[len(macd_30M_sell)-5]) & (macds_30M_sell[len(macds_30M_sell)-1] >= macds_30M_buy[len(macds_30M_sell)-5])) ):
						if ((((MACD_signal_cross_30M_sell['signal'] == 'buy') | (MACD_signal_cross_30M_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_sell['index']<=968))
							| (((MACD_signal_cross_30M_sell['signal'] == 'sell') | (MACD_signal_cross_30M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_30M_sell['index']>968)) ):
							print('sell')
							flag_cross_1M = 'sell'
		except:
			print('signal problem 1M SELL MACD!!!')

		#****************--------------------++++++++++++++++++++++++****************************************************************++++++++++++++++++++++

		try:

			if ((MACD_signal_cross_5M_buy['signal'] == 'buy') & (MACD_signal_cross_5M_buy['index'] >= 997)):
				print('buy tarkibi 0: ',sym.name)
				print('macd30 buy = ',macd_30M_buy[len(macd_30M_buy)-1])
				print('macds30 buy = ',macds_30M_buy[len(macd_30M_buy)-1])
				print('diff30 = ',data_macd_30M_buy['diff_minus'])
				if ((macd_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_minus']/2)) & (macds_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_minus']/2))):
					print('buy tarkibi 1')
					if ((macd_30M_buy[len(macd_30M_buy)-1] >= macd_30M_buy[len(macd_30M_buy)-1]) & (macds_30M_buy[len(macd_30M_buy)-1] >= macds_30M_buy[len(macd_30M_buy)-1])
						| ((macd_30M_buy[len(macd_30M_buy)-1] >= macd_30M_buy[len(macd_30M_buy)-1]) & (macds_30M_buy[len(macd_30M_buy)-1] <= macds_30M_buy[len(macd_30M_buy)-1])) ):
						print('buy tarkibi 2')
						if (macd_30M_buy[len(macd_30M_buy)-1] < macds_30M_buy[len(macd_30M_buy)-1]):
							print('buy tarkibi 3')
							#print('1M signal = ',MACD_signal_cross_1M_buy['signal'])
							if True:#(((MACD_signal_cross_1M_buy['signal'] == 'buy') | (MACD_signal_cross_1M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1M_buy['index'] >= 975)):
								print('buy tarkibi finished')
								flag_cross_5M = 'buy'

			if ((((MACD_signal_cross_30M_buy['signal'] == 'sell') | (MACD_signal_cross_30M_buy['signal'] == 'faild_sell')) & (MACD_signal_cross_30M_buy['index'] > 993))):
				flag_cross_5M = 'failed'
				print('buy tarkibi failed')
						
		except:
			print('signal problem 5M BUY MACD!!!')

		try:

			if ((MACD_signal_cross_5M_sell['signal'] == 'sell') & (MACD_signal_cross_5M_sell['index'] >= 997)):
				print('sell tarkibi 0: ',sym.name)
				print('macd30 sell = ',macd_30M_sell[len(macd_30M_sell)-1])
				print('macds30 sell = ',macds_30M_sell[len(macd_30M_sell)-1])
				print('diff30 = ',data_macd_30M_sell['diff_plus'])
				if ((macd_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_plus']/2)) & (macds_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_plus']/2))):
					print('macd30 sell= ',MACD_signal_cross_30M_sell)
					print('sell tarkibi 1')
					if ((macd_30M_sell[len(macd_30M_sell)-1] <= macd_30M_sell[len(macd_30M_sell)-1]) & (macds_30M_sell[len(macds_30M_sell)-1] <= macds_30M_buy[len(macds_30M_sell)-1])
						| ((macd_30M_sell[len(macd_30M_sell)-1] <= macd_30M_sell[len(macd_30M_sell)-1]) & (macds_30M_sell[len(macds_30M_sell)-1] >= macds_30M_buy[len(macds_30M_sell)-1])) ):

						print('sell tarkibi 2')

						if (macds_30M_sell[len(macds_30M_sell)-1] < macd_30M_sell[len(macd_30M_sell)-1]):
							print('sell tarkibi 3')
							#print('1M signal = ',MACD_signal_cross_1M_sell['signal'])
							if True:#(((MACD_signal_cross_1M_sell['signal'] == 'sell') | (MACD_signal_cross_1M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_1M_sell['index'] >= 975)):
								print('sell tarkibi finished')
								flag_cross_5M = 'sell'

			if ((((MACD_signal_cross_30M_sell['signal'] == 'buy') | (MACD_signal_cross_30M_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_sell['index'] > 993))):
				flag_cross_5M = 'failed'
				print('sell tarkibi failed')
						
		except:
			print('signal problem 5M SELL MACD!!!')

		try:

			if (((MACD_signal_cross_1H_buy['signal'] == 'buya') & True#(TsKs_signal_cross_1H_buy['signal'] == 'buy')
				& (MACD_signal_cross_1H_buy['index']>=497) 
				& ((macd_1H_buy[len(macd_1H_buy)-1]<=data_macd_1H_buy['diff_minus']) & (macds_1H_buy[len(macd_1H_buy)-1]<=data_macd_1H_buy['diff_minus']) ))):
				if ((macd_1D_buy[len(macd_1D_buy)-1] <= (data_macd_1D_buy['diff_minus']/2)) & (macds_1D_buy[len(macd_30M_buy)-1] <= (data_macd_1D_buy['diff_minus']/2))):
					if ((macd_1D_buy[len(macd_1D_buy)-1] >= macd_1D_buy[len(macd_1D_buy)-2]) & (macds_1D_buy[len(macds_1D_buy)-1] >= macds_1D_buy[len(macds_1D_buy)-2])
						| ((macd_1D_buy[len(macd_1D_buy)-1] >= macd_1D_buy[len(macd_1D_buy)-2]) & (macds_1D_buy[len(macds_1D_buy)-1] <= macds_1D_buy[len(macds_1D_buy)-2])) ):

						if (((MACD_signal_cross_1M_buy['signal'] == 'buy')) & (MACD_signal_cross_1M_buy['index'] >= 962)):
							if (((MACD_signal_cross_5M_buy['signal'] == 'buy')) & (MACD_signal_cross_5M_buy['index'] >= 982)):
								flag_cross_1H = 'buy'

						if ((((MACD_signal_cross_1D_buy['signal'] == 'sell') | (MACD_signal_cross_1D_buy['signal'] == 'faild_sell')) & (MACD_signal_cross_1D_buy['index'] > 493))):
							flag_cross_1H = 'failed'
						
		except:
			print('signal problem 1H BUY MACD!!!')

		try:

			if (((MACD_signal_cross_1H_sell['signal'] == 'sella') & True#(TsKs_signal_cross_1H_sell['signal'] == 'sell')
				& (MACD_signal_cross_1H_sell['index']>=497) 
				& ((macd_1H_sell[len(macd_1H_sell)-1]>=data_macd_1H_sell['diff_plus']) & (macds_1H_sell[len(macd_1H_sell)-1]>=data_macd_1H_sell['diff_plus']) ))):
				if ((macd_1D_sell[len(macd_1D_sell)-1] >= (data_macd_1D_sell['diff_plus']/2)) & (macds_1D_sell[len(macd_1D_sell)-1] >= (data_macd_1D_sell['diff_plus']/2))):
					if ((macd_1D_sell[len(macd_1D_sell)-1] <= macd_1D_sell[len(macd_1D_sell)-2]) & (macds_1D_sell[len(macds_1D_sell)-1] <= macds_1D_sell[len(macds_1D_sell)-2])
						| ((macd_1D_sell[len(macd_1D_sell)-1] <= macd_1D_sell[len(macd_1D_sell)-2]) & (macds_1D_sell[len(macds_1D_sell)-1] >= macds_1D_sell[len(macds_1D_sell)-2])) ):

						if (((MACD_signal_cross_1M_sell['signal'] == 'sell')) & (MACD_signal_cross_1M_sell['index'] >= 962)):
							if(((MACD_signal_cross_5M_sell['signal'] == 'sell')) & (MACD_signal_cross_5M_sell['index'] >= 982)):
								flag_cross_1H = 'sell'

						if ((((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] > 493))):
							flag_cross_1H = 'failed'
						
		except:
			print('signal problem 1H SELL MACD!!!')

		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#print(flag_cross_1H,flag_cross_30M,flag_cross_5M)

		account_count = 1000

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal Porro ********************************************************')

			if (flag_cross_porro == 'buy'):

				if True:
					
					while account_count <= 1001:

						log_multi_account(account_count)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')
					#continue

						if (flag_cross_porro == 'buy'):
							comment = 'nporro gen MACDCross'



						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	

							if (flag_cross_porro == 'buy'):
								tp_buy = (price + ((((abs(data_macd_porro_buy['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_macd_porro_buy['st'])) + spred + 0.5) * price)/100))#(tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']] - ((0.05 * tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_macd_porro_buy['score']/1000))

							if (tp_buy <= 0): break
	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						
							lot = float("{:.2f}".format((lot) * 10))

							if (lot >= 0.1):
								lot = 0.1

							if ((vol_traded + lot) >= vol_traded_max): break

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
							print('request failed Porro Trade MACD')
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
										print('send Done Porro Trade MACD!!!')
						except:
							print('some thing wrong send Porro Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_porro == 'sell'):
				
					

					while account_count <= 1001:
						log_multi_account(account_count)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
								print('same sell')
					#continue

						if (flag_cross_porro == 'sell'):
							comment = 'nporro gen MACDCross'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue


							if (flag_cross_porro == 'sell'):
								tp_sell = (price - ((((abs(data_macd_porro_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_macd_porro_sell['st'])) + spred + 0.5) * price)/100))#(tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']] + ((0.05 * tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_macd_porro_sell['score']/1000))

							if (tp_sell <= 0): break

							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot) * 10))

							if (lot >= 0.1):
								lot = 0.1

							if ((vol_traded + lot) >= vol_traded_max): break

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
							print('request failed Porro Trade MACD')
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
										print('send Done Porro Trade MACD!!!')
						except:
							print('some thing wrong send Porro Trade MACD')
							continue
		except:
			print('cant Play Porro Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************

		#************************************** 5M30M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal 5M30M ********************************************************')

			if (flag_cross_5M30M == 'buy'):

				if True:
					
					while account_count <= 1001:
						log_multi_account(account_count)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')
					#continue

						if (flag_cross_5M30M == 'buy'):
							comment = 'n5M30M gen MACDCross'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	

							if (flag_cross_5M30M == 'buy'):
								tp_buy = (price + ((((abs(data_macd_5M30M_buy['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_macd_5M30M_buy['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_5M30M_buy['score']/1000))
	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))



							if (lot >= 0.1):
								lot = 0.1

							if ((vol_traded + lot) >= vol_traded_max): break

						

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
							print('request failed 5M30M Trade MACD')
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
										print('send Done 5M30M Trade MACD!!!')
						except:
							print('some thing wrong send 5M30M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_5M30M == 'sell'):
				
					

					while account_count <= 1001:
						log_multi_account(account_count)
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
								print('same sell')
					#continue

						if (flag_cross_5M30M == 'sell'):
							comment = 'n5M30M gen MACDCross'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue


							if (flag_cross_5M30M == 'sell'):
								tp_sell = (price - ((((abs(data_macd_5M30M_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_macd_5M30M_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_5M30M_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))


							if (lot >= 0.1):
								lot = 0.1

							if ((vol_traded + lot) >= vol_traded_max): break

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
							print('request failed')
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
										print('send Done 5M30M Trade MACD!!!')
						except:
							print('some thing wrong send 5M30M Trade MACD')
							continue
		except:
			print('cant Play 5M30M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 1H *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal 1H ********************************************************')

			if ((flag_cross_1H == 'buy') & True):#(m >= 0) & (m <= 2)):

				if True:
					log_multi_account(1000)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')
					#continue

						if (flag_cross_1H == 'buy'):
							comment = '1H gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	


							if (flag_cross_1H == 'buy'):
								tp_buy = (price + ((((abs(data_macd_1H_sell['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_macd_1H_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_1H_buy['score']/1000))
	
							if (((abs(data_macd_1H_sell['tp'])) - spred) <= 0): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): 
								#print('lot = ',(vol_traded + lot))
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
							print('request failed 1H Trade MACD')
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
										print('send Done 1H Trade MACD!!!')
						except:
							print('some thing wrong send 1H Trade MACD')
							continue

			account_count = 1


			if ((flag_cross_1H == 'sell') & True):#(m >= 0) & (m <= 2)):
				
					log_multi_account(1000)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
								print('same sell')
					#continue

						if (flag_cross_1H == 'sell'):
							comment = '1H gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue

							if (flag_cross_1H == 'sell'):
								tp_sell = (price - ((((abs(data_macd_1H_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_macd_1H_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_1H_sell['score']/1000))

							if (((abs(data_macd_1H_sell['tp'])) - spred) <= 0): break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): 
								#print('lot = ',(vol_traded + lot))
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
							print('request failed 1H Trade MACD')
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
										print('send Done 1H Trade MACD!!!')
						except:
							print('some thing wrong send 1H Trade MACD')
							continue
		except:
			print('cant Play 1H Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		


		#************************************** 30M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal 30M ********************************************************')
			#print('30M MACD BUY = ',signal_cross_30M_buy)
			#print('30M MACD SELL = ',signal_cross_30M_sell)

			if ((flag_cross_30M == 'buy')):#(m%30 >= 0) & (m%30 <= 2)):

				if True:
					log_multi_account(1000)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)

					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')

					#continue

						if (flag_cross_30M == 'buy'):
							comment = '30M gen tarkibi'

						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	


							if (flag_cross_30M == 'buy'):
								tp_buy = (price + ((((abs(data_macd_30M_buy['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_macd_30M_buy['st'])) + spred + 0.5) * price)/100))#(tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']] - ((0.05 * tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))	
								lot = float("{:.2f}".format(data_macd_30M_buy['score']/1000))
								#print('********************************* Score = ',data_macd_30M_buy['score'],'************************************')
								#print('********************************* Lot = ',lot,'**************************************')
	
							if (((abs(data_macd_30M_buy['tp'])) - spred) <= 0): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						
							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): 
								#print('lot = ',(vol_traded + lot))
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
							print('request failed 30M Trade MACD')
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
										print('send Done 30M Trade MACD!!!')
						except:
							print('some thing wrong send 30M Trade MACD')
							continue

			account_count = 1


			if ((flag_cross_30M == 'sell')):#(m%30 >= 0) & (m%30 <= 2)):
				
					log_multi_account(1000)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
								print('same sell')
					#continue

						if (flag_cross_30M == 'sell'):
							comment = '30M gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue



							if (flag_cross_30M == 'sell'):
								tp_sell = (price - ((((abs(data_macd_30M_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_macd_30M_sell['st'])) + spred + 0.5) * price)/100))#(tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']] + ((0.05 * tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_macd_30M_sell['score']/1000))

							if (((abs(data_macd_30M_sell['tp'])) - spred) <= 0): break

							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))


							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): 
								#print('lot = ',(vol_traded + lot))
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
							print('request failed 30M Trade MACD')
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
										print('send Done 30M Trade MACD!!!')
						except:
							print('some thing wrong send 30M Trade MACD')
							continue
		except:
			print('cant Play 30M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 5M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal 5M ********************************************************')

			if (flag_cross_5M == 'buy'):

				if True:

					log_multi_account(1000)
					
					while account_count <= 1000:
						
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')
					#continue

						if (flag_cross_5M == 'buy'):
							comment = 'N5M gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	

							if (flag_cross_5M == 'buy'):
								tp_buy = (price + ((((abs(data_macd_5M_buy['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_macd_5M_buy['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_5M_buy['score']/1000))
	
							if (((abs(data_macd_5M_buy['tp'])) - spred) <= 0): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								print('No Money')
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
							print('request failed 5M Trade MACD')
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
										print('send Done 5M Trade MACD!!!')
						except:
							print('some thing wrong send 5M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_5M == 'sell'):
				
					


					log_multi_account(1000)
					while account_count <= 1000:
						
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								print('same sell')
								continue
								
					#continue
						if (flag_cross_5M == 'sell'):
							comment = 'N5M gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue

							
							if (flag_cross_5M == 'sell'):
								tp_sell = (price - ((((abs(data_macd_5M_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_macd_5M_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_5M_sell['score']/1000))

							if (((abs(data_macd_5M_sell['tp'])) - spred) <= 0): 
								#print(((abs(data_macd_5M_sell['tp'])) - spred))
								break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) > vol_traded_max): 
								print('No Money')
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
							print('request failed 5M Trade MACD')
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
										print('send Done 5M Trade MACD!!!')
						except:
							print('some thing wrong send 5M Trade MACD')
							continue
		except:
			print('cant Play 5M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		#************************************** 1M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1

		h,m,s,d = time_func()
		try:
			#print('**************************************** MACD Trade Signal 1M ********************************************************')

			if (flag_cross_1M == 'buy'):

				if True:
					log_multi_account(1000)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
								print('same buy')
					#continue

						if (flag_cross_1M == 'buy'):
							comment = 'N1M gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1	

							if (spred > 0.04):
								print("spred = ", spred)
								continue	

							if (flag_cross_1M == 'buy'):
								tp_buy = (price + ((((abs(data_macd_1M_buy['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_macd_1M_buy['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_1M_buy['score']/1000))
	
							if (((abs(data_macd_1M_buy['tp'])) - spred) <= 0): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): break

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
							print('request failed 1M Trade MACD')
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
										print('send Done 1M Trade MACD!!!')
						except:
							print('some thing wrong send 1M Trade MACD')
							continue

			account_count = 1


			if (flag_cross_1M == 'sell'):
				
					log_multi_account(1000)



					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
								vol_position = position[9]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								print('same sell')
								continue
								
					#continue
						if (flag_cross_1M == 'sell'):
							comment = 'N1M gen tarkibi'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = ((abs(price_ask-price_bid)/price_ask) * 100)
							deviation = 5
							magic += 1

							if (spred > 0.04):
								print("spred = ", spred)
								continue

							
							if (flag_cross_1M == 'sell'):
								tp_sell = (price - ((((abs(data_macd_1M_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_macd_1M_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_macd_1M_sell['score']/1000))

							if (((abs(data_macd_1M_sell['tp'])) - spred) <= 0): 
								#print(((abs(data_macd_5M_sell['tp'])) - spred))
								break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= vol_traded_max):
								lot = vol_traded_max

							if ((vol_traded + lot) >= vol_traded_max): 
								#print('lot = ',(vol_traded + lot))
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
							print('request failed 1M Trade MACD')
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
										print('send Done 1M Trade MACD!!!')
						except:
							print('some thing wrong send 1M Trade MACD')
							continue
		except:
			print('cant Play 1M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		

#trade_strategy_tarkibi(20)
