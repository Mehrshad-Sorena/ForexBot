from log_get_data import log_get_data_Genetic
from carrier import carrier_buy, carrier_sell
from basket_manager import basket_manager
from datetime import datetime
from forex_news import news
from cci import last_signal
import MetaTrader5 as mt5
from logger import logs
import pandas as pd
import numpy as np
import json
import time
import os


symbol_black_list = np.array(
	[
		'WSt30_m_i','SPX500_m_i','NQ100_m_i','GER40_m_i',
		'GER40_i','USDRUR','USDRUR_i','USDRUB','USDRUB_i',
		'USDHKD','WTI_i','BRN_i','STOXX50_i','NQ100_i',
		'NG_i','HSI50_i','CAC40_i','ASX200_i','SPX500_i',
		'NIKK225_i','IBEX35_i','FTSE100_i','RUBRUR',
		'EURDKK_i','DAX30_i','XRPUSD_i','XBNUSD_i',
		'LTCUSD_i','ETHUSD_i','BTCUSD_i','_DXY','_DJI',
		'EURTRY_i','USDTRY_i','USDDKK_i'
	])

def get_all_deta_online():
	symbol_data_5M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,1000)
	symbol_data_15M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,1200)
	symbol_data_H1,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,600)
	symbol_data_H4,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,360)
	symbol_data_D1,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,60)

	return symbol_data_5M,symbol_data_15M,symbol_data_H1,symbol_data_H4,symbol_data_D1,symbol,money


def trader(symbol_data_5M,symbol_data_15M,symbol_data_H1,symbol_data_H4,symbol_data_D1,symbol,money):
	forexnews_path = 'forexnews.json'
	time_last = time.time()

	for sym in symbol:

		if np.where(sym.name == symbol_black_list)[0].size != 0: continue

		if os.path.exists(forexnews_path):
			with open(forexnews_path, 'r') as file:
				forex_news = json.loads(file.read())

			now = datetime.now()
			for fn in forex_news.keys():
				if fn in sym.name:
					hour = forex_news.get(fn).get('hour')
					minute = forex_news.get(fn).get('min')
					impact = forex_news.get(fn).get('impact')
				else:
					impact = None
			
			if impact == 'medium' or impact == 'high':
				time_now_min = now.hour*60 + now.minute
				time_forexnews_min = hour*60 + minute
				if time_forexnews_min-30 < time_now_min < time_forexnews_min+30: continue
		else:
			news()

		signal, tp, st = last_signal(symbol_data_5M,symbol_data_15M,symbol_data_H1,symbol_data_H4,symbol_data_D1,sym.name)

		lot = basket_manager(symbols=symbol,symbol=sym.name,my_money=money,signal=signal)

		logs('================> {}'.format(sym.name))
		logs('signal =  {}'.format(signal))
		logs('tp: {}'.format(tp))
		logs('st: {}'.format(st))
		logs('lot: '.format(lot))
		logs('================================')

		if lot:
			if signal == 'buy':
				carrier_buy(symbol=sym.name,lot=lot,st=st,tp=tp,comment='cci golden cross',magic=time.time_ns())
			elif signal == 'sell':
				carrier_sell(symbol=sym.name,lot=lot,st=st,tp=tp,comment='cci golden cross',magic=time.time_ns())
			elif signal == 'no_trade':
				continue
		else:
			continue

	print(time.time()-time_last)
	return

def trader_task():
	try:
		print('****************** Start *************************')
		symbol_data_5M,symbol_data_15M,symbol_data_H1,symbol_data_H4,symbol_data_D1,symbol,money = get_all_deta_online()
		trader(symbol_data_5M,symbol_data_15M,symbol_data_H1,symbol_data_H4,symbol_data_D1,symbol,money)
		print('****************** Finish *************************')
	except Exception as ex:
		print('===== Trader ===> ',ex)
	return