from macd import genetic_algo_div_macd, read_ga_result
from log_get_data import read_dataset_csv, get_symbols, log_get_data_Genetic
from datetime import datetime
from random import randint
import MetaTrader5 as mt5
from random import seed
import pandas as pd
import numpy as np
import threading
import logging
import sys
import os
import warnings
warnings.filterwarnings("ignore")


#ga_runner()
#dataset_spliter()
#ga_optimizer_buy()
#ga_tester_buy()
#learning_buy()
#ga_optimizer_sell()
#ga_tester_sell()
#learning_sell()

#**************************************** Logger *****************
"""
now = datetime.now()
log_path = 'log/cci/golden_cross_zero/optimizer------.log',now.year, now.month, now.day, now.hour, now.minute, now.second)
log_level = 'info'
logger = logging.getLogger()

if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

if log_level == 'info':
    logger.setLevel(logging.INFO)
elif log_level == 'warning':
    logger.setLevel(logging.WARNING)
elif log_level == 'debug':
    logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
formatter = logging.Formatter('%(asctime)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def print(message):
    logger.info(message)
"""

#/////////////////////////////////////////////////////////////////////////////////////////////////////////


def dataset_spliter(
					symbol,
					dataset_5M,
					dataset_1H,
					spliter_5M_end,
					spliter_5M_first
					):
	symbol_data_5M = pd.DataFrame()
	symbol_data_1H = pd.DataFrame()

	symbol_data_5M = {
						symbol: dataset_5M[symbol].copy()
						}

	symbol_data_5M[symbol]['low'] = dataset_5M[symbol]['low'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['high'] = dataset_5M[symbol]['high'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['close'] = dataset_5M[symbol]['close'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['open'] = dataset_5M[symbol]['open'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HL/2'] = dataset_5M[symbol]['HL/2'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HLC/3'] = dataset_5M[symbol]['HLC/3'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HLCC/4'] = dataset_5M[symbol]['HLCC/4'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['OHLC/4'] = dataset_5M[symbol]['OHLC/4'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['volume'] = dataset_5M[symbol]['volume'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['time'] = dataset_5M[symbol]['time'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)

	loc_1H = 0
	location_1H = -1
	for ti in dataset_1H[symbol]['time']:
		#print('1H===> ',ti.year)
		if (
			ti.year == symbol_data_5M[symbol]['time'].iloc[-1].year and
			ti.month == symbol_data_5M[symbol]['time'].iloc[-1].month and
			ti.day == symbol_data_5M[symbol]['time'].iloc[-1].day and
			ti.hour == symbol_data_5M[symbol]['time'].iloc[-1].hour
			):
			location_1H = loc_1H

		loc_1H += 1

	symbol_data_1H = {
						symbol: dataset_1H[symbol].copy()
						}

	symbol_data_1H[symbol]['low'] = dataset_1H[symbol]['low'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['high'] = dataset_1H[symbol]['high'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['close'] = dataset_1H[symbol]['close'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['open'] = dataset_1H[symbol]['open'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HL/2'] = dataset_1H[symbol]['HL/2'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HLC/3'] = dataset_1H[symbol]['HLC/3'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HLCC/4'] = dataset_1H[symbol]['HLCC/4'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['OHLC/4'] = dataset_1H[symbol]['OHLC/4'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['volume'] = dataset_1H[symbol]['volume'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['time'] = dataset_1H[symbol]['time'][0:location_1H].reset_index(drop=True)

	return symbol_data_5M, symbol_data_1H

def ga_runner(
				symbol_data_5M,
				symbol_data_15M,
				symbol_data_1H,
				symbol_data_4H,
				symbol,
				num_turn,
				max_score_ga_buy,
				max_score_ga_sell,
				primary_doing,
				secondry_doing,
				flag_trade='buy'
				):

	try:
		genetic_algo_div_macd(
								symbol_data_5M=symbol_data_5M,
								symbol_data_15M=symbol_data_15M,
								dataset_1H=symbol_data_1H,
								dataset_4H=symbol_data_4H,
								symbol=symbol,
								num_turn=num_turn,
								max_score_ga_buy=max_score_ga_buy,
								max_score_ga_sell=max_score_ga_sell,
								flag_trade=flag_trade,
								primary_doing=primary_doing,
								secondry_doing=secondry_doing
								)
		pass
	except Exception as ex:
		print('getting error GA Runner: ', ex)


def ga_optimizer_buy():

	print('================================> ga optimizer buy')

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			#sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			sym.name == 'EURCAD_i' or
			sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			sym.name == 'EURJPY_i' or
			sym.name == 'GBPAUD_i' or
			sym.name == 'GBPCAD_i' or
			sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			sym.name == 'USDJPY_i' or
			sym.name == 'USDCAD_i'
			#sym.name == 'XAUUSD_i'
			): continue

		#if sym.name != my_sym: continue



		learn_counter = 0
		while learn_counter < 1:


			low_distance = randint((learn_counter*16800)+6000, ((learn_counter*16800) + 16800))
			high_distance = randint((learn_counter*16800), ((learn_counter*12850) + 16800))
			if high_distance < low_distance: continue
			if high_distance - low_distance != 10000: continue
			print('===================== high_distance buy ==> ',high_distance)
			print('===================== low_distance buy ===> ',low_distance)

			print('=================== my_sym optimizer buy => ',sym.name)

			print('======================== AI Buy ==========> ',learn_counter)
			

			dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																								sym=sym.name,
																								num_5M=99000,
																								num_15M=1,
																								num_1H=8250,
																								num_4H=1
																								)
			symbol_data_5M,symbol_data_1H = dataset_spliter(
														symbol=sym.name,
														dataset_5M=dataset_5M,
														dataset_1H=dataset_1H,
														spliter_5M_end=90000,
														spliter_5M_first=6000
														)

			print('======================== len 5M ==========> ',len(symbol_data_5M[sym.name]['open']))
			print('======================== len 1H ==========> ',len(symbol_data_1H[sym.name]['open']))
			print()

			buy_path_primary = 'GA/MACD/primary/buy/'+sym.name+'.csv'
			
			#print('*************> ',sym.name)

			if not os.path.exists(buy_path_primary):
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=400,
						max_score_ga_buy=600,
						max_score_ga_sell=600,
						flag_trade='buy',
						primary_doing=True,
						secondry_doing=False
						)
			else:
				learn_counter = 2
				if learn_counter > 1: 
					num_turn = 120
				else:
					num_turn = 200
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=num_turn,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='buy',
						primary_doing=True,
						secondry_doing=False
						)

			#print('======= learn_counter buy ====> ',learn_counter)

			learn_counter += 1

def ga_tester_buy():

	print('================================> ga tester buy')

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			#sym.name == 'EURCAD_i' or
			#sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			#sym.name == 'EURJPY_i' or
			#sym.name == 'GBPAUD_i' or
			#sym.name == 'GBPCAD_i' or
			#sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			#sym.name == 'USDJPY_i' or
			#sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		if sym.name != my_sym: continue
		print('======================== my_sym tester buy ====> ',my_sym)

		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'

		if os.path.exists(buy_path):
			print('*********** Tester Buy *')

			ga_result_buy, _ = read_ga_result(symbol=sym.name)

			if 'permit' not in ga_result_buy.columns:


				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=9000,
																										num_15M=1,
																										num_1H=8000,
																										num_4H=1
																										)
				golden_cross_tester_for_permit(
												dataset=symbol_data_5M,
												dataset_15M=symbol_data_15M,
												symbol_data_1H=symbol_data_1H,
												symbol_data_4H=symbol_data_4H,
												symbol=sym.name,
												flag_trade='buy'
												)

			ga_result_buy, _ = read_ga_result(symbol=sym.name)
			if 'permit' in ga_result_buy.columns:
				while ga_result_buy['permit'][0] != True:
					ga_optimizer_buy()
					ga_tester_buy()


def ga_optimizer_sell():

	print('================================> ga optimizer sell')

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			#sym.name == 'EURCAD_i' or
			#sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			#sym.name == 'EURJPY_i' or
			#sym.name == 'GBPAUD_i' or
			#sym.name == 'GBPCAD_i' or
			#sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			#sym.name == 'USDJPY_i' or
			#sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		if sym.name != my_sym: continue

		learn_counter = 0
		while learn_counter < 1:

			low_distance = randint((learn_counter*12850), ((learn_counter*12850) + 12850))
			high_distance = randint((learn_counter*12850), ((learn_counter*12850) + 12850))
			if high_distance < low_distance: continue
			if high_distance - low_distance != 10000: continue
			print('====================== high_distance sell ==> ',high_distance)
			print('====================== low_distance sell ===> ',low_distance)

			print('================= my_sym optimizer sell ====> ',my_sym)

			print('========================= AI Sell ==========> ',learn_counter)
			print()

			dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																								sym=sym.name,
																								num_5M=99000,
																								num_15M=1,
																								num_1H=8250,
																								num_4H=1
																								)
			symbol_data_5M,symbol_data_1H = dataset_spliter(
														symbol=sym.name,
														dataset_5M=dataset_5M,
														dataset_1H=dataset_1H,
														spliter_5M_end=high_distance,
														spliter_5M_first=low_distance
														)

			sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'
			
			#print('*************> ',sym.name)

			if not os.path.exists(sell_path):
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=8000,
						max_score_ga_buy=70,
						max_score_ga_sell=70,
						flag_trade='sell'
						)
			else:
				if learn_counter > 1: 
					num_turn = 40
				else:
					num_turn = 200
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=num_turn,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='sell'
						)


			learn_counter += 1

