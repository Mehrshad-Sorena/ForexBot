from Mt5_LoginGetData import LoginGetData as getdata
from carrier import carrier_buy, carrier_sell
from macd_BascketManager import basket_manager_macd_div
from datetime import datetime
from forex_news import news
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import json
import time
import os

from macd_Parameters import Parameters as MACDParameters
from macd_Config import Config as MACDConfig
from macd_MACD import MACD




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

def get_all_deta_online(symbol, account_name):

	loging = getdata()
	loging.account_name = account_name
	loging.initilizer()
	loging.login()

	symbol_data_5M = loging.getone(timeframe = '5M', number = 18000, symbol = symbol)
	symbol_data_1H = loging.getone(timeframe = '1H', number = 2000, symbol = symbol)

	symbol = loging.get_symbols()

	money = loging.get_balance()

	return symbol_data_5M, symbol_data_1H, symbol, money


def trader_macd_div(
					symbol_data_5M,
					symbol_data_1H,
					symbol,
					money,
					account_name
					):
	forexnews_path = 'forexnews.json'
	time_last = time.time()

	for sym in symbol:

		#if np.where(sym.name == symbol_black_list)[0].size != 0: continue

		if not (
			# sym.name == 'AUDCAD_i' or
			# sym.name == 'AUDCHF_i' or
			# sym.name == 'AUDUSD_i' or
			# sym.name == 'CADJPY_i' or
			# sym.name == 'EURAUD_i' or
			# sym.name == 'EURCAD_i' or
			# sym.name == 'EURCHF_i' or
			# sym.name == 'EURGBP_i' or
			# sym.name == 'EURUSD_i' or
			# sym.name == 'EURJPY_i' or
			# sym.name == 'GBPAUD_i' or
			# sym.name == 'GBPCAD_i' or
			# sym.name == 'GBPJPY_i' or
			# sym.name == 'GBPUSD_i' or
			# sym.name == 'USDJPY_i' or
			# sym.name == 'USDCAD_i' or
			# sym.name == 'CAC40_i' or
			# sym.name == 'FTSE100_i' or
			# sym.name == 'GER40_i' or
			# sym.name == 'WSt30_m_i' or
			# sym.name == 'STOXX50_i' or
			# sym.name == 'CHNA50_m_i' or
			# sym.name == 'HSI50_i' or
			# sym.name == 'NQ100_i' or
			# sym.name == 'LTCUSD_i' or
			# sym.name == 'XRPUSD_i' or
			# sym.name == 'BTCUSD_i' or
			#sym.name == 'ETHUSD_i'
			sym.name == 'XAUUSD_i'
			): continue

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


		macd_parameters = MACDParameters()
		macd_config = MACDConfig()

		macd_parameters.elements['dataset_5M'] = symbol_data_5M
		macd_parameters.elements['dataset_1H'] = symbol_data_1H
		macd_parameters.elements['symbol'] = sym.name

		macd = MACD(parameters = macd_parameters, config = macd_config)
		signal, tp, st = macd.LastSignal(
										dataset_5M = macd_parameters.elements['dataset_5M'], 
										dataset_1H = macd_parameters.elements['dataset_1H'], 
										symbol = sym.name,
										)

		lot = basket_manager_macd_div(symbols=symbol,symbol=sym.name,my_money=money,signal=signal, account_name = account_name)

		if lot > 0.09: lot = 0.09
		if 0 < lot < 0.01: lot = 0.01

		if (
			sym.name == 'CAC40_i' or
			sym.name == 'CHNA50_m_i' or
			sym.name == 'FTSE100_i' or
			sym.name == 'GER40_i' or
			sym.name == 'HSI50_i' or
			sym.name == 'NQ100_i' or
			sym.name == 'STOXX50_i' or
			sym.name == 'WSt30_m_i'
			):
			
			lot = lot * 0#10 
			lot = float("{:.1f}".format((lot)))

		print('================> ',sym.name)
		print('signal =  ',signal)
		print('tp: ',tp)
		print('st: ',st)
		print('lot: ',lot)
		print('================================')

		if lot:
			if (
				signal == 'buy_primary' or
				signal == 'buy_secondry'
				):
				carrier_buy(symbol=sym.name,lot=lot,st=st,tp=tp,comment='macd div'+signal,magic=time.time_ns())
			elif (
				signal == 'sell_primary' or
				signal == 'sell_secondry'
				):
				carrier_sell(symbol=sym.name,lot=lot,st=st,tp=tp,comment='macd div'+signal,magic=time.time_ns())
			elif signal == 'no_trade':
				continue
		else:
			continue
	return

def trader_task_macd_div(symbol, account_name):
	try:
		print('****************** Start *************************')
		symbol_data_5M,symbol_data_1H,symbol,money = get_all_deta_online(symbol = symbol, account_name = account_name)
		trader_macd_div(
						symbol_data_5M = symbol_data_5M,
						symbol_data_1H = symbol_data_1H,
						symbol = symbol,
						money = money,
						account_name = account_name
						)
		print('****************** Finish *************************')
	except Exception as ex:
		print('===== Trader Error ===> ',ex)
	return