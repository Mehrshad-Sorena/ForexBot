from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
#import matplotlib.pyplot as plt
import numpy as np
#from find_flat import *
#from three_flat_find import *
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
import threading
from multiprocessing import Process
import statistics


def tester_strategy_bot_BUY(sym_num,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M):

	sym_input = {
	1: 'AUDCAD_i',
	2: 'AUDCHF_i',
	3: 'AUDJPY_i',
	4: 'AUDNZD_i',
	5: 'AUDUSD_i',
	6: 'CADCHF_i',
	7: 'CADJPY_i',
	8: 'CHFJPY_i',
	9: 'EURAUD_i',
	10: 'EURCAD_i',
	11: 'EURCHF_i',
	12: 'EURGBP_i',
	13: 'EURJPY_i',
	14: 'EURNZD_i',
	15: 'EURRUB_i',
	16: 'EURUSD_i',
	17: 'GBPAUD_i',
	18: 'GBPCAD_i',
	19: 'GBPCHF_i',
	20: 'GBPJPY_i',
	21: 'GBPNZD_i',
	22: 'GBPSGD_i',
	23: 'GBPUSD_i',
	24: 'NZDCAD_i',
	25: 'NZDCHF_i',
	26: 'NZDJPY_i',
	27: 'NZDUSD_i',
	28: 'USDCAD_i',
	29: 'USDCHF_i',
	30: 'USDJPY_i',
	31: 'USDSGD_i',
	32: 'XAGUSD_i',
	33: 'XAUUSD_i'
	}

	#window_end = 99999
	window_end = 12096

	window_start = 0

	symbols,my_money = get_symbols(10)

	hour,minute,second,day = time_func()

	log_name = 'Logs/tester_strategy_bot/bot_log_BUY_'+day+'-'+str(hour)+'-'+str(minute)+'-'+str(second)+sym_input[sym_num]+'.log'
	
	logging.basicConfig(filename=log_name, level=logging.DEBUG)

	SUCCSESSFULLY = 0
	FAILED = 0

	alfa_SUC = {}
	alfa_SUC[0] = 0
	alfa_FA = {}
	alfa_FA[0] = 0

	Profit_Plus = 0
	Profit_Minus = 0

	ramp = 0
	ramp_Suc = {}
	ramp_Suc[0] = 0
	ramp_Fa = {}
	ramp_Fa[0] = 0


	ramp_sell = 0
	ramp_Suc_sell = {}
	ramp_Suc_sell[0] = 0
	ramp_Fa_sell = {}
	ramp_Fa_sell[0] = 0

	ramp_buy = 0
	ramp_Suc_buy = {}
	ramp_Suc_buy[0] = 0
	ramp_Fa_buy = {}
	ramp_Fa_buy[0] = 0


	ramp_candle = 0
	ramp_candle_Suc = {}
	ramp_candle_Suc[0] = 0
	ramp_candle_Fa = {}
	ramp_candle_Fa[0] = 0

	ramp_candle_sell = 0
	ramp_candle_Suc_sell = {}
	ramp_candle_Suc_sell[0] = 0
	ramp_candle_Fa_sell = {}
	ramp_candle_Fa_sell[0] = 0

	ramp_candle_buy = 0
	ramp_candle_Suc_buy = {}
	ramp_candle_Suc_buy[0] = 0
	ramp_candle_Fa_buy = {}
	ramp_candle_Fa_buy[0] = 0


	Coef_ramps_Suc = {}
	Coef_ramps_Suc[0] = 0
	Coef_ramps_Fa = {}
	Coef_ramps_Fa[0] = 0

	dif_ramps_Suc = {}
	dif_ramps_Suc[0] = 0
	dif_ramps_Fa = {}
	dif_ramps_Fa[0] = 0

	st_Suc = {}
	st_Suc[0] = 0
	st_Fa = {}
	st_Fa[0] = 0

	Vol_Coef_Suc = {}
	Vol_Coef_Fa = {}
	Vol_Coef_Suc[0] = 1
	Vol_Coef_Fa[0] = 1

	for sym in symbols:
		

		if (sym.name != sym_input[sym_num]):continue
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

		logging.debug('************************************************* Start Symbol *************************************************')
		logging.info('************************************************* BUY **********************************************************************')
		logging.info('*************************************************** BUY ********************************************************************')
		logging.info('**************************************************** BUY *******************************************************************')
		logging.debug('                                           %s' %sym.name)
		
		

		print(sym.name)


		#****************************** Data_Buy 5M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_5M_buy = line
					data_macd_5M_buy['tp'] = float(data_macd_5M_buy['tp'])
					data_macd_5M_buy['tp'] = (data_macd_5M_buy['tp']/3)*2

					data_macd_5M_buy['st'] = float(data_macd_5M_buy['st'])
					data_macd_5M_buy['macd_fast'] = 12#float(data_macd_5M_buy['macd_fast'])
					data_macd_5M_buy['macd_slow'] = 26#float(data_macd_5M_buy['macd_slow'])
					data_macd_5M_buy['macd_signal'] = 9#float(data_macd_5M_buy['macd_signal'])
					data_macd_5M_buy['diff_minus'] = float(data_macd_5M_buy['diff_minus'])
					data_macd_5M_buy['diff_plus'] = float(data_macd_5M_buy['diff_plus'])
					data_macd_5M_buy['score'] = (float(data_macd_5M_buy['score']) / 2)

					if(data_macd_5M_buy['score'] < max_allow_score):
						data_macd_5M_buy['score'] = data_macd_5M_buy['score']/10

		except:
			#continue

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 0}

			try:
				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_buy)))

				data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
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
					data_macd_5M_sell['macd_fast'] = 12#float(data_macd_5M_sell['macd_fast'])
					data_macd_5M_sell['macd_slow'] = 26#float(data_macd_5M_sell['macd_slow'])
					data_macd_5M_sell['macd_signal'] = 9#float(data_macd_5M_sell['macd_signal'])
					data_macd_5M_sell['diff_minus'] = float(data_macd_5M_sell['diff_minus'])
					data_macd_5M_sell['diff_plus'] = float(data_macd_5M_sell['diff_plus'])
					data_macd_5M_sell['score'] = (float(data_macd_5M_sell['score']) / 2)

					if(data_macd_5M_sell['score'] < max_allow_score):
						data_macd_5M_sell['score'] = data_macd_5M_sell['score']/10

		except:
			#continue
			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
			,'diff_plus':0 , 'diff_minus': 0,'score': 20}

			try:
				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_sell)))

				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 0}

			except:
				#print('Cant calc MACD 5M SELL')
				logging.warning('Cant calc MACD 5M SELL')
				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 12 , 'macd_slow': 26, 'macd_signal': 9
				,'diff_plus': 0 , 'diff_minus': 0,'score': 100}

		#******************************//////////////////////***********************************************************

		

		spred = 0.04#((abs(price_ask-price_bid)/price_ask) * 100)

		if (spred > 0.045):
			print('High spred')
			continue


		diff_counter = 0

		num_trade = 0
		#[0:window_counter_1M]

		window_counter_5M = window_end-1

		print('5M first = ',symbol_data_5M[sym.name]['time'][len(symbol_data_5M[sym.name]['time'])-1])

		print('')

		#print(day_first)

		window_counter_5M = window_end - 1



		
		#window_counter_5M = 52000
		#window_counter_5M = 50000

		while window_counter_5M >= 150:

			
			if ((window_counter_5M-2)<0):break

			try:

				# *******************++++++++++++ MACD Buy 5M************************************************************

				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)[0:window_counter_5M+1]

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
				#print(window_counter_5M)
				#print(macd_5M_buy)
				macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
				macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
				#MACD_signal_cross_5M_buy = cross_macd(macd_5M_buy,macds_5M_buy,macdh_5M_buy,sym.name,data_macd_5M_buy['diff_minus'],data_macd_5M_sell['diff_plus']/100)

				#print('MACD_signal_cross_5M_buy = ',MACD_signal_cross_5M_buy)
				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
				#print(window_counter_5M)
				#print(macd_5M_buy)
				macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
				macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Buy Macd Wrong!!')
				logging.warning('5M Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 5M************************************************************

				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)[0:window_counter_5M+1]

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
				#print(macd_5M_sell)
				macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
				macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
				#MACD_signal_cross_5M_sell = cross_macd(macd_5M_sell,macds_5M_sell,macdh_5M_sell,sym.name,data_macd_5M_buy['diff_minus']/100,data_macd_5M_sell['diff_plus'])

				#print('MACD_signal_cross_5M_sell = ',MACD_signal_cross_5M_sell)

				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
				#print(macd_5M_sell)
				macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
				macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Sell Macd Wrong!!')
				logging.warning('5M Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			#///////////////////////////////////////////////***********************-----------+++++++///////////////////////////////////////////


			#***************************************** ichimokou ******************************************************************************

			try:
				# *******************++++++++++++ TSKS 5M************************************************************
				ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_5M+1]
				SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]][0:window_counter_5M+1]
				SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]][0:window_counter_5M+1]
				tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter_5M+1]
				kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter_5M+1]
				chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]][0:window_counter_5M+1]

				TsKs_signal_cross_5M = {}
				#TsKs_signal_cross_5M = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

				ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
				SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
				tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
				kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
				chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Buy TsKs Wrong!!')
				logging.warning('5M Buy TsKs Wrong!!')
			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




			if (sym.name == 'AUDCAD_i') | (sym.name == 'AUDCAD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  0.062

				ramp_MACD_fixed_buy = 0.000001
				ramp_candle_fixed_buy = -0.000001

				Max_ramp_MACD_fixed_buy = 0.000011
				Max_ramp_candle_fixed_buy = -0.000025

				ramp_sell_fixed = -0.000002

				coef_ramps_fixed_buy = -2.2
				diff_ramps_fixed_buy = 0.000003

				Max_coef_ramps_fixed_buy = -16.0
				Max_diff_ramps_fixed_buy = 0.000027

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0.000044

				sma_288_5M_fixed_low = 0.0007
				sma_168_5M_fixed_low = 0.00055

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 2 #2.2
				tp_first_Coef_fixed_buy = 5

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.051

				ramp_MACD_fixed_sell = -0.000013
				ramp_candle_fixed_sell = 0.000035

				Max_ramp_MACD_fixed_sell = -0.00002
				Max_ramp_candle_fixed_sell = 0.000055

				ramp_buy_fixed = -0.000028

				coef_ramps_fixed_sell = -2.7
				diff_ramps_fixed_sell = 0.000048

				Max_coef_ramps_fixed_sell = -3.1
				Max_diff_ramps_fixed_sell = 0.000073

				st_Coef_fixed_sell = 1.0019
				tp_Coef_fixed_sell = 1.5

			elif (sym.name == 'AUDCHF_i') | (sym.name == 'AUDCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  0.075

				ramp_MACD_fixed_buy = 0.000002
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0.00007

				sma_288_5M_fixed_low = 0.000835
				sma_168_5M_fixed_low = 0.0007

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.107

				ramp_MACD_fixed_sell = -0.00001
				ramp_candle_fixed_sell = 0.000022

				Max_ramp_MACD_fixed_sell = -0.00001
				Max_ramp_candle_fixed_sell = 0.000013

				ramp_buy_fixed = 0.000016

				coef_ramps_fixed_sell = -4
				diff_ramps_fixed_sell = 0.000016

				Max_coef_ramps_fixed_sell = -6.5
				Max_diff_ramps_fixed_sell = 0.000017

				st_Coef_fixed_sell = 1.0018
				tp_Coef_fixed_sell = 3.3

			elif (sym.name == 'AUDJPY_i') | (sym.name == 'AUDJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  0.232

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0.000859
				Max_ramp_candle_fixed_buy = -0.0041

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = -286
				Max_diff_ramps_fixed_buy = 0.0038

				sma_288_5M_fixed_high = 0.059
				sma_168_5M_fixed_high = 0.014

				sma_288_5M_fixed_low = 1
				sma_168_5M_fixed_low = 1

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy_1 = 1.2
				tp_Coef_fixed_buy = 2.2
				tp_first_Coef_fixed_buy = 2.5

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.081
 
				ramp_MACD_fixed_sell = -0.00051
				ramp_candle_fixed_sell = 0.004

				Max_ramp_MACD_fixed_sell = -0.0014
				Max_ramp_candle_fixed_sell = 0.00187

				ramp_buy_fixed = 0.000601

				coef_ramps_fixed_sell = -4
				diff_ramps_fixed_sell = 0.0044

				Max_coef_ramps_fixed_sell = 10
				Max_diff_ramps_fixed_sell = 0.0033

				st_Coef_fixed_sell = 1.0043
				tp_Coef_fixed_sell = 2.6

			elif (sym.name == 'AUDNZD_i') | (sym.name == 'AUDNZD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = 0

				Max_ramp_MACD_fixed_buy = 0.000012
				Max_ramp_candle_fixed_buy = -0.000022

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = -30
				Max_diff_ramps_fixed_buy = 0.000022

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0.0012
				sma_168_5M_fixed_low = 0.000307

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1.2
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.119

				ramp_MACD_fixed_sell = -0.000051
				ramp_candle_fixed_sell = 0.000038

				Max_ramp_MACD_fixed_sell = -0.000052
				Max_ramp_candle_fixed_sell = 0.000057

				ramp_buy_fixed = 0.000006

				coef_ramps_fixed_sell = -0.74
				diff_ramps_fixed_sell = 0.000089

				Max_coef_ramps_fixed_sell = -3
				Max_diff_ramps_fixed_sell = 0.000109

				st_Coef_fixed_sell = 1.0026
				tp_Coef_fixed_sell = 1.5

			elif (sym.name == 'AUDUSD_i') | (sym.name == 'AUDUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = 0

				Max_ramp_MACD_fixed_buy = 0.000008
				Max_ramp_candle_fixed_buy = -0.000026

				ramp_sell_fixed = -0.000002

				coef_ramps_fixed_buy = -1
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = -10
				Max_diff_ramps_fixed_buy = 0.00002

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0.000088

				sma_288_5M_fixed_low = 1
				sma_168_5M_fixed_low = 1

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 2.7
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.044

				ramp_MACD_fixed_sell = -0.000024
				ramp_candle_fixed_sell = 0.000026

				Max_ramp_MACD_fixed_sell = -0.000026
				Max_ramp_candle_fixed_sell = 0.000049

				ramp_buy_fixed = 0.000008

				coef_ramps_fixed_sell = -1
				diff_ramps_fixed_sell = 0.00005

				Max_coef_ramps_fixed_sell = -2
				Max_diff_ramps_fixed_sell = 0.000076

				st_Coef_fixed_sell = 1.004
				tp_Coef_fixed_sell = 3.2

			elif (sym.name == 'CADCHF_i') | (sym.name == 'CADCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0.000008
				Max_ramp_candle_fixed_buy = -0.000027

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = -30
				Max_diff_ramps_fixed_buy = 0.000026

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 1
				sma_168_5M_fixed_low = 1

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.05

				ramp_MACD_fixed_sell = -0.000012
				ramp_candle_fixed_sell = 0.000029

				Max_ramp_MACD_fixed_sell = -0.00003
				Max_ramp_candle_fixed_sell = 0.000013

				ramp_buy_fixed = 0.000004

				coef_ramps_fixed_sell = -1.7
				diff_ramps_fixed_sell = 0.000011

				Max_coef_ramps_fixed_sell = -3.5
				Max_diff_ramps_fixed_sell = 0.000017 

				st_Coef_fixed_sell = 1.0051
				tp_Coef_fixed_sell = 2.9

			elif (sym.name == 'CADJPY_i') | (sym.name == 'CADJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.061

				ramp_MACD_fixed_sell = -0.00084
				ramp_candle_fixed_sell = 0.00277

				Max_ramp_MACD_fixed_sell = -0.001
				Max_ramp_candle_fixed_sell = 0.007

				ramp_buy_fixed = 0.00016

				coef_ramps_fixed_sell = -3.2
				diff_ramps_fixed_sell = 0.0036

				Max_coef_ramps_fixed_sell = 8.9
				Max_diff_ramps_fixed_sell = 0.0083

				st_Coef_fixed_sell = 1.002
				tp_Coef_fixed_sell = 2.6

			elif (sym.name == 'CHFJPY_i') | (sym.name == 'CHFJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				Vol_Coef_Fixed_buy = 1

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.041

				ramp_MACD_fixed_sell = -0.0018
				ramp_candle_fixed_sell = 0.004

				Max_ramp_MACD_fixed_sell = -0.00308
				Max_ramp_candle_fixed_sell = 0.0099

				ramp_buy_fixed = 0.00134

				coef_ramps_fixed_sell = -2
				diff_ramps_fixed_sell = 0.006

				Max_coef_ramps_fixed_sell = -3.2
				Max_diff_ramps_fixed_sell = 0.012

				st_Coef_fixed_sell = 1.0015
				tp_Coef_fixed_sell = 1.5

			elif (sym.name == 'EURAUD_i') | (sym.name == 'EURAUD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.094

				ramp_MACD_fixed_sell = -0.000016
				ramp_candle_fixed_sell = 0.000027

				Max_ramp_MACD_fixed_sell = 0.00003
				Max_ramp_candle_fixed_sell = 0.00009

				ramp_buy_fixed = 0.000007

				coef_ramps_fixed_sell = -1.6
				diff_ramps_fixed_sell = 0.000043

				Max_coef_ramps_fixed_sell = -8
				Max_diff_ramps_fixed_sell = 0.00009

				st_Coef_fixed_sell = 1.0043
				tp_Coef_fixed_sell = 1.6

			elif (sym.name == 'EURCAD_i') | (sym.name == 'EURCAD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = No OK
				alfa_fixed_sell = 0.056

				ramp_MACD_fixed_sell = -0.000015
				ramp_candle_fixed_sell = 0.000033

				Max_ramp_MACD_fixed_sell = -0.000019
				Max_ramp_candle_fixed_sell = 0.00002

				ramp_buy_fixed = 0.000002

				coef_ramps_fixed_sell = -0.92
				diff_ramps_fixed_sell = 0.00005

				Max_coef_ramps_fixed_sell = -5.7
				Max_diff_ramps_fixed_sell = 0.00002

				st_Coef_fixed_sell = 1.002
				tp_Coef_fixed_sell = 3

			elif (sym.name == 'EURCHF_i') | (sym.name == 'EURCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.146

				ramp_MACD_fixed_sell = 0
				ramp_candle_fixed_sell = 0.00002199

				Max_ramp_MACD_fixed_sell = -0.000001
				Max_ramp_candle_fixed_sell = 0.000055

				ramp_buy_fixed = 0.0000221

				coef_ramps_fixed_sell = -54.99
				diff_ramps_fixed_sell = 0.000023

				Max_coef_ramps_fixed_sell = -136
				Max_diff_ramps_fixed_sell = 0.000056

				st_Coef_fixed_sell = 1.0016
				tp_Coef_fixed_sell = 1.2

			elif (sym.name == 'EURGBP_i') | (sym.name == 'EURGBP'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.066

				ramp_MACD_fixed_sell = -0.00001
				ramp_candle_fixed_sell = 0.000017

				Max_ramp_MACD_fixed_sell = -0.000012
				Max_ramp_candle_fixed_sell = 0.000036

				ramp_buy_fixed = 0.000004

				coef_ramps_fixed_sell = -1.6
				diff_ramps_fixed_sell = 0.000027

				Max_coef_ramps_fixed_sell = -3.3
				Max_diff_ramps_fixed_sell = 0.000047

				st_Coef_fixed_sell = 1.005
				tp_Coef_fixed_sell = 1.5

			elif (sym.name == 'EURJPY_i') | (sym.name == 'EURJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.06

				ramp_MACD_fixed_sell = -0.0012
				ramp_candle_fixed_sell = 0.002

				Max_ramp_MACD_fixed_sell = -0.00197
				Max_ramp_candle_fixed_sell = 0.0072

				ramp_buy_fixed = 0.000196

				coef_ramps_fixed_sell = -1.3
				diff_ramps_fixed_sell = 0.0036

				Max_coef_ramps_fixed_sell = -5
				Max_diff_ramps_fixed_sell = 0.0087

				st_Coef_fixed_sell = 1.0033
				tp_Coef_fixed_sell = 3.7

			elif (sym.name == 'EURNZD_i') | (sym.name == 'EURNZD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.069

				ramp_MACD_fixed_sell = -0.00001
				ramp_candle_fixed_sell = 0.000021

				Max_ramp_MACD_fixed_sell = -0.00003
				Max_ramp_candle_fixed_sell = 0.0001

				ramp_buy_fixed = 0.000008

				coef_ramps_fixed_sell =  -2
				diff_ramps_fixed_sell = 0.000029

				Max_coef_ramps_fixed_sell = -17.0
				Max_diff_ramps_fixed_sell = 0.0001

				st_Coef_fixed_sell = 1.0025
				tp_Coef_fixed_sell = 4.2

			elif (sym.name == 'EURRUB_i') | (sym.name == 'EURRUB'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = No OK
				alfa_fixed_sell = 0

				ramp_MACD_fixed_sell = 0
				ramp_candle_fixed_sell = 0

				Max_ramp_MACD_fixed_sell = 0
				Max_ramp_candle_fixed_sell = 0

				ramp_buy_fixed = 1

				coef_ramps_fixed_sell = 0
				diff_ramps_fixed_sell = 0

				Max_coef_ramps_fixed_sell = 0
				Max_diff_ramps_fixed_sell = 0

				st_Coef_fixed_sell = 1.005
				tp_Coef_fixed_sell = 1

			elif (sym.name == 'EURUSD_i') | (sym.name == 'EURUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy =  1

				ramp_MACD_fixed_buy = 0
				ramp_candle_fixed_buy = -0

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = 0

				coef_ramps_fixed_buy = 0
				diff_ramps_fixed_buy = 0

				Max_coef_ramps_fixed_buy = 0
				Max_diff_ramps_fixed_buy = 0

				sma_288_5M_fixed_high = 0
				sma_168_5M_fixed_high = 0

				sma_288_5M_fixed_low = 0
				sma_168_5M_fixed_low = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1
				tp_first_Coef_fixed_buy = 3

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.048

				ramp_MACD_fixed_sell = -0.000027
				ramp_candle_fixed_sell = 0.000013

				Max_ramp_MACD_fixed_sell = -0.000039
				Max_ramp_candle_fixed_sell = 0.000061

				ramp_buy_fixed = 0.000006

				coef_ramps_fixed_sell = -0.32
				diff_ramps_fixed_sell = 0.000042

				Max_coef_ramps_fixed_sell = -1.9
				Max_diff_ramps_fixed_sell = 0.000094

				st_Coef_fixed_sell = 1.005
				tp_Coef_fixed_sell = 2.8

			elif (sym.name == 'GBPAUD_i') | (sym.name == 'GBPAUD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.083

				ramp_MACD_fixed_sell = -0.000009
				ramp_candle_fixed_sell = 0.000077

				Max_ramp_MACD_fixed_sell = -0.000013
				Max_ramp_candle_fixed_sell = 0.00013

				ramp_buy_fixed = 0.000008

				coef_ramps_fixed_sell = -8.8
				diff_ramps_fixed_sell = 0.000086

				Max_coef_ramps_fixed_sell = -11
				Max_diff_ramps_fixed_sell = 0.000142

				st_Coef_fixed_sell = 1.0039
				tp_Coef_fixed_sell = 2.5

			elif (sym.name == 'GBPCAD_i') | (sym.name == 'GBPCAD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.037

				ramp_MACD_fixed_sell = -0.000016
				ramp_candle_fixed_sell = 0.000054

				Max_ramp_MACD_fixed_sell = -0.000017
				Max_ramp_candle_fixed_sell = 0.000105

				ramp_buy_fixed = 0.000002

				coef_ramps_fixed_sell = -6.5
				diff_ramps_fixed_sell = 0.0001

				Max_coef_ramps_fixed_sell = -6.7
				Max_diff_ramps_fixed_sell = 0.00012

				st_Coef_fixed_sell = 1.0019
				tp_Coef_fixed_sell = 2.5

			elif (sym.name == 'GBPCHF_i') | (sym.name == 'GBPCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.118

				ramp_MACD_fixed_sell = -0.000012
				ramp_candle_fixed_sell = 0.000041

				Max_ramp_MACD_fixed_sell = -0.000029
				Max_ramp_candle_fixed_sell = 0.000044

				ramp_buy_fixed = 0.000014

				coef_ramps_fixed_sell = -3.2
				diff_ramps_fixed_sell = 0.000053

				Max_coef_ramps_fixed_sell = -10.0
				Max_diff_ramps_fixed_sell = 0.000048

				st_Coef_fixed_sell = 1.0026
				tp_Coef_fixed_sell = 3

			elif (sym.name == 'GBPJPY_i') | (sym.name == 'GBPJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.12

				ramp_MACD_fixed_sell = -0.001
				ramp_candle_fixed_sell = 0.0039

				Max_ramp_MACD_fixed_sell = -0.002
				Max_ramp_candle_fixed_sell = 0.006

				ramp_buy_fixed = 0.0019

				coef_ramps_fixed_sell = -1.9
				diff_ramps_fixed_sell = 0.0049

				Max_coef_ramps_fixed_sell = -2.2
				Max_diff_ramps_fixed_sell = 0.00348

				st_Coef_fixed_sell = 1.0039
				tp_Coef_fixed_sell = 5#1.2

			elif (sym.name == 'GBPNZD_i') | (sym.name == 'GBPNZD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.157

				ramp_MACD_fixed_sell = -0.000011
				ramp_candle_fixed_sell = 0.00002699

				Max_ramp_MACD_fixed_sell = -0.000058
				Max_ramp_candle_fixed_sell = 0.0001

				ramp_buy_fixed = 0.000006

				coef_ramps_fixed_sell = -2.9
				diff_ramps_fixed_sell = 0.00002799

				Max_coef_ramps_fixed_sell = -7
				Max_diff_ramps_fixed_sell = 0.00015

				st_Coef_fixed_sell = 1.0045
				tp_Coef_fixed_sell = 2.7

			elif (sym.name == 'GBPSGD_i') | (sym.name == 'GBPSGD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.08

				ramp_MACD_fixed_sell = -0.000009
				ramp_candle_fixed_sell = 0.000027

				Max_ramp_MACD_fixed_sell = -0.000017
				Max_ramp_candle_fixed_sell = 0.000050

				ramp_buy_fixed = 0.000001

				coef_ramps_fixed_sell = -2.2
				diff_ramps_fixed_sell = 0.000035

				Max_coef_ramps_fixed_sell = -4.1
				Max_diff_ramps_fixed_sell = 0.000062

				st_Coef_fixed_sell = 1.002
				tp_Coef_fixed_sell = 3.6#1.2

			elif (sym.name == 'GBPUSD_i') | (sym.name == 'GBPUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.074

				ramp_MACD_fixed_sell = -0.00001
				ramp_candle_fixed_sell = 0.000014

				Max_ramp_MACD_fixed_sell = -0.000016
				Max_ramp_candle_fixed_sell = 0.00001

				ramp_buy_fixed = 0.000008

				coef_ramps_fixed_sell = -2.4
				diff_ramps_fixed_sell = 0.000034

				Max_coef_ramps_fixed_sell = -5
				Max_diff_ramps_fixed_sell = 0.00003

				st_Coef_fixed_sell = 1.0036
				tp_Coef_fixed_sell = 3.5#1.2

			elif (sym.name == 'NZDCAD_i') | (sym.name == 'NZDCAD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.143

				ramp_MACD_fixed_sell = -0.000013
				ramp_candle_fixed_sell = 0.000023

				Max_ramp_MACD_fixed_sell = -0.000022
				Max_ramp_candle_fixed_sell = 0.000077

				ramp_buy_fixed = 0.000006

				coef_ramps_fixed_sell = -2#-0.3799
				diff_ramps_fixed_sell = 0.000033

				Max_coef_ramps_fixed_sell = -6.0
				Max_diff_ramps_fixed_sell = 0.000087

				st_Coef_fixed_sell = 1.0046
				tp_Coef_fixed_sell = 2.5

			elif (sym.name == 'NZDCHF_i') | (sym.name == 'NZDCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.09

				ramp_MACD_fixed_sell = -0.000004
				ramp_candle_fixed_sell = 0.000022

				Max_ramp_MACD_fixed_sell = -0.00001
				Max_ramp_candle_fixed_sell = 0.00001

				ramp_buy_fixed = 0.00001

				coef_ramps_fixed_sell = -7
				diff_ramps_fixed_sell = 0.00000899

				Max_coef_ramps_fixed_sell = -10
				Max_diff_ramps_fixed_sell = 0.00002

				st_Coef_fixed_sell = 1.003
				tp_Coef_fixed_sell = 2

			elif (sym.name == 'NZDJPY_i') | (sym.name == 'NZDJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.088

				ramp_MACD_fixed_sell = -0.0006
				ramp_candle_fixed_sell = 0.0018

				Max_ramp_MACD_fixed_sell = -0.0005
				Max_ramp_candle_fixed_sell = 0.001

				ramp_buy_fixed = 0.003412

				coef_ramps_fixed_sell = -2.9
				diff_ramps_fixed_sell = 0.0024

				Max_coef_ramps_fixed_sell = -4
				Max_diff_ramps_fixed_sell = 0.0009

				st_Coef_fixed_sell = 1.0031
				tp_Coef_fixed_sell = 5.2

			elif (sym.name == 'NZDUSD_i') | (sym.name == 'NZDUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.065

				ramp_MACD_fixed_sell = -0.00001
				ramp_candle_fixed_sell = 0.000039

				Max_ramp_MACD_fixed_sell = -0.000016
				Max_ramp_candle_fixed_sell = 0.000041

				ramp_buy_fixed = 0.00000

				coef_ramps_fixed_sell = -2.6
				diff_ramps_fixed_sell = 0.000049

				Max_coef_ramps_fixed_sell = -4.2
				Max_diff_ramps_fixed_sell = 0.000055

				st_Coef_fixed_sell = 1.0022
				tp_Coef_fixed_sell = 5

			elif (sym.name == 'USDCAD_i') | (sym.name == 'USDCAD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.078

				ramp_MACD_fixed_sell = -0.000011
				ramp_candle_fixed_sell = 0.000028

				Max_ramp_MACD_fixed_sell = -0.00001
				Max_ramp_candle_fixed_sell = 0.00001

				ramp_buy_fixed = 0.000009

				coef_ramps_fixed_sell = -2.2
				diff_ramps_fixed_sell = 0.00002

				Max_coef_ramps_fixed_sell = -5
				Max_diff_ramps_fixed_sell = 0.000035

				st_Coef_fixed_sell = 1.005
				tp_Coef_fixed_sell = 2.5

			elif (sym.name == 'USDCHF_i') | (sym.name == 'USDCHF'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK OK
				alfa_fixed_sell = 0.074

				ramp_MACD_fixed_sell = -0.000007
				ramp_candle_fixed_sell = 0.000018

				Max_ramp_MACD_fixed_sell = -0.000009
				Max_ramp_candle_fixed_sell = 0.00001

				ramp_buy_fixed = 0.000021

				coef_ramps_fixed_sell = -1.0
				diff_ramps_fixed_sell = 0.000024

				Max_coef_ramps_fixed_sell = -6
				Max_diff_ramps_fixed_sell = 0.00001

				st_Coef_fixed_sell = 1.0013
				tp_Coef_fixed_sell = 9.5

			elif (sym.name == 'USDJPY_i') | (sym.name == 'USDJPY'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.067

				ramp_MACD_fixed_sell = -0.0012
				ramp_candle_fixed_sell = 0.002

				Max_ramp_MACD_fixed_sell = -0.0013
				Max_ramp_candle_fixed_sell = 0.003

				ramp_buy_fixed = 0.0046

				coef_ramps_fixed_sell = -1.9
				diff_ramps_fixed_sell = 0.003

				Max_coef_ramps_fixed_sell = -9.8
				Max_diff_ramps_fixed_sell = 0.005

				st_Coef_fixed_sell = 1.0014
				tp_Coef_fixed_sell = 1.8

			elif (sym.name == 'USDSGD_i') | (sym.name == 'USDSGD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.047

				ramp_MACD_fixed_sell = -0.000005
				ramp_candle_fixed_sell = 0.000003

				Max_ramp_MACD_fixed_sell = -0.000003
				Max_ramp_candle_fixed_sell = 0.000009

				ramp_buy_fixed = 0.000007

				coef_ramps_fixed_sell = -2
				diff_ramps_fixed_sell = 0.000004

				Max_coef_ramps_fixed_sell = -35
				Max_diff_ramps_fixed_sell = 0.000009

				st_Coef_fixed_sell = 1.0012
				tp_Coef_fixed_sell = 5.5

			elif (sym.name == 'XAGUSD_i') | (sym.name == 'XAGUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = No OK
				alfa_fixed_sell = 1

				ramp_MACD_fixed_sell = 0
				ramp_candle_fixed_sell = 0

				Max_ramp_MACD_fixed_sell = 0
				Max_ramp_candle_fixed_sell = 0

				ramp_buy_fixed = 1

				coef_ramps_fixed_sell = 0
				diff_ramps_fixed_sell = 0

				Max_coef_ramps_fixed_sell = 0
				Max_diff_ramps_fixed_sell = 0

				st_Coef_fixed_sell = 1.005
				tp_Coef_fixed_sell = 1

			elif (sym.name == 'XAUUSD_i') | (sym.name == 'XAUUSD'):

				#************ BUY *******************    Final = 
				alfa_fixed_buy = 1

				ramp_MACD_fixed_buy = -1
				ramp_candle_fixed_buy = 1

				Max_ramp_MACD_fixed_buy = 0
				Max_ramp_candle_fixed_buy = -0

				ramp_sell_fixed = -1

				coef_ramps_fixed_buy = 1
				diff_ramps_fixed_buy =  -1

				Max_coef_ramps_fixed_buy = -0
				Max_diff_ramps_fixed_buy = 0

				st_Coef_fixed_buy = 0.9999
				tp_Coef_fixed_buy = 1

				#************ SELL *******************    Final = OK
				alfa_fixed_sell = 0.0709

				ramp_MACD_fixed_sell = -0.006
				ramp_candle_fixed_sell = 0.0014

				Max_ramp_MACD_fixed_sell = -0.003
				Max_ramp_candle_fixed_sell = 0.001

				ramp_buy_fixed = 0.015

				coef_ramps_fixed_sell = -3.5
				diff_ramps_fixed_sell = 0.0057

				Max_coef_ramps_fixed_sell = -8.2
				Max_diff_ramps_fixed_sell = 0.005

				st_Coef_fixed_sell = 1.004
				tp_Coef_fixed_sell = 12


			#****************--------------------++++++++++++++++++++++++***** 1M BUY ***********************************************************++++++++++++++++++++++
			#log_multi_account(1001)
			#try:
			if True:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_5M_BUY = window_counter_5M
								end_search_counter = search_counter_5M_BUY + 12

								if (end_search_counter > (len(symbol_data_5M[sym.name]['low'])-1)):
									end_search_counter = len(symbol_data_5M[sym.name]['low']) - 1

								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_5M_BUY <= end_search_counter):


									if True:#(((symbol_data_1M[sym.name]['low'][(search_counter_1M_BUY)] > symbol_data_1M[sym.name]['low'][(search_counter_1M_BUY-1)]))):
										#print('1M Position = ',search_counter_1M_BUY)
										#print('Signal 5M = ',MACD_signal_cross_5M_sell['signal'])
										if True:#(((symbol_data_5M[sym.name]['low'][search_counter_5M_BUY - 2] < symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-3)])
											#& (symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-1)] <= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-2)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] > symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-1)]))

											#| ((symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-3)] < symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-4)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2] < symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-3)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-1] >= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-2)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] >= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-1)]))

											#| ((symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-4)] <= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-5)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-3] < symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-4)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2] >= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-3)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-1] >= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-2)])
											#& (symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] >= symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY-1)]))):

											#print('5M Pass')
											
											if True:#(((symbol_data_15M[sym.name]['low'][window_counter_15M - 2] < symbol_data_15M[sym.name]['low'][(window_counter_15M-3)]))
												#& ((symbol_data_15M[sym.name]['low'][(window_counter_15M-1)] <= symbol_data_15M[sym.name]['low'][(window_counter_15M-2)]))
												#& ((symbol_data_15M[sym.name]['low'][window_counter_15M] > symbol_data_15M[sym.name]['low'][(window_counter_15M-1)]))):

												#print('15M Pass')
												#hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

												#time_4H_1 = 0
												#time_4H_2 = 4
												#time_4H_3 = 8
												#time_4H_4 = 12
												#time_4H_5 = 16
												#time_4H_6 = 20

												#if (((hour_5M - time_4H_1) >= 0) & ((hour_5M - time_4H_1) <= 3)):
													#hour_4H = 0
												#elif (((hour_5M - time_4H_2) >= 0) & ((hour_5M - time_4H_2) <= 3)):
													#hour_4H = 4
												#elif (((hour_5M - time_4H_3) >= 0) & ((hour_5M - time_4H_3) <= 3)):
													#hour_4H = 8
												#elif (((hour_5M - time_4H_4) >= 0) & ((hour_5M - time_4H_4) <= 3)):
													#hour_4H = 12
												#elif (((hour_5M - time_4H_5) >= 0) & ((hour_5M - time_4H_5) <= 3)):
													#hour_4H = 16
												#elif (((hour_5M - time_4H_6) >= 0) & ((hour_5M - time_4H_6) <= 3)):
													#hour_4H = 20

												if True:#((symbol_data_4H[sym.name]['low'][(window_counter_4H)] <= symbol_data_4H[sym.name]['low'][(window_counter_4H-1)])):

													if True:#(((symbol_data_1H[sym.name]['low'][(window_counter_1H)] < symbol_data_1H[sym.name]['low'][(window_counter_1H-1)]))):

														hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

														time_4H_1 = 0
														time_4H_2 = 4
														time_4H_3 = 8
														time_4H_4 = 12
														time_4H_5 = 16
														time_4H_6 = 20

														if (((hour_5M - time_4H_1) >= 0) & ((hour_5M - time_4H_1) <= 3)):
															hour_4H = 0
														elif (((hour_5M - time_4H_2) >= 0) & ((hour_5M - time_4H_2) <= 3)):
															hour_4H = 4
														elif (((hour_5M - time_4H_3) >= 0) & ((hour_5M - time_4H_3) <= 3)):
															hour_4H = 8
														elif (((hour_5M - time_4H_4) >= 0) & ((hour_5M - time_4H_4) <= 3)):
															hour_4H = 12
														elif (((hour_5M - time_4H_5) >= 0) & ((hour_5M - time_4H_5) <= 3)):
															hour_4H = 16
														elif (((hour_5M - time_4H_6) >= 0) & ((hour_5M - time_4H_6) <= 3)):
															hour_4H = 20

														min_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].minute

														diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

														if (int(diff_5M_U_4H) < 0):
															diff_5M_U_4H = 0

														if (min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)-1):search_counter_5M_BUY]) <= min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)-48-1):search_counter_5M_BUY-48])):
															#print('4H Pass')
															#print('Pre')

															macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)[0:search_counter_5M_BUY+1]

															macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
																#print(macd_5M_sell)
															macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
															macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]


															macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)[0:search_counter_5M_BUY+1]

															macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
																#print(macd_5M_sell)
															macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
															macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]


															ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
																		tenkan=9,kijun=26,snkou=52)[0:search_counter_5M_BUY+1]
															SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]][0:search_counter_5M_BUY+1]
															SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]][0:search_counter_5M_BUY+1]
															tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:search_counter_5M_BUY+1]
															kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:search_counter_5M_BUY+1]
															chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]][0:search_counter_5M_BUY+1]


															sma_288_5M = ind.sma(symbol_data_5M[sym.name]['HLCC/4'],length=288)[0:search_counter_5M_BUY+1]

															sma_48_5M = ind.sma(symbol_data_5M[sym.name]['HLCC/4'],length=48)[0:search_counter_5M_BUY+1]

															sma_168_5M = ind.sma(symbol_data_5M[sym.name]['HLCC/4'],length=168)[0:search_counter_5M_BUY+1]

															sma_2304_5M = ind.sma(symbol_data_5M[sym.name]['HLCC/4'],length=2304)[0:search_counter_5M_BUY+1]


															if True:#((MACD_signal_cross_5M_sell_now['signal'] == 'sell') | (MACD_signal_cross_5M_sell_now['signal'] == 'faild_sell')):

																#print('1M last = ',symbol_data_1M[sym.name]['time'][search_counter_1M_BUY])

																#print('5M last = ',symbol_data_5M[sym.name]['time'][window_counter_5M])
				
																#print('5M cross = ',symbol_data_5M[sym.name]['time'][MACD_signal_cross_5M_sell_now['index']])

																#print('window_counter_5M = ',window_counter_5M)
																#print('MACD_signal_cross_5M_sell_now = ',MACD_signal_cross_5M_sell_now['index'])

																hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

																time_4H_1 = 0
																time_4H_2 = 4
																time_4H_3 = 8
																time_4H_4 = 12
																time_4H_5 = 16
																time_4H_6 = 20

																if (((hour_5M - time_4H_1) >= 0) & ((hour_5M - time_4H_1) <= 3)):
																	hour_4H = 0
																elif (((hour_5M - time_4H_2) >= 0) & ((hour_5M - time_4H_2) <= 3)):
																	hour_4H = 4
																elif (((hour_5M - time_4H_3) >= 0) & ((hour_5M - time_4H_3) <= 3)):
																	hour_4H = 8
																elif (((hour_5M - time_4H_4) >= 0) & ((hour_5M - time_4H_4) <= 3)):
																	hour_4H = 12
																elif (((hour_5M - time_4H_5) >= 0) & ((hour_5M - time_4H_5) <= 3)):
																	hour_4H = 16
																elif (((hour_5M - time_4H_6) >= 0) & ((hour_5M - time_4H_6) <= 3)):
																	hour_4H = 20

																min_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].minute

																diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																#print('diff_5M_U_4H 1 = ',diff_5M_U_4H)
																#print(window_counter_5M)
																#print('diff time = ',symbol_data_5M[sym.name]['time'][diff_5M_U_4H])

																if (search_counter_5M_BUY - int(diff_5M_U_4H)) < (search_counter_5M_BUY-5):
																	protect_buy_find_5M = min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY])

																	counter_index_min = search_counter_5M_BUY
																	for min_low_candle_find in symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY]:
																		#print(min_low_candle_find)
																		#print(protect_buy_find_5M)
																		if min_low_candle_find == protect_buy_find_5M:
																			counter_min_find = counter_index_min
																			#print(min_low_candle_find)
																			#print(protect_buy_find_5M)
																			#print('count = ',counter_index_min)
																		counter_index_min -= 1
																	flag_min_find = 0


																	while (counter_min_find >= (search_counter_5M_BUY - int(diff_5M_U_4H))):
																		if (macd_5M_buy[counter_min_find - 1] <= macd_5M_buy[counter_min_find]):
																			min_macd_find = macd_5M_buy[counter_min_find - 1]
																			flag_min_find += 1
																			#print('flag_max_find = ',flag_max_find)
																		if ((macd_5M_buy[counter_min_find - 2] > macd_5M_buy[counter_min_find - 1]) & (flag_min_find >= 2)
																			& (macd_5M_buy[counter_min_find - 3] > macd_5M_buy[counter_min_find - 1])):
																			min_macd_div_2 = min_macd_find
																			break
																		else:
																			min_macd_div_2 = 10000
																		counter_min_find -= 1

																	#max_macd_div_2 = max(macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])

																	#min_candle_2 = min(symbol_data_5M[sym.name]['low'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	#print('min_macd_div_2 = ',min_macd_div_2)
																	index_counter = (search_counter_5M_BUY - int(diff_5M_U_4H))
																	for i in macd_5M_buy[(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY]:
																		if (i == min_macd_div_2):
																			min_macd_div_2_index = index_counter
																			break
																		else:
																			min_macd_div_2_index = 1
																		index_counter += 1

																	min_candle_2 = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY]
																	min_candle_2_index = search_counter_5M_BUY

																	min_candle_2_line = symbol_data_5M[sym.name]['low'][min_macd_div_2_index]
																	min_candle_2_index_line = min_macd_div_2_index

																else:
																	protect_buy_find_1M = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY]
																	min_macd_div_2 = macd_5M_buy[search_counter_5M_BUY]
																	min_macd_div_2_index = search_counter_5M_BUY

																	min_candle_2 = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY]
																	min_candle_2_index = search_counter_5M_BUY

																	min_candle_2_line = symbol_data_5M[sym.name]['low'][min_macd_div_2_index]
																	min_candle_2_index_line = min_macd_div_2_index




																low_counter_4H = 1
																counter_for_low = 48
																while (counter_for_low < 145):
																	if ((search_counter_5M_BUY - int(diff_5M_U_4H)-counter_for_low-1) < (search_counter_5M_BUY - 1)): break
																	if (min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)-1):search_counter_5M_BUY]) <= min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - int(diff_5M_U_4H)-counter_for_low-1):search_counter_5M_BUY-counter_for_low])):
																		low_counter_4H += 1
																	counter_for_low += 1

																hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

																#print('low_counter_4H = ',low_counter_4H)

																time_4H_1 = 0
																time_4H_2 = 4
																time_4H_3 = 8
																time_4H_4 = 12
																time_4H_5 = 16
																time_4H_6 = 20

																if (((hour_5M - time_4H_1 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_1 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 0
																elif (((hour_5M - time_4H_2 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_2 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 4
																elif (((hour_5M - time_4H_3 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_3 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 8
																elif (((hour_5M - time_4H_4 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_4 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 12
																elif (((hour_5M - time_4H_5 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_5 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 16
																elif (((hour_5M - time_4H_6 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_6 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 20

																min_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].minute

																diff_5M_U_4H = (abs(hour_5M - hour_4H) * 12) #+ (min_5M/5)

																#print('diff_5M_U_4H 2 = ',diff_5M_U_4H)


																#hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																#hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																#min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																#diff_5M_U_4H_end = (abs(hour_5M - hour_4H) * 12) + int(min_5M/5) + 1


																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																#print('int(diff_5M_U_4H) = ',int(diff_5M_U_4H))
																#print(((min_macd_div_2_index - 1) - int(diff_5M_U_4H)))

																if ((((min_macd_div_2_index - 1) - int(diff_5M_U_4H)) < ((min_macd_div_2_index - 1))) & (min_macd_div_2_index != 1)):
																	#print('in if')
																	min_macd_div_1 = min(macd_5M_buy[((min_macd_div_2_index - 1) - int(diff_5M_U_4H)):(min_macd_div_2_index - 1)])
																	

																	#print('min_candle_1 = ',min_candle_1)

																	index_counter = ((min_macd_div_2_index - 1) - int(diff_5M_U_4H))
																	for i in macd_5M_buy[((min_macd_div_2_index - 1) - int(diff_5M_U_4H)):(min_macd_div_2_index - 1)]:
																		if (i == min_macd_div_1):
																			min_macd_div_1_index = index_counter
																		index_counter += 1

																	min_candle_1 = symbol_data_5M[sym.name]['low'][min_macd_div_1_index]
																	min_candle_1_index = min_macd_div_1_index

																else:
																	search_counter_5M_BUY += 1
																	#print('continue 1')
																	continue
																	min_macd_div_1 = macd_5M_buy[(min_macd_div_2_index - 1)]
																	min_macd_div_1_index = (min_macd_div_2_index - 1)

																	min_candle_1 = symbol_data_5M[sym.name]['low'][min_macd_div_1_index]
																	min_candle_1_index = min_macd_div_1_index

																#print('max_macd_div_1 = ',max_macd_div_1)
																#print('max_macd_div_2 = ',max_macd_div_2)

																#print('max_macd_div_1_index = ',max_macd_div_1_index)
																#print('max_macd_div_2_index = ',max_macd_div_2_index)

																if ((min_macd_div_2_index-min_macd_div_1_index) >= 1):
																	ramp = ((min_macd_div_2 - min_macd_div_1)/(min_macd_div_2_index-min_macd_div_1_index))

																if ((min_candle_2_index-min_candle_1_index) >= 1):
																	ramp_candle = ((min_candle_2 - min_candle_1)/(min_candle_2_index-min_candle_1_index))

																if ((min_candle_2_index_line-min_candle_1_index) >= 1):
																	ramp_candle_line = ((min_candle_2_line - min_candle_1)/(min_candle_2_index_line-min_candle_1_index))

																	protect_line = ramp_candle_line * ((search_counter_5M_BUY) - min_candle_1_index) + min_candle_1
																else:
																	protect_line = 0



																#+ ((symbol_data_4H[sym.name]['HLC/3'][window_counter_4H-1]) * (0.5 * ramp_candle))#symbol_data_4H[sym.name]['close'][window_counter_4H-1] + (abs(symbol_data_4H[sym.name]['open'][window_counter_4H-1] - symbol_data_4H[sym.name]['close'][window_counter_4H-1]) * 0.6) #- symbol_data_5M[sym.name]['high'][window_counter_5M])/2) + symbol_data_5M[sym.name]['high'][window_counter_5M]

																#print('1 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

																#protect_buy_find_5M = min(symbol_data_5M[sym.name]['low'][(search_counter_5M_BUY - 3):search_counter_5M_BUY])

																protect_buy_find_5M = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] * 0.9997

																#if ((abs(protect_buy_find_5M-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY])/protect_buy_find_5M)*100 >= 0.05):
																#	protect_buy_find_5M = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] * 0.9997

																dangrouse_line = protect_buy_find_5M + (((protect_buy_find_5M)*alfa_fixed_buy)/100)

																

																alfa = ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] - protect_buy_find_5M)/(protect_buy_find_5M)) * 100


																#print(dangrouse_line)
																#print('alfa = ', alfa)
																#print('high = ',symbol_data_5M[sym.name]['high'][window_counter_5M])
																#print('protect_buy_find_1M = ',protect_buy_find_1M)
																#print('alfa = ',alfa)

																if (ramp != 0):
																	Coef_ramps = (ramp_candle/ramp)
																else:
																	Coef_ramps = 0

																diff_ramps = (abs(ramp_candle)-ramp)

																
																protect_buy_find_5M = protect_buy_find_5M * 0.9996

																#resist_buy_find_5M = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] + ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]-protect_buy_find_5M)*5)
																#resist_buy_find_5M = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] + (((((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]-protect_buy_find_5M)/symbol_data_5M[sym.name]['high'][window_counter_5M]))*tp_first_Coef_fixed_buy) * symbol_data_5M[sym.name]['high'][window_counter_5M])

																if((min_macd_div_2_index-1)-(min_macd_div_1_index+1)>0):
																	resist_buy_find_5M = ((max(symbol_data_5M[sym.name]['high'][(min_macd_div_1_index+1):(min_macd_div_2_index-1)]) - symbol_data_5M[sym.name]['high'][min_macd_div_1_index]) * tp_first_Coef_fixed_buy) + symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]
																	protect_buy_find_5M = symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] - ((max(symbol_data_5M[sym.name]['high'][(min_macd_div_1_index+1):(min_macd_div_2_index-1)]) - symbol_data_5M[sym.name]['high'][min_macd_div_1_index]) * 2)
																	protect_buy_find_5M = protect_buy_find_5M * 0.999
																else:
																	resist_buy_find_5M = 0
																	protect_buy_find_5M = 0
																#protect_buy_find_5M = protect_buy_find_5M * 0.998#st_Coef_fixed_buy


																if False:#(((((resist_buy_find_5M - symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])/symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])*100) >= 0.07)):
																	if ((ramp >= Max_ramp_MACD_fixed_buy) | (ramp_candle <= Max_ramp_MACD_fixed_buy) | (Coef_ramps <= Max_coef_ramps_fixed_buy) | (diff_ramps >= Max_diff_ramps_fixed_buy)):
																		if (ramp >= Max_ramp_MACD_fixed_buy):
																			logging.debug('ramp = %f'%ramp)
																		if(ramp_candle >= abs(Max_ramp_MACD_fixed_buy)):
																			logging.debug('ramp_candle = %f'%ramp_candle)
																		if(Coef_ramps <= Max_coef_ramps_fixed_buy):
																			logging.debug('Coef_ramps = %f'%Coef_ramps)
																		if(diff_ramps >= Max_diff_ramps_fixed_buy):
																			logging.debug('diff_ramps = %f'%diff_ramps)
																		if False:#(tp_Coef_fixed_buy != 1):
																			resist_buy_find_5M = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] + (((((resist_buy_find_5M - symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])/symbol_data_5M[sym.name]['high'][window_counter_5M]))/tp_Coef_fixed_buy) * symbol_data_5M[sym.name]['high'][window_counter_5M])
																			#print('2 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

																


																

																	#print('ramp = ',ramp)

																




																# Sell Check ***********************************************************

																hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

																time_4H_1 = 0
																time_4H_2 = 4
																time_4H_3 = 8
																time_4H_4 = 12
																time_4H_5 = 16
																time_4H_6 = 20

																if (((hour_5M - time_4H_1) >= 0) & ((hour_5M - time_4H_1) <= 3)):
																	hour_4H = 0
																elif (((hour_5M - time_4H_2) >= 0) & ((hour_5M - time_4H_2) <= 3)):
																	hour_4H = 4
																elif (((hour_5M - time_4H_3) >= 0) & ((hour_5M - time_4H_3) <= 3)):
																	hour_4H = 8
																elif (((hour_5M - time_4H_4) >= 0) & ((hour_5M - time_4H_4) <= 3)):
																	hour_4H = 12
																elif (((hour_5M - time_4H_5) >= 0) & ((hour_5M - time_4H_5) <= 3)):
																	hour_4H = 16
																elif (((hour_5M - time_4H_6) >= 0) & ((hour_5M - time_4H_6) <= 3)):
																	hour_4H = 20

																min_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].minute

																diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																#print(diff_5M_U_4H)
																#print(window_counter_5M)
																#print('diff time = ',symbol_data_5M[sym.name]['time'][diff_5M_U_4H])

																if (search_counter_5M_BUY - int(diff_5M_U_4H)) < (search_counter_5M_BUY-5):
																	protect_sell_find_1M = max(symbol_data_5M[sym.name]['high'][(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY])

																	counter_index_max = search_counter_5M_BUY
																	for max_low_candle_find in symbol_data_5M[sym.name]['high'][(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY]:
																		#print(min_low_candle_find)
																		#print(protect_buy_find_5M)
																		if max_low_candle_find == protect_sell_find_1M:
																			counter_max_find = counter_index_max
																			#print(min_low_candle_find)
																			#print(protect_buy_find_5M)
																			#print('count = ',counter_index_min)
																		counter_index_max -= 1
																	flag_max_find = 0

																	#print('counter_max_find = ',counter_max_find)
																	#print('last = ',(window_counter_5M - int(diff_5M_U_4H)))

																	while (counter_max_find >= (search_counter_5M_BUY - int(diff_5M_U_4H))):
																		if (macd_5M_sell[counter_max_find - 1] >= macd_5M_sell[counter_max_find]):
																			max_macd_find = macd_5M_sell[counter_max_find - 1]
																			flag_max_find += 1
																			#print('flag_max_find = ',flag_max_find)
																		if ((macd_5M_sell[counter_max_find - 2] < macd_5M_sell[counter_max_find - 1]) & (flag_max_find >= 2)
																			& (macd_5M_sell[counter_max_find - 3] < macd_5M_sell[counter_max_find - 1])):
																			max_macd_div_2 = max_macd_find
																			break
																		else:
																			max_macd_div_2 = 10000
																		counter_max_find -= 1

																	#max_macd_div_2 = max(macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])

																	#min_candle_2 = min(symbol_data_5M[sym.name]['low'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	#print('min_macd_div_2 = ',min_macd_div_2)
																	index_counter = (search_counter_5M_BUY - int(diff_5M_U_4H))
																	for i in macd_5M_sell[(search_counter_5M_BUY - int(diff_5M_U_4H)):search_counter_5M_BUY]:
																		if (i == max_macd_div_2):
																			max_macd_div_2_index = index_counter
																			break
																		else:
																			max_macd_div_2_index = 1
																		index_counter += 1

																	max_candle_2 = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]
																	max_candle_2_index = search_counter_5M_BUY

																	max_candle_2_line = symbol_data_5M[sym.name]['high'][max_macd_div_2_index]
																	max_candle_2_index_line = max_macd_div_2_index

																else:
																	protect_sell_find_1M = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]
																	max_macd_div_2 = macd_5M_sell[search_counter_5M_BUY]
																	max_macd_div_2_index = search_counter_5M_BUY

																	max_candle_2 = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]
																	max_candle_2_index = search_counter_5M_BUY

																	max_candle_2_line = symbol_data_5M[sym.name]['high'][max_macd_div_2_index]
																	max_candle_2_index_line = max_macd_div_2_index



																low_counter_4H = 1
																counter_for_low = 48
																while (counter_for_low < 145):
																	if ((search_counter_5M_BUY - int(diff_5M_U_4H)-counter_for_low-1) < (search_counter_5M_BUY-1)): break
																	if (max(symbol_data_5M[sym.name]['high'][(search_counter_5M_BUY - int(diff_5M_U_4H)-1):search_counter_5M_BUY]) >= min(symbol_data_5M[sym.name]['high'][(search_counter_5M_BUY - int(diff_5M_U_4H)-counter_for_low-1):search_counter_5M_BUY-counter_for_low])):
																		low_counter_4H += 1
																	counter_for_low += 1

																hour_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].hour

																time_4H_1 = 0
																time_4H_2 = 4
																time_4H_3 = 8
																time_4H_4 = 12
																time_4H_5 = 16
																time_4H_6 = 20

																if (((hour_5M - time_4H_1 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_1 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 0
																elif (((hour_5M - time_4H_2 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_2 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 4
																elif (((hour_5M - time_4H_3 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_3 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 8
																elif (((hour_5M - time_4H_4 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_4 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 12
																elif (((hour_5M - time_4H_5 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_5 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 16
																elif (((hour_5M - time_4H_6 - (low_counter_4H*4)) >= 0) & ((hour_5M - time_4H_6 - (low_counter_4H*4)) <= 3)):
																	hour_4H = 20

																min_5M = symbol_data_5M[sym.name]['time'][search_counter_5M_BUY].minute

																diff_5M_U_4H = (abs(hour_5M - hour_4H) * 12) #+ (min_5M/5)


																#hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																#hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																#min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																#diff_5M_U_4H_end = (abs(hour_5M - hour_4H) * 12) + int(min_5M/5) + 1

																#print(diff_5M_U_4H)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																if ((((max_macd_div_2_index - 1) - int(diff_5M_U_4H)) < ((max_macd_div_2_index - 1))) & (max_macd_div_2_index != 1)):
																	max_macd_div_1 = max(macd_5M_sell[((max_macd_div_2_index - 1) - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)])
																	

																	#print('min_candle_1 = ',min_candle_1)

																	index_counter = ((max_macd_div_2_index - 1) - int(diff_5M_U_4H))
																	for i in macd_5M_sell[((max_macd_div_2_index - 1) - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)]:
																		if (i == max_macd_div_1):
																			max_macd_div_1_index = index_counter
																		index_counter += 1

																	max_candle_1 = symbol_data_5M[sym.name]['high'][max_macd_div_1_index]
																	max_candle_1_index = max_macd_div_1_index

																else:
																	search_counter_5M_BUY += 1
																	#print('continue 2')
																	continue
																	max_macd_div_1 = macd_5M_sell[(max_macd_div_2_index - 1)]
																	max_macd_div_1_index = (max_macd_div_2_index - 1)

																	max_candle_1 = symbol_data_5M[sym.name]['high'][max_macd_div_1_index]
																	max_candle_1_index = max_macd_div_1_index

																#print('max_macd_div_1 = ',max_macd_div_1)
																#print('max_macd_div_2 = ',max_macd_div_2)

																#print('max_macd_div_1_index = ',max_macd_div_1_index)
																#print('max_macd_div_2_index = ',max_macd_div_2_index)

																if ((max_macd_div_2_index-max_macd_div_1_index) >= 1):
																	ramp_sell = ((max_macd_div_2 - max_macd_div_1)/(max_macd_div_2_index-max_macd_div_1_index))
																else:
																	ramp_sell = 0

																if ((max_candle_2_index-max_candle_1_index) >= 1):
																	ramp_candle_sell = ((max_candle_2 - max_candle_1)/(max_candle_2_index-max_candle_1_index))
																else:
																	ramp_candle_sell = 0

																if ((max_candle_2_index_line-max_candle_1_index) >= 1):
																	ramp_candle_line_sell = ((max_candle_2_line - max_candle_1)/(max_candle_2_index_line-max_candle_1_index))

																	protect_line_sell = ramp_candle_line_sell * ((search_counter_5M_BUY) - max_candle_1_index) + max_candle_1
																else:
																	protect_line_sell = 0



																#print('min_macd_div_2 = ',min_macd_div_2)
																#print('min_macd_div_1 = ',min_macd_div_1)

																#print('dangrouse_line = ',dangrouse_line)
																#print('symbol_data_5M[sym.name][low] = ',symbol_data_5M[sym.name]['high'][window_counter_5M])
																#print('0')



																


																#print('1')
																if (ramp_candle <= ramp_candle_fixed_buy):
																	if True:#(symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] <= dangrouse_line):

																		#print('2')
																		if (ramp >= ramp_MACD_fixed_buy):
																			#print('4')
																			if (Coef_ramps <= coef_ramps_fixed_buy):
																				#print('5')

																				if (ramp_sell <= ramp_sell_fixed):
																					#print('3')
																					#print('6')
																					if True:#(diff_ramps >= diff_ramps_fixed_buy):
																						#print('7')
																						if (alfa <= alfa_fixed_buy):
																							#print('8')
																							#print('rsi = ',ind.rsi(symbol_data_5M[sym.name]['OHLC/4'],48)[search_counter_5M_BUY])
																							if (ind.rsi(symbol_data_5M[sym.name]['OHLC/4'], length=14)[search_counter_5M_BUY] < 40):

																								#Vol_1 = statistics.mean(symbol_data_5M[sym.name]['volume'][(search_counter_5M_BUY-90):search_counter_5M_BUY])
																								#Vol_2 = statistics.mean(symbol_data_5M[sym.name]['volume'][(search_counter_5M_BUY-180):(search_counter_5M_BUY-90)])

																								
																								Vol_1 = (symbol_data_5M[sym.name]['volume'][min_macd_div_1_index])
																								Vol_2 = (symbol_data_5M[sym.name]['volume'][search_counter_5M_BUY])
																								if Vol_1 > (Vol_2 * Vol_Coef_Fixed_buy):

																									if True:#(((symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] - sma_168_5M[len(sma_168_5M)-1]) >= (sma_168_5M_fixed_high)) & ((symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] - sma_168_5M[len(sma_168_5M)-1]) < (sma_168_5M_fixed_low))):
				
																										if True:#((symbol_data_5M[sym.name]['low'][search_counter_5M_BUY] >= sma_2304_5M[len(sma_2304_5M)-1])):
																											#print('10')

																											if True:#((symbol_data_1M[sym.name]['high'][search_counter_1M_BUY] <= SPANA_1M[search_counter_1M_BUY]) & (symbol_data_1M[sym.name]['high'][search_counter_1M_BUY] <= SPANB_1M[search_counter_1M_BUY])):

																												if True:#((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] <= SPANA_5M[search_counter_5M_BUY]) & (symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] <= SPANB_5M[search_counter_5M_BUY])):

																													flag_cross_5M = 'buy'

																													signal_counter_5M_buy = search_counter_5M_BUY

																													if (flag_cross_5M == 'buy'): 
																														print('flag_cross_5M = ',flag_cross_5M)

																													#***************************************************** 1M SELL ******************************************************************
																													if (flag_cross_5M == 'buy'):

																														if (((((resist_buy_find_5M - symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])/symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])*100) >= 0.07)):
																															if ((ramp >= Max_ramp_MACD_fixed_buy) | (ramp_candle <= Max_ramp_candle_fixed_buy) | (Coef_ramps <= Max_coef_ramps_fixed_buy) | (diff_ramps >= Max_diff_ramps_fixed_buy)):
																																#logging.debug('******************************** Tp Check *************************')
																																#if (ramp >= Max_ramp_MACD_fixed_buy):
																																#	logging.debug('ramp = %f'%ramp)
																																#if(ramp_candle <= Max_ramp_candle_fixed_buy):
																																#	logging.debug('ramp_candle = %f'%ramp_candle)
																																#if(Coef_ramps <= Max_coef_ramps_fixed_buy):
																																#	logging.debug('Coef_ramps = %f'%Coef_ramps)
																																#if(diff_ramps >= Max_diff_ramps_fixed_buy):
																																#	logging.debug('diff_ramps = %f'%diff_ramps)
																																#logging.debug('******************************** Tp Check *************************')
																																if (tp_Coef_fixed_buy != 1):
																																	#resist_buy_find_5M = symbol_data_5M[sym.name]['high'][search_counter_5M_BUY] + (((((resist_buy_find_5M - symbol_data_5M[sym.name]['high'][search_counter_5M_BUY])/symbol_data_5M[sym.name]['high'][window_counter_5M]))/tp_Coef_fixed_buy) * symbol_data_5M[sym.name]['high'][window_counter_5M])
																																	resist_buy_find_5M = ((max(symbol_data_5M[sym.name]['high'][(min_macd_div_1_index+1):(min_macd_div_2_index-1)]) - symbol_data_5M[sym.name]['high'][min_macd_div_1_index]) * (tp_first_Coef_fixed_buy-tp_Coef_fixed_buy)) + symbol_data_5M[sym.name]['high'][search_counter_5M_BUY]

																														if (resist_buy_find_5M < protect_buy_find_5M): 
																															search_counter_5M_BUY += 1
																															continue

																														#************************************************ 1M Top Low Touched ************************************************************

																														print('////////////// flag_cross_5M = ',flag_cross_5M)

																														if (flag_cross_5M == 'buy'):

																															if (sym.name == 'XAUUSD_i'):
																																#data_macd_1M_buy['tp'] = min(resist_buy_find_1M,(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]*1.001))
																																data_macd_5M_buy['tp'] = resist_buy_find_5M * 0.9993
																															else:
																																data_macd_5M_buy['tp'] = resist_buy_find_5M * 0.9993



																															data_macd_5M_buy['st'] = protect_buy_find_5M

					

																															if data_macd_5M_buy['tp'] > symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]: 
																																#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
																																#continue

																																counter_i = signal_counter_5M_buy
																																final_index = (signal_counter_5M_buy + 5760)

																																flag_index = 1

																																if (final_index ) >= len(symbol_data_5M[sym.name]['close'])-1:
																																	final_index = len(symbol_data_5M[sym.name]['close'])-1
																																	flag_index = 0



																																counter_j = 0

																																percentage_buy_tp = {}
																																percentage_buy_st = {}


																																while (counter_i <= final_index):
																																	percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][signal_counter_5M_buy])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]) * 100
																																	percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][signal_counter_5M_buy] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]) * 100

																															#print(percentage_buy_tp[counter_j])
																															##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

																																	if (percentage_buy_tp[counter_j] >= (((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]-data_macd_5M_buy['tp'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]))*100)):
																																		#print('test_tp_break')
																																		logging.debug('SUCCSESSFULLY Break')
																																		break

																																	#print(abs(percentage_buy_st[counter_j]))

																																	if (abs(percentage_buy_st[counter_j]) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]-data_macd_5M_buy['st'])/data_macd_5M_buy['st']))*100)):
																																		#print('test_tp_break')
																																		logging.debug('Failled Break')
																																		break

																																	counter_i += 1
																																	counter_j += 1

							

																																	#if (counter_j > 50): break

																																try:
																																	percentage_buy_tp_save_5M = max(percentage_buy_tp.values())
																																	percentage_buy_st_save_5M = max(percentage_buy_st.values())
																																except:
																																	percentage_buy_tp_save_5M = 0
																																	percentage_buy_st_save_5M = 0

																																logging.debug('************************ OUT_1M buy *******************************')

																																if (abs(percentage_buy_tp_save_5M) >= (((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]-data_macd_5M_buy['tp'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]))*100)):
																																	logging.debug('buy_5M = SUCCSESSFULLY')
																																	logging.debug('------------------------%s' %sym.name)

																																	if ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] <= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])) #pin Bar
																																		| (((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] >= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]))): #pin Bar
																																		logging.debug('Pin Bar')

																																	if ((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3] > symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3])): #inGolf
																																		logging.debug('InGolf')
																																	
																																	if ((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3] > symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) 
																																		& ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] <= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])) #pin Bar
																																		| (((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] >= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]))) #pin Bar
																																		& (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1])
																																		& (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2])):
																																		logging.debug('three Candle')

																																	logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]-data_macd_5M_buy['tp'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]))*100))
																																	logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]-data_macd_5M_buy['st'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]))*100))
																																	#logging.debug('tp resist_buy_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_1D)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																	#logging.debug('tp resist_buy_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_4H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																	#logging.debug('tp resist_buy_find_1H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_1H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																	#logging.debug('tp resist_buy_find_30M = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_30M)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))

																																	#logging.debug('st Protect_buy_find = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))
																																	#logging.debug('st Protect_buy_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find_1D)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))
																																	#logging.debug('st Protect_buy_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find_4H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))

																																	#logging.debug('signal_counter_5M1H_buy = %f'%(signal_counter_1M_buy - MACD_signal_cross_1M_buy['index']))

																																	#logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
																																	logging.debug('signal_counter_1M_buy[] = %s'%symbol_data_5M[sym.name]['time'][signal_counter_5M_buy])

																																	logging.debug('RSI = %f'%ind.rsi(symbol_data_5M[sym.name]['OHLC/4'], length=48)[search_counter_5M_BUY])

																																	logging.debug('Vol_Coef_Suc = %f'%(Vol_1/Vol_2))


							

																																	Profit_Plus_now = (((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]-data_macd_5M_buy['tp'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]))*100) * 10
																																	Profit_Plus = Profit_Plus + Profit_Plus_now

							



																																	SUCCSESSFULLY += 1

																																	ramp_Suc[SUCCSESSFULLY] = ramp
																																	ramp_candle_Suc[SUCCSESSFULLY] = ramp_candle

																																	Vol_Coef_Suc[SUCCSESSFULLY] = (Vol_1/Vol_2)

																																	ramp_Suc_sell[SUCCSESSFULLY] = ramp_sell
																																	ramp_candle_Suc_sell[SUCCSESSFULLY] = ramp_candle_sell

																																	alfa_SUC[SUCCSESSFULLY] = alfa

																																	st_Suc[SUCCSESSFULLY] = percentage_buy_st_save_5M

																																	logging.debug('FiS = %d'%SUCCSESSFULLY)
																																	logging.debug('FiF = %d'%FAILED)

																																	logging.debug('alfa = %f'%(alfa))

																																	#logging.debug('alfa_SUC_tot = %f'%(alfa_SUC[SUCCSESSFULLY]))
																																	logging.debug('ramp_Suc = %f'%(ramp_Suc[SUCCSESSFULLY]))
																																	logging.debug('ramp_candle_Suc = %f'%(ramp_candle_Suc[SUCCSESSFULLY]))

																																	logging.debug('ramp_Suc_sell = %f'%(ramp_Suc_sell[SUCCSESSFULLY]))
																																	logging.debug('ramp_candle_Suc_sell = %f'%(ramp_candle_Suc_sell[SUCCSESSFULLY]))

																																	dif_ramps_Suc[SUCCSESSFULLY] = (abs(ramp_candle_Suc[SUCCSESSFULLY])-ramp_Suc[SUCCSESSFULLY])
																																	Coef_ramps_Suc[SUCCSESSFULLY] = (ramp_candle_Suc[SUCCSESSFULLY]/ramp_Suc[SUCCSESSFULLY])

																																	logging.debug('dif_ramps_Suc = %f'%(dif_ramps_Suc[SUCCSESSFULLY]))
																																	logging.debug('Coef_ramps_Suc = %f'%(Coef_ramps_Suc[SUCCSESSFULLY]))

																																	logging.debug('dif_SMA_288 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_288_5M[len(sma_288_5M)-1]))

																																	logging.debug('dif_SMA_48 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_48_5M[len(sma_48_5M)-1]))

																																	logging.debug('dif_SMA_168 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_168_5M[len(sma_168_5M)-1]))

																																	logging.debug('PP = %f'%Profit_Plus)
																																	logging.debug('PM = %f'%Profit_Minus)
																																	logging.debug('PT = %f'%(Profit_Plus - Profit_Minus))

																																	logging.debug('')
																																	logging.debug('min_candle_2_index = %s'%symbol_data_5M[sym.name]['time'][min_candle_2_index])
																																	logging.debug('min_candle_1_index = %s'%symbol_data_5M[sym.name]['time'][min_candle_1_index])
																																	logging.debug('min_macd_div_2_index = %s'%symbol_data_5M[sym.name]['time'][min_macd_div_2_index])
																																	logging.debug('min_macd_div_1_index = %s'%symbol_data_5M[sym.name]['time'][min_macd_div_1_index])
																																	logging.debug('protect_line = %f'%protect_line)
							
																																	logging.debug('')

																																else:
																																	if (spred <= 0.045) & True:#(flag_index != 0):
																																		logging.debug('buy_5M = FAILED')
																																		logging.debug('------------------------%s' %sym.name)

																																		if ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] <= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])) #pin Bar
																																			| (((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] >= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]))): #pin Bar
																																			logging.debug('Pin Bar')

																																		if ((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3] > symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1]) & (symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2] < symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3])): #inGolf
																																			logging.debug('InGolf')
																																	
																																		if ((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-3] > symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-3]) 
																																			& ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] <= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])) #pin Bar
																																			| (((symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['low'][search_counter_5M_BUY-2]) >= ((symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2])*3)) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1]) & ((((symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2]-symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])/symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2])*100) < 0.01) & (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-2] >= symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-2]))) #pin Bar
																																			& (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['open'][search_counter_5M_BUY-1])
																																			& (symbol_data_5M[sym.name]['close'][search_counter_5M_BUY-1] > symbol_data_5M[sym.name]['high'][search_counter_5M_BUY-2])):
																																			logging.debug('three Candle')

																																		logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]-data_macd_5M_buy['tp'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_buy]))*100))
																																		logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]-data_macd_5M_buy['st'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]))*100))
																																		#logging.debug('tp resist_buy_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_1D)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																		#logging.debug('tp resist_buy_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_4H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																		#logging.debug('tp resist_buy_find_1H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_1H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))
																																		#logging.debug('tp resist_buy_find_30M = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]-resist_buy_find_30M)/symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]))*100))

																																		#logging.debug('st Protect_buy_find = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))
																																		#logging.debug('st Protect_buy_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find_1D)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))
																																		#logging.debug('st Protect_buy_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]-protect_buy_find_4H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_buy]))*100))

																																		#logging.debug('signal_counter_1M_buy = %f'%(signal_counter_1M_buy - MACD_signal_cross_1M_buy['index']))

																																		#logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
																																		logging.debug('signal_counter_5M_buy[] = %s'%symbol_data_5M[sym.name]['time'][signal_counter_5M_buy])

																																		logging.debug('RSI = %f'%ind.rsi(symbol_data_5M[sym.name]['OHLC/4'], length=48)[search_counter_5M_BUY])

																																		logging.debug('Vol_Coef = %f'%(Vol_1/Vol_2))

																																		Profit_Minus_now = (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]-data_macd_5M_buy['st'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_buy]))*100) * 10 #(((abs(symbol_data_1M[sym.name]['close'][signal_counter_1M_buy]-data_macd_1M_buy['st'])/data_macd_1M_buy['st']))*100) * 10
																																		Profit_Minus = Profit_Minus + Profit_Minus_now

								

																																		FAILED += 1

																																		ramp_candle_Fa[FAILED] = ramp_candle
																																		ramp_Fa[FAILED] = ramp


																																		ramp_candle_Fa_sell[FAILED] = ramp_candle_sell
																																		ramp_Fa_sell[FAILED] = ramp_sell

																																		Vol_Coef_Fa[FAILED] = (Vol_1/Vol_2)



																																		alfa_FA[FAILED] = alfa

																																		st_Fa[FAILED] = percentage_buy_st_save_5M

																																		logging.debug('ramp_Fa = %f'%(ramp_Fa[FAILED]))
																																		logging.debug('ramp_candle_Fa = %f'%(ramp_candle_Fa[FAILED]))


																																		logging.debug('ramp_Fa_sell = %f'%(ramp_Fa_sell[FAILED]))
																																		logging.debug('ramp_candle_Fa_sell = %f'%(ramp_candle_Fa_sell[FAILED]))


																																		dif_ramps_Fa[FAILED] = (abs(ramp_candle_Fa[FAILED])-ramp_Fa[FAILED])
																																		Coef_ramps_Fa[FAILED] = (ramp_candle_Fa[FAILED]/ramp_Fa[FAILED])

																																		logging.debug('dif_ramps_Fa = %f'%(dif_ramps_Fa[FAILED]))
																																		logging.debug('Coef_ramps_Fa = %f'%(Coef_ramps_Fa[FAILED]))

																																		logging.debug('dif_SMA_288 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_288_5M[len(sma_288_5M)-1]))

																																		logging.debug('dif_SMA_48 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_48_5M[len(sma_48_5M)-1]))

																																		logging.debug('dif_SMA_168 = %f'%(symbol_data_5M[sym.name]['low'][signal_counter_5M_buy] - sma_168_5M[len(sma_168_5M)-1]))


																																		logging.debug('FiS = %d'%SUCCSESSFULLY)
																																		logging.debug('FiF = %d'%FAILED)

																																		logging.debug('alfa = %f'%(alfa))

																																		#logging.debug('alfa_SUC_tot = %f'%(alfa_SUC))
																																		#logging.debug('alfa_FA_tot = %f'%(alfa_FA))

																																		logging.debug('PP = %f'%Profit_Plus)
																																		logging.debug('PM = %f'%Profit_Minus)
																																		logging.debug('PT = %f'%(Profit_Plus - Profit_Minus))

																																		logging.debug('')
																																		logging.debug('min_candle_2_index = %s'%symbol_data_5M[sym.name]['time'][min_candle_2_index])
																																		logging.debug('min_candle_1_index = %s'%symbol_data_5M[sym.name]['time'][min_candle_1_index])
																																		logging.debug('min_macd_div_2_index = %s'%symbol_data_5M[sym.name]['time'][min_macd_div_2_index])
																																		logging.debug('min_macd_div_1_index = %s'%symbol_data_5M[sym.name]['time'][min_macd_div_1_index])
																																		logging.debug('')

																																#logging.debug('num_15M30M = %d'%counter_sell_15M30M)
																																logging.debug('percentage_buy_tp_save_5M = %f'%percentage_buy_tp_save_5M)
																																logging.debug('percentage_buy_st_save_5M = %f'%percentage_buy_st_save_5M)



																													

									search_counter_5M_BUY += 1
			#except:
			else:
				zzzzzzz = 1
				#print('signal problem 1M BUY MACD!!!')
				#logging.warning('signal problem 1M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




			#****************--------------------++++++++++++++++++++++++***** 1M SELL ***********************************************************++++++++++++++++++++++
			#log_multi_account(1001)
			#try:
			if False:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_1M_SELL = window_counter_1M
								end_search_counter = search_counter_1M_SELL + 12

								if (end_search_counter > (len(symbol_data_1M[sym.name]['low'])-1)):
									end_search_counter = len(symbol_data_1M[sym.name]['low']) - 1

								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_1M_SELL <= end_search_counter):

									window_counter_5M = search_counter_1M_SELL
									window_counter_15M = int(search_counter_1M_SELL/15)
									window_counter_30M = int(search_counter_1M_SELL/30)
									window_counter_1H = int(search_counter_1M_SELL/60)
									window_counter_4H = int(search_counter_1M_SELL/48)

									window_counter_15M,window_counter_30M,window_counter_1H,window_counter_4H = truth_candle_time(search_counter_1M_SELL,window_counter_5M,window_counter_15M,window_counter_30M,window_counter_1H,window_counter_4H,sym.name,symbol_data_1M,symbol_data_5M,symbol_data_15M,symbol_data_30M,symbol_data_1H,symbol_data_4H)
									
									if (symbol_data_4H[sym.name]['time'][window_counter_4H].hour > symbol_data_5M[sym.name]['time'][window_counter_5M].hour): window_counter_4H -= 1
									#print('1M last = ',symbol_data_1M[sym.name]['time'][search_counter_1M_BUY])

									#print('5M last = ',symbol_data_5M[sym.name]['time'][window_counter_5M])

									#print('15M last = ',symbol_data_15M[sym.name]['time'][window_counter_15M])

									#print('30M last = ',symbol_data_30M[sym.name]['time'][window_counter_30M])

									#print('1H last = ',symbol_data_1H[sym.name]['time'][window_counter_1H])

									#print('4H last = ',symbol_data_4H[sym.name]['time'][window_counter_4H])

									

									if True:#(((symbol_data_1M[sym.name]['low'][(search_counter_1M_BUY)] > symbol_data_1M[sym.name]['low'][(search_counter_1M_BUY-1)]))):
										#print('1M Position = ',search_counter_1M_BUY)
										#print('Signal 5M = ',MACD_signal_cross_5M_sell['signal'])
										if (((symbol_data_5M[sym.name]['high'][window_counter_5M - 2] > symbol_data_5M[sym.name]['high'][(window_counter_5M-3)])
											& (symbol_data_5M[sym.name]['high'][(window_counter_5M-1)] >= symbol_data_5M[sym.name]['high'][(window_counter_5M-2)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M] < symbol_data_5M[sym.name]['high'][(window_counter_5M-1)]))

											| ((symbol_data_5M[sym.name]['high'][(window_counter_5M-3)] > symbol_data_5M[sym.name]['high'][(window_counter_5M-4)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M-2] > symbol_data_5M[sym.name]['high'][(window_counter_5M-3)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M-1] <= symbol_data_5M[sym.name]['high'][(window_counter_5M-2)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M] <= symbol_data_5M[sym.name]['high'][(window_counter_5M-1)]))

											| ((symbol_data_5M[sym.name]['high'][(window_counter_5M-4)] >= symbol_data_5M[sym.name]['high'][(window_counter_5M-5)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M-3] > symbol_data_5M[sym.name]['high'][(window_counter_5M-4)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M-2] <= symbol_data_5M[sym.name]['high'][(window_counter_5M-3)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M-1] <= symbol_data_5M[sym.name]['high'][(window_counter_5M-2)])
											& (symbol_data_5M[sym.name]['high'][window_counter_5M] <= symbol_data_5M[sym.name]['high'][(window_counter_5M-1)]))):

											#print('5M Pass')
											
											if True:#(((symbol_data_15M[sym.name]['low'][window_counter_15M - 2] < symbol_data_15M[sym.name]['low'][(window_counter_15M-3)]))
												#& ((symbol_data_15M[sym.name]['low'][(window_counter_15M-1)] <= symbol_data_15M[sym.name]['low'][(window_counter_15M-2)]))
												#& ((symbol_data_15M[sym.name]['low'][window_counter_15M] > symbol_data_15M[sym.name]['low'][(window_counter_15M-1)]))):

												#print('15M Pass')
												if True:#(((symbol_data_30M[sym.name]['low'][(window_counter_30M)] < symbol_data_30M[sym.name]['low'][(window_counter_30M-1)]))):

													if True:#(((symbol_data_1H[sym.name]['low'][(window_counter_1H)] < symbol_data_1H[sym.name]['low'][(window_counter_1H-1)]))):

														if ((symbol_data_4H[sym.name]['high'][(window_counter_4H)] >= symbol_data_4H[sym.name]['high'][(window_counter_4H-1)])):
															#& (symbol_data_4H[sym.name]['open'][(window_counter_4H)] <= symbol_data_4H[sym.name]['close'][(window_counter_4H-1)])):

															#print('4H Pass')
															#print('Pre')

															macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)[0:window_counter_5M+1]

															macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
																#print(macd_5M_sell)
															macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
															macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]


															macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)[0:window_counter_5M+1]

															macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
																#print(macd_5M_sell)
															macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
															macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]



															ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
																		tenkan=9,kijun=26,snkou=52)[0:window_counter_5M+1]
															SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]][0:window_counter_5M+1]
															SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]][0:window_counter_5M+1]
															tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter_5M+1]
															kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter_5M+1]
															chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]][0:window_counter_5M+1]

															if True:#((MACD_signal_cross_5M_sell_now['signal'] == 'sell') | (MACD_signal_cross_5M_sell_now['signal'] == 'faild_sell')):

																#print('1M last = ',symbol_data_1M[sym.name]['time'][search_counter_1M_BUY])

																#print('5M last = ',symbol_data_5M[sym.name]['time'][window_counter_5M])
				
																#print('5M cross = ',symbol_data_5M[sym.name]['time'][MACD_signal_cross_5M_sell_now['index']])

																#print('window_counter_5M = ',window_counter_5M)
																#print('MACD_signal_cross_5M_sell_now = ',MACD_signal_cross_5M_sell_now['index'])

																hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																#print(diff_5M_U_4H)
																#print(window_counter_5M)
																#print('diff time = ',symbol_data_5M[sym.name]['time'][diff_5M_U_4H])

																if (window_counter_5M - int(diff_5M_U_4H)) < window_counter_5M:
																	protect_sell_find_1M = max(symbol_data_5M[sym.name]['high'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	counter_max_find = window_counter_5M
																	flag_max_find = 0

																	#print('counter_max_find = ',counter_max_find)
																	#print('last = ',(window_counter_5M - int(diff_5M_U_4H)))

																	while (counter_max_find >= (window_counter_5M - int(diff_5M_U_4H))):
																		if (macd_5M_sell[counter_max_find - 1] >= macd_5M_sell[counter_max_find]):
																			max_macd_find = macd_5M_sell[counter_max_find - 1]
																			flag_max_find += 1
																			#print('flag_max_find = ',flag_max_find)
																		if ((macd_5M_sell[counter_max_find - 2] < macd_5M_sell[counter_max_find - 1]) & (flag_max_find >= 2)
																			& (macd_5M_sell[counter_max_find - 3] < macd_5M_sell[counter_max_find - 1])):
																			max_macd_div_2 = max_macd_find
																			break
																		else:
																			max_macd_div_2 = 10000
																		counter_max_find -= 1

																	#max_macd_div_2 = max(macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])

																	#min_candle_2 = min(symbol_data_5M[sym.name]['low'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	#print('min_macd_div_2 = ',min_macd_div_2)
																	index_counter = (window_counter_5M - int(diff_5M_U_4H))
																	for i in macd_5M_sell[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M]:
																		if (i == max_macd_div_2):
																			max_macd_div_2_index = index_counter
																			break
																		else:
																			max_macd_div_2_index = 1
																		index_counter += 1

																	max_candle_2 = symbol_data_5M[sym.name]['high'][window_counter_5M]
																	max_candle_2_index = window_counter_5M

																	max_candle_2_line = symbol_data_5M[sym.name]['high'][max_macd_div_2_index]
																	max_candle_2_index_line = max_macd_div_2_index

																else:
																	protect_sell_find_1M = symbol_data_5M[sym.name]['high'][window_counter_5M]
																	max_macd_div_2 = macd_5M_sell[window_counter_5M]
																	max_macd_div_2_index = window_counter_5M

																	max_candle_2 = symbol_data_5M[sym.name]['high'][window_counter_5M]
																	max_candle_2_index = window_counter_5M

																	max_candle_2_line = symbol_data_5M[sym.name]['high'][max_macd_div_2_index]
																	max_candle_2_index_line = max_macd_div_2_index


																low_counter_4H = 1
																counter_for_low = 1
																while (counter_for_low < 3):
																	if (symbol_data_4H[sym.name]['high'][window_counter_4H] > symbol_data_4H[sym.name]['high'][window_counter_4H-counter_for_low]):
																		low_counter_4H += 1
																	counter_for_low += 1

																hour_5M = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H-low_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H = (abs(hour_5M - hour_4H) * 12) #+ (min_5M/5)


																hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H_end = (abs(hour_5M - hour_4H) * 12) + int(min_5M/5) + 1

																#print(diff_5M_U_4H)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																if (window_counter_5M - int(diff_5M_U_4H)) < (max_macd_div_2_index - 1):
																	max_macd_div_1 = max(macd_5M_sell[(window_counter_5M - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)])
																	

																	#print('min_candle_1 = ',min_candle_1)

																	index_counter = (window_counter_5M - int(diff_5M_U_4H))
																	for i in macd_5M_sell[(window_counter_5M - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)]:
																		if (i == max_macd_div_1):
																			max_macd_div_1_index = index_counter
																		index_counter += 1

																	max_candle_1 = symbol_data_5M[sym.name]['high'][max_macd_div_1_index]
																	max_candle_1_index = max_macd_div_1_index

																else:
																	search_counter_1M_SELL += 1
																	continue
																	max_macd_div_1 = macd_5M_sell[(max_macd_div_2_index - 1)]
																	max_macd_div_1_index = (max_macd_div_2_index - 1)

																	max_candle_1 = symbol_data_5M[sym.name]['high'][max_macd_div_1_index]
																	max_candle_1_index = max_macd_div_1_index

																#print('max_macd_div_1 = ',max_macd_div_1)
																#print('max_macd_div_2 = ',max_macd_div_2)

																#print('max_macd_div_1_index = ',max_macd_div_1_index)
																#print('max_macd_div_2_index = ',max_macd_div_2_index)

																if ((max_macd_div_2_index-max_macd_div_1_index) >= 1):
																	ramp = ((max_macd_div_2 - max_macd_div_1)/(max_macd_div_2_index-max_macd_div_1_index))
																else:
																	ramp = 0

																if ((max_candle_2_index-max_candle_1_index) >= 1):
																	ramp_candle = ((max_candle_2 - max_candle_1)/(max_candle_2_index-max_candle_1_index))
																else:
																	ramp_candle = 0

																if ((max_candle_2_index_line-max_candle_1_index) >= 1):
																	ramp_candle_line = ((max_candle_2_line - max_candle_1)/(max_candle_2_index_line-max_candle_1_index))

																	protect_line = ramp_candle_line * ((window_counter_5M) - max_candle_1_index) + max_candle_1
																else:
																	protect_line = 0



																resist_sell_find_1M = (symbol_data_4H[sym.name]['HLC/3'][window_counter_4H-1])#symbol_data_4H[sym.name]['close'][window_counter_4H-1] + (abs(symbol_data_4H[sym.name]['open'][window_counter_4H-1] - symbol_data_4H[sym.name]['close'][window_counter_4H-1]) * 0.6) #- symbol_data_5M[sym.name]['high'][window_counter_5M])/2) + symbol_data_5M[sym.name]['high'][window_counter_5M]

																#print('1 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

																dangrouse_line = protect_sell_find_1M - (((protect_sell_find_1M)*alfa_fixed_sell)/100)

																#print('dangrouse_line = ',dangrouse_line)
																#print(symbol_data_5M[sym.name]['low'][window_counter_5M])

																alfa = ((protect_sell_find_1M - symbol_data_5M[sym.name]['low'][window_counter_5M])/(protect_sell_find_1M)) * 100

																if (ramp != 0):
																	Coef_ramps = (ramp_candle/ramp)
																else:
																	Coef_ramps = 0

																diff_ramps = (abs(ramp_candle)-ramp)


																if ((((abs(resist_sell_find_1M - symbol_data_5M[sym.name]['low'][window_counter_5M])/symbol_data_5M[sym.name]['low'][window_counter_5M])*100) >= 0)
																	& ((ramp >= Max_ramp_MACD_fixed_sell) | (ramp_candle <= Max_ramp_MACD_fixed_sell)
																	| (Coef_ramps <= Max_coef_ramps_fixed_sell) | (diff_ramps >= Max_diff_ramps_fixed_sell))):

																	if (tp_Coef_fixed_sell != 1):
																		resist_sell_find_1M = symbol_data_5M[sym.name]['low'][window_counter_5M] - ((((abs(resist_sell_find_1M - symbol_data_5M[sym.name]['low'][window_counter_5M])/resist_sell_find_1M))/tp_Coef_fixed_sell) * symbol_data_5M[sym.name]['low'][window_counter_5M])
																		#print('2 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

																

																#************************** BUY MACD Section ************************************

																hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																#print(diff_5M_U_4H)
																#print(window_counter_5M)
																#print('diff time = ',symbol_data_5M[sym.name]['time'][diff_5M_U_4H])

																if (window_counter_5M - int(diff_5M_U_4H)) < window_counter_5M:
																	protect_buy_find_1M = min(symbol_data_5M[sym.name]['low'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	counter_min_find = window_counter_5M
																	flag_min_find = 0

																	#print('counter_max_find = ',counter_max_find)
																	#print('last = ',(window_counter_5M - int(diff_5M_U_4H)))

																	while (counter_min_find >= (window_counter_5M - int(diff_5M_U_4H))):
																		if (macd_5M_buy[counter_min_find - 1] <= macd_5M_buy[counter_min_find]):
																			min_macd_find = macd_5M_buy[counter_min_find - 1]
																			flag_min_find += 1
																			#print('flag_max_find = ',flag_max_find)
																		if ((macd_5M_buy[counter_min_find - 2] > macd_5M_buy[counter_min_find - 1]) & (flag_min_find >= 2)
																			& (macd_5M_buy[counter_min_find - 3] > macd_5M_buy[counter_min_find - 1])):
																			min_macd_div_2 = min_macd_find
																			break
																		else:
																			min_macd_div_2 = 10000
																		counter_min_find -= 1

																	#max_macd_div_2 = max(macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])

																	#min_candle_2 = min(symbol_data_5M[sym.name]['low'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
																	#print('min_macd_div_2 = ',min_macd_div_2)
																	index_counter = (window_counter_5M - int(diff_5M_U_4H))
																	for i in macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M]:
																		if (i == min_macd_div_2):
																			min_macd_div_2_index = index_counter
																			break
																		else:
																			min_macd_div_2_index = 1
																		index_counter += 1

																	min_candle_2 = symbol_data_5M[sym.name]['low'][window_counter_5M]
																	min_candle_2_index = window_counter_5M

																	min_candle_2_line = symbol_data_5M[sym.name]['low'][min_macd_div_2_index]
																	min_candle_2_index_line = min_macd_div_2_index

																else:
																	protect_buy_find_1M = symbol_data_5M[sym.name]['low'][window_counter_5M]
																	min_macd_div_2 = macd_5M_buy[window_counter_5M]
																	min_macd_div_2_index = window_counter_5M

																	min_candle_2 = symbol_data_5M[sym.name]['low'][window_counter_5M]
																	min_candle_2_index = window_counter_5M

																	min_candle_2_line = symbol_data_5M[sym.name]['low'][min_macd_div_2_index]
																	min_candle_2_index_line = min_macd_div_2_index




																low_counter_4H = 1
																counter_for_low = 1
																while (counter_for_low < 3):
																	if (symbol_data_4H[sym.name]['low'][window_counter_4H] <= symbol_data_4H[sym.name]['low'][window_counter_4H-counter_for_low]):
																		low_counter_4H += 1
																	counter_for_low += 1

																hour_5M = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H-low_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H = (abs(hour_5M - hour_4H) * 12) #+ (min_5M/5)


																hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

																hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

																min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

																diff_5M_U_4H_end = (abs(hour_5M - hour_4H) * 12) + int(min_5M/5) + 1

																#print(diff_5M_U_4H)

																if (int(diff_5M_U_4H) < 0):
																	diff_5M_U_4H = 0

																if (window_counter_5M - int(diff_5M_U_4H)) < (min_macd_div_2_index - 1):
																	min_macd_div_1 = min(macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):(min_macd_div_2_index - 1)])
																	

																	#print('min_candle_1 = ',min_candle_1)

																	index_counter = (window_counter_5M - int(diff_5M_U_4H))
																	for i in macd_5M_buy[(window_counter_5M - int(diff_5M_U_4H)):(min_macd_div_2_index - 1)]:
																		if (i == min_macd_div_1):
																			min_macd_div_1_index = index_counter
																		index_counter += 1

																	min_candle_1 = symbol_data_5M[sym.name]['low'][min_macd_div_1_index]
																	min_candle_1_index = min_macd_div_1_index

																else:
																	search_counter_1M_SELL += 1
																	continue
																	min_macd_div_1 = macd_5M_buy[(min_macd_div_2_index - 1)]
																	min_macd_div_1_index = (min_macd_div_2_index - 1)

																	min_candle_1 = symbol_data_5M[sym.name]['low'][min_macd_div_1_index]
																	min_candle_1_index = min_macd_div_1_index

																#print('max_macd_div_1 = ',max_macd_div_1)
																#print('max_macd_div_2 = ',max_macd_div_2)

																#print('max_macd_div_1_index = ',max_macd_div_1_index)
																#print('max_macd_div_2_index = ',max_macd_div_2_index)

																if ((min_macd_div_2_index-min_macd_div_1_index) >= 1):
																	ramp_buy = ((min_macd_div_2 - min_macd_div_1)/(min_macd_div_2_index-min_macd_div_1_index))

																if ((min_candle_2_index-min_candle_1_index) >= 1):
																	ramp_candle_buy = ((min_candle_2 - min_candle_1)/(min_candle_2_index-min_candle_1_index))

																#*************************************************************************************************


																

																	#print('ramp = ',ramp)

																protect_sell_find_1M = protect_sell_find_1M * st_Coef_fixed_sell



																#print('min_macd_div_2 = ',min_macd_div_2)
																#print('min_macd_div_1 = ',min_macd_div_1)

																#print('dangrouse_line = ',dangrouse_line)
																#print('symbol_data_5M[sym.name][low] = ',symbol_data_5M[sym.name]['low'][window_counter_5M])
																#print('0')

																if (resist_sell_find_1M > protect_sell_find_1M): 
																	search_counter_1M_SELL += 1
																	continue

																#print('ramp_candle = ',ramp_candle)
																#print('ramp_candle_fixed_sell = ',ramp_candle_fixed_sell)
																#print('1')
																if (ramp_candle >= ramp_candle_fixed_sell):
																	#print('1.5')
																	if (symbol_data_5M[sym.name]['low'][window_counter_5M] >= dangrouse_line):

																		#print('2')
																		if (ramp <= ramp_MACD_fixed_sell):
																			#print('4')
																			if (Coef_ramps <= coef_ramps_fixed_sell):
																				#print('5')

																				if (ramp_buy <= ramp_buy_fixed):
																					if (diff_ramps >= diff_ramps_fixed_sell):
																						#print('7')
																						if (alfa <= alfa_fixed_sell):
																							#print('8')
																							if ((symbol_data_5M[sym.name]['low'][window_counter_5M] <= protect_line)):

																								if True:#((tenkan_5M[window_counter_5M-8] < kijun_5M[window_counter_5M-8])
																									#& (tenkan_5M[window_counter_5M-7] <= kijun_5M[window_counter_5M-7])
																									#& (tenkan_5M[window_counter_5M-6] <= kijun_5M[window_counter_5M-6])
																									#& (tenkan_5M[window_counter_5M-5] <= kijun_5M[window_counter_5M-5])
																									#& (tenkan_5M[window_counter_5M-4] <= kijun_5M[window_counter_5M-4])
																									#& (tenkan_5M[window_counter_5M-3] <= kijun_5M[window_counter_5M-3])
																									#& (tenkan_5M[window_counter_5M-2] <= kijun_5M[window_counter_5M-2])
																									#& (tenkan_5M[window_counter_5M-1] <= kijun_5M[window_counter_5M-1])
																									#& (tenkan_5M[window_counter_5M] <= kijun_5M[window_counter_5M])):
																									#print('9')

																									if True:#((symbol_data_1M[sym.name]['low'][search_counter_1M_BUY] <= tenkan_1M[search_counter_1M_BUY]) & (symbol_data_1M[sym.name]['high'][search_counter_1M_BUY] <= kijun_1M[search_counter_1M_BUY])):
				
																										if True:#((symbol_data_5M[sym.name]['low'][window_counter_5M] <= tenkan_5M[window_counter_5M]) & (symbol_data_5M[sym.name]['high'][window_counter_5M] <= kijun_5M[window_counter_5M])):
																											#print('10')

																											if True:#((symbol_data_1M[sym.name]['high'][search_counter_1M_BUY] <= SPANA_1M[search_counter_1M_BUY]) & (symbol_data_1M[sym.name]['high'][search_counter_1M_BUY] <= SPANB_1M[search_counter_1M_BUY])):

																												if ((symbol_data_5M[sym.name]['low'][window_counter_5M] > SPANA_5M[window_counter_5M]) & (symbol_data_5M[sym.name]['low'][window_counter_5M] > SPANB_5M[window_counter_5M])):

																													flag_cross_1M = 'sell'

																													
																													print('flag_cross_1M = ',flag_cross_1M)
																						

																													signal_counter_1M_sell = search_counter_1M_SELL

																													if (flag_cross_1M == 'sell'):

																														print('////////////// flag_cross_1M = ',flag_cross_1M)


																														if (flag_cross_1M == 'sell'):

																															if (sym.name == 'XAUUSD_i'):
																																#data_macd_1M_buy['tp'] = min(resist_buy_find_1M,(symbol_data_1M[sym.name]['high'][signal_counter_1M_buy]*1.001))
																																data_macd_1M_sell['tp'] = resist_sell_find_1M * 1.0007
																															else:
																																data_macd_1M_sell['tp'] = resist_sell_find_1M * 1.0007



																															data_macd_1M_sell['st'] = protect_sell_find_1M * 1.0002

					

																															if data_macd_1M_sell['tp'] < symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]: 
																																#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
																																#continue

																																counter_i = signal_counter_1M_sell
																																final_index = (signal_counter_1M_sell + 4320)

																																flag_index = 1

																																if (final_index ) >= len(symbol_data_5M[sym.name]['close'])-1:
																																	final_index = len(symbol_data_5M[sym.name]['close'])-1
																																	flag_index = 0



																																counter_j = 0

																																percentage_sell_tp = {}
																																percentage_sell_st = {}


																																while (counter_i <= final_index):
																																	percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_counter_1M_sell])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]) * 100
																																	percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_counter_1M_sell] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]) * 100

																																#print(percentage_buy_tp[counter_j])
																																##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

																																	if(percentage_sell_tp[counter_j]<0):
																																		if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100)):
																																			#print('fine')
																																			break

																																	counter_i += 1
																																	counter_j += 1

						

																																#if (counter_j > 50): break

																																try:
																																	percentage_sell_tp_save_1M = min(percentage_sell_tp.values())
																																	percentage_sell_st_save_1M = min(percentage_sell_st.values())
																																except:
																																	percentage_sell_tp_save_1M = 0
																																	percentage_sell_st_save_1M = 0

																																logging.debug('************************ OUT 1M sell *******************************')

																																if (abs(percentage_sell_tp_save_1M) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100)):
																																	logging.debug('sell_1M = SUCCSESSFULLY')
																																	logging.debug('------------------------%s' %sym.name)
																																	logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100))
																																	logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_1M_sell]-data_macd_1M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_1M_sell]))*100))

																																	logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
																																	logging.debug('signal_counter_1M_buy[] = %s'%symbol_data_5M[sym.name]['time'][signal_counter_1M_sell])
																																	SUCCSESSFULLY += 1
							

																																	Profit_Plus_now = (((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100) * 10
																																	Profit_Plus = Profit_Plus + Profit_Plus_now

																																	ramp_Suc[SUCCSESSFULLY] = ramp
																																	ramp_candle_Suc[SUCCSESSFULLY] = ramp_candle

																																	alfa_SUC[SUCCSESSFULLY] = alfa

																																	ramp_Suc_sell[SUCCSESSFULLY] = ramp_buy
																																	ramp_candle_Suc_sell[SUCCSESSFULLY] = ramp_candle_buy

																																	st_Suc[SUCCSESSFULLY] = abs(percentage_sell_st_save_1M)

																																	logging.debug('FiS = %d'%SUCCSESSFULLY)
																																	logging.debug('FiF = %d'%FAILED)

																																	logging.debug('alfa = %f'%(alfa))

																																	#logging.debug('alfa_SUC_tot = %f'%(alfa_SUC[SUCCSESSFULLY]))
																																	logging.debug('ramp_Suc = %f'%(ramp_Suc[SUCCSESSFULLY]))
																																	logging.debug('ramp_candle_Suc = %f'%(ramp_candle_Suc[SUCCSESSFULLY]))

																																	logging.debug('ramp_Suc_buy = %f'%(ramp_Suc_sell[SUCCSESSFULLY]))
																																	logging.debug('ramp_candle_Suc_buy = %f'%(ramp_candle_Suc_sell[SUCCSESSFULLY]))

																																	dif_ramps_Suc[SUCCSESSFULLY] = (abs(ramp_candle_Suc[SUCCSESSFULLY])-ramp_Suc[SUCCSESSFULLY])

																																	if (ramp_Suc[SUCCSESSFULLY] != 0):
																																		Coef_ramps_Suc[SUCCSESSFULLY] = (ramp_candle_Suc[SUCCSESSFULLY]/ramp_Suc[SUCCSESSFULLY])
																																	else:
																																		Coef_ramps_Suc[SUCCSESSFULLY] = 0

																																	logging.debug('dif_ramps_Suc = %f'%(dif_ramps_Suc[SUCCSESSFULLY]))
																																	logging.debug('Coef_ramps_Suc = %f'%(Coef_ramps_Suc[SUCCSESSFULLY]))

																																	logging.debug('PP = %f'%Profit_Plus)
																																	logging.debug('PM = %f'%Profit_Minus)
																																	logging.debug('PT = %f'%(Profit_Plus - Profit_Minus))

																																	logging.debug('')
																																	logging.debug('min_candle_2_index = %s'%symbol_data_5M[sym.name]['time'][max_candle_2_index])
																																	logging.debug('min_candle_1_index = %s'%symbol_data_5M[sym.name]['time'][max_candle_1_index])
																																	logging.debug('min_macd_div_2_index = %s'%symbol_data_5M[sym.name]['time'][max_macd_div_2_index])
																																	logging.debug('min_macd_div_1_index = %s'%symbol_data_5M[sym.name]['time'][max_macd_div_1_index])

																																	logging.debug('min_macd_div_2_index = %d'%max_macd_div_2_index)
																																	logging.debug('min_macd_div_1_index = %d'%max_macd_div_1_index)
																																	logging.debug('')


																																else:
																																	if (spred <= 0.045) & (flag_index != 0):
																																		logging.debug('sell_1M = FAILED')
																																		logging.debug('------------------------%s' %sym.name)
																																		logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100))
																																		logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_1M_sell]-data_macd_1M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_1M_sell]))*100))

																																		logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
																																		logging.debug('signal_counter_1M_buy[] = %s'%symbol_data_5M[sym.name]['time'][signal_counter_1M_sell])

																																		Profit_Minus_now = (((abs(symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_1M_sell]))*100) * 10
																																		Profit_Minus = Profit_Minus + Profit_Minus_now

																																		FAILED += 1

																																		ramp_candle_Fa[FAILED] = ramp_candle
																																		ramp_Fa[FAILED] = ramp

																																		ramp_Fa_sell[FAILED] = ramp_buy
																																		ramp_candle_Fa_sell[FAILED] = ramp_candle_buy

																																		alfa_FA[FAILED] = alfa

																																		st_Fa[FAILED] = abs(percentage_sell_st_save_1M)

																																		logging.debug('ramp_Fa = %f'%(ramp_Fa[FAILED]))
																																		logging.debug('ramp_candle_Fa = %f'%(ramp_candle_Fa[FAILED]))

																																		logging.debug('ramp_Fa_buy = %f'%(ramp_Fa_sell[FAILED]))
																																		logging.debug('ramp_candle_Fa_buy = %f'%(ramp_candle_Fa_sell[FAILED]))

																																		dif_ramps_Fa[FAILED] = (abs(ramp_candle_Fa[FAILED])-ramp_Fa[FAILED])

																																		if (ramp_Fa[FAILED] != 0):
																																			Coef_ramps_Fa[FAILED] = (ramp_candle_Fa[FAILED]/ramp_Fa[FAILED])
																																		else:
																																			Coef_ramps_Fa[FAILED] = 0

																																		logging.debug('dif_ramps_Fa = %f'%(dif_ramps_Fa[FAILED]))
																																		logging.debug('Coef_ramps_Fa = %f'%(Coef_ramps_Fa[FAILED]))


																																		logging.debug('FiS = %d'%SUCCSESSFULLY)
																																		logging.debug('FiF = %d'%FAILED)

																																		logging.debug('alfa = %f'%(alfa))

																																		#logging.debug('alfa_SUC_tot = %f'%(alfa_SUC))
																																		#logging.debug('alfa_FA_tot = %f'%(alfa_FA))

																																		logging.debug('PP = %f'%Profit_Plus)
																																		logging.debug('PM = %f'%Profit_Minus)
																																		logging.debug('PT = %f'%(Profit_Plus - Profit_Minus))

																																		logging.debug('')
																																		logging.debug('max_candle_2_index = %s'%symbol_data_5M[sym.name]['time'][max_candle_2_index])
																																		logging.debug('max_candle_1_index = %s'%symbol_data_5M[sym.name]['time'][max_candle_1_index])
																																		logging.debug('max_macd_div_2_index = %s'%symbol_data_5M[sym.name]['time'][max_macd_div_2_index])
																																		logging.debug('max_macd_div_1_index = %s'%symbol_data_5M[sym.name]['time'][max_macd_div_1_index])

																															#logging.debug('num_1M = %d'%counter_sell_1M)
																																logging.debug('percentage_sell_tp_save_1M = %f'%percentage_sell_tp_save_1M)
																																logging.debug('percentage_sell_st_save_1M = %f'%percentage_sell_st_save_1M)


																			#if (((MACD_signal_cross_1M_sell['signal'] == 'sell') | (MACD_signal_cross_1M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_1M_sell['index'] >= ((search_counter_1M_BUY) - 5))):
																			#	flag_cross_1M = 'failed_buy'

																			#	if (((MACD_signal_cross_5M_sell['signal'] == 'sell') | (MACD_signal_cross_5M_sell['signal'] == 'faild_sell')) & (MACD_signal_cross_5M_sell['index'] >= (int(search_counter_1M_BUY/5) - 3))):
																			#		flag_cross_1M = 'failed_buy'

																			#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_1M_SELL/1440)+458 - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_1M_SELL/1440)+458 - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			#if (macds_1D_sell[int(search_counter_1M_BUY/1440)+458] >= macd_1D_sell[int(search_counter_1M_BUY/1440)+458]):
																			#	flag_cross_1M = 'failed_buy'

																			#if (macds_4H_sell[int(search_counter_1M_BUY/240)] > macd_4H_sell[int(search_counter_1M_BUY/240)]):
																			#	flag_cross_1M = 'failed_buy'

																			#print('******************** flag_cross_1M = ',flag_cross_1M)

																													

									search_counter_1M_SELL += 1
			#except:
			else:
				zzzzzzz = 1
				#print('signal problem 1M SELL MACD!!!')
				#logging.warning('signal problem 1M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






			window_counter_5M -= 10
			if (window_counter_5M < 100):
				break
			print(sym.name,' = ',symbol_data_5M[sym.name]['time'][window_counter_5M])

				#print('window_counter_1M = ',window_counter_1M)


		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('')
		logging.debug('')

	logging.debug('Finished Symbol')
	logging.debug('FiS = %d'%SUCCSESSFULLY)
	logging.debug('FiF = %d'%FAILED)

	logging.debug('PP = %f'%Profit_Plus)
	logging.debug('PM = %f'%Profit_Minus)
	logging.debug('PT = %f'%(Profit_Plus - Profit_Minus))

	if (len(alfa_SUC)-1 > 1):
		logging.debug('Min alfa_SUC = %f'%min(alfa_SUC.values()))
		logging.debug('Max alfa_SUC = %f'%max(alfa_SUC.values()))
		logging.debug('Mean alfa_SUC = %f'%statistics.mean(alfa_SUC.values()))
	else:
		logging.debug('Min alfa_SUC = %f'%alfa_SUC[SUCCSESSFULLY])
		logging.debug('Max alfa_SUC = %f'%alfa_SUC[SUCCSESSFULLY])
		logging.debug('Mean alfa_SUC = %f'%alfa_SUC[SUCCSESSFULLY])


	if (len(alfa_FA)-1 > 1):
		logging.debug('Min alfa_FA = %f'%min(alfa_FA.values()))
		logging.debug('Max alfa_FA = %f'%max(alfa_FA.values()))
		logging.debug('Mean alfa_FA = %f'%statistics.mean(alfa_FA.values()))
	else:
		logging.debug('Min alfa_FA = %f'%alfa_FA[FAILED])
		logging.debug('Max alfa_FA = %f'%alfa_FA[FAILED])
		logging.debug('Mean alfa_FA = %f'%alfa_FA[FAILED])


	if (len(ramp_Suc)-1 > 1):
		logging.debug('Min ramp_Suc = %f'%min(ramp_Suc.values()))
		logging.debug('Max ramp_Suc = %f'%max(ramp_Suc.values()))
		logging.debug('Mean ramp_Suc = %f'%statistics.mean(ramp_Suc.values()))
	else:
		logging.debug('Min ramp_Suc = %f'%ramp_Suc[SUCCSESSFULLY])
		logging.debug('Max ramp_Suc = %f'%ramp_Suc[SUCCSESSFULLY])
		logging.debug('Mean ramp_Suc = %f'%ramp_Suc[SUCCSESSFULLY])

	if (len(ramp_Fa)-1 > 1):
		logging.debug('Min ramp_Fa = %f'%min(ramp_Fa.values()))
		logging.debug('Max ramp_Fa = %f'%max(ramp_Fa.values()))
		logging.debug('Mean ramp_Fa = %f'%statistics.mean(ramp_Fa.values()))
	else:
		logging.debug('Min ramp_Fa = %f'%ramp_Fa[FAILED])
		logging.debug('Max ramp_Fa = %f'%ramp_Fa[FAILED])
		logging.debug('Mean ramp_Fa = %f'%ramp_Fa[FAILED])


	if (len(ramp_Suc_sell)-1 > 1):
		logging.debug('Min ramp_Suc_sell = %f'%min(ramp_Suc_sell.values()))
		logging.debug('Max ramp_Suc_sell = %f'%max(ramp_Suc_sell.values()))
		logging.debug('Mean ramp_Suc_sell = %f'%statistics.mean(ramp_Suc_sell.values()))
	else:
		logging.debug('Min ramp_Suc_sell = %f'%ramp_Suc_sell[SUCCSESSFULLY])
		logging.debug('Max ramp_Suc_sell = %f'%ramp_Suc_sell[SUCCSESSFULLY])
		logging.debug('Mean ramp_Suc_sell = %f'%ramp_Suc_sell[SUCCSESSFULLY])

	if (len(ramp_Fa_sell)-1 > 1):
		logging.debug('Min ramp_Fa_sell = %f'%min(ramp_Fa_sell.values()))
		logging.debug('Max ramp_Fa_sell = %f'%max(ramp_Fa_sell.values()))
		logging.debug('Mean ramp_Fa_sell = %f'%statistics.mean(ramp_Fa_sell.values()))
	else:
		logging.debug('Min ramp_Fa_sell = %f'%ramp_Fa_sell[FAILED])
		logging.debug('Max ramp_Fa_sell = %f'%ramp_Fa_sell[FAILED])
		logging.debug('Mean ramp_Fa_sell = %f'%ramp_Fa_sell[FAILED])



	if (len(ramp_candle_Suc)-1 > 1):
		logging.debug('Min ramp_candle_Suc = %f'%min(ramp_candle_Suc.values()))
		logging.debug('Max ramp_candle_Suc = %f'%max(ramp_candle_Suc.values()))
		logging.debug('Mean ramp_candle_Suc = %f'%statistics.mean(ramp_candle_Suc.values()))
	else:
		logging.debug('Min ramp_candle_Suc = %f'%ramp_candle_Suc[SUCCSESSFULLY])
		logging.debug('Max ramp_candle_Suc = %f'%ramp_candle_Suc[SUCCSESSFULLY])
		logging.debug('Mean ramp_candle_Suc = %f'%ramp_candle_Suc[SUCCSESSFULLY])

	if (len(ramp_candle_Fa)-1 > 1):
		logging.debug('Min ramp_candle_Fa = %f'%min(ramp_candle_Fa.values()))
		logging.debug('Max ramp_candle_Fa = %f'%max(ramp_candle_Fa.values()))
		logging.debug('Mean ramp_candle_Fa = %f'%statistics.mean(ramp_candle_Fa.values()))
	else:
		logging.debug('Min ramp_candle_Fa = %f'%ramp_candle_Fa[FAILED])
		logging.debug('Max ramp_candle_Fa = %f'%ramp_candle_Fa[FAILED])
		logging.debug('Mean ramp_candle_Fa = %f'%ramp_candle_Fa[FAILED])



	if (len(ramp_candle_Suc_sell)-1 > 1):
		logging.debug('Min ramp_candle_Suc_sell = %f'%min(ramp_candle_Suc_sell.values()))
		logging.debug('Max ramp_candle_Suc_sell = %f'%max(ramp_candle_Suc_sell.values()))
		logging.debug('Mean ramp_candle_Suc_sell = %f'%statistics.mean(ramp_candle_Suc_sell.values()))
	else:
		logging.debug('Min ramp_candle_Suc_sell = %f'%ramp_candle_Suc_sell[SUCCSESSFULLY])
		logging.debug('Max ramp_candle_Suc_sell = %f'%ramp_candle_Suc_sell[SUCCSESSFULLY])
		logging.debug('Mean ramp_candle_Suc_sell = %f'%ramp_candle_Suc_sell[SUCCSESSFULLY])

	if (len(ramp_candle_Fa)-1 > 1):
		logging.debug('Min ramp_candle_Fa_sell = %f'%min(ramp_candle_Fa_sell.values()))
		logging.debug('Max ramp_candle_Fa_sell = %f'%max(ramp_candle_Fa_sell.values()))
		logging.debug('Mean ramp_candle_Fa_sell = %f'%statistics.mean(ramp_candle_Fa_sell.values()))
	else:
		logging.debug('Min ramp_candle_Fa_sell = %f'%ramp_candle_Fa_sell[FAILED])
		logging.debug('Max ramp_candle_Fa_sell = %f'%ramp_candle_Fa_sell[FAILED])
		logging.debug('Mean ramp_candle_Fa_sell = %f'%ramp_candle_Fa_sell[FAILED])



	if (len(dif_ramps_Suc)-1 > 1):
		logging.debug('Min dif_ramps_Suc = %f'%min(dif_ramps_Suc.values()))
		logging.debug('Max dif_ramps_Suc = %f'%max(dif_ramps_Suc.values()))
		logging.debug('Mean dif_ramps_Suc = %f'%statistics.mean(dif_ramps_Suc.values()))
	else:
		logging.debug('Min dif_ramps_Suc = %f'%dif_ramps_Suc[SUCCSESSFULLY])
		logging.debug('Max dif_ramps_Suc = %f'%dif_ramps_Suc[SUCCSESSFULLY])
		logging.debug('Mean dif_ramps_Suc = %f'%dif_ramps_Suc[SUCCSESSFULLY])

	if (len(dif_ramps_Fa)-1 > 1):
		logging.debug('Min dif_ramps_Fa = %f'%min(dif_ramps_Fa.values()))
		logging.debug('Max dif_ramps_Fa = %f'%max(dif_ramps_Fa.values()))
		logging.debug('Mean dif_ramps_Fa = %f'%statistics.mean(dif_ramps_Fa.values()))
	else:
		logging.debug('Min dif_ramps_Fa = %f'%dif_ramps_Fa[FAILED])
		logging.debug('Max dif_ramps_Fa = %f'%dif_ramps_Fa[FAILED])
		logging.debug('Mean dif_ramps_Fa = %f'%dif_ramps_Fa[FAILED])



	if (len(Coef_ramps_Suc)-1 > 1):
		logging.debug('Min Coef_ramps_Suc = %f'%min(Coef_ramps_Suc.values()))
		logging.debug('Max Coef_ramps_Suc = %f'%max(Coef_ramps_Suc.values()))
		logging.debug('Mean Coef_ramps_Suc = %f'%statistics.mean(Coef_ramps_Suc.values()))
	else:
		logging.debug('Min Coef_ramps_Suc = %f'%Coef_ramps_Suc[SUCCSESSFULLY])
		logging.debug('Max Coef_ramps_Suc = %f'%Coef_ramps_Suc[SUCCSESSFULLY])
		logging.debug('Mean Coef_ramps_Suc = %f'%Coef_ramps_Suc[SUCCSESSFULLY])

	if (len(Coef_ramps_Fa)-1 > 1):
		logging.debug('Min Coef_ramps_Fa = %f'%min(Coef_ramps_Fa.values()))
		logging.debug('Max Coef_ramps_Fa = %f'%max(Coef_ramps_Fa.values()))
		logging.debug('Mean Coef_ramps_Fa = %f'%statistics.mean(Coef_ramps_Fa.values()))
	else:
		logging.debug('Min Coef_ramps_Fa = %f'%Coef_ramps_Fa[FAILED])
		logging.debug('Max Coef_ramps_Fa = %f'%Coef_ramps_Fa[FAILED])
		logging.debug('Mean Coef_ramps_Fa = %f'%Coef_ramps_Fa[FAILED])


	if (len(Vol_Coef_Suc)-1 > 1):
		logging.debug('Min Vol_Coef_Suc = %f'%min(Vol_Coef_Suc.values()))
		logging.debug('Max Vol_Coef_Suc = %f'%max(Vol_Coef_Suc.values()))
		logging.debug('Mean Vol_Coef_Suc = %f'%statistics.mean(Vol_Coef_Suc.values()))
	else:
		logging.debug('Min Vol_Coef_Suc = %f'%Vol_Coef_Suc[SUCCSESSFULLY])
		logging.debug('Max Vol_Coef_Suc = %f'%Vol_Coef_Suc[SUCCSESSFULLY])
		logging.debug('Mean Vol_Coef_Suc = %f'%Vol_Coef_Suc[SUCCSESSFULLY])


	if (len(Vol_Coef_Fa)-1 > 1):
		logging.debug('Min Vol_Coef_Fa = %f'%min(Vol_Coef_Fa.values()))
		logging.debug('Max Vol_Coef_Fa = %f'%max(Vol_Coef_Fa.values()))
		logging.debug('Mean Vol_Coef_Fa = %f'%statistics.mean(Vol_Coef_Fa.values()))
	else:
		logging.debug('Min Vol_Coef_Fa = %f'%Vol_Coef_Fa[FAILED])
		logging.debug('Max Vol_Coef_Fa = %f'%Vol_Coef_Fa[FAILED])
		logging.debug('Mean Vol_Coef_Fa = %f'%Vol_Coef_Fa[FAILED])



	if (len(st_Suc)-1 > 1):
		logging.debug('Min st_Suc = %f'%min(st_Suc.values()))
		logging.debug('Max st_Suc = %f'%max(st_Suc.values()))
		logging.debug('Mean st_Suc = %f'%statistics.mean(st_Suc.values()))
	else:
		logging.debug('Min st_Suc = %f'%st_Suc[SUCCSESSFULLY])
		logging.debug('Max st_Suc = %f'%st_Suc[SUCCSESSFULLY])
		logging.debug('Mean st_Suc = %f'%st_Suc[SUCCSESSFULLY])

	if (len(st_Fa)-1 > 1):
		logging.debug('Min st_Fa = %f'%min(st_Fa.values()))
		logging.debug('Max st_Fa = %f'%max(st_Fa.values()))
		logging.debug('Mean st_Fa = %f'%statistics.mean(st_Fa.values()))
	else:
		logging.debug('Min st_Fa = %f'%st_Fa[FAILED])
		logging.debug('Max st_Fa = %f'%st_Fa[FAILED])
		logging.debug('Mean st_Fa = %f'%st_Fa[FAILED])









