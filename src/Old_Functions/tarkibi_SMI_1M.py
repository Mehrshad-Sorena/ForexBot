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

		if (my_money == 0): continue

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
		if ((sym.name == 'AUDNZD_i') | (sym.name == 'AUDNZD')):continue
		if ((sym.name == 'AUDCHF_i') | (sym.name == 'AUDCHF')):continue
		if ((sym.name == 'GBPNZD_i') | (sym.name == 'GBPNZD')):continue
		if ((sym.name == 'NZDJPY_i') | (sym.name == 'NZDJPY')):continue

		logging.info('***********************************************************************************************************************')
		logging.info('***********************************************************************************************************************')
		logging.info('***********************************************************************************************************************')
		logging.debug('                                           %s' %sym.name)
		#print('***********************************************************************************************************************')
		#print('***********************************************************************************************************************')
		#print('***********************************************************************************************************************')
		print('                                           ', sym.name,'                                                               ')

		symbol_data_5M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M5,200,sym.name)
		symbol_data_4H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H4,100,sym.name)

		vol_traded_max = (my_money/100) * 0.1

		symbol_data_vol,my_money,symbols_vol = log_get_data(mt5.TIMEFRAME_M1,10)

		vol_traded = 0

		flag_same_sell_5M = ''
		flag_same_buy_5M = ''

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

					if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M30M gen SMI')):
						#print('same sell')
						flag_same_sell_5M = 'same_sell'

					if ((sym.name == symbol_position) & (type_position == 0) & (comment_position == '5M30M gen SMI')):
						#print('same buy')
						flag_same_buy_5M = 'same_buy'

		#print(sym.name)
		if (vol_traded >= vol_traded_max): 
			#print('No Money')
			logging.warning('No Money')
			continue

		#****************************** Data_Buy 5M MACD *******************************************************************
		try:
			with open("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				#print('yes')
				for line in csv.DictReader(myfile):
					data_macd_5M_buy = line
					data_macd_5M_buy['tp'] = float(data_macd_5M_buy['tp'])
					data_macd_5M_buy['tp'] = (data_macd_5M_buy['tp']/3)*2

					data_macd_5M_buy['st'] = float(data_macd_5M_buy['st'])
					data_macd_5M_buy['macd_fast'] = 8#float(data_macd_5M_buy['macd_fast'])
					data_macd_5M_buy['macd_slow'] = 18#float(data_macd_5M_buy['macd_slow'])
					data_macd_5M_buy['macd_signal'] = 6#float(data_macd_5M_buy['macd_signal'])
					data_macd_5M_buy['diff_minus'] = float(data_macd_5M_buy['diff_minus'])
					data_macd_5M_buy['diff_plus'] = float(data_macd_5M_buy['diff_plus'])
					data_macd_5M_buy['score'] = 200#(float(data_macd_5M_buy['score']) / 2)

					#if(data_macd_5M_buy['score'] < max_allow_score):
					#	data_macd_5M_buy['score'] = data_macd_5M_buy['score']/10

		except:
			#continue

			data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 200}

			try:
				macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

				macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_buy)))

				data_macd_5M_buy = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2) ,'score': 200}

			except:
				#print('Cant calc MACD 5M Buy')
				logging.warning('Cant calc MACD 5M Buy')
				data_macd_5M_buy = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': 0 , 'diff_minus': 0,'score': 200}

			

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 5M MACD *******************************************************************

		try:
			with open("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M_sell = line
					data_macd_5M_sell['tp'] = float(data_macd_30M_sell['tp'])
					data_macd_5M_sell['tp'] = (data_macd_30M_sell['tp']/3)*2

					data_macd_5M_sell['st'] = float(data_macd_30M_sell['st'])
					data_macd_5M_sell['macd_fast'] = 8#float(data_macd_5M_sell['macd_fast'])
					data_macd_5M_sell['macd_slow'] = 18#float(data_macd_5M_sell['macd_slow'])
					data_macd_5M_sell['macd_signal'] = 6#float(data_macd_5M_sell['macd_signal'])
					data_macd_5M_sell['diff_minus'] = float(data_macd_5M_sell['diff_minus'])
					data_macd_5M_sell['diff_plus'] = float(data_macd_5M_sell['diff_plus'])
					data_macd_5M_sell['score'] = 200#(float(data_macd_5M_sell['score']) / 2)

					#if(data_macd_5M_sell['score'] < max_allow_score):
					#	data_macd_5M_sell['score'] = data_macd_5M_sell['score']/10

		except:
			#continue
			data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
			'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
			,'diff_plus':0 , 'diff_minus': 0,'score': 200}

			try:
				macd_all_5M_sell = ind.macd(symbol_data_5M[sym.name][data_macd_5M_sell['apply_to']],fast=data_macd_5M_sell['macd_fast'], slow=data_macd_5M_sell['macd_slow'],signal=data_macd_5M_sell['macd_signal'], verbose=True)

				macd_5M_sell = macd_all_5M_sell[macd_all_5M_sell.columns[0]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M_sell)))

				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.04, 'st' : 0.3,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': (abs(mean_macd) * 2) , 'diff_minus': ((-1) * abs(mean_macd) * 2),'score': 200}

			except:
				#print('Cant calc MACD 5M SELL')
				logging.warning('Cant calc MACD 5M SELL')
				data_macd_5M_sell = {'apply_to': 'close','tp' : 0.1, 'st' : 0.2,
				'macd_fast': 8 , 'macd_slow': 18, 'macd_signal': 6
				,'diff_plus': 0 , 'diff_minus': 0,'score': 200}

		#******************************//////////////////////***********************************************************

		#******************************//////////////////////***********************************************************
		#print('////////////////////////////////////////////')
		#print('Loading Data 2 .............')

		logging.debug('////////////////////////////////////////////')
		logging.debug('Loading Data 2 .............')

		symbol_data_5M,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_M5,200,sym.name)
		symbol_data_4H,my_money = log_get_data_one_by_one(mt5.TIMEFRAME_H4,100,sym.name)

		#print('Start Calculate .............')
		logging.debug('Start Calculate .............')
		

		#*************************************************************************************************************
		#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
		try:

			# *******************++++++++++++ MACD Buy 5M************************************************************

			macd_all_5M_buy = ind.macd(symbol_data_5M[sym.name][data_macd_5M_buy['apply_to']],fast=data_macd_5M_buy['macd_fast'], slow=data_macd_5M_buy['macd_slow'],signal=data_macd_5M_buy['macd_signal'], verbose=True)

			macd_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[0]]
			macdh_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[1]]
			macds_5M_buy = macd_all_5M_buy[macd_all_5M_buy.columns[2]]
			#MACD_signal_cross_5M_buy = cross_macd(macd_5M_buy,macds_5M_buy,macdh_5M_buy,sym.name,data_macd_5M_buy['diff_minus'],data_macd_5M_sell['diff_plus']/100)

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
			#MACD_signal_cross_5M_sell = cross_macd(macd_5M_sell,macds_5M_sell,macdh_5M_sell,sym.name,data_macd_5M_buy['diff_minus']/100,data_macd_5M_sell['diff_plus'])

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
                    tenkan=9,kijun=26,snkou=52)
			SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			#TsKs_signal_cross_5M = {}
			#TsKs_signal_cross_5M = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			#print('5M Buy TsKs Wrong!!')
			logging.warning('5M Buy TsKs Wrong!!')

			#*********************---------------------*************/////////////*************************************************
		signal = 0

		flag_cross_5M_buy = ''

		flag_cross_5M_sell = ''

		resist_buy_find_5M = 0
		protect_buy_find_5M = 0


		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('****** Signal Checking ********')
		logging.debug('')

		#******************************* Signal Checking 5M **************************************************************************

		alfa_fixed_buy = 0

		ramp_MACD_fixed_buy = 0
		ramp_candle_fixed_buy = 0

		Max_ramp_MACD_fixed_buy = 0
		Max_ramp_candle_fixed_buy = 0

		coef_ramps_fixed_buy = 0
		diff_ramps_fixed_buy = 0

		Max_coef_ramps_fixed_buy = 0
		Max_diff_ramps_fixed_buy = 0

		st_Coef_fixed_buy = 0
		tp_Coef_fixed_buy = 0

		if (sym.name == 'AUDCAD_i') | (sym.name == 'AUDCAD'):

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.089#0.6#0.062

			ramp_MACD_fixed_buy = 0.000004#0.000005
			ramp_candle_fixed_buy = -0.000013#-0.000014

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.000018

			ramp_sell_fixed = 0.000008

			coef_ramps_fixed_buy = -1.7
			diff_ramps_fixed_buy =  0.000006

			Max_coef_ramps_fixed_buy = -8.0
			Max_diff_ramps_fixed_buy = 0.000016

			st_Coef_fixed_buy = 0.9946
			tp_Coef_fixed_buy = 1

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.094#0.6

			ramp_MACD_fixed_buy = 0.000002#0.000005
			ramp_candle_fixed_buy = -0.000003#-0.000012

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00001

			ramp_sell_fixed = 0.00003

			coef_ramps_fixed_buy = -2.0
			diff_ramps_fixed_buy =  0.000002

			Max_coef_ramps_fixed_buy = -9.0
			Max_diff_ramps_fixed_buy = 0.00001

			st_Coef_fixed_buy = 0.994
			tp_Coef_fixed_buy = 1.2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.142#0.6

			ramp_MACD_fixed_buy = 0.000054#0.00001
			ramp_candle_fixed_buy = -0.000776#-0.001

			Max_ramp_MACD_fixed_buy = 0.0004
			Max_ramp_candle_fixed_buy = -0.001

			ramp_sell_fixed = -0.000302

			coef_ramps_fixed_buy = -2.3
			diff_ramps_fixed_buy =  0.000444

			Max_coef_ramps_fixed_buy = -12
			Max_diff_ramps_fixed_buy = 0.001

			st_Coef_fixed_buy = 0.9987
			tp_Coef_fixed_buy = 4.8

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.08#0.6

			ramp_MACD_fixed_buy = 0.000005#0.000012
			ramp_candle_fixed_buy = -0.000017#-0.000008

			Max_ramp_MACD_fixed_buy = 0.000012
			Max_ramp_candle_fixed_buy = -0.00003

			ramp_sell_fixed = -0.000001

			coef_ramps_fixed_buy = -3.2
			diff_ramps_fixed_buy =  0.000012

			Max_coef_ramps_fixed_buy = -6.0
			Max_diff_ramps_fixed_buy = 0.00003

			st_Coef_fixed_buy = 0.9957
			tp_Coef_fixed_buy = 2.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.112#0.6

			ramp_MACD_fixed_buy = 0.000005#0.000002
			ramp_candle_fixed_buy = -0.000016#-0.000014

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00001

			ramp_sell_fixed = 0.000006

			coef_ramps_fixed_buy = -2.3#-4
			diff_ramps_fixed_buy =  0.00001#0.000007

			Max_coef_ramps_fixed_buy = -7.0
			Max_diff_ramps_fixed_buy = 0.000006

			st_Coef_fixed_buy = 0.994
			tp_Coef_fixed_buy = 1.2#5.4

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.158#0.6 #0.33

			ramp_MACD_fixed_buy = 0.000002#0.000006
			ramp_candle_fixed_buy = -0.000021#-0.000013

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = 0.000009

			coef_ramps_fixed_buy = -4.0
			diff_ramps_fixed_buy =  0.000019

			Max_coef_ramps_fixed_buy = -3.0
			Max_diff_ramps_fixed_buy = 0.000008

			st_Coef_fixed_buy = 0.996
			tp_Coef_fixed_buy = 2.5#6.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.063#0.6#0.49

			ramp_MACD_fixed_buy = 0.0001#0.00055
			ramp_candle_fixed_buy = -0.001#-0.0019

			Max_ramp_MACD_fixed_buy = 0.0005
			Max_ramp_candle_fixed_buy = -0.001

			ramp_sell_fixed = -0.000413

			coef_ramps_fixed_buy = -2.9
			diff_ramps_fixed_buy =  0.0019

			Max_coef_ramps_fixed_buy = -4.0
			Max_diff_ramps_fixed_buy = 0.001

			st_Coef_fixed_buy = 0.9948
			tp_Coef_fixed_buy = 1.5#11

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.095#0.6#0.34

			ramp_MACD_fixed_buy = 0.0002#0.00066
			ramp_candle_fixed_buy = -0.001#-0.00067

			Max_ramp_MACD_fixed_buy = 0.001
			Max_ramp_candle_fixed_buy = -0.002

			ramp_sell_fixed = -0.00047

			coef_ramps_fixed_buy = -2.5
			diff_ramps_fixed_buy =  0.00065

			Max_coef_ramps_fixed_buy = -9.0
			Max_diff_ramps_fixed_buy = 0.001

			st_Coef_fixed_buy = 0.9955
			tp_Coef_fixed_buy = 1.5#12

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.034#0.6#0.15

			ramp_MACD_fixed_buy = 0.000004#0.000007
			ramp_candle_fixed_buy = -0.000033#-0.000032

			Max_ramp_MACD_fixed_buy = 0.000017
			Max_ramp_candle_fixed_buy = -0.000025

			ramp_sell_fixed = -0.000003

			coef_ramps_fixed_buy = -7.4
			diff_ramps_fixed_buy =  0.000029

			Max_coef_ramps_fixed_buy = -32.0
			Max_diff_ramps_fixed_buy = 0.000015

			st_Coef_fixed_buy = 0.998
			tp_Coef_fixed_buy = 1.5#2#2.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.116#0.17

			ramp_MACD_fixed_buy = 0.000003#0.00001
			ramp_candle_fixed_buy = -0.000002#-0.000017

			Max_ramp_MACD_fixed_buy = 0.000015
			Max_ramp_candle_fixed_buy = -0.00015

			ramp_sell_fixed = -0.000018

			coef_ramps_fixed_buy = -2.5
			diff_ramps_fixed_buy =  0.000006

			Max_coef_ramps_fixed_buy = -4.0
			Max_diff_ramps_fixed_buy = 0.000008

			st_Coef_fixed_buy = 0.9945
			tp_Coef_fixed_buy = 2.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.085#0.07

			ramp_MACD_fixed_buy = 0#0.000004
			ramp_candle_fixed_buy = -0.000012#-0.000007

			Max_ramp_MACD_fixed_buy = 0.000006
			Max_ramp_candle_fixed_buy = -0.00001

			ramp_sell_fixed = -0.000016

			coef_ramps_fixed_buy = -2.0
			diff_ramps_fixed_buy =  0.000006

			Max_coef_ramps_fixed_buy = -4.0
			Max_diff_ramps_fixed_buy = 0.000009

			st_Coef_fixed_buy = 0.996
			tp_Coef_fixed_buy = 2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.091#0.16

			ramp_MACD_fixed_buy = 0.000006#0.000003
			ramp_candle_fixed_buy = -0.000012#-0.000010

			Max_ramp_MACD_fixed_buy = 0.000012
			Max_ramp_candle_fixed_buy = -0.000004

			ramp_sell_fixed = -0.000013

			coef_ramps_fixed_buy = -1.6
			diff_ramps_fixed_buy =  0.000006

			Max_coef_ramps_fixed_buy = -30
			Max_diff_ramps_fixed_buy = 0.00004

			st_Coef_fixed_buy = 0.998
			tp_Coef_fixed_buy = 3.2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.081#0.18

			ramp_MACD_fixed_buy = 0.0005#0.00056
			ramp_candle_fixed_buy = -0.0016#-0.00084

			Max_ramp_MACD_fixed_buy = 0.001
			Max_ramp_candle_fixed_buy = -0.003

			ramp_sell_fixed = -0.00094

			coef_ramps_fixed_buy = -2.5
			diff_ramps_fixed_buy =  0.00098

			Max_coef_ramps_fixed_buy = -10
			Max_diff_ramps_fixed_buy = 0.002

			st_Coef_fixed_buy = 0.998
			tp_Coef_fixed_buy = 3

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.046#0.34

			ramp_MACD_fixed_buy = 0.000007#0.000015
			ramp_candle_fixed_buy = -0.000068#-0.000027

			Max_ramp_MACD_fixed_buy = 0.000019
			Max_ramp_candle_fixed_buy = -0.000035

			ramp_sell_fixed = -0.000007

			coef_ramps_fixed_buy = -7.8
			diff_ramps_fixed_buy =  0.00006

			Max_coef_ramps_fixed_buy = -10
			Max_diff_ramps_fixed_buy = 0.000019

			st_Coef_fixed_buy = 0.9957
			tp_Coef_fixed_buy = 1.1

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

			#************ BUY *******************    Final = No OK
			alfa_fixed_buy = 0#0.32

			ramp_MACD_fixed_buy = 0.0005# 0.000096
			ramp_candle_fixed_buy = -0.002#-0.000179

			Max_ramp_MACD_fixed_buy = 0.001
			Max_ramp_candle_fixed_buy = -0.0017

			ramp_sell_fixed = -0.004078

			coef_ramps_fixed_buy = -1.0
			diff_ramps_fixed_buy =  0.00007

			Max_coef_ramps_fixed_buy = -2
			Max_diff_ramps_fixed_buy = 0.001

			st_Coef_fixed_buy = 0.997
			tp_Coef_fixed_buy = 2.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.091#0.24

			ramp_MACD_fixed_buy = 0.000007#0.000009
			ramp_candle_fixed_buy = -0.00002#-0.00001

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = -0.000011

			coef_ramps_fixed_buy = -2.7
			diff_ramps_fixed_buy =  0.000013

			Max_coef_ramps_fixed_buy = -4.0
			Max_diff_ramps_fixed_buy = 0.00002

			st_Coef_fixed_buy = 0.998
			tp_Coef_fixed_buy = 2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.079#0.2

			ramp_MACD_fixed_buy = 0.000005#0.000005
			ramp_candle_fixed_buy = -0.000023#-0.000012

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = -0.000012

			coef_ramps_fixed_buy = -3
			diff_ramps_fixed_buy =  0.000017

			Max_coef_ramps_fixed_buy = -5.5
			Max_diff_ramps_fixed_buy = 0.00001

			st_Coef_fixed_buy = 0.9934
			tp_Coef_fixed_buy = 1.2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.029#0.28

			ramp_MACD_fixed_buy = 0.000015#0.000018
			ramp_candle_fixed_buy = -0.000034#-0.000039

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00004

			ramp_sell_fixed = -0.000007

			coef_ramps_fixed_buy = -2.5
			diff_ramps_fixed_buy =  0.00003

			Max_coef_ramps_fixed_buy = -8
			Max_diff_ramps_fixed_buy = 0.00003

			st_Coef_fixed_buy = 0.9993
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

			#************ BUY *******************    Final = OK
			alfa_fixed_buy = 0.086#0.24

			ramp_MACD_fixed_buy = 0.000004#0.000006
			ramp_candle_fixed_buy = -0.000017#-0.000007

			Max_ramp_MACD_fixed_buy = 0.000012
			Max_ramp_candle_fixed_buy = -0.000017

			ramp_sell_fixed = -0.000015

			coef_ramps_fixed_buy = -3.5
			diff_ramps_fixed_buy =  0.000013

			Max_coef_ramps_fixed_buy = -7.0
			Max_diff_ramps_fixed_buy = 0.000032

			st_Coef_fixed_buy = 0.9948
			tp_Coef_fixed_buy = 1.2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.099#0.35

			ramp_MACD_fixed_buy = 0.00012#0.003
			ramp_candle_fixed_buy = -0.002#-0.0008

			Max_ramp_MACD_fixed_buy = 0.000059
			Max_ramp_candle_fixed_buy = -0.006

			ramp_sell_fixed = -0.00086

			coef_ramps_fixed_buy = -4.2
			diff_ramps_fixed_buy =  0.0016

			Max_coef_ramps_fixed_buy = -5
			Max_diff_ramps_fixed_buy = 0.002

			st_Coef_fixed_buy = 0.997
			tp_Coef_fixed_buy = 1.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.106#0.37

			ramp_MACD_fixed_buy = 0.000005#0.000006
			ramp_candle_fixed_buy = -0.000035#-0.00002

			Max_ramp_MACD_fixed_buy = 0.000017
			Max_ramp_candle_fixed_buy = -0.00005

			ramp_sell_fixed = 0.000001

			coef_ramps_fixed_buy = -2.7
			diff_ramps_fixed_buy =  0.00003

			Max_coef_ramps_fixed_buy = -8.5
			Max_diff_ramps_fixed_buy = 0.000045

			st_Coef_fixed_buy = 0.9937
			tp_Coef_fixed_buy = 2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.076#0.34

			ramp_MACD_fixed_buy = 0.000007#0.000002
			ramp_candle_fixed_buy = -0.000019#-0.000001

			Max_ramp_MACD_fixed_buy = 0.000016
			Max_ramp_candle_fixed_buy = -0.000055

			ramp_sell_fixed = -0.000001

			coef_ramps_fixed_buy = -2.2
			diff_ramps_fixed_buy =  0.000011

			Max_coef_ramps_fixed_buy = -10
				Max_diff_ramps_fixed_buy = 0.00005

			st_Coef_fixed_buy = 0.9988
			tp_Coef_fixed_buy = 1.2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.09#0.34

			ramp_MACD_fixed_buy = 0.000005#0.000005
			ramp_candle_fixed_buy = -0.000009#-0.000012

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = -0.000002

			coef_ramps_fixed_buy = -1.7
			diff_ramps_fixed_buy =  0.000004

			Max_coef_ramps_fixed_buy = -4
			Max_diff_ramps_fixed_buy = 0.00001

			st_Coef_fixed_buy = 0.9945
			tp_Coef_fixed_buy = 1.5

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

			#************ BUY *******************    Final = OK
			alfa_fixed_buy = 0

			ramp_MACD_fixed_buy = 0.000004
			ramp_candle_fixed_buy = -0.000014

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = 0.000001

			coef_ramps_fixed_buy = -1.4
			diff_ramps_fixed_buy = 0.000008

			Max_coef_ramps_fixed_buy = -3.8
			Max_diff_ramps_fixed_buy = 0.000012

			st_Coef_fixed_buy = 0.997
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

			#************ BUY *******************    Final = OK
			alfa_fixed_buy = 0#0.16

			ramp_MACD_fixed_buy = 0.000007
			ramp_candle_fixed_buy = -0.000002

			Max_ramp_MACD_fixed_buy = 0.000007
			Max_ramp_candle_fixed_buy = -0.000007

			ramp_sell_fixed = -0.000003

			coef_ramps_fixed_buy = -4.2
			diff_ramps_fixed_buy =  0.000007

			Max_coef_ramps_fixed_buy = -4.0
			Max_diff_ramps_fixed_buy = 0.000012

			st_Coef_fixed_buy = 0.9979
			tp_Coef_fixed_buy = 1.5

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

			#************ BUY *******************    Final = OK
			alfa_fixed_buy = 0#0.08#0.553

			ramp_MACD_fixed_buy = 0.00078
			ramp_candle_fixed_buy = -0.0001

			Max_ramp_MACD_fixed_buy = 0.0001
			Max_ramp_candle_fixed_buy = -0.0003

			ramp_sell_fixed = -0.0003

			coef_ramps_fixed_buy = -4.7
			diff_ramps_fixed_buy =  0.00002

			Max_coef_ramps_fixed_buy = -3.0
			Max_diff_ramps_fixed_buy = 0.00005

			st_Coef_fixed_buy = 0.992
			tp_Coef_fixed_buy = 2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.057

			ramp_MACD_fixed_buy = 0.000008
			ramp_candle_fixed_buy = -0.000037

			Max_ramp_MACD_fixed_buy = 0.00001
			Max_ramp_candle_fixed_buy = -0.00003

			ramp_sell_fixed = -0.00001

			coef_ramps_fixed_buy = -4.5
			diff_ramps_fixed_buy =  0.000029

			Max_coef_ramps_fixed_buy = -6
			Max_diff_ramps_fixed_buy = 0.00003

			st_Coef_fixed_buy = 0.9967
			tp_Coef_fixed_buy = 2

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.068

			ramp_MACD_fixed_buy = 0.00001
			ramp_candle_fixed_buy = -0.000022

			Max_ramp_MACD_fixed_buy = 0.000013
			Max_ramp_candle_fixed_buy = -0.00003

			ramp_sell_fixed = -0.000005#-0.000013

			coef_ramps_fixed_buy = -1.8
			diff_ramps_fixed_buy =  0.000011

			Max_coef_ramps_fixed_buy = -6.5
			Max_diff_ramps_fixed_buy = 0.00002

			st_Coef_fixed_buy = 0.9958
			tp_Coef_fixed_buy = 1.2

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

			#************ BUY *******************    Final = No OK
			alfa_fixed_buy = 0

			ramp_MACD_fixed_buy = 0.000005
			ramp_candle_fixed_buy = -0.00007

			Max_ramp_MACD_fixed_buy = 0
			Max_ramp_candle_fixed_buy = -0.00002

			ramp_sell_fixed = -0.000035

			coef_ramps_fixed_buy = -1.6
			diff_ramps_fixed_buy =  0.000004

			Max_coef_ramps_fixed_buy = -5.3
			Max_diff_ramps_fixed_buy = 0.00002

			st_Coef_fixed_buy = 0.9988
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

			#************ BUY *******************    Final = OK
			alfa_fixed_buy = 0.063

			ramp_MACD_fixed_buy = 0.0008
			ramp_candle_fixed_buy = -0.0005

			Max_ramp_MACD_fixed_buy = 0.0004
			Max_ramp_candle_fixed_buy = -0.003

			ramp_sell_fixed = -0.000455

			coef_ramps_fixed_buy = -1.2
			diff_ramps_fixed_buy =  0.00014

			Max_coef_ramps_fixed_buy = -8
			Max_diff_ramps_fixed_buy = 0.0001

			st_Coef_fixed_buy = 0.995
			tp_Coef_fixed_buy = 2.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.05

			ramp_MACD_fixed_buy = 0.000003
			ramp_candle_fixed_buy = -0.00001

			Max_ramp_MACD_fixed_buy = 0.000006
			Max_ramp_candle_fixed_buy = -0.000016

			ramp_sell_fixed = -0.000003

			coef_ramps_fixed_buy = -1.7
			diff_ramps_fixed_buy =  0.000005

			Max_coef_ramps_fixed_buy = -5.5
			Max_diff_ramps_fixed_buy = 0.000014

			st_Coef_fixed_buy = 0.995
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

			#************ BUY *******************    Final = No OK
			alfa_fixed_buy = 0

			ramp_MACD_fixed_buy = 0.000351
			ramp_candle_fixed_buy = -0.002577

			Max_ramp_MACD_fixed_buy = 0.0001
			Max_ramp_candle_fixed_buy = -0.006

			ramp_sell_fixed = -0.004173

			coef_ramps_fixed_buy = -7.3
			diff_ramps_fixed_buy =  0.002226

			Max_coef_ramps_fixed_buy = -16.0
			Max_diff_ramps_fixed_buy = 0.006

			st_Coef_fixed_buy = 0.997
			tp_Coef_fixed_buy = 1.5

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

			#************ BUY *******************    Final = OK OK
			alfa_fixed_buy = 0.054

			ramp_MACD_fixed_buy = 0.009
			ramp_candle_fixed_buy = -0.025

			Max_ramp_MACD_fixed_buy = 0.012
			Max_ramp_candle_fixed_buy = -0.05

			ramp_sell_fixed = -0.014

			coef_ramps_fixed_buy = -2.7
			diff_ramps_fixed_buy =  0.015

			Max_coef_ramps_fixed_buy = -4.6
			Max_diff_ramps_fixed_buy = 0.03

			st_Coef_fixed_buy = 0.9947
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


		window_counter_5M = len(symbol_data_5M[sym.name]['low']) - 1
		window_counter_4H = len(symbol_data_4H[sym.name]['low']) - 1

		#******************************************** Signal Checking BUY ************************************************************
		try:
		#if True:

			if (((symbol_data_5M[sym.name]['low'][window_counter_5M - 2] < symbol_data_5M[sym.name]['low'][(window_counter_5M-3)])
				& (symbol_data_5M[sym.name]['low'][(window_counter_5M-1)] <= symbol_data_5M[sym.name]['low'][(window_counter_5M-2)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M] > symbol_data_5M[sym.name]['low'][(window_counter_5M-1)]))

				| ((symbol_data_5M[sym.name]['low'][(window_counter_5M-3)] < symbol_data_5M[sym.name]['low'][(window_counter_5M-4)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M-2] < symbol_data_5M[sym.name]['low'][(window_counter_5M-3)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M-1] >= symbol_data_5M[sym.name]['low'][(window_counter_5M-2)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M] >= symbol_data_5M[sym.name]['low'][(window_counter_5M-1)]))

				| ((symbol_data_5M[sym.name]['low'][(window_counter_5M-4)] <= symbol_data_5M[sym.name]['low'][(window_counter_5M-5)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M-3] < symbol_data_5M[sym.name]['low'][(window_counter_5M-4)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M-2] >= symbol_data_5M[sym.name]['low'][(window_counter_5M-3)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M-1] >= symbol_data_5M[sym.name]['low'][(window_counter_5M-2)])
				& (symbol_data_5M[sym.name]['low'][window_counter_5M] >= symbol_data_5M[sym.name]['low'][(window_counter_5M-1)]))):

				if ((symbol_data_4H[sym.name]['low'][(window_counter_4H)] <= symbol_data_4H[sym.name]['low'][(window_counter_4H-1)])):

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
								#print('count 1')
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
								#print('count 2')
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
						#print('count 3')
						#continue
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

						protect_line = ramp_candle_line * ((window_counter_5M) - min_candle_1_index) + min_candle_1
					else:
						protect_line = 0



					resist_buy_find_1M = symbol_data_4H[sym.name]['HLC/3'][window_counter_4H-1] #+ ((symbol_data_4H[sym.name]['HLC/3'][window_counter_4H-1]) * (0.5 * ramp_candle))#symbol_data_4H[sym.name]['close'][window_counter_4H-1] + (abs(symbol_data_4H[sym.name]['open'][window_counter_4H-1] - symbol_data_4H[sym.name]['close'][window_counter_4H-1]) * 0.6) #- symbol_data_5M[sym.name]['high'][window_counter_5M])/2) + symbol_data_5M[sym.name]['high'][window_counter_5M]

					#print('1 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

					dangrouse_line = protect_buy_find_1M + (((protect_buy_find_1M)*alfa_fixed_buy)/100)

					alfa = ((symbol_data_5M[sym.name]['high'][window_counter_5M] - protect_buy_find_1M)/(protect_buy_find_1M)) * 100

					#print('high = ',symbol_data_5M[sym.name]['high'][window_counter_5M])
					#print('protect_buy_find_1M = ',protect_buy_find_1M)
					#print('alfa = ',alfa)

					if (ramp != 0):
						Coef_ramps = (ramp_candle/ramp)
					else:
						Coef_ramps = 0

					diff_ramps = (abs(ramp_candle)-ramp)


					if (((((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100) >= 0.07)
						& ((ramp >= Max_ramp_MACD_fixed_buy) | (ramp_candle <= Max_ramp_MACD_fixed_buy)
						| (Coef_ramps <= Max_coef_ramps_fixed_buy) | (diff_ramps >= Max_diff_ramps_fixed_buy))):

						if (tp_Coef_fixed_buy != 1):
							resist_buy_find_1M = symbol_data_5M[sym.name]['high'][window_counter_5M] + (((((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M]))/tp_Coef_fixed_buy) * symbol_data_5M[sym.name]['high'][window_counter_5M])
							#print('2 = ',(((resist_buy_find_1M - symbol_data_5M[sym.name]['high'][window_counter_5M])/symbol_data_5M[sym.name]['high'][window_counter_5M])*100))

																


																

						#print('ramp = ',ramp)

					protect_buy_find_1M = protect_buy_find_1M * st_Coef_fixed_buy




					# Sell Check ***********************************************************

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
						#protect_sell_find_1M = max(symbol_data_5M[sym.name]['high'][(window_counter_5M - int(diff_5M_U_4H)):window_counter_5M])
																	
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
								#print('count 4')
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
								#print('count 5')
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
						#search_counter_1M_BUY += 1
						#print('count 6')
						#continue
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

						protect_line_sell = ramp_candle_line_sell * ((window_counter_5M) - max_candle_1_index) + max_candle_1
					else:
						protect_line_sell = 0



					#print('min_macd_div_2 = ',min_macd_div_2)
					#print('min_macd_div_1 = ',min_macd_div_1)

					#print('dangrouse_line = ',dangrouse_line)
					#print('symbol_data_5M[sym.name][low] = ',symbol_data_5M[sym.name]['high'][window_counter_5M])
					#print('0')

					#print('-1')

					if (resist_buy_find_1M >= protect_buy_find_1M):
						#print('0')
						if (ramp_candle <= ramp_candle_fixed_buy):
							#print('1')
							if (symbol_data_5M[sym.name]['high'][window_counter_5M] <= dangrouse_line):
								#print('2')
								if (ramp >= ramp_MACD_fixed_buy):
									#print('4')
									if (Coef_ramps <= coef_ramps_fixed_buy):
										#print('5')
										if ((symbol_data_5M[sym.name]['high'][window_counter_5M] >= protect_line)):
											#print('6')
											if (diff_ramps >= diff_ramps_fixed_buy):
												#print('7')
												if (alfa <= alfa_fixed_buy):
													#print('8')
													if ((symbol_data_5M[sym.name]['high'][window_counter_5M] <= SPANA_5M[window_counter_5M]) & (symbol_data_5M[sym.name]['high'][window_counter_5M] <= SPANB_5M[window_counter_5M])):

														if (ramp_sell >= ramp_sell_fixed):

															flag_cross_5M_buy = 'buy'

															data_macd_5M_buy['tp'] = resist_buy_find_1M
															data_macd_5M_buy['st'] = protect_buy_find_1M

															if (data_macd_5M_buy['tp'] < symbol_data_5M[sym.name]['high'][window_counter_5M]):
																flag_cross_5M_buy = ''

															if (flag_cross_5M_buy == 'buy'): 
																print('flag_cross_5M_buy = ',flag_cross_5M_buy)
																#continue
		except:
		#else:
			print('signal problem 1M BUY MACD!!!')
			#logging.warning('signal problem 1M SELL MACD!!!')
		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


		#******************************************** Signal Checking SELL ************************************************************

		window_counter_5M = len(symbol_data_5M[sym.name]['low']) - 1
		window_counter_4H = len(symbol_data_4H[sym.name]['low']) - 1

		try:
		#if True:

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

				if ((symbol_data_4H[sym.name]['high'][(window_counter_4H)] >= symbol_data_4H[sym.name]['high'][(window_counter_4H-1)])):


					hour_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].hour

					hour_4H = symbol_data_4H[sym.name]['time'][window_counter_4H].hour

					min_5M = symbol_data_5M[sym.name]['time'][window_counter_5M].minute

					diff_5M_U_4H = ((hour_5M - hour_4H) * 12) + int(min_5M/5)

					if (int(diff_5M_U_4H) < 0):
						diff_5M_U_4H = 0


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

					if (int(diff_5M_U_4H) < 0):
						diff_5M_U_4H = 0

					if (window_counter_5M - int(diff_5M_U_4H)) < (max_macd_div_2_index - 1):
						max_macd_div_1 = max(macd_5M_sell[(window_counter_5M - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)])

						index_counter = (window_counter_5M - int(diff_5M_U_4H))
						for i in macd_5M_sell[(window_counter_5M - int(diff_5M_U_4H)):(max_macd_div_2_index - 1)]:
							if (i == max_macd_div_1):
								max_macd_div_1_index = index_counter
							index_counter += 1

						max_candle_1 = symbol_data_5M[sym.name]['high'][max_macd_div_1_index]
						max_candle_1_index = max_macd_div_1_index

					else:
						#continue
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
						#continue
						min_macd_div_1 = macd_5M_buy[(min_macd_div_2_index - 1)]
						min_macd_div_1_index = (min_macd_div_2_index - 1)

						min_candle_1 = symbol_data_5M[sym.name]['low'][min_macd_div_1_index]
						min_candle_1_index = min_macd_div_1_index

					#print('max_macd_div_1 = ',max_macd_div_1)
					#print('max_macd_div_2 = ',max_macd_div_2)

					#print('max_macd_div_1_index = ',max_macd_div_1_index)
					
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

					if (resist_sell_find_1M <= protect_sell_find_1M): 

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

														if ((symbol_data_5M[sym.name]['low'][window_counter_5M] > SPANA_5M[window_counter_5M]) & (symbol_data_5M[sym.name]['low'][window_counter_5M] > SPANB_5M[window_counter_5M])):

															flag_cross_5M_sell = 'sell'

															data_macd_5M_sell['tp'] = resist_sell_find_1M
															data_macd_5M_sell['st'] = protect_sell_find_1M

															if (data_macd_5M_sell['tp'] > symbol_data_5M[sym.name]['low'][window_counter_5M]):
																flag_cross_5M_sell = ''

															if (flag_cross_5M_sell == 'sell'): 
																print('flag_cross_5M_buy = ',flag_cross_5M_buy)					
		except:
			print('Something wrong SELL')

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('')
		logging.debug('******* Signals ***********')

		#print('flag_cross_5M = ',flag_cross_5M)

		logging.debug('flag_cross_5M_buy = %s'%flag_cross_5M_buy)
		logging.debug('flag_cross_5M_sell = %s'%flag_cross_5M_sell)

		logging.debug('')
		logging.debug('////////////////////////////////////////////')
		logging.debug('')
		logging.debug('****** SELL OR BUY Doing ***********')
		logging.debug('')

		#************************************** 15M *******************************************************************************************
		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		account_count = 1000

		h,m,s,d = time_func()

		#************************************** 5M *******************************************************************************************
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
								sp_buy = ((abs(data_macd_5M_buy['st'])) - (((spred) * abs(data_macd_5M_buy['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_buy['score'] * my_money)/1000000))
	
							if (tp_buy <= (price)): continue

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
								sp_sell = ((abs(data_macd_5M_sell['st'])) + (((spred) * abs(data_macd_5M_sell['st']))/100))
								lot = float("{:.2f}".format((data_macd_5M_sell['score'] * my_money)/1000000))


							if (tp_sell >= (price)): continue


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
								continue

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
