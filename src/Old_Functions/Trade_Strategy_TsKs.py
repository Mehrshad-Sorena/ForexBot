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
from multiprocessing import Process
import threading
from Accounts import *
from UTC_Time import *


def trade_strategy_TsKs():
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


	symbol_data_30M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
	symbol_data_1H,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,300)
	#symbol_data_D1,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,100)
	symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)
	#symbol_data_M1,my_money,symbols = log_get_data(mt5.TIMEFRAME_M1,1000)
	#print("money",my_money)
#print("symbol = ",symbols.name)

	#symbol_data = symbol_daind.append(symbol_data_local, ignore_index = True)	

#print(type(MACD(symbol_data['EURUSD']['open'],26,12,9,False) ))
	magic = time.time_ns()

	for sym in symbols:
		if (my_money == 0): break
		if (sym.name == 'EURDKK'): continue
#g = float("{:.2f}".format(x))
		
		#****************************** Data_Buy 5M TsKs *******************************************************************
		try:
			with open("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M_buy = line
					data_TsKs_5M_buy['tp'] = float(data_TsKs_5M_buy['tp'])
					data_TsKs_5M_buy['tp'] = (data_TsKs_5M_buy['tp']/3)*2

					data_TsKs_5M_buy['st'] = float(data_TsKs_5M_buy['st'])
					data_TsKs_5M_buy['kijun'] = float(data_TsKs_5M_buy['kijun'])
					data_TsKs_5M_buy['tenkan'] = float(data_TsKs_5M_buy['tenkan'])
					data_TsKs_5M_buy['snkou'] = float(data_TsKs_5M_buy['snkou'])
					data_TsKs_5M_buy['score'] = float(data_TsKs_5M_buy['score'])

		except:
			#continue
			data_TsKs_5M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 5M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M_sell = line
					data_TsKs_5M_sell['tp'] = float(data_TsKs_5M_sell['tp'])
					data_TsKs_5M_sell['tp'] = (data_TsKs_5M_sell['tp']/3)*2

					data_TsKs_5M_sell['st'] = float(data_TsKs_5M_sell['st'])
					data_TsKs_5M_sell['kijun'] = float(data_TsKs_5M_sell['kijun'])
					data_TsKs_5M_sell['tenkan'] = float(data_TsKs_5M_sell['tenkan'])
					data_TsKs_5M_sell['snkou'] = float(data_TsKs_5M_sell['snkou'])
					data_TsKs_5M_sell['score'] = float(data_TsKs_5M_sell['score'])

		except:
			#continue
			data_TsKs_5M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************
		
		#****************************** Data_Buy 30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_30M_buy = line
					data_TsKs_30M_buy['tp'] = float(data_TsKs_30M_buy['tp'])
					data_TsKs_30M_buy['tp'] = (data_TsKs_30M_buy['tp']/3)*2

					data_TsKs_30M_buy['st'] = float(data_TsKs_30M_buy['st'])
					data_TsKs_30M_buy['kijun'] = float(data_TsKs_30M_buy['kijun'])
					data_TsKs_30M_buy['tenkan'] = float(data_TsKs_30M_buy['tenkan'])
					data_TsKs_30M_buy['snkou'] = float(data_TsKs_30M_buy['snkou'])
					data_TsKs_30M_buy['score'] = float(data_TsKs_30M_buy['score'])
		except:
			#continue
			data_TsKs_30M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Sell 30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_30M_sell = line
					data_TsKs_30M_sell['tp'] = float(data_TsKs_30M_sell['tp'])
					data_TsKs_30M_sell['tp'] = (data_TsKs_30M_sell['tp']/3)*2

					data_TsKs_30M_sell['st'] = float(data_TsKs_30M_sell['st'])
					data_TsKs_30M_sell['kijun'] = float(data_TsKs_30M_sell['kijun'])
					data_TsKs_30M_sell['tenkan'] = float(data_TsKs_30M_sell['tenkan'])
					data_TsKs_30M_sell['snkou'] = float(data_TsKs_30M_sell['snkou'])
					data_TsKs_30M_sell['score'] = float(data_TsKs_30M_sell['score'])
		except:
			#continue
			data_TsKs_30M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}



		#******************************//////////////////////***********************************************************

		#****************************** Data_Buy 1H TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_1H_buy = line
					data_TsKs_1H_buy['tp'] = float(data_TsKs_1H_buy['tp'])
					data_TsKs_1H_buy['tp'] = (data_TsKs_1H_buy['tp']/3)*2

					data_TsKs_1H_buy['st'] = float(data_TsKs_1H_buy['st'])
					data_TsKs_1H_buy['kijun'] = float(data_TsKs_1H_buy['kijun'])
					data_TsKs_1H_buy['tenkan'] = float(data_TsKs_1H_buy['tenkan'])
					data_TsKs_1H_buy['snkou'] = float(data_TsKs_1H_buy['snkou'])
					data_TsKs_1H_buy['score'] = float(data_TsKs_1H_buy['score'])


		except:
			#continue
			data_TsKs_1H_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 1H TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_1H_sell = line
					data_TsKs_1H_sell['tp'] = float(data_TsKs_1H_sell['tp'])
					data_TsKs_1H_sell['tp'] = (data_TsKs_1H_sell['tp']/3)*2

					data_TsKs_1H_sell['st'] = float(data_TsKs_1H_sell['st'])
					data_TsKs_1H_sell['kijun'] = float(data_TsKs_1H_sell['kijun'])
					data_TsKs_1H_sell['tenkan'] = float(data_TsKs_1H_sell['tenkan'])
					data_TsKs_1H_sell['snkou'] = float(data_TsKs_1H_sell['snkou'])
					data_TsKs_1H_sell['score'] = float(data_TsKs_1H_sell['score'])


		except:
			#continue
			data_TsKs_1H_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 8 , 'tenkan': 18, 'snkou': 6
			,'score': 0}


		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 5M30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M30M_buy = line
					data_TsKs_5M30M_buy['tp'] = float(data_TsKs_5M30M_buy['tp'])
					data_TsKs_5M30M_buy['tp'] = (data_TsKs_5M30M_buy['tp']/3)*2

					data_TsKs_5M30M_buy['st'] = float(data_TsKs_5M30M_buy['st'])
					data_TsKs_5M30M_buy['kijun5M'] = float(data_TsKs_5M30M_buy['kijun5M'])
					data_TsKs_5M30M_buy['tenkan5M'] = float(data_TsKs_5M30M_buy['tenkan5M'])
					data_TsKs_5M30M_buy['snkou5M'] = float(data_TsKs_5M30M_buy['snkou5M'])
					data_TsKs_5M30M_buy['kijun30M'] = float(data_TsKs_5M30M_buy['kijun30M'])
					data_TsKs_5M30M_buy['tenkan30M'] = float(data_TsKs_5M30M_buy['tenkan30M'])
					data_TsKs_5M30M_buy['snkou30M'] = float(data_TsKs_5M30M_buy['snkou30M'])
					data_TsKs_5M30M_buy['score'] = float(data_TsKs_5M30M_buy['score'])

					if(data_TsKs_5M30M_buy['score'] < 90):
						data_TsKs_5M30M_buy['score'] = data_TsKs_5M30M_buy['score']/10

		except:
			#continue
			data_TsKs_5M30M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 8 , 'tenkan5M': 18, 'snkou5M': 6,'kijun30M': 8 , 'tenkan30M': 18, 'snkou30M': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 5M30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M30M_sell = line
					data_TsKs_5M30M_sell['tp'] = float(data_TsKs_5M30M_sell['tp'])
					data_TsKs_5M30M_sell['tp'] = (data_TsKs_5M30M_sell['tp']/3)*2

					data_TsKs_5M30M_sell['st'] = float(data_TsKs_5M30M_sell['st'])
					data_TsKs_5M30M_sell['kijun5M'] = float(data_TsKs_5M30M_sell['kijun5M'])
					data_TsKs_5M30M_sell['tenkan5M'] = float(data_TsKs_5M30M_sell['tenkan5M'])
					data_TsKs_5M30M_sell['snkou5M'] = float(data_TsKs_5M30M_sell['snkou5M'])
					data_TsKs_5M30M_sell['kijun30M'] = float(data_TsKs_5M30M_sell['kijun30M'])
					data_TsKs_5M30M_sell['tenkan30M'] = float(data_TsKs_5M30M_sell['tenkan30M'])
					data_TsKs_5M30M_sell['snkou30M'] = float(data_TsKs_5M30M_sell['snkou30M'])
					data_TsKs_5M30M_sell['score'] = float(data_TsKs_5M30M_sell['score'])

					if(data_TsKs_5M30M_sell['score'] < 90):
						data_TsKs_5M30M_sell['score'] = data_TsKs_5M30M_sell['score']/10

		except:
			#continue
			data_TsKs_5M30M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 8 , 'tenkan5M': 18, 'snkou5M': 6,'kijun30M': 8 , 'tenkan30M': 18, 'snkou30M': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy porro TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_porro_buy = line
					data_TsKs_porro_buy['tp'] = float(data_TsKs_porro_buy['tp'])
					data_TsKs_porro_buy['tp'] = (data_TsKs_porro_buy['tp']/3)*2

					data_TsKs_porro_buy['st'] = float(data_TsKs_porro_buy['st'])
					data_TsKs_porro_buy['kijun5M'] = float(data_TsKs_porro_buy['kijun5M'])
					data_TsKs_porro_buy['tenkan5M'] = float(data_TsKs_porro_buy['tenkan5M'])
					data_TsKs_porro_buy['snkou5M'] = float(data_TsKs_porro_buy['snkou5M'])
					data_TsKs_porro_buy['kijun30M'] = float(data_TsKs_porro_buy['kijun30M'])
					data_TsKs_porro_buy['tenkan30M'] = float(data_TsKs_porro_buy['tenkan30M'])
					data_TsKs_porro_buy['snkou30M'] = float(data_TsKs_porro_buy['snkou30M'])
					data_TsKs_porro_buy['kijun1H'] = float(data_TsKs_porro_buy['kijun1H'])
					data_TsKs_porro_buy['tenkan1H'] = float(data_TsKs_porro_buy['tenkan1H'])
					data_TsKs_porro_buy['snkou1H'] = float(data_TsKs_porro_buy['snkou1H'])
					data_TsKs_porro_buy['score'] = float(data_TsKs_porro_buy['score'])

					if(data_TsKs_porro_buy['score'] < 90):
						data_TsKs_porro_buy['score'] = data_TsKs_porro_buy['score']/10

		except:
			#continue
			data_TsKs_porro_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 8 , 'tenkan5M': 18, 'snkou5M': 6,'kijun30M': 8 , 'tenkan30M': 18, 'snkou30M': 6,'kijun1H': 8 , 'tenkan1H': 18, 'snkou1H': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell porro TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_porro_sell = line
					data_TsKs_porro_sell['tp'] = float(data_TsKs_porro_sell['tp'])
					data_TsKs_porro_sell['tp'] = (data_TsKs_porro_sell['tp']/3)*2
					
					data_TsKs_porro_sell['st'] = float(data_TsKs_porro_sell['st'])
					data_TsKs_porro_sell['kijun5M'] = float(data_TsKs_porro_sell['kijun5M'])
					data_TsKs_porro_sell['tenkan5M'] = float(data_TsKs_porro_sell['tenkan5M'])
					data_TsKs_porro_sell['snkou5M'] = float(data_TsKs_porro_sell['snkou5M'])
					data_TsKs_porro_sell['kijun30M'] = float(data_TsKs_porro_sell['kijun30M'])
					data_TsKs_porro_sell['tenkan30M'] = float(data_TsKs_porro_sell['tenkan30M'])
					data_TsKs_porro_sell['snkou30M'] = float(data_TsKs_porro_sell['snkou30M'])
					data_TsKs_porro_sell['kijun1H'] = float(data_TsKs_porro_sell['kijun1H'])
					data_TsKs_porro_sell['tenkan1H'] = float(data_TsKs_porro_sell['tenkan1H'])
					data_TsKs_porro_sell['snkou1H'] = float(data_TsKs_porro_sell['snkou1H'])
					data_TsKs_porro_sell['score'] = float(data_TsKs_porro_sell['score'])

					if(data_TsKs_porro_sell['score'] < 90):
						data_TsKs_porro_sell['score'] = data_TsKs_porro_sell['score']/10

		except:
			#continue
			data_TsKs_porro_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 8 , 'tenkan5M': 18, 'snkou5M': 6,'kijun30M': 8 , 'tenkan30M': 18, 'snkou30M': 6,'kijun1H': 8 , 'tenkan1H': 18, 'snkou1H': 6
			,'score': 0}

		#******************************//////////////////////***********************************************************

		symbol_data_30M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
		symbol_data_H1,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,300)
		#symbol_data_D1,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,100)
		symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)

	#help(ind.macd)
		try:
			# *******************++++++++++++ TSKS Buy 30M************************************************************
			ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_30M_buy['tenkan'],kijun=data_TsKs_30M_buy['kijun'],snkou=data_TsKs_30M_buy['snkou'])
			SPANA_30M_buy = ichi_30M[0][ichi_30M[0].columns[0]]
			SPANB_30M_buy = ichi_30M[0][ichi_30M[0].columns[1]]
			tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]]
			kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]]
			chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

			signal_cross_30M_buy = {}
			signal_cross_30M_buy = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('30M Buy TsKs Wrong!!')

		try:

			# *******************++++++++++++ TSKS Sell 30M************************************************************

			ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_30M_sell['tenkan'],kijun=data_TsKs_30M_sell['kijun'],snkou=data_TsKs_30M_sell['snkou'])
			SPANA_30M_sell = ichi_30M[0][ichi_30M[0].columns[0]]
			SPANB_30M_sell = ichi_30M[0][ichi_30M[0].columns[1]]
			tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]]
			kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]]
			chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

			signal_cross_30M_sell = {}
			signal_cross_30M_sell = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************
		except:
			print('30M Sell TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************

			ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M_buy['tenkan'],kijun=data_TsKs_5M_buy['kijun'],snkou=data_TsKs_5M_buy['snkou'])
			SPANA_5M_buy = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M_buy = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			signal_cross_5M_buy = {}
			signal_cross_5M_buy = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Sell 5M************************************************************

			ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M_sell['tenkan'],kijun=data_TsKs_5M_sell['kijun'],snkou=data_TsKs_5M_sell['snkou'])
			SPANA_5M_sell = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M_sell = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			signal_cross_5M_sell = {}
			signal_cross_5M_sell = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Sell TsKs Wrong!!')
			

		try:
			# *******************++++++++++++ TSKS Buy 1H************************************************************

			ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_1H_buy['tenkan'],kijun=data_TsKs_1H_buy['kijun'],snkou=data_TsKs_1H_buy['snkou'])
			SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
			SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
			tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]]
			kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]]
			chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

			signal_cross_1H_buy = {}
			signal_cross_1H_buy = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1H Buy TsKs Wrong!!')



		try:
			# *******************++++++++++++ TSKS Sell 1H************************************************************

			ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_1H_sell['tenkan'],kijun=data_TsKs_1H_sell['kijun'],snkou=data_TsKs_1H_sell['snkou'])
			SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
			SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
			tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]]
			kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]]
			chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

			signal_cross_1H_sell = {}
			signal_cross_1H_sell = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

			#*********************---------------------*************/////////////*************************************************
			#print(macd_5M)
			#print(len(macd_5M))
		except:
			print('1H Sell TsKs Wrong!!')


		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#********************************************* 5M30M BUY TSKS ******************************************************************
		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************
			ichi_5M30M_buy_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_buy['tenkan5M'],kijun=data_TsKs_5M30M_buy['kijun5M'],snkou=data_TsKs_5M30M_buy['snkou5M'])
			SPANA_5M30M_buy_5M = ichi_5M30M_buy_5M[0][ichi_5M30M_buy_5M[0].columns[0]]
			SPANB_5M30M_buy_5M = ichi_5M30M_buy_5M[0][ichi_5M30M_buy_5M[0].columns[1]]
			tenkan_5M30M_buy_5M = ichi_5M30M_buy_5M[0][ichi_5M30M_buy_5M[0].columns[2]]
			kijun_5M30M_buy_5M = ichi_5M30M_buy_5M[0][ichi_5M30M_buy_5M[0].columns[3]]
			chikospan_5M30M_buy_5M = ichi_5M30M_buy_5M[0][ichi_5M30M_buy_5M[0].columns[4]]

			signal_cross_5M30M_buy_5M = {}
			signal_cross_5M30M_buy_5M = cross_TsKs_Buy_signal(tenkan_5M30M_buy_5M,kijun_5M30M_buy_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M30M 5M Buy TsKs Wrong!!')

		try:
			# *******************++++++++++++ TSKS Buy 30M************************************************************

			ichi_5M30M_buy_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_buy['tenkan30M'],kijun=data_TsKs_5M30M_buy['kijun30M'],snkou=data_TsKs_5M30M_buy['snkou30M'])
			SPANA_5M30M_buy_30M = ichi_5M30M_buy_30M[0][ichi_5M30M_buy_30M[0].columns[0]]
			SPANB_5M30M_buy_30M = ichi_5M30M_buy_30M[0][ichi_5M30M_buy_30M[0].columns[1]]
			tenkan_5M30M_buy_30M = ichi_5M30M_buy_30M[0][ichi_5M30M_buy_30M[0].columns[2]]
			kijun_5M30M_buy_30M = ichi_5M30M_buy_30M[0][ichi_5M30M_buy_30M[0].columns[3]]
			chikospan_5M30M_buy_30M = ichi_5M30M_buy_30M[0][ichi_5M30M_buy_30M[0].columns[4]]

			signal_cross_5M30M_buy_30M = {}
			signal_cross_5M30M_buy_30M = cross_TsKs_Buy_signal(tenkan_5M30M_buy_30M,kijun_5M30M_buy_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M30M 30M Buy TsKs Wrong!!')
		#********************************************///////////////////****************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

		#********************************************* 5M30M SELL TSKS ******************************************************************
		try:

			# *******************++++++++++++ TSKS sell 5M************************************************************

			ichi_5M30M_sell_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_sell['tenkan5M'],kijun=data_TsKs_5M30M_sell['kijun5M'],snkou=data_TsKs_5M30M_sell['snkou5M'])
			SPANA_5M30M_sell_5M = ichi_5M30M_sell_5M[0][ichi_5M30M_sell_5M[0].columns[0]]
			SPANB_5M30M_sell_5M = ichi_5M30M_sell_5M[0][ichi_5M30M_sell_5M[0].columns[1]]
			tenkan_5M30M_sell_5M = ichi_5M30M_sell_5M[0][ichi_5M30M_sell_5M[0].columns[2]]
			kijun_5M30M_sell_5M = ichi_5M30M_sell_5M[0][ichi_5M30M_sell_5M[0].columns[3]]
			chikospan_5M30M_sell_5M = ichi_5M30M_sell_5M[0][ichi_5M30M_sell_5M[0].columns[4]]

			signal_cross_5M30M_sell_5M = {}
			signal_cross_5M30M_sell_5M = cross_TsKs_Buy_signal(tenkan_5M30M_sell_5M,kijun_5M30M_sell_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M30M 5M sell TsKs Wrong!!')

		try:

			# *******************++++++++++++ TSKS Sell 30M************************************************************

			ichi_5M30M_sell_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_sell['tenkan30M'],kijun=data_TsKs_5M30M_sell['kijun30M'],snkou=data_TsKs_5M30M_sell['snkou30M'])
			SPANA_5M30M_sell_30M = ichi_5M30M_sell_30M[0][ichi_5M30M_sell_30M[0].columns[0]]
			SPANB_5M30M_sell_30M = ichi_5M30M_sell_30M[0][ichi_5M30M_sell_30M[0].columns[1]]
			tenkan_5M30M_sell_30M = ichi_5M30M_sell_30M[0][ichi_5M30M_sell_30M[0].columns[2]]
			kijun_5M30M_sell_30M = ichi_5M30M_sell_30M[0][ichi_5M30M_sell_30M[0].columns[3]]
			chikospan_5M30M_sell_30M = ichi_5M30M_sell_30M[0][ichi_5M30M_sell_30M[0].columns[4]]

			signal_cross_5M30M_sell_30M = {}
			signal_cross_5M30M_sell_30M = cross_TsKs_Buy_signal(tenkan_5M30M_sell_30M,kijun_5M30M_sell_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************
		except:
			print('5M30M 30M Sell TsKs Wrong!!')

		#********************************************///////////////////****************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#********************************************* Porro BUY TSKS ******************************************************************

		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************
			ichi_porro_buy_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_porro_buy['tenkan5M'],kijun=data_TsKs_porro_buy['kijun5M'],snkou=data_TsKs_porro_buy['snkou5M'])
			SPANA_porro_buy_5M = ichi_porro_buy_5M[0][ichi_porro_buy_5M[0].columns[0]]
			SPANB_porro_buy_5M = ichi_porro_buy_5M[0][ichi_porro_buy_5M[0].columns[1]]
			tenkan_porro_buy_5M = ichi_porro_buy_5M[0][ichi_porro_buy_5M[0].columns[2]]
			kijun_porro_buy_5M = ichi_porro_buy_5M[0][ichi_porro_buy_5M[0].columns[3]]
			chikospan_porro_buy_5M = ichi_porro_buy_5M[0][ichi_porro_buy_5M[0].columns[4]]

			signal_cross_porro_buy_5M = {}
			signal_cross_porro_buy_5M = cross_TsKs_Buy_signal(tenkan_porro_buy_5M,kijun_porro_buy_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('Porro 5M Buy TsKs Wrong!!')

		try:
			# *******************++++++++++++ TSKS Buy 30M************************************************************

			ichi_porro_buy_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_porro_buy['tenkan30M'],kijun=data_TsKs_porro_buy['kijun30M'],snkou=data_TsKs_porro_buy['snkou30M'])
			SPANA_porro_buy_30M = ichi_porro_buy_30M[0][ichi_porro_buy_30M[0].columns[0]]
			SPANB_porro_buy_30M = ichi_porro_buy_30M[0][ichi_porro_buy_30M[0].columns[1]]
			tenkan_porro_buy_30M = ichi_porro_buy_30M[0][ichi_porro_buy_30M[0].columns[2]]
			kijun_porro_buy_30M = ichi_porro_buy_30M[0][ichi_porro_buy_30M[0].columns[3]]
			chikospan_porro_buy_30M = ichi_porro_buy_30M[0][ichi_porro_buy_30M[0].columns[4]]

			signal_cross_porro_buy_30M = {}
			signal_cross_porro_buy_30M = cross_TsKs_Buy_signal(tenkan_porro_buy_30M,kijun_porro_buy_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('Porro 30M Buy TsKs Wrong!!')

		try:
			# *******************++++++++++++ TSKS Buy 1H************************************************************

			ichi_porro_buy_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_porro_buy['tenkan1H'],kijun=data_TsKs_porro_buy['kijun1H'],snkou=data_TsKs_porro_buy['snkou1H'])
			SPANA_porro_buy_1H = ichi_porro_buy_1H[0][ichi_porro_buy_1H[0].columns[0]]
			SPANB_porro_buy_1H = ichi_porro_buy_1H[0][ichi_porro_buy_1H[0].columns[1]]
			tenkan_porro_buy_1H = ichi_porro_buy_1H[0][ichi_porro_buy_1H[0].columns[2]]
			kijun_porro_buy_1H = ichi_porro_buy_1H[0][ichi_porro_buy_1H[0].columns[3]]
			chikospan_porro_buy_1H = ichi_porro_buy_1H[0][ichi_porro_buy_1H[0].columns[4]]

			signal_cross_porro_buy_1H = {}
			signal_cross_porro_buy_1H = cross_TsKs_Buy_signal(tenkan_porro_buy_1H,kijun_porro_buy_1H,sym.name)
			#*********************---------------------*************/////////////*************************************************

		except:
			print('Porro 1H Buy TsKs Wrong!!')

		#********************************************///////////////////****************************************************************
		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



		#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		#********************************************* Porro SELL TSKS ******************************************************************
		try:

			# *******************++++++++++++ TSKS sell 5M************************************************************

			ichi_porro_sell_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_porro_sell['tenkan5M'],kijun=data_TsKs_porro_sell['kijun5M'],snkou=data_TsKs_porro_sell['snkou5M'])
			SPANA_porro_sell_5M = ichi_porro_sell_5M[0][ichi_porro_sell_5M[0].columns[0]]
			SPANB_porro_sell_5M = ichi_porro_sell_5M[0][ichi_porro_sell_5M[0].columns[1]]
			tenkan_porro_sell_5M = ichi_porro_sell_5M[0][ichi_porro_sell_5M[0].columns[2]]
			kijun_porro_sell_5M = ichi_porro_sell_5M[0][ichi_porro_sell_5M[0].columns[3]]
			chikospan_porro_sell_5M = ichi_porro_sell_5M[0][ichi_porro_sell_5M[0].columns[4]]

			signal_cross_porro_sell_5M = {}
			signal_cross_porro_sell_5M = cross_TsKs_Buy_signal(tenkan_porro_sell_5M,kijun_porro_sell_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('porro 5M sell TsKs Wrong!!')

		try:

			# *******************++++++++++++ TSKS Sell 30M************************************************************

			ichi_porro_sell_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_porro_sell['tenkan30M'],kijun=data_TsKs_porro_sell['kijun30M'],snkou=data_TsKs_porro_sell['snkou30M'])
			SPANA_porro_sell_30M = ichi_porro_sell_30M[0][ichi_porro_sell_30M[0].columns[0]]
			SPANB_porro_sell_30M = ichi_porro_sell_30M[0][ichi_porro_sell_30M[0].columns[1]]
			tenkan_porro_sell_30M = ichi_porro_sell_30M[0][ichi_porro_sell_30M[0].columns[2]]
			kijun_porro_sell_30M = ichi_porro_sell_30M[0][ichi_porro_sell_30M[0].columns[3]]
			chikospan_porro_sell_30M = ichi_porro_sell_30M[0][ichi_porro_sell_30M[0].columns[4]]

			signal_cross_porro_sell_30M = {}
			signal_cross_porro_sell_30M = cross_TsKs_Buy_signal(tenkan_porro_sell_30M,kijun_porro_sell_30M,sym.name)

			#*********************---------------------*************/////////////*************************************************
		except:
			print('porro 30M Sell TsKs Wrong!!')

		try:
			# *******************++++++++++++ TSKS Buy 1H************************************************************

			# *******************++++++++++++ TSKS Sell 1H************************************************************

			ichi_porro_sell_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_porro_sell['tenkan1H'],kijun=data_TsKs_porro_sell['kijun1H'],snkou=data_TsKs_porro_sell['snkou1H'])
			SPANA_porro_sell_1H = ichi_porro_sell_1H[0][ichi_porro_sell_1H[0].columns[0]]
			SPANB_porro_sell_1H = ichi_porro_sell_1H[0][ichi_porro_sell_1H[0].columns[1]]
			tenkan_porro_sell_1H = ichi_porro_sell_1H[0][ichi_porro_sell_1H[0].columns[2]]
			kijun_porro_sell_1H = ichi_porro_sell_1H[0][ichi_porro_sell_1H[0].columns[3]]
			chikospan_porro_sell_1H = ichi_porro_sell_1H[0][ichi_porro_sell_1H[0].columns[4]]

			signal_cross_porro_sell_1H = {}
			signal_cross_porro_sell_1H = cross_TsKs_Buy_signal(tenkan_porro_sell_1H,kijun_porro_sell_1H,sym.name)

		except:
			print('Porro 1H sell TsKs Wrong!!')


		#********************************************///////////////////****************************************************************
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
		flag_cross_1H = ''
		flag_cross_porro = ''
		flag_cross_5M30M = ''

		try:
			#print(sym.name)

			if (((signal_cross_30M_buy['signal'] == 'buy') & (signal_cross_30M_buy['index']>=994))
				& (signal_cross_30M_sell['signal'] != 'sell')):
				flag_cross_30M = 'sell'
		except:
			print('signal problem 30M Buy TSKS!!!')


		try:

			if (((signal_cross_30M_sell['signal'] == 'sell') & (signal_cross_30M_sell['index']>=994))
				& (signal_cross_30M_buy['signal'] != 'buy')):
				flag_cross_30M = 'buy'
		except:
			print('signal problem 30M Sell TSKS!!!')


		try:

			if (((signal_cross_5M_buy['signal'] == 'buy') & (signal_cross_5M_buy['index']>=994))
				& (signal_cross_5M_sell['signal'] != 'sell')):
				flag_cross_5M = 'sell'

		except:
			print('signal problem 5M Buy TSKS!!!')


		try:

			if (((signal_cross_5M_sell['signal'] == 'sell') & (signal_cross_5M_sell['index']>=994))
				& (signal_cross_5M_buy['signal'] != 'buy')):
				flag_cross_5M = 'buy'
		except:
			print('signal problem 5M Sell TSKS!!!')

		try:

			if (((signal_cross_1H_buy['signal'] == 'buy') & (signal_cross_1H_buy['index']>=994))
				& (signal_cross_1H_sell['signal'] != 'sell')):
				flag_cross_1H = 'sell'
		except:
			print('signal problem 1H Buy TSKS!!!')

		try:

			if (((signal_cross_1H_sell['signal'] == 'sell') & (signal_cross_1H_sell['index']>=994))
				& (signal_cross_1H_buy['signal'] != 'buy')):
				flag_cross_1H = 'buy'
		except:
			print('signal problem 1H Sell TSKS!!!')

		try:

			if ((signal_cross_5M30M_buy_5M['signal'] == 'buy') & (signal_cross_5M30M_buy_5M['index']>=994)
				& (signal_cross_5M30M_buy_30M['signal'] == 'buy') & (signal_cross_5M30M_buy_30M['index']>=994)):
				flag_cross_5M30M = 'sell'
		except:
			print('signal problem 5M30M Buy TSKS!!!')

		try:

			if ((signal_cross_5M30M_sell_5M['signal'] == 'sell') & (signal_cross_5M30M_sell_5M['index']>=994)
				& (signal_cross_5M30M_sell_30M['signal'] == 'sell') & (signal_cross_5M30M_sell_30M['index']>=994)):
				flag_cross_5M30M = 'buy'
		except:
			print('signal problem 5M30M Sell TSKS!!!')

		try:

			if ((signal_cross_porro_buy_5M['signal'] == 'buy') & (signal_cross_porro_buy_5M['index']>=994)
				& (signal_cross_porro_buy_30M['signal'] == 'buy') & (signal_cross_porro_buy_1H['signal'] == 'buy')):
				flag_cross_porro = 'sell'
		except:
			print('signal problem Porro Buy TSKS!!!')

		try:

			if ((signal_cross_porro_sell_5M['signal'] == 'sell') & (signal_cross_porro_sell_5M['index']>=994)
				& (signal_cross_porro_sell_30M['signal'] == 'sell') & (signal_cross_porro_sell_1H['signal'] == 'sell')):
				flag_cross_porro = 'buy'
		except:
			print('signal problem Porro Sell TSKS!!!')

		account_count = 1

		#******************************************* Trade Porro **************************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		h,m,s = time_func()
		try:
			#print('**************************************** TsKs Trade Porro ********************************************************')

			if (flag_cross_porro == 'buy'):

				if True:
					log_multi_account(7)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
					#continue

						if (flag_cross_porro == 'buy'):
							comment = 'nporro gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1	

							if (spred > 0.06):
								print("spred = ", spred)
								continue	


							if (flag_cross_porro == 'buy'):
								tp_buy = (price + ((((abs(data_TsKs_porro_buy['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_TsKs_porro_buy['st'])) + spred) * price)/100))#(tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']] - ((0.05 * tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_porro_buy['score']/1000))
	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

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
							print('request failed Porro TSKS Trade')
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
										print('send Done Porro TSKS Trade!!!')
						except:
							print('some thing wrong send Porro TSKS Trade')
							continue

			account_count = 1


			if (flag_cross_porro == 'sell'):
				
					log_multi_account(7)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
					#continue

						if (flag_cross_porro == 'sell'):
							comment = 'nporro gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1

							if (spred > 0.06):
								print("spred = ", spred)
								continue


							if (flag_cross_porro == 'sell'):
								tp_sell = (price - ((((abs(data_TsKs_porro_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_TsKs_porro_sell['st'])) + spred) * price)/100))#(tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']] + ((0.05 * tenkan_5M[chiko_sig_5M[sym.name][len(chiko_sig_5M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_porro_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

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
							print('request failed Porro TSKS Trade')
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
										print('send Done Porro TSKS Trade!!!')
						except:
							print('some thing wrong send Porro TSKS Trade')
							continue
		except:
			print('cant Play Porro TSKS Trade!!!')
		#**************************************************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#******************************************* Trade 5M30M **************************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		h,m,s = time_func()
		try:
			#print('**************************************** TsKs Trade Signal 5M30M ********************************************************')

			if (flag_cross_5M30M == 'buy'):

				if True:
					log_multi_account(7)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
					#continue

						if (flag_cross_5M30M == 'buy'):
							comment = 'n5M30M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1	

							if (spred > 0.06):
								print("spred = ", spred)
								continue	


							if (flag_cross_5M30M == 'buy'):
								tp_buy = (price + ((((abs(data_TsKs_5M30M_buy['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_TsKs_5M30M_buy['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_5M30M_buy['score']/1000))


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

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
							print('request failed 5M30M TSKS Trade')
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
										print('send Done 5M30M TSKS Trade!!!')
						except:
							print('some thing wrong send 5M30M TSKS Trade')
							continue

			account_count = 1


			if (flag_cross_5M30M == 'sell'):
				
					log_multi_account(7)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
					#continue

						if (flag_cross_5M30M == 'sell'):
							comment = 'n5M30M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1

							if (spred > 0.06):
								print("spred = ", spred)
								continue


							if (flag_cross_5M30M == 'sell'):
								tp_sell = (price - ((((abs(data_TsKs_5M30M_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_TsKs_5M30M_sell['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_5M30M_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

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
							print('request failed 5M30M TSKS Trade')
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
										print('send Done!!!')
						except:
							print('some thing wrong send 5M30M TSKS Trade')
							continue
		except:
			print('cant Play 5M30M TSKS Trade!!!')
		#**************************************************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#******************************************* Trade 1H **************************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		h,m,s = time_func()
		try:
			#print('**************************************** TsKs Trade Signal 1H ********************************************************')
			#print('1H TsKs BUY = ',signal_cross_1H_buy)

			#print('1H TsKs SELL = ',signal_cross_1H_sell)

			if ((flag_cross_1H == 'buy') & True):#(m >= 0) & (m <= 2)):

				if True:
					log_multi_account(7)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
					#continue

						if (flag_cross_1H == 'buy'):
							comment = '1H gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1	

							if (spred > 0.06):
								print("spred = ", spred)
								continue	


							if (flag_cross_1H == 'buy'):
								tp_buy = (price + ((((abs(data_TsKs_1H_sell['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_TsKs_1H_sell['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_1H_buy['score']/1000))

	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

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
							print('request failed 1H TSKS Trade')
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
										print('send Done 1H TSKS Trade!!!')
						except:
							print('some thing wrong send 1H TSKS Trade')
							continue

			account_count = 1


			if ((flag_cross_1H == 'sell') & True):#(m >= 0) & (m <= 2)):
				
					log_multi_account(7)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
					#continue

						if (flag_cross_1H == 'sell'):
							comment = '1H gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1

							if (spred > 0.06):
								print("spred = ", spred)
								continue


							if (flag_cross_1H == 'sell'):
								tp_sell = (price - ((((abs(data_TsKs_1H_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_TsKs_1H_sell['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_1H_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

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
							print('request failed 1H TSKS Trade')
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
										print('send Done 1H TSKS Trade!!!')
						except:
							print('some thing wrong send 1H TSKS Trade')
							continue
		except:
			print('cant Play 1H TSKS Trade!!!')
		#**************************************************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#******************************************* Trade 30M **************************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		h,m,s = time_func()
		try:
			#print('**************************************** TsKs Trade Signal 30M ********************************************************')
			#print('30M TsKs BUY = ',signal_cross_30M_buy)

			#print('30M TsKs SELL = ',signal_cross_30M_sell)

			if ((flag_cross_30M == 'buy') & True):#(m%30 >= 0) & (m%30 <= 2)):

				if True:
					log_multi_account(7)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
					#continue

						if (flag_cross_30M == 'buy'):
							comment = '30M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1	

							if (spred > 0.06):
								print("spred = ", spred)
								continue	


							if (flag_cross_30M == 'buy'):
								tp_buy = (price + ((((abs(data_TsKs_30M_buy['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_TsKs_30M_buy['st'])) + spred) * price)/100))#(tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']] - ((0.05 * tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))	
								lot = float("{:.2f}".format(data_TsKs_30M_buy['score']/1000))
								#print('********************************* Score = ',data_TsKs_30M_buy['score'],'************************************')
								#print('********************************* Lot = ',lot,'**************************************')
	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

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
							print('request failed 30M TSKS Trade')
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
										print('send Done 30M TSKS Trade!!!')
						except:
							print('some thing wrong send 30M TSKS Trade')
							continue

			account_count = 1


			if ((flag_cross_30M == 'sell') & True):#(m%30 >= 0) & (m%30 <= 2)):
				
					log_multi_account(7)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
					#continue

						if (flag_cross_30M == 'sell'):
							comment = '30M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1

							if (spred > 0.06):
								print("spred = ", spred)
								continue



							if (flag_cross_30M == 'sell'):
								tp_sell = (price - ((((abs(data_TsKs_30M_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_TsKs_30M_sell['st'])) + spred) * price)/100))#(tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']] + ((0.05 * tenkan_30M[chiko_sig_30M[sym.name][len(chiko_sig_30M[sym.name])-1]['number']])/100))#(price - (((2 + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_30M_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

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
							print('request failed 30M TSKS Trade')
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
										print('send Done 30M TSKS Trade!!!')
						except:
							print('some thing wrong send 30M TSKS Trade')
							continue
		except:
			print('cant Play 30M TSKS Trade!!!')
		#**************************************************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#******************************************* Trade 5M **************************************************************************
		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		h,m,s = time_func()
		try:
			#print('**************************************** TsKs Trade Signal 5M ********************************************************')
			#print('5M TsKs BUY = ',signal_cross_5M_buy)

			#print('5M TsKs SELL = ',signal_cross_5M_sell)

			if (flag_cross_5M == 'buy'):

				if True:
					log_multi_account(7)
					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
					#print(positions)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 0):
								continue
					#continue

						if (flag_cross_5M == 'buy'):
							comment = '5M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).ask
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1	

							if (spred > 0.06):
								print("spred = ", spred)
								continue	

							if (flag_cross_5M == 'buy'):
								tp_buy = (price + ((((abs(data_TsKs_5M_buy['tp']))) * price)/100))
								sp_buy = (price - ((((abs(data_TsKs_5M_buy['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_5M_buy['score']/1000))
	


							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

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
							print('request failed 5M TSKS Trade')
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
										print('send Done 5M TSKS Trade!!!')
						except:
							print('some thing wrong send 5M TSKS Trade')
							continue

			account_count = 1


			if (flag_cross_5M == 'sell'):
				
					log_multi_account(7)

					while account_count <= 1:
					
						account_count += 1

						positions = mt5.positions_get(symbol=sym.name)
						if positions == None:
							print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
						elif len(positions)>0:
							for position in positions:
								type_position = position[5]
					
							print("Total positions on ",sym.name,' = ',len(positions))
							if (type_position == 1):
								continue
					#continue
						if (flag_cross_5M == 'sell'):
							comment = '5M gen TSKS'


						try:
							lot = 0.01
							point = mt5.symbol_info(sym.name).point
							price_ask = mt5.symbol_info_tick(sym.name).ask
							price = mt5.symbol_info_tick(sym.name).bid
							price_bid = mt5.symbol_info_tick(sym.name).bid
							spred = abs(price_ask-price_bid)
							deviation = 10
							magic += 1

							if (spred > 0.06):
								print("spred = ", spred)
								continue

							
							if (flag_cross_5M == 'sell'):
								tp_sell = (price - ((((abs(data_TsKs_5M_sell['tp']))) * price)/100))
								sp_sell = (price + ((((abs(data_TsKs_5M_sell['st'])) + spred) * price)/100))
								lot = float("{:.2f}".format(data_TsKs_5M_sell['score']/1000))


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

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
							print('request failed 5M TSKS Trade')
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
										print('send Done 5M TSKS Trade!!!')
						except:
							print('some thing wrong send 5M TSKS Trade')
							continue
		except:
			print('cant Play 5M TSKS Trade!!!')
		#**************************************************************************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#trade_strategy_TsKs()

