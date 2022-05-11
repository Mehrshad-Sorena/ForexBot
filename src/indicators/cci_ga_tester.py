from cci import genetic_algo_cci_golden_cross,one_year_golden_cross_tester, read_ga_result
from log_get_data import read_dataset_csv, get_symbols
import MetaTrader5 as mt5
import pandas as pd
import os
import sys

def dataset_spliter(
					symbol,
					dataset_5M,
					dataset_1H,
					spliter_5M
					):
	symbol_data_5M = pd.DataFrame()
	symbol_data_1H = pd.DataFrame()

	symbol_data_5M = {
						symbol: dataset_5M[symbol].copy()
						}

	symbol_data_5M[symbol]['low'] = dataset_5M[symbol]['low'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['high'] = dataset_5M[symbol]['high'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['close'] = dataset_5M[symbol]['close'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['open'] = dataset_5M[symbol]['open'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['HL/2'] = dataset_5M[symbol]['HL/2'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['HLC/3'] = dataset_5M[symbol]['HLC/3'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['HLCC/4'] = dataset_5M[symbol]['HLCC/4'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['OHLC/4'] = dataset_5M[symbol]['OHLC/4'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['volume'] = dataset_5M[symbol]['volume'][0:spliter_5M].reset_index(drop=True)
	symbol_data_5M[symbol]['time'] = dataset_5M[symbol]['time'][0:spliter_5M].reset_index(drop=True)

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


def ga_optimizer():

	symbols,my_money = get_symbols(mt5.TIMEFRAME_M1)

	for sym in symbols:

		if not (
			#sym.name == 'AUDCAD_i' or
			#sym.name == 'AUDCHF_i' or
			sym.name == 'AUDUSD_i' or
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

		if sym.name != 'AUDUSD_i': continue

		dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																								sym=sym.name,
																								num_5M=26000,
																								num_15M=1,
																								num_1H=8000,
																								num_4H=1
																								)

		
		symbol_data_5M,symbol_data_1H = dataset_spliter(
														symbol=sym.name,
														dataset_5M=dataset_5M,
														dataset_1H=dataset_1H,
														spliter_5M=20000
														)

		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'
		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		print('*************> ',sym.name)

		if not os.path.exists(buy_path):
			ga_runner(
					symbol_data_5M=symbol_data_5M,
					symbol_data_15M=symbol_data_15M,
					symbol_data_1H=symbol_data_1H,
					symbol_data_4H=symbol_data_4H,
					symbol=sym.name,
					num_turn=2000,
					max_score_ga_buy=73,
					max_score_ga_sell=73,
					flag_trade='buy'
					)
	
		if not os.path.exists(sell_path):
			ga_runner(
					symbol_data_5M=symbol_data_5M,
					symbol_data_15M=symbol_data_15M,
					symbol_data_1H=symbol_data_1H,
					symbol_data_4H=symbol_data_4H,
					symbol=sym.name,
					num_turn=2000,
					max_score_ga_buy=73,
					max_score_ga_sell=73,
					flag_trade='sell'
					)

		if os.path.exists(buy_path):
			print('*********** Optimizer Buy *')

			ga_result_buy, _ = read_ga_result(symbol=sym.name)

			if 'permit' not in ga_result_buy.columns:


				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=6000,
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

			while ga_result_buy['permit'][0] != True:

				dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=26000,
																									num_15M=1,
																									num_1H=8250,
																									num_4H=1
																									)

				symbol_data_5M,symbol_data_1H = dataset_spliter(
																symbol=sym.name,
																dataset_5M=dataset_5M,
																dataset_1H=dataset_1H,
																spliter_5M=20000
																)

				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=500,
						max_score_ga_buy=2,
						max_score_ga_sell=2,
						flag_trade='buy'
						)

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=6000,
																									num_15M=1,
																									num_1H=8250,
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


		if os.path.exists(sell_path):
			print('*********** Optimizer Sell *')

			_, ga_result_sell = read_ga_result(symbol=sym.name)

			if 'permit' in ga_result_sell.columns:
				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																										sym=sym.name,
																										num_5M=6000,
																										num_15M=1,
																										num_1H=8250,
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

			while ga_result_sell['permit'][0] != True:

				dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=26000,
																									num_15M=1,
																									num_1H=8000,
																									num_4H=1
																									)

				symbol_data_5M,symbol_data_1H = dataset_spliter(
																symbol=sym.name,
																dataset_5M=dataset_5M,
																dataset_1H=dataset_1H,
																spliter_5M=20000
																)

				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=500,
						max_score_ga_buy=2,
						max_score_ga_sell=2,
						flag_trade='sell'
						)

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=6000,
																									num_15M=1,
																									num_1H=8250,
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


ga_optimizer()