def ga_tester_sell():

	print('================================> ga tester sell')

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			#sym.name == 'EURCAD_i' or
			#sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			#sym.name == 'EURJPY_i' or
			#sym.name == 'GBPAUD_i' or
			#sym.name == 'GBPCAD_i' or
			#sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			#sym.name == 'USDJPY_i' or
			#sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		if sym.name != my_sym: continue

		print('======================= my_sym tester sell ====> ',my_sym)

		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		if os.path.exists(sell_path):
			print('=============================> tester Permit Sell *')

			_, ga_result_sell = read_ga_result(symbol=sym.name)

			if 'permit' not in ga_result_sell.columns:


				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=9000,
																										num_15M=1,
																										num_1H=8000,
																										num_4H=1
																										)
				golden_cross_tester_for_permit(
												dataset=symbol_data_5M,
												dataset_15M=symbol_data_15M,
												symbol_data_1H=symbol_data_1H,
												symbol_data_4H=symbol_data_4H,
												symbol=sym.name,
												flag_trade='sell'
												)

			_, ga_result_sell = read_ga_result(symbol=sym.name)
			if 'permit' in ga_result_sell.columns:
				while ga_result_sell['permit'][0] != True:
					ga_optimizer_sell()
					ga_tester_sell()

def learning_buy():

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			#sym.name == 'EURCAD_i' or
			#sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			#sym.name == 'EURJPY_i' or
			#sym.name == 'GBPAUD_i' or
			#sym.name == 'GBPCAD_i' or
			#sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			#sym.name == 'USDJPY_i' or
			#sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		if sym.name != my_sym: continue
		dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=1,
																									num_1H=8250,
																									num_4H=1
																									)

		symbol_data_5M,symbol_data_1H = dataset_spliter(
														symbol=sym.name,
														dataset_5M=dataset_5M,
														dataset_1H=dataset_1H,
														spliter_5M_end=99000,
														spliter_5M_first=6000
														)


		#print('getting....')
		#symbol_data_5M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,99000)
		#print('get 5M')
		#mem_data = pd.DataFrame()
		#mem_data = mem_data.append(symbol_data_5M,ignore_index=True)
		#print(mem_data)
		#print(mem_data.info(memory_usage='deep'))

		#symbol_data_1H,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,8250)
		#print('get 1H')
		#mem_data = pd.DataFrame()
		#mem_data = mem_data.append(symbol_data_1H,ignore_index=True)
		#print(mem_data)
		#print(mem_data.info(memory_usage='deep'))

		max_learning_turn = 100
		learn_out = pd.DataFrame(np.zeros(max_learning_turn))
		learn_out['score'] = np.nan
		learn_out['value_min_upper_cci_pr'] = np.nan
		learn_out['power_pr_high'] = np.nan
		learn_out['power_pr_low'] = np.nan
		learn_out['max_st'] = np.nan
		learn_out['max_tp'] = np.nan
		learn_out['max_st_now'] = np.nan
		learn_out['max_tp_now'] = np.nan

		print('5M = ',len(symbol_data_5M[sym.name]['open']))
		print('1H = ',len(symbol_data_1H[sym.name]['open']))

		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'

		if os.path.exists(buy_path):
			print('*********** Tester Buy *')

			ga_result_buy, _ = read_ga_result(symbol=sym.name)

		out_buy,_ = one_year_golden_cross_tester(
									dataset=symbol_data_5M,
									dataset_15M=symbol_data_15M,
									symbol_data_1H=symbol_data_1H,
									symbol_data_4H=symbol_data_4H,
									symbol=sym.name,
									flag_trade='buy',
									alfa=0.99,
									max_st=ga_result_buy['max_st'][0],
									max_tp=ga_result_buy['max_tp'][0],
									permit_flag=False
									)

		learn_out['score'][0] = out_buy['score_pr'][0]
		learn_out['value_min_upper_cci_pr'][0] = out_buy['value_min_upper_cci_pr'][0]
		learn_out['power_pr_high'][0] = out_buy['power_pr_high'][0]
		learn_out['power_pr_low'][0] = out_buy['power_pr_low'][0]
		learn_out['max_st'][0] = out_buy['max_st'][0]
		learn_out['max_tp'][0] = out_buy['max_tp'][0]
		learn_out['max_st_now'][0] = out_buy['max_st'][0]
		learn_out['max_tp_now'][0] = out_buy['max_tp'][0]
		#learn_out['max_st_pr'][0] = out_buy['max_st_pr'][0]
		#learn_out['max_tp_pr'][0] = out_buy['max_tp_pr'][0]

		learning_turn = 1
		alfa = 0.99
		max_learn_turn = 0
		while learning_turn < max_learning_turn:
			print('============================= Leraning Turn ======> ',learning_turn)
			print('5M = ',len(symbol_data_5M[sym.name]['open']))
			print('1H = ',len(symbol_data_1H[sym.name]['open']))

			if learn_out['max_st'][learning_turn-1] == 0: learn_out['max_st'][learning_turn-1] = randint(30,120)/100
			if learn_out['max_tp'][learning_turn-1] == 0: learn_out['max_tp'][learning_turn-1] = randint(30,120)/100

			print('max_st = ',learn_out['max_st'][learning_turn-1])
			print('max_tp = ',learn_out['max_tp'][learning_turn-1])

			out_buy,_ = one_year_golden_cross_tester(
									dataset=symbol_data_5M,
									dataset_15M=symbol_data_15M,
									symbol_data_1H=symbol_data_1H,
									symbol_data_4H=symbol_data_4H,
									symbol=sym.name,
									flag_trade='buy',
									alfa=alfa,
									max_st=learn_out['max_st'][learning_turn-1],
									max_tp=learn_out['max_tp'][learning_turn-1],
									permit_flag=False
									)
			
			learn_out['score'][learning_turn] = out_buy['score_pr'][0]
			learn_out['value_min_upper_cci_pr'][learning_turn] = out_buy['value_min_upper_cci_pr'][0]
			learn_out['power_pr_high'][learning_turn] = out_buy['power_pr_high'][0]
			learn_out['power_pr_low'][learning_turn] = out_buy['power_pr_low'][0]
			learn_out['max_st'][learning_turn] = out_buy['max_st'][0]
			learn_out['max_tp'][learning_turn] = out_buy['max_tp'][0]
			learn_out['max_st_now'][learning_turn] = learn_out['max_st'][learning_turn-1]
			learn_out['max_tp_now'][learning_turn] = learn_out['max_tp'][learning_turn-1]
			learning_turn += 1

			buy_path = "Genetic_cci_output_buy/" + 'AUDUSD_i' + '.csv'

			if os.path.exists(buy_path):
				ga_result_buy, _ = read_ga_result(symbol=sym.name)

			if out_buy['score_pr'][0] <= ga_result_buy['score_pr'][0]:
				alfa = randint(40, 99)/100
				print('alfa = ',alfa)

				if out_buy['score_pr'][0] < ga_result_buy['score_pr'][0] * 0.5:
					learn_out['max_st'][learning_turn-1] = randint(30,120)/100
					learn_out['max_tp'][learning_turn-1] = randint(30,120)/100
				#max_learn_turn += 1
				continue
			if max_learn_turn >= max_learning_turn: break

			max_learn_turn += 1

		max_score_learn = np.max(learn_out['score'].dropna())
		max_score_learn_index = np.where((learn_out['score']==max_score_learn))[0]

		print()
		print('=========================== learn_out => ',learn_out)
		print('===================== max_score_learn => ',max_score_learn)
		print('=============== max_score_learn_index => ',max_score_learn_index)
		print()

		buy_path = "Genetic_cci_output_buy/" + 'AUDUSD_i' + '.csv'

		if os.path.exists(buy_path):
			ga_result_buy, _ = read_ga_result(symbol=sym.name)

		ga_result_buy['score_learn'] = learn_out['score'][max_score_learn_index]
		ga_result_buy['value_min_upper_cci_pr'] = learn_out['value_min_upper_cci_pr'][max_score_learn_index]
		ga_result_buy['power_pr_high'] = learn_out['power_pr_high'][max_score_learn_index]
		ga_result_buy['power_pr_low'] = learn_out['power_pr_low'][max_score_learn_index]
		ga_result_buy['max_st'][0] = learn_out['max_st_now'][max_score_learn_index]
		ga_result_buy['max_tp'][0] = learn_out['max_tp_now'][max_score_learn_index]
		ga_result_buy['score_pr'][0] = learn_out['score'][max_score_learn_index]

		if os.path.exists(buy_path):
			os.remove(buy_path)

		ga_result_buy.to_csv(buy_path)

