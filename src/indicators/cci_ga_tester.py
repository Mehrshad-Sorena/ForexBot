from cci import genetic_algo_cci_golden_cross,one_year_golden_cross_tester, read_ga_result
from log_get_data import read_dataset_csv, get_symbols
import MetaTrader5 as mt5
import os
import sys


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
			sym.name == 'AUDCAD_i' or
			sym.name == 'AUDCHF_i' or
			sym.name == 'AUDUSD_i' or
			sym.name == 'CADJPY_i' or
			sym.name == 'EURAUD_i' or
			sym.name == 'EURCAD_i' or
			sym.name == 'EURCHF_i' or
			sym.name == 'EURGBP_i' or
			sym.name == 'EURUSD_i' or
			sym.name == 'EURJPY_i' or
			sym.name == 'GBPAUD_i' or
			sym.name == 'GBPCAD_i' or
			sym.name == 'GBPJPY_i' or
			sym.name == 'GBPUSD_i' or
			sym.name == 'USDJPY_i' or
			sym.name == 'USDCAD_i' or
			sym.name == 'XAUUSD_i'
			): continue

		symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																								sym=sym.name,
																								num_5M=12000,
																								num_15M=4000,
																								num_1H=1,
																								num_4H=1
																								)

		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'
		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		if not os.path.exists(buy_path):
			ga_runner(
					symbol_data_5M=symbol_data_5M,
					symbol_data_15M=symbol_data_15M,
					symbol_data_1H=symbol_data_1H,
					symbol_data_4H=symbol_data_4H,
					symbol=sym.name,
					num_turn=200,
					max_score_ga_buy=2,
					max_score_ga_sell=2,
					flag_trade='buy'
					)
	
		if not os.path.exists(sell_path):
			ga_runner(
					symbol_data_5M=symbol_data_5M,
					symbol_data_15M=symbol_data_15M,
					symbol_data_1H=symbol_data_1H,
					symbol_data_4H=symbol_data_4H,
					symbol=sym.name,
					num_turn=200,
					max_score_ga_buy=2,
					max_score_ga_sell=2,
					flag_trade='sell'
					)

		if os.path.exists(buy_path):
			print('*********** Optimizer Buy *')

			symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=33000,
																									num_1H=1,
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

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=36000,
																									num_15M=12000,
																									num_1H=1,
																									num_4H=1
																									)

				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=40,
						max_score_ga_buy=2,
						max_score_ga_sell=2,
						flag_trade='buy'
						)

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=33000,
																									num_1H=1,
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

			symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=33000,
																									num_1H=1,
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

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=36000,
																									num_15M=12000,
																									num_1H=1,
																									num_4H=1
																									)

				ga_runner(
						symbol_data_5M=symbol_data_5M,
						symbol_data_15M=symbol_data_15M,
						symbol_data_1H=symbol_data_1H,
						symbol_data_4H=symbol_data_4H,
						symbol=sym.name,
						num_turn=40,
						max_score_ga_buy=2,
						max_score_ga_sell=2,
						flag_trade='sell'
						)

				symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																									sym=sym.name,
																									num_5M=99000,
																									num_15M=33000,
																									num_1H=1,
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