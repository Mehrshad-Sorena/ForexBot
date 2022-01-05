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
from progress.bar import Bar



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
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	range(1)
	value = randint(50, 100)

	Chromosome_5M[0] = {
	'apply_to': 'close',
	'macd_slow': 12,
	'macd_fast': 26,
	'macd_signal': 9
	}
	Chromosome_30M[0] = {
	'apply_to': 'close',
	'macd_slow': 12,
	'macd_fast': 26,
	'macd_signal': 9
	}
	Chromosome_1H[0] = {
	'apply_to': 'close',
	'macd_slow': 12,
	'macd_fast': 26,
	'macd_signal': 9
	}

	Chromosome_5M[1] = {
	'apply_to': 'close',
	'macd_slow': 8,
	'macd_fast': 16,
	'macd_signal': 6
	}
	Chromosome_30M[1] = {
	'apply_to': 'close',
	'macd_slow': 8,
	'macd_fast': 16,
	'macd_signal': 6
	}
	Chromosome_1H[1] = {
	'apply_to': 'close',
	'macd_slow': 8,
	'macd_fast': 16,
	'macd_signal': 6
	}
	i = 2
	while i < 8:
		Chromosome_5M[i] = {
			'apply_to': apply_to[randint(0, 7)],
			'macd_slow': randint(20, 40),
			'macd_fast': randint(1, 20),
			'macd_signal': randint(1, 18)
		}
		Chromosome_30M[i] = {
			'apply_to': apply_to[randint(0, 7)],
			'macd_slow': randint(20, 40),
			'macd_fast': randint(1, 20),
			'macd_signal': randint(1, 18)
		}
		Chromosome_1H[i] = {
			'apply_to': apply_to[randint(0, 7)],
			'macd_slow': randint(20, 40),
			'macd_fast': randint(1, 20),
			'macd_signal': randint(1, 18)
		}
		res = list(Chromosome_5M[i].keys()) 
		#print(res[1])
		#print(Chromosome_5M[i][res[1]])
		i += 1

	#***********************************************************************************
	return Chromosome_5M, Chromosome_30M, Chromosome_1H

def gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	Chromosome_Cutter_5M = randint(0, 3)
	Chromosome_Cutter_30M = randint(0, 3)
	Chromosome_Cutter_1H = randint(0, 3)

	Chromosome_selector_5M = randint(0, 7)
	Chromosome_selector_30M = randint(0, 7)
	Chromosome_selector_1H = randint(0, 7)

	baby_5M = {}
	baby_30M = {}
	baby_1H = {}
	#print('Generate Baby')
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
		'apply_to': apply_to[randint(0, 7)],
		'macd_slow': randint(20, 40),
		'macd_fast': randint(1, 20),
		'macd_signal': randint(1, 18)
		}
		Chromosome_30M[i] = {
		#'sl': '',
		#'tp': '',
		#'diff_min_max': '',
		'apply_to': apply_to[randint(0, 7)],
		'macd_slow': randint(20, 40),
		'macd_fast': randint(1, 20),
		'macd_signal': randint(1, 18)
		}
		Chromosome_1H[i] = {
		#'sl': '',
		#'tp': '',
		#'diff_min_max': '',
		'apply_to': apply_to[randint(0, 7)],
		'macd_slow': randint(20, 40),
		'macd_fast': randint(1, 20),
		'macd_signal': randint(1, 18)
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

	return Chromosome_5M,Chromosome_30M,Chromosome_1H
				


#***********///////////********************************** BUY ALGO 30M *********///////////////////******************************************


#initilize_values()
def macd_genetic_buy_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	window_end = 2000
	window_start = 0
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)


	chorm_signal_cross_30M = {}
	sym_counter = 0

	print('**************************** START MACD 30M BUY *********************************************')

	bar = Bar('Processing 30M BUY MACD = ', max=73)

	print('\n')
	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_30M = 0

		data_save_30M = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		

		if os.path.exists("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_30M[7] = line

					Chromosome_30M[7]['macd_fast'] = float(Chromosome_30M[7]['macd_fast'])
					Chromosome_30M[7]['macd_slow'] = float(Chromosome_30M[7]['macd_slow'])
					Chromosome_30M[7]['macd_signal'] = float(Chromosome_30M[7]['macd_signal'])
			#continue

		chrom_counter = 0


		chrom_faild = 0
		chrom_faild_30M = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_30M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY 30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

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

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_30M)))

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				

				if ((signal_cross_30M['signal'] == 'buy')):

					signal_cross_30M['index'] += 3

					counter_i = signal_cross_30M['index']
					final_index = (len(macd_30M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_30M)-1)):
							final_index = (len(macd_30M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100

						#print(percentage_buy_tp[counter_j])
						##if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 50): break

					try:
						percentage_buy_tp_save_30M[tp_counter_30M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_30M[tp_counter_30M] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_30M[tp_counter_30M] = 0
						percentage_buy_st_save_30M[tp_counter_30M] = 0

					#print('Max = ', percentage_buy_tp_save_30M[tp_counter_30M])

					if (percentage_buy_st_save_30M[tp_counter_30M] < 0): 
						percentage_buy_st_save_30M[tp_counter_30M] = 0
						score_30M += 0

					if (percentage_buy_st_save_30M[tp_counter_30M] > (spred+0.02)):
						score_30M -= 0

					if (percentage_buy_tp_save_30M[tp_counter_30M] > (spred+tp_limit)): 
						score_30M += 1
						diff_plus_30M += (signal_cross_30M['diff_plus'] * 0.8)
						diff_minus_30M += (signal_cross_30M['diff_minus'] * 0.8)

						diff_counter += 1

						if (abs(percentage_buy_st_save_30M[tp_counter_30M]) >= abs(percentage_buy_tp_save_30M[tp_counter_30M])):
							score_30M -= 1
						else:
							score_30M += 1

					if (percentage_buy_tp_save_30M[tp_counter_30M] <= (spred+tp_limit)): 
						score_30M -= 1
						percentage_buy_tp_save_30M[tp_counter_30M] = -1000

					

					num_trade += 1


					tp_counter_30M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_30M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_30M = (score_30M/num_trade) * 100

			#print('Score = ', score_30M)

			if (num_trade < max_num_trade):
				score_30M = -10
			#print('*************************************** score_30M = ',score_30M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 30M ************************************************************************

			if (score_30M < max_score_30M):
				chrom_faild_30M += 1
				chrom_faild += 1

				Chromosome_30M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				##print('new baby 30M')
				while (Chromosome_30M[chrom_counter]['macd_fast'] >= Chromosome_30M[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					
				chrom_faild_30M = 0
				score_30M = 0

				#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_30M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_30M)
				else:
					continue
				

			if (score_30M >= max_score_30M):
				chrom_faild_30M = 0
				try:
					max_score_30M = score_30M
					diff_plus_30M = diff_plus_30M/diff_counter
					diff_minus_30M = diff_minus_30M/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_30M.items()}

					percentage_buy_tp_save_30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_30M.items()}

					percentage_buy_st_save_30M = max(res.values())

					if percentage_buy_tp_save_30M != 0:
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_30M,
						'st': percentage_buy_st_save_30M,
						'signal': 'buy',
						'score': score_30M,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_30M,
						'diff_minus': diff_minus_30M
						}
						chorm_save_counter_30M += 1

						if (score_30M >= 195): faild_flag = num_turn + 1
					score_30M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_30M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************



		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_30M.values()])
			max_find_30M = {}
			min_find_30M = {}
			max_find_tp_30M = {}
			counter_find = 0
			for i in data_save_30M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_30M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_30M.values()])

			counter_find = 0
			for i in max_find_30M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_30M.values()])

			counter_find = 0
			for i in max_find_tp_30M.values():
				if abs(i['st']) == min_st:
					min_find_30M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_30M[0]['apply_to'],'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
			'macd_fast': min_find_30M[0]['macd_fast'] , 'macd_slow': min_find_30M[0]['macd_slow'], 'macd_signal': min_find_30M[0]['macd_signal']
			,'diff_plus':min_find_30M[0]['diff_plus'] , 'diff_minus': min_find_30M[0]['diff_minus']
			,'score': min_find_30M[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 30M BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 30M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************

#***********///////////********************************** SELL ALGO 30M *********///////////////////******************************************

def macd_genetic_sell_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)

	chorm_signal_cross_30M = {}
	sym_counter = 0

	print('**************************** START MACD 30M SELL *********************************************')

	bar = Bar('Processing 30M SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_30M = 0

		data_save_30M = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_30M[7] = line

					Chromosome_30M[7]['macd_fast'] = float(Chromosome_30M[7]['macd_fast'])
					Chromosome_30M[7]['macd_slow'] = float(Chromosome_30M[7]['macd_slow'])
					Chromosome_30M[7]['macd_signal'] = float(Chromosome_30M[7]['macd_signal'])
			#continue


		chrom_faild = 0
		chrom_faild_30M = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_30M):
			window_end = 2000
			window_start = 0
			

			window_length = 10

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL 30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_30M = 0
			tp_counter_30M = 0
			percentage_buy_tp_save_30M = {}
			percentage_buy_st_save_30M = {}
			percentage_sell_tp_save_30M = {}
			percentage_sell_st_save_30M = {}
			diff_minus_30M = 0
			diff_plus_30M = 0

			num_trade = 0

			diff_counter = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_30M)))

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				

				if ((signal_cross_30M['signal'] == 'sell')):

					signal_cross_30M['index'] += 3

					counter_i = signal_cross_30M['index']
					final_index = (len(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']])-1)

					#if (counter_i >= final_index)
					#print(counter_i,final_index)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_30M)-1)):
							final_index = (len(macd_30M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['low'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_30M[sym.name]['low'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['high'][counter_i])/symbol_data_30M[sym.name]['low'][signal_cross_30M['index']]) * 100

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 50): break

					try:
						percentage_sell_tp_save_30M[tp_counter_30M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_30M[tp_counter_30M] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_30M[tp_counter_30M] = 0
						percentage_sell_st_save_30M[tp_counter_30M] = 0


					if (percentage_sell_st_save_30M[tp_counter_30M] > 0): 
						percentage_sell_st_save_30M[tp_counter_30M] = 0
						score_30M += 0

					if (percentage_sell_st_save_30M[tp_counter_30M] < (-1 * (spred+0.02))): 
						score_30M -= 0

					if (percentage_sell_tp_save_30M[tp_counter_30M] < (-1 * (spred+tp_limit))): 
						diff_plus_30M += (signal_cross_30M['diff_plus'] * 0.8)
						diff_minus_30M += (signal_cross_30M['diff_minus'] * 0.8)

						diff_counter += 1

						score_30M += 1
						if (abs(percentage_sell_st_save_30M[tp_counter_30M]) >= abs(percentage_sell_tp_save_30M[tp_counter_30M])):
							score_30M -= 1
						else:
							score_30M += 1

					if (percentage_sell_tp_save_30M[tp_counter_30M] >= (-1 * (spred+0.04))): 
						score_30M -= 1
						percentage_sell_tp_save_30M[tp_counter_30M] = 1000

				

					

					num_trade += 1


					tp_counter_30M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_30M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_30M = (score_30M/num_trade) * 100

			if (num_trade < max_num_trade):
				score_30M = -10

			#print('*************************************** score_30M = ',score_30M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************

			


			#************************************************* Check save recreate 30M ************************************************************************

			if (score_30M < max_score_30M):
				chrom_faild_30M += 1
				chrom_faild += 1

				Chromosome_30M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_30M[chrom_counter]['macd_fast'] >= Chromosome_30M[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_30M = 0
					score_30M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_30M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_30M)
				else:
					continue

			if (score_30M >= max_score_30M):
				chrom_faild_30M = 0
				try:
					max_score_30M = score_30M
					diff_plus_30M = diff_plus_30M/diff_counter
					diff_minus_30M = diff_minus_30M/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_30M.items()}

					percentage_sell_tp_save_30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_30M.items()}

					percentage_sell_st_save_30M = max(res.values())

					if percentage_sell_tp_save_30M != 0:
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_30M,
						'st': percentage_sell_st_save_30M,
						'signal': 'sell',
						'score': score_30M,
						'macd_fast': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_30M,
						'diff_minus': diff_minus_30M
						}
						chorm_save_counter_30M += 1

						if (score_30M >= 195): faild_flag = num_turn + 1
					score_30M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1
			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0

				chrom_faild = 0
				chrom_faild_30M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_30M.values()])
			max_find_30M = {}
			min_find_30M = {}
			max_find_tp_30M = {}
			counter_find = 0
			for i in data_save_30M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_30M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_30M.values()])

			counter_find = 0
			for i in max_find_30M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_30M.values()])

			counter_find = 0
			for i in max_find_tp_30M.values():
				if abs(i['st']) == min_st:
					min_find_30M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_30M[0]['apply_to'],'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
			'macd_fast': min_find_30M[0]['macd_fast'] , 'macd_slow': min_find_30M[0]['macd_slow'], 'macd_signal': min_find_30M[0]['macd_signal']
			,'diff_plus':min_find_30M[0]['diff_plus'] , 'diff_minus': min_find_30M[0]['diff_minus']
			,'score': min_find_30M[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 30M SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 30M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#macd_genetic_sell_algo_30M(0.09,3,5,50)

#***********///////////********************************** BUY ALGO 5M *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

	chorm_signal_cross_5M = {}
	sym_counter = 0

	print('**************************** START MACD 5M BUY *********************************************')

	bar = Bar('Processing 5M BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_5M = 0

		data_save_5M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_5M[7] = line

					Chromosome_5M[7]['macd_fast'] = float(Chromosome_5M[7]['macd_fast'])
					Chromosome_5M[7]['macd_slow'] = float(Chromosome_5M[7]['macd_slow'])
					Chromosome_5M[7]['macd_signal'] = float(Chromosome_5M[7]['macd_signal'])
			#continue


		chrom_faild = 0
		chrom_faild_5M = 0

		faild_flag = 0

		print('************************MACD 5M BUY sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_5M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
			#print('+++++++++++++++++++++++++++ BUY 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_5M = 0
			tp_counter_5M = 0
			percentage_buy_tp_save_5M = {}
			percentage_buy_st_save_5M = {}
			percentage_sell_tp_save_5M = {}
			percentage_sell_st_save_5M = {}
			diff_minus_5M = 0
			diff_plus_5M = 0

			diff_counter = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M)))

				


				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,(((-1) * (abs(mean_macd))) * 1.5 ),(abs(mean_macd) * 1.5 ))



				if ((signal_cross_5M['signal'] == 'buy')):

					signal_cross_5M['index'] += 3

					counter_i = signal_cross_5M['index']
					final_index = (len(macd_5M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_5M)-1)):
							final_index = (len(macd_5M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 300): break

					try:
						percentage_buy_tp_save_5M[tp_counter_5M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_5M[tp_counter_5M] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_5M[tp_counter_5M] = 0
						percentage_buy_st_save_5M[tp_counter_5M] = 0


					#print('max = ',percentage_buy_tp_save_5M[tp_counter_5M])

					#print('macd = ',macd_5M[len(macd_5M)-1])
					#print('mean = ',abs(mean_macd))

					if (percentage_buy_st_save_5M[tp_counter_5M] < 0): 
						percentage_buy_st_save_5M[tp_counter_5M] = 0
						score_5M += 0

					if (percentage_buy_st_save_5M[tp_counter_5M] > (spred+0.02)):
						score_5M -= 0

					if (percentage_buy_tp_save_5M[tp_counter_5M] > (spred+tp_limit)): 
						score_5M += 1
						diff_plus_5M += (signal_cross_5M['diff_plus'] * 0.8)
						diff_minus_5M += (signal_cross_5M['diff_minus'] * 0.8)
						diff_counter += 1

						if (abs(percentage_buy_st_save_5M[tp_counter_5M]) >= abs(percentage_buy_tp_save_5M[tp_counter_5M])):
							score_5M -= 1
						else:
							score_5M += 1

					if (percentage_buy_tp_save_5M[tp_counter_5M] <= (spred+tp_limit)): 
						score_5M -= 1
						percentage_buy_tp_save_5M[tp_counter_5M] = -1000

					


					num_trade += 1


					tp_counter_5M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_5M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_5M = (score_5M/num_trade) * 100

			if (num_trade < max_num_trade):
				score_5M = -10

			#print('score = ', score_5M)

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_5M) + 1
				break
			#******************************************************* ////////// ********************************************************



			#************************************************* Check save recreate 5M ************************************************************************

			if (score_5M < max_score_5M):
				chrom_faild_5M += 1
				chrom_faild += 1

				Chromosome_5M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_5M[chrom_counter]['macd_fast'] >= Chromosome_5M[chrom_counter]['macd_slow']):#(chrom_faild_5M > (len(Chromosome_5M)/4)):
					##print('new baby 5M')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(5, 18)
						}
					chrom_faild_5M = 0
					score_5M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_5M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_5M)
				else:
					continue

			if (score_5M >= max_score_5M):
				chrom_faild_5M = 0
				try:
					max_score_5M = score_5M
					diff_plus_5M = diff_plus_5M/diff_counter
					diff_minus_5M = diff_minus_5M/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_5M.items()}

					percentage_buy_tp_save_5M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_5M.items()}

					percentage_buy_st_save_5M = max(res.values())

					if percentage_buy_tp_save_5M != 0:
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_5M,
						'st': percentage_buy_st_save_5M,
						'signal': 'buy',
						'score': score_5M,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_5M,
						'diff_minus': diff_minus_5M
						}
						chorm_save_counter_5M += 1

						if (score_5M >= 195): faild_flag = num_turn + 1
					score_5M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_5M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_5M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_5M.values()])
			max_find_5M = {}
			min_find_5M = {}
			max_find_tp_5M = {}
			counter_find = 0
			for i in data_save_5M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_5M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_5M.values()])

			counter_find = 0
			for i in max_find_5M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_5M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_5M.values()])

			counter_find = 0
			for i in max_find_tp_5M.values():
				if abs(i['st']) == min_st:
					min_find_5M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_5M[0]['apply_to'],'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
			'macd_fast': min_find_5M[0]['macd_fast'] , 'macd_slow': min_find_5M[0]['macd_slow'], 'macd_signal': min_find_5M[0]['macd_signal']
			,'diff_plus':min_find_5M[0]['diff_plus'] , 'diff_minus': min_find_5M[0]['diff_minus']
			,'score': min_find_5M[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 5M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#macd_genetic_buy_algo_5M(0.04,3,5,50)

#***********///////////********************************** SELL ALGO 5M *********///////////////////******************************************

def macd_genetic_sell_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

	chorm_signal_cross_5M = {}
	sym_counter = 0

	print('**************************** START MACD 5M SELL *********************************************')

	bar = Bar('Processing 5M SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_5M = 0

		data_save_5M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_5M[7] = line

					Chromosome_5M[7]['macd_fast'] = float(Chromosome_5M[7]['macd_fast'])
					Chromosome_5M[7]['macd_slow'] = float(Chromosome_5M[7]['macd_slow'])
					Chromosome_5M[7]['macd_signal'] = float(Chromosome_5M[7]['macd_signal'])
			#continue

		chrom_faild = 0
		chrom_faild_5M = 0

		faild_flag = 0

		print('************************MACD 5M SELL sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_5M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
			#print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_5M = 0
			tp_counter_5M = 0
			percentage_buy_tp_save_5M = {}
			percentage_buy_st_save_5M = {}
			percentage_sell_tp_save_5M = {}
			percentage_sell_st_save_5M = {}
			diff_minus_5M = 0
			diff_plus_5M = 0
			diff_counter = 0

			num_trade = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_5M)))

				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,(((-1) * (abs(mean_macd))) * 1.5 ),(abs(mean_macd) * 1.5))


				if ((signal_cross_5M['signal'] == 'sell')):

					signal_cross_5M['index'] += 3
					counter_i = signal_cross_5M['index']

					final_index = (len(macd_5M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_5M)-1)):
							final_index = (len(macd_5M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][signal_cross_5M['index']]) * 100

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 300): break

					try:
						percentage_sell_tp_save_5M[tp_counter_5M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_5M[tp_counter_5M] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_5M[tp_counter_5M] = 0
						percentage_sell_st_save_5M[tp_counter_5M] = 0


					if (percentage_sell_st_save_5M[tp_counter_5M] > 0): 
						percentage_sell_st_save_5M[tp_counter_5M] = 0
						score_5M += 0

					if (percentage_sell_st_save_5M[tp_counter_5M] < (-1 * (spred+0.02))): 
						score_5M -= 0

					if (percentage_sell_tp_save_5M[tp_counter_5M] < (-1 * (spred+tp_limit))): 
						diff_plus_5M += (signal_cross_5M['diff_plus'] * 0.8)
						diff_minus_5M += (signal_cross_5M['diff_minus'] * 0.8)

						diff_counter += 1

						score_5M += 1
						if (abs(percentage_sell_st_save_5M[tp_counter_5M]) >= abs(percentage_sell_tp_save_5M[tp_counter_5M])):
							score_5M -= 1
						else:
							score_5M += 1

					if (percentage_sell_tp_save_5M[tp_counter_5M] >= (-1 * (spred+0.04))): 
						score_5M -= 1
						percentage_sell_tp_save_5M[tp_counter_5M] = 1000

					

					num_trade += 1


					tp_counter_5M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_5M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_5M = (score_5M/num_trade) * 100

			if (num_trade < max_num_trade): score_5M = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_5M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 5M ************************************************************************

			if (score_5M < max_score_5M):
				chrom_faild_5M += 1
				chrom_faild += 1

				Chromosome_5M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_5M[chrom_counter]['macd_fast'] >= Chromosome_5M[chrom_counter]['macd_slow']):#(chrom_faild_5M > (len(Chromosome_5M)/4)):
					##print('new baby 5M')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(5, 18)
						}
					chrom_faild_5M = 0
					score_5M = 0

					chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_5M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_5M)
				else:
					continue

			if (score_5M >= max_score_5M):
				chrom_faild_5M = 0
				try:
					max_score_5M = score_5M
					diff_plus_5M = diff_plus_5M/diff_counter
					diff_minus_5M = diff_minus_5M/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_5M.items()}

					percentage_sell_tp_save_5M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_5M.items()}

					percentage_sell_st_save_5M = max(res.values())

					if percentage_sell_tp_save_5M != 0:
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_5M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_5M,
						'st': percentage_sell_st_save_5M,
						'signal': 'sell',
						'score': score_5M,
						'macd_fast': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_5M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_5M,
						'diff_minus': diff_minus_5M
						}
						chorm_save_counter_5M += 1

						if (score_5M >= 195): faild_flag = num_turn + 1
					score_5M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_5M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				#chrom_counter = 0

				chrom_faild = 0
				chrom_faild_5M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_5M.values()])
			max_find_5M = {}
			min_find_5M = {}
			max_find_tp_5M = {}
			counter_find = 0
			for i in data_save_5M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_5M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_5M.values()])

			counter_find = 0
			for i in max_find_5M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_5M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_5M.values()])

			counter_find = 0
			for i in max_find_tp_5M.values():
				if abs(i['st']) == min_st:
					min_find_5M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_5M[0]['apply_to'],'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
			'macd_fast': min_find_5M[0]['macd_fast'] , 'macd_slow': min_find_5M[0]['macd_slow'], 'macd_signal': min_find_5M[0]['macd_signal']
			,'diff_plus':min_find_5M[0]['diff_plus'] , 'diff_minus': min_find_5M[0]['diff_minus']
			,'score': min_find_5M[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 5M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#macd_genetic_sell_algo_5M(0.04,3,5,50)




#***********///////////********************************** BUY ALGO 15M *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_15M(tp_limit,max_num_trade,num_turn,max_score_15M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_15M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M15,window_start,window_end)

	chorm_signal_cross_15M = {}
	sym_counter = 0

	print('**************************** START MACD 15M BUY *********************************************')

	bar = Bar('Processing 15M BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_15M = 0

		data_save_15M = {}

		Chromosome_15M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_15M[7] = line

					Chromosome_15M[7]['macd_fast'] = float(Chromosome_15M[7]['macd_fast'])
					Chromosome_15M[7]['macd_slow'] = float(Chromosome_15M[7]['macd_slow'])
					Chromosome_15M[7]['macd_signal'] = float(Chromosome_15M[7]['macd_signal'])
			#continue


		chrom_faild = 0
		chrom_faild_15M = 0

		faild_flag = 0

		print('************************MACD 15M BUY sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_15M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
			#print('+++++++++++++++++++++++++++ BUY 15M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_15M = 0
			tp_counter_15M = 0
			percentage_buy_tp_save_15M = {}
			percentage_buy_st_save_15M = {}
			percentage_sell_tp_save_15M = {}
			percentage_sell_st_save_15M = {}
			diff_minus_15M = 0
			diff_plus_15M = 0

			diff_counter = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				macd_all_15M = ind.macd(symbol_data_15M[sym.name][Chromosome_15M[chrom_counter]['apply_to']],fast=Chromosome_15M[chrom_counter]['macd_fast'], slow=Chromosome_15M[chrom_counter]['macd_slow'],signal=Chromosome_15M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_15M = macd_all_15M[macd_all_15M.columns[0]]
				macdh_15M = macd_all_15M[macd_all_15M.columns[1]]
				macds_15M = macd_all_15M[macd_all_15M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_15M)))

				


				signal_cross_15M = cross_macd(macd_15M,macds_15M,macdh_15M,sym.name,(((-1) * (abs(mean_macd))) * 1.5 ),(abs(mean_macd) * 1.5 ))



				if ((signal_cross_15M['signal'] == 'buy')):

					signal_cross_15M['index'] += 3

					counter_i = signal_cross_15M['index']
					final_index = (len(macd_15M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_15M)-1)):
							final_index = (len(macd_15M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_15M[sym.name]['close'][counter_i] - symbol_data_15M[sym.name]['high'][signal_cross_15M['index']])/symbol_data_15M[sym.name]['high'][signal_cross_15M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_15M[sym.name]['high'][signal_cross_15M['index']] - symbol_data_15M[sym.name]['low'][counter_i])/symbol_data_15M[sym.name]['high'][signal_cross_15M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 300): break

					try:
						percentage_buy_tp_save_15M[tp_counter_15M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_15M[tp_counter_15M] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_15M[tp_counter_15M] = 0
						percentage_buy_st_save_15M[tp_counter_15M] = 0


					#print('max = ',percentage_buy_tp_save_5M[tp_counter_5M])

					#print('macd = ',macd_5M[len(macd_5M)-1])
					#print('mean = ',abs(mean_macd))

					if (percentage_buy_st_save_15M[tp_counter_15M] < 0): 
						percentage_buy_st_save_15M[tp_counter_15M] = 0
						score_15M += 0

					if (percentage_buy_st_save_15M[tp_counter_15M] > (spred+0.02)):
						score_15M -= 0

					if (percentage_buy_tp_save_15M[tp_counter_15M] > (spred+tp_limit)): 
						score_15M += 1
						diff_plus_15M += (signal_cross_15M['diff_plus'] * 0.8)
						diff_minus_15M += (signal_cross_15M['diff_minus'] * 0.8)
						diff_counter += 1

						if (abs(percentage_buy_st_save_15M[tp_counter_15M]) >= abs(percentage_buy_tp_save_15M[tp_counter_15M])):
							score_15M -= 1
						else:
							score_15M += 1

					if (percentage_buy_tp_save_15M[tp_counter_15M] <= (spred+tp_limit)): 
						score_15M -= 1
						percentage_buy_tp_save_15M[tp_counter_15M] = -1000

					


					num_trade += 1


					tp_counter_15M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_15M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_15M = (score_15M/num_trade) * 100

			if (num_trade < max_num_trade):
				score_15M = -10

			#print('score = ', score_5M)

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_15M) + 1
				break
			#******************************************************* ////////// ********************************************************



			#************************************************* Check save recreate 5M ************************************************************************

			if (score_15M < max_score_15M):
				chrom_faild_15M += 1
				chrom_faild += 1

				Chromosome_15M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_15M[chrom_counter]['macd_fast'] >= Chromosome_15M[chrom_counter]['macd_slow']):#(chrom_faild_5M > (len(Chromosome_5M)/4)):
					##print('new baby 5M')
					Chromosome_15M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(5, 18)
						}
					chrom_faild_15M = 0
					score_15M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_15M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_15M)
				else:
					continue

			if (score_15M >= max_score_15M):
				chrom_faild_15M = 0
				try:
					max_score_15M = score_15M
					diff_plus_15M = diff_plus_15M/diff_counter
					diff_minus_15M = diff_minus_15M/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_15M.items()}

					percentage_buy_tp_save_15M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_15M.items()}

					percentage_buy_st_save_15M = max(res.values())

					if percentage_buy_tp_save_15M != 0:
						data_save_15M[chorm_save_counter_15M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_15M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_15M,
						'st': percentage_buy_st_save_15M,
						'signal': 'buy',
						'score': score_15M,
						'macd_fast': Chromosome_15M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_15M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_15M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_15M,
						'diff_minus': diff_minus_15M
						}
						chorm_save_counter_15M += 1

						if (score_15M >= 195): faild_flag = num_turn + 1
					score_15M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_15M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_15M = 0

				Chromosome_15M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_15M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_15M.values()])
			max_find_15M = {}
			min_find_15M = {}
			max_find_tp_15M = {}
			counter_find = 0
			for i in data_save_15M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_15M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_15M.values()])

			counter_find = 0
			for i in max_find_15M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_15M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_15M.values()])

			counter_find = 0
			for i in max_find_tp_15M.values():
				if abs(i['st']) == min_st:
					min_find_15M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_15M[0]['apply_to'],'tp' : min_find_15M[0]['tp'], 'st' : min_find_15M[0]['st'],
			'macd_fast': min_find_15M[0]['macd_fast'] , 'macd_slow': min_find_15M[0]['macd_slow'], 'macd_signal': min_find_15M[0]['macd_signal']
			,'diff_plus':min_find_15M[0]['diff_plus'] , 'diff_minus': min_find_15M[0]['diff_minus']
			,'score': min_find_15M[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/15M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 15M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#macd_genetic_buy_algo_15M(0.04,3,2,50)

#***********///////////********************************** SELL ALGO 15M *********///////////////////******************************************

def macd_genetic_sell_algo_15M(tp_limit,max_num_trade,num_turn,max_score_15M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_15M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M15,window_start,window_end)

	chorm_signal_cross_15M = {}
	sym_counter = 0

	print('**************************** START MACD 15M SELL *********************************************')

	bar = Bar('Processing 15M SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_15M = 0

		data_save_15M = {}

		Chromosome_15M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_15M[7] = line

					Chromosome_15M[7]['macd_fast'] = float(Chromosome_15M[7]['macd_fast'])
					Chromosome_15M[7]['macd_slow'] = float(Chromosome_15M[7]['macd_slow'])
					Chromosome_15M[7]['macd_signal'] = float(Chromosome_15M[7]['macd_signal'])
			#continue

		chrom_faild = 0
		chrom_faild_15M = 0

		faild_flag = 0

		print('************************MACD 15M SELL sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_15M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
			#print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_15M = 0
			tp_counter_15M = 0
			percentage_buy_tp_save_15M = {}
			percentage_buy_st_save_15M = {}
			percentage_sell_tp_save_15M = {}
			percentage_sell_st_save_15M = {}
			diff_minus_15M = 0
			diff_plus_15M = 0
			diff_counter = 0

			num_trade = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				macd_all_15M = ind.macd(symbol_data_15M[sym.name][Chromosome_15M[chrom_counter]['apply_to']],fast=Chromosome_15M[chrom_counter]['macd_fast'], slow=Chromosome_15M[chrom_counter]['macd_slow'],signal=Chromosome_15M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_15M = macd_all_15M[macd_all_15M.columns[0]]
				macdh_15M = macd_all_15M[macd_all_15M.columns[1]]
				macds_15M = macd_all_15M[macd_all_15M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_15M)))

				signal_cross_15M = cross_macd(macd_15M,macds_15M,macdh_15M,sym.name,(((-1) * (abs(mean_macd))) * 1.5 ),(abs(mean_macd) * 1.5))


				if ((signal_cross_15M['signal'] == 'sell')):

					signal_cross_15M['index'] += 3
					counter_i = signal_cross_15M['index']

					final_index = (len(macd_15M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_15M)-1)):
							final_index = (len(macd_15M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_15M[sym.name]['close'][counter_i] - symbol_data_15M[sym.name]['low'][signal_cross_15M['index']])/symbol_data_15M[sym.name]['low'][signal_cross_15M['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_15M[sym.name]['low'][signal_cross_15M['index']] - symbol_data_15M[sym.name]['high'][counter_i])/symbol_data_15M[sym.name]['low'][signal_cross_15M['index']]) * 100

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 300): break

					try:
						percentage_sell_tp_save_15M[tp_counter_15M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_15M[tp_counter_15M] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_15M[tp_counter_15M] = 0
						percentage_sell_st_save_15M[tp_counter_15M] = 0


					if (percentage_sell_st_save_15M[tp_counter_15M] > 0): 
						percentage_sell_st_save_15M[tp_counter_15M] = 0
						score_15M += 0

					if (percentage_sell_st_save_15M[tp_counter_15M] < (-1 * (spred+0.02))): 
						score_15M -= 0

					if (percentage_sell_tp_save_15M[tp_counter_15M] < (-1 * (spred+tp_limit))): 
						diff_plus_15M += (signal_cross_15M['diff_plus'] * 0.8)
						diff_minus_15M += (signal_cross_15M['diff_minus'] * 0.8)

						diff_counter += 1

						score_15M += 1
						if (abs(percentage_sell_st_save_15M[tp_counter_15M]) >= abs(percentage_sell_tp_save_15M[tp_counter_15M])):
							score_15M -= 1
						else:
							score_15M += 1

					if (percentage_sell_tp_save_15M[tp_counter_15M] >= (-1 * (spred+0.04))): 
						score_15M -= 1
						percentage_sell_tp_save_15M[tp_counter_15M] = 1000

					

					num_trade += 1


					tp_counter_15M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_15M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_15M = (score_15M/num_trade) * 100

			if (num_trade < max_num_trade): score_15M = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_15M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 5M ************************************************************************

			if (score_15M < max_score_15M):
				chrom_faild_15M += 1
				chrom_faild += 1

				Chromosome_15M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_15M[chrom_counter]['macd_fast'] >= Chromosome_15M[chrom_counter]['macd_slow']):#(chrom_faild_5M > (len(Chromosome_5M)/4)):
					##print('new baby 5M')
					Chromosome_15M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(5, 18)
						}
					chrom_faild_15M = 0
					score_15M = 0

					chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_15M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_15M)
				else:
					continue

			if (score_15M >= max_score_15M):
				chrom_faild_15M = 0
				try:
					max_score_15M = score_15M
					diff_plus_15M = diff_plus_15M/diff_counter
					diff_minus_15M = diff_minus_15M/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_15M.items()}

					percentage_sell_tp_save_15M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_15M.items()}

					percentage_sell_st_save_15M = max(res.values())

					if percentage_sell_tp_save_15M != 0:
						data_save_15M[chorm_save_counter_15M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_15M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_15M,
						'st': percentage_sell_st_save_15M,
						'signal': 'sell',
						'score': score_15M,
						'macd_fast': Chromosome_15M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_15M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_15M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_15M,
						'diff_minus': diff_minus_15M
						}
						chorm_save_counter_15M += 1

						if (score_15M >= 195): faild_flag = num_turn + 1
					score_15M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_15M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				#chrom_counter = 0

				chrom_faild = 0
				chrom_faild_15M = 0

				Chromosome_15M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_15M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_15M.values()])
			max_find_15M = {}
			min_find_15M = {}
			max_find_tp_15M = {}
			counter_find = 0
			for i in data_save_15M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_15M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_15M.values()])

			counter_find = 0
			for i in max_find_15M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_15M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_15M.values()])

			counter_find = 0
			for i in max_find_tp_15M.values():
				if abs(i['st']) == min_st:
					min_find_15M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_15M[0]['apply_to'],'tp' : min_find_15M[0]['tp'], 'st' : min_find_15M[0]['st'],
			'macd_fast': min_find_15M[0]['macd_fast'] , 'macd_slow': min_find_15M[0]['macd_slow'], 'macd_signal': min_find_15M[0]['macd_signal']
			,'diff_plus':min_find_15M[0]['diff_plus'] , 'diff_minus': min_find_15M[0]['diff_minus']
			,'score': min_find_15M[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/15M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 15M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#macd_genetic_sell_algo_15M(0.04,3,2,50)





#***********///////////********************************** BUY ALGO 1H *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_1H(tp_limit,max_num_trade,num_turn,max_score_1H):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)

	chorm_signal_cross_1H = {}
	sym_counter = 0

	print('**************************** START MACD 1H BUY *********************************************')

	bar = Bar('Processing 1H BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1H = 0

		data_save_1H = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1H[7] = line
					
					Chromosome_1H[7]['macd_fast'] = float(Chromosome_1H[7]['macd_fast'])
					Chromosome_1H[7]['macd_slow'] = float(Chromosome_1H[7]['macd_slow'])
					Chromosome_1H[7]['macd_signal'] = float(Chromosome_1H[7]['macd_signal'])
			#continue


		chrom_faild = 0
		chrom_faild_1H = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1H):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_1H),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY 1H ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1H = 0
			tp_counter_1H = 0
			percentage_buy_tp_save_1H = {}
			percentage_buy_st_save_1H = {}
			percentage_sell_tp_save_1H = {}
			percentage_sell_st_save_1H = {}
			diff_minus_1H = 0
			diff_plus_1H = 0

			num_trade = 0

			diff_counter = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 1H Chorme *********************************************************************
				macd_all_1H = ind.macd(symbol_data_1H[sym.name][Chromosome_1H[chrom_counter]['apply_to']],fast=Chromosome_1H[chrom_counter]['macd_fast'], slow=Chromosome_1H[chrom_counter]['macd_slow'],signal=Chromosome_1H[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1H = macd_all_1H[macd_all_1H.columns[0]]
				macdh_1H = macd_all_1H[macd_all_1H.columns[1]]
				macds_1H = macd_all_1H[macd_all_1H.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1H)))

				signal_cross_1H = cross_macd(macd_1H,macds_1H,macdh_1H,sym.name,(((-1) * (abs(mean_macd)) * 1.5)),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1H['signal'] == 'buy')):

					signal_cross_1H['index'] += 3

					counter_i = signal_cross_1H['index']
					final_index = (len(macd_1H)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1H)-1)):
							final_index = (len(macd_1H)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['high'][signal_cross_1H['index']])/symbol_data_1H[sym.name]['high'][signal_cross_1H['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_1H[sym.name]['high'][signal_cross_1H['index']] - symbol_data_1H[sym.name]['low'][counter_i])/symbol_data_1H[sym.name]['high'][signal_cross_1H['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 30): break

					try:
						percentage_buy_tp_save_1H[tp_counter_1H] = max(percentage_buy_tp.values())
						percentage_buy_st_save_1H[tp_counter_1H] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_1H[tp_counter_1H] = 0
						percentage_buy_st_save_1H[tp_counter_1H] = 0

					if (percentage_buy_st_save_1H[tp_counter_1H] < 0): 
						percentage_buy_st_save_1H[tp_counter_1H] = 0
						score_1H += 0

					if (percentage_buy_st_save_1H[tp_counter_1H] > (spred+0.02)):
						score_1H -= 0

					if (percentage_buy_tp_save_1H[tp_counter_1H] > (spred+tp_limit)): 
						score_1H += 1

						diff_plus_1H += (signal_cross_1H['diff_plus'] * 0.8)
						diff_minus_1H += (signal_cross_1H['diff_minus'] * 0.8)

						diff_counter += 1

						if (abs(percentage_buy_st_save_1H[tp_counter_1H]) >= abs(percentage_buy_tp_save_1H[tp_counter_1H])):
							score_1H -= 1
						else:
							score_1H += 1

					if (percentage_buy_tp_save_1H[tp_counter_1H] <= (spred+tp_limit)): 
						score_1H -= 1
						percentage_buy_tp_save_1H[tp_counter_1H] = -1000

					


					num_trade += 1


					tp_counter_1H += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1H['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1H = (score_1H/num_trade) * 100

			if (num_trade < max_num_trade): score_1H = -10

			#print('*************************************** score_1H = ',score_1H,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1H) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 1H ************************************************************************

			if (score_1H < max_score_1H):
				chrom_faild_1H += 1
				chrom_faild += 1

				Chromosome_1H[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1H[chrom_counter]['macd_fast'] >= Chromosome_1H[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1H[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1H = 0
					score_1H = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1H)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1H)
				else:
					continue

			if (score_1H >= max_score_1H):
				chrom_faild_1H = 0
				try:
					max_score_1H = score_1H
					diff_plus_1H = diff_plus_1H/diff_counter
					diff_minus_1H = diff_minus_1H/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_1H.items()}

					percentage_buy_tp_save_1H = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_1H.items()}

					percentage_buy_st_save_1H = max(res.values())

					if percentage_buy_tp_save_1H != 0:
						data_save_1H[chorm_save_counter_1H] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1H[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_1H,
						'st': percentage_buy_st_save_1H,
						'signal': 'buy',
						'score': score_1H,
						'macd_fast': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1H[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1H,
						'diff_minus': diff_minus_1H
						}
						chorm_save_counter_1H += 1

						if (score_1H >= 195): faild_flag = num_turn + 1
					score_1H = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1H)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_1H = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1H.values()])
			max_find_1H = {}
			min_find_1H = {}
			max_find_tp_1H = {}
			counter_find = 0
			for i in data_save_1H.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1H[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1H.values()])

			counter_find = 0
			for i in max_find_1H.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1H[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1H.values()])

			counter_find = 0
			for i in max_find_tp_1H.values():
				if abs(i['st']) == min_st:
					min_find_1H[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1H[0]['apply_to'],'tp' : min_find_1H[0]['tp'], 'st' : min_find_1H[0]['st'],
			'macd_fast': min_find_1H[0]['macd_fast'] , 'macd_slow': min_find_1H[0]['macd_slow'], 'macd_signal': min_find_1H[0]['macd_signal']
			,'diff_plus':min_find_1H[0]['diff_plus'] , 'diff_minus': min_find_1H[0]['diff_minus']
			,'score': min_find_1H[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/1H/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1H BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1H BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 1H *********///////////////////******************************************

def macd_genetic_sell_algo_1H(tp_limit,max_num_trade,num_turn,max_score_1H):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)

	chorm_signal_cross_1H = {}
	sym_counter = 0

	print('**************************** START MACD 1H SELL *********************************************')

	bar = Bar('Processing 1H SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1H = 0

		data_save_1H = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1H[7] = line
					
					Chromosome_1H[7]['macd_fast'] = float(Chromosome_1H[7]['macd_fast'])
					Chromosome_1H[7]['macd_slow'] = float(Chromosome_1H[7]['macd_slow'])
					Chromosome_1H[7]['macd_signal'] = float(Chromosome_1H[7]['macd_signal'])
			#continue

		chrom_faild = 0
		chrom_faild_1H = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1H):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_1H),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL 1H ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1H = 0
			tp_counter_1H = 0
			percentage_buy_tp_save_1H = {}
			percentage_buy_st_save_1H = {}
			percentage_sell_tp_save_1H = {}
			percentage_sell_st_save_1H = {}
			diff_minus_1H = 0
			diff_plus_1H = 0

			num_trade = 0

			diff_counter = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 1H Chorme *********************************************************************
				macd_all_1H = ind.macd(symbol_data_1H[sym.name][Chromosome_1H[chrom_counter]['apply_to']],fast=Chromosome_1H[chrom_counter]['macd_fast'], slow=Chromosome_1H[chrom_counter]['macd_slow'],signal=Chromosome_1H[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1H = macd_all_1H[macd_all_1H.columns[0]]
				macdh_1H = macd_all_1H[macd_all_1H.columns[1]]
				macds_1H = macd_all_1H[macd_all_1H.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1H)))

				signal_cross_1H = cross_macd(macd_1H,macds_1H,macdh_1H,sym.name,(((-1) * (abs(mean_macd)) * 1.5)),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1H['signal'] == 'sell')):

					signal_cross_1H['index'] += 3
					counter_i = signal_cross_1H['index']

					final_index = (len(macd_1H)-1)
					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1H)-1)):
							final_index = (len(macd_1H)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['low'][signal_cross_1H['index']])/symbol_data_1H[sym.name]['low'][signal_cross_1H['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_1H[sym.name]['low'][signal_cross_1H['index']] - symbol_data_1H[sym.name]['high'][counter_i])/symbol_data_1H[sym.name]['low'][signal_cross_1H['index']]) * 100

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 30): break

					try:
						percentage_sell_tp_save_1H[tp_counter_1H] = min(percentage_sell_tp.values())
						percentage_sell_st_save_1H[tp_counter_1H] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_1H[tp_counter_1H] = 0
						percentage_sell_st_save_1H[tp_counter_1H] = 0

					if (percentage_sell_st_save_1H[tp_counter_1H] > 0): 
						percentage_sell_st_save_1H[tp_counter_1H] = 0
						score_1H += 0

					if (percentage_sell_st_save_1H[tp_counter_1H] < (-1 * (spred+0.02))): 
						score_1H -= 0

					if (percentage_sell_tp_save_1H[tp_counter_1H] < (-1 * (spred+tp_limit))): 
						diff_plus_1H += (signal_cross_1H['diff_plus'] * 0.8)
						diff_minus_1H += (signal_cross_1H['diff_minus'] * 0.8)
						score_1H += 1

						diff_counter += 1

						if (abs(percentage_sell_st_save_1H[tp_counter_1H]) >= abs(percentage_sell_tp_save_1H[tp_counter_1H])):
							score_1H -= 1
						else:
							score_1H += 1

					if (percentage_sell_tp_save_1H[tp_counter_1H] >= (-1 * (spred+0.04))): 
						score_1H -= 1
						percentage_sell_tp_save_1H[tp_counter_1H] = 1000

					

					num_trade += 1


					tp_counter_1H += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1H['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1H = (score_1H/num_trade) * 100

			if (num_trade < max_num_trade): score_1H = -10

			#print('*************************************** score_1H = ',score_1H,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1H) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 1H ************************************************************************

			if (score_1H < max_score_1H):
				chrom_faild_1H += 1
				chrom_faild += 1

				Chromosome_1H[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1H[chrom_counter]['macd_fast'] >= Chromosome_1H[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1H[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1H = 0
					score_1H = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1H)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1H)
				else:
					continue

			if (score_1H >= max_score_1H):
				chrom_faild_1H = 0
				try:
					max_score_1H = score_1H
					diff_plus_1H = diff_plus_1H/diff_counter
					diff_minus_1H = diff_minus_1H/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_1H.items()}

					percentage_sell_tp_save_1H = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_1H.items()}

					percentage_sell_st_save_1H = max(res.values())

					if percentage_sell_tp_save_1H != 0:
						data_save_1H[chorm_save_counter_1H] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1H[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_1H,
						'st': percentage_sell_st_save_1H,
						'signal': 'sell',
						'score': score_1H,
						'macd_fast': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1H[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1H,
						'diff_minus': diff_minus_1H
						}
						chorm_save_counter_1H += 1

						if (score_1H >= 195): faild_flag = num_turn + 1
					score_1H = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1H)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0

				chrom_faild = 0
				chrom_faild_1H = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1H.values()])
			max_find_1H = {}
			min_find_1H = {}
			max_find_tp_1H = {}
			counter_find = 0
			for i in data_save_1H.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1H[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1H.values()])

			counter_find = 0
			for i in max_find_1H.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1H[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1H.values()])

			counter_find = 0
			for i in max_find_tp_1H.values():
				if abs(i['st']) == min_st:
					min_find_1H[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1H[0]['apply_to'],'tp' : min_find_1H[0]['tp'], 'st' : min_find_1H[0]['st'],
			'macd_fast': min_find_1H[0]['macd_fast'] , 'macd_slow': min_find_1H[0]['macd_slow'], 'macd_signal': min_find_1H[0]['macd_signal']
			,'diff_plus':min_find_1H[0]['diff_plus'] , 'diff_minus': min_find_1H[0]['diff_minus']
			,'score': min_find_1H[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/1H/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1H SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1H SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************



#***********///////////********************************** BUY ALGO 5M30M *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_5M30M(tp_limit,max_num_trade,num_turn,max_score_5M30M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	chorm_signal_cross_30M = {}
	chorm_signal_cross_5M = {}
	sym_counter = 0

	print('**************************** START MACD 5M30M BUY *********************************************')

	bar = Bar('Processing 5M30M BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		chorm_save_counter_5M30M = 0

		data_save_5M30M = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M30M_buy = line

					Chromosome_5M[7]['macd_fast'] = float(data_macd_5M30M_buy['macd_fast5M'])
					Chromosome_5M[7]['macd_slow'] = float(data_macd_5M30M_buy['macd_slow5M'])
					Chromosome_5M[7]['macd_signal'] = float(data_macd_5M30M_buy['macd_signal5M'])
					Chromosome_5M[7]['apply_to'] = data_macd_5M30M_buy['apply_to5M']

					Chromosome_30M[7]['macd_fast'] = float(data_macd_5M30M_buy['macd_fast30M'])
					Chromosome_30M[7]['macd_slow'] = float(data_macd_5M30M_buy['macd_slow30M'])
					Chromosome_30M[7]['macd_signal'] = float(data_macd_5M30M_buy['macd_signal30M'])
					Chromosome_30M[7]['apply_to'] = data_macd_5M30M_buy['apply_to30M']
			continue


		chrom_faild = 0

		chrom_faild_5M30M = 0

		faild_flag = 0

		window_end = 10000
		window_start = 0

		symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
		symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

		while chrom_counter < len(Chromosome_30M):
			window_end = 10000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY 5M30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end


			score_5M30M = 0
			tp_counter_5M30M = 0
			percentage_buy_tp_save_5M30M = {}
			percentage_buy_st_save_5M30M = {}
			percentage_sell_tp_save_5M30M = {}
			percentage_sell_st_save_5M30M = {}

			diff_minus_5M30M_5M = 0
			diff_plus_5M30M_5M = 0

			diff_minus_5M30M_30M = 0
			diff_plus_5M30M_30M = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,0,0)

				#******************************************* 5M Chorme *********************************************************************
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,0,0)

				#******************************************* 5M30M Chorme *********************************************************************

				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid
				spred = ((abs(price_ask-price_bid)/price_ask) * 100)

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

					percentage_buy_tp_save_5M30M[tp_counter_5M30M] = max(percentage_buy_tp.values())
					percentage_buy_st_save_5M30M[tp_counter_5M30M] = max(percentage_buy_st.values())

					if (percentage_buy_st_save_5M30M[tp_counter_5M30M] < 0): 
						percentage_buy_st_save_5M30M[tp_counter_5M30M] = 0
						score_5M30M += 0

					if (percentage_buy_st_save_5M30M[tp_counter_5M30M] > (spred+0.02)):
						score_5M30M -= 0

					if (percentage_buy_tp_save_5M30M[tp_counter_5M30M] > (spred+tp_limit)): 
						score_5M30M += 1
						diff_plus_5M30M_5M += signal_cross_5M['diff_plus']
						diff_minus_5M30M_5M += signal_cross_5M['diff_minus']

						diff_plus_5M30M_30M += signal_cross_30M['diff_plus']
						diff_minus_5M30M_30M += signal_cross_30M['diff_minus']

						if (abs(percentage_buy_st_save_5M30M[tp_counter_5M30M]) >= abs(percentage_buy_tp_save_5M30M[tp_counter_5M30M])):
							score_5M30M -= 1
						else:
							score_5M30M += 1

					if (percentage_buy_tp_save_5M30M[tp_counter_5M30M] <= (spred+tp_limit)): 
						score_5M30M -= 1
						percentage_buy_tp_save_5M30M[tp_counter_5M30M] = -1000

					

					num_trade += 1


					tp_counter_5M30M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_30M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_5M30M = (score_5M30M/num_trade) * 100

			if (num_trade < max_num_trade): score_5M30M = -10

			#print('*************************************** score_5M30M = ',score_5M30M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************

			#************************************************* Check save recreate 5M30M ************************************************************************

			if (score_5M30M < max_score_5M30M):
				chrom_faild_5M30M += 1
				chrom_faild += 1
				if True:#(chrom_faild_5M30M > (len(Chromosome_30M)/4)):
					##print('new baby 5M30M')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_5M30M = 0
					score_5M30M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_5M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_5M)
				else:
					continue

			if (score_5M30M >= max_score_5M30M):
				chrom_faild_5M30M = 0
				try:
					max_score_5M30M = score_5M30M
					
					diff_plus_5M30M_5M = diff_plus_5M30M_5M/tp_counter_5M30M
					diff_minus_5M30M_5M = diff_minus_5M30M_5M/tp_counter_5M30M

					diff_plus_5M30M_30M = diff_plus_5M30M_30M/tp_counter_5M30M
					diff_minus_5M30M_30M = diff_minus_5M30M_30M/tp_counter_5M30M

					res = {key : abs(val) for key, val in percentage_buy_tp_save_5M30M.items()}

					percentage_buy_tp_save_5M30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_5M30M.items()}

					percentage_buy_st_save_5M30M = max(res.values())

					if percentage_buy_tp_save_5M30M != 0:
						data_save_5M30M[chorm_save_counter_5M30M] = {
						'symbol': sym.name,
						'apply_to5M': Chromosome_5M[chrom_counter]['apply_to'],
						'apply_to30M': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_5M30M,
						'st': percentage_buy_st_save_5M30M,
						'signal': 'sell',
						'score': score_5M30M,
						'macd_fast5M': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow5M': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal5M': Chromosome_5M[chrom_counter]['macd_signal'],
						'macd_fast30M': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow30M': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal30M': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus5M': diff_plus_5M30M_5M,
						'diff_minus5M': diff_minus_5M30M_5M,
						'diff_plus30M': diff_plus_5M30M_30M,
						'diff_minus30M': diff_minus_5M30M_30M
						}
						chorm_save_counter_5M30M += 1

						if (score_5M30M >= 195): faild_flag = num_turn + 1
					score_5M30M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_5M30M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************
		
		try:
			max_score = max([abs(i['score']) for i in data_save_5M30M.values()])
			max_find_5M30M = {}
			min_find_5M30M = {}
			max_find_tp_5M30M = {}
			counter_find = 0
			for i in data_save_5M30M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_5M30M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_5M30M.values()])

			counter_find = 0
			for i in max_find_5M30M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_5M30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_5M30M.values()])

			counter_find = 0
			for i in max_find_tp_5M30M.values():
				if abs(i['st']) == min_st:
					min_find_5M30M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')


		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv')

			add_row = {'apply_to5M': min_find_5M30M[0]['apply_to5M'],'apply_to30M': min_find_5M30M[0]['apply_to30M'],
			'tp' : min_find_5M30M[0]['tp'], 'st' : min_find_5M30M[0]['st'],
			'macd_fast5M': min_find_5M30M[0]['macd_fast5M'] , 'macd_slow5M': min_find_5M30M[0]['macd_slow5M'], 'macd_signal5M': min_find_5M30M[0]['macd_signal5M'],
			'macd_fast30M': min_find_5M30M[0]['macd_fast30M'] , 'macd_slow30M': min_find_5M30M[0]['macd_slow30M'], 'macd_signal30M': min_find_5M30M[0]['macd_signal30M']
			,'diff_plus5M':min_find_5M30M[0]['diff_plus5M'] , 'diff_minus5M': min_find_5M30M[0]['diff_minus5M']
			,'diff_plus30M':min_find_5M30M[0]['diff_plus30M'] , 'diff_minus30M': min_find_5M30M[0]['diff_minus30M']
			,'score': min_find_5M30M[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to5M','apply_to30M','tp','st','macd_fast5M','macd_slow5M','macd_signal5M',
				   'macd_fast30M','macd_slow30M','macd_signal30M','diff_plus5M','diff_minus5M','diff_plus30M','diff_minus30M','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 5M30M BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 5M30M BUY *********************************************')

		#*****************************////////////******************************************************************

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 5M30M *********///////////////////******************************************

def macd_genetic_sell_algo_5M30M(tp_limit,max_num_trade,num_turn,max_score_5M30M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	chorm_signal_cross_30M = {}
	chorm_signal_cross_5M = {}

	sym_counter = 0

	print('**************************** START MACD 5M30M SELL *********************************************')

	bar = Bar('Processing 5M30M SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		chorm_save_counter_5M30M = 0

		data_save_5M30M = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_5M30M_sell = line

					Chromosome_5M[7]['macd_fast'] = float(data_macd_5M30M_sell['macd_fast5M'])
					Chromosome_5M[7]['macd_slow'] = float(data_macd_5M30M_sell['macd_slow5M'])
					Chromosome_5M[7]['macd_signal'] = float(data_macd_5M30M_sell['macd_signal5M'])
					Chromosome_5M[7]['apply_to'] = data_macd_5M30M_sell['apply_to5M']

					Chromosome_30M[7]['macd_fast'] = float(data_macd_5M30M_sell['macd_fast30M'])
					Chromosome_30M[7]['macd_slow'] = float(data_macd_5M30M_sell['macd_slow30M'])
					Chromosome_30M[7]['macd_signal'] = float(data_macd_5M30M_sell['macd_signal30M'])
					Chromosome_30M[7]['apply_to'] = data_macd_5M30M_sell['apply_to30M']
			continue


		chrom_faild = 0

		chrom_faild_5M30M = 0

		faild_flag = 0

		window_end = 10000
		window_start = 0

		symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
		symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

		while chrom_counter < len(Chromosome_30M):
			window_end = 10000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL 5M30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_5M30M = 0
			tp_counter_5M30M = 0
			percentage_buy_tp_save_5M30M = {}
			percentage_buy_st_save_5M30M = {}
			percentage_sell_tp_save_5M30M = {}
			percentage_sell_st_save_5M30M = {}
			
			diff_minus_5M30M_5M = 0
			diff_plus_5M30M_5M = 0

			diff_minus_5M30M_30M = 0
			diff_plus_5M30M_30M = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 5M Chorme *********************************************************************
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 5M30M Chorme *********************************************************************

				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid
				spred = ((abs(price_ask-price_bid)/price_ask) * 100)


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
					percentage_sell_tp_save_5M30M[tp_counter_5M30M] = min(percentage_sell_tp.values())
					percentage_sell_st_save_5M30M[tp_counter_5M30M] = min(percentage_sell_st.values())

					if (percentage_sell_st_save_5M30M[tp_counter_5M30M] > 0): 
						percentage_sell_st_save_5M30M[tp_counter_5M30M] = 0
						score_5M30M += 0

					if (percentage_sell_st_save_5M30M[tp_counter_5M30M] < (-1 * (spred+0.02))): 
						score_5M30M -= 0

					if (percentage_sell_tp_save_5M30M[tp_counter_5M30M] < (-1 * (spred+0.04))): 

						diff_plus_5M30M_5M += signal_cross_5M['diff_plus']
						diff_minus_5M30M_5M += signal_cross_5M['diff_minus']

						diff_plus_5M30M_30M += signal_cross_30M['diff_plus']
						diff_minus_5M30M_30M += signal_cross_30M['diff_minus']
						score_5M30M += 1
						if (abs(percentage_sell_st_save_5M30M[tp_counter_5M30M]) >= abs(percentage_sell_tp_save_5M30M[tp_counter_5M30M])):
							score_5M30M -= 1
						else:
							score_5M30M += 1

					if (percentage_sell_tp_save_5M30M[tp_counter_5M30M] >= (-1 * (spred+0.04))): 
						score_5M30M -= 1
						percentage_sell_tp_save_5M30M[tp_counter_5M30M] = 1000
					

					num_trade += 1


					tp_counter_5M30M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_30M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_5M30M = (score_5M30M/num_trade) * 100

			if (num_trade < max_num_trade): score_5M30M = -10

			#print('*************************************** score_5M30M = ',score_5M30M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 5M30M ************************************************************************

			if (score_5M30M < max_score_5M30M):
				chrom_faild_5M30M += 1
				chrom_faild += 1
				if True:#(chrom_faild_5M30M > (len(Chromosome_30M)/4)):
					##print('new baby 5M30M')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_5M30M = 0
					score_5M30M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_5M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_5M)
				else:
					continue

			if (score_5M30M >= max_score_5M30M):
				chrom_faild_5M30M = 0
				print('5M30M save')
				try:
					max_score_5M30M = score_5M30M
					
					diff_plus_5M30M_5M = diff_plus_5M30M_5M/tp_counter_5M30M
					diff_minus_5M30M_5M = diff_minus_5M30M_5M/tp_counter_5M30M

					diff_plus_5M30M_30M = diff_plus_5M30M_30M/tp_counter_5M30M
					diff_minus_5M30M_30M = diff_minus_5M30M_30M/tp_counter_5M30M


					res = {key : abs(val) for key, val in percentage_sell_tp_save_5M30M.items()}

					percentage_sell_tp_save_5M30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_5M30M.items()}

					percentage_sell_st_save_5M30M = max(res.values())

					if percentage_sell_tp_save_5M30M != 0:
						data_save_5M30M[chorm_save_counter_5M30M] = {
						'symbol': sym.name,
						'apply_to5M': Chromosome_5M[chrom_counter]['apply_to'],
						'apply_to30M': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_5M30M,
						'st': percentage_sell_st_save_5M30M,
						'signal': 'sell',
						'score': score_5M30M,
						'macd_fast5M': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow5M': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal5M': Chromosome_5M[chrom_counter]['macd_signal'],
						'macd_fast30M': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow30M': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal30M': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus5M': diff_plus_5M30M_5M,
						'diff_minus5M': diff_minus_5M30M_5M,
						'diff_plus30M': diff_plus_5M30M_30M,
						'diff_minus30M': diff_minus_5M30M_30M
						}
						chorm_save_counter_5M30M += 1

						if (score_5M30M >= 195): faild_flag = num_turn + 1
					score_5M30M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0

				chrom_faild = 0

				chrom_faild_5M30M = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_5M30M.values()])
			max_find_5M30M = {}
			min_find_5M30M = {}
			max_find_tp_5M30M = {}
			counter_find = 0
			for i in data_save_5M30M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_5M30M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_5M30M.values()])

			counter_find = 0
			for i in max_find_5M30M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_5M30M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_5M30M.values()])

			counter_find = 0
			for i in max_find_tp_5M30M.values():
				if abs(i['st']) == min_st:
					min_find_5M30M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv')

			add_row = {'apply_to5M': min_find_5M30M[0]['apply_to5M'],'apply_to30M': min_find_5M30M[0]['apply_to30M'],
			'tp' : min_find_5M30M[0]['tp'], 'st' : min_find_5M30M[0]['st'],
			'macd_fast5M': min_find_5M30M[0]['macd_fast5M'] , 'macd_slow5M': min_find_5M30M[0]['macd_slow5M'], 'macd_signal5M': min_find_5M30M[0]['macd_signal5M'],
			'macd_fast30M': min_find_5M30M[0]['macd_fast30M'] , 'macd_slow30M': min_find_5M30M[0]['macd_slow30M'], 'macd_signal30M': min_find_5M30M[0]['macd_signal30M']
			,'diff_plus5M':min_find_5M30M[0]['diff_plus5M'] , 'diff_minus5M': min_find_5M30M[0]['diff_minus5M']
			,'diff_plus30M':min_find_5M30M[0]['diff_plus30M'] , 'diff_minus30M': min_find_5M30M[0]['diff_minus30M']
			,'score': min_find_5M30M[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to5M','apply_to30M','tp','st','macd_fast5M','macd_slow5M','macd_signal5M',
				   'macd_fast30M','macd_slow30M','macd_signal30M','diff_plus5M','diff_minus5M','diff_plus30M','diff_minus30M','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 5M30M SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 5M30M SELL *********************************************')
		#*****************************////////////******************************************************************


#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** BUY ALGO porro *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_porro(tp_limit,max_num_trade,num_turn,max_score_porro):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	chorm_signal_cross_30M = {}
	chorm_signal_cross_5M = {}
	chorm_signal_cross_1H = {}
	sym_counter = 0

	print('**************************** START MACD poroo BUY *********************************************')

	bar = Bar('Processing Porro BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		chorm_save_counter_porro = 0

		data_save_porro = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_porro_buy = line

					Chromosome_5M[7]['macd_fast'] = float(data_macd_porro_buy['macd_fast5M'])
					Chromosome_5M[7]['macd_slow'] = float(data_macd_porro_buy['macd_slow5M'])
					Chromosome_5M[7]['macd_signal'] = float(data_macd_porro_buy['macd_signal5M'])
					Chromosome_5M[7]['apply_to'] = data_macd_porro_buy['apply_to5M']

					Chromosome_30M[7]['macd_fast'] = float(data_macd_porro_buy['macd_fast30M'])
					Chromosome_30M[7]['macd_slow'] = float(data_macd_porro_buy['macd_slow30M'])
					Chromosome_30M[7]['macd_signal'] = float(data_macd_porro_buy['macd_signal30M'])
					Chromosome_30M[7]['apply_to'] = data_macd_porro_buy['apply_to30M']

					Chromosome_1H[7]['macd_fast'] = float(data_macd_porro_buy['macd_fast1H'])
					Chromosome_1H[7]['macd_slow'] = float(data_macd_porro_buy['macd_slow1H'])
					Chromosome_1H[7]['macd_signal'] = float(data_macd_porro_buy['macd_signal1H'])
					Chromosome_1H[7]['apply_to'] = data_macd_porro_buy['apply_to1H']
			continue


		chrom_faild = 0

		chrom_faild_porro = 0

		faild_flag = 0

		window_end = 10000
		window_start = 0

		symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
		symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)
		symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

		while chrom_counter < len(Chromosome_30M):
			window_end = 10000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY PORRO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_porro = 0
			tp_counter_porro = 0
			percentage_buy_tp_save_porro = {}
			percentage_buy_st_save_porro = {}
			percentage_sell_tp_save_porro = {}
			percentage_sell_st_save_porro = {}
			
			diff_minus_porro_5M = 0
			diff_plus_porro_5M = 0

			diff_minus_porro_1H = 0
			diff_plus_porro_1H = 0

			diff_minus_porro_30M = 0
			diff_plus_porro_30M = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 5M Chorme *********************************************************************
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 1H Chorme *********************************************************************
				macd_all_1H = ind.macd(symbol_data_1H[sym.name][Chromosome_1H[chrom_counter]['apply_to']],fast=Chromosome_1H[chrom_counter]['macd_fast'], slow=Chromosome_1H[chrom_counter]['macd_slow'],signal=Chromosome_1H[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1H = macd_all_1H[macd_all_1H.columns[0]]
				macdh_1H = macd_all_1H[macd_all_1H.columns[1]]
				macds_1H = macd_all_1H[macd_all_1H.columns[2]]

				signal_cross_1H = cross_macd(macd_1H,macds_1H,macdh_1H,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* porro Chorme *********************************************************************

				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid
				spred = ((abs(price_ask-price_bid)/price_ask) * 100)

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

					percentage_buy_tp_save_porro[tp_counter_porro] = max(percentage_buy_tp.values())
					percentage_buy_st_save_porro[tp_counter_porro] = max(percentage_buy_st.values())

					if (percentage_buy_st_save_porro[tp_counter_porro] < 0): 
						percentage_buy_st_save_porro[tp_counter_porro] = 0
						score_porro += 0

					if (percentage_buy_st_save_porro[tp_counter_porro] > (spred+0.02)):
						score_porro -= 0

					if (percentage_buy_tp_save_porro[tp_counter_porro] > (spred+tp_limit)): 
						score_porro += 1
						diff_plus_porro_5M += signal_cross_5M['diff_plus']
						diff_minus_porro_5M += signal_cross_5M['diff_minus']

						diff_plus_porro_1H += signal_cross_1H['diff_plus']
						diff_minus_porro_1H += signal_cross_1H['diff_minus']

						diff_plus_porro_30M += signal_cross_30M['diff_plus']
						diff_minus_porro_30M += signal_cross_30M['diff_minus']

						if (abs(percentage_buy_st_save_porro[tp_counter_porro]) >= abs(percentage_buy_tp_save_porro[tp_counter_porro])):
							score_porro -= 1
						else:
							score_porro += 1

					if (percentage_buy_tp_save_porro[tp_counter_porro] <= (spred+tp_limit)): 
						score_porro -= 1
						percentage_buy_tp_save_porro[tp_counter_porro] = -1000
					

					num_trade += 1


					tp_counter_porro += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_5M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_porro = (score_porro/num_trade) * 100

			if (num_trade < max_num_trade): score_porro = -10

			#print('*************************************** score_porro = ',score_porro,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate porro ************************************************************************

			if (score_porro < max_score_porro):
				chrom_faild_porro += 1
				chrom_faild += 1
				if True:#(chrom_faild_porro > (len(Chromosome_30M)/4)):
					##print('new baby porro')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_1H[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_porro = 0
					score_porro = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_30M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_30M)
				else:
					continue

			if (score_porro >= max_score_porro):
				chrom_faild_porro = 0
				try:
					max_score_porro = score_porro
					diff_plus_porro_5M = diff_plus_porro_5M/tp_counter_porro
					diff_minus_porro_5M = diff_minus_porro_5M/tp_counter_porro

					diff_plus_porro_1H = diff_plus_porro_1H/tp_counter_porro
					diff_minus_porro_1H = diff_minus_porro_1H/tp_counter_porro

					diff_plus_porro_30M = diff_plus_porro_30M/tp_counter_porro
					diff_minus_porro_30M = diff_minus_porro_30M/tp_counter_porro

					res = {key : abs(val) for key, val in percentage_buy_tp_save_porro.items()}

					percentage_buy_tp_save_porro = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_porro.items()}

					percentage_buy_st_save_porro = max(res.values())

					if percentage_buy_tp_save_porro != 0:
						data_save_porro[chorm_save_counter_porro] = {
						'symbol': sym.name,
						'apply_to5M': Chromosome_5M[chrom_counter]['apply_to'],
						'apply_to1H': Chromosome_1H[chrom_counter]['apply_to'],
						'apply_to30M': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_porro,
						'st': percentage_buy_st_save_porro,
						'signal': 'sell',
						'score': score_porro,
						'macd_fast5M': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow5M': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal5M': Chromosome_5M[chrom_counter]['macd_signal'],
						'macd_fast1H': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow1H': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal1H': Chromosome_1H[chrom_counter]['macd_signal'],
						'macd_fast30M': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow30M': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal30M': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus5M': diff_plus_porro_5M,
						'diff_minus5M': diff_minus_porro_5M,
						'diff_plus1H': diff_plus_porro_1H,
						'diff_minus1H': diff_minus_porro_1H,
						'diff_plus30M': diff_plus_porro_30M,
						'diff_minus30M': diff_minus_porro_30M
						}
						chorm_save_counter_porro += 1

						if (score_porro >= 195): faild_flag = num_turn + 1
					score_porro = 0
				except:
					print('fault')


			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0

				chrom_faild_porro = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************
		
		try:
			max_score = max([abs(i['score']) for i in data_save_porro.values()])
			max_find_porro = {}
			min_find_porro = {}
			max_find_tp_porro = {}
			counter_find = 0
			for i in data_save_porro.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_porro[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_porro.values()])

			counter_find = 0
			for i in max_find_porro.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_porro[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_porro.values()])

			counter_find = 0
			for i in max_find_tp_porro.values():
				if abs(i['st']) == min_st:
					min_find_porro[counter_find] = i
					counter_find += 1		
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************
		
		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv')

			add_row = {'apply_to5M': min_find_porro[0]['apply_to5M'],'apply_to1H': min_find_porro[0]['apply_to1H'],'apply_to30M': min_find_porro[0]['apply_to30M'],
			'tp' : min_find_porro[0]['tp'], 'st' : min_find_porro[0]['st'],
			'macd_fast5M': min_find_porro[0]['macd_fast5M'] , 'macd_slow5M': min_find_porro[0]['macd_slow5M'], 'macd_signal5M': min_find_porro[0]['macd_signal5M'],
			'macd_fast1H': min_find_porro[0]['macd_fast1H'] , 'macd_slow1H': min_find_porro[0]['macd_slow1H'], 'macd_signal1H': min_find_porro[0]['macd_signal1H'],
			'macd_fast30M': min_find_porro[0]['macd_fast30M'] , 'macd_slow30M': min_find_porro[0]['macd_slow30M'], 'macd_signal30M': min_find_porro[0]['macd_signal30M']
			,'diff_plus5M':min_find_porro[0]['diff_plus5M'] , 'diff_minus5M': min_find_porro[0]['diff_minus5M']
			,'diff_plus1H':min_find_porro[0]['diff_plus1H'] , 'diff_minus1H': min_find_porro[0]['diff_minus1H']
			,'diff_plus30M':min_find_porro[0]['diff_plus30M'] , 'diff_minus30M': min_find_porro[0]['diff_minus30M']
			,'score': min_find_porro[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/porro/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to5M','apply_to1H','apply_to30M','tp','st','macd_fast5M','macd_slow5M','macd_signal5M',
				   'macd_fast1H','macd_slow1H','macd_signal1H','macd_fast30M','macd_slow30M','macd_signal30M',
				   'diff_plus5M','diff_minus5M','diff_plus1H','diff_minus1H','diff_plus30M','diff_minus30M','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD porro BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD poroo BUY *********************************************')
		#*****************************////////////******************************************************************

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO porro *********///////////////////******************************************

def macd_genetic_sell_algo_porro(tp_limit,max_num_trade,num_turn,max_score_porro):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	
	#*************************** Algorithm *************************************************//
	
	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

	chorm_signal_cross_30M = {}
	chorm_signal_cross_5M = {}
	chorm_signal_cross_1H = {}
	sym_counter = 0

	print('**************************** START MACD poroo SELL *********************************************')

	bar = Bar('Processing Porro SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		chorm_save_counter_porro = 0

		data_save_porro = {}

		Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_macd_porro_sell = line

					Chromosome_5M[7]['macd_fast'] = float(data_macd_porro_sell['macd_fast5M'])
					Chromosome_5M[7]['macd_slow'] = float(data_macd_porro_sell['macd_slow5M'])
					Chromosome_5M[7]['macd_signal'] = float(data_macd_porro_sell['macd_signal5M'])
					Chromosome_5M[7]['apply_to'] = data_macd_porro_sell['apply_to5M']

					Chromosome_30M[7]['macd_fast'] = float(data_macd_porro_sell['macd_fast30M'])
					Chromosome_30M[7]['macd_slow'] = float(data_macd_porro_sell['macd_slow30M'])
					Chromosome_30M[7]['macd_signal'] = float(data_macd_porro_sell['macd_signal30M'])
					Chromosome_30M[7]['apply_to'] = data_macd_porro_sell['apply_to30M']

					Chromosome_1H[7]['macd_fast'] = float(data_macd_porro_sell['macd_fast1H'])
					Chromosome_1H[7]['macd_slow'] = float(data_macd_porro_sell['macd_slow1H'])
					Chromosome_1H[7]['macd_signal'] = float(data_macd_porro_sell['macd_signal1H'])
					Chromosome_1H[7]['apply_to'] = data_macd_porro_sell['apply_to30M']
			continue

		chrom_faild = 0

		chrom_faild_porro = 0

		faild_flag = 0

		window_end = 10000
		window_start = 0

		symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
		symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)
		symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

		while chrom_counter < len(Chromosome_30M):
			window_end = 10000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL PORRO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_porro = 0
			tp_counter_porro = 0
			percentage_sell_tp_save_porro = {}
			percentage_sell_st_save_porro = {}
			diff_minus_porro_5M = 0
			diff_plus_porro_5M = 0

			diff_minus_porro_1H = 0
			diff_plus_porro_1H = 0

			diff_minus_porro_30M = 0
			diff_plus_porro_30M = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				macd_all_30M = ind.macd(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to']],fast=Chromosome_30M[chrom_counter]['macd_fast'], slow=Chromosome_30M[chrom_counter]['macd_slow'],signal=Chromosome_30M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_30M = macd_all_30M[macd_all_30M.columns[0]]
				macdh_30M = macd_all_30M[macd_all_30M.columns[1]]
				macds_30M = macd_all_30M[macd_all_30M.columns[2]]

				signal_cross_30M = cross_macd(macd_30M,macds_30M,macdh_30M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 5M Chorme *********************************************************************
				macd_all_5M = ind.macd(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to']],fast=Chromosome_5M[chrom_counter]['macd_fast'], slow=Chromosome_5M[chrom_counter]['macd_slow'],signal=Chromosome_5M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_5M = macd_all_5M[macd_all_5M.columns[0]]
				macdh_5M = macd_all_5M[macd_all_5M.columns[1]]
				macds_5M = macd_all_5M[macd_all_5M.columns[2]]

				signal_cross_5M = cross_macd(macd_5M,macds_5M,macdh_5M,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* 1H Chorme *********************************************************************
				macd_all_1H = ind.macd(symbol_data_1H[sym.name][Chromosome_1H[chrom_counter]['apply_to']],fast=Chromosome_1H[chrom_counter]['macd_fast'], slow=Chromosome_1H[chrom_counter]['macd_slow'],signal=Chromosome_1H[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1H = macd_all_1H[macd_all_1H.columns[0]]
				macdh_1H = macd_all_1H[macd_all_1H.columns[1]]
				macds_1H = macd_all_1H[macd_all_1H.columns[2]]

				signal_cross_1H = cross_macd(macd_1H,macds_1H,macdh_1H,sym.name,0,0)

				#******************************************************///////*****************************************************************************

				#******************************************* porro Chorme *********************************************************************

				price_ask = mt5.symbol_info_tick(sym.name).ask
				price_bid = mt5.symbol_info_tick(sym.name).bid
				spred = ((abs(price_ask-price_bid)/price_ask) * 100)

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
					percentage_sell_tp_save_porro[tp_counter_porro] = min(percentage_sell_tp.values())
					percentage_sell_st_save_porro[tp_counter_porro] = min(percentage_sell_st.values())

					if (percentage_sell_st_save_porro[tp_counter_porro] > 0): 
						percentage_sell_st_save_porro[tp_counter_porro] = 0
						score_porro += 0

					if (percentage_sell_st_save_porro[tp_counter_porro] < (-1 * (spred+0.02))): 
						score_porro -= 0

					if (percentage_sell_tp_save_porro[tp_counter_porro] < (-1 * (spred+0.04))): 
						diff_plus_porro_5M += signal_cross_5M['diff_plus']
						diff_minus_porro_5M += signal_cross_5M['diff_minus']

						diff_plus_porro_1H += signal_cross_1H['diff_plus']
						diff_minus_porro_1H += signal_cross_1H['diff_minus']

						diff_plus_porro_30M += signal_cross_30M['diff_plus']
						diff_minus_porro_30M += signal_cross_30M['diff_minus']
						score_porro += 1

						if (abs(percentage_sell_st_save_porro[tp_counter_porro]) >= abs(percentage_sell_tp_save_porro[tp_counter_porro])):
							score_porro -= 1
						else:
							score_porro += 1

					if (percentage_sell_tp_save_porro[tp_counter_porro] >= (-1 * (spred+0.04))): 
						score_porro -= 1
						percentage_sell_tp_save_porro[tp_counter_porro] = 1000

					

					num_trade += 1


					tp_counter_porro += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_5M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_porro = (score_porro/num_trade) * 100

			if (num_trade < max_num_trade): score_porro = -10

			#print('*************************************** score_porro = ',score_porro,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_30M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate porro ************************************************************************

			if (score_porro < max_score_porro):
				chrom_faild_porro += 1
				chrom_faild += 1
				if True:#(chrom_faild_porro > (len(Chromosome_30M)/4)):
					##print('new baby porro')
					Chromosome_5M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_30M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					Chromosome_1H[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(20, 40),
						'macd_fast': randint(1, 20),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_porro = 0
					score_porro = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_30M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_30M)
				else:
					continue

			if (score_porro >= max_score_porro):
				chrom_faild_porro = 0
				print('porro save')
				try:
					max_score_porro = score_porro
					diff_plus_porro_5M = diff_plus_porro_5M/tp_counter_porro
					diff_minus_porro_5M = diff_minus_porro_5M/tp_counter_porro

					diff_plus_porro_1H = diff_plus_porro_1H/tp_counter_porro
					diff_minus_porro_1H = diff_minus_porro_1H/tp_counter_porro

					diff_plus_porro_30M = diff_plus_porro_30M/tp_counter_porro
					diff_minus_porro_30M = diff_minus_porro_30M/tp_counter_porro

					res = {key : abs(val) for key, val in percentage_sell_tp_save_porro.items()}

					percentage_sell_tp_save_porro = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_porro.items()}

					percentage_sell_st_save_porro = max(res.values())

					if percentage_sell_tp_save_porro != 0:
						data_save_porro[chorm_save_counter_porro] = {
						'symbol': sym.name,
						'apply_to5M': Chromosome_5M[chrom_counter]['apply_to'],
						'apply_to1H': Chromosome_1H[chrom_counter]['apply_to'],
						'apply_to30M': Chromosome_30M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_porro,
						'st': percentage_sell_st_save_porro,
						'signal': 'sell',
						'score': score_porro,
						'macd_fast5M': Chromosome_5M[chrom_counter]['macd_fast'],
						'macd_slow5M': Chromosome_5M[chrom_counter]['macd_slow'],
						'macd_signal5M': Chromosome_5M[chrom_counter]['macd_signal'],
						'macd_fast1H': Chromosome_1H[chrom_counter]['macd_fast'],
						'macd_slow1H': Chromosome_1H[chrom_counter]['macd_slow'],
						'macd_signal1H': Chromosome_1H[chrom_counter]['macd_signal'],
						'macd_fast30M': Chromosome_30M[chrom_counter]['macd_fast'],
						'macd_slow30M': Chromosome_30M[chrom_counter]['macd_slow'],
						'macd_signal30M': Chromosome_30M[chrom_counter]['macd_signal'],
						'diff_plus5M': diff_plus_porro_5M,
						'diff_minus5M': diff_minus_porro_5M,
						'diff_plus1H': diff_plus_porro_1H,
						'diff_minus1H': diff_minus_porro_1H,
						'diff_plus30M': diff_plus_porro_30M,
						'diff_minus30M': diff_minus_porro_30M
						}
						chorm_save_counter_porro += 1

						if (score_porro >= 195): faild_flag = num_turn + 1
					score_porro = 0
				except:
					print('fault')


			
			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_30M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0

				chrom_faild_porro = 0

				Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_porro.values()])
			max_find_porro = {}
			min_find_porro = {}
			max_find_tp_porro = {}
			counter_find = 0
			for i in data_save_porro.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_porro[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_porro.values()])

			counter_find = 0
			for i in max_find_porro.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_porro[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_porro.values()])

			counter_find = 0
			for i in max_find_tp_porro.values():
				if abs(i['st']) == min_st:
					min_find_porro[counter_find] = i
					counter_find += 1		
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv')

			add_row = {'apply_to5M': min_find_porro[0]['apply_to5M'],'apply_to1H': min_find_porro[0]['apply_to1H'],'apply_to30M': min_find_porro[0]['apply_to30M'],
			'tp' : min_find_porro[0]['tp'], 'st' : min_find_porro[0]['st'],
			'macd_fast5M': min_find_porro[0]['macd_fast5M'] , 'macd_slow5M': min_find_porro[0]['macd_slow5M'], 'macd_signal5M': min_find_porro[0]['macd_signal5M'],
			'macd_fast1H': min_find_porro[0]['macd_fast1H'] , 'macd_slow1H': min_find_porro[0]['macd_slow1H'], 'macd_signal1H': min_find_porro[0]['macd_signal1H'],
			'macd_fast30M': min_find_porro[0]['macd_fast30M'] , 'macd_slow30M': min_find_porro[0]['macd_slow30M'], 'macd_signal30M': min_find_porro[0]['macd_signal30M']
			,'diff_plus5M':min_find_porro[0]['diff_plus5M'] , 'diff_minus5M': min_find_porro[0]['diff_minus5M']
			,'diff_plus1H':min_find_porro[0]['diff_plus1H'] , 'diff_minus1H': min_find_porro[0]['diff_minus1H']
			,'diff_plus30M':min_find_porro[0]['diff_plus30M'] , 'diff_minus30M': min_find_porro[0]['diff_minus30M']
			,'score': min_find_porro[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/porro/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to5M','apply_to1H','apply_to30M','tp','st','macd_fast5M','macd_slow5M','macd_signal5M',
				   'macd_fast1H','macd_slow1H','macd_signal1H','macd_fast30M','macd_slow30M','macd_signal30M',
				   'diff_plus5M','diff_minus5M','diff_plus1H','diff_minus1H','diff_plus30M','diff_minus30M','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)	
		except:
			print('some thing wrong')

		print('************************MACD porro SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD poroo SELL *********************************************')
		#*****************************////////////******************************************************************



	#***********///////////********************************** BUY ALGO 1D *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_1D(tp_limit,max_num_trade,num_turn,max_score_1D):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

	window_end = 500
	window_start = 0

	symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,window_start,window_end)

	chorm_signal_cross_1D = {}
	sym_counter = 0

	print('**************************** START MACD 1D BUY *********************************************')

	bar = Bar('Processing 1D BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1D = 0

		data_save_1D = {}

		Chromosome_1D,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1D[7] = line

					Chromosome_1D[7]['macd_fast'] = float(Chromosome_1D[7]['macd_fast'])
					Chromosome_1D[7]['macd_slow'] = float(Chromosome_1D[7]['macd_slow'])
					Chromosome_1D[7]['macd_signal'] = float(Chromosome_1D[7]['macd_signal'])
			#continue


		chrom_faild = 0
		chrom_faild_1D = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1D):
			window_end = 500
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1D = 0
			tp_counter_1D = 0
			percentage_buy_tp_save_1D = {}
			percentage_buy_st_save_1D = {}
			percentage_sell_tp_save_1D = {}
			percentage_sell_st_save_1D = {}
			diff_minus_1D = 0
			diff_plus_1D = 0

			num_trade = 0

			diff_counter = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				macd_all_1D = ind.macd(symbol_data_1D[sym.name][Chromosome_1D[chrom_counter]['apply_to']],fast=Chromosome_1D[chrom_counter]['macd_fast'], slow=Chromosome_1D[chrom_counter]['macd_slow'],signal=Chromosome_1D[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1D = macd_all_1D[macd_all_1D.columns[0]]
				macdh_1D = macd_all_1D[macd_all_1D.columns[1]]
				macds_1D = macd_all_1D[macd_all_1D.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1D)))

				signal_cross_1D = cross_macd(macd_1D,macds_1D,macdh_1D,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1D['signal'] == 'buy')):

					signal_cross_1D['index'] += 3

					counter_i = signal_cross_1D['index']


					final_index = (len(macd_1D)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1D)-1)):
							final_index = (len(macd_1D)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_1D[sym.name]['close'][counter_i] - symbol_data_1D[sym.name]['high'][signal_cross_1D['index']])/symbol_data_1D[sym.name]['high'][signal_cross_1D['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_1D[sym.name]['high'][signal_cross_1D['index']] - symbol_data_1D[sym.name]['low'][counter_i])/symbol_data_1D[sym.name]['high'][signal_cross_1D['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 20): break

					try:
						percentage_buy_tp_save_1D[tp_counter_1D] = max(percentage_buy_tp.values())
						percentage_buy_st_save_1D[tp_counter_1D] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_1D[tp_counter_1D] = 0
						percentage_buy_st_save_1D[tp_counter_1D] = 0

					if (percentage_buy_st_save_1D[tp_counter_1D] < 0): 
						percentage_buy_st_save_1D[tp_counter_1D] = 0
						score_1D += 0

					if (percentage_buy_st_save_1D[tp_counter_1D] > (spred+0.02)):
						score_1D -= 0

					if (percentage_buy_tp_save_1D[tp_counter_1D] > (spred+tp_limit)): 
						score_1D += 1

						diff_plus_1D += (signal_cross_1D['diff_plus'] * 0.8)
						diff_minus_1D += (signal_cross_1D['diff_minus'] * 0.8)

						diff_counter += 1

						if (abs(percentage_buy_st_save_1D[tp_counter_1D]) >= abs(percentage_buy_tp_save_1D[tp_counter_1D])):
							score_1D -= 1
						else:
							score_1D += 1

					if (percentage_buy_tp_save_1D[tp_counter_1D] <= (spred+tp_limit)): 
						score_1D -= 1
						percentage_buy_tp_save_1D[tp_counter_1D] = -1000

					


					num_trade += 1


					tp_counter_1D += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1D['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1D = (score_1D/num_trade) * 100

			if (num_trade < max_num_trade):
				score_1D = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1D) + 1
				break
			#******************************************************* ////////// ********************************************************



			#************************************************* Check save recreate 1D ************************************************************************

			if (score_1D < max_score_1D):
				chrom_faild_1D += 1
				chrom_faild += 1

				Chromosome_1D[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1D[chrom_counter]['macd_fast'] >= Chromosome_1D[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1D[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1D = 0
					score_1D = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1D)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1D)
				else:
					continue

			if (score_1D >= max_score_1D):
				chrom_faild_1D = 0
				try:
					max_score_1D = score_1D
					diff_plus_1D = diff_plus_1D/diff_counter
					diff_minus_1D = diff_minus_1D/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_1D.items()}

					percentage_buy_tp_save_1D = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_1D.items()}

					percentage_buy_st_save_1D = max(res.values())

					if percentage_buy_tp_save_1D != 0:
						data_save_1D[chorm_save_counter_1D] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1D[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_1D,
						'st': percentage_buy_st_save_1D,
						'signal': 'buy',
						'score': score_1D,
						'macd_fast': Chromosome_1D[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1D[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1D[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1D,
						'diff_minus': diff_minus_1D
						}
						chorm_save_counter_1D += 1

						if (score_1D >= 195): faild_flag = num_turn + 1
					score_1D = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1D)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_1D = 0

				Chromosome_1D,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1D,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1D.values()])
			max_find_1D = {}
			min_find_1D = {}
			max_find_tp_1D = {}
			counter_find = 0
			for i in data_save_1D.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1D[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1D.values()])

			counter_find = 0
			for i in max_find_1D.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1D[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1D.values()])

			counter_find = 0
			for i in max_find_tp_1D.values():
				if abs(i['st']) == min_st:
					min_find_1D[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1D[0]['apply_to'],'tp' : min_find_1D[0]['tp'], 'st' : min_find_1D[0]['st'],
			'macd_fast': min_find_1D[0]['macd_fast'] , 'macd_slow': min_find_1D[0]['macd_slow'], 'macd_signal': min_find_1D[0]['macd_signal']
			,'diff_plus':min_find_1D[0]['diff_plus'] , 'diff_minus': min_find_1D[0]['diff_minus']
			,'score': min_find_1D[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/1D/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1D BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1D BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 1D *********///////////////////******************************************

def macd_genetic_sell_algo_1D(tp_limit,max_num_trade,num_turn,max_score_1D):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

	window_end = 500
	window_start = 0

	symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,window_start,window_end)

	chorm_signal_cross_1D = {}
	sym_counter = 0

	print('**************************** START MACD 1D SELL *********************************************')

	bar = Bar('Processing 1D SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1D = 0

		data_save_1D = {}

		Chromosome_1D,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1D[7] = line

					Chromosome_1D[7]['macd_fast'] = float(Chromosome_1D[7]['macd_fast'])
					Chromosome_1D[7]['macd_slow'] = float(Chromosome_1D[7]['macd_slow'])
					Chromosome_1D[7]['macd_signal'] = float(Chromosome_1D[7]['macd_signal'])
			#continue

		chrom_faild = 0
		chrom_faild_1D = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1D):
			window_end = 500
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1D = 0
			tp_counter_1D = 0
			percentage_buy_tp_save_1D = {}
			percentage_buy_st_save_1D = {}
			percentage_sell_tp_save_1D = {}
			percentage_sell_st_save_1D = {}
			diff_minus_1D = 0
			diff_plus_1D = 0

			num_trade = 0

			diff_counter = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				macd_all_1D = ind.macd(symbol_data_1D[sym.name][Chromosome_1D[chrom_counter]['apply_to']],fast=Chromosome_1D[chrom_counter]['macd_fast'], slow=Chromosome_1D[chrom_counter]['macd_slow'],signal=Chromosome_1D[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1D = macd_all_1D[macd_all_1D.columns[0]]
				macdh_1D = macd_all_1D[macd_all_1D.columns[1]]
				macds_1D = macd_all_1D[macd_all_1D.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1D)))

				signal_cross_1D = cross_macd(macd_1D,macds_1D,macdh_1D,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1D['signal'] == 'sell')):

					signal_cross_1D['index'] += 3
					counter_i = signal_cross_1D['index']

					final_index = (len(macd_1D)-1)
					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1D)-1)):
							final_index = (len(macd_1D)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_1D[sym.name]['close'][counter_i] - symbol_data_1D[sym.name]['low'][signal_cross_1D['index']])/symbol_data_1D[sym.name]['low'][signal_cross_1D['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_1D[sym.name]['low'][signal_cross_1D['index']] - symbol_data_1D[sym.name]['high'][counter_i])/symbol_data_1D[sym.name]['low'][signal_cross_1D['index']]) * 100
						#print(percentage_sell_tp[counter_j])

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 20): break

					try:
						percentage_sell_tp_save_1D[tp_counter_1D] = min(percentage_sell_tp.values())
						percentage_sell_st_save_1D[tp_counter_1D] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_1D[tp_counter_1D] = 0
						percentage_sell_st_save_1D[tp_counter_1D] = 0
					#print('Max = ',percentage_sell_tp_save_1D[tp_counter_1D])

					if (percentage_sell_st_save_1D[tp_counter_1D] > 0): 
						percentage_sell_st_save_1D[tp_counter_1D] = 0
						score_1D += 0

					if (percentage_sell_st_save_1D[tp_counter_1D] < (-1 * (spred+0.02))): 
						score_1D -= 0

					if (percentage_sell_tp_save_1D[tp_counter_1D] < (-1 * (spred+tp_limit))): 
						diff_plus_1D += (signal_cross_1D['diff_plus'] * 0.8)
						diff_minus_1D += (signal_cross_1D['diff_minus'] * 0.8)
						score_1D += 1

						diff_counter += 1

						if (abs(percentage_sell_st_save_1D[tp_counter_1D]) >= abs(percentage_sell_tp_save_1D[tp_counter_1D])):
							score_1D -= 1
						else:
							score_1D += 1

					if (percentage_sell_tp_save_1D[tp_counter_1D] >= (-1 * (spred+0.04))): 
						score_1D -= 1
						percentage_sell_tp_save_1D[tp_counter_1D] = 1000

					

					num_trade += 1


					tp_counter_1D += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1D['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1D = (score_1D/num_trade) * 100

			if (num_trade < max_num_trade): score_1D = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1D) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 5M ************************************************************************

			if (score_1D < max_score_1D):
				chrom_faild_1D += 1
				chrom_faild += 1

				Chromosome_1D[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1D[chrom_counter]['macd_fast'] >= Chromosome_1D[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1D[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1D = 0
					score_1D = 0

					chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1D)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1D)
				else:
					continue

			if (score_1D >= max_score_1D):
				chrom_faild_1D = 0
				try:
					max_score_1D = score_1D
					diff_plus_1D = diff_plus_1D/diff_counter
					diff_minus_1D = diff_minus_1D/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_1D.items()}

					percentage_sell_tp_save_1D = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_1D.items()}

					percentage_sell_st_save_1D = max(res.values())

					if percentage_sell_tp_save_1D != 0:
						data_save_1D[chorm_save_counter_1D] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1D[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_1D,
						'st': percentage_sell_st_save_1D,
						'signal': 'sell',
						'score': score_1D,
						'macd_fast': Chromosome_1D[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1D[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1D[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1D,
						'diff_minus': diff_minus_1D
						}
						chorm_save_counter_1D += 1

						if (score_1D >= 195): faild_flag = num_turn + 1
					score_1D = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1D)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				#chrom_counter = 0

				chrom_faild = 0
				chrom_faild_1D = 0

				Chromosome_1D,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1D,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1D.values()])
			max_find_1D = {}
			min_find_1D = {}
			max_find_tp_1D = {}
			counter_find = 0
			for i in data_save_1D.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1D[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1D.values()])

			counter_find = 0
			for i in max_find_1D.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1D[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1D.values()])

			counter_find = 0
			for i in max_find_tp_1D.values():
				if abs(i['st']) == min_st:
					min_find_1D[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1D[0]['apply_to'],'tp' : min_find_1D[0]['tp'], 'st' : min_find_1D[0]['st'],
			'macd_fast': min_find_1D[0]['macd_fast'] , 'macd_slow': min_find_1D[0]['macd_slow'], 'macd_signal': min_find_1D[0]['macd_signal']
			,'diff_plus':min_find_1D[0]['diff_plus'] , 'diff_minus': min_find_1D[0]['diff_minus']
			,'score': min_find_1D[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/1D/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1D SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1D SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#********************************//////////////-----------+++++++++++++//////////////***************************************************************

#macd_genetic_buy_algo_1D(0.1,2,2,20)
#macd_genetic_sell_algo_1D(0.1,2,2,20)



#***********///////////********************************** BUY ALGO 1M *********///////////////////******************************************

#initilize_values()
def macd_genetic_buy_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

	window_end = 5000
	window_start = 0

	symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

	chorm_signal_cross_1M = {}
	sym_counter = 0

	print('**************************** START MACD 1M BUY *********************************************')

	bar = Bar('Processing 1M BUY MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1M = 0

		data_save_1M = {}

		Chromosome_1M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1M[7] = line

					Chromosome_1M[7]['macd_fast'] = float(Chromosome_1M[7]['macd_fast'])
					Chromosome_1M[7]['macd_slow'] = float(Chromosome_1M[7]['macd_slow'])
					Chromosome_1M[7]['macd_signal'] = float(Chromosome_1M[7]['macd_signal'])
			continue


		chrom_faild = 0
		chrom_faild_1M = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1M):
			window_end = 5000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ BUY 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1M = 0
			tp_counter_1M = 0
			percentage_buy_tp_save_1M = {}
			percentage_buy_st_save_1M = {}
			percentage_sell_tp_save_1M = {}
			percentage_sell_st_save_1M = {}
			diff_minus_1M = 0
			diff_plus_1M = 0

			num_trade = 0

			diff_counter = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				macd_all_1M = ind.macd(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to']],fast=Chromosome_1M[chrom_counter]['macd_fast'], slow=Chromosome_1M[chrom_counter]['macd_slow'],signal=Chromosome_1M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1M = macd_all_1M[macd_all_1M.columns[0]]
				macdh_1M = macd_all_1M[macd_all_1M.columns[1]]
				macds_1M = macd_all_1M[macd_all_1M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1M)))

				signal_cross_1M = cross_macd(macd_1M,macds_1M,macdh_1M,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1M['signal'] == 'buy')):
					signal_cross_1M['index'] += 3

					counter_i = signal_cross_1M['index']


					final_index = (len(macd_1M)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1M)-1)):
							final_index = (len(macd_1M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['high'][signal_cross_1M['index']])/symbol_data_1M[sym.name]['high'][signal_cross_1M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_1M[sym.name]['high'][signal_cross_1M['index']] - symbol_data_1M[sym.name]['low'][counter_i])/symbol_data_1M[sym.name]['high'][signal_cross_1M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 600): break

					try:
						percentage_buy_tp_save_1M[tp_counter_1M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_1M[tp_counter_1M] = max(percentage_buy_st.values())
					except:
						percentage_buy_tp_save_1M[tp_counter_1M] = 0
						percentage_buy_st_save_1M[tp_counter_1M] = 0

					if (percentage_buy_st_save_1M[tp_counter_1M] < 0): 
						percentage_buy_st_save_1M[tp_counter_1M] = 0
						score_1M += 0

					if (percentage_buy_st_save_1M[tp_counter_1M] > (spred+0.02)):
						score_1M -= 0

					if (percentage_buy_tp_save_1M[tp_counter_1M] > (spred+tp_limit)): 
						score_1M += 1

						diff_plus_1M += (signal_cross_1M['diff_plus'] * 0.8)
						diff_minus_1M += (signal_cross_1M['diff_minus'] * 0.8)

						diff_counter += 1

						if (abs(percentage_buy_st_save_1M[tp_counter_1M]) >= abs(percentage_buy_tp_save_1M[tp_counter_1M])):
							score_1M -= 1
						else:
							score_1M += 1

					if (percentage_buy_tp_save_1M[tp_counter_1M] <= (spred+tp_limit)): 
						score_1M -= 1
						percentage_buy_tp_save_1M[tp_counter_1M] = -1000

					


					num_trade += 1


					tp_counter_1M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1M = (score_1M/num_trade) * 100

			if (num_trade < max_num_trade):
				score_1M = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1M) + 1
				break
			#******************************************************* ////////// ********************************************************



			#************************************************* Check save recreate 1D ************************************************************************

			if (score_1M < max_score_1M):
				chrom_faild_1M += 1
				chrom_faild += 1

				Chromosome_1M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1M[chrom_counter]['macd_fast'] >= Chromosome_1M[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1M = 0
					score_1M = 0

					#chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1M)
				else:
					continue

			if (score_1M >= max_score_1M):
				chrom_faild_1M = 0
				try:
					max_score_1M = score_1M
					diff_plus_1M = diff_plus_1M/diff_counter
					diff_minus_1M = diff_minus_1M/diff_counter

					res = {key : abs(val) for key, val in percentage_buy_tp_save_1M.items()}

					percentage_buy_tp_save_1D = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_1M.items()}

					percentage_buy_st_save_1M = max(res.values())

					if percentage_buy_tp_save_1M != 0:
						data_save_1M[chorm_save_counter_1M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1M[chrom_counter]['apply_to'],
						'tp': percentage_buy_tp_save_1M,
						'st': percentage_buy_st_save_1M,
						'signal': 'buy',
						'score': score_1M,
						'macd_fast': Chromosome_1M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1M[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1M,
						'diff_minus': diff_minus_1M
						}
						chorm_save_counter_1M += 1

						if (score_1M >= 195): faild_flag = num_turn + 1
					score_1M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				chrom_counter = 0


				chrom_faild_1M = 0

				Chromosome_1M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1M.values()])
			max_find_1M = {}
			min_find_1M = {}
			max_find_tp_1M = {}
			counter_find = 0
			for i in data_save_1M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1M.values()])

			counter_find = 0
			for i in max_find_1M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1M.values()])

			counter_find = 0
			for i in max_find_tp_1M.values():
				if abs(i['st']) == min_st:
					min_find_1M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1M[0]['apply_to'],'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
			'macd_fast': min_find_1M[0]['macd_fast'] , 'macd_slow': min_find_1M[0]['macd_slow'], 'macd_signal': min_find_1M[0]['macd_signal']
			,'diff_plus':min_find_1M[0]['diff_plus'] , 'diff_minus': min_find_1M[0]['diff_minus']
			,'score': min_find_1M[0]['score']}

			with open("Genetic_macd_output_buy_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1M BUY sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 1M *********///////////////////******************************************

def macd_genetic_sell_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

	apply_to = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}


	

	#*************************** Algorithm *************************************************//
	
	#symbol_data_1D,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

	window_end = 5000
	window_start = 0

	symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

	chorm_signal_cross_1M = {}
	sym_counter = 0

	print('**************************** START MACD 1D SELL *********************************************')

	bar = Bar('Processing 1M SELL MACD = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1M = 0

		data_save_1M = {}

		Chromosome_1M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv'):
			with open("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					Chromosome_1M[7] = line

					Chromosome_1M[7]['macd_fast'] = float(Chromosome_1M[7]['macd_fast'])
					Chromosome_1M[7]['macd_slow'] = float(Chromosome_1M[7]['macd_slow'])
					Chromosome_1M[7]['macd_signal'] = float(Chromosome_1M[7]['macd_signal'])
			continue

		chrom_faild = 0
		chrom_faild_1M = 0

		faild_flag = 0

		

		while chrom_counter < len(Chromosome_1M):
			window_end = 5000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			#print('************************MACD sym number = = ',sym_counter,' ******************************************')
			#print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			window_counter = window_end

			score_1M = 0
			tp_counter_1M = 0
			percentage_buy_tp_save_1M = {}
			percentage_buy_st_save_1M = {}
			percentage_sell_tp_save_1M = {}
			percentage_sell_st_save_1M = {}
			diff_minus_1M = 0
			diff_plus_1M = 0

			num_trade = 0

			diff_counter = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				macd_all_1M = ind.macd(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to']],fast=Chromosome_1M[chrom_counter]['macd_fast'], slow=Chromosome_1M[chrom_counter]['macd_slow'],signal=Chromosome_1M[chrom_counter]['macd_signal'], verbose=True)[0:window_counter]


				macd_1M = macd_all_1M[macd_all_1M.columns[0]]
				macdh_1M = macd_all_1M[macd_all_1M.columns[1]]
				macds_1M = macd_all_1M[macd_all_1M.columns[2]]

				mean_macd = abs(pd.DataFrame.mean(abs(macd_1M)))

				signal_cross_1M = cross_macd(macd_1M,macds_1M,macdh_1M,sym.name,(((-1) * (abs(mean_macd))) * 1.5),(abs(mean_macd)) * 1.5)


				if ((signal_cross_1M['signal'] == 'sell')):
					signal_cross_1M['index'] += 3
					counter_i = signal_cross_1M['index']

					final_index = (len(macd_1M)-1)
					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(macd_1M)-1)):
							final_index = (len(macd_1M)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['low'][signal_cross_1M['index']])/symbol_data_1M[sym.name]['low'][signal_cross_1M['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_1M[sym.name]['low'][signal_cross_1M['index']] - symbol_data_1M[sym.name]['high'][counter_i])/symbol_data_1M[sym.name]['low'][signal_cross_1M['index']]) * 100
						#print(percentage_sell_tp[counter_j])

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 600): break

					try:
						percentage_sell_tp_save_1M[tp_counter_1M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_1M[tp_counter_1M] = min(percentage_sell_st.values())
					except:
						percentage_sell_tp_save_1M[tp_counter_1M] = 0
						percentage_sell_st_save_1M[tp_counter_1M] = 0
					#print('Max = ',percentage_sell_tp_save_1D[tp_counter_1D])

					if (percentage_sell_st_save_1M[tp_counter_1M] > 0): 
						percentage_sell_st_save_1M[tp_counter_1M] = 0
						score_1M += 0

					if (percentage_sell_st_save_1M[tp_counter_1M] < (-1 * (spred+0.02))): 
						score_1M -= 0

					if (percentage_sell_tp_save_1M[tp_counter_1M] < (-1 * (spred+tp_limit))): 

						diff_plus_1M += (signal_cross_1M['diff_plus'] * 0.8)
						diff_minus_1M += (signal_cross_1M['diff_minus'] * 0.8)
						
						score_1M += 1

						diff_counter += 1

						if (abs(percentage_sell_st_save_1M[tp_counter_1M]) >= abs(percentage_sell_tp_save_1M[tp_counter_1M])):
							score_1M -= 1
						else:
							score_1M += 1

					if (percentage_sell_tp_save_1M[tp_counter_1M] >= (-1 * (spred+0.04))): 
						score_1M -= 1
						percentage_sell_tp_save_1M[tp_counter_1M] = 1000

					

					num_trade += 1


					tp_counter_1M += 1

					#******************************************************///////*****************************************************************************
				window_counter = signal_cross_1M['index'] - 1

			if (num_trade == 0): num_trade = 100000
			score_1M = (score_1M/num_trade) * 100

			if (num_trade < max_num_trade): score_1M = -10

			#print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

			#******************************************************** faild break ***************************************************
			if (faild_flag >= num_turn):
				#print('faild flag')
				chrom_counter = len(Chromosome_1M) + 1
				break
			#******************************************************* ////////// ********************************************************


			#************************************************* Check save recreate 5M ************************************************************************

			if (score_1M < max_score_1M):
				chrom_faild_1M += 1
				chrom_faild += 1

				Chromosome_1M[chrom_counter] = {
					'apply_to': apply_to[randint(0, 7)],
					'macd_slow': randint(5, 50),
					'macd_fast': randint(5, 50),
					'macd_signal': randint(1, 18)
					}

				while (Chromosome_1M[chrom_counter]['macd_fast'] >= Chromosome_1M[chrom_counter]['macd_slow']):#(chrom_faild_30M > (len(Chromosome_30M)/4)):
					##print('new baby 30M')
					Chromosome_1M[chrom_counter] = {
						'apply_to': apply_to[randint(0, 7)],
						'macd_slow': randint(5, 50),
						'macd_fast': randint(5, 50),
						'macd_signal': randint(1, 18)
						}
					chrom_faild_1M = 0
					score_1M = 0

					chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_1M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_1M)
				else:
					continue

			if (score_1M >= max_score_1M):
				chrom_faild_1M = 0
				try:
					max_score_1M = score_1M
					diff_plus_1M = diff_plus_1M/diff_counter
					diff_minus_1M = diff_minus_1M/diff_counter

					res = {key : abs(val) for key, val in percentage_sell_tp_save_1M.items()}

					percentage_sell_tp_save_1M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_1M.items()}

					percentage_sell_st_save_1M = max(res.values())

					if percentage_sell_tp_save_1M != 0:
						data_save_1M[chorm_save_counter_1M] = {
						'symbol': sym.name,
						'apply_to': Chromosome_1M[chrom_counter]['apply_to'],
						'tp': percentage_sell_tp_save_1M,
						'st': percentage_sell_st_save_1M,
						'signal': 'sell',
						'score': score_1M,
						'macd_fast': Chromosome_1M[chrom_counter]['macd_fast'],
						'macd_slow': Chromosome_1M[chrom_counter]['macd_slow'],
						'macd_signal': Chromosome_1D[chrom_counter]['macd_signal'],
						'diff_plus': diff_plus_1M,
						'diff_minus': diff_minus_1M
						}
						chorm_save_counter_1M += 1

						if (score_1M >= 195): faild_flag = num_turn + 1
					score_1M = 0
				except:
					print('fault')

			

			#******************************************************/////////////////////************************************************************************

			chrom_counter += 1

			#************************************* Create Gen ***********************************************************************
			if (chrom_counter >= ((len(Chromosome_1M)))):
				chrom_faild = 0
				faild_flag += 1
				#print('Gen Create')

				#chrom_counter = 0

				chrom_faild = 0
				chrom_faild_1M = 0

				Chromosome_1M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1M,Chromosome_30M,Chromosome_1H)
				continue
			#************************************ /////////// ************************************************************************

		#**************************** Calc Max tp & Min st *********************************************************

		try:
			max_score = max([abs(i['score']) for i in data_save_1M.values()])
			max_find_1M = {}
			min_find_1M = {}
			max_find_tp_1M = {}
			counter_find = 0
			for i in data_save_1M.values():
				if ((abs((i['score'])) == max_score) & (max_score != 0)):
					max_find_1M[counter_find] = i
					counter_find += 1

			max_tp = max([abs(i['tp']) for i in max_find_1M.values()])

			counter_find = 0
			for i in max_find_1M.values():
				if abs(i['tp']) == max_tp:
					max_find_tp_1M[counter_find] = i
					counter_find += 1

			min_st = min([abs(i['st']) for i in max_find_tp_1M.values()])

			counter_find = 0
			for i in max_find_tp_1M.values():
				if abs(i['st']) == min_st:
					min_find_1M[counter_find] = i
					counter_find += 1
		except:
			print('Empty')

		#********************************///////////////****************************************************************

		#*************************** Save to TXT File ***************************************************************

		try:
			if os.path.exists("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv'):
				os.remove("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv')

			add_row = {'apply_to': min_find_1M[0]['apply_to'],'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
			'macd_fast': min_find_1M[0]['macd_fast'] , 'macd_slow': min_find_1M[0]['macd_slow'], 'macd_signal': min_find_1M[0]['macd_signal']
			,'diff_plus':min_find_1M[0]['diff_plus'] , 'diff_minus': min_find_1M[0]['diff_minus']
			,'score': min_find_1M[0]['score']}

			with open("Genetic_macd_output_sell_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to','tp','st','macd_fast','macd_slow','macd_signal','diff_plus','diff_minus','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		print('************************MACD 1M SELL sym number = = ',sym_counter,' ******************************************')
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#********************************//////////////-----------+++++++++++++//////////////***************************************************************

#macd_genetic_buy_algo_1M(0.1,2,2,20)
#macd_genetic_sell_algo_1M(0.1,2,2,20)		