from random import seed
from random import randint
from log_get_data import *
from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
from cross_macd import *
import csv
import os


def initilize_values():
	#************************** initialize Values ******************************************************
	Chromosome_5M = {}
	Chromosome_30M = {}
	Chromosome_1H = {}
	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4'
	}

	range(1)
	value = randint(50, 100)
	i = 0
	while i < 8:
		Chromosome_5M[i] = {
			#'sl': '',
			#'tp': '',
			#'diff_min_max': '',
			'apply_to': apply_to[randint(0, 6)],
			'macd_slow': randint(1, 50),
			'macd_fast': randint(1, 50),
			'macd_signal': randint(5, 20)
		}
		Chromosome_30M[i] = {
			#'sl': '',
			#'tp': '',
			#'diff_min_max': '',
			'apply_to': apply_to[randint(0, 6)],
			'macd_slow': randint(1, 50),
			'macd_fast': randint(1, 50),
			'macd_signal': randint(5, 20)
		}
		Chromosome_1H[i] = {
			#'sl': '',
			#'tp': '',
			#'diff_min_max': '',
			'apply_to': apply_to[randint(0, 6)],
			'macd_slow': randint(1, 50),
			'macd_fast': randint(1, 50),
			'macd_signal': randint(5, 20)
		}
		res = list(Chromosome_5M[i].keys()) 
		#print(res[1])
		#print(Chromosome_5M[i][res[1]])
		i += 1

	#***********************************************************************************
	return Chromosome_5M, Chromosome_30M, Chromosome_1H

