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
import schedule as schedule_1
import schedule as schedule_5
import schedule as schedule_15
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
from Genetic_KSTSCross_buysell_algo_onebyone import *
from multiprocessing import Process
import threading
from Trade_Strategy_MACD import *
from Trade_Strategy_TsKs import *
from Accounts import *
from UTC_Time import *
from tarkibiporro import *
from tarkibiporro1000 import *
from Genetic_SMA import *
from tarkibi_SMI_5M import *
from tarkibi_SMI_15M import *
from tarkibi_SMI_1M import *
from stoploss_buy_find import *
from stoploss_sell_find import *
from tester_strategy_bot import *


#from ta import add_all_ta_features
#from ind.utils import dropna
#from ind.trend import MACD
#symbol_data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,1000)
#symbol_data_ichi,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,1000)

    

#my_func()
#help(ind.macd)

#macd_genetic_another_algo()

def Task_stoploss_buy_find_1D():
	try:
		print('******************************************* Start Task_stoploss_buy_find_1D ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,1000)

		for sym in symbols:
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

			print(sym.name,'1D')
			stoploss_buy_find(data[sym.name],0.5,'1D',sym.name)

		print('******************************************* Stop Task_stoploss_buy_find_1D ***********************************************')
	except:
		print('cant')

def Task_stoploss_buy_find_4H():
	try:
		print('******************************************* Start Task_stoploss_buy_find_4H ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H4,1000)

		for sym in symbols:
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

			print(sym.name,'4H')
			stoploss_buy_find(data[sym.name],0.2,'4H',sym.name)

		print('******************************************* Stop Task_stoploss_buy_find_4H ***********************************************')
	except:
		print('cant')

def Task_stoploss_buy_find_1H():
	try:
		print('******************************************* Start Task_stoploss_buy_find_1H ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,2000)

		for sym in symbols:
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

			print(sym.name,'1H')
			stoploss_buy_find(data[sym.name],0.1,'1H',sym.name)

		print('******************************************* Stop Task_stoploss_buy_find_1H ***********************************************')
	except:
		print('cant')


def Task_stoploss_buy_find_15M():
	print('******************************************* Start Task_stoploss_buy_find_15M ***********************************************')
	data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M15,1000)

	for sym in symbols:
		print(sym.name,'15M')
		stoploss_buy_find(data[sym.name],0.1,'15M',sym.name)

	print('******************************************* Stop Task_stoploss_buy_find_15M ***********************************************')

def Task_stoploss_buy_find_30M():
	try:
		print('******************************************* Start Task_stoploss_buy_find_30M ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,4000)

		for sym in symbols:
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

			print(sym.name,'30M')
			stoploss_buy_find(data[sym.name],0.05,'30M',sym.name)

		print('******************************************* Stop Task_stoploss_buy_find_30M ***********************************************')
	except:
		print('cant')


def Task_stoploss_buy_find_5M():
	print('******************************************* Start Task_stoploss_buy_find_5M ***********************************************')
	data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,2000)

	for sym in symbols:

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

		print(sym.name,'5M')
		stoploss_buy_find(data[sym.name],0.04,'5M',sym.name)

	print('******************************************* Stop Task_stoploss_buy_find_5M ***********************************************')

#*****************************************************************************************************************************************************

def Task_stoploss_sell_find_1D():
	try:
		print('******************************************* Start Task_stoploss_sell_find_1D ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_D1,1000)

		for sym in symbols:
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

			print(sym.name,'1D')
			stoploss_sell_find(data[sym.name],0.5,'1D',sym.name)

		print('******************************************* Stop Task_stoploss_sell_find_1D ***********************************************')
	except:
		print('cant')

def Task_stoploss_sell_find_4H():
	try:
		print('******************************************* Start Task_stoploss_sell_find_4H ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H4,1000)

		for sym in symbols:
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

			print(sym.name,'4H')
			stoploss_sell_find(data[sym.name],0.2,'4H',sym.name)

		print('******************************************* Stop Task_stoploss_sell_find_4H ***********************************************')
	except:
		print('cant')

def Task_stoploss_sell_find_1H():
	try:
		print('******************************************* Start Task_stoploss_sell_find_1H ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,2000)

		for sym in symbols:
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

			print(sym.name,'1H')
			stoploss_sell_find(data[sym.name],0.1,'1H',sym.name)

		print('******************************************* Stop Task_stoploss_sell_find_1H ***********************************************')
	except:
		print('cant')

def Task_stoploss_sell_find_30M():
	try:
		print('******************************************* Start Task_stoploss_sell_find_30M ***********************************************')
		data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M30,4000)

		for sym in symbols:
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

			print(sym.name,'30M')
			stoploss_sell_find(data[sym.name],0.05,'30M',sym.name)

		print('******************************************* Stop Task_stoploss_sell_find_30M ***********************************************')
	except:
		print('cant')


def Task_stoploss_sell_find_15M():
	print('******************************************* Start Task_stoploss_sell_find_15M ***********************************************')
	data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M15,1000)

	for sym in symbols:
		print(sym.name,'15M')
		stoploss_sell_find(data[sym.name],0.1,'15M',sym.name)

	print('******************************************* Stop Task_stoploss_sell_find_15M ***********************************************')

def Task_stoploss_sell_find_5M():
	print('******************************************* Start Task_stoploss_sell_find_5M ***********************************************')
	data,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,2000)

	for sym in symbols:

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

		print(sym.name,'5M')
		stoploss_sell_find(data[sym.name],0.04,'5M',sym.name)

	print('******************************************* Stop Task_stoploss_sell_find_5M ***********************************************')







def Task_MACD():
	#hour,minute,second = time_func()
	#print('MACD = ',hour,'::',minute,'::',second)
	if True:#(((minute%5) >= 0) & ((minute%5) <= 1)):
		if True:#(hour != 0):
			print('******************************************* Start MACD ***********************************************')
			max_allow_score = 50
			#trade_strategy_macd(max_allow_score)
			print('******************************************* Stop MACD ***********************************************')

def Task_TsKs():
	#hour,minute,second = time_func()
	#print('TsKs = ',hour,'::',minute,'::',second)
	if True:#(((minute%5) >= 0) & ((minute%5) <= 1)):
		if True:#(hour != 0):
			print('******************************************* Start TsKs ***********************************************')
			#trade_strategy_TsKs()
			print('******************************************* Stop TsKs ***********************************************')

def Task_tarkibiporro():
	#hour,minute,second = time_func()
	#print('TsKs = ',hour,'::',minute,'::',second)
	if True:#(((minute%5) >= 0) & ((minute%5) <= 1)):
		if False:
			print('******************************************* ERROR Time Trade ********************************************')
			#continue
		else:
			print('******************************************* Start Tarkibi ***********************************************')

			trade_strategy_tarkibi(20)
			print('******************************************* Stop Tarkibi ***********************************************')

def Task_tarkibi_SMI_5M():
	print('******************************************* Start SMI 5M Trade ***********************************************')
	T_TarkibiSMI_5M = threading.Thread(target=trade_strategy_SMI_5M)
	T_TarkibiSMI_5M.start()
	T_TarkibiSMI_5M.join()

	#P_TarkibiSMI_5M = Process(target=trade_strategy_SMI_5M)
	#P_TarkibiSMI_5M.start()
	#P_TarkibiSMI_5M.join()

	#trade_strategy_SMI_5M(20)
	print('******************************************* Stop SMI 5M Trade ***********************************************')


def Task_tarkibi_SMI_1M():
	print('******************************************* Start SMI 1M Trade ***********************************************')
	hour,minute,second,day = time_func()
	print(hour,':',minute,':',second)

	#T_TarkibiSMI_1M = threading.Thread(target=trade_strategy_SMI_1M)
	#T_TarkibiSMI_1M.start()
	#T_TarkibiSMI_1M.join()

	#P_TarkibiSMI_1M = Process(target=trade_strategy_SMI_1M)
	#P_TarkibiSMI_1M.start()
	#P_TarkibiSMI_1M.join()

	trade_strategy_SMI_1M()
	hour,minute,second,day = time_func()
	print(hour,':',minute,':',second)

	#print('trade_counter = ',trade_counter)
	
	print('******************************************* Stop SMI 1M Trade ***********************************************')

#Task_tarkibi_SMI_1M()

def Task_tarkibi_SMI_15M():
	print('******************************************* Start SMI 15M Trade ***********************************************')
	T_TarkibiSMI_15M = threading.Thread(target=trade_strategy_SMI_15M)
	T_TarkibiSMI_15M.start()
	T_TarkibiSMI_15M.join()

	#P_TarkibiSMI_15M = Process(target=trade_strategy_SMI_15M)
	#P_TarkibiSMI_15M.start()
	#P_TarkibiSMI_15M.join()

	print('******************************************* Stop SMI 15M Trade ***********************************************')


#trade_strategy_tarkibi(20,0.1)
#trade_strategy_tarkibi(20)
def Task_tarkibiporro_1000():
	#hour,minute,second = time_func()
	#print('TsKs = ',hour,'::',minute,'::',second)
	if True:#(((minute%5) >= 0) & ((minute%5) <= 1)):
		if False:
			print('******************************************* ERROR Time Trade ********************************************')
			#continue
		else:
			print('******************************************* Start Tarkibi ***********************************************')
			trade_strategy_tarkibi_1000(20)
			print('******************************************* Stop Tarkibi ***********************************************')


#time_func()
#help(ind.ichimoku)
#Task_1()
#schedule.every(1).minutes.do(Task_1)
#schedule.every(4320).minutes.do(macd_genetic)
#schedule.every(4320).minutes.do(macd_genetic_sell_algo)
#schedule.every(4740).minutes.do(macd_genetic_buy_algo)

#my_func()

#schedule.every(10).seconds.do(time_func)



def Task_Trade_main_1M():
	#T_MACD = threading.Thread(target=Task_MACD)
	#T_MACD.start()

	#T_TsKs = threading.Thread(target=Task_TsKs)
	#T_TsKs.start()

	

	



	while True:
		#print('schedule')
		hour,minute,second,day = time_func()
		if False:#((minute == 29) | (minute == 59)):
			#(((hour == 0) & (minute >= 30))
#			| (hour == 1)
#			| ((hour == 2) & (minute <= 30))

#			| (hour == 3)
#			| ((hour == 4) & (minute <= 30))

#			| ((hour == 10))
#			| ((hour == 11))
#			| ((hour == 12))

#			| ((hour == 15) & (minute >= 30))
#			| (hour == 16)

#			| ((hour == 19) & (minute >= 30))
#			| ((hour == 20))

			#| ((day == 'Friday') & (hour >= 6))
			#| ((day == 'Saturday') & (hour <= 6))):
			#print('hello')
			schedule_1.clear()
			continue
		#else:
			#print('yellow')
			

			

			

			
			#T_TarkibiSMA = threading.Thread(target=Task_tarkibi_SMA)
			#T_TarkibiSMA.start()

			#T_Tarkibiporro_1000 = threading.Thread(target=Task_tarkibiporro_1000)
			#T_Tarkibiporro_1000.start()
			
			#T_MACD.join()
			#T_TsKs.join()
			
			
			
			
			#T_TarkibiSMA.join()

			#T_Tarkibiporro_1000.join()

		try:
			schedule_1.run_pending()
			#os.sleep(10)
		except:
			print('thread Wrong 1M')

def Task_Trade_main_5M():
	#T_MACD = threading.Thread(target=Task_MACD)
	#T_MACD.start()

	#T_TsKs = threading.Thread(target=Task_TsKs)
	#T_TsKs.start()

	

	



	while True:
		#print('schedule')
		hour,minute,second,day = time_func()
		if ((minute == 29) | (minute == 59)):
			#(((hour == 0) & (minute >= 30))
#			| (hour == 1)
#			| ((hour == 2) & (minute <= 30))

#			| (hour == 3)
#			| ((hour == 4) & (minute <= 30))

#			| ((hour == 10))
#			| ((hour == 11))
#			| ((hour == 12))

#			| ((hour == 15) & (minute >= 30))
#			| (hour == 16)

#			| ((hour == 19) & (minute >= 30))
#			| ((hour == 20))

			#| ((day == 'Friday') & (hour >= 6))
			#| ((day == 'Saturday') & (hour <= 6))):
			#print('hello')
			schedule_5.clear()
			continue
		#else:
			#print('yellow')
			

			

			

			
			#T_TarkibiSMA = threading.Thread(target=Task_tarkibi_SMA)
			#T_TarkibiSMA.start()

			#T_Tarkibiporro_1000 = threading.Thread(target=Task_tarkibiporro_1000)
			#T_Tarkibiporro_1000.start()
			
			#T_MACD.join()
			#T_TsKs.join()
			
			
			
			
			#T_TarkibiSMA.join()

			#T_Tarkibiporro_1000.join()

		try:
			schedule_5.run_pending()
			#os.sleep(10)
		except:
			print('thread Wrong 5M')


def Task_Trade_main_15M():
	#T_MACD = threading.Thread(target=Task_MACD)
	#T_MACD.start()

	#T_TsKs = threading.Thread(target=Task_TsKs)
	#T_TsKs.start()

	

	



	while True:
		#print('schedule')
		hour,minute,second,day = time_func()
		if ((minute == 29) | (minute == 59)):
			#(((hour == 0) & (minute >= 30))
#			| (hour == 1)
#			| ((hour == 2) & (minute <= 30))

#			| (hour == 3)
#			| ((hour == 4) & (minute <= 30))

#			| ((hour == 10))
#			| ((hour == 11))
#			| ((hour == 12))

#			| ((hour == 15) & (minute >= 30))
#			| (hour == 16)

#			| ((hour == 19) & (minute >= 30))
#			| ((hour == 20))

			#| ((day == 'Friday') & (hour >= 6))
			#| ((day == 'Saturday') & (hour <= 6))):
			#print('hello')
			schedule_15.clear()
			continue
		#else:
			#print('yellow')
			

			

			

			
			#T_TarkibiSMA = threading.Thread(target=Task_tarkibi_SMA)
			#T_TarkibiSMA.start()

			#T_Tarkibiporro_1000 = threading.Thread(target=Task_tarkibiporro_1000)
			#T_Tarkibiporro_1000.start()
			
			#T_MACD.join()
			#T_TsKs.join()
			
			
			
			
			#T_TarkibiSMA.join()

			#T_Tarkibiporro_1000.join()

		try:
			schedule_15.run_pending()
			#os.sleep(10)
		except:
			print('thread Wrong 15M')
#Task_Trade_main()	

#schedule_5.every(5).minutes.do(Task_tarkibi_SMI_5M)

#schedule_15.every(15).minutes.do(Task_tarkibi_SMI_15M)

Task_tarkibi_SMI_1M()



schedule_1.every(3).minutes.do(Task_tarkibi_SMI_1M)

#try:
#	Task_stoploss_buy_find_1D()
#except:
#	print('cant')

#try:
#	Task_stoploss_buy_find_4H()
#except:
#	print('cant')

#try:
#	Task_stoploss_buy_find_1H()
#except:
#	print('cant')

#try:
#	Task_stoploss_buy_find_30M()
#except:
#	print('cant')

#Task_stoploss_buy_find_15M()
#Task_stoploss_buy_find_5M()

#try:
#	Task_stoploss_sell_find_1D()
#except:
#	print('cant')

#try:
#	Task_stoploss_sell_find_4H()
#except:
#	print('cant')

#try:
#	Task_stoploss_sell_find_1H()
#except:
#	print('cant')

#try:
#	Task_stoploss_sell_find_30M()
#except:
#	print('cant')
#Task_stoploss_sell_find_15M()
#Task_stoploss_sell_find_5M()

schedule_1.every(1440).minutes.do(Task_stoploss_buy_find_1D)

schedule_1.every(720).minutes.do(Task_stoploss_buy_find_4H)

schedule_1.every(720).minutes.do(Task_stoploss_buy_find_1H)

schedule_1.every(720).minutes.do(Task_stoploss_buy_find_30M)

#schedule_1.every(60).minutes.do(Task_stoploss_buy_find_5M)


schedule_1.every(1440).minutes.do(Task_stoploss_sell_find_1D)

schedule_1.every(720).minutes.do(Task_stoploss_sell_find_4H)

schedule_1.every(720).minutes.do(Task_stoploss_sell_find_1H)

schedule_1.every(720).minutes.do(Task_stoploss_sell_find_30M)

#schedule_1.every(60).minutes.do(Task_stoploss_sell_find_5M)


#macd_genetic_buy_algo_5M(0.02,2,5,30)


def Task_5M_AND_30M_MACD_Algo():
	num_turn = 5
	max_score = 50
	max_num_trade = 3
	tp_limit = 0.1

	#T_1M_Buy = threading.Thread(target=macd_genetic_buy_algo_1M, args=(0.02,max_num_trade,num_turn,20))
	#T_1M_Buy.start()

	#T_1M_Sell = threading.Thread(target=macd_genetic_sell_algo_1M, args=(0.02,max_num_trade,num_turn,20))
	#T_1M_Sell.start()

	T_5M_Buy = threading.Thread(target=macd_genetic_buy_algo_5M, args=(0.04,max_num_trade,num_turn,50))
	T_5M_Buy.start()

	T_5M_Sell = threading.Thread(target=macd_genetic_sell_algo_5M, args=(0.04,max_num_trade,num_turn,50))
	T_5M_Sell.start()


	T_15M_Buy = threading.Thread(target=macd_genetic_buy_algo_15M, args=(0.2,max_num_trade,num_turn,50))
	T_15M_Buy.start()

	T_15M_Sell = threading.Thread(target=macd_genetic_sell_algo_15M, args=(0.2,max_num_trade,num_turn,50))
	T_15M_Sell.start()



	T_1H_Buy = threading.Thread(target=macd_genetic_buy_algo_1H, args=(0.2,max_num_trade,num_turn,max_score))
	T_1H_Buy.start()

	T_1H_Sell = threading.Thread(target=macd_genetic_sell_algo_1H, args=(0.2,max_num_trade,num_turn,max_score))
	T_1H_Sell.start()



	T_30M_Buy = threading.Thread(target=macd_genetic_buy_algo_30M, args=(0.08,max_num_trade,num_turn,max_score))
	T_30M_Buy.start()

	T_30M_Sell = threading.Thread(target=macd_genetic_sell_algo_30M, args=(0.08,max_num_trade,num_turn,max_score))
	T_30M_Sell.start()


	T_1D_Buy = threading.Thread(target=macd_genetic_buy_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	T_1D_Buy.start()

	T_1D_Sell = threading.Thread(target=macd_genetic_sell_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	T_1D_Sell.start()

	#T_5M30M_Buy = threading.Thread(target=macd_genetic_buy_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Buy.start()

	#T_5M30M_Sell = threading.Thread(target=macd_genetic_sell_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Sell.start()

	#T_porro_Buy = threading.Thread(target=macd_genetic_buy_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Buy.start()

	#T_porro_Sell = threading.Thread(target=macd_genetic_sell_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Sell.start()

	#T_1M_Buy.join()
	#T_1M_Sell.join()

	T_5M_Buy.join()
	T_5M_Sell.join()

	T_15M_Buy.join()
	T_15M_Sell.join()

	T_30M_Sell.join()
	T_30M_Buy.join()

	T_1H_Sell.join()
	T_1H_Buy.join()

	T_1D_Sell.join()
	T_1D_Buy.join()

	#T_5M30M_Sell.join()
	#T_5M30M_Buy.join()

	#T_porro_Sell.join()
	#T_porro_Buy.join()

def Task_1H_AND_1D_MACD_Algo():
	num_turn = 5
	max_score = 50
	max_num_trade = 3
	tp_limit = 0.1

	#T_5M_Buy = threading.Thread(target=macd_genetic_buy_algo_5M, args=(0.07,max_num_trade,num_turn,1))
	#T_5M_Buy.start()

	#T_5M_Sell = threading.Thread(target=macd_genetic_sell_algo_5M, args=(0.07,max_num_trade,num_turn,1))
	#T_5M_Sell.start()

	T_1H_Buy = threading.Thread(target=macd_genetic_buy_algo_1H, args=(0.09,max_num_trade,num_turn,50))
	T_1H_Buy.start()

	T_1H_Sell = threading.Thread(target=macd_genetic_sell_algo_1H, args=(0.09,max_num_trade,num_turn,50))
	T_1H_Sell.start()

	#T_30M_Buy = threading.Thread(target=macd_genetic_buy_algo_30M, args=(0.12,max_num_trade,num_turn,max_score))
	#T_30M_Buy.start()

	#T_30M_Sell = threading.Thread(target=macd_genetic_sell_algo_30M, args=(0.12,max_num_trade,num_turn,max_score))
	#T_30M_Sell.start()


	T_1D_Buy = threading.Thread(target=macd_genetic_buy_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	T_1D_Buy.start()

	T_1D_Sell = threading.Thread(target=macd_genetic_sell_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	T_1D_Sell.start()

	#T_5M30M_Buy = threading.Thread(target=macd_genetic_buy_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Buy.start()

	#T_5M30M_Sell = threading.Thread(target=macd_genetic_sell_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Sell.start()

	#T_porro_Buy = threading.Thread(target=macd_genetic_buy_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Buy.start()

	#T_porro_Sell = threading.Thread(target=macd_genetic_sell_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Sell.start()

	#T_5M_Buy.join()
	#T_5M_Sell.join()

	#T_30M_Sell.join()
	#T_30M_Buy.join()

	T_1H_Sell.join()
	T_1H_Buy.join()

	T_1D_Sell.join()
	T_1D_Buy.join()

	#T_5M30M_Sell.join()
	#T_5M30M_Buy.join()

	#T_porro_Sell.join()
	#T_porro_Buy.join()

#schedule.every(1440).minutes.do(Task_5M_AND_1H_AND_30M_MACD_Algo)


def Task_5M_AND_1H_AND_30M_TsKs_Algo():
	num_turn = 5
	max_score = 50
	max_num_trade = 3
	tp_limit = 0.1

	T_1M_Buy = threading.Thread(target=TsKs_genetic_buy_algo_1M, args=(0.04,max_num_trade,num_turn,max_score))
	T_1M_Buy.start()

	T_1M_Sell = threading.Thread(target=TsKs_genetic_sell_algo_1M, args=(0.04,max_num_trade,num_turn,max_score))
	T_1M_Sell.start()

	T_5M_Buy = threading.Thread(target=TsKs_genetic_buy_algo_5M, args=(0.08,max_num_trade,num_turn,max_score))
	T_5M_Buy.start()

	T_5M_Sell = threading.Thread(target=TsKs_genetic_sell_algo_5M, args=(0.08,max_num_trade,num_turn,max_score))
	T_5M_Sell.start()

	T_30M_Buy = threading.Thread(target=TsKs_genetic_buy_algo_30M, args=(0.12,max_num_trade,num_turn,max_score))
	T_30M_Buy.start()

	T_30M_Sell = threading.Thread(target=TsKs_genetic_sell_algo_30M, args=(0.12,max_num_trade,num_turn,max_score))
	T_30M_Sell.start()

	T_1H_Buy = threading.Thread(target=TsKs_genetic_buy_algo_1H, args=(0.15,max_num_trade,num_turn,max_score))
	T_1H_Buy.start()

	T_1H_Sell = threading.Thread(target=TsKs_genetic_sell_algo_1H, args=(0.15,max_num_trade,num_turn,max_score))
	T_1H_Sell.start()


	#T_5M30M_Buy = threading.Thread(target=TsKs_genetic_buy_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Buy.start()

	#T_5M30M_Sell = threading.Thread(target=TsKs_genetic_sell_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Sell.start()

	#T_porro_Buy = threading.Thread(target=TsKs_genetic_buy_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Buy.start()

	#T_porro_Sell = threading.Thread(target=TsKs_genetic_sell_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Sell.start()

	T_1M_Sell.join()
	T_1M_Buy.join()

	T_5M_Sell.join()
	T_5M_Buy.join()

	T_30M_Sell.join()
	T_30M_Buy.join()

	T_1H_Sell.join()
	T_1H_Buy.join()

	#T_5M30M_Sell.join()
	#T_5M30M_Buy.join()

	#T_porro_Sell.join()
	#T_porro_Buy.join()

#schedule.every(1440).minutes.do(Task_5M_AND_1H_AND_30M_TsKs_Algo)


def Task_5M_AND_30M_SMA_Algo():
	num_turn = 4
	max_score = 50
	max_num_trade = 3
	tp_limit = 0.1

	T_1M_Buy = threading.Thread(target=SMA_genetic_buy_algo_1M, args=(0.04,max_num_trade,num_turn,50))
	T_1M_Buy.start()

	T_1M_Sell = threading.Thread(target=SMA_genetic_sell_algo_1M, args=(0.04,max_num_trade,num_turn,50))
	T_1M_Sell.start()

	T_5M_Buy = threading.Thread(target=SMA_genetic_buy_algo_5M, args=(0.06,max_num_trade,num_turn,50))
	T_5M_Buy.start()

	T_5M_Sell = threading.Thread(target=SMA_genetic_sell_algo_5M, args=(0.06,max_num_trade,num_turn,50))
	T_5M_Sell.start()

	#T_1H_Buy = threading.Thread(target=macd_genetic_buy_algo_1H, args=(0.09,max_num_trade,num_turn,max_score))
	#T_1H_Buy.start()

	#T_1H_Sell = threading.Thread(target=macd_genetic_sell_algo_1H, args=(0.09,max_num_trade,num_turn,max_score))
	#T_1H_Sell.start()

	#T_30M_Buy = threading.Thread(target=SMA_genetic_buy_algo_30M, args=(0.08,max_num_trade,num_turn,max_score))
	#T_30M_Buy.start()

	#T_30M_Sell = threading.Thread(target=SMA_genetic_sell_algo_30M, args=(0.08,max_num_trade,num_turn,max_score))
	#T_30M_Sell.start()


	#T_1D_Buy = threading.Thread(target=macd_genetic_buy_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	#T_1D_Buy.start()

	#T_1D_Sell = threading.Thread(target=macd_genetic_sell_algo_1D, args=(1.4,max_num_trade,num_turn,max_score))
	#T_1D_Sell.start()

	#T_5M30M_Buy = threading.Thread(target=macd_genetic_buy_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Buy.start()

	#T_5M30M_Sell = threading.Thread(target=macd_genetic_sell_algo_5M30M, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_5M30M_Sell.start()

	#T_porro_Buy = threading.Thread(target=macd_genetic_buy_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Buy.start()

	#T_porro_Sell = threading.Thread(target=macd_genetic_sell_algo_porro, args=(tp_limit,max_num_trade,num_turn,max_score))
	#T_porro_Sell.start()

	T_1M_Buy.join()
	T_1M_Sell.join()

	T_5M_Buy.join()
	T_5M_Sell.join()

	#T_30M_Sell.join()
	#T_30M_Buy.join()

	#T_1H_Sell.join()
	#T_1H_Buy.join()

	#T_1D_Sell.join()
	#T_1D_Buy.join()

	#T_5M30M_Sell.join()
	#T_5M30M_Buy.join()

	#T_porro_Sell.join()
	#T_porro_Buy.join()


if __name__ == "__main__":
	#threading.Thread(target=macd_genetic_buy_algo_30M).start()

	#threading.Thread(target=macd_genetic_buy_algo_30M, args=(tp_limit,max_num_trade,num_turn,max_score)).start()

	
	print('Start')

	#st_P_1 = Process(target=Task_stoploss_buy_find_1H)
	#st_P_1.start()

	#st_P_2 = threading.Thread(target=Task_stoploss_buy_find_30M)
	#st_P_2.start()

	#st_P_3 = threading.Thread(target=Task_stoploss_sell_find_1H)
	#st_P_3.start()

	#st_P_4 = threading.Thread(target=Task_stoploss_sell_find_30M)
	#st_P_4.start()

	#st_P_5 = threading.Thread(target=Task_stoploss_sell_find_5M)
	#st_P_5.start()

	#st_P_6 = threading.Thread(target=Task_stoploss_buy_find_5M)
	#st_P_6.start()

	#tester_P = threading.Thread(target=tester_strategy_bot)
	#tester_P.start()


	#st_T_1 = threading.Thread(target=Task_stoploss_buy_find_1D)
	#st_T_1.start()

	#st_T_2 = threading.Thread(target=Task_stoploss_buy_find_4H)
	#st_T_2.start()

	#st_T_3 = threading.Thread(target=Task_stoploss_sell_find_1D)
	#st_T_3.start()

	#st_T_4 = threading.Thread(target=Task_stoploss_sell_find_4H)
	#st_T_4.start()


	#st_P_1.join()
	#st_P_2.join()
	#st_P_3.join()
	#st_P_4.join()

	#st_P_5.join()
	#st_P_6.join()

	#tester_P.join()

	#st_T_1.join()
	#st_T_2.join()
	#st_T_3.join()
	#st_T_4.join()


	#p_MACD_1 = Process(target=Task_5M_AND_30M_MACD_Algo)
	#p_MACD_1.start()

	#p_MACD_2 = Process(target=Task_1H_AND_1D_MACD_Algo)
	#p_MACD_2.start()

	#p_SMA = Process(target=Task_5M_AND_30M_SMA_Algo)
	#p_SMA.start()

	

	#p_TsKs = Process(target=Task_5M_AND_1H_AND_30M_TsKs_Algo)
	#p_TsKs.start()

	#trade = Process(target=Task_Trade_main_1M)
	#trade.start()

	#trade_1M = threading.Thread(target=Task_Trade_main_1M)
	#trade_1M.start()

	Task_Trade_main_1M()

	#trade_5M = threading.Thread(target=Task_Trade_main_5M)
	#trade_5M.start()

	#trade_15M = threading.Thread(target=Task_Trade_main_15M)
	#trade_15M.start()

	#p_MACD_1.join()
	#p_MACD_2.join()

	#p_SMA.join()

	#p_TsKs.join()
	

	#trade.join()

	#trade_1M.join()

	#trade_5M.join()

	#trade_15M.join()


	#sc_1.join()
	#sc_5.join()
	#sc_15.join()



	print('End')


	
	
	

#macd_all = ind.macd(symbol_data['EURUSD']['open'],fast=10, slow=50,signal=5, verbose=True)

#macd = macd_all[macd_all.columns[0]]
#macdh = macd_all[macd_all.columns[1]]
#macds = macd_all[macd_all.columns[2]]

#macd = macd.dropna() # delete nan values


#print("macd = ",macd[macd.columns[0]])#macd
#print("macd = ",macd[macd.columns[1]])#histogram
#print("macd = ",macd[macd.columns[2]])#signal

#macd cross signal
#print("cross = ",cross_macd(macd,macds,macdh,'EURUSD'))



#ma = ind.sma(symbol_data['EURUSD']['open'],length=3)


#print(divergence(ma,macd,30,'EURUSD'))


#plt.plot(macd)
#plt.ylabel('some numbers')
#plt.show()

#plt.plot(diff_1)
#plt.ylabel('some numbers')
#plt.show()


#diff_3 = np.diff(diff_2)


#help(ind.ichimoku)
#ichi = ind.ichimoku(high=symbol_data['EURUSD']['high'],low=symbol_data['EURUSD']['low'],close=symbol_data['EURUSD']['close'],
#	tenkan=9,kijun=26,snkou=2)

#SPANA = ichi[0][ichi[0].columns[0]]
#SPANB = ichi[0][ichi[0].columns[1]]
#tenkan = ichi[0][ichi[0].columns[2]]
#kijun = ichi[0][ichi[0].columns[3]]
#chikospan = ichi[0][ichi[0].columns[4]]

#print("cross ichi signal buy: ",cross_TsKs_Buy_signal(tenkan,kijun,'EURUSD'))
#print("\n\r\r\r\r")
#print("exit_signal_TsKs: ",exit_signal_TsKs(tenkan,kijun,'EURUSD'))
#print("\n\r\r")
#print("chiko signal : ",chiko_signal(chikospan,tenkan,kijun,'EURUSD'))


#print("SPANA = ",ichi[0][ichi[0].columns[0]])#SPANA
#print("SPANB = ",ichi[0][ichi[0].columns[1]])#SPANB
#print("tenkan = ",tenkan)#tenkan_sen
#print("kiju = ",kijun)#kijun_sen


#ichi_data = ichi[0][ichi[0].columns[3]]

#print("check flat!!!!!!!!!!!!!!!!!!!!!!!")

#print(find_flat(ichi_data,"Kiju",'EURUSD'))


#values_view = find_flat(ichi_data,"Kiju",'EURUSD')
#find_spanA = find_flat(ichi[0][ichi[0].columns[0]],"SPANA",'EURUSD')
#find_spanB = find_flat(ichi[0][ichi[0].columns[1]],"SPANB",'EURUSD')
#find_kiju = find_flat(ichi[0][ichi[0].columns[2]],"kiju",'EURUSD')
#find_tenku = find_flat(ichi[0][ichi[0].columns[3]],"tenku",'EURUSD')

#three_flat = three_flat_find(ichi[0][ichi[0].columns[0]],ichi[0][ichi[0].columns[1]],ichi[0][ichi[0].columns[2]],ichi[0][ichi[0].columns[3]],'EURUSD')

#print(find_spanA )
#print("\n\r\r\r\r")
#print(find_spanB  )
#print("\n\r\r\r\r")
#print(find_kiju  )
#print("\n\r\r\r\r")
#print(len(find_tenku) )
#print("\n\r\r\r\r")

#print(three_flat)


#help(ind.rsi)

#rsi = ind.rsi(symbol_data['EURUSD']['open'],length=5)

#print("rsi = ",rsi[len(rsi)-1])
# display data
#print("\nDisplay dataframe with data")
#print(symbol_data['EURUSD']['open']) 

#help(ind.sma)

#print(ma)

#plt.plot(symbol_data['EURUSD']['open'])
#plt.ylabel('some numbers')
#plt.show()

#schedule.every(15).minutes.do(my_func)
#schedule.every(10).seconds.do(time_func)



#while True:
#    try:
#        schedule.run_pending()
#    except:
#        print('schedule wrong')
 
#
# shut down connection to the MetaTrader 5 terminal
#mt5.shutdown()