def learning_sell():

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == my_sym or
			#sym.name == 'CADJPY_i' or
			#sym.name == 'EURAUD_i' or
			#sym.name == 'EURCAD_i' or
			#sym.name == 'EURCHF_i' or
			#sym.name == 'EURGBP_i' or
			#sym.name == 'EURUSD_i' or
			#sym.name == 'EURJPY_i' or
			#sym.name == 'GBPAUD_i' or
			#sym.name == 'GBPCAD_i' or
			#sym.name == 'GBPJPY_i' or
			#sym.name == 'GBPUSD_i' or
			#sym.name == 'USDJPY_i' or
			#sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		if sym.name != my_sym: continue
		dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=1,
																									num_1H=8250,
																									num_4H=1
																									)

		symbol_data_5M,symbol_data_1H = dataset_spliter(
														symbol=sym.name,
														dataset_5M=dataset_5M,
														dataset_1H=dataset_1H,
														spliter_5M_end=90000,
														spliter_5M_first=0
														)


		max_learning_turn = 50
		learn_out = pd.DataFrame(np.zeros(max_learning_turn))
		learn_out['score'] = np.nan
		learn_out['value_max_lower_cci_pr'] = np.nan
		learn_out['power_pr_high'] = np.nan
		learn_out['power_pr_low'] = np.nan
		learn_out['max_st'] = np.nan
		learn_out['max_tp'] = np.nan

		_, out_sell = one_year_golden_cross_tester(
									dataset=symbol_data_5M,
									dataset_15M=symbol_data_15M,
									symbol_data_1H=symbol_data_1H,
									symbol_data_4H=symbol_data_4H,
									symbol=sym.name,
									flag_trade='sell',
									max_st=1,
									max_tp=1,
									permit_flag=False
									)
		learn_out['score'][0] = out_sell['score_pr'][0]
		learn_out['value_max_lower_cci_pr'][0] = out_sell['value_max_lower_cci_pr'][0]
		learn_out['power_pr_high'][0] = out_sell['power_pr_high'][0]
		learn_out['power_pr_low'][0] = out_sell['power_pr_low'][0]
		learn_out['max_st'][0] = out_sell['max_st'][0]
		learn_out['max_tp'][0] = out_sell['max_tp'][0]

		learning_turn = 1
		alfa = 0.1
		max_learn_turn = 0
		while learning_turn < max_learning_turn:
			print('============================ Leraning Turn ======> ',learning_turn)
			_, out_sell = one_year_golden_cross_tester(
									dataset=symbol_data_5M,
									dataset_15M=symbol_data_15M,
									symbol_data_1H=symbol_data_1H,
									symbol_data_4H=symbol_data_4H,
									symbol=sym.name,
									flag_trade='sell',
									alfa=alfa,
									max_st=learn_out['max_st'][learning_turn-1],
									max_tp=learn_out['max_tp'][learning_turn-1],
									permit_flag=False
									)
			if out_sell['score_pr'][0] > learn_out['score'][learning_turn-1]:
				learn_out['score'][learning_turn] = out_sell['score_pr'][0]
				learn_out['value_max_lower_cci_pr'][learning_turn] = out_sell['value_max_lower_cci_pr'][0]
				learn_out['power_pr_high'][learning_turn] = out_sell['power_pr_high'][0]
				learn_out['power_pr_low'][learning_turn] = out_sell['power_pr_low'][0]
				learn_out['max_st'][learning_turn] = out_sell['max_st'][0]
				learn_out['max_tp'][learning_turn] = out_sell['max_tp'][0]
				learning_turn += 1
			else:
				alfa = randint(0, 50)/100
				max_learn_turn += 1
				continue

			if max_learn_turn >= 50: break

			max_learn_turn += 1

		max_score_learn = np.max(learn_out['score'].dropna())
		max_score_learn_index = np.where((learn_out['score']==max_score_learn))[0]

		print()
		print('====================== max_score_learn => ',max_score_learn)
		print('================ max_score_learn_index => ',max_score_learn_index)
		print('============================ learn_out => ',learn_out)
		print()

		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		if os.path.exists(sell_path):
			_, ga_result_sell = read_ga_result(symbol=sym.name)

		ga_result_sell['score_learn'] = learn_out['score'][max_score_learn_index]
		ga_result_sell['value_max_lower_cci_pr'] = learn_out['value_max_lower_cci_pr'][max_score_learn_index]
		ga_result_sell['power_pr_high'] = learn_out['power_pr_high'][max_score_learn_index]
		ga_result_sell['power_pr_low'] = learn_out['power_pr_low'][max_score_learn_index]
		ga_result_sell['max_st'] = learn_out['max_st'][max_score_learn_index]
		ga_result_sell['max_tp'] = learn_out['max_tp'][max_score_learn_index]

		if os.path.exists(sell_path):
			os.remove(sell_path)

		ga_result_sell.to_csv(sell_path)

def Task_optimizer():
	job_thread_buy = threading.Thread(target=ga_optimizer_buy)
	job_thread_buy.start()
	print()
	print('optimizer job_thread_buy ===> optimizer job_thread_buy runed')

	job_thread_sell = threading.Thread(target=ga_optimizer_sell)
	job_thread_sell.start()
	print()
	print('optimizer job_thread_sell ===> optimizer job_thread_sell runed')

	
	job_thread_buy.join()
	job_thread_sell.join()

def Task_tester():
	job_thread_buy = threading.Thread(target=ga_tester_buy)
	job_thread_buy.start()
	print()
	print('tester job_thread_buy ===> tester job_thread_buy runed')

	job_thread_sell = threading.Thread(target=ga_tester_sell)
	job_thread_sell.start()
	print()
	print('tester job_thread_sell ===> tester job_thread_sell runed')

	
	job_thread_buy.join()
	job_thread_sell.join()


my_sym = 'GBPUSD_i'

#learning_buy()
#ga_tester_buy()
ga_optimizer_buy()
#learning_buy()
#ga_tester_buy()

#ga_optimizer_sell()
#learning_sell()
#ga_tester_sell()


#Task_optimizer()

#Task_tester()
#ga_optimizer_buy()