#initilize_values()
def macd_genetic():

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	chorm_signal_cross_30M = {}
	chorm_signal_cross_5M = {}
	chorm_signal_cross_1H = {}
	sym_counter = 0

	for sym in symbols:
		window_counter = 0
		chorm_save_counter_30M = 0
		chorm_save_counter_5M = 0
		chorm_save_counter_1H = 0
		chorm_save_counter_5M30M = 0
		chorm_save_counter_porro = 0

		data_save_30M = {}
		data_save_5M = {}
		data_save_1H = {}
		data_save_5M30M = {}
		data_save_porro = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		print('************************ sym number = ',sym_counter,' ******************************************')
		sym_counter += 1
		while window_counter <= 7:
			window_start = randint(0, 500)
			window_end = randint(500, 1000)
			print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')
			symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
			symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)
			symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

			print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')


			genetic_counter = 0

			while genetic_counter < 2:

				chrom_counter = 0

				while chrom_counter < len(Chromosome_30M):
					#print(chrom_counter)
					macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)

					macd_30M = macd_all_30M[macd_all_30M.columns[0]]
					macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
					macds_30M = macd_all_30M[macd_all_30M.columns[2]]

					signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,0,0)

					if ((signal_cross_30M['signal'] == 'buy')):

						counter_i = signal_cross_30M['index']
						final_index = (len(macd_30M)-1)

						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_buy_tp = {}
						percentage_buy_st = {}


						while (counter_i <= final_index):
							percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100
							percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100

							counter_i += 1
							counter_j += 1

						percentage_buy_tp_save = max(percentage_buy_tp.values())
						if (percentage_buy_tp_save < 0): 
							percentage_buy_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_buy_st_save = min(percentage_buy_st.values())
						if (percentage_buy_st_save > 0): percentage_buy_st_save = 0

						if (percentage_buy_tp_save > 0):
							score = int(percentage_buy_tp_save * 100)
						else:
							score = 0
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save,
						'st': percentage_buy_st_save,
						'signal': 'buy',
						'score': score,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_30M['diff_plus'],
						'diff_minus': signal_cross_30M['diff_minus']
						}
						chorm_save_counter_30M += 1
					if ((signal_cross_30M['signal'] == 'sell')):
						counter_i = signal_cross_30M['index']
						final_index = (len(macd_30M)-1)
						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}

						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['low'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_30M[sym.name]['low'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['high'][counter_i])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_sell_tp_save = min(percentage_sell_tp.values())
						if (percentage_sell_tp_save > 0): 
							percentage_sell_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_sell_st_save = max(percentage_sell_st.values())
						if (percentage_sell_st_save < 0): percentage_sell_st_save = 0

						if (percentage_sell_tp_save < 0):
							score = abs(int(percentage_sell_tp_save * 100))
						else:
							score = 0
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save,
						'st': percentage_sell_st_save,
						'signal': 'sell',
						'score': score,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_30M['diff_plus'],
						'diff_minus': signal_cross_30M['diff_minus']
						}
						chorm_save_counter_30M += 1


					macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)

					macd_5M = macd_all_5M[macd_all_5M.columns[0]]
					macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
					macds_5M = macd_all_5M[macd_all_5M.columns[2]]

					signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,0,0)

					if ((signal_cross_5M['signal'] == 'buy')):
						counter_i = signal_cross_5M['index']
						final_index = (len(macd_5M)-1)

						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_buy_tp = {}
						percentage_buy_st = {}

						while (counter_i <= final_index):
							percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100
							percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_buy_tp_save = max(percentage_buy_tp.values())
						if (percentage_buy_tp_save < 0): 
							percentage_buy_tp_save = 0
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_buy_st_save = min(percentage_buy_st.values())
						if (percentage_buy_st_save > 0): percentage_buy_st_save = 0


						if (percentage_buy_tp_save > 0):
							score = int(percentage_buy_tp_save * 100)
						else:
							score = 0
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save,
						'st': percentage_buy_st_save,
						'signal': 'buy',
						'score': score,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_5M['diff_plus'],
						'diff_minus': signal_cross_5M['diff_minus']
						}
						chorm_save_counter_5M += 1

					if ((signal_cross_5M['signal'] == 'sell')):
						counter_i = signal_cross_5M['index']
						final_index = (len(macd_5M)-1)
						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}

						

						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_sell_tp_save = min(percentage_sell_tp.values())
						if (percentage_sell_tp_save > 0):
							percentage_sell_tp_save = 0
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_sell_st_save = max(percentage_sell_st.values())
						if (percentage_sell_st_save < 0): percentage_sell_st_save = 0

						if (percentage_sell_tp_save < 0):
							score = abs(int(percentage_sell_tp_save * 100))
						else:
							score = 0
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save,
						'st': percentage_sell_st_save,
						'signal': 'sell',
						'score': score,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_5M['diff_plus'],
						'diff_minus': signal_cross_5M['diff_minus']
						}
						chorm_save_counter_5M += 1

			
					macd_all_1H = ind.macd(symbol_data_1H[sym.name][Chromosome_1H[chrom_counter]['apply_to']],fast=Chromosome_1H[chrom_counter]['macd_fast'], slow=Chromosome_1H[chrom_counter]['macd_slow'],signal=Chromosome_1H[chrom_counter]['macd_signal'], verbose=True)

					macd_1H = macd_all_1H[macd_all_1H.columns[0]]
					macdh_1H = macd_all_1H[macd_all_1H.columns[1]]
					macds_1H = macd_all_1H[macd_all_1H.columns[2]]

					signal_cross_1H = cross_macd(macd_1H,macds_1H,macdh_1H,sym.name,0,0)

					if ((signal_cross_1H['signal'] == 'buy')):
						counter_i = signal_cross_1H['index']
						final_index = (len(macd_1H)-1)

						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_buy_tp = {}
						percentage_buy_st = {}

						while (counter_i <= final_index):
							percentage_buy_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['high'][signal_cross_1H['index']])/symbol_data_1H[sym.name]['high'][signal_cross_1H['index']]) * 100
							percentage_buy_st[counter_j] = ((symbol_data_1H[sym.name]['high'][signal_cross_1H['index']] - symbol_data_1H[sym.name]['low'][counter_i])/symbol_data_1H[sym.name]['high'][signal_cross_1H['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_buy_tp_save = max(percentage_buy_tp.values())
						if (percentage_buy_tp_save < 0): 
							percentage_buy_tp_save = 0
							Chromosome_1H[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_buy_st_save = min(percentage_buy_st.values())
						if (percentage_buy_st_save > 0): percentage_buy_st_save = 0

						if (percentage_buy_tp_save > 0):
							score = int(percentage_buy_tp_save * 100)
						else:
							score = 0
						data_save_1H[chorm_save_counter_1H] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1H[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save,
						'st': percentage_buy_st_save,
						'signal': 'buy',
						'score': score,
						'macd_fast': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1H[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_1H['diff_plus'],
						'diff_minus': signal_cross_1H['diff_minus']
						}
						chorm_save_counter_1H += 1

					if ((signal_cross_1H['signal'] == 'sell')):
						counter_i = signal_cross_1H['index']
						final_index = (len(macd_1H)-1)
						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)
						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}

						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['low'][signal_cross_1H['index']])/symbol_data_1H[sym.name]['low'][signal_cross_1H['index']]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_1H[sym.name]['low'][signal_cross_1H['index']] - symbol_data_1H[sym.name]['high'][counter_i])/symbol_data_1H[sym.name]['low'][signal_cross_1H['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_sell_tp_save = min(percentage_sell_tp.values())
						if (percentage_sell_tp_save > 0): 
							percentage_sell_tp_save = 0
							Chromosome_1H[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_sell_st_save = max(percentage_sell_st.values())
						if (percentage_sell_st_save < 0): percentage_sell_st_save = 0

						if (percentage_sell_tp_save < 0):
							score = abs(int(percentage_sell_tp_save * 100))
						else:
							score = 0
						data_save_1H[chorm_save_counter_1H] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1H[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save,
						'st': percentage_sell_st_save,
						'signal': 'sell',
						'score': score,
						'macd_fast': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1H[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_1H['diff_plus'],
						'diff_minus': signal_cross_1H['diff_minus']
						}
						chorm_save_counter_1H += 1

					# ********************************************** tarkibi zaeef **************************************************************************

					if ((signal_cross_30M['signal'] == 'buy') & (signal_cross_5M['signal'] == 'buy') & (signal_cross_30M['index'] == signal_cross_5M['index'])):

						counter_i = signal_cross_30M['index']
						final_index = (len(macd_30M)-1)

						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)

						counter_j = 0

						percentage_buy_tp = {}
						percentage_buy_st = {}

						while (counter_i <= final_index):
							percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100
							percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_buy_tp_save = max(percentage_buy_tp.values())
						if (percentage_buy_tp_save < 0): 
							percentage_buy_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_buy_st_save = min(percentage_buy_st.values())
						if (percentage_buy_st_save > 0): percentage_buy_st_save = 0

						if (percentage_buy_tp_save > 0):
							score = int(percentage_buy_tp_save * 100)
						else:
							score = 0
						data_save_5M30M[chorm_save_counter_5M30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save,
						'st': percentage_buy_st_save,
						'signal': 'buy',
						'score': score,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_30M['diff_plus'],
						'diff_minus': signal_cross_30M['diff_minus']
						}
						chorm_save_counter_5M30M += 1

					if ((signal_cross_30M['signal'] == 'sell') & (signal_cross_5M['signal'] == 'sell') & (signal_cross_30M['index'] == signal_cross_5M['index'])):
						counter_i = signal_cross_30M['index']
						final_index = (len(macd_30M)-1)
						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_30M)-1)):
								final_index = (len(macd_30M)-1)
						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}

						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['low'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_30M[sym.name]['low'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['high'][counter_i])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_sell_tp_save = min(percentage_sell_tp.values())
						if (percentage_sell_tp_save < 0): 
							percentage_sell_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_sell_st_save = max(percentage_sell_st.values())
						if (percentage_sell_st_save < 0): percentage_sell_st_save = 0

						if (percentage_sell_tp_save < 0):
							score = abs(int(percentage_sell_tp_save * 100))
						else:
							score = 0
						data_save_5M30M[chorm_save_counter_5M30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save,
						'st': percentage_sell_st_save,
						'signal': 'sell',
						'score': score,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_30M['diff_plus'],
						'diff_minus': signal_cross_30M['diff_minus']
						}
						chorm_save_counter_5M30M += 1

					# **************************************//////******************************************************************

					# ********************************************** tarkibi porro **************************************************************************

					if ((signal_cross_1H['signal'] == 'buy') & (signal_cross_30M['signal'] == 'buy') & (signal_cross_5M['signal'] == 'buy') & (signal_cross_30M['index'] <= signal_cross_5M['index']) & (signal_cross_1H['index'] <= signal_cross_5M['index'])):

						counter_i = signal_cross_5M['index']
						final_index = (len(macd_5M)-1)

						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_5M)-1)):
								final_index = (len(macd_5M)-1)

						counter_j = 0

						percentage_buy_tp = {}
						percentage_buy_st = {}

						while (counter_i <= final_index):
							percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100
							percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_buy_tp_save = max(percentage_buy_tp.values())
						if (percentage_buy_tp_save < 0): 
							percentage_buy_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_1H[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_buy_st_save = min(percentage_buy_st.values())
						if (percentage_buy_st_save > 0): percentage_buy_st_save = 0

						if (percentage_buy_tp_save > 0):
							score = int(percentage_buy_tp_save * 100)
						else:
							score = 0
						data_save_porro[chorm_save_counter_porro] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save,
						'st': percentage_buy_st_save,
						'signal': 'buy',
						'score': score,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_5M['diff_plus'],
						'diff_minus': signal_cross_5M['diff_minus']
						}
						chorm_save_counter_porro += 1

					if ((signal_cross_1H['signal'] == 'sell') & (signal_cross_30M['signal'] == 'sell') & (signal_cross_5M['signal'] == 'sell') & (signal_cross_30M['index'] <= signal_cross_5M['index']) & (signal_cross_1H['index'] <= signal_cross_5M['index'])):
						counter_i = signal_cross_5M['index']
						final_index = (len(macd_5M)-1)
						if (final_index - counter_i) >= 20:
							final_index = counter_i + 20
							if (final_index > (len(macd_5M)-1)):
								final_index = (len(macd_5M)-1)
						counter_j = 0

						percentage_sell_tp = {}
						percentage_sell_st = {}

						while (counter_i <= final_index):
							percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100
							percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100

							counter_i += 1
							counter_j += 1
						percentage_sell_tp_save = min(percentage_sell_tp.values())
						if (percentage_sell_tp_save > 0): 
							percentage_sell_tp_save = 0
							Chromosome_30M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_5M[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							Chromosome_1H[chrom_counter] = {
							#'sl': '',
							#'tp': '',
							#'diff_min_max': '',
							'apply_to': apply_to[randint(0, 6)],
							'macd_slow': randint(1, 50),
							'macd_fast': randint(1, 50),
							'macd_signal': randint(5, 20)
							}
							continue
						percentage_sell_st_save = max(percentage_sell_st.values())
						if (percentage_sell_st_save < 0): percentage_sell_st_save = 0

						if (percentage_sell_tp_save < 0):
							score = abs(int(percentage_sell_tp_save * 100))
						else:
							score = 0
						data_save_porro[chorm_save_counter_porro] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save,
						'st': percentage_sell_st_save,
						'signal': 'sell',
						'score': score,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': signal_cross_5M['diff_plus'],
						'diff_minus': signal_cross_5M['diff_minus']
						}
						chorm_save_counter_porro += 1

					# **************************************//////******************************************************************

					chrom_counter += 1
				genetic_counter += 1

			Chromosome_Cutter_5M = randint(0, 3)
			Chromosome_Cutter_30M = randint(0, 3)
			Chromosome_Cutter_1H = randint(0, 3)

			Chromosome_selector_5M = randint(0, 7)
			Chromosome_selector_30M = randint(0, 7)
			Chromosome_selector_1H = randint(0, 7)

			baby_5M = {}
			baby_30M = {}
			baby_1H = {}
			print('Generate Baby')
			chrom_creator_counter = 0
			baby_counter_5M = 0
			baby_counter_30M = 0
			baby_counter_1H = 0

			baby_counter_create = 0

			while (baby_counter_create < (len(Chromosome_30M) * 2)):
				baby_1H[baby_counter_create] = {
				'apply_to': 0,
				'macd_slow': 0,
				'macd_fast': 0,
				'macd_signal': 0
				}
				baby_30M[baby_counter_create] = {
				'apply_to': 0,
				'macd_slow': 0,
				'macd_fast': 0,
				'macd_signal': 0
				}
				baby_5M[baby_counter_create] = {
				'apply_to': 0,
				'macd_slow': 0,
				'macd_fast': 0,
				'macd_signal': 0
				}

				baby_counter_create += 1
			while chrom_creator_counter < len(Chromosome_30M):

				#********************************************* 5M Baby ************************************************************
				Chromosome_selector_5M_1 = randint(0, 7)
				Chromosome_selector_5M_2 = randint(0, 7)

				res_5M_1 = list(Chromosome_5M[Chromosome_selector_5M_1].keys())
				res_5M_2 = list(Chromosome_5M[Chromosome_selector_5M_2].keys())

				

					#print(type(res_5M_1[0]))

				Chromosome_Cutter_5M = randint(0, 3)
				change_chrom_counter = 0
					
					#print('counter',chrom_creator_counter)

				while change_chrom_counter < Chromosome_Cutter_5M:
						#print(change_chrom_counter)
					baby_5M[baby_counter_5M].update({res_5M_1[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_1][res_5M_1[change_chrom_counter]]})
					baby_5M[baby_counter_5M + 1].update({res_5M_2[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_2][res_5M_2[change_chrom_counter]]})

					change_chrom_counter += 1

				change_chrom_counter = Chromosome_Cutter_5M

				while change_chrom_counter < 4:
					baby_5M[baby_counter_5M].update({res_5M_2[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_2][res_5M_2[change_chrom_counter]]})
					baby_5M[baby_counter_5M + 1].update({res_5M_1[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_1][res_5M_1[change_chrom_counter]]})
					change_chrom_counter += 1

					#print(Chromosome_5M)
					#print('baby = ',baby_5M)


				baby_counter_5M = baby_counter_5M + 2

					#********************************************///////***************************************************************************

					#****************************************** 30M Baby **************************************************************************
				Chromosome_selector_30M_1 = randint(0, 7)
				Chromosome_selector_30M_2 = randint(0, 7)

				res_30M_1 = list(Chromosome_30M[Chromosome_selector_30M_1].keys())
				res_30M_2 = list(Chromosome_30M[Chromosome_selector_30M_2].keys())

					#print(type(res_30M_1[0]))

				Chromosome_Cutter_30M = randint(0, 3)
				change_chrom_counter = 0
					
					#print('counter',chrom_creator_counter)

				while change_chrom_counter < Chromosome_Cutter_30M:
						#print(change_chrom_counter)
					baby_30M[baby_counter_30M].update({res_30M_1[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_1][res_30M_1[change_chrom_counter]]})
					baby_30M[baby_counter_30M + 1].update({res_30M_2[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_2][res_30M_2[change_chrom_counter]]})

					change_chrom_counter += 1

				change_chrom_counter = Chromosome_Cutter_30M

				while change_chrom_counter < 4:
					baby_30M[baby_counter_30M].update({res_30M_2[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_2][res_30M_2[change_chrom_counter]]})
					baby_30M[baby_counter_30M + 1].update({res_30M_1[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_1][res_30M_1[change_chrom_counter]]})
					change_chrom_counter += 1

					
					#print(Chromosome_30M)
					#print('baby = ',baby_30M)
				baby_counter_30M = baby_counter_30M + 2

				#*********************************************************////****************************************************

				#********************************************************* 1H Baby ***************************************************
				Chromosome_selector_1H_1 = randint(0, 7)
				Chromosome_selector_1H_2 = randint(0, 7)

				res_1H_1 = list(Chromosome_1H[Chromosome_selector_1H_1].keys())
				res_1H_2 = list(Chromosome_1H[Chromosome_selector_1H_2].keys())

					#print(type(res_1H_1[0]))

				Chromosome_Cutter_1H = randint(0, 3)
				change_chrom_counter = 0
					
					#print('counter',chrom_creator_counter)

				while change_chrom_counter < Chromosome_Cutter_1H:
						#print(change_chrom_counter)
					baby_1H[baby_counter_1H].update({res_1H_1[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_1][res_1H_1[change_chrom_counter]]})
					baby_1H[baby_counter_1H + 1].update({res_1H_2[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_2][res_1H_2[change_chrom_counter]]})

					change_chrom_counter += 1

				change_chrom_counter = Chromosome_Cutter_1H

				while change_chrom_counter < 4:
					baby_1H[baby_counter_1H].update({res_1H_2[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_2][res_1H_2[change_chrom_counter]]})
					baby_1H[baby_counter_1H + 1].update({res_1H_1[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_1][res_1H_1[change_chrom_counter]]})
					change_chrom_counter += 1

					#print(Chromosome_1H)
					#print('baby = ',baby_1H)
					

				baby_counter_1H = baby_counter_1H + 2

			#************************************************///////*************************************************************************



				chrom_creator_counter += 1

			i = 0
			limit_counter = len(Chromosome_5M) * 2 
			while i < (limit_counter):
				Chromosome_5M[i] = {
				#'sl': '',
				#'tp': '',
				#'diff_min_max': '',
				'apply_to': apply_to[randint(0, 6)],
				'macd_slow': randint(1, 50),
				'macd_fast': randint(1, 50),
				'macd_signal': randint(5, 20)
				}
				Chromosome_30M[i] = {
				#'sl': '',
				#'tp': '',
				#'diff_min_max': '',
				'apply_to': apply_to[randint(0, 6)],
				'macd_slow': randint(1, 50),
				'macd_fast': randint(1, 50),
				'macd_signal': randint(5, 20)
				}
				Chromosome_1H[i] = {
				#'sl': '',
				#'tp': '',
				#'diff_min_max': '',
				'apply_to': apply_to[randint(0, 6)],
				'macd_slow': randint(1, 50),
				'macd_fast': randint(1, 50),
				'macd_signal': randint(5, 20)
				}
				i += 1

			re_counter = 0
			while (re_counter < limit_counter):
				Chromosome_5M[re_counter]['apply_to'] = baby_5M[re_counter]['apply_to']
				Chromosome_5M[re_counter]['macd_slow'] = baby_5M[re_counter]['macd_slow']
				Chromosome_5M[re_counter]['macd_fast'] = baby_5M[re_counter]['macd_fast']
				Chromosome_5M[re_counter]['macd_signal'] = baby_5M[re_counter]['macd_signal']
				re_counter += 1
				#print(Chromosome_5M[6])

			re_counter = 0
			while (re_counter < limit_counter):
				Chromosome_30M[re_counter]['apply_to'] = baby_30M[re_counter]['apply_to']
				Chromosome_30M[re_counter]['macd_slow'] = baby_30M[re_counter]['macd_slow']
				Chromosome_30M[re_counter]['macd_fast'] = baby_30M[re_counter]['macd_fast']
				Chromosome_30M[re_counter]['macd_signal'] = baby_30M[re_counter]['macd_signal']
				re_counter += 1


			re_counter = 0
			while (re_counter < limit_counter):
				Chromosome_1H[re_counter]['apply_to'] = baby_1H[re_counter]['apply_to']
				Chromosome_1H[re_counter]['macd_slow'] = baby_1H[re_counter]['macd_slow']
				Chromosome_1H[re_counter]['macd_fast'] = baby_1H[re_counter]['macd_fast']
				Chromosome_1H[re_counter]['macd_signal'] = baby_1H[re_counter]['macd_signal']
				re_counter += 1
				
			window_counter += 1

		#**************************** Calc Max tp & Min st *********************************************************
		try:
			max_tp = max([abs(i['tp']) for i in data_save_5M.values()])
			max_find_5M = {}
			min_find_5M = {}
			counter_find = 0
			for i in data_save_5M.values():
				if ((abs((i['tp'])) == max_tp) & (max_tp != 0)):
					max_find_5M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_5M.values()])

			counter_find = 0
			for i in max_find_5M.values():
				if abs(i['st']) == min_st:
					min_find_5M[counter_find] = i
					counter_find += 1
			print(min_find_5M)
		except:
			print('Empty')

		try:
			max_tp = max([abs(i['tp']) for i in data_save_30M.values()])
			max_find_30M = {}
			min_find_30M = {}
			counter_find = 0
			for i in data_save_30M.values():
				if ((abs((i['tp'])) == max_tp) & (max_tp != 0)):
					max_find_30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_30M.values()])

			counter_find = 0
			for i in max_find_30M.values():
				if abs(i['st']) == min_st:
					min_find_30M[counter_find] = i
					counter_find += 1
			#print(min_find_30M)
		except:
			print('Empty')


		try:
			max_tp = max([abs(i['tp']) for i in data_save_1H.values()])
			max_find_1H = {}
			min_find_1H = {}
			counter_find = 0
			for i in data_save_1H.values():
				if ((abs((i['tp'])) == max_tp) & (max_tp != 0)):
					max_find_1H[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_1H.values()])

			counter_find = 0
			for i in max_find_1H.values():
				if abs(i['st']) == min_st:
					min_find_1H[counter_find] = i
					counter_find += 1
			#print(min_find_1H)
		except:
			print('Empty')


		try:
			max_tp = max([abs(i['tp']) for i in data_save_5M30M.values()])
			max_find_5M30M = {}
			min_find_5M30M = {}
			counter_find = 0
			for i in data_save_5M30M.values():
				if ((abs((i['tp'])) == max_tp) & (max_tp != 0)):
					max_find_5M30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_5M30M.values()])

			counter_find = 0
			for i in max_find_5M30M.values():
				if abs(i['st']) == min_st:
					min_find_5M30M[counter_find] = i
					counter_find += 1
			#print(min_find_5M30M)
		except:
			print('Empty')


		try:
			max_tp = max([abs(i['tp']) for i in data_save_porro.values()])
			max_find_porro = {}
			min_find_porro = {}
			counter_find = 0
			for i in data_save_porro.values():
				if ((abs((i['tp'])) == max_tp) & (max_tp != 0)):
					max_find_porro[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_porro.values()])

			counter_find = 0
			for i in max_find_porro.values():
				if abs(i['st']) == min_st:
					min_find_porro[counter_find] = i
					counter_find += 1
			#print(min_find_porro)
		except:
			print('Empty')


		#print(type(data_save_5M))
		#print('tp check = ','tp' in data_save_5M[0])
		#********************************///////////////****************************************************************
		
		#*************************** Save to TXT File ***************************************************************
		try:
			if os.path.exists("Genetic_macd_output/5M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output/5M/"+sym.name+'.csv')
			add_row = {'apply_to': min_find_5M[0]['apply_to'],'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
			'macd_fast': min_find_5M[0]['macd_fast'] , 'macd_slow': min_find_5M[0]['macd_slow'], 'macd_signal': min_find_5M[0]['macd_signal']
			,'diff_plus':min_find_5M[0]['diff_plus'] , 'diff_minus': min_find_5M[0]['diff_minus']}

			with open("Genetic_macd_output/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		try:
			if os.path.exists("Genetic_macd_output/30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output/30M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_30M[0]['apply_to'],'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
			'macd_fast': min_find_30M[0]['macd_fast'] , 'macd_slow': min_find_30M[0]['macd_slow'], 'macd_signal': min_find_30M[0]['macd_signal']
			,'diff_plus':min_find_30M[0]['diff_plus'] , 'diff_minus': min_find_30M[0]['diff_minus']}

			with open("Genetic_macd_output/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')


		try:
			if os.path.exists("Genetic_macd_output/1H/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output/1H/"+sym.name+'.csv')
			add_row = {'apply_to': min_find_1H[0]['apply_to'],'tp' : min_find_1H[0]['tp'], 'st' : min_find_1H[0]['st'],
			'macd_fast': min_find_1H[0]['macd_fast'] , 'macd_slow': min_find_1H[0]['macd_slow'], 'macd_signal': min_find_1H[0]['macd_signal']
			,'diff_plus':min_find_1H[0]['diff_plus'] , 'diff_minus': min_find_1H[0]['diff_minus']}

			with open("Genetic_macd_output/1H/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')


		try:
			if os.path.exists("Genetic_macd_output/5M30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output/5M30M/"+sym.name+'.csv')
			add_row = {'apply_to': min_find_5M30M[0]['apply_to'],'tp' : min_find_5M30M[0]['tp'], 'st' : min_find_5M30M[0]['st'],
			'macd_fast': min_find_5M30M[0]['macd_fast'] , 'macd_slow': min_find_5M30M[0]['macd_slow'], 'macd_signal': min_find_5M30M[0]['macd_signal']
			,'diff_plus':min_find_5M30M[0]['diff_plus'] , 'diff_minus': min_find_5M30M[0]['diff_minus']}

			with open("Genetic_macd_output/5M30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')


		try:
			if os.path.exists("Genetic_macd_output/porro/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output/porro/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_porro[0]['apply_to'],'tp' : min_find_porro[0]['tp'], 'st' : min_find_porro[0]['st'],
			'macd_fast': min_find_porro[0]['macd_fast'] , 'macd_slow': min_find_porro[0]['macd_slow'], 'macd_signal': min_find_porro[0]['macd_signal']
			,'diff_plus':min_find_porro[0]['diff_plus'] , 'diff_minus': min_find_porro[0]['diff_minus']}

			with open("Genetic_macd_output/porro/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')
		#*****************************////////////******************************************************************


#macd_genetic()
