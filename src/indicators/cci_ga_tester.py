from cci import genetic_algo_cci_golden_cross,one_year_golden_cross_tester, read_ga_result
from log_get_data import read_dataset_csv, get_symbols
from random import randint
import MetaTrader5 as mt5
from random import seed
import pandas as pd
import threading
import sys
import os


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
				flag_trade='buy'
				):

	try:
		genetic_algo_cci_golden_cross(
									symbol_data_5M=symbol_data_5M,
									symbol_data_15M=symbol_data_15M,
									dataset_1H=symbol_data_1H,
									dataset_4H=symbol_data_4H,
									symbol=symbol,
									num_turn=num_turn,
									max_score_ga_buy=max_score_ga_buy,
									max_score_ga_sell=max_score_ga_sell,
									flag_trade=flag_trade
									)
		pass
	except Exception as ex:
		print('getting error GA Runner: ', ex)


def ga_optimizer_buy():

	print('===========> ga optimizer buy')
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
		while learn_counter < 4:
			low_distance = randint(0, 90000)
			high_distance = randint(0, 90000)
			if high_distance < low_distance: continue
			if high_distance - low_distance != 9000: continue
			print('high_distance = ',high_distance)
			print('low_distance = ',low_distance)

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

			buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'
			
			print('*************> ',sym.name)

			if not os.path.exists(buy_path):
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=2000,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='buy'
						)
			else:
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=200,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='buy'
						)

			print('======= learn_counter buy ====> ',learn_counter)

			learn_counter += 1

def ga_tester_buy():

	print('===========> ga tester buy')

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

		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'

		if os.path.exists(buy_path):
			print('*********** Optimizer Buy *')

			ga_result_buy, _ = read_ga_result(symbol=sym.name)

			if 'permit' not in ga_result_buy.columns:


				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=9000,
																										num_15M=1,
																										num_1H=8000,
																										num_4H=1
																										)

				one_year_golden_cross_tester(
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
					ga_optimizer_buy(my_sym=my_sym)
					ga_tester_buy(my_sym=my_sym)


def ga_optimizer_sell():

	print('===========> ga optimizer sell')

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
		while learn_counter < 4:
			low_distance = randint(0, 90000)
			high_distance = randint(0, 90000)
			if high_distance < low_distance: continue
			if high_distance - low_distance != 9000: continue
			print('high_distance = ',high_distance)
			print('low_distance = ',low_distance)

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
			
			print('*************> ',sym.name)

			if not os.path.exists(sell_path):
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=2000,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='sell'
						)
			else:
				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=200,
						max_score_ga_buy=10,
						max_score_ga_sell=10,
						flag_trade='sell'
						)

			print('======= learn_counter sell ====> ',learn_counter)

			learn_counter += 1

def ga_tester_sell():

	print('===========> ga tester sell')

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

		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		if os.path.exists(sell_path):
			print('*********** Optimizer Buy *')

			_, ga_result_sell = read_ga_result(symbol=sym.name)

			if 'permit' not in ga_result_sell.columns:


				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=9000,
																										num_15M=1,
																										num_1H=8000,
																										num_4H=1
																										)

				one_year_golden_cross_tester(
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
					ga_optimizer_sell(my_sym=my_sym)
					ga_tester_sell(my_sym=my_sym)

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


my_sym = 'AUDUSD_i'

Task_optimizer()

Task_tester()