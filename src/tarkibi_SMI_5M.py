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

#from ta import add_all_ta_features
#from ind.utils import dropna
#from ind.trend import MACD
#symbol_data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
#symbol_data_ichi,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)


def trade_strategy_SMI_5M():
	
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
	symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)

	vol_traded_max = (my_money/100) * 0.05

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
			#break

		#print(sym.name)
#g = float("{:.2f}".format(x))

		
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
					data_macd_5M_buy['score'] = (float(data_macd_5M_buy['score']))

		except:
			#continue

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

			macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_buy)))

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2) ,'score': 150}

			

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
					data_macd_5M_sell['score'] = (float(data_macd_5M_sell['score']))

		except:
			#continue
			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

			macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_sell)))

			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2),'score': 150}

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

			macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

			macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_buy)))

			data_macd_30M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			

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

			macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

			macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_30M_sell)))

			data_macd_30M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

		#******************************//////////////////////***********************************************************


		#******************************//////////////////////***********************************************************

		symbol_data_30M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
		symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)



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

			# *******************++++++++++++ MACD Sell 5M************************************************************

			macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

			macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]
			macdh_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[1]]
			macds_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[2]]
			MACD_signal_cross_30M_sell = cross_macd(macd_30M_sell,macds_30M_sell,macdh_30M_sell,sym.name,data_macd_30M_sell['diff_minus'],data_macd_30M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('30M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



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
			print('30M Buy TsKs Wrong!!')


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

			#print('tenkan = ',tenkan_5M)

			#print('tsks signal = ',TsKs_signal_cross_5M)


			#print(sym.name)
			#print('spana = ',SPANA_5M)


			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Buy TsKs Wrong!!')

		


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
		flag_cross_5M = ''
		flag_cross_1M = ''

		


		#print('get signal!!!')

		#****************--------------------++++++++++++++++++++++++*********** 5M *****************************************************++++++++++++++++++++++
		#log_multi_account(1001)
		try:
			if (((MACD_signal_cross_5M_buy['signal'] == 'buy') | (MACD_signal_cross_5M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_5M_buy['index'] >= 963)):
				print('buy 0 5M: MACD 5M Sig: ',sym.name)
				if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= 963)):
					print('buy 1 5M: MACD 30 Sig ')
					if ((macd_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_plus']/2)) & (macds_30M_buy[len(macd_30M_buy)-1] <= (data_macd_30M_buy['diff_plus']/2))):
						print('buy 2 5M: MACD 30 under plus ')
						if ((TsKs_signal_cross_5M['signal'] == 'buy') & (TsKs_signal_cross_5M['index'] >= 965)):
							print('buy 3 5M: TSKS 5M Cross ')
							search_counter = MACD_signal_cross_5M_buy['index']
							while (search_counter <= (len(symbol_data_5M[sym.name]['high']) - 1)):
								print('search_counter 5M= ',search_counter)
								if (symbol_data_5M[sym.name]['HL/2'][search_counter] > SPANA_5M[search_counter]) & (symbol_data_5M[sym.name]['HL/2'][search_counter] > SPANB_5M[search_counter]):
									print('buy 4 5M: candle above cloud ')
									if ((symbol_data_5M[sym.name]['HL/2'][search_counter] * 0.7) <= chikospan_5M[search_counter]):
										print('buy 5 5M: candle under chiko ')
										if (chikospan_5M[(search_counter)] > symbol_data_5M[sym.name]['high'][(search_counter-26)]):
											print('buy 6 5M: chiko above candle -26 ')
											if (((symbol_data_5M[sym.name]['low'][search_counter] >= tenkan_5M[search_counter]) | (symbol_data_5M[sym.name]['low'][search_counter] >= kijun_5M[search_counter])) & (tenkan_5M[search_counter] >= kijun_5M[search_counter])):
												print('buy 7 5M: candle above TSKS ')
												if ((symbol_data_30M[sym.name]['high'][(len(symbol_data_30M[sym.name]['high']) - 1)] > SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]) & (symbol_data_30M[sym.name]['high'][(len(symbol_data_30M[sym.name]['high']) - 1)] > SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)])):
													flag_cross_5M = 'buy'

													if data_macd_5M_buy['tp'] >= 0.2:
														data_macd_5M_buy['tp'] = 0.2
													data_macd_5M_buy['st'] = kijun_5M[TsKs_signal_cross_5M['index']]

													print('buy finished 5M: ',sym.name)

													#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] >= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
													#	data_macd_5M_buy['tp'] = (data_macd_5M_buy['tp'] * 2)
								search_counter += 1
		except:
			print('signal problem 5M BUY MACD!!!')


		try:
			if (((MACD_signal_cross_5M_sell['signal'] == 'sell') | (MACD_signal_cross_5M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_5M_sell['index'] >= 963)):
				print('sell 0 5M: MACD 5 Sig ',sym.name)
				if (((MACD_signal_cross_30M_sell['signal'] == 'sell') | (MACD_signal_cross_30M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_30M_sell['index'] >= 963)):
					print('sell 1 5M: MACD 30 Sig ')
					if ((macd_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_minus']/2)) & (macd_30M_sell[len(macd_30M_sell)-1] >= (data_macd_30M_sell['diff_minus']/2))):
						print('sell 2 5M: MACD 30 above minus ')
						if ((TsKs_signal_cross_5M['signal'] == 'sell') & (TsKs_signal_cross_5M['index'] >= 965)):
							print ('sell 3 5M: TSKS 5M Cross ')
							search_counter = MACD_signal_cross_5M_sell['index']
							while (search_counter <= (len(symbol_data_5M[sym.name]['high']) - 1)):
								print('search_counter 5M= ',search_counter)
								if (symbol_data_5M[sym.name]['HL/2'][search_counter] < SPANA_5M[search_counter]) & (symbol_data_5M[sym.name]['HL/2'][search_counter] < SPANB_5M[search_counter]):
									print('sell 4 5M: candle under cloud ')
									if ((symbol_data_5M[sym.name]['HL/2'][search_counter] * 0.7) >= chikospan_5M[(search_counter)]):
										print('sell 5 5M: candle above chiko ')
										if (chikospan_5M[(search_counter)] < symbol_data_5M[sym.name]['low'][(search_counter-26)]):
											print('sell 6 5M: chiko above candle -26 ')
											if (((symbol_data_5M[sym.name]['high'][search_counter] <= tenkan_5M[search_counter]) | (symbol_data_5M[sym.name]['high'][search_counter] <= kijun_5M[search_counter])) & (tenkan_5M[search_counter] <= kijun_5M[search_counter])):
												print('sell 7 5M: candle under TSKS ')
												if ((symbol_data_30M[sym.name]['low'][(len(symbol_data_30M[sym.name]['low']) - 1)] < SPANA_30M[(len(symbol_data_30M[sym.name]['low']) - 1)]) & (symbol_data_30M[sym.name]['low'][(len(symbol_data_30M[sym.name]['low']) - 1)] < SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)])):
													flag_cross_5M = 'sell'

													if data_macd_5M_sell['tp'] >= 0.2:
														data_macd_5M_sell['tp'] = 0.2
													data_macd_5M_sell['st'] = kijun_5M[TsKs_signal_cross_5M['index']]

													print('sell finished 5M: ',sym.name)

													#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
													#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

								search_counter += 1
		except:
			print('signal problem 5M SELL MACD!!!')

		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#************************************** 5M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()

		#flag_cross_5M = 'buy'
		try:
			#print('**************************************** MACD Trade Signal 5M ********************************************************')

			if (flag_cross_5M == 'buy'):

				if True:

					
					while account_count <= 1000:

						my_money = log_multi_account(account_count)
					
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
											#continue
							except:
								print('modify error')

							if ((type_position == 0) & (comment_position == '5M gen SMI')):
								continue
								print('same buy')

						vol_traded_max = (my_money/100) * 0.06
					#continue

						if (flag_cross_5M == 'buy'):
							comment = '5M gen SMI'


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
								sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred + 0.03) * price)/100))
								lot = float("{:.2f}".format((data_macd_5M_buy['score'] * my_money)/1000000))
	
							if (((abs(data_macd_5M_buy['tp'])) - spred) <= 0): break

							if (sp_buy >= price):
								sp_buy = (price - (((0.3 + spred) * price)/100))

						

							lot = float("{:.2f}".format((lot)))

							if (lot >= 50):
								lot = 50

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
				
					


					
					while account_count <= 1001:

						my_money = log_multi_account(account_count)
					
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
											#continue

							except:
								print('modify error')
					
							#print("Total positions on ",sym.name,' = ',len(positions))
							if ((type_position == 1) & (comment_position == '5M gen SMI')):
								print('same sell')
								continue

						vol_traded_max = (my_money/100) * 0.06
								
					#continue
						if (flag_cross_5M == 'sell'):
							comment = '5M gen SMI'


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
								sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred + 0.03) * price)/100))
								lot = float("{:.2f}".format((data_macd_5M_sell['score'] * my_money)/1000000))

							if (((abs(data_macd_5M_sell['tp'])) - spred) <= 0): 
								#print(((abs(data_macd_5M_sell['tp'])) - spred))
								break


							if (sp_sell <= price):
								sp_sell = (price + (((0.3 + spred) * price)/100))

							lot = float("{:.2f}".format((lot)))

							if (lot >= 50):
								lot = 50

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

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 1M ********************************************************')



			if (flag_cross_1M == 'buy'):

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

						if (flag_cross_1M == 'buy'):
							comment = '1M gen SMA'


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
								tp_buy = (price + ((((abs(data_SMA_1M_buy['tp'])) - spred) * price)/100))
								sp_buy = (price - ((((abs(data_SMA_1M_buy['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_SMA_1M_buy['score']/100))
	
							if (((abs(data_macd_1M_buy['tp'])) - spred) <= 0): break

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

			account_count = 1000


			if (flag_cross_1M == 'sell'):
				
				


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
						if (flag_cross_1M == 'sell'):
							comment = '1M gen SMA'


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
								tp_sell = (price - ((((abs(data_SMA_1M_sell['tp'])) - spred) * price)/100))
								sp_sell = (price + ((((abs(data_SMA_1M_sell['st'])) + spred + 0.5) * price)/100))
								lot = float("{:.2f}".format(data_SMA_1M_sell['score']/1000))

							if (((abs(data_macd_1M_sell['tp'])) - spred) <= 0): 
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


		

#trade_strategy_tarkibi(20,2)
#trade_strategy_SMI_5M()
