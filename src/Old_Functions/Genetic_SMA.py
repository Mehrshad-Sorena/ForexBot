from random import seed
from random import randint
from log_get_data import *
from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
from SMA_Signal_Cross import *
import csv
import os
from progress.bar import Bar



def initilize_values():
	#************************** initialize Values ******************************************************
	Chromosome_5M = {}
	Chromosome_30M = {}
	Chromosome_1H = {}
	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 50,
	'period_high': 100
	}
	Chromosome_30M[0] = {
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 50,
	'period_high': 100
	}
	Chromosome_1H[0] = {
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 50,
	'period_high': 100
	}

	Chromosome_5M[1] = {
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 100,
	'period_high': 150
	}
	Chromosome_30M[1] = {
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 100,
	'period_high': 150
	}
	Chromosome_1H[1] = {
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'period_low': 100,
	'period_high': 150
	}
	i = 2
	while i < 8:
		Chromosome_5M[i] = {
			'apply_to_low': apply_to_low[randint(0, 7)],
			'apply_to_high': apply_to_high[randint(0, 7)],
			'period_low': randint(20, 80),
			'period_high': randint(80, 200)
		}

		Chromosome_30M[i] = {
			'apply_to_low': apply_to_low[randint(0, 7)],
			'apply_to_high': apply_to_high[randint(0, 7)],
			'period_low': randint(20, 80),
			'period_high': randint(80, 200)
		}
		Chromosome_1H[i] = {
			'apply_to_low': apply_to_low[randint(0, 7)],
			'apply_to_high': apply_to_high[randint(0, 7)],
			'period_low': randint(20, 80),
			'period_high': randint(80, 200)
		}
		res = list(Chromosome_5M[i].keys()) 
		#print(res[1])
		#print(Chromosome_5M[i][res[1]])
		i += 1

	#***********************************************************************************
	return Chromosome_5M, Chromosome_30M, Chromosome_1H

def gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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
			'apply_to_low': 0,
			'apply_to_high': 0,
			'period_low': 0,
			'period_high': 0
		}

		baby_30M[baby_counter_create] = {
			'apply_to_low': 0,
			'apply_to_high': 0,
			'period_low': 0,
			'period_high': 0
		}
		baby_5M[baby_counter_create] = {
			'apply_to_low': 0,
			'apply_to_high': 0,
			'period_low': 0,
			'period_high': 0
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
		'apply_to_low': apply_to_low[randint(0, 7)],
		'apply_to_high': apply_to_high[randint(0, 7)],
		'period_low': randint(20, 80),
		'period_high': randint(80, 200)
		}

		Chromosome_30M[i] = {
		#'sl': '',
		#'tp': '',
		#'diff_min_max': '',
		'apply_to_low': apply_to_low[randint(0, 7)],
		'apply_to_high': apply_to_high[randint(0, 7)],
		'period_low': randint(20, 80),
		'period_high': randint(80, 200)
		}
		Chromosome_1H[i] = {
		#'sl': '',
		#'tp': '',
		#'diff_min_max': '',
		'apply_to_low': apply_to_low[randint(0, 7)],
		'apply_to_high': apply_to_high[randint(0, 7)],
		'period_low': randint(20, 80),
		'period_high': randint(80, 200)
		}
		i += 1

	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome_5M[re_counter]['apply_to_low'] = baby_5M[re_counter]['apply_to_low']
		Chromosome_5M[re_counter]['apply_to_high'] = baby_5M[re_counter]['apply_to_high']
		Chromosome_5M[re_counter]['period_low'] = baby_5M[re_counter]['period_low']
		Chromosome_5M[re_counter]['period_high'] = baby_5M[re_counter]['period_high']
		re_counter += 1
		#print(Chromosome_5M[6])

	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome_30M[re_counter]['apply_to_low'] = baby_30M[re_counter]['apply_to_low']
		Chromosome_30M[re_counter]['apply_to_high'] = baby_30M[re_counter]['apply_to_high']
		Chromosome_30M[re_counter]['period_low'] = baby_30M[re_counter]['period_low']
		Chromosome_30M[re_counter]['period_high'] = baby_30M[re_counter]['period_high']
		re_counter += 1


	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome_1H[re_counter]['apply_to_low'] = baby_1H[re_counter]['apply_to_low']
		Chromosome_1H[re_counter]['apply_to_high'] = baby_1H[re_counter]['apply_to_high']
		Chromosome_1H[re_counter]['period_low'] = baby_1H[re_counter]['period_low']
		Chromosome_1H[re_counter]['period_high'] = baby_1H[re_counter]['period_high']
		re_counter += 1

	return Chromosome_5M,Chromosome_30M,Chromosome_1H