#********************************************** SELL Tester ***************************************************************
#***************************************************************************************************************************
#***************************************************************************************************************************
#***************************************************************************************************************************




def tester_strategy_bot_SELL(sym_num,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M):

	sym_input = {
	1: 'AUDCAD_i',
	2: 'AUDCHF_i',
	3: 'AUDJPY_i',
	4: 'AUDNZD_i',
	5: 'AUDUSD_i',
	6: 'CADCHF_i',
	7: 'CADJPY_i',
	8: 'CHFJPY_i',
	9: 'EURAUD_i',
	10: 'EURCAD_i',
	11: 'EURCHF_i',
	12: 'EURGBP_i',
	13: 'EURJPY_i',
	14: 'EURNZD_i',
	15: 'EURRUB_i',
	16: 'EURUSD_i',
	17: 'GBPAUD_i',
	18: 'GBPCAD_i',
	19: 'GBPCHF_i',
	20: 'GBPJPY_i',
	21: 'GBPNZD_i',
	22: 'GBPSGD_i',
	23: 'GBPUSD_i',
	24: 'NZDCAD_i',
	25: 'NZDCHF_i',
	26: 'NZDJPY_i',
	27: 'NZDUSD_i',
	28: 'USDCAD_i',
	29: 'USDCHF_i',
	30: 'USDJPY_i',
	31: 'USDSGD_i',
	32: 'XAGUSD_i',
	33: 'XAUUSD_i'
	}

	window_end = 60480
	window_start = 0

	symbols,my_money = get_symbols(10)

	hour,minute,second,day = time_func()

	log_name = 'Logs/tester_strategy_bot/bot_log_SELL_'+day+'-'+str(hour)+'-'+str(minute)+'-'+str(second)+sym_input[sym_num]+'.log'
	
	logging.basicConfig(filename=log_name, level=logging.DEBUG)

	SUCCSESSFULLY = 0
	FAILED = 0

	for sym in symbols:
		

		if (sym.name != sym_input[sym_num]):continue
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

		logging.info('**************************************************** SELL *******************************************************************')
		logging.info('****************************************************** SELL *****************************************************************')
		logging.info('**************************************************** SELL ***************************************************************')
		logging.debug('                                           %s' %sym.name)
		
		

		print(sym.name)

		counter_buy_1M = 0
		counter_buy_5M1H = 0
		counter_buy_5M30M = 0
		counter_buy_5M15M = 0
		counter_buy_15M1H = 0
		counter_buy_15M30M = 0

		counter_sell_5M1H = 0
		counter_sell_5M30M = 0
		counter_sell_5M15M = 0
		counter_sell_15M1H = 0
		counter_sell_15M30M = 0


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


		

		


		#print('')
		#print('')
		#print('***** Top Low Touceh Cheking *****')
		#print('')

		#logging.debug('***** Top Low Touceh Cheking *****')
		#logging.debug('')

		spred = 0.04#((abs(price_ask-price_bid)/price_ask) * 100)

		if (spred > 0.045):
			print('High spred')
			continue

		score_30M = 0
		tp_counter_30M = 0
		percentage_buy_tp_save_30M = {}
		percentage_buy_st_save_30M = {}
		percentage_sell_tp_save_30M = {}
		percentage_sell_st_save_30M = {}
		diff_minus_30M = 0
		diff_plus_30M = 0

		diff_counter = 0

		num_trade = 0
		#[0:window_counter_1M]

		#window_counter_1M = window_end
		#window_counter_1M = 56200
		window_counter_1M = 52000

		while window_counter_1M >= 12000:

			flag_cross_1M = ''
			flag_cross_5M = ''
			flag_cross_15M = ''
			flag_cross_5M15M = ''
			flag_cross_15M30M = ''
			flag_cross_5M1H = ''

			flag_hightouch_1D = ''
			flag_lowtouch_1D = ''
			flag_hightouch_4H = ''
			flag_lowtouch_4H = ''
			flag_hightouch_1M = ''
			flag_lowtouch_1M = ''
			flag_hightouch_1H = ''
			flag_lowtouch_1H = ''
			flag_hightouch_30M = ''
			flag_lowtouch_30M = ''
			flag_hightouch_15M = ''
			flag_lowtouch_15M = ''
			flag_hightouch_5M = ''
			flag_lowtouch_5M = ''

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
			#print(window_counter_1M)

			
			window_counter_5M = int(window_counter_1M/5)+1
			window_counter_15M = int(window_counter_5M/3)+1
			window_counter_30M = int(window_counter_15M/2)+1
			window_counter_1H = int(window_counter_30M/2)+1
			window_counter_4H = int(window_counter_1H/4)+1
			window_counter_1D = int(window_counter_4H/6)+1+458


			if ((window_counter_1M-2)<0):break
			if ((window_counter_5M-2)<0):break
			if ((window_counter_15M-2)<0):break
			if ((window_counter_30M-2)<0):break
			if ((window_counter_1H-2)<0):break
			if ((window_counter_4H-2)<0):break
			if ((window_counter_1D-2)<0):break



			try:
				# *******************++++++++++++ MACD Buy 1D************************************************************

				macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)[0:window_counter_1D]

				macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]
				macdh_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[1]]
				macds_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[2]]
				MACD_signal_cross_1D_buy = cross_macd(macd_1D_buy,macds_1D_buy,macdh_1D_buy,sym.name,data_macd_1D_buy['diff_minus'],(data_macd_1D_sell['diff_plus']/100))

				#print('MACD_signal_cross_1D_buy = ',MACD_signal_cross_1D_buy)
				macd_all_1D_buy = ind.macd(symbol_data_1D[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

				macd_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[0]]
				macdh_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[1]]
				macds_1D_buy = macd_all_1D_buy[macd_all_1D_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1D Buy Macd Wrong!!')
				logging.warning('1D Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 1D************************************************************

				macd_all_1D_sell = ind.macd(symbol_data_1D[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)[0:window_counter_1D]

				macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]
				macdh_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[1]]
				macds_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[2]]
				MACD_signal_cross_1D_sell = cross_macd(macd_1D_sell,macds_1D_sell,macdh_1D_sell,sym.name,(data_macd_1D_buy['diff_minus']/100),data_macd_1D_sell['diff_plus'])

				#print('MACD_signal_cross_1D_sell = ',MACD_signal_cross_1D_sell)
				macd_all_1D_sell = ind.macd(symbol_data_1D[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

				macd_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[0]]
				macdh_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[1]]
				macds_1D_sell = macd_all_1D_sell[macd_all_1D_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1D Sell Macd Wrong!!')
				logging.warning('1D Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			try:
				# *******************++++++++++++ MACD Buy 4H ************************************************************

				macd_all_4H_buy = ind.macd(symbol_data_4H[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)[0:window_counter_4H]

				macd_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[0]]
				macdh_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[1]]
				macds_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[2]]
				MACD_signal_cross_4H_buy = cross_macd(macd_4H_buy,macds_4H_buy,macdh_4H_buy,sym.name,data_macd_1D_buy['diff_minus'],(data_macd_1D_sell['diff_plus']/100))

				macd_all_4H_buy = ind.macd(symbol_data_4H[sym.name][data_macd_1D_buy['apply_to']],fast=data_macd_1D_buy['macd_fast'], slow=data_macd_1D_buy['macd_slow'],signal=data_macd_1D_buy['macd_signal'], verbose=True)

				macd_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[0]]
				macdh_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[1]]
				macds_4H_buy = macd_all_4H_buy[macd_all_4H_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1D Buy Macd Wrong!!')
				logging.warning('4H Buy Macd Wrong!!')

			try:

				# *******************++++++++++++ MACD 4H ************************************************************

				macd_all_4H_sell = ind.macd(symbol_data_4H[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)[0:window_counter_4H]

				macd_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[0]]
				macdh_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[1]]
				macds_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[2]]
				MACD_signal_cross_4H_sell = cross_macd(macd_4H_sell,macds_4H_sell,macdh_4H_sell,sym.name,(data_macd_1D_buy['diff_minus']/100),data_macd_1D_sell['diff_plus'])

				macd_all_4H_sell = ind.macd(symbol_data_4H[sym.name][data_macd_1D_sell['apply_to']],fast=data_macd_1D_sell['macd_fast'], slow=data_macd_1D_sell['macd_slow'],signal=data_macd_1D_sell['macd_signal'], verbose=True)

				macd_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[0]]
				macdh_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[1]]
				macds_4H_sell = macd_all_4H_sell[macd_all_4H_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1D Sell Macd Wrong!!')
				logging.warning('4H Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


			try:

				# *******************++++++++++++ MACD Buy 1H************************************************************

				macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)[0:window_counter_1H]

				macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]
				macdh_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[1]]
				macds_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[2]]
				MACD_signal_cross_1H_buy = cross_macd(macd_1H_buy,macds_1H_buy,macdh_1H_buy,sym.name,data_macd_1H_buy['diff_minus'],data_macd_1H_sell['diff_plus']/100)

				#print('MACD_signal_cross_1H_buy = ',MACD_signal_cross_1H_buy)

				macd_all_1H_buy = ind.macd(symbol_data_1H[sym.name][data_macd_1H_buy['apply_to']],fast=data_macd_1H_buy['macd_fast'], slow=data_macd_1H_buy['macd_slow'],signal=data_macd_1H_buy['macd_signal'], verbose=True)

				macd_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[0]]
				macdh_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[1]]
				macds_1H_buy = macd_all_1H_buy[macd_all_1H_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1H Buy Macd Wrong!!')
				logging.warning('1H Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 1H************************************************************

				macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)[0:window_counter_1H]

				macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]
				macdh_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[1]]
				macds_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[2]]
				MACD_signal_cross_1H_sell = cross_macd(macd_1H_sell,macds_1H_sell,macdh_1H_sell,sym.name,data_macd_1H_buy['diff_minus']/100,data_macd_1H_sell['diff_plus'])

				#print('MACD_signal_cross_1H_sell = ',MACD_signal_cross_1H_sell)

				macd_all_1H_sell = ind.macd(symbol_data_1H[sym.name][data_macd_1H_sell['apply_to']],fast=data_macd_1H_sell['macd_fast'], slow=data_macd_1H_sell['macd_slow'],signal=data_macd_1H_sell['macd_signal'], verbose=True)

				macd_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[0]]
				macdh_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[1]]
				macds_1H_sell = macd_all_1H_sell[macd_all_1H_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1H Sell Macd Wrong!!')
				logging.warning('1H Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



			try:

				# *******************++++++++++++ MACD Buy 15M************************************************************

				macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)[0:window_counter_15M]

				macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]
				macdh_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[1]]
				macds_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[2]]
				MACD_signal_cross_15M_buy = cross_macd(macd_15M_buy,macds_15M_buy,macdh_15M_buy,sym.name,data_macd_15M_buy['diff_minus'],data_macd_15M_sell['diff_plus']/100)

				#print('MACD_signal_cross_15M_buy = ',MACD_signal_cross_15M_buy)

				macd_all_15M_buy = ind.macd(symbol_data_15M[sym.name][data_macd_15M_buy['apply_to']],fast=data_macd_15M_buy['macd_fast'], slow=data_macd_15M_buy['macd_slow'],signal=data_macd_15M_buy['macd_signal'], verbose=True)

				macd_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[0]]
				macdh_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[1]]
				macds_15M_buy = macd_all_15M_buy[macd_all_15M_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('15M Buy Macd Wrong!!')
				logging.warning('15M Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 15M************************************************************

				macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)[0:window_counter_15M]

				macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]
				macdh_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[1]]
				macds_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[2]]
				MACD_signal_cross_15M_sell = cross_macd(macd_15M_sell,macds_15M_sell,macdh_15M_sell,sym.name,data_macd_15M_buy['diff_minus']/100,data_macd_15M_sell['diff_plus'])

				#print('MACD_signal_cross_15M_sell = ',MACD_signal_cross_15M_sell)

				macd_all_15M_sell = ind.macd(symbol_data_15M[sym.name][data_macd_15M_sell['apply_to']],fast=data_macd_15M_sell['macd_fast'], slow=data_macd_15M_sell['macd_slow'],signal=data_macd_15M_sell['macd_signal'], verbose=True)

				macd_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[0]]
				macdh_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[1]]
				macds_15M_sell = macd_all_15M_sell[macd_all_15M_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('15M Sell Macd Wrong!!')
				logging.warning('15M Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			#///////////////////////////////////////////////***********************-----------+++++++///////////////////////////////////////////

			try:

				# *******************++++++++++++ MACD Buy 30M************************************************************

				macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)[0:window_counter_30M]

				macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]
				macdh_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[1]]
				macds_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[2]]
				MACD_signal_cross_30M_buy = cross_macd(macd_30M_buy,macds_30M_buy,macdh_30M_buy,sym.name,data_macd_30M_buy['diff_minus'],data_macd_30M_sell['diff_plus']/100)

				#print('MACD_signal_cross_30M_buy = ',MACD_signal_cross_30M_buy)

				macd_all_30M_buy = ind.macd(symbol_data_30M[sym.name][data_macd_30M_buy['apply_to']],fast=data_macd_30M_buy['macd_fast'], slow=data_macd_30M_buy['macd_slow'],signal=data_macd_30M_buy['macd_signal'], verbose=True)

				macd_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[0]]
				macdh_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[1]]
				macds_30M_buy = macd_all_30M_buy[macd_all_30M_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('30M Buy Macd Wrong!!')
				logging.warning('30M Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 5M************************************************************

				macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)[0:window_counter_30M]

				macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]
				macdh_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[1]]
				macds_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[2]]
				MACD_signal_cross_30M_sell = cross_macd(macd_30M_sell,macds_30M_sell,macdh_30M_sell,sym.name,data_macd_30M_buy['diff_minus']/100,data_macd_30M_sell['diff_plus'])

				#print('MACD_signal_cross_30M_sell = ',MACD_signal_cross_30M_sell)

				macd_all_30M_sell = ind.macd(symbol_data_30M[sym.name][data_macd_30M_sell['apply_to']],fast=data_macd_30M_sell['macd_fast'], slow=data_macd_30M_sell['macd_slow'],signal=data_macd_30M_sell['macd_signal'], verbose=True)

				macd_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[0]]
				macdh_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[1]]
				macds_30M_sell = macd_all_30M_sell[macd_all_30M_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('30M Sell Macd Wrong!!')
				logging.warning('30M Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



			try:

				# *******************++++++++++++ MACD Buy 5M************************************************************

				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)[0:window_counter_5M]

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
				#print(window_counter_5M)
				#print(macd_5M_buy)
				macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
				macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
				MACD_signal_cross_5M_buy = cross_macd(macd_5M_buy,macds_5M_buy,macdh_5M_buy,sym.name,data_macd_5M_buy['diff_minus'],data_macd_5M_sell['diff_plus']/100)

				#print('MACD_signal_cross_5M_buy = ',MACD_signal_cross_5M_buy)
				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
				#print(window_counter_5M)
				#print(macd_5M_buy)
				macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
				macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Buy Macd Wrong!!')
				logging.warning('5M Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 5M************************************************************

				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)[0:window_counter_5M]

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
				#print(macd_5M_sell)
				macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
				macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
				MACD_signal_cross_5M_sell = cross_macd(macd_5M_sell,macds_5M_sell,macdh_5M_sell,sym.name,data_macd_5M_buy['diff_minus']/100,data_macd_5M_sell['diff_plus'])

				#print('MACD_signal_cross_5M_sell = ',MACD_signal_cross_5M_sell)

				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]
				#print(macd_5M_sell)
				macdh_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[1]]
				macds_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Sell Macd Wrong!!')
				logging.warning('5M Sell Macd Wrong!!')

			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



			try:

				# *******************++++++++++++ MACD Buy 1M************************************************************

				macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)[0:window_counter_1M]

				macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]
				#print(window_counter_1M)
				#print(macd_1M_buy)
				macdh_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[1]]
				macds_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[2]]
				MACD_signal_cross_1M_buy = cross_macd(macd_1M_buy,macds_1M_buy,macdh_1M_buy,sym.name,data_macd_1M_buy['diff_minus'],data_macd_1M_sell['diff_plus']/100)

				#print('MACD_signal_cross_1M_buy = ',MACD_signal_cross_1M_buy)

				macd_all_1M_buy = ind.macd(symbol_data_1M[sym.name][data_macd_1M_buy['apply_to']],fast=data_macd_1M_buy['macd_fast'], slow=data_macd_1M_buy['macd_slow'],signal=data_macd_1M_buy['macd_signal'], verbose=True)

				macd_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[0]]
				#print(window_counter_1M)
				#print(macd_1M_buy)
				macdh_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[1]]
				macds_1M_buy = macd_all_1M_buy[macd_all_1M_buy.columns[2]]
				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1M Buy Macd Wrong!!')
				logging.warning('1M Buy Macd Wrong!!')


			try:

				# *******************++++++++++++ MACD Sell 1M************************************************************

				macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)[0:window_counter_1M]

				macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]
				macdh_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[1]]
				macds_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[2]]
				MACD_signal_cross_1M_sell = cross_macd(macd_1M_sell,macds_1M_sell,macdh_1M_sell,sym.name,data_macd_1M_buy['diff_minus']/100,data_macd_1M_sell['diff_plus'])

				#print('MACD_signal_cross_1M_sell = ',MACD_signal_cross_1M_sell)

				macd_all_1M_sell = ind.macd(symbol_data_1M[sym.name][data_macd_1M_sell['apply_to']],fast=data_macd_1M_sell['macd_fast'], slow=data_macd_1M_sell['macd_slow'],signal=data_macd_1M_sell['macd_signal'], verbose=True)

				macd_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[0]]
				macdh_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[1]]
				macds_1M_sell = macd_all_1M_sell[macd_all_1M_sell.columns[2]]
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
						tenkan=9,kijun=26,snkou=52)[0:window_counter_30M]
				SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]][0:window_counter_30M]
				SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]][0:window_counter_30M]
				tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter_30M]
				kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter_30M]
				chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]][0:window_counter_30M]

				TsKs_signal_cross_30M = {}
				TsKs_signal_cross_30M = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

				ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_30M]
				SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
				SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
				tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]]
				kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]]
				chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('30M Buy TsKs Wrong!!')
				logging.warning('30M Buy TsKs Wrong!!')


			try:
				# *******************++++++++++++ TSKS 1D************************************************************
				ichi_1D = ind.ichimoku(high=symbol_data_1D[sym.name]['high'],low=symbol_data_1D[sym.name]['low'],close=symbol_data_1D[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_1D]
				SPANA_1D = ichi_1D[0][ichi_1D[0].columns[0]][0:window_counter_1D]
				SPANB_1D = ichi_1D[0][ichi_1D[0].columns[1]][0:window_counter_1D]
				tenkan_1D = ichi_1D[0][ichi_1D[0].columns[2]][0:window_counter_1D]
				kijun_1D = ichi_1D[0][ichi_1D[0].columns[3]][0:window_counter_1D]
				chikospan_1D = ichi_1D[0][ichi_1D[0].columns[4]][0:window_counter_1D]

				TsKs_signal_cross_1D = {}
				TsKs_signal_cross_1D = cross_TsKs_Buy_signal(tenkan_1D,kijun_1D,sym.name)

				ichi_1D = ind.ichimoku(high=symbol_data_1D[sym.name]['high'],low=symbol_data_1D[sym.name]['low'],close=symbol_data_1D[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_1D = ichi_1D[0][ichi_1D[0].columns[0]]
				SPANB_1D = ichi_1D[0][ichi_1D[0].columns[1]]
				tenkan_1D = ichi_1D[0][ichi_1D[0].columns[2]]
				kijun_1D = ichi_1D[0][ichi_1D[0].columns[3]]
				chikospan_1D = ichi_1D[0][ichi_1D[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1D Buy TsKs Wrong!!')
				logging.warning('1D Buy TsKs Wrong!!')


			try:
				# *******************++++++++++++ TSKS 1H************************************************************
				ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
					   tenkan=9,kijun=26,snkou=52)[0:window_counter_1H]
				SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]][0:window_counter_1H]
				SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]][0:window_counter_1H]
				tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]][0:window_counter_1H]
				kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]][0:window_counter_1H]
				chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]][0:window_counter_1H]

				TsKs_signal_cross_1H = {}
				TsKs_signal_cross_1H = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

				ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
					   tenkan=9,kijun=26,snkou=52)
				SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
				SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
				tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]]
				kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]]
				chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('1H Buy TsKs Wrong!!')
				logging.warning('1H Buy TsKs Wrong!!')


			try:
				# *******************++++++++++++ TSKS 4H************************************************************
				ichi_4H = ind.ichimoku(high=symbol_data_4H[sym.name]['high'],low=symbol_data_4H[sym.name]['low'],close=symbol_data_4H[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_4H]
				SPANA_4H = ichi_4H[0][ichi_4H[0].columns[0]][0:window_counter_4H]
				SPANB_4H = ichi_4H[0][ichi_4H[0].columns[1]][0:window_counter_4H]
				tenkan_4H = ichi_4H[0][ichi_4H[0].columns[2]][0:window_counter_4H]
				kijun_4H = ichi_4H[0][ichi_4H[0].columns[3]][0:window_counter_4H]
				chikospan_4H = ichi_4H[0][ichi_4H[0].columns[4]][0:window_counter_4H]

				TsKs_signal_cross_4H = {}
				TsKs_signal_cross_4H = cross_TsKs_Buy_signal(tenkan_4H,kijun_4H,sym.name)

				ichi_4H = ind.ichimoku(high=symbol_data_4H[sym.name]['high'],low=symbol_data_4H[sym.name]['low'],close=symbol_data_4H[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_4H = ichi_4H[0][ichi_4H[0].columns[0]]
				SPANB_4H = ichi_4H[0][ichi_4H[0].columns[1]]
				tenkan_4H = ichi_4H[0][ichi_4H[0].columns[2]]
				kijun_4H = ichi_4H[0][ichi_4H[0].columns[3]]
				chikospan_4H = ichi_4H[0][ichi_4H[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('4H Buy TsKs Wrong!!')
				logging.warning('4H Buy TsKs Wrong!!')


			try:

				# *******************++++++++++++ TSKS 15M************************************************************

				ichi_15M = ind.ichimoku(high=symbol_data_15M[sym.name]['high'],low=symbol_data_15M[sym.name]['low'],close=symbol_data_15M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_15M]
				SPANA_15M = ichi_15M[0][ichi_15M[0].columns[0]][0:window_counter_15M]
				SPANB_15M = ichi_15M[0][ichi_15M[0].columns[1]][0:window_counter_15M]
				tenkan_15M = ichi_15M[0][ichi_15M[0].columns[2]][0:window_counter_15M]
				kijun_15M = ichi_15M[0][ichi_15M[0].columns[3]][0:window_counter_15M]
				chikospan_15M = ichi_15M[0][ichi_15M[0].columns[4]][0:window_counter_15M]

				TsKs_signal_cross_15M = {}

				TsKs_signal_cross_15M = cross_TsKs_Buy_signal(tenkan_15M,kijun_15M,sym.name)

				ichi_15M = ind.ichimoku(high=symbol_data_15M[sym.name]['high'],low=symbol_data_15M[sym.name]['low'],close=symbol_data_15M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_15M = ichi_15M[0][ichi_15M[0].columns[0]]
				SPANB_15M = ichi_15M[0][ichi_15M[0].columns[1]]
				tenkan_15M = ichi_15M[0][ichi_15M[0].columns[2]]
				kijun_15M = ichi_15M[0][ichi_15M[0].columns[3]]
				chikospan_15M = ichi_15M[0][ichi_15M[0].columns[4]]


			except:
				#print('15M Buy TsKs Wrong!!')
				logging.warning('15M Buy TsKs Wrong!!')


			try:
				# *******************++++++++++++ TSKS 5M************************************************************
				ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_5M]
				SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]][0:window_counter_5M]
				SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]][0:window_counter_5M]
				tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter_5M]
				kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter_5M]
				chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]][0:window_counter_5M]

				TsKs_signal_cross_5M = {}
				TsKs_signal_cross_5M = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

				ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
				SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
				tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
				kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
				chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

				#*********************---------------------*************/////////////*************************************************

			except:
				#print('5M Buy TsKs Wrong!!')
				logging.warning('5M Buy TsKs Wrong!!')


			try:

				# *******************++++++++++++ TSKS 1M************************************************************

				ichi_1M = ind.ichimoku(high=symbol_data_1M[sym.name]['high'],low=symbol_data_1M[sym.name]['low'],close=symbol_data_1M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)[0:window_counter_1M]
				SPANA_1M = ichi_1M[0][ichi_1M[0].columns[0]][0:window_counter_1M]
				SPANB_1M = ichi_1M[0][ichi_1M[0].columns[1]][0:window_counter_1M]
				tenkan_1M = ichi_1M[0][ichi_1M[0].columns[2]][0:window_counter_1M]
				kijun_1M = ichi_1M[0][ichi_1M[0].columns[3]][0:window_counter_1M]
				chikospan_1M = ichi_1M[0][ichi_1M[0].columns[4]][0:window_counter_1M]

				TsKs_signal_cross_1M = {}

				TsKs_signal_cross_1M = cross_TsKs_Buy_signal(tenkan_1M,kijun_1M,sym.name)

				ichi_1M = ind.ichimoku(high=symbol_data_1M[sym.name]['high'],low=symbol_data_1M[sym.name]['low'],close=symbol_data_1M[sym.name]['close'],
						tenkan=9,kijun=26,snkou=52)
				SPANA_1M = ichi_1M[0][ichi_1M[0].columns[0]]
				SPANB_1M = ichi_1M[0][ichi_1M[0].columns[1]]
				tenkan_1M = ichi_1M[0][ichi_1M[0].columns[2]]
				kijun_1M = ichi_1M[0][ichi_1M[0].columns[3]]
				chikospan_1M = ichi_1M[0][ichi_1M[0].columns[4]]

				#print(kijun_1M)

			except:
				print('1M Buy TsKs Wrong!!')
				#logging.warning('1M Buy TsKs Wrong!!')
			#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


				#****************************************** Res_Buy_Protection_Sell ***************************************************************

			#window_counter_1M += 1
			window_counter_5M -= 1
			window_counter_15M -= 1
			window_counter_30M -= 1
			window_counter_1H -= 1
			window_counter_4H -= 1
			window_counter_1D -= 1


			if ((window_counter_1M-2)<0):break
			if ((window_counter_5M-2)<0):break
			if ((window_counter_15M-2)<0):break
			if ((window_counter_30M-2)<0):break
			if ((window_counter_1H-2)<0):break
			if ((window_counter_4H-2)<0):break
			if ((window_counter_1D-2)<0):break


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

			resist_buy_final_5M1H = {}
			protect_sell_final_5M1H = {}

			resist_buy_final_5M30M = {}
			protect_sell_final_5M30M = {}

			resist_buy_final_5M15M = {}
			protect_sell_final_5M15M = {}

			resist_buy_final_15M1H = {}
			protect_sell_final_15M1H = {}

			resist_buy_final_15M30M = {}
			protect_sell_final_15M30M = {}


			

				#resist_buy_final_5M = {}
				#protect_sell_final_5M = {}

			try:
				with open("Res_Buy_Protection_Sell/1D/"+sym.name+'.csv', 'r', newline='') as myfile:

					for line in csv.DictReader(myfile):
						for l in line.values():

							resist_buy[i] = float(l)
							protect_sell[i] = float(l)

							if (((symbol_data_1D[sym.name]['open'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['open'][(window_counter_1D-1 - 1)])/2) < resist_buy[i]):
								resist_buy_final_1D[j] = resist_buy[i]
								resist_buy_final[j] = resist_buy[i]

								j += 1

							if (((symbol_data_1D[sym.name]['open'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['open'][(window_counter_1D-1 - 1)])/2) < resist_buy[i]):
								resist_buy_final_1D[j] = resist_buy[i]
								resist_buy_final[j] = resist_buy[i]
								j += 1
							if (((symbol_data_1D[sym.name]['open'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['open'][(window_counter_1D-1 - 1)])/2) < protect_sell[i]):
								protect_sell_final_1D[j] = protect_sell[i]
								protect_sell_final[j] = protect_sell[i]
								j += 1
							if (((symbol_data_1D[sym.name]['open'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['open'][(window_counter_1D-1 - 1)])/2) < protect_sell[i]):
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
					for line in csv.DictReader(myfile):
						for l in line.values():
							resist_buy[i] = float(l)
							protect_sell[i] = float(l)

							if (((symbol_data_4H[sym.name]['open'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['open'][(window_counter_4H-1 - 1)])/2) < resist_buy[i]):
								resist_buy_final_4H[j] = resist_buy[i]
								resist_buy_final[j] = resist_buy[i]
								j += 1
							if (((symbol_data_4H[sym.name]['open'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['open'][(window_counter_4H-1 - 1)])/2) < resist_buy[i]):
								resist_buy_final_4H[j] = resist_buy[i]
								resist_buy_final[j] = resist_buy[i]
								j += 1
							if (((symbol_data_4H[sym.name]['open'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['open'][(window_counter_4H-1 - 1)])/2) < protect_sell[i]):
								protect_sell_final_4H[j] = protect_sell[i]
								protect_sell_final[j] = protect_sell[i]
								j += 1

							if (((symbol_data_4H[sym.name]['open'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['open'][(window_counter_4H -1- 1)])/2) < protect_sell[i]):
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
					price_ask = ((symbol_data_1H[sym.name]['open'][(window_counter_1H-1)] + symbol_data_1H[sym.name]['open'][(window_counter_1H-1 - 1)])/2)
					price_bid = ((symbol_data_1H[sym.name]['open'][(window_counter_1H-1)] + symbol_data_1H[sym.name]['open'][(window_counter_1H-1 - 1)])/2)

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
					price_ask = ((symbol_data_30M[sym.name]['open'][(window_counter_30M-1)] + symbol_data_30M[sym.name]['open'][(window_counter_30M-1 - 1)])/2)
					price_bid = ((symbol_data_30M[sym.name]['open'][(window_counter_30M-1)] + symbol_data_30M[sym.name]['open'][(window_counter_30M-1 - 1)])/2)

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


			resist_buy = {}
			protect_sell = {}


			try:
				with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
					price_ask = ((symbol_data_1M[sym.name]['open'][(window_counter_1M-1)] + symbol_data_1M[sym.name]['open'][(window_counter_1M-1 - 1)])/2)
					price_bid = ((symbol_data_1M[sym.name]['open'][(window_counter_1M-1)] + symbol_data_1M[sym.name]['open'][(window_counter_1M-1 - 1)])/2)

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



			resist_buy_find = -100000000000
			protect_sell_find = -100000000000

			resist_buy_find_1D = -100000000000
			protect_sell_find_1D = -100000000000

			resist_buy_find_4H = -100000000000
			protect_sell_find_4H = -100000000000
			resist_buy_find_1H = -100000000000
			protect_sell_find_1H = -100000000000


			resist_buy_find_30M = -100000000000
			protect_sell_find_30M = -100000000000

			resist_buy_find_1M = -100000000000
			protect_sell_find_1M = -100000000000

			resist_buy_find_5M1H = -100000000000
			protect_sell_find_5M1H = -100000000000

			resist_buy_find_5M30M = -100000000000
			protect_sell_find_5M30M = -100000000000

			resist_buy_find_5M15M = -100000000000
			protect_sell_find_5M15M = -100000000000

			resist_buy_find_15M1H = -100000000000
			protect_sell_find_15M1H = -100000000000

			resist_buy_find_5M30M = -100000000000
			protect_sell_find_5M30M = -100000000000


			try:
				if (len(resist_buy_final.values()) >1):
					resist_buy_find = min(resist_buy_final.values())
				else:
					resist_buy_find = resist_buy_final.values()

				if (len(protect_sell_final.values()) >1):
					protect_sell_find = min(protect_sell_final.values())
				else:
					protect_sell_find = protect_sell_final.values()

#********************************** 1D *****************************************************************************
				if (len(resist_buy_final_1D.values()) >1):
					resist_buy_find_1D = min(resist_buy_final_1D.values())
				else:
					resist_buy_find_1D = resist_buy_final_1D.values()

				if (len(protect_sell_final_1D.values()) >1):
					protect_sell_find_1D = min(protect_sell_final_1D.values())
				else:
					protect_sell_find_1D = protect_sell_final_1D.values()
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#************************************* 4H ****************************************************************************
				if (len(resist_buy_final_4H.values()) >1):
					resist_buy_find_4H = min(resist_buy_final_4H.values())
				else:
					resist_buy_find_4H = resist_buy_final_4H.values()

				if (len(protect_sell_final_4H.values()) >1):
					protect_sell_find_4H = min(protect_sell_final_4H.values())
				else:
					protect_sell_find_4H = protect_sell_final_4H.values()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
#********************************* 1H ****************************************************************************
				if (len(resist_buy_final_1H.values()) >1):
					resist_buy_find_1H = min(resist_buy_final_1H.values())
				else:
					resist_buy_find_1H = resist_buy_final_1H.values()

				if (len(protect_sell_final_1H.values()) >1):
					protect_sell_find_1H = min(protect_sell_final_1H.values())
				else:
					protect_sell_find_1H = min(protect_sell_final_1H.values())
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#************************************ 30M ******************************************************************************
				if (len(resist_buy_final_30M.values()) >1):
					resist_buy_find_30M = min(resist_buy_final_30M.values())
				else:
					resist_buy_find_30M = resist_buy_final_30M.values()

				if (len(protect_sell_final_30M.values()) >1):
					protect_sell_find_30M = min(protect_sell_final_30M.values())
				else:
					protect_sell_find_30M = protect_sell_final_30M.values()
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////
#*********************************** 1M ******************************************************************************
				if (len(resist_buy_final_1M.values()) >1):
					resist_buy_find_1M = min(resist_buy_final_1M.values())
				else:
					resist_buy_find_1M = resist_buy_final_1M.values()

				if (len(protect_sell_final_1M.values()) >1):
					protect_sell_find_1M = min(protect_sell_final_1M.values())
				else:
					protect_sell_find_1M = protect_sell_final_1M.values()
					#protect_sell_find_1M = min(protect_sell_find_1M,protect_sell_find_30M,protect_sell_find_1H,protect_sell_find_4H,protect_sell_find_1D)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////

			except:
					#print('some thing wrongt Res_Buy_Protection_Sell')
				logging.warning('some thing wrongt Res_Buy_Protection_Sell')
					#break

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

			protect_buy_final_5M1H = {}
			resist_sell_final_5M1H = {}

			protect_buy_final_5M30M = {}
			resist_sell_final_5M30M = {}

			protect_buy_final_5M15M = {}
			resist_sell_final_5M15M = {}

			protect_buy_final_15M1H = {}
			resist_sell_final_15M1H = {}

			protect_buy_final_15M30M = {}
			resist_sell_final_15M30M = {}



			try:
				with open("Res_Sell_Protection_Buy/1D/"+sym.name+'.csv', 'r', newline='') as myfile:

					for line in csv.DictReader(myfile):

						for l in line.values():

							protect_buy[i] = float(l)
							resist_sell[i] = float(l)

							if (((symbol_data_1D[sym.name]['close'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['close'][(window_counter_1D-1 - 1)])/2) > protect_buy[i]):
								protect_buy_final_1D[j] = protect_buy[i]
								protect_buy_final[j] = protect_buy[i]
								j += 1

							if (((symbol_data_1D[sym.name]['close'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['close'][(window_counter_1D-1 - 1)])/2) > protect_buy[i]):
								protect_buy_final_1D[j] = protect_buy[i]
								protect_buy_final[j] = protect_buy[i]
								j += 1

							if (((symbol_data_1D[sym.name]['close'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['close'][(window_counter_1D-1 - 1)])/2) > resist_sell[i]):
								resist_sell_final_1D[j] = resist_sell[i]
								resist_sell_final[j] = resist_sell[i]
								j += 1

							if (((symbol_data_1D[sym.name]['close'][(window_counter_1D-1)] + symbol_data_1D[sym.name]['close'][(window_counter_1D-1 - 1)])/2) > resist_sell[i]):
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

					for line in csv.DictReader(myfile):

						for l in line.values():

							protect_buy[i] = float(l)
							resist_sell[i] = float(l)

							if (((symbol_data_4H[sym.name]['close'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['close'][(window_counter_4H-1 - 1)])/2) > protect_buy[i]):
								protect_buy_final_4H[j] = protect_buy[i]
								protect_buy_final[j] = protect_buy[i]
								j += 1

							if (((symbol_data_4H[sym.name]['close'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['close'][(window_counter_4H-1 - 1)])/2) > protect_buy[i]):
								protect_buy_final_4H[j] = protect_buy[i]
								protect_buy_final[j] = protect_buy[i]
								j += 1

							if (((symbol_data_4H[sym.name]['close'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['close'][(window_counter_4H-1 - 1)])/2) > resist_sell[i]):
								resist_sell_final_4H[j] = resist_sell[i]
								resist_sell_final[j] = resist_sell[i]
								j += 1

							if (((symbol_data_4H[sym.name]['close'][(window_counter_4H-1)] + symbol_data_4H[sym.name]['close'][(window_counter_4H-1 - 1)])/2) > resist_sell[i]):
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
					price_ask = ((symbol_data_1H[sym.name]['close'][(window_counter_1H-1)] + symbol_data_1H[sym.name]['close'][(window_counter_1H-1 - 1)])/2)
					price_bid = ((symbol_data_1H[sym.name]['close'][(window_counter_1H-1)] + symbol_data_1H[sym.name]['close'][(window_counter_1H-1 - 1)])/2)

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
					price_ask = ((symbol_data_30M[sym.name]['close'][(window_counter_30M-1)] + symbol_data_30M[sym.name]['close'][(window_counter_30M-1 - 1)])/2)
					price_bid = ((symbol_data_30M[sym.name]['close'][(window_counter_30M-1)] + symbol_data_30M[sym.name]['close'][(window_counter_30M-1 - 1)])/2)

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
				logging.warning('some thing wrongt Res_Sell_Protection_Buy 30M')


			protect_buy = {}
			resist_sell = {}


			try:
				with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
					price_ask = ((symbol_data_1M[sym.name]['close'][(window_counter_1M-1)] + symbol_data_1M[sym.name]['close'][(window_counter_1M-1 - 1)])/2)
					price_bid = ((symbol_data_1M[sym.name]['close'][(window_counter_1M-1)] + symbol_data_1M[sym.name]['close'][(window_counter_1M-1 - 1)])/2)

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
				logging.warning('some thing wrongt Res_Sell_Protection_Buy 1M')

			protect_buy = {}
			resist_sell = {}


			protect_buy_find = -100000000000
			resist_sell_find = -100

			protect_buy_find_1D = -100000000000
			resist_sell_find_1D = -100

			protect_buy_find_4H = -100000000000
			resist_sell_find_4H = -100

			protect_buy_find_1H = -100000000000
			resist_sell_find_1H = -100

			protect_buy_find_30M = -100000000000
			resist_sell_find_30M = -100

			protect_buy_find_1M = -100
			resist_sell_find_1M = -100

			protect_buy_find_5M1H = -100
			resist_sell_find_5M1H = -100

			protect_buy_find_5M30M = -100
			resist_sell_find_5M30M = -100

			protect_buy_find_5M15M = -100
			resist_sell_find_5M15M = -100

			protect_buy_find_15M1H = -100
			resist_sell_find_15M1H = -100

			protect_buy_find_15M30M = -100
			resist_sell_find_15M30M = -100

			try:
				#************************** FULl **********************************************************
				if (len(protect_buy_final.values()) >1):
					protect_buy_find = max(protect_buy_final.values())
				else:
					protect_buy_find = max(protect_buy_final.values())

				if (len(resist_sell_final.values()) >1):
					resist_sell_find = max(resist_sell_final.values())
				else:
					resist_sell_find = resist_sell_final.values()
#//////////////////////////////////////////////////////////////////////////////////////////////
#******************************* 1D ********************************************************************					
				if (len(protect_buy_final_1D.values()) >1):
					protect_buy_find_1D = max(protect_buy_final_1D.values())
				else:
					protect_buy_find_1D = protect_buy_final_1D.values()

				if (len(resist_sell_final_1D.values()) >1):
					resist_sell_find_1D = max(resist_sell_final_1D.values())
				else:
					resist_sell_find_1D = resist_sell_final_1D.values()
#////////////////////////////////////////////////////////////////////////////////////////////////
#******************************* 4H ***********************************************************************
				if (len(protect_buy_final_4H.values()) >1):
					protect_buy_find_4H = max(protect_buy_final_4H.values())
				else:
					protect_buy_find_4H = protect_buy_final_4H.values()

				if (len(resist_sell_final_4H.values()) >1):
					resist_sell_find_4H = max(resist_sell_final_4H.values())
				else:
					resist_sell_find_4H = resist_sell_final_4H.values()
#////////////////////////////////////////////////////////////////////////////////////////////
#************************************** 1H ***********************************************************
				if (len(protect_buy_final_1H.values()) >1):
					protect_buy_find_1H = max(protect_buy_final_1H.values())
				else:
					protect_buy_find_1H = protect_buy_final_1H.values()

				if (len(resist_sell_final_1H.values()) >1):
					resist_sell_find_1H = max(resist_sell_final_1H.values())
				else:
					resist_sell_find_1H = resist_sell_final_1H.values()
#////////////////////////////////////////////////////////////////////////////////////////
#*********************************** 30M *********************************************************
				if (len(protect_buy_final_30M.values()) >1):
					protect_buy_find_30M = max(protect_buy_final_30M.values())
				else:
					protect_buy_find_30M = protect_buy_final_30M.values()

				if (len(resist_sell_final_30M.values()) >1):
					resist_sell_find_30M = max(resist_sell_final_30M.values())
				else:
					resist_sell_find_30M = resist_sell_final_30M.values()
#//////////////////////////////////////////////////////////////////////////////////////
#******************************** 1M ***************************************************************
				if (len(protect_buy_final_1M.values()) >1):
					protect_buy_find_1M = max(protect_buy_final_1M.values())	
				else:
					protect_buy_find_1M = protect_buy_final_1M.values()

				if (len(resist_sell_final_1M.values()) >1):
					resist_sell_find_1M = max(resist_sell_final_1M.values())
					resist_sell_find_1M = max(resist_sell_find_1M,resist_sell_find_1H,resist_sell_find_4H,resist_sell_find_1D)
				else:
					resist_sell_find_1M = resist_sell_final_1M.values()
					resist_sell_find_1M = max(resist_sell_find_1M,resist_sell_find_1H,resist_sell_find_4H,resist_sell_find_1D)
#////////////////////////////////////////////////////////////////////////////////////////////////////////
			except:
				logging.warning('some thing wrongt Res_Sell_Protection_Buy')
			

			window_counter_1M -= 1
			window_counter_5M -= 1
			window_counter_15M -= 1
			window_counter_30M -= 1
			window_counter_1H -= 1
			window_counter_4H -= 1
			window_counter_1D -= 1

			coef_1M = 0.1
			coef_5M = 0.1
			coef_15M = 0.1

			if (sym.name == 'XAUUSD_i'):
				coef_1M = 0.01
				coef_5M = 0.1
				coef_15M = 0.1


			#****************--------------------++++++++++++++++++++++++***** 1M ***********************************************************++++++++++++++++++++++
			#log_multi_account(1001)
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_1M_SELL = MACD_signal_cross_1M_sell['index']
								end_search_counter = (window_counter_1M)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_1M_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_1M[sym.name]['HLC/3'][(search_counter_1M_SELL)] + symbol_data_1M[sym.name]['HLC/3'][(search_counter_1M_SELL - 1)])/2)
											price_bid = ((symbol_data_1M[sym.name]['close'][(search_counter_1M_SELL)] + symbol_data_1M[sym.name]['close'][(search_counter_1M_SELL - 1)])/2)

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
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 1M')

									resist_sell_find_1M = max(resist_sell_final_1M.values())
									resist_sell_find_1M = max(resist_sell_find_1M,resist_sell_find_4H,resist_sell_find_1D)

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_1M[sym.name]['open'][(search_counter_1M_SELL)] + symbol_data_1M[sym.name]['open'][(search_counter_1M_SELL - 1)])/2)
											price_bid = ((symbol_data_1M[sym.name]['high'][(search_counter_1M_SELL)] + symbol_data_1M[sym.name]['high'][(search_counter_1M_SELL - 1)])/2)

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

									protect_sell_find_1M = min(protect_sell_final_1M.values())
									protect_sell_find_1M = min(protect_sell_find_1M,protect_sell_find_4H,protect_sell_find_1D)


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)

									if (((abs(symbol_data_1M[sym.name]['low'][search_counter_1M_SELL]-protect_sell_find_1M)/symbol_data_1M[sym.name]['low'][search_counter_1M_SELL]) * 100) < ((((protect_sell_find_1M-resist_sell_find_1M)/resist_sell_find_1M) * 100)*coef_1M)):
										#print('sell 4 1M: candle under cloud ')
										if (protect_sell_find_1M < resist_sell_find_1M): continue
										if ((macds_1M_sell[search_counter_1M_SELL] <= macd_1M_sell[search_counter_1M_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_1M[(search_counter_1M_SELL-26)] > symbol_data_1M[sym.name]['high'][(search_counter_1M_SELL)]):
												#print('sell 6 1M: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_5M_sell[(int(search_counter_1M_SELL/5))] <= macd_5M_sell[(int(search_counter_1M_SELL/5))]):
													#print('sell 7 1M: candle under TSKS ')
													if (chikospan_5M[(int(search_counter_1M_SELL/5)-26)] > symbol_data_5M[sym.name]['high'][(int(search_counter_1M_SELL/5))]):
														#print('int(search_counter_1M_SELL/5) - 1 = ',int(search_counter_1M_SELL/5) - 1)
														if (tenkan_1M[search_counter_1M_SELL] >= kijun_1M[search_counter_1M_SELL]):
															#print('sell 8 1M: candle under TSKS ')
															if True:#(tenkan_5M[(int(search_counter_1M_SELL/5))] >= kijun_5M[(int(search_counter_1M_SELL/5))]):

																if (symbol_data_1M[sym.name]['low'][search_counter_1M_SELL] >= tenkan_1M[search_counter_1M_SELL]):
																	#print('sell 9 1M: candle under TSKS ')
																	if True:#(symbol_data_5M[sym.name]['low'][(int(search_counter_1M_SELL/5))] >= tenkan_5M[(int(search_counter_1M_SELL/5))]):
																		#print('sell 10 1M: candle under TSKS ')
																		if ((symbol_data_1M[sym.name]['low'][search_counter_1M_SELL] >= SPANA_1M[search_counter_1M_SELL]) & (symbol_data_1M[sym.name]['low'][search_counter_1M_SELL] >= SPANB_1M[search_counter_1M_SELL])):
																			#print('sell 11 1M: candle under TSKS ')
																			if True:#((symbol_data_5M[sym.name]['low'][(int(search_counter_1M_SELL/5))] >= SPANA_5M[(int(search_counter_1M_SELL/5))]) & (symbol_data_5M[sym.name]['low'][(int(search_counter_1M_SELL/5))] >= SPANB_5M[(int(search_counter_1M_SELL/5))])):
																				#print('sell 12 1M: candle under TSKS ')
																				price_bid = mt5.symbol_info_tick(sym.name).bid
																				if (macds_15M_sell[(int(search_counter_1M_SELL/15))] <= macd_15M_sell[(int(search_counter_1M_SELL/15))]):
																					#print('Pre Finish 1M SELL: ',sym.name)
																					#logging.debug('Pre Finish 1M SELL: %s'%sym.name)
																					if (macds_1H_sell[(int(search_counter_1M_SELL/60))] <= macd_1H_sell[(int(search_counter_1M_SELL/60))]):
																						flag_cross_1M = 'sell'

																						signal_counter_1M_sell = search_counter_1M_SELL

																						#print('sell finished 1M: ',sym.name)
																						#logging.debug('sell finished 1M: %s'%sym.name)

																					else:
																						flag_cross_1M = 'failed_sell'
																				else:
																					flag_cross_1M = 'failed_sell'

																			#if (((MACD_signal_cross_1M_buy['signal'] == 'buy') | (MACD_signal_cross_1M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1M_buy['index'] >= ((search_counter_1M_SELL) - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			#if (((MACD_signal_cross_5M_buy['signal'] == 'buy') | (MACD_signal_cross_5M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_5M_buy['index'] >= (int(search_counter_1M_SELL/5) - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_1M_SELL/1440)+458 - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_1M_SELL/1440)+458 - 6))):
																			#	flag_cross_1M = 'failed_sell'

																			if (macds_1D_buy[int(search_counter_1M_SELL/1440)+458] <= macd_1D_buy[int(search_counter_1M_SELL/1440)+458]):
																				flag_cross_1M = 'failed_sell'

																			if (macds_4H_buy[int(search_counter_1M_SELL/240)] < macd_4H_buy[int(search_counter_1M_SELL/240)]):
																				flag_cross_1M = 'failed_sell'

																			#print('******************** flag_cross_1M = ',flag_cross_1M)

																			if (flag_cross_1M == 'sell'): 
																				#print('******************************************sell 1***********************************************************')
																				#logging.warning('break')
																				break

									#if ((symbol_data_1M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_1M[sym.name]['high'] - 1) - 10))):
										#flag_cross_1M = 'low_toched'
										#print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++low toched 1M++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_1M_SELL += 1
									#touch_counter -= 1
			except:
				print('signal problem 1M SELL MACD!!!')
				#logging.warning('signal problem 1M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


			#****************--------------------++++++++++++++++++++++++*********** 5M 1H *****************************************************++++++++++++++++++++++
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_5M1H_SELL = MACD_signal_cross_5M_sell['index']
								end_search_counter = (window_counter_5M)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_5M1H_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M1H_SELL)] + symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M1H_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['close'][(search_counter_5M1H_SELL)] + symbol_data_5M[sym.name]['close'][(search_counter_5M1H_SELL - 1)])/2)

											for line in csv.DictReader(myfile):

												for l in line.values():

													protect_buy[i] = float(l)
													resist_sell[i] = float(l)

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M1H[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M1H[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M1H[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M1H[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													i += 1

									except:
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

									resist_sell_find_5M1H = max(resist_sell_final_5M1H.values())
									resist_sell_find_5M1H = max(resist_sell_find_5M1H,resist_sell_find_4H,resist_sell_find_1D)

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['open'][(search_counter_5M1H_SELL)] + symbol_data_5M[sym.name]['open'][(search_counter_5M1H_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['high'][(search_counter_5M1H_SELL)] + symbol_data_5M[sym.name]['high'][(search_counter_5M1H_SELL - 1)])/2)

											for line in csv.DictReader(myfile):
												for l in line.values():

													resist_buy[i] = float(l)
													protect_sell[i] = float(l)

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M1H[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M1H[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M1H[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M1H[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1
						
													i += 1

									except:
					#print('some thing wrongt Res_Buy_Protection_Sell 4H')
										logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

									protect_sell_find_5M1H = min(protect_sell_final_5M1H.values())
									protect_sell_find_5M1H = min(protect_sell_find_5M1H,protect_sell_find_4H,protect_sell_find_1D)


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)
									if (((abs(symbol_data_5M[sym.name]['low'][search_counter_5M1H_SELL]-protect_sell_find_5M1H)/symbol_data_5M[sym.name]['low'][search_counter_5M1H_SELL]) * 100) < ((((protect_sell_find_5M1H-resist_sell_find_5M1H)/resist_sell_find_5M1H) * 100)*coef_5M)):
										if (protect_sell_find_5M1H < resist_sell_find_5M1H): continue
										#print('sell 4 5M1H: candle under cloud ')
										if ((macds_5M_sell[search_counter_5M1H_SELL] <= macd_5M_sell[search_counter_5M1H_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_5M[(search_counter_5M1H_SELL-26)] > symbol_data_5M[sym.name]['high'][(search_counter_5M1H_SELL)]):
												#print('sell 6 5M1H: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_1H_sell[(int(search_counter_5M1H_SELL/12))] <= macd_1H_sell[(int(search_counter_5M1H_SELL/12))]):
													#print('sell 7 5M1H: candle under TSKS ')
													if (chikospan_1H[((int(search_counter_5M1H_SELL/12))-26)] > symbol_data_1H[sym.name]['high'][((int(search_counter_5M1H_SELL/12)))]):
														#print('int(search_counter_5M1H_SELL/5) - 1 = ',int(search_counter_5M1H_SELL/12) - 1)
														if (tenkan_5M[search_counter_5M1H_SELL] > kijun_5M[search_counter_5M1H_SELL]):
															#print('sell 9 5M1H: candle under TSKS ')
															if True:#(tenkan_1H[(int(search_counter_5M1H_SELL/12))] >= kijun_1H[(int(search_counter_5M1H_SELL/12))]):
																#print('sell 10 5M1H: candle under TSKS ')
																if (symbol_data_5M[sym.name]['low'][search_counter_5M1H_SELL] >= tenkan_5M[search_counter_5M1H_SELL]):
																	#print('sell 11 5M1H: candle under TSKS ')
																	if True:#(symbol_data_1H[sym.name]['low'][(int(search_counter_5M1H_SELL/12))] >= tenkan_1H[(int(search_counter_5M1H_SELL/12))]):
																		if ((symbol_data_5M[sym.name]['low'][search_counter_5M1H_SELL] >= SPANA_5M[search_counter_5M1H_SELL]) & (symbol_data_5M[sym.name]['low'][search_counter_5M1H_SELL] >= SPANB_5M[search_counter_5M1H_SELL])):
																			#price_bid = mt5.symbol_info_tick(sym.name).bid
																			if True:#((symbol_data_1H[sym.name]['low'][(int(search_counter_5M1H_SELL/12))] >= SPANA_1H[(int(search_counter_5M1H_SELL/12))]) & (symbol_data_1H[sym.name]['low'][(int(search_counter_5M1H_SELL/12))] >= SPANB_1H[(int(search_counter_5M1H_SELL/12))])):
																				#print('Pre Finish 5M1H SELL: ',sym.name)
																				#logging.debug('Pre Finish 5M1H SELL: %s'%sym.name)
																				if True:#((flag_cross_5M1H != 'low_toched') & ((((protect_sell_find-price_bid)/price_bid) * 100) < ((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))):
																					flag_cross_5M1H = 'sell'

																					signal_counter_5M1H_sell = search_counter_5M1H_SELL
																					#print('sell finished 5M: ',sym.name)
																					#logging.debug('sell finished 5M: %s'%sym.name)

																				else:
																					flag_cross_5M1H = 'failed_sell'
																			else:
																				flag_cross_5M1H = 'failed_sell'


																	#if (((MACD_signal_cross_5M_buy['signal'] == 'buy') | (MACD_signal_cross_5M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_5M_buy['index'] >= (int(search_counter_5M1H_SELL) - 6))):
																	#	flag_cross_5M1H = 'failed_sell'

																	#if (((MACD_signal_cross_1H_buy['signal'] == 'buy') | (MACD_signal_cross_1H_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1H_buy['index'] >= (int(search_counter_5M1H_SELL/12) - 6))):
																	#	flag_cross_5M1H = 'failed_sell'

																	#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_5M1H_SELL/288)+458 - 6))):
																	#	flag_cross_5M1H = 'failed_sell'

																	#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_5M1H_SELL/288)+458 - 6))):
																	#	flag_cross_5M1H = 'failed_sell'

																	if (macds_1D_buy[int(search_counter_5M1H_SELL/288)+458] <= macd_1D_buy[int(search_counter_5M1H_SELL/288)+458]):
																		flag_cross_5M1H = 'failed_sell'

																	if (macds_4H_buy[int(search_counter_5M1H_SELL/48)] < macd_4H_buy[int(search_counter_5M1H_SELL/48)]):
																		flag_cross_5M1H = 'failed_sell'

																	if (flag_cross_5M1H == 'sell'): 
																		#print('sell 1')
																		break


									#if ((symbol_data_5M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_5M[sym.name]['high'] - 1) - 30))):
									#	flag_cross_5M1H = 'low_toched'
									#	print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++low toched 5M1H++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_5M1H_SELL += 1
									#touch_counter -= 1
			except:
				print('signal problem 5M SELL MACD!!!')
				#logging.warning('signal problem 5M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


			#****************--------------------++++++++++++++++++++++++*********** 5M *****************************************************++++++++++++++++++++++
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_5M30M_SELL = int(MACD_signal_cross_5M_sell['index'])
								end_search_counter = int(window_counter_5M)

								#print('search_counter_5M15M_SELL = ',search_counter_5M15M_SELL)
								#print('end_search_counter = ',end_search_counter)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_5M30M_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M30M_SELL)] + symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M30M_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['close'][(search_counter_5M30M_SELL)] + symbol_data_5M[sym.name]['close'][(search_counter_5M30M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):

												for l in line.values():

													protect_buy[i] = float(l)
													resist_sell[i] = float(l)

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M30M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M30M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M30M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M30M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													i += 1

									except:
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

									try:
										resist_sell_find_5M30M = max(resist_sell_final_5M30M.values())
										resist_sell_find_5M30M = max(resist_sell_find_5M30M,resist_sell_find_4H,resist_sell_find_1D)
									except:
										print('No Data')

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['open'][(search_counter_5M30M_SELL)] + symbol_data_5M[sym.name]['open'][(search_counter_5M30M_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['high'][(search_counter_5M30M_SELL)] + symbol_data_5M[sym.name]['high'][(search_counter_5M30M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):
												for l in line.values():

													resist_buy[i] = float(l)
													protect_sell[i] = float(l)

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M30M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M30M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M30M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M30M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1
						
													i += 1

									except:
					#print('some thing wrongt Res_Buy_Protection_Sell 4H')
										logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

									try:
										protect_sell_find_5M30M = min(protect_sell_final_5M30M.values())
										protect_sell_find_5M30M = min(protect_sell_find_5M30M,protect_sell_find_4H,protect_sell_find_1D)
									except:
										print('No Data')


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)
									if (((abs(symbol_data_5M[sym.name]['low'][search_counter_5M30M_SELL]-protect_sell_find_5M30M)/symbol_data_5M[sym.name]['low'][search_counter_5M30M_SELL]) * 100) < ((((protect_sell_find_5M30M-resist_sell_find_5M30M)/resist_sell_find_5M30M) * 100)*coef_5M)):
										if (protect_sell_find_5M30M < resist_sell_find_5M30M): continue
										#print('sell 4 5M15M: candle under cloud ')
										if ((macds_5M_sell[search_counter_5M30M_SELL] <= macd_5M_sell[search_counter_5M30M_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_5M[(search_counter_5M30M_SELL-26)] > symbol_data_5M[sym.name]['high'][(search_counter_5M30M_SELL)]):
												#print('sell 6 5M15M: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_30M_sell[(int(search_counter_5M30M_SELL/6))] <= macd_30M_sell[(int(search_counter_5M30M_SELL/6))]):
													#print('sell 7 5M15M: candle under TSKS ')
													if (chikospan_30M[(int(search_counter_5M30M_SELL/6))-26] > symbol_data_30M[sym.name]['high'][(int(search_counter_5M30M_SELL/6))]):
														#print('int(search_counter_5M15M_SELL/5) - 1 = ',int(search_counter_5M30M_SELL/6) - 1)
														#print('sell 8 5M: candle under TSKS ')
														if (tenkan_5M[search_counter_5M30M_SELL] >= kijun_5M[search_counter_5M30M_SELL]):
															#print('sell 9 5M: candle under TSKS ')
															if True:#(tenkan_30M[(int(search_counter_5M30M_SELL/6))] >= kijun_30M[(int(search_counter_5M30M_SELL/6))]):
																#print('sell 10 5M: candle under TSKS ')
																if (symbol_data_5M[sym.name]['low'][search_counter_5M30M_SELL] >= tenkan_5M[search_counter_5M30M_SELL]):
																	#print('sell 11 5M: candle under TSKS ')
																	if True:#(symbol_data_30M[sym.name]['low'][(int(search_counter_5M30M_SELL/6))] >= tenkan_30M[(int(search_counter_5M30M_SELL/6))]):
																		#print('sell 12 5M: candle under SPAN D1 ')
																		if ((symbol_data_5M[sym.name]['low'][search_counter_5M30M_SELL] >= SPANA_5M[search_counter_5M30M_SELL]) & (symbol_data_5M[sym.name]['low'][search_counter_5M30M_SELL] >= SPANB_5M[search_counter_5M30M_SELL])):
																			#price_bid = mt5.symbol_info_tick(sym.name).bid
																			if True:#((symbol_data_30M[sym.name]['low'][(int(search_counter_5M30M_SELL/6))] >= SPANA_30M[(int(search_counter_5M30M_SELL/6))]) & (symbol_data_30M[sym.name]['low'][(int(search_counter_5M30M_SELL/6))] >= SPANB_30M[(int(search_counter_5M30M_SELL/6))])):
																				#print('sell 13 5M: res pro ',flag_cross_5M)
																				#print('Pre Finish 5M30M SELL: ',sym.name)
																				#logging.debug('Pre Finish 5M30M SELL: %s'%sym.name)
																				if True:#((flag_cross_5M != 'low_toched') & ((((protect_sell_find-price_bid)/price_bid) * 100) < ((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))):
																					flag_cross_5M = 'sell'

																					signal_counter_5M_sell = search_counter_5M30M_SELL

																					#print('sell finished 5M: ',sym.name)
																					#logging.debug('sell finished 5M: %s'%sym.name)

																				else:
																					flag_cross_5M = 'failed_sell'
																			else:
																				flag_cross_5M = 'failed_sell'


																	#if (((MACD_signal_cross_5M_buy['signal'] == 'buy') | (MACD_signal_cross_5M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_5M_buy['index'] >= (int(search_counter_5M30M_SELL) - 6))):
																	#	flag_cross_5M = 'failed_sell'

																	#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(search_counter_5M30M_SELL/6) - 6))):
																	#	flag_cross_5M = 'failed_sell'

																	#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_5M30M_SELL/288)+458 - 6))):
																	#	flag_cross_5M = 'failed_sell'

																	#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_5M30M_SELL/288)+458 - 6))):
																	#	flag_cross_5M = 'failed_sell'

																	if (macds_1D_buy[int(search_counter_5M30M_SELL/288)+458] <= macd_1D_buy[int(search_counter_5M30M_SELL/288)+458]):
																		flag_cross_5M = 'failed_sell'

																	if (macds_4H_buy[int(search_counter_5M30M_SELL/48)] < macd_4H_buy[int(search_counter_5M30M_SELL/48)]):
																		flag_cross_5M = 'failed_sell'

																	if (flag_cross_5M == 'sell'): 
																		#print('sell 1')
																		break


									#if ((symbol_data_5M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_5M[sym.name]['high'] - 1) - 30))):
									#	flag_cross_5M = 'low_toched'
									#	print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++low toched 5M30M++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_5M30M_SELL += 1
									#touch_counter -= 1
			except:
				#print('signal problem 5M SELL MACD!!!')
				logging.warning('signal problem 5M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			#****************--------------------++++++++++++++++++++++++*********** 5M 15M *****************************************************++++++++++++++++++++++
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_5M15M_SELL = int(MACD_signal_cross_5M_sell['index'])
								end_search_counter = int(window_counter_5M)

								#print('search_counter_5M15M_SELL = ',search_counter_5M15M_SELL)
								#print('end_search_counter = ',end_search_counter)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_5M15M_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M15M_SELL)] + symbol_data_5M[sym.name]['HLC/3'][(search_counter_5M15M_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['close'][(search_counter_5M15M_SELL)] + symbol_data_5M[sym.name]['close'][(search_counter_5M15M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):

												for l in line.values():

													protect_buy[i] = float(l)
													resist_sell[i] = float(l)

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M15M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_bid > protect_buy[i]):
														protect_buy_final_5M15M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M15M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_5M15M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													i += 1

									except:
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

									try:
										resist_sell_find_5M15M = max(resist_sell_final_5M15M.values())
										resist_sell_find_5M15M = max(resist_sell_find_5M15M,resist_sell_find_4H,resist_sell_find_1D)
									except:
										print('No Data')

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_5M[sym.name]['open'][(search_counter_5M15M_SELL)] + symbol_data_5M[sym.name]['open'][(search_counter_5M15M_SELL - 1)])/2)
											price_bid = ((symbol_data_5M[sym.name]['high'][(search_counter_5M15M_SELL)] + symbol_data_5M[sym.name]['high'][(search_counter_5M15M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):
												for l in line.values():

													resist_buy[i] = float(l)
													protect_sell[i] = float(l)

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M15M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_ask < resist_buy[i]):
														resist_buy_final_5M15M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M15M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_5M15M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1
						
													i += 1

									except:
					#print('some thing wrongt Res_Buy_Protection_Sell 4H')
										logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

									try:
										protect_sell_find_5M15M = min(protect_sell_final_5M15M.values())
										protect_sell_find_5M15M = min(protect_sell_find_5M15M,protect_sell_find_4H,protect_sell_find_1D)
									except:
										print('No Data')


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)
									if (((abs(symbol_data_5M[sym.name]['low'][search_counter_5M15M_SELL]-protect_sell_find_5M15M)/symbol_data_5M[sym.name]['low'][search_counter_5M15M_SELL]) * 100) < ((((protect_sell_find_5M15M-resist_sell_find_5M15M)/resist_sell_find_5M15M) * 100)*coef_5M)):
										if (protect_sell_find_5M15M < resist_sell_find_5M15M): continue
										#print('sell 4 5M15M: candle under cloud ')
										if ((macds_5M_sell[search_counter_5M15M_SELL] <= macd_5M_sell[search_counter_5M15M_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_5M[(search_counter_5M15M_SELL-26)] > symbol_data_5M[sym.name]['high'][(search_counter_5M15M_SELL)]):
												#print('sell 6 5M15M: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_15M_sell[(int(search_counter_5M15M_SELL/3))] <= macd_15M_sell[(int(search_counter_5M15M_SELL/3))]):
													#print('sell 7 5M15M: candle under TSKS ')
													if (chikospan_15M[((int(search_counter_5M15M_SELL/3))-26)] > symbol_data_15M[sym.name]['high'][((int(search_counter_5M15M_SELL/3)))]):
														#print('int(search_counter_5M15M_SELL/5) - 1 = ',int(search_counter_5M15M_SELL/3) - 1)
														if (tenkan_5M[search_counter_5M15M_SELL] >= kijun_5M[search_counter_5M15M_SELL]):

															if True:#(tenkan_15M[(int(search_counter_5M15M_SELL/3))] >= kijun_15M[(int(search_counter_5M15M_SELL/3))]):
																#print('sell 9 5M15: candle under TSKS ')
																if (symbol_data_5M[sym.name]['low'][search_counter_5M15M_SELL] >= tenkan_5M[search_counter_5M15M_SELL]):
																	#print('sell 10 5M15: candle under TSKS ')
																	if True:#(symbol_data_15M[sym.name]['low'][(int(search_counter_5M15M_SELL/3))] >= tenkan_15M[(int(search_counter_5M15M_SELL/3))]):
																		#print('sell 11 5M15: candle under TSKS ')
																		if ((symbol_data_5M[sym.name]['low'][search_counter_5M15M_SELL] >= SPANA_5M[search_counter_5M15M_SELL]) & (symbol_data_5M[sym.name]['low'][search_counter_5M15M_SELL] >= SPANB_5M[search_counter_5M15M_SELL])):
																			#price_bid = mt5.symbol_info_tick(sym.name).bid
																			if True:#((symbol_data_15M[sym.name]['low'][(int(search_counter_5M15M_SELL/3))] >= SPANA_15M[(int(search_counter_5M15M_SELL/3))]) & (symbol_data_15M[sym.name]['low'][(int(search_counter_5M15M_SELL/3))] >= SPANB_15M[(int(search_counter_5M15M_SELL/3))])):
																				#print('Pre Finish 5M15M SELL: ',sym.name)
																				#logging.debug('Pre Finish 5M15M SELL: %s'%sym.name)
																				if True:#((flag_cross_5M15M != 'low_toched') & ((((protect_sell_find-price_bid)/price_bid) * 100) < ((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))):
																					flag_cross_5M15M = 'sell'

																					signal_counter_5M15M_sell = search_counter_5M15M_SELL

																					#print('sell finished 5M15M: ',sym.name)
																					#logging.debug('sell finished 5M15M: %s'%sym.name)

																				else:
																					flag_cross_5M15M = 'failed_sell'
																			else:
																				flag_cross_5M15M = 'failed_sell'

																		#if (((MACD_signal_cross_5M_buy['signal'] == 'buy') | (MACD_signal_cross_5M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_5M_buy['index'] >= (int(search_counter_5M15M_SELL) - 6))):
																		#	flag_cross_5M15M = 'failed_sell'

																		#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= (int(search_counter_5M15M_SELL/3) - 6))):
																		#	flag_cross_5M15M = 'failed_sell'

																		#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_5M15M_SELL/288)+458 - 6))):
																		#	flag_cross_5M15M = 'failed_sell'

																		#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_5M15M_SELL/288)+458 - 6))):
																		#	flag_cross_5M15M = 'failed_sell'

																		if (macds_1D_buy[int(search_counter_5M15M_SELL/288)+458] <= macd_1D_buy[int(search_counter_5M15M_SELL/288)+458]):
																			flag_cross_5M15M = 'failed_sell'

																		if (macds_4H_buy[int(search_counter_5M15M_SELL/48)] < macd_4H_buy[int(search_counter_5M15M_SELL/48)]):
																			flag_cross_5M15M = 'failed_sell'

																		if (flag_cross_5M15M == 'sell'): 
																			#print('sell 1')
																			break

									#if ((symbol_data_5M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_5M[sym.name]['high'] - 1) - 15))):
									#	flag_cross_5M15M = 'low_toched'
									#	print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++low toched 5M15M++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_5M15M_SELL += 1
									#touch_counter -= 1
			except:
				#print('signal problem 5M15 SELL MACD!!!')
				logging.warning('signal problem 5M15 SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			#****************--------------------++++++++++++++++++++++++****** 15M **********************************************************++++++++++++++++++++++
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_15M1H_SELL = int(MACD_signal_cross_15M_sell['index'])
								end_search_counter = int(window_counter_15M)

								#print('search_counter_5M15M_SELL = ',search_counter_5M15M_SELL)
								#print('end_search_counter = ',end_search_counter)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_15M1H_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_15M[sym.name]['HLC/3'][(search_counter_15M1H_SELL)] + symbol_data_15M[sym.name]['HLC/3'][(search_counter_15M1H_SELL - 1)])/2)
											price_bid = ((symbol_data_15M[sym.name]['close'][(search_counter_15M1H_SELL)] + symbol_data_15M[sym.name]['close'][(search_counter_15M1H_SELL - 1)])/2)

											for line in csv.DictReader(myfile):

												for l in line.values():

													protect_buy[i] = float(l)
													resist_sell[i] = float(l)

													if (price_bid > protect_buy[i]):
														protect_buy_final_15M1H[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_bid > protect_buy[i]):
														protect_buy_final_15M1H[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_15M1H[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_15M1H[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													i += 1

									except:
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

									try:
										resist_sell_find_15M1H = max(resist_sell_final_15M1H.values())
										resist_sell_find_15M1H = max(resist_sell_find_15M1H,resist_sell_find_4H,resist_sell_find_1D)
									except:
										print('No Data')

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_15M[sym.name]['open'][(search_counter_15M1H_SELL)] + symbol_data_15M[sym.name]['open'][(search_counter_15M1H_SELL - 1)])/2)
											price_bid = ((symbol_data_15M[sym.name]['high'][(search_counter_15M1H_SELL)] + symbol_data_15M[sym.name]['high'][(search_counter_15M1H_SELL - 1)])/2)

											for line in csv.DictReader(myfile):
												for l in line.values():

													resist_buy[i] = float(l)
													protect_sell[i] = float(l)

													if (price_ask < resist_buy[i]):
														resist_buy_final_15M1H[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_ask < resist_buy[i]):
														resist_buy_final_15M1H[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_15M1H[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_15M1H[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1
						
													i += 1

									except:
					#print('some thing wrongt Res_Buy_Protection_Sell 4H')
										logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

									try:
										protect_sell_find_15M1H = min(protect_sell_final_15M1H.values())
										protect_sell_find_15M1H = min(protect_sell_find_15M1H,protect_sell_find_4H,protect_sell_find_1D)
									except:
										print('No Data')


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)
									if (((abs(symbol_data_15M[sym.name]['low'][search_counter_15M1H_SELL]-protect_sell_find_15M1H)/symbol_data_15M[sym.name]['low'][search_counter_15M1H_SELL]) * 100) < ((((protect_sell_find_15M1H-resist_sell_find_15M1H)/resist_sell_find_15M1H) * 100)*coef_15M)):
										if (protect_sell_find_15M1H < resist_sell_find_15M1H): continue
										#print('sell 4 5M15M: candle under cloud ')
										if ((macds_15M_sell[search_counter_15M1H_SELL] <= macd_15M_sell[search_counter_15M1H_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_15M[(search_counter_15M1H_SELL-26)] > symbol_data_15M[sym.name]['high'][(search_counter_15M1H_SELL)]):
												#print('sell 6 5M15M: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_1H_sell[(int(search_counter_15M1H_SELL/4))] <= macd_1H_sell[(int(search_counter_15M1H_SELL/4))]):
													#print('sell 7 5M15M: candle under TSKS ')
													if (chikospan_1H[((int(search_counter_15M1H_SELL/4))-26)] > symbol_data_1H[sym.name]['high'][((int(search_counter_15M1H_SELL/4)))]):
														#print('int(search_counter_5M15M_SELL/5) - 1 = ',int(search_counter_15M1H_SELL/3) - 1)
														if (tenkan_15M[search_counter_15M1H_SELL] >= kijun_15M[search_counter_15M1H_SELL]):
															#print('sell 9 15M: candle under TSKS ')
															if True:#(tenkan_1H[(int(search_counter_15M1H_SELL/4))] >= kijun_1H[(int(search_counter_15M1H_SELL/4))]):
																#print('sell 10 15M: candle under TSKS ')
																if (symbol_data_15M[sym.name]['low'][search_counter_15M1H_SELL] >= tenkan_15M[search_counter_15M1H_SELL]):
																	#print('sell 11 15M: candle under TSKS ')
																	if True:#(symbol_data_1H[sym.name]['low'][(int(search_counter_15M1H_SELL/4))] >= tenkan_1H[(int(search_counter_15M1H_SELL/4))]):
																		if ((symbol_data_15M[sym.name]['low'][search_counter_15M1H_SELL] >= SPANA_15M[search_counter_15M1H_SELL]) & (symbol_data_15M[sym.name]['low'][search_counter_15M1H_SELL] >= SPANB_15M[search_counter_15M1H_SELL])):
																			#price_bid = mt5.symbol_info_tick(sym.name).bid
																			if True:#((symbol_data_1H[sym.name]['low'][(int(search_counter_15M1H_SELL/4))] >= SPANA_1H[(int(search_counter_15M1H_SELL/4))]) & (symbol_data_1H[sym.name]['low'][(int(search_counter_15M1H_SELL/4))] >= SPANB_1H[(int(search_counter_15M1H_SELL/4))])):
																				#print('Pre Finish 15M1H SELL: ',sym.name)
																				#logging.debug('Pre Finish 15M1H SELL: %s'%sym.name)
																				if True:#((flag_cross_15M != 'low_toched') & ((((protect_sell_find-price_bid)/price_bid) * 100) < ((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))):
																					flag_cross_15M = 'sell'

																					signal_counter_15M_sell = search_counter_15M1H_SELL

																					#print('sell finished 5M: ',sym.name)
																					#logging.debug('sell finished 5M: %s'%sym.name)

																				else:
																					flag_cross_15M = 'failed_sell'
																			else:
																				flag_cross_15M = 'failed_sell'

																	#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= (int(search_counter_15M1H_SELL) - 6))):
																	#	flag_cross_15M = 'failed_sell'

																	#if (((MACD_signal_cross_1H_buy['signal'] == 'buy') | (MACD_signal_cross_1H_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1H_buy['index'] >= (int(search_counter_15M1H_SELL/4) - 6))):
																	#	flag_cross_15M = 'failed_sell'

																	#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_15M1H_SELL/96)+458 - 6))):
																	#	flag_cross_15M = 'failed_sell'

																	#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_15M1H_SELL/96)+458 - 6))):
																	#	flag_cross_15M = 'failed_sell'

																	if (macds_1D_buy[int(search_counter_15M1H_SELL/96)+458] <= macd_1D_buy[int(search_counter_15M1H_SELL/96)+458]):
																		flag_cross_15M = 'failed_sell'

																	if (macds_4H_buy[int(search_counter_15M1H_SELL/16)] < macd_4H_buy[int(search_counter_15M1H_SELL/16)]):
																		flag_cross_15M = 'failed_sell'

																	if (flag_cross_15M == 'sell'): 
																		#print('sell 1')
																		break


									#if ((symbol_data_15M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_15M[sym.name]['high'] - 1) - 30))):
									#	flag_cross_15M = 'low_toched'
									#	print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++low toched 15M1H++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_15M1H_SELL += 1
									#touch_counter -= 1
			except:
				#print('signal problem 15M SELL MACD!!!')
				logging.warning('signal problem 15M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


			#****************--------------------++++++++++++++++++++++++****** 15M 30M **********************************************************++++++++++++++++++++++
			try:
				if True:#((macds_1M_sell[window_counter_1M] < macd_1M_sell[window_counter_1M]) & (macd_1M_sell[window_counter_1M] >= 0) & (macds_1M_sell[window_counter_1M] >= 0)):
					#print('buy 0 1M: MACD 1M Sig: ',sym.name)
					if True:#(macds_5M_sell[(int(window_counter_1M/5))] > macd_5M_sell[(int(window_counter_1M/5))]):
						#print('buy 1 1M: MACD 15 Sig ')
						if True:#(((abs(symbol_data_1M[sym.name]['low'][window_counter_1M]-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 100)/5)):
							#print('buy 2 1M: MACD 5 under plus ')
							if True:#(tenkan_1M[window_counter_1M] > kijun_1M[window_counter_1M]):
								#print('buy 3 1M: TSKS 1M Cross ')
								search_counter_15M30M_SELL = int(MACD_signal_cross_15M_sell['index'])
								end_search_counter = int(window_counter_15M)

								#print('search_counter_5M15M_SELL = ',search_counter_5M15M_SELL)
								#print('end_search_counter = ',end_search_counter)
								#touch_counter = len(symbol_data_1M[sym.name]['high'] - 1)
								while (search_counter_15M30M_SELL <= end_search_counter):

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0


									try:
										with open("Res_Sell_Protection_Buy/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_15M[sym.name]['HLC/3'][(search_counter_15M30M_SELL)] + symbol_data_15M[sym.name]['HLC/3'][(search_counter_15M30M_SELL - 1)])/2)
											price_bid = ((symbol_data_15M[sym.name]['close'][(search_counter_15M30M_SELL)] + symbol_data_15M[sym.name]['close'][(search_counter_15M30M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):

												for l in line.values():

													protect_buy[i] = float(l)
													resist_sell[i] = float(l)

													if (price_bid > protect_buy[i]):
														protect_buy_final_15M30M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_bid > protect_buy[i]):
														protect_buy_final_15M30M[j] = protect_buy[i]
									#protect_buy_final[j] = protect_buy[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_15M30M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													if (price_ask > resist_sell[i]):
														resist_sell_final_15M30M[j] = resist_sell[i]
									#resist_sell_final[j] = resist_sell[i]
														j += 1

													i += 1

									except:
										logging.warning('some thing wrongt Res_Sell_Protection_Buy 5M')

									try:
										resist_sell_find_15M30M = max(resist_sell_final_15M30M.values())
										resist_sell_find_15M30M = max(resist_sell_find_15M30M,resist_sell_find_4H,resist_sell_find_1D)
									except:
										print('No Data')

									protect_buy = {}
									resist_sell = {}

									i = 0
									j = 0

									try:
										with open("Res_Buy_Protection_Sell/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
											price_ask = ((symbol_data_15M[sym.name]['open'][(search_counter_15M30M_SELL)] + symbol_data_15M[sym.name]['open'][(search_counter_15M30M_SELL - 1)])/2)
											price_bid = ((symbol_data_15M[sym.name]['high'][(search_counter_15M30M_SELL)] + symbol_data_15M[sym.name]['high'][(search_counter_15M30M_SELL - 1)])/2)

											for line in csv.DictReader(myfile):
												for l in line.values():

													resist_buy[i] = float(l)
													protect_sell[i] = float(l)

													if (price_ask < resist_buy[i]):
														resist_buy_final_15M30M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_ask < resist_buy[i]):
														resist_buy_final_15M30M[j] = resist_buy[i]
									#resist_buy_final[j] = resist_buy[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_15M30M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1

													if (price_bid < protect_sell[i]):
														protect_sell_final_15M30M[j] = protect_sell[i]
									#protect_sell_final[j] = protect_sell[i]

														j += 1
						
													i += 1

									except:
					#print('some thing wrongt Res_Buy_Protection_Sell 4H')
										logging.warning('some thing wrongt Res_Buy_Protection_Sell 5M')

									try:
										protect_sell_find_15M30M = min(protect_sell_final_15M30M.values())
										protect_sell_find_15M30M = min(protect_sell_find_15M30M,protect_sell_find_4H,protect_sell_find_1D)
									except:
										print('No Data')


									#if ((macds_1M_sell[search_counter_1M_SELL] > macd_1M_sell[search_counter_1M_SELL])):
									#	break

									#price_ask = mt5.symbol_info_tick(sym.name).ask
									#if (((((price_ask-protect_buy_find)/protect_buy_find) * 100) < ((((resist_buy_find-protect_buy_find)/protect_buy_find) * 200)/3)) & (touch_counter > (len(symbol_data_1M[sym.name]['high'] - 1) - 10)) & (flag_cross_1M == 'high_toched')):
										#flag_cross_1M = 'not_toched'
									#print('search_counter 1M = ',search_counter,flag_cross_1M)
									if (((abs(symbol_data_15M[sym.name]['low'][search_counter_15M30M_SELL]-protect_sell_find_15M30M)/symbol_data_15M[sym.name]['low'][search_counter_15M30M_SELL]) * 100) < ((((protect_sell_find_15M30M-resist_sell_find_15M30M)/resist_sell_find_15M30M) * 100)*coef_15M)):
										if (protect_sell_find_15M30M < resist_sell_find_15M30M): continue
										#print('sell 4 5M15M: candle under cloud ')
										if ((macds_15M_sell[search_counter_15M30M_SELL] <= macd_15M_sell[search_counter_15M30M_SELL])):
											#print('sell 5 1M: candle above chiko ')
											if (chikospan_15M[(search_counter_15M30M_SELL-26)] > symbol_data_15M[sym.name]['high'][(search_counter_15M30M_SELL)]):
												#print('sell 6 5M15M: chiko above candle -26 ')
												#print('search_counter_1M_SELL = ',search_counter_1M_SELL)
												if (macds_30M_sell[(int(search_counter_15M30M_SELL/2))] <= macd_30M_sell[(int(search_counter_15M30M_SELL/2))]):
													#print('sell 7 5M15M: candle under TSKS ')
													if (chikospan_30M[((int(search_counter_15M30M_SELL/2))-26)] > symbol_data_30M[sym.name]['high'][((int(search_counter_15M30M_SELL/2)))]):
														#print('int(search_counter_5M15M_SELL/5) - 1 = ',int(search_counter_15M30M_SELL/3) - 1)
														if (tenkan_15M[search_counter_15M30M_SELL] >= kijun_15M[search_counter_15M30M_SELL]):

															if True:#(tenkan_30M[(int(search_counter_15M30M_SELL/2))] >= kijun_30M[(int(search_counter_15M30M_SELL/2))]):
																#print('sell 8 15M30M: candle 1D under Cloude ')
																if (symbol_data_15M[sym.name]['low'][search_counter_15M30M_SELL] >= tenkan_15M[search_counter_15M30M_SELL]):
																	#print('sell 9 15M30M: candle 1D Chicko ')
																	if True:#(symbol_data_30M[sym.name]['low'][(int(search_counter_15M30M_SELL/2))] >= tenkan_30M[(int(search_counter_15M30M_SELL/2))]):
																		#print('sell 10 15M30M: candle 1D under TSKS ')
																		if ((symbol_data_15M[sym.name]['low'][search_counter_15M30M_SELL] >= SPANA_15M[search_counter_15M30M_SELL]) & (symbol_data_15M[sym.name]['low'][search_counter_15M30M_SELL] >= SPANB_15M[search_counter_15M30M_SELL])):
																			#price_bid = mt5.symbol_info_tick(sym.name).bid
																			if True:#((symbol_data_30M[sym.name]['low'][(int(search_counter_15M30M_SELL/2))] >= SPANA_30M[(int(search_counter_15M30M_SELL/2))]) & (symbol_data_30M[sym.name]['low'][(int(search_counter_15M30M_SELL/2))] >= SPANB_30M[(int(search_counter_15M30M_SELL/2))])):
																				#print('sell 11 15M30M: candle 1D Chicko ')
																				#print('Pre Finish 15M30M SELL: ',sym.name)
																				#logging.debug('Pre Finish 15M30M SELL: %s'%sym.name)
																				if True:#((flag_cross_15M30M != 'low_toched') & ((((protect_sell_find-price_bid)/price_bid) * 100) < ((((protect_sell_find-resist_sell_find)/protect_sell_find) * 200)/3))):
																					flag_cross_15M30M = 'sell'

																					signal_counter_15M30M_sell = search_counter_15M30M_SELL

																					#print('sell finished 15M30M: ',sym.name)
																					#logging.debug('sell finished 15M30M: %s'%sym.name)

																				else:
																					flag_cross_15M30M = 'failed_sell'
																			else:
																				flag_cross_15M30M = 'failed_sell'

																		#if (((MACD_signal_cross_15M_buy['signal'] == 'buy') | (MACD_signal_cross_15M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_15M_buy['index'] >= (int(search_counter_15M30M_SELL) - 6))):
																		#	flag_cross_15M30M = 'failed_sell'

																		#if (((MACD_signal_cross_30M_buy['signal'] == 'buy') | (MACD_signal_cross_30M_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_30M_buy['index'] >= (int(search_counter_15M30M_SELL/2) - 6))):
																		#	flag_cross_15M30M = 'failed_sell'

																		#if (((MACD_signal_cross_1D_buy['signal'] == 'buy') | (MACD_signal_cross_1D_buy['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_buy['index'] >= (int(search_counter_15M30M_SELL/96)+458 - 6))):
																		#	flag_cross_15M30M = 'failed_sell'

																		#if (((MACD_signal_cross_1D_sell['signal'] == 'buy') | (MACD_signal_cross_1D_sell['signal'] == 'faild_buy')) & (MACD_signal_cross_1D_sell['index'] >= (int(search_counter_15M30M_SELL/96)+458 - 6))):
																		#	flag_cross_15M30M = 'failed_sell'

																		if (macds_1D_buy[int(search_counter_15M30M_SELL/96)+458] <= macd_1D_buy[int(search_counter_15M30M_SELL/96)+458]):
																			flag_cross_15M30M = 'failed_sell'

																		if (macds_4H_buy[int(search_counter_15M30M_SELL/16)] < macd_4H_buy[int(search_counter_15M30M_SELL/16)]):
																			flag_cross_15M30M = 'failed_sell'

																		if (flag_cross_15M30M == 'sell'): 
																			#print('sell 1')
																			break



									#if ((symbol_data_15M[sym.name]['low'][touch_counter] <= resist_buy_find) & (touch_counter <= (len(symbol_data_15M[sym.name]['high'] - 1) - 30))):
									#	print('low toched 15M30M')
									#	flag_cross_15M30M = 'low_toched'


								
														#if (SPANA_30M[(len(symbol_data_30M[sym.name]['high']) - 1)] <= SPANB_30M[(len(symbol_data_30M[sym.name]['high']) - 1)]):
														#	data_macd_5M_sell['tp'] = (data_macd_5M_sell['tp'] * 2)

									search_counter_15M30M_SELL += 1
									#touch_counter -= 1
			except:
				#print('signal problem 15M30M SELL MACD!!!')
				logging.warning('signal problem 15M30M SELL MACD!!!')

			#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			#print('sell')
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

			#logging.debug('////////////////////////////////////////////')
			#logging.debug('')
			##logging.debug('')
			#logging.debug('******* Signals ***********')


			#print('flag_cross_1M = ',flag_cross_1M)
			#print('flag_cross_5M = ',flag_cross_5M)
			#print('flag_cross_15M = ',flag_cross_15M)
			#print('flag_cross_5M15M = ',flag_cross_5M15M)
			#print('flag_cross_15M30M = ',flag_cross_15M30M)
			#print('flag_cross_5M1H = ',flag_cross_5M1H)

			#logging.debug('flag_cross_1M = %s'%flag_cross_1M)
			#logging.debug('flag_cross_5M = %s'%flag_cross_5M)
			#logging.debug('flag_cross_15M = %s'%flag_cross_15M)
			#logging.debug('flag_cross_5M15M = %s'%flag_cross_5M15M)
			#logging.debug('flag_cross_15M30M = %s'%flag_cross_15M30M)
			#logging.debug('flag_cross_5M1H = %s'%flag_cross_5M1H)


			#print('')
			#print('////////////////////////////////////////////')
			#print('')
			#print('****** SELL OR BUY Doing ***********')
			#print('')

			#logging.debug('')
			#logging.debug('////////////////////////////////////////////')
			#logging.debug('')
			#logging.debug('****** SELL OR BUY Doing ***********')
			#logging.debug('')

			percentage_buy_tp_save_1M = {}
			percentage_buy_st_save_1M = {}

			percentage_buy_tp_save_5M1H = {}
			percentage_buy_st_save_5M1H = {}

			percentage_buy_tp_save_5M30M = {}
			percentage_buy_st_save_5M30M = {}

			percentage_buy_tp_save_5M15M = {}
			percentage_buy_st_save_5M15M = {}

			percentage_buy_tp_save_15M1H = {}
			percentage_buy_st_save_15M1H = {}

			percentage_buy_tp_save_15M30M = {}
			percentage_buy_st_save_15M30M = {}


			percentage_sell_tp_save_1M = {}
			percentage_sell_st_save_1M = {}

			percentage_sell_tp_save_5M1H = {}
			percentage_sell_st_save_5M1H = {}

			percentage_sell_tp_save_5M30M = {}
			percentage_sell_st_save_5M30M = {}

			percentage_sell_tp_save_5M15M = {}
			percentage_sell_st_save_5M15M = {}

			percentage_sell_tp_save_15M1H = {}
			percentage_sell_st_save_15M1H = {}

			percentage_sell_tp_save_15M30M = {}
			percentage_sell_st_save_15M30M = {}

			
			#***************************************************** 1M SELL ******************************************************************
			if (flag_cross_1M == 'sell'):

				#************************************************ 1M Top Low Touched ************************************************************
			

				window_counter_1D = int(signal_counter_1M_sell/1440) + 458 + 1
				window_counter_4H = int(signal_counter_1M_sell/240) + 1
				window_counter_1H = int(signal_counter_1M_sell/60) + 1
				window_counter_30M = int(signal_counter_1M_sell/30) + 1
				window_counter_15M = int(signal_counter_1M_sell/15) + 1
				window_counter_5M = int(signal_counter_1M_sell/5) + 1

				#print('')
				#print('')
				#logging.debug('')



				try:
					touch_counter = signal_counter_1M_sell

					while touch_counter > (signal_counter_1M_sell - 300):
						if ((symbol_data_1M[sym.name]['low'][touch_counter] <= (resist_sell_find_1M * 1.0002))):
							flag_lowtouch_1M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						#if ((symbol_data_1M[sym.name]['high'][(signal_counter_1M_sell - 2)] >= (protect_sell_find_1M * 1.0002))
						#	| (symbol_data_1M[sym.name]['high'][(signal_counter_1M_sell - 1)] >= (protect_sell_find_1M * 1.0002))
						#	| (symbol_data_1M[sym.name]['high'][(signal_counter_1M_sell)] >= (protect_sell_find_1M * 1.0002))):
						#	flag_lowtouch_1M = ''
						#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
						#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				try:
					touch_counter = window_counter_5M-1

					while touch_counter > (window_counter_5M - 20):
						if ((symbol_data_5M[sym.name]['low'][touch_counter] <= (resist_sell_find * 1.0002))):
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_5M[sym.name]['high'][(window_counter_5M-1 - 2)] >= (protect_sell_find * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(window_counter_5M-1 - 1)] >= (protect_sell_find * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(window_counter_5M-1)] >= (protect_sell_find * 1.0002))):
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				#print('')
				#print('')
				#logging.debug('')

				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')

				#************************************************ 4H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_1M = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_1M = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_1M = 'failed_sell'

				if (flag_lowtouch_1M == 'low_toched'):
					flag_cross_1M = 'failed_sell'

				#print('////////////// flag_cross_1M = ',flag_cross_1M)

				if (flag_cross_1M == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_1M_sell['tp'] = max(resist_sell_find_1M,(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]*0.999))
					else:
						data_macd_1M_sell['tp'] = resist_sell_find_1M * 1.0004
					print('data_macd_1M_sell = ',data_macd_1M_sell['tp'])


					if (SPANA_1D[int(signal_counter_1M_sell/1440)+458] > SPANB_1D[int(signal_counter_1M_sell/1440)+458]):
						data_macd_1M_sell['st'] = protect_sell_find_1M

					if (SPANA_1D[int(signal_counter_1M_sell/1440)+458] <= SPANB_1D[int(signal_counter_1M_sell/1440)+458]):
						data_macd_1M_sell['st'] = protect_sell_find_1M

					if data_macd_1M_sell['tp'] < symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]: 
						#print('************ Trade **********************')
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
						#continue


						counter_i = signal_counter_1M_sell

						final_index = (signal_counter_1M_sell + 600)

						flag_index = 1

						if (final_index ) >= len(symbol_data_1M[sym.name]['close'])-1:
							final_index = len(symbol_data_1M[sym.name]['close'])-1
							flag_index =  0


						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['low'][signal_counter_1M_sell])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_1M[sym.name]['low'][signal_counter_1M_sell] - symbol_data_1M[sym.name]['high'][counter_i])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]) * 100

						#print(percentage_buy_tp[counter_j])
						##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100)):
									#print('fine')
									break

							counter_i += 1
							counter_j += 1

						

						#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_1M = min(percentage_sell_tp.values())
							percentage_sell_st_save_1M = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_1M = 0
							percentage_sell_st_save_1M = 0

						logging.debug('************************ OUT 1M sell *******************************')

						if (abs(percentage_sell_tp_save_1M) >= (((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100)):
							logging.debug('sell_1M = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-data_macd_1M_sell['st'])/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_1D)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_4H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_1H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_30M)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find_1D)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find_4H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))

							logging.debug('signal_counter_1M_sell = %f'%(signal_counter_1M_sell - MACD_signal_cross_1M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_1M_sell[] = %f'%signal_counter_1M_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_1M = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-data_macd_1M_sell['tp'])/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))

								logging.debug('st = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-data_macd_1M_sell['st'])/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_1D)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_4H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_1H)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]-resist_sell_find_30M)/symbol_data_1M[sym.name]['low'][signal_counter_1M_sell]))*100))

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find_1D)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]-protect_sell_find_4H)/symbol_data_1M[sym.name]['high'][signal_counter_1M_sell]))*100))

								logging.debug('signal_counter_1M_sell = %f'%(signal_counter_1M_sell - MACD_signal_cross_1M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_1M_sell[] = %f'%signal_counter_1M_sell)

								FAILED += 1

					#logging.debug('num_1M = %d'%counter_sell_1M)
						logging.debug('percentage_sell_tp_save_1M = %f'%percentage_sell_tp_save_1M)
						logging.debug('percentage_sell_st_save_1M = %f'%percentage_sell_st_save_1M)

					#counter_sell_1M += 1


			#***************************************************** 5M1H SELL ******************************************************************

			if (flag_cross_5M1H == 'sell'):

				#************************************************ 1M Top Low Touched ************************************************************
			

				window_counter_1D = int(signal_counter_5M1H_sell/288) + 458 + 1
				window_counter_4H = int(signal_counter_5M1H_sell/48) + 1
				window_counter_1H = int(signal_counter_5M1H_sell/12) + 1
				window_counter_30M = int(signal_counter_5M1H_sell/6) + 1
				window_counter_15M = int(signal_counter_5M1H_sell/3) + 1
				
			#************************************************ 5M Top Low Touched ************************************************************

				try:
					touch_counter = signal_counter_5M1H_sell

					while touch_counter > (signal_counter_5M1H_sell - 60):
						if ((symbol_data_5M[sym.name]['high'][touch_counter] >= (resist_buy_find_5M1H * 0.9998))):
							flag_hightouch_5M = 'high_toched'
							flag_hightouch_5M = 'high_toched'
							flag_hightouch_5M = 'high_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& top touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_5M[sym.name]['low'][(signal_counter_5M1H_sell - 2)] <= (protect_sell_find_5M1H * 0.9998))
							| (symbol_data_5M[sym.name]['low'][(signal_counter_5M1H_sell - 1)] <= (protect_sell_find_5M1H * 0.9998))
							| (symbol_data_5M[sym.name]['low'][(signal_counter_5M1H_sell)] <= (protect_sell_find_5M1H * 0.9998))):
							flag_hightouch_5M = ''
							flag_hightouch_5M = ''
							flag_hightouch_5M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				#print('')
				#print('')
				#logging.debug('')

				try:
					touch_counter = signal_counter_5M1H_sell

					while touch_counter > (signal_counter_5M1H_sell - 20):
						if ((symbol_data_5M[sym.name]['low'][touch_counter] <= (resist_sell_find * 1.0002))):
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_5M[sym.name]['high'][(signal_counter_5M1H_sell - 2)] >= (protect_sell_find * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M1H_sell - 1)] >= (protect_sell_find * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M1H_sell)] >= (protect_sell_find * 1.0002))):
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')

				#************************************************ 4H Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_5M1H = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_5M1H = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_5M1H = 'failed_sell'

				if (flag_lowtouch_5M == 'low_toched'):
					flag_cross_5M1H = 'failed_sell'

				if (flag_cross_5M1H == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_5M_sell['tp'] = max(resist_sell_find_5M1H,(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]*0.998))
					else:
						data_macd_5M_sell['tp'] = resist_sell_find_5M1H * 1.0004



					if (SPANA_1D[int(signal_counter_5M1H_sell/288)+458] > SPANB_1D[int(signal_counter_5M1H_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M1H

					if (SPANA_1D[int(signal_counter_5M1H_sell/288)+458] <= SPANB_1D[int(signal_counter_5M1H_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M1H

					if data_macd_5M_sell['tp'] < symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]: 
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
						#continue

						counter_i = signal_counter_5M1H_sell
						final_index = (signal_counter_5M1H_sell + 400)

						flag_index = 1

						if (final_index ) >= len(symbol_data_5M[sym.name]['close'])-1:
							final_index = len(symbol_data_5M[sym.name]['close'])-1
							flag_index = 0


						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]) * 100

						#print(percentage_buy_tp[counter_j])
						##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100)):
									break

							counter_i += 1
							counter_j += 1

						

						#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_5M1H = min(percentage_sell_tp.values())
							percentage_sell_st_save_5M1H = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_5M1H = 0
							percentage_sell_st_save_5M1H = 0

						logging.debug('************************ OUT_5M1H sell *******************************')

						if (abs(percentage_sell_tp_save_5M1H) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100)):
							logging.debug('sell_5M1H = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))

							logging.debug('signal_counter_5M1H_sell = %f'%(signal_counter_5M1H_sell - MACD_signal_cross_5M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_5M1H_sell[] = %f'%signal_counter_5M1H_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_5M1H = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
								logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M1H_sell]))*100))

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M1H_sell]))*100))

								logging.debug('signal_counter_5M1H_sell = %f'%(signal_counter_5M1H_sell - MACD_signal_cross_5M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_5M1H_sell[] = %f'%signal_counter_5M1H_sell)

								FAILED += 1

						#logging.debug('num_5M1H = %d'%counter_sell_5M1H)
						logging.debug('percentage_sell_tp_save_5M1H = %f'%percentage_sell_tp_save_5M1H)
						logging.debug('percentage_sell_st_save_5M1H = %f'%percentage_sell_st_save_5M1H)

					#counter_sell_5M1H += 1

				#************************************** 5M30M SELL ******************************************************************

			if (flag_cross_5M == 'sell'):

				#************************************************ 1M Top Low Touched ************************************************************
			

				window_counter_1D = int(signal_counter_5M_sell/288) + 458 + 1
				window_counter_4H = int(signal_counter_5M_sell/48) + 1
				window_counter_1H = int(signal_counter_5M_sell/12) + 1
				window_counter_30M = int(signal_counter_5M_sell/6) + 1
				window_counter_15M = int(signal_counter_5M_sell/3) + 1
				
			#************************************************ 5M Top Low Touched ************************************************************

				try:
					touch_counter = signal_counter_5M_sell

					while touch_counter > (signal_counter_5M_sell - 60):
						if ((symbol_data_5M[sym.name]['low'][touch_counter] <= (resist_sell_find_5M30M * 1.0002))):
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_5M[sym.name]['high'][(signal_counter_5M_sell - 2)] >= (protect_sell_find_5M30M * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M_sell - 1)] >= (protect_sell_find_5M30M * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M_sell)] >= (protect_sell_find_5M30M * 1.0002))):
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')

				#************************************************ 4H Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_5M = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_5M = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_5M = 'failed_sell'

				if (flag_lowtouch_5M == 'low_toched'):
					flag_cross_5M = 'failed_sell'

				if (flag_cross_5M == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_5M_sell['tp'] = max(resist_sell_find_5M30M,(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]*0.998))
					else:
						data_macd_5M_sell['tp'] = resist_sell_find_5M30M * 1.0004


					if (SPANA_1D[int(signal_counter_5M_sell/288)+458] > SPANB_1D[int(signal_counter_5M_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M30M

					if (SPANA_1D[int(signal_counter_5M_sell/288)+458] <= SPANB_1D[int(signal_counter_5M_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M30M

					if data_macd_5M_sell['tp'] < symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]: 
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
							#continue

						counter_i = signal_counter_5M_sell
						final_index = (signal_counter_5M_sell + 400)

						flag_index = 1

						if (final_index ) >= len(symbol_data_5M[sym.name]['close'])-1:
							final_index = len(symbol_data_5M[sym.name]['close'])-1
							flag_index = 0


						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_counter_5M_sell])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_counter_5M_sell] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]) * 100

							#print(percentage_buy_tp[counter_j])
							##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100)):
									break

							counter_i += 1
							counter_j += 1

							

							#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_5M30M = min(percentage_sell_tp.values())
							percentage_sell_st_save_5M30M = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_5M30M = 0
							percentage_sell_st_save_5M30M = 0

						logging.debug('************************ OUT_5M30M sell *******************************')

						if (abs(percentage_sell_tp_save_5M30M) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100)):
							logging.debug('sell_5M30M = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))

							logging.debug('signal_counter_5M_sell = %f'%(signal_counter_5M_sell - MACD_signal_cross_5M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_5M_sell[] = %f'%signal_counter_5M_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_5M30M = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
								logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M_sell]))*100))

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M_sell]))*100))

								logging.debug('signal_counter_5M_sell = %f'%(signal_counter_5M_sell - MACD_signal_cross_5M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_5M_sell[] = %f'%signal_counter_5M_sell)

								FAILED += 1


						#logging.debug('num_5M30M = %d'%counter_sell_5M30M)
						logging.debug('percentage_sell_tp_save_5M30M = %f'%percentage_sell_tp_save_5M30M)
						logging.debug('percentage_sell_st_save_5M30M = %f'%percentage_sell_st_save_5M30M)

					#counter_sell_5M30M += 1
			#**************************************** 5M15M SELL ******************************************************************


			if (flag_cross_5M15M == 'sell'):

				#************************************************ 1M Top Low Touched ************************************************************
			

				window_counter_1D = int(signal_counter_5M15M_sell/288) + 458 + 1
				window_counter_4H = int(signal_counter_5M15M_sell/48) + 1
				window_counter_1H = int(signal_counter_5M15M_sell/12) + 1
				window_counter_30M = int(signal_counter_5M15M_sell/6) + 1
				window_counter_15M = int(signal_counter_5M15M_sell/3) + 1
				
			#************************************************ 5M Top Low Touched ************************************************************

				try:
					touch_counter = signal_counter_5M15M_sell

					while touch_counter > (signal_counter_5M15M_sell - 60):
						if ((symbol_data_5M[sym.name]['low'][touch_counter] <= (resist_sell_find_5M15M * 1.0002))):
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							flag_lowtouch_5M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_5M[sym.name]['high'][(signal_counter_5M15M_sell - 2)] >= (protect_sell_find_5M15M * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M15M_sell - 1)] >= (protect_sell_find_5M15M * 1.0002))
							| (symbol_data_5M[sym.name]['high'][(signal_counter_5M15M_sell)] >= (protect_sell_find_5M15M * 1.0002))):
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							flag_lowtouch_5M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 5M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')

				#print('')
				#print('')
				#logging.debug('')

			#************************************************ 15M Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_15M-1

					while touch_counter > (window_counter_15M - 10):
						if ((symbol_data_15M[sym.name]['low'][touch_counter] <= (resist_sell_find * 1.0002))):
							flag_lowtouch_15M = 'low_toched'
							flag_lowtouch_15M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_15M[sym.name]['high'][(window_counter_15M-1 - 2)] >= (protect_sell_find * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(window_counter_15M-1 - 1)] >= (protect_sell_find * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(window_counter_15M-1)] >= (protect_sell_find * 1.0002))):
							flag_lowtouch_15M = ''
							flag_lowtouch_15M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')



				#logging.debug('')
				#************************************************ 4H Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_5M15M = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_5M15M = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_5M15M = 'failed_sell'

				if (flag_lowtouch_5M == 'low_toched'):
					flag_cross_5M15M = 'failed_sell'

				#print('************* flag_cross_5M15M = ',flag_cross_5M15M,'*****************')

				if (flag_cross_5M15M == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_5M_sell['tp'] = max(resist_sell_find_5M15M,(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]*0.998))
					else:
						data_macd_5M_sell['tp'] = resist_sell_find_5M15M * 1.0004


					if (SPANA_1D[int(signal_counter_5M15M_sell/288)+458] > SPANB_1D[int(signal_counter_5M15M_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M15M

					if (SPANA_1D[int(signal_counter_5M15M_sell/288)+458] <= SPANB_1D[int(signal_counter_5M15M_sell/288)+458]):
						data_macd_5M_sell['st'] = protect_sell_find_5M15M

					if data_macd_5M_sell['tp'] < symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]: 
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
						#continue

						counter_i = signal_counter_5M15M_sell
						final_index = (signal_counter_5M15M_sell + 400)

						flag_index = 1

						if (final_index ) >= len(symbol_data_5M[sym.name]['close'])-1:
							final_index = len(symbol_data_5M[sym.name]['close'])-1
							flag_index = 0


						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]) * 100

							#print(percentage_buy_tp[counter_j])
							##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100)):
									break

							counter_i += 1
							counter_j += 1

							

						#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_5M15M = min(percentage_sell_tp.values())
							percentage_sell_st_save_5M15M = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_5M15M = 0
							percentage_sell_st_save_5M15M = 0

						logging.debug('************************ OUT_5M15M sell *******************************')

						if (abs(percentage_sell_tp_save_5M15M) >= (((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100)):
							logging.debug('sell_5M15M = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
							logging.debug('signal_counter_5M15M_sell = %f'%signal_counter_5M15M_sell)

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))

							logging.debug('signal_counter_5M15M_sell = %f'%(signal_counter_5M15M_sell - MACD_signal_cross_5M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_5M15M_sell[] = %f'%signal_counter_5M15M_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_5M15M = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-data_macd_5M_sell['tp'])/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
								logging.debug('st = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-data_macd_5M_sell['st'])/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_1D)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_4H)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_1H)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]-resist_sell_find_30M)/symbol_data_5M[sym.name]['low'][signal_counter_5M15M_sell]))*100))
								logging.debug('signal_counter_5M15M_sell = %f'%signal_counter_5M15M_sell)

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find_1D)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]-protect_sell_find_4H)/symbol_data_5M[sym.name]['high'][signal_counter_5M15M_sell]))*100))

								logging.debug('signal_counter_5M15M_sell = %f'%(signal_counter_5M15M_sell - MACD_signal_cross_5M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_5M15M_sell[] = %f'%signal_counter_5M15M_sell)

								FAILED += 1

						#logging.debug('num_5M15M = %d'%counter_sell_5M15M)
						logging.debug('percentage_sell_tp_save_5M15M = %f'%percentage_sell_tp_save_5M15M)
						logging.debug('percentage_sell_st_save_5M15M = %f'%percentage_sell_st_save_5M15M)

					#counter_sell_5M15M += 1

			#******************************************** 15M1H SELL ******************************************************************

			if (flag_cross_15M == 'sell'):
			

				window_counter_1D = int(signal_counter_15M_sell/96) + 458 + 1
				window_counter_4H = int(signal_counter_15M_sell/16) + 1
				window_counter_1H = int(signal_counter_15M_sell/4) + 1
				window_counter_30M = int(signal_counter_15M_sell/2) + 1
				

			#************************************************ 15M Top Low Touched ************************************************************
				try:
					touch_counter = signal_counter_15M_sell

					while touch_counter > (signal_counter_15M_sell - 40):
						if ((symbol_data_15M[sym.name]['low'][touch_counter] <= (resist_sell_find_15M1H * 1.0002))):
							flag_lowtouch_15M = 'low_toched'
							flag_lowtouch_15M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_15M[sym.name]['high'][(signal_counter_15M_sell - 2)] >= (protect_sell_find_15M1H * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(signal_counter_15M_sell - 1)] >= (protect_sell_find_15M1H * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(signal_counter_15M_sell)] >= (protect_sell_find_15M1H * 1.0002))):
							flag_lowtouch_15M = ''
							flag_lowtouch_15M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')



				#logging.debug('')

				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')

				#************************************************ 4H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_15M = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_15M = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_15M = 'failed_sell'

				if (flag_lowtouch_5M == 'low_toched'):
					flag_cross_15M = 'failed_sell'

				if (flag_cross_15M == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_15M_sell['tp'] = max(resist_sell_find_15M1H,(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]*0.998))
					else:
						data_macd_15M_sell['tp'] = resist_sell_find_15M1H * 1.0004

					
					if (SPANA_1D[int(signal_counter_15M_sell/96)+458] > SPANB_1D[int(signal_counter_15M_sell/96)+458]):
						data_macd_15M_sell['st'] = protect_sell_find_15M1H

					if (SPANA_1D[int(signal_counter_15M_sell/96)+458] <= SPANB_1D[int(signal_counter_15M_sell/96)+458]):
						data_macd_15M_sell['st'] = protect_sell_find_15M1H

					if data_macd_15M_sell['tp'] < symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]: 
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
						#continue

						counter_i = signal_counter_15M_sell
						final_index = (signal_counter_15M_sell + 300)

						flag_index = 1

						if (final_index ) >= len(symbol_data_15M[sym.name]['close'])-1:
							final_index = len(symbol_data_15M[sym.name]['close'])-1
							flag_index = 0


						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_15M[sym.name]['close'][counter_i] - symbol_data_15M[sym.name]['low'][signal_counter_15M_sell])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_15M[sym.name]['low'][signal_counter_15M_sell] - symbol_data_15M[sym.name]['high'][counter_i])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]) * 100

							#print(percentage_buy_tp[counter_j])
							##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break

							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100)):
									break

							counter_i += 1
							counter_j += 1

							

							#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_15M1H = min(percentage_sell_tp.values())
							percentage_sell_st_save_15M1H = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_15M1H = 0
							percentage_sell_st_save_15M1H = 0

						logging.debug('************************ OUT_15M1H sell *******************************')

						if (abs(percentage_sell_tp_save_15M1H) >= (((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100)):
							logging.debug('sell_15M1H = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-data_macd_15M_sell['st'])/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_1D)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_4H)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_1H)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_30M)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
							logging.debug('signal_counter_15M_sell = %f'%signal_counter_15M_sell)

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find_1D)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find_4H)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))

							logging.debug('signal_counter_15M_sell = %f'%(signal_counter_15M_sell - MACD_signal_cross_15M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_15M_sell[] = %f'%signal_counter_15M_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_15M1H = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
								logging.debug('st = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-data_macd_15M_sell['st'])/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_1D)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_4H)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_1H)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]-resist_sell_find_30M)/symbol_data_15M[sym.name]['low'][signal_counter_15M_sell]))*100))
								logging.debug('signal_counter_15M_sell = %f'%signal_counter_15M_sell)

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find_1D)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]-protect_sell_find_4H)/symbol_data_15M[sym.name]['high'][signal_counter_15M_sell]))*100))

								logging.debug('signal_counter_15M_sell = %f'%(signal_counter_15M_sell - MACD_signal_cross_15M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_15M_sell[] = %f'%signal_counter_15M_sell)

								FAILED += 1


						#logging.debug('num_15M1H = %d'%counter_sell_15M1H)
						logging.debug('percentage_sell_tp_save_15M1H = %f'%percentage_sell_tp_save_15M1H)
						logging.debug('percentage_sell_st_save_15M1H = %f'%percentage_sell_st_save_15M1H)

					#counter_sell_15M1H += 1

			#*************************************** 15M30M SELL ******************************************************************


			if (flag_cross_15M30M == 'sell'):
			

				window_counter_1D = int(signal_counter_15M30M_sell/96) + 458 + 1
				window_counter_4H = int(signal_counter_15M30M_sell/16) + 1
				window_counter_1H = int(signal_counter_15M30M_sell/4) + 1
				window_counter_30M = int(signal_counter_15M30M_sell/2) + 1
				

			#************************************************ 15M Top Low Touched ************************************************************
				try:
					touch_counter = signal_counter_15M30M_sell

					while touch_counter > (signal_counter_15M30M_sell - 40):
						if ((symbol_data_15M[sym.name]['low'][touch_counter] <= (resist_sell_find_15M30M * 1.0002))):
							flag_lowtouch_15M = 'low_toched'
							flag_lowtouch_15M = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_15M[sym.name]['high'][(signal_counter_15M30M_sell - 2)] >= (protect_sell_find_15M30M * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(signal_counter_15M30M_sell - 1)] >= (protect_sell_find_15M30M * 1.0002))
							| (symbol_data_15M[sym.name]['high'][(signal_counter_15M30M_sell)] >= (protect_sell_find_15M30M * 1.0002))):
							flag_lowtouch_15M = ''
							flag_lowtouch_15M = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 15M &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')



				#logging.debug('')

				#************************************************ 1H Top Low Touched ************************************************************

				try:
					touch_counter = window_counter_1H-1

					while touch_counter > (window_counter_1H - 10):
						if ((symbol_data_1H[sym.name]['low'][touch_counter] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 2)] >= (protect_sell_find_1H)) 
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1 - 1)] >= (protect_sell_find_1H))
							| (symbol_data_1H[sym.name]['high'][(window_counter_1H-1)] >= (protect_sell_find_1H))):
							flag_lowtouch_1H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_1H[sym.name]['low'][(window_counter_1H-1)] <= (resist_sell_find_1H * 1.0002))):
							flag_lowtouch_1H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')

				#************************************************ 4H Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_4H-1

					while touch_counter > (window_counter_4H - 6):
						if ((symbol_data_4H[sym.name]['low'][touch_counter] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if ((symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 2)] >= (protect_sell_find)) 
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1 - 1)] >= (protect_sell_find))
							| (symbol_data_4H[sym.name]['high'][(window_counter_4H-1)] >= (protect_sell_find))):
							flag_lowtouch_4H = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						if (#(symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 3)] <= (resist_sell_find_4H * 1.0004)) 
							#| (symbol_data_4H[sym.name]['low'][(len(symbol_data_4H[sym.name]['low']) - 2)] <= (resist_sell_find_4H * 1.0004))
							(symbol_data_4H[sym.name]['low'][(window_counter_4H-1)] <= (resist_sell_find_4H * 1.0002))):
							flag_lowtouch_4H = 'low_toched'
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 4H &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')
					#logging.warning('No Data')


				#logging.debug('')
				#************************************************ 1D Top Low Touched ************************************************************
				try:
					touch_counter = window_counter_1D-1

					while touch_counter > (window_counter_1D - 30):
						if ((symbol_data_1D[sym.name]['low'][touch_counter] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if ((symbol_data_1D[sym.name]['high'][(window_counter_1D - 3)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D - 2)] >= (protect_sell_find))
						 | (symbol_data_1D[sym.name]['high'][(window_counter_1D-1)] >= (protect_sell_find))):
							flag_lowtouch_1D = ''
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


						if (#(symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 3)] <= (resist_sell_find_1D * 1.0016))
						 #| (symbol_data_1D[sym.name]['low'][(len(symbol_data_1D[sym.name]['low']) - 2)] <= (resist_sell_find_1D * 1.0016))
						 (symbol_data_1D[sym.name]['low'][(window_counter_1D-1)] <= (resist_sell_find_1D * 1.0002))):
							flag_lowtouch_1D = 'low_toched'
							#print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& protect touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
							#logging.debug('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& low touched 1D &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

						touch_counter -= 1

				except:
					print('No Data')


				if (flag_lowtouch_4H == 'low_toched'):
					flag_cross_15M30M = 'failed_sell'

				if (flag_lowtouch_1H == 'low_toched'):
					flag_cross_15M30M = 'failed_sell'

				#if (flag_lowtouch_1D == 'low_toched'):
				#	flag_cross_15M30M = 'failed_sell'

				if (flag_lowtouch_5M == 'low_toched'):
					flag_cross_15M30M = 'failed_sell'

				if (flag_cross_15M30M == 'sell'):

					if (sym.name == 'XAUUSD_i'):
						data_macd_15M_sell['tp'] = max(resist_sell_find_15M30M,(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]*0.998))
					else:
						data_macd_15M_sell['tp'] = resist_sell_find_15M30M * 1.0004


					if (SPANA_1D[int(signal_counter_15M30M_sell/96)+458] > SPANB_1D[int(signal_counter_15M30M_sell/96)+458]):
						data_macd_15M_sell['st'] = protect_sell_find_15M30M

					if (SPANA_1D[int(signal_counter_15M30M_sell/96)+458] <= SPANB_1D[int(signal_counter_15M30M_sell/96)+458]):
						data_macd_15M_sell['st'] = protect_sell_find_15M30M

					

					if data_macd_15M_sell['tp'] < symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]: 
						#window_counter_1M = MACD_signal_cross_1M_sell['index'] - 1
						#continue

						counter_i = signal_counter_15M30M_sell
						final_index = (signal_counter_15M30M_sell + 300)

						flag_index = 1

						if (final_index ) >= len(symbol_data_15M[sym.name]['close'])-1:
							final_index = len(symbol_data_15M[sym.name]['close'])-1
							flag_index = 0



						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}


						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_15M[sym.name]['close'][counter_i] - symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell] - symbol_data_15M[sym.name]['high'][counter_i])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]) * 100

							#print(percentage_buy_tp[counter_j])
							##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
							if(percentage_sell_tp[counter_j]<0):
								if (abs(percentage_sell_tp[counter_j]) >= (((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100)):
									break

							counter_i += 1
							counter_j += 1

							

							#if (counter_j > 50): break

						try:
							percentage_sell_tp_save_15M30M = min(percentage_sell_tp.values())
							percentage_sell_st_save_15M30M = min(percentage_sell_st.values())
						except:
							percentage_sell_tp_save_15M30M = 0
							percentage_sell_st_save_15M30M = 0

						logging.debug('************************ OUT_15M30M sell *******************************')

						if (abs(percentage_sell_tp_save_15M30M) >= (((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100)):
							logging.debug('sell_15M30M = SUCCSESSFULLY')
							logging.debug('------------------------%s' %sym.name)
							logging.debug('tp = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
							logging.debug('st = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-data_macd_15M_sell['st'])/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
							logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_1D)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
							logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_4H)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
							logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_1H)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
							logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_30M)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))

							logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
							logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find_1D)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
							logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find_4H)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))

							logging.debug('signal_counter_15M30M_sell = %f'%(signal_counter_15M30M_sell - MACD_signal_cross_15M_sell['index']))

							logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
							logging.debug('signal_counter_15M30M_sell[] = %f'%signal_counter_15M30M_sell)
							SUCCSESSFULLY += 1
						else:
							if (spred <= 0.045) & (flag_index != 0):
								logging.debug('sell_15M30M = FAILED')
								logging.debug('------------------------%s' %sym.name)
								logging.debug('tp = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-data_macd_15M_sell['tp'])/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
								logging.debug('st = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-data_macd_15M_sell['st'])/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
								logging.debug('tp resist_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_1D)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
								logging.debug('tp resist_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_4H)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
								logging.debug('tp resist_sell_find_1H = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_1H)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))
								logging.debug('tp resist_sell_find_30M = %f'%(((abs(symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]-resist_sell_find_30M)/symbol_data_15M[sym.name]['low'][signal_counter_15M30M_sell]))*100))

								logging.debug('st Protect_sell_find = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
								logging.debug('st Protect_sell_find_1D = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find_1D)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))
								logging.debug('st Protect_sell_find_4H = %f'%(((abs(symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]-protect_sell_find_4H)/symbol_data_15M[sym.name]['high'][signal_counter_15M30M_sell]))*100))

								logging.debug('signal_counter_15M30M_sell = %f'%(signal_counter_15M30M_sell - MACD_signal_cross_15M_sell['index']))

								logging.debug('window_counter_1D = %d'%(window_counter_1D-1))
								logging.debug('signal_counter_15M30M_sell[] = %f'%signal_counter_15M30M_sell)


								FAILED += 1

						#logging.debug('num_15M30M = %d'%counter_sell_15M30M)
						logging.debug('percentage_sell_tp_save_15M30M = %f'%percentage_sell_tp_save_15M30M)
						logging.debug('percentage_sell_st_save_15M30M = %f'%percentage_sell_st_save_15M30M)

					#counter_sell_15M30M += 1

			window_counter_1M = (MACD_signal_cross_1M_sell['index']) - 1
			if (window_counter_1M < 12000):
				break
			print(sym.name,' = ',window_counter_1M)

				#print('window_counter_1M = ',window_counter_1M)


		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
		logging.debug('')
		logging.debug('')

	logging.debug('FiS = %d'%SUCCSESSFULLY)
	logging.debug('FiF = %d'%FAILED)
#tester_strategy_bot_BUY()
#tester_strategy_bot_SELL()


def Task_BUY(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M):

	

	

	tester_BUY_AUDCAD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(1,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_AUDCAD_i.start()

	tester_BUY_AUDCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(2,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_AUDCHF_i.start()

	tester_BUY_AUDJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(3,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_AUDJPY_i.start()

	tester_BUY_AUDNZD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(4,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_AUDNZD_i.start()

	tester_BUY_AUDUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(5,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_AUDUSD_i.start()

	tester_BUY_CADCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(6,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_CADCHF_i.start()

	tester_BUY_CADJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(7,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_CADJPY_i.start()

	tester_BUY_CHFJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(8,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_CHFJPY_i.start()

	tester_BUY_EURAUD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(9,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURAUD_i.start()

	tester_BUY_EURCAD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(10,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURCAD_i.start()

	tester_BUY_EURCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(11,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURCHF_i.start()

	tester_BUY_EURGBP_i = threading.Thread(target=tester_strategy_bot_BUY,args=(12,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURGBP_i.start()

	tester_BUY_EURJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(13,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURJPY_i.start()

	tester_BUY_EURNZD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(14,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURNZD_i.start()

	tester_BUY_EURRUB_i = threading.Thread(target=tester_strategy_bot_BUY,args=(15,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURRUB_i.start()

	tester_BUY_EURUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(16,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_EURUSD_i.start()

	tester_BUY_GBPAUD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(17,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPAUD_i.start()

	tester_BUY_GBPCAD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(18,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPCAD_i.start()

	tester_BUY_GBPCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(19,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPCHF_i.start()

	tester_BUY_GBPJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(20,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPJPY_i.start()

	tester_BUY_GBPNZD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(21,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPNZD_i.start()

	tester_BUY_GBPSGD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(22,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPSGD_i.start()

	tester_BUY_GBPUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(23,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_GBPUSD_i.start()

	tester_BUY_NZDCAD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(24,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_NZDCAD_i.start()

	tester_BUY_NZDCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(25,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_NZDCHF_i.start()

	tester_BUY_NZDJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(26,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_NZDJPY_i.start()

	tester_BUY_NZDUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(27,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_NZDUSD_i.start()

	tester_BUY_USDCAD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(28,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_USDCAD_i.start()

	tester_BUY_USDCHF_i = threading.Thread(target=tester_strategy_bot_BUY,args=(29,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_USDCHF_i.start()

	tester_BUY_USDJPY_i = threading.Thread(target=tester_strategy_bot_BUY,args=(30,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_USDJPY_i.start()

	tester_BUY_USDSGD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(31,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_USDSGD_i.start()

	tester_BUY_XAGUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(32,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_XAGUSD_i.start()

	tester_BUY_XAUUSD_i = threading.Thread(target=tester_strategy_bot_BUY,args=(33,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_BUY_XAUUSD_i.start()

	tester_BUY_AUDCAD_i.join()
	tester_BUY_AUDCHF_i.join()
	tester_BUY_AUDJPY_i.join()
	tester_BUY_AUDNZD_i.join()
	tester_BUY_AUDUSD_i.join()
	tester_BUY_CADCHF_i.join()
	tester_BUY_CADJPY_i.join()
	tester_BUY_CHFJPY_i.join()
	tester_BUY_EURAUD_i.join()
	tester_BUY_EURCAD_i.join()
	tester_BUY_EURCHF_i.join()
	tester_BUY_EURGBP_i.join()
	tester_BUY_EURJPY_i.join()
	tester_BUY_EURNZD_i.join()
	tester_BUY_EURRUB_i.join()
	tester_BUY_EURUSD_i.join()
	tester_BUY_GBPAUD_i.join()
	tester_BUY_GBPCAD_i.join()
	tester_BUY_GBPCHF_i.join()
	tester_BUY_GBPJPY_i.join()
	tester_BUY_GBPNZD_i.join()
	tester_BUY_GBPSGD_i.join()
	tester_BUY_GBPUSD_i.join()
	tester_BUY_NZDCAD_i.join()
	tester_BUY_NZDCHF_i.join()
	tester_BUY_NZDJPY_i.join()
	tester_BUY_NZDUSD_i.join()
	tester_BUY_USDCAD_i.join()
	tester_BUY_USDCHF_i.join()
	tester_BUY_USDJPY_i.join()
	tester_BUY_USDSGD_i.join()
	tester_BUY_XAGUSD_i.join()
	tester_BUY_XAUUSD_i.join()



def Task_SELL(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M):

	tester_SELL_AUDCAD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(1,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_AUDCAD_i.start()

	tester_SELL_AUDCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(2,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_AUDCHF_i.start()

	tester_SELL_AUDJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(3,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_AUDJPY_i.start()

	tester_SELL_AUDNZD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(4,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_AUDNZD_i.start()

	tester_SELL_AUDUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(5,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_AUDUSD_i.start()

	tester_SELL_CADCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(6,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_CADCHF_i.start()

	tester_SELL_CADJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(7,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_CADJPY_i.start()

	tester_SELL_CHFJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(8,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_CHFJPY_i.start()

	tester_SELL_EURAUD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(9,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURAUD_i.start()

	tester_SELL_EURCAD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(10,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURCAD_i.start()

	tester_SELL_EURCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(11,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURCHF_i.start()

	tester_SELL_EURGBP_i = threading.Thread(target=tester_strategy_bot_SELL,args=(12,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURGBP_i.start()

	tester_SELL_EURJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(13,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURJPY_i.start()

	tester_SELL_EURNZD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(14,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURNZD_i.start()

	tester_SELL_EURRUB_i = threading.Thread(target=tester_strategy_bot_SELL,args=(15,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURRUB_i.start()

	tester_SELL_EURUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(16,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_EURUSD_i.start()

	tester_SELL_GBPAUD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(17,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPAUD_i.start()

	tester_SELL_GBPCAD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(18,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPCAD_i.start()

	tester_SELL_GBPCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(19,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPCHF_i.start()

	tester_SELL_GBPJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(20,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPJPY_i.start()

	tester_SELL_GBPNZD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(21,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPNZD_i.start()

	tester_SELL_GBPSGD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(22,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPSGD_i.start()

	tester_SELL_GBPUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(23,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_GBPUSD_i.start()

	tester_SELL_NZDCAD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(24,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_NZDCAD_i.start()

	tester_SELL_NZDCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(25,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_NZDCHF_i.start()

	tester_SELL_NZDJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(26,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_NZDJPY_i.start()

	tester_SELL_NZDUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(27,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_NZDUSD_i.start()

	tester_SELL_USDCAD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(28,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_USDCAD_i.start()

	tester_SELL_USDCHF_i = threading.Thread(target=tester_strategy_bot_SELL,args=(29,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_USDCHF_i.start()

	tester_SELL_USDJPY_i = threading.Thread(target=tester_strategy_bot_SELL,args=(30,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_USDJPY_i.start()

	tester_SELL_USDSGD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(31,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_USDSGD_i.start()

	tester_SELL_XAGUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(32,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_XAGUSD_i.start()

	tester_SELL_XAUUSD_i = threading.Thread(target=tester_strategy_bot_SELL,args=(33,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	tester_SELL_XAUUSD_i.start()

	tester_SELL_AUDCAD_i.join()
	tester_SELL_AUDCHF_i.join()
	tester_SELL_AUDJPY_i.join()
	tester_SELL_AUDNZD_i.join()
	tester_SELL_AUDUSD_i.join()
	tester_SELL_CADCHF_i.join()
	tester_SELL_CADJPY_i.join()
	tester_SELL_CHFJPY_i.join()
	tester_SELL_EURAUD_i.join()
	tester_SELL_EURCAD_i.join()
	tester_SELL_EURCHF_i.join()
	tester_SELL_EURGBP_i.join()
	tester_SELL_EURJPY_i.join()
	tester_SELL_EURNZD_i.join()
	tester_SELL_EURRUB_i.join()
	tester_SELL_EURUSD_i.join()
	tester_SELL_GBPAUD_i.join()
	tester_SELL_GBPCAD_i.join()
	tester_SELL_GBPCHF_i.join()
	tester_SELL_GBPJPY_i.join()
	tester_SELL_GBPNZD_i.join()
	tester_SELL_GBPSGD_i.join()
	tester_SELL_GBPUSD_i.join()
	tester_SELL_NZDCAD_i.join()
	tester_SELL_NZDCHF_i.join()
	tester_SELL_NZDJPY_i.join()
	tester_SELL_NZDUSD_i.join()
	tester_SELL_USDCAD_i.join()
	tester_SELL_USDCHF_i.join()
	tester_SELL_USDJPY_i.join()
	tester_SELL_USDSGD_i.join()
	tester_SELL_XAGUSD_i.join()
	tester_SELL_XAUUSD_i.join()


if __name__ == "__main__":
	print('Start')

	symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,12096)

	#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,99999)

	symbol_data_1D,my_money,symbols = symbol_data_5M,my_money,symbols#log_get_data_Genetic(mt5.TIMEFRAME_D1,0,500)

	#symbol_data_4H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,252)

	symbol_data_4H,my_money,symbols = symbol_data_5M,my_money,symbols

	symbol_data_1H,my_money,symbols = symbol_data_5M,my_money,symbols#log_get_data_Genetic(mt5.TIMEFRAME_H1,0,1008)
	symbol_data_30M,my_money,symbols = symbol_data_5M,my_money,symbols#log_get_data_Genetic(mt5.TIMEFRAME_M30,0,2016)
	symbol_data_15M,my_money,symbols = symbol_data_5M,my_money,symbols#log_get_data_Genetic(mt5.TIMEFRAME_M15,0,4032)
	#symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,0,60480)

	symbol_data_1M,my_money,symbols = symbol_data_5M,my_money,symbols

	#tester_strategy_bot_SELL(9,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	

	
	tester_strategy_bot_BUY(1,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(2,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(3,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(4,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(5,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	#tester_strategy_bot_BUY(6,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	
	tester_strategy_bot_BUY(7,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(8,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(9,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(10,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(11,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	
	tester_strategy_bot_BUY(12,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	
	tester_strategy_bot_BUY(13,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(14,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	
	tester_strategy_bot_BUY(16,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(17,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)


	tester_strategy_bot_BUY(18,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(19,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(20,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(21,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	
	tester_strategy_bot_BUY(22,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(23,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(24,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(25,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(26,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(27,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(28,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(29,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(30,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	tester_strategy_bot_BUY(31,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	tester_strategy_bot_BUY(33,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	
	

	#tester_strategy_bot_BUY(32,symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)
	


	#tester_BUY = threading.Thread(target=Task_BUY,args=(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	#tester_BUY.start()

	#tester_SELL = threading.Thread(target=Task_SELL,args=(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M))
	#tester_SELL.start()

	#tester_BUY.join()
	#tester_SELL.join()

	#Task_SELL(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	#Task_BUY(symbol_data_1D,symbol_data_4H,symbol_data_1H,symbol_data_30M,symbol_data_15M,symbol_data_5M,symbol_data_1M)

	print('End')
