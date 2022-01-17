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


def trade_strategy_SMI_15M():

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


	symbol_data_15M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M15,10)

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


	symbol_data_1H,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,300)
	symbol_data_15M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M15,1000)

	vol_traded_max = (my_money/100) * 0.1

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

			macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)

			macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_15M_buy)))

			data_macd_15M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2) ,'score': 160}

			

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

			macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)

			macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_15M_sell)))

			data_macd_15M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus': (abs(mean_macd)/2) , 'diff_minus': ((-1) * abs(mean_macd)/2),'score': 160}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 1H MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_1H_buy = line
					data_macd_1H_buy['tp'] = float(data_macd_1H_buy['tp'])
					data_macd_v_buy['tp'] = (data_macd_1H_buy['tp']/3)*2

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

			macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)

			macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_1H_buy)))

			data_macd_1H_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 0}

			

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

			macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

			macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]

			mean_macd = abs(pd.DataFrame.mean(abs(macd_1H_sell)))

			data_macd_1H_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

		#******************************//////////////////////***********************************************************


		#******************************//////////////////////***********************************************************

		symbol_data_1H,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,300)
		symbol_data_15M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M15,1000)

		#print('calculate MACD',sym.name)

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

			# *******************++++++++++++ MACD Sell 1H************************************************************

			macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

			macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]
			macdh_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[1]]
			macds_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[2]]
			MACD_signal_cross_1H_sell = cross_macd(macd_1H_sell,macds_1H_sell,macdh_1H_sell,sym.name,data_macd_1H_sell['diff_minus'],data_macd_1H_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('1H Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



		try:

			# *******************++++++++++++ MACD Buy 15M************************************************************

			macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)

			macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]
			macdh_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[1]]
			macds_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[2]]
			MACD_signal_cross_15M_buy = cross_macd(macd_15M_buy,macds_15M_buy,macdh_15M_buy,sym.name,data_macd_15M_buy['diff_minus'],data_macd_15M_buy['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('15M Buy Macd Wrong!!')


		try:

			# *******************++++++++++++ MACD Sell 15M************************************************************

			macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)

			macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]
			macdh_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[1]]
			macds_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[2]]
			MACD_signal_cross_15M_sell = cross_macd(macd_15M_sell,macds_15M_sell,macdh_15M_sell,sym.name,data_macd_15M_sell['diff_minus'],data_macd_15M_sell['diff_plus'])

			#*********************---------------------*************/////////////*************************************************

		except:
			print('15M Sell Macd Wrong!!')

		#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#///////////////////////////////////////////////***********************-----------+++++++///////////////////////////////////////////


		#***************************************** ichimokou ******************************************************************************
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
			print('1H Buy TsKs Wrong!!')


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

			#print('tenkan = ',tenkan_5M)

			#print('tsks signal = ',TsKs_signal_cross_5M)


			#print(sym.name)
			#print('spana = ',SPANA_5M)


			#*********************---------------------*************/////////////*************************************************

		except:
			print('15M Buy TsKs Wrong!!')

		


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
		flag_cross_15M = ''
		flag_cross_1H = ''

		


		#print('get signal!!!')

		#****************--------------------++++++++++++++++++++++++****** 15M **********************************************************++++++++++++++++++++++
		#log_multi_account(1001)
		try:
			if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= 963)):
				print('buy 0 15M: MACD 15M Sig: ',sym.name)
				if (((MACD_signal_cross_1H_buy['signal'] == 'buy') | (MACD_signal_cross_1H_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1H_buy['index'] >= 963)):
					print('buy 1 15M: MACD 1H Sig ')
					if ((macd_1H_buy[len(macd_1H_buy)-1] <= (data_macd_1H_buy['diff_plus']/2)) & (macds_1H_buy[len(macd_1H_buy)-1] <= (data_macd_1H_buy['diff_plus']/2))):
						print('buy 2 15M: MACD 1H under plus ')
						if ((TsKs_signal_cross_15M['signal'] == 'buy') & (TsKs_signal_cross_15M['index'] >= 965)):
							print('buy 3 15M: TSKS 15M Cross ')
							search_counter = MACD_signal_cross_15M_buy['index']
							while (search_counter <= (len(symbol_data_15M[sym.name]['high']) - 1)):
								print('search_counter 15M = ',search_counter)
								if (symbol_data_15M[sym.name]['HL/2'][search_counter] > SPANA_15M[search_counter]) & (symbol_data_15M[sym.name]['HL/2'][search_counter] > SPANB_15M[search_counter]):
									print('buy 4 15M: candle above cloud ')
									if ((symbol_data_15M[sym.name]['HL/2'][search_counter] * 0.7) <= chikospan_15M[search_counter]):
										print('buy 5 15M: candle under chiko ')
										if (chikospan_15M[(search_counter)] > symbol_data_15M[sym.name]['high'][(search_counter-26)]):
											print('buy 6 15M: chiko above candle -26 ')
											if (((symbol_data_15M[sym.name]['low'][search_counter] >= tenkan_15M[search_counter]) | (symbol_data_15M[sym.name]['low'][search_counter] >= kijun_15M[search_counter])) & (tenkan_15M[search_counter] >= kijun_15M[search_counter])):
												print('buy 7 15M: candle above TSKS ')
												if ((symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['high']) - 1)] > SPANA_1H[(len(symbol_data_1H[sym.name]['high']) - 1)]) & (symbol_data_1H[sym.name]['high'][(len(symbol_data_1H[sym.name]['high']) - 1)] > SPANB_1H[(len(symbol_data_1H[sym.name]['high']) - 1)])):
													flag_cross_15M = 'buy'

													if data_macd_15M_buy['tp'] >= 0.3:
														data_macd_15M_buy['tp'] = 0.3
													data_macd_15M_buy['st'] = kijun_15M[TsKs_signal_cross_15M['index']]

													print('buy finished 15M: ',sym.name)

													#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] >= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
													#	data_macd_5M_buy['tp'] = (data_macd_5M_buy['tp'] * 2)
								search_counter += 1
		except:
			print('signal problem 15M BUY MACD!!!')


		try:
			if (((MACD_signal_cross_15M_sell['signal'] == 'sell') | (MACD_signal_cross_15M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_15M_sell['index'] >= 963)):
				print('sell 0 15M: MACD 15 Sig ',sym.name)
				if (((MACD_signal_cross_1H_sell['signal'] == 'sell') | (MACD_signal_cross_1H_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_1H_sell['index'] >= 963)):
					print('sell 1 15M: MACD 1H Sig ')
					if ((macd_1H_sell[len(macd_1H_sell)-1] >= (data_macd_1H_sell['diff_minus']/2)) & (macd_1H_sell[len(macd_1H_sell)-1] >= (data_macd_1H_sell['diff_minus']/2))):
						print('sell 2 15M: MACD 1H above minus ')
						if ((TsKs_signal_cross_15M['signal'] == 'sell') & (TsKs_signal_cross_15M['index'] >= 965)):
							print ('sell 3 15M: TSKS 15M Cross ')
							search_counter = MACD_signal_cross_15M_sell['index']
							while (search_counter <= (len(symbol_data_15M[sym.name]['high']) - 1)):
								print('search_counter 15M = ',search_counter)
								if (symbol_data_15M[sym.name]['HL/2'][search_counter] < SPANA_15M[search_counter]) & (symbol_data_15M[sym.name]['HL/2'][search_counter] < SPANB_15M[search_counter]):
									print('sell 4 15M: candle under cloud 15M')
									if ((symbol_data_15M[sym.name]['HL/2'][search_counter] * 0.7) >= chikospan_15M[(search_counter)]):
										print('sell 5 15M: candle above chiko 15M')
										if (chikospan_15M[(search_counter)] < symbol_data_15M[sym.name]['low'][(search_counter-26)]):
											print('sell 6 15M: chiko above candle -26 ')
											if (((symbol_data_15M[sym.name]['high'][search_counter] <= tenkan_15M[search_counter]) | (symbol_data_15M[sym.name]['high'][search_counter] <= kijun_15M[search_counter])) & (tenkan_15M[search_counter] <= kijun_15M[search_counter])):
												print('sell 7 15M: candle under TSKS ')
												if ((symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 1)] < SPANA_1H[(len(symbol_data_1H[sym.name]['low']) - 1)]) & (symbol_data_1H[sym.name]['low'][(len(symbol_data_1H[sym.name]['low']) - 1)] < SPANB_1H[(len(symbol_data_1H[sym.name]['high']) - 1)])):
													flag_cross_15M = 'sell'

													if data_macd_15M_sell['tp'] >= 0.3:
														data_macd_15M_sell['tp'] = 0.3
													data_macd_15M_sell['st'] = kijun_15M[TsKs_signal_cross_15M['index']]

													print('sell finished 15M: ',sym.name)

													#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
													#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

								search_counter += 1
		except:
			print('signal problem 15M SELL MACD!!!')

		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#************************************** 15M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()


		try:
			#print('**************************************** MACD Trade Signal 15M ********************************************************')

			if (flag_cross_15M == 'buy'):

				if True:

					
					while account_count <= 1001:

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
							if ((type_position == 0) & (comment_position == '15M gen SMI')):
								continue
								print('same buy')

						vol_traded_max = (my_money/100) * 0.06
					#continue

						if (flag_cross_15M == 'buy'):
							comment = '15M gen SMI'


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

							if (flag_cross_15M == 'buy'):
								tp_buy = (price + ((((abs(data_macd_15M_buy['tp'])) - spred) * price)/100))
								sp_buy = ((abs(data_macd_15M_buy['st'])) - (((spred + 0.03) * price)/100))
								lot = float("{:.2f}".format((data_macd_15M_buy['score'] * my_money)/1000000))
	
							if (((abs(data_macd_15M_buy['tp'])) - spred) <= 0): break

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
							print('request failed 15M Trade MACD')
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
										print('send Done 15M Trade MACD!!!')
						except:
							print('some thing wrong send 15M Trade MACD')
							continue

			account_count = 1000


			if (flag_cross_15M == 'sell'):
				
					


					
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
							if ((type_position == 1) & (comment_position == '15M gen SMI')):
								print('same sell')
								continue

						vol_traded_max = (my_money/100) * 0.06
								
					#continue
						if (flag_cross_15M == 'sell'):
							comment = '15M gen SMI'


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

							
							if (flag_cross_15M == 'sell'):
								tp_sell = (price - ((((abs(data_macd_15M_sell['tp'])) - spred) * price)/100))
								sp_sell = ((abs(data_macd_15M_sell['st'])) + (((spred + 0.03) * price)/100))
								lot = float("{:.2f}".format((data_macd_15M_sell['score'] * my_money)/1000000))

							if (((abs(data_macd_15M_sell['tp'])) - spred) <= 0): 
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
							print('request failed 15M Trade MACD')
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
										print('send Done 15M Trade MACD!!!')
						except:
							print('some thing wrong send 15M Trade MACD')
							continue
		except:
			print('cant Play 15M Trade MACD!!!')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		#///*************************************************************************************************************************************************


		

#trade_strategy_tarkibi(20,2)
#trade_strategy_SMI_15M()