#***********///////////********************************** BUY ALGO 30M *********///////////////////******************************************

#initilize_values()
def SMA_genetic_buy_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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
	
	#symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)

	chorm_signal_cross_30M = {}
	sym_counter = 0

	print('**************************** START SMA 30M BUY *********************************************')

	bar = Bar('Processing 30M BUY SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_30M = 0

		data_save_30M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Buy_onebyone/30M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_30M[7] = line

					Chromosome_30M[7]['apply_to_low'] = Chromosome_30M[7]['apply_to_low']
					Chromosome_30M[7]['apply_to_high'] = Chromosome_30M[7]['apply_to_high']
					Chromosome_30M[7]['period_low'] = float(Chromosome_30M[7]['period_low'])
					Chromosome_30M[7]['period_high'] = float(Chromosome_30M[7]['period_high'])
			continue


		chrom_faild = 0
		chrom_faild_30M = 0

		faild_flag = 0

		print('************************ SMA 30M BUY sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_30M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			
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
				#print(Chromosome_30M[chrom_counter]['apply_to'])
				

				SMA_low = ind.sma(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to_low']],length=Chromosome_30M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to_high']],length=Chromosome_30M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_30M = cross_SMA(SMA_low,SMA_high,sym.name)

				#print('signal = ',signal_cross_30M)



				if ((signal_cross_30M['signal'] == 'buy')):

					signal_cross_30M['index'] += 3

					counter_i = signal_cross_30M['index']
					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][signal_cross_30M['index']])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][signal_cross_30M['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][signal_cross_30M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						#print('tp = ',percentage_buy_tp[counter_j])
						counter_i += 1
						counter_j += 1

						

						if (counter_j > 300): break

					try:
						percentage_buy_tp_save_30M[tp_counter_30M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_30M[tp_counter_30M] = max(percentage_buy_st.values())

						#print('max = ',percentage_buy_tp_save_30M[tp_counter_30M])
					except:
						percentage_buy_tp_save_30M[tp_counter_30M] = 0
						percentage_buy_st_save_30M[tp_counter_30M] = 0


					#print('max = ',percentage_buy_tp_save_30M[tp_counter_30M])

					#print('macd = ',macd_30M[len(macd_30M)-1])
					#print('mean = ',abs(mean_macd))

					if (percentage_buy_st_save_30M[tp_counter_30M] < 0): 
						percentage_buy_st_save_30M[tp_counter_30M] = 0
						score_30M += 0

					if (percentage_buy_st_save_30M[tp_counter_30M] > (spred+0.02)):
						score_30M -= 0

					if (percentage_buy_tp_save_30M[tp_counter_30M] > (spred+tp_limit)): 
						score_30M += 1

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

			if (num_trade < max_num_trade):
				score_30M = -10

			#print('score = ', score_30M)

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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 400),
					'period_high': randint(5, 400)
					}

				while ((Chromosome_30M[chrom_counter]['period_high'] - Chromosome_30M[chrom_counter]['period_low']) <= 50):
					Chromosome_30M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
							}
							
					while (Chromosome_30M[chrom_counter]['period_low'] >= Chromosome_30M[chrom_counter]['period_high']):
						Chromosome_30M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
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

					res = {key : abs(val) for key, val in percentage_buy_tp_save_30M.items()}

					percentage_buy_tp_save_30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_30M.items()}

					percentage_buy_st_save_30M = max(res.values())

					if percentage_buy_tp_save_30M != 0:
						if (Chromosome_30M[chrom_counter]['period_low'] >= Chromosome_30M[chrom_counter]['period_high']): 
							print('hello')
							continue
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_30M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_30M[chrom_counter]['apply_to_high'],
						'tp': percentage_buy_tp_save_30M,
						'st': percentage_buy_st_save_30M,
						'signal': 'buy',
						'score': score_30M,
						'period_low': Chromosome_30M[chrom_counter]['period_low'],
						'period_high': Chromosome_30M[chrom_counter]['period_high'],
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
			if os.path.exists("Genetic_SMA_Buy_onebyone/30M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Buy_onebyone/30M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_30M[0]['apply_to_low'],'apply_to_high': min_find_30M[0]['apply_to_high'],'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
			'period_low': min_find_30M[0]['period_low'] , 'period_high': min_find_30M[0]['period_high']
			,'score': min_find_30M[0]['score']}

			with open("Genetic_SMA_Buy_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		sym_counter += 1
		bar.next()

	print('**************************** Finish SMA 30M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_buy_algo_30M(0.04,3,3,50)

#***********///////////********************************** SELL ALGO 30M *********///////////////////******************************************

def SMA_genetic_sell_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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
	
	#symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

	window_end = 2000
	window_start = 0

	symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)

	chorm_signal_cross_30M = {}
	sym_counter = 0

	print('**************************** START SMA 30M SELL *********************************************')

	bar = Bar('Processing 30M SELL SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_30M = 0

		data_save_30M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Sell_onebyone/30M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_30M[7] = line

					Chromosome_30M[7]['apply_to_low'] = Chromosome_30M[7]['apply_to_low']
					Chromosome_30M[7]['apply_to_high'] = Chromosome_30M[7]['apply_to_high']
					Chromosome_30M[7]['period_low'] = float(Chromosome_30M[7]['period_low'])
					Chromosome_30M[7]['period_high'] = float(Chromosome_30M[7]['period_high'])
			continue


		chrom_faild = 0
		chrom_faild_30M = 0

		faild_flag = 0

		print('************************ SMA 30M SELL sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_30M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
			
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
			diff_counter = 0

			num_trade = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 30M Chorme *********************************************************************
				#print(Chromosome_30M[chrom_counter]['apply_to'])
				SMA_low = ind.sma(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to_low']],length=Chromosome_30M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_30M[sym.name][Chromosome_30M[chrom_counter]['apply_to_high']],length=Chromosome_30M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_30M = cross_SMA(SMA_low,SMA_high,sym.name)


				if ((signal_cross_30M['signal'] == 'sell')):

					signal_cross_30M['index'] += 3
					counter_i = signal_cross_30M['index']

					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

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

						if (counter_j > 300): break

					try:
						percentage_sell_tp_save_30M[tp_counter_30M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_30M[tp_counter_30M] = min(percentage_sell_st.values())

						#print('min = ',percentage_sell_tp_save_30M[tp_counter_30M])

					except:
						percentage_sell_tp_save_30M[tp_counter_30M] = 0
						percentage_sell_st_save_30M[tp_counter_30M] = 0


					if (percentage_sell_st_save_30M[tp_counter_30M] > 0): 
						percentage_sell_st_save_30M[tp_counter_30M] = 0
						score_30M += 0

					if (percentage_sell_st_save_30M[tp_counter_30M] < (-1 * (spred+0.02))): 
						score_30M -= 0

					if (percentage_sell_tp_save_30M[tp_counter_30M] < (-1 * (spred+tp_limit))): 
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

			if (num_trade < max_num_trade): score_30M = -10

			#print('score = ',score_30M)

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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 400),
					'period_high': randint(5, 400)
					}

				while ((Chromosome_30M[chrom_counter]['period_high'] - Chromosome_30M[chrom_counter]['period_low']) <= 50):
					Chromosome_30M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
							}
							
					while (Chromosome_30M[chrom_counter]['period_low'] >= Chromosome_30M[chrom_counter]['period_high']):
						Chromosome_30M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
							}
					chrom_faild_30M = 0
					score_30M = 0

					chrom_counter = 0

				if (chrom_faild >= ((len(Chromosome_30M)))):
					chrom_faild = 0
					chrom_counter = len(Chromosome_30M)
				else:
					continue

			if (score_30M >= max_score_30M):
				chrom_faild_30M = 0
				try:
					max_score_30M = score_30M

					res = {key : abs(val) for key, val in percentage_sell_tp_save_30M.items()}

					percentage_sell_tp_save_30M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_30M.items()}

					percentage_sell_st_save_30M = max(res.values())

					if percentage_sell_tp_save_30M != 0:
						if (Chromosome_30M[chrom_counter]['period_low'] >= Chromosome_30M[chrom_counter]['period_high']): 
							#print('hello')
							continue
						#print('yes')
						data_save_30M[chorm_save_counter_30M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_30M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_30M[chrom_counter]['apply_to_high'],
						'tp': percentage_sell_tp_save_30M,
						'st': percentage_sell_st_save_30M,
						'signal': 'sell',
						'score': score_30M,
						'period_low': Chromosome_30M[chrom_counter]['period_low'],
						'period_high': Chromosome_30M[chrom_counter]['period_high'],
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

				#chrom_counter = 0

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
			if os.path.exists("Genetic_SMA_Sell_onebyone/30M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Sell_onebyone/30M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_30M[0]['apply_to_low'],'apply_to_high': min_find_30M[0]['apply_to_high'],'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
			'period_low': min_find_30M[0]['period_low'] , 'period_high': min_find_30M[0]['period_high']
			,'score': min_find_30M[0]['score']}

			with open("Genetic_SMA_Sell_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 30M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_sell_algo_30M(0.04,3,2,50)
				

#***********///////////********************************** BUY ALGO 5M *********///////////////////******************************************

#initilize_values()
def SMA_genetic_buy_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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

	print('**************************** START SMA 5M BUY *********************************************')

	bar = Bar('Processing 5M BUY SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_5M = 0

		data_save_5M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Buy_onebyone/5M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_5M[7] = line

					Chromosome_5M[7]['apply_to_low'] = Chromosome_5M[7]['apply_to_low']
					Chromosome_5M[7]['apply_to_high'] = Chromosome_5M[7]['apply_to_high']
					Chromosome_5M[7]['period_low'] = float(Chromosome_5M[7]['period_low'])
					Chromosome_5M[7]['period_high'] = float(Chromosome_5M[7]['period_high'])
			#continue


		chrom_faild = 0
		chrom_faild_5M = 0

		faild_flag = 0

		print('************************ SMA 5M BUY sym number = = ',sym_counter,' ******************************************')

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
				

				SMA_low = ind.sma(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to_low']],length=Chromosome_5M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to_high']],length=Chromosome_5M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_5M = cross_SMA(SMA_low,SMA_high,sym.name)

				#print('signal = ',signal_cross_5M)



				if ((signal_cross_5M['signal'] == 'buy')):

					signal_cross_5M['index'] += 3

					counter_i = signal_cross_5M['index']
					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][signal_cross_5M['index']])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][signal_cross_5M['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][signal_cross_5M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						#print('tp = ',percentage_buy_tp[counter_j])
						counter_i += 1
						counter_j += 1

						

						if (counter_j > 300): break

					try:
						percentage_buy_tp_save_5M[tp_counter_5M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_5M[tp_counter_5M] = max(percentage_buy_st.values())

						#print('max = ',percentage_buy_tp_save_5M[tp_counter_5M])
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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 30),
					'period_high': randint(5, 40)
					}

				while ((Chromosome_5M[chrom_counter]['period_high'] - Chromosome_5M[chrom_counter]['period_low']) <= 2):
					Chromosome_5M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 30),
							'period_high': randint(5, 40)
							}
							
					while (Chromosome_5M[chrom_counter]['period_low'] >= Chromosome_5M[chrom_counter]['period_high']):
						Chromosome_5M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 30),
							'period_high': randint(5, 40)
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

					res = {key : abs(val) for key, val in percentage_buy_tp_save_5M.items()}

					percentage_buy_tp_save_5M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_5M.items()}

					percentage_buy_st_save_5M = max(res.values())

					if percentage_buy_tp_save_5M != 0:
						if (Chromosome_5M[chrom_counter]['period_low'] >= Chromosome_5M[chrom_counter]['period_high']): 
							print('hello')
							continue
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_5M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_5M[chrom_counter]['apply_to_high'],
						'tp': percentage_buy_tp_save_5M,
						'st': percentage_buy_st_save_5M,
						'signal': 'buy',
						'score': score_5M,
						'period_low': Chromosome_5M[chrom_counter]['period_low'],
						'period_high': Chromosome_5M[chrom_counter]['period_high'],
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
			if os.path.exists("Genetic_SMA_Buy_onebyone/5M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Buy_onebyone/5M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_5M[0]['apply_to_low'],'apply_to_high': min_find_5M[0]['apply_to_high'],'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
			'period_low': min_find_5M[0]['period_low'] , 'period_high': min_find_5M[0]['period_high']
			,'score': min_find_5M[0]['score']}

			with open("Genetic_SMA_Buy_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		sym_counter += 1
		bar.next()

	print('**************************** Finish SMA 5M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_buy_algo_5M(0.06,3,4,50)

#***********///////////********************************** SELL ALGO 5M *********///////////////////******************************************

def SMA_genetic_sell_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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

	print('**************************** START SMA 5M SELL *********************************************')

	bar = Bar('Processing 5M SELL SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_5M = 0

		data_save_5M = {}

		Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Sell_onebyone/5M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_5M[7] = line

					Chromosome_5M[7]['apply_to_low'] = Chromosome_5M[7]['apply_to_low']
					Chromosome_5M[7]['apply_to_high'] = Chromosome_5M[7]['apply_to_high']
					Chromosome_5M[7]['period_low'] = float(Chromosome_5M[7]['period_low'])
					Chromosome_5M[7]['period_high'] = float(Chromosome_5M[7]['period_high'])
			#continue


		chrom_faild = 0
		chrom_faild_5M = 0

		faild_flag = 0

		print('************************ SMA 5M SELL sym number = = ',sym_counter,' ******************************************')

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
				SMA_low = ind.sma(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to_low']],length=Chromosome_5M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_5M[sym.name][Chromosome_5M[chrom_counter]['apply_to_high']],length=Chromosome_5M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_5M = cross_SMA(SMA_low,SMA_high,sym.name)


				if ((signal_cross_5M['signal'] == 'sell')):

					signal_cross_5M['index'] += 3
					counter_i = signal_cross_5M['index']

					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 400),
					'period_high': randint(5, 400)
					}

				while ((Chromosome_5M[chrom_counter]['period_high'] - Chromosome_5M[chrom_counter]['period_low']) <= 100):
					Chromosome_5M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
							}
							
					while (Chromosome_5M[chrom_counter]['period_low'] >= Chromosome_5M[chrom_counter]['period_high']):
						Chromosome_5M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 400),
							'period_high': randint(5, 400)
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

					res = {key : abs(val) for key, val in percentage_sell_tp_save_5M.items()}

					percentage_sell_tp_save_5M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_5M.items()}

					percentage_sell_st_save_5M = max(res.values())

					if percentage_sell_tp_save_5M != 0:
						if (Chromosome_5M[chrom_counter]['period_low'] >= Chromosome_5M[chrom_counter]['period_high']): continue
						data_save_5M[chorm_save_counter_5M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_5M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_5M[chrom_counter]['apply_to_high'],
						'tp': percentage_sell_tp_save_5M,
						'st': percentage_sell_st_save_5M,
						'signal': 'sell',
						'score': score_5M,
						'period_low': Chromosome_5M[chrom_counter]['period_low'],
						'period_high': Chromosome_5M[chrom_counter]['period_high'],
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
			if os.path.exists("Genetic_SMA_Sell_onebyone/5M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Sell_onebyone/5M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_5M[0]['apply_to_low'],'apply_to_high': min_find_5M[0]['apply_to_high'],'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
			'period_low': min_find_5M[0]['period_low'] , 'period_high': min_find_5M[0]['period_high']
			,'score': min_find_5M[0]['score']}

			with open("Genetic_SMA_Sell_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 5M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_sell_algo_5M(0.04,3,5,50)



#***********///////////********************************** BUY ALGO 1M *********///////////////////******************************************

#initilize_values()
def SMA_genetic_buy_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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

	symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

	chorm_signal_cross_1M = {}
	sym_counter = 0

	print('**************************** START SMA 1M BUY *********************************************')

	bar = Bar('Processing 1M BUY SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1M = 0

		data_save_1M = {}

		Chromosome_1M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Buy_onebyone/1M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Buy_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_1M[7] = line

					Chromosome_1M[7]['apply_to_low'] = Chromosome_1M[7]['apply_to_low']
					Chromosome_1M[7]['apply_to_high'] = Chromosome_1M[7]['apply_to_high']
					Chromosome_1M[7]['period_low'] = float(Chromosome_1M[7]['period_low'])
					Chromosome_1M[7]['period_high'] = float(Chromosome_1M[7]['period_high'])
			#continue


		chrom_faild = 0
		chrom_faild_1M = 0

		faild_flag = 0

		print('************************ SMA 1M BUY sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_1M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
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

			diff_counter = 0

			num_trade = 0

			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				

				SMA_low = ind.sma(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to_low']],length=Chromosome_1M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to_high']],length=Chromosome_1M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_1M = cross_SMA(SMA_low,SMA_high,sym.name)

				#print('signal = ',signal_cross_5M)



				if ((signal_cross_1M['signal'] == 'buy')):

					signal_cross_1M['index'] += 3

					counter_i = signal_cross_1M['index']
					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_buy_tp = {}
					percentage_buy_st = {}


					while (counter_i <= final_index):
						percentage_buy_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['high'][signal_cross_1M['index']])/symbol_data_1M[sym.name]['high'][signal_cross_1M['index']]) * 100
						percentage_buy_st[counter_j] = ((symbol_data_1M[sym.name]['high'][signal_cross_1M['index']] - symbol_data_1M[sym.name]['low'][counter_i])/symbol_data_1M[sym.name]['high'][signal_cross_1M['index']]) * 100

						#if (percentage_buy_tp[counter_j] > (spred+tp_limit)): break
						#print('tp = ',percentage_buy_tp[counter_j])
						counter_i += 1
						counter_j += 1

						

						if (counter_j > 300): break

					try:
						percentage_buy_tp_save_1M[tp_counter_1M] = max(percentage_buy_tp.values())
						percentage_buy_st_save_1M[tp_counter_1M] = max(percentage_buy_st.values())

						#print('max = ',percentage_buy_tp_save_5M[tp_counter_5M])
					except:
						percentage_buy_tp_save_1M[tp_counter_1M] = 0
						percentage_buy_st_save_1M[tp_counter_1M] = 0


					#print('max = ',percentage_buy_tp_save_5M[tp_counter_5M])

					#print('macd = ',macd_5M[len(macd_5M)-1])
					#print('mean = ',abs(mean_macd))

					if (percentage_buy_st_save_1M[tp_counter_1M] < 0): 
						percentage_buy_st_save_1M[tp_counter_1M] = 0
						score_1M += 0

					if (percentage_buy_st_save_1M[tp_counter_1M] > (spred+0.02)):
						score_1M -= 0

					if (percentage_buy_tp_save_1M[tp_counter_1M] > (spred+tp_limit)): 
						score_1M += 1

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

			#print('score = ', score_5M)

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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 500),
					'period_high': randint(5, 500)
					}
				while ((Chromosome_1M[chrom_counter]['period_high'] - Chromosome_1M[chrom_counter]['period_low']) <= 100):
					Chromosome_1M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 500),
							'period_high': randint(5, 500)
							}

					while (Chromosome_1M[chrom_counter]['period_low'] >= Chromosome_1M[chrom_counter]['period_high']):
						Chromosome_1M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 500),
							'period_high': randint(5, 500)
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

					res = {key : abs(val) for key, val in percentage_buy_tp_save_1M.items()}

					percentage_buy_tp_save_1M = min(res.values())

					res = {key : abs(val) for key, val in percentage_buy_st_save_1M.items()}

					percentage_buy_st_save_1M = max(res.values())

					if percentage_buy_tp_save_1M != 0:
						if (Chromosome_1M[chrom_counter]['period_low'] >= Chromosome_1M[chrom_counter]['period_high']): continue
						data_save_1M[chorm_save_counter_1M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_1M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_1M[chrom_counter]['apply_to_high'],
						'tp': percentage_buy_tp_save_1M,
						'st': percentage_buy_st_save_1M,
						'signal': 'buy',
						'score': score_1M,
						'period_low': Chromosome_1M[chrom_counter]['period_low'],
						'period_high': Chromosome_1M[chrom_counter]['period_high'],
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
			if os.path.exists("Genetic_SMA_Buy_onebyone/1M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Buy_onebyone/1M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_1M[0]['apply_to_low'],'apply_to_high': min_find_1M[0]['apply_to_high'],'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
			'period_low': min_find_1M[0]['period_low'] , 'period_high': min_find_1M[0]['period_high']
			,'score': min_find_1M[0]['score']}

			with open("Genetic_SMA_Buy_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		sym_counter += 1
		bar.next()

	print('**************************** Finish SMA 1M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_buy_algo_1M(0.04,3,5,50)

#***********///////////********************************** SELL ALGO 1M *********///////////////////******************************************

def SMA_genetic_sell_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

	apply_to_low = {
		0: 'open',
		1: 'close',
		2: 'high',
		3: 'low',
		4: 'HL/2',
		5: 'HLC/3',
		6: 'HLCC/4',
		7: 'OHLC/4'
	}

	apply_to_high = {
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

	symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

	chorm_signal_cross_1M = {}
	sym_counter = 0

	print('**************************** START SMA 1M SELL *********************************************')

	bar = Bar('Processing 1M SELL SMA = ', max=73)
	print('\n')

	for sym in symbols:

		price_ask = mt5.symbol_info_tick(sym.name).ask
		price_bid = mt5.symbol_info_tick(sym.name).bid
		spred = ((abs(price_ask-price_bid)/price_ask) * 100)

		chorm_save_counter_1M = 0

		data_save_1M = {}

		Chromosome_1M,Chromosome_30M,Chromosome_1H = initilize_values()

		chrom_counter = 0

		if os.path.exists("Genetic_SMA_Sell_onebyone/1M/"+sym.name+'.csv'):
			with open("Genetic_SMA_Sell_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):

					Chromosome_1M[7] = line

					Chromosome_1M[7]['apply_to_low'] = Chromosome_1M[7]['apply_to_low']
					Chromosome_1M[7]['apply_to_high'] = Chromosome_1M[7]['apply_to_high']
					Chromosome_1M[7]['period_low'] = float(Chromosome_1M[7]['period_low'])
					Chromosome_1M[7]['period_high'] = float(Chromosome_1M[7]['period_high'])
			#continue


		chrom_faild = 0
		chrom_faild_1M = 0

		faild_flag = 0

		print('************************ SMA 1M SELL sym number = = ',sym_counter,' ******************************************')

		while chrom_counter < len(Chromosome_1M):
			window_end = 2000
			window_start = 0

			window_length = 10

			

			#print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
			
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
			diff_counter = 0

			num_trade = 0


			while window_counter > window_start:
				#print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

				#******************************************* 5M Chorme *********************************************************************
				#print(Chromosome_5M[chrom_counter]['apply_to'])
				SMA_low = ind.sma(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to_low']],length=Chromosome_1M[chrom_counter]['period_low'])[0:window_counter]
				SMA_high = ind.sma(symbol_data_1M[sym.name][Chromosome_1M[chrom_counter]['apply_to_high']],length=Chromosome_1M[chrom_counter]['period_high'])[0:window_counter]

				
				signal_cross_1M = cross_SMA(SMA_low,SMA_high,sym.name)


				if ((signal_cross_1M['signal'] == 'sell')):

					signal_cross_1M['index'] += 3
					counter_i = signal_cross_1M['index']

					final_index = (len(SMA_low)-1)

					if (final_index - counter_i) >= 20:
						#final_index = counter_i + 20
						if (final_index > (len(SMA_low)-1)):
							final_index = (len(SMA_low)-1)

					final_index = window_end - 1

					counter_j = 0

					percentage_sell_tp = {}
					percentage_sell_st = {}

					while (counter_i <= final_index):
						percentage_sell_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['low'][signal_cross_1M['index']])/symbol_data_1M[sym.name]['low'][signal_cross_1M['index']]) * 100
						percentage_sell_st[counter_j] = ((symbol_data_1M[sym.name]['low'][signal_cross_1M['index']] - symbol_data_1M[sym.name]['high'][counter_i])/symbol_data_1M[sym.name]['low'][signal_cross_1M['index']]) * 100

						#if (percentage_sell_tp[counter_j] < (-1 * (spred+tp_limit))): break
						counter_i += 1
						counter_j += 1

						if (counter_j > 300): break

					try:
						percentage_sell_tp_save_1M[tp_counter_1M] = min(percentage_sell_tp.values())
						percentage_sell_st_save_1M[tp_counter_1M] = min(percentage_sell_st.values())

					except:
						percentage_sell_tp_save_1M[tp_counter_1M] = 0
						percentage_sell_st_save_1M[tp_counter_1M] = 0


					if (percentage_sell_st_save_1M[tp_counter_1M] > 0): 
						percentage_sell_st_save_1M[tp_counter_1M] = 0
						score_1M += 0

					if (percentage_sell_st_save_1M[tp_counter_1M] < (-1 * (spred+0.02))): 
						score_1M -= 0

					if (percentage_sell_tp_save_1M[tp_counter_1M] < (-1 * (spred+tp_limit))): 
						score_1M += 1
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
					'apply_to_low': apply_to_low[randint(0, 7)],
					'apply_to_high': apply_to_high[randint(0, 7)],
					'period_low': randint(5, 500),
					'period_high': randint(5, 500)
					}

				while ((Chromosome_1M[chrom_counter]['period_high'] - Chromosome_1M[chrom_counter]['period_low']) <= 100):
					Chromosome_1M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 500),
							'period_high': randint(5, 500)
							}
							
					while (Chromosome_1M[chrom_counter]['period_low'] >= Chromosome_1M[chrom_counter]['period_high']):
						Chromosome_1M[chrom_counter] = {
							'apply_to_low': apply_to_low[randint(0, 7)],
							'apply_to_high': apply_to_high[randint(0, 7)],
							'period_low': randint(5, 500),
							'period_high': randint(5, 500)
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

					res = {key : abs(val) for key, val in percentage_sell_tp_save_1M.items()}

					percentage_sell_tp_save_1M = min(res.values())

					res = {key : abs(val) for key, val in percentage_sell_st_save_1M.items()}

					percentage_sell_st_save_1M = max(res.values())

					if percentage_sell_tp_save_1M != 0:
						if (Chromosome_1M[chrom_counter]['period_low'] >= Chromosome_1M[chrom_counter]['period_high']): continue
						data_save_1M[chorm_save_counter_1M] = {
						'symbol': sym.name,
						'apply_to_low': Chromosome_1M[chrom_counter]['apply_to_low'],
						'apply_to_high': Chromosome_1M[chrom_counter]['apply_to_high'],
						'tp': percentage_sell_tp_save_1M,
						'st': percentage_sell_st_save_1M,
						'signal': 'sell',
						'score': score_1M,
						'period_low': Chromosome_1M[chrom_counter]['period_low'],
						'period_high': Chromosome_1M[chrom_counter]['period_high'],
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
			if os.path.exists("Genetic_SMA_Sell_onebyone/1M/"+sym.name+'.csv'):
				os.remove("Genetic_SMA_Sell_onebyone/1M/"+sym.name+'.csv')

			add_row = {'apply_to_low': min_find_1M[0]['apply_to_low'],'apply_to_high': min_find_1M[0]['apply_to_high'],'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
			'period_low': min_find_1M[0]['period_low'] , 'period_high': min_find_1M[0]['period_high']
			,'score': min_find_1M[0]['score']}

			with open("Genetic_SMA_Sell_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
				   fields=['apply_to_low','apply_to_high','tp','st','period_low','period_high','score']
				   writer=csv.DictWriter(myfile,fieldnames=fields)
				   writer.writeheader()
				   writer.writerow(add_row)
		except:
			print('some thing wrong')

		
		sym_counter += 1
		bar.next()

	print('**************************** Finish MACD 1M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************
#SMA_genetic_sell_algo_1M(0.04,3,5,50)