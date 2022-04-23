import pandas as pd
import pandas_ta as ind
from log_get_data import *
from sklearn.cluster import KMeans
import math
from scipy import stats
from fitter import Fitter, get_common_distributions, get_distributions
import fitter
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from scipy.optimize import fsolve
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from numpy.random import randint
import numpy as np
from datetime import datetime
import logging
import sys
import os
from tqdm import tqdm
import csv

#**************************************** Logger *****************
now = datetime.now()
log_path = 'log/sma/golden_cross/{}-{}-{}-{}-{}-{}.log'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
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


def logs(message):
    logger.info(message)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ind.sma)

#**************************************************** Golden Cross *******************************************************
def golden_cross(dataset,Low_Period,High_Period,Low_ApplyTo,High_ApplyTo):

	x = np.arange(0,len(dataset[Low_ApplyTo]),1)

	SMA_Low = ind.sma(dataset[Low_ApplyTo], length = int(Low_Period))
	SMA_High = ind.sma(dataset[High_ApplyTo], length = int(High_Period))

	try:
		first_line = LineString(np.column_stack((x[(int(High_Period)-1):], SMA_Low[(int(High_Period)-1):])))
		second_line = LineString(np.column_stack((x[(int(High_Period)-1):], SMA_High.dropna())))
	except Exception as ex:
		logs("===> No SMA Cross")
		signal_buy = pd.DataFrame(np.zeros(1))
		signal_buy['signal'] = np.nan
		signal_buy['values'] = np.nan
		signal_buy['index'] = np.nan
		signal_buy['profit'] = np.nan

		signal_buy['signal'][0] = 'no_flag'
		signal_buy['values'][0] = -1
		signal_buy['index'][0] = -1
		signal_buy['profit'][0] = -1

		signal_sell = pd.DataFrame(np.zeros(1))
		signal_sell['signal'] = np.nan
		signal_sell['values'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['profit'] = np.nan

		signal_sell['signal'][0] = 'no_flag'
		signal_sell['values'][0] = -1
		signal_sell['index'][0] = -1
		signal_sell['profit'][0] = -1

		return signal_buy, signal_sell


	intersection = first_line.intersection(second_line)

	cross_find_flag = False

	if intersection.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection).xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index

		cross_find_flag = True
    
	elif intersection.geom_type == 'Point':
		cross = pd.DataFrame(*intersection.xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index

		cross_find_flag = True

	if not cross_find_flag:
		signal_buy = pd.DataFrame(np.zeros(1))
		signal_buy['signal'] = np.nan
		signal_buy['values'] = np.nan
		signal_buy['index'] = np.nan
		signal_buy['profit'] = np.nan

		signal_buy['signal'][0] = 'no_flag'
		signal_buy['values'][0] = -1
		signal_buy['index'][0] = -1
		signal_buy['profit'][0] = -1

		signal_sell = pd.DataFrame(np.zeros(1))
		signal_sell['signal'] = np.nan
		signal_sell['values'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['profit'] = np.nan

		signal_sell['signal'][0] = 'no_flag'
		signal_sell['values'][0] = -1
		signal_sell['index'][0] = -1
		signal_sell['profit'][0] = -1

		return signal_buy, signal_sell

	signal_buy = pd.DataFrame(np.zeros(len(cross['index'])))
	signal_buy['signal'] = np.nan
	signal_buy['values'] = np.nan
	signal_buy['index'] = np.nan
	signal_buy['profit'] = np.nan

	signal_buy['signal'][0] = 'no_flag'
	signal_buy['values'][0] = -1
	signal_buy['index'][0] = -1
	signal_buy['profit'][0] = -1

	signal_sell = pd.DataFrame(np.zeros(len(cross['index'])))
	signal_sell['signal'] = np.nan
	signal_sell['values'] = np.nan
	signal_sell['index'] = np.nan
	signal_sell['profit'] = np.nan

	signal_sell['signal'][0] = 'no_flag'
	signal_sell['values'][0] = -1
	signal_sell['index'][0] = -1
	signal_sell['profit'][0] = -1

	i = 0
	j = 0
	k = 0

	for elm in cross['index']:
		#print(elm)
		if ((SMA_Low[elm-1]<SMA_High[elm-1])&(SMA_Low[elm+1]>SMA_High[elm+1])):
			signal_buy['signal'][i] = 'buy'
			signal_buy['values'][i] = cross['values'][j]
			signal_buy['index'][i] = elm

			if ((j+1) < len(cross)):
				signal_buy['profit'][i] = (np.max(dataset['close'][elm:cross['index'][j+1]] - dataset['close'][elm])/dataset['close'][elm]) * 100
			else:
				signal_buy['profit'][i] = (np.max(dataset['close'][elm:-1] - dataset['close'][elm])/dataset['close'][elm]) * 100
			
			if np.isnan(signal_buy['profit'][i]): signal_buy['profit'][i] = 0

			i += 1

		elif ((SMA_Low[elm-1]>SMA_High[elm-1])&(SMA_Low[elm+1]<SMA_High[elm+1])):
			signal_sell['signal'][k] = 'sell'
			signal_sell['values'][k] = cross['values'][j]
			signal_sell['index'][k] = elm
			if ((j+1) < len(cross)):
				signal_sell['profit'][k] = (np.max(dataset['close'][elm] - dataset['close'][elm:cross['index'][j+1]])/np.min(dataset['close'][elm:cross['index'][j+1]])) * 100
			else:
				signal_sell['profit'][k] = (np.max(dataset['close'][elm] - dataset['close'][elm:-1])/np.min(dataset['close'][elm:-1])) * 100
			
			if np.isnan(signal_sell['profit'][k]): signal_sell['profit'][k] = 0
			k += 1
		j += 1


	signal_buy = signal_buy.dropna(inplace = False)
	signal_sell = signal_sell.dropna(inplace = False)

	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_sell = signal_sell.sort_values(by = ['index'])

	return signal_buy,signal_sell

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************* Genetic Algotithm ******************************************************************

#**************************************************** Create First Cromosomes *******************************************************
#@stTime

apply_to_list_ga = [
	'open',
	'close',
	'low',
	'high',
	'HL/2',
	'HLC/3',
	'HLCC/4',
	'OHLC/4'
	]

def initilize_values_genetic():
	#************************** initialize Values ******************************************************
	Chromosome = {}

	Chromosome[0] = {
	'high_period': 50,
	'low_period': 25,
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}

	Chromosome[1] = {
	'high_period': 100,
	'low_period': 50,
	'apply_to_low': 'close',
	'apply_to_high': 'close',
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}
	i = 2
	while i < 20:
		Chromosome[i] = {
			'high_period': randint(30, 400),
			'low_period': randint(10, 400),
			'apply_to_low': np.random.choice(apply_to_list_ga),
			'apply_to_high': np.random.choice(apply_to_list_ga),
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
		}
		if (Chromosome[i]['high_period'] < Chromosome[i]['low_period']): continue
		res = list(Chromosome[i].keys()) 
		#print(res[1])
		#print(Chromosome[i][res[1]])
		i += 1
	#***********************************************************************************
	return Chromosome
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#************************************************ Gen Creator ****************************************************************
def takeSecond(elem):
    return elem[1]

def scoring(buy_data, sell_data):
	buy_profit = buy_data['profit'] * 10
	sell_profit = sell_data['profit'] * 10

	success_score_buy = len(np.where(buy_profit > 0)[0]) - len(np.where(buy_profit <= 0)[0])
	success_score_sell = len(np.where(sell_profit > 0)[0]) - len(np.where(sell_profit <= 0)[0])

	if success_score_buy <= 0:
		success_score_buy = 1
	if success_score_sell <= 0:
		success_score_sell = 1

	profit_score_buy = 1
	profit_score_sell = 1
	for bf in buy_profit:
		if bf <= 0:
			bf = 1
		profit_score_buy *= bf

	for sf in sell_profit:
		if sf <= 0:
			sf = 1
		profit_score_sell *= sf

	score_buy = success_score_buy * profit_score_buy
	score_sell = success_score_sell * profit_score_sell

	return score_buy, score_sell


def find_max_score(chromosome_buy, chromosome_sell):

	buy = {}
	sell = {}
	max_buy = np.max(chromosome_buy['score_buy'])
	max_sell = np.max(chromosome_sell['score_sell'])

	max_buy_index = np.argmax(chromosome_buy['score_buy'])
	max_sell_index = np.argmax(chromosome_sell['score_sell'])

	print(chromosome_buy)

	buy.update(
		{
			'high_period': chromosome_buy['high_period'][max_buy_index],
			'low_period': chromosome_buy['low_period'][max_buy_index],
			'apply_to_low': chromosome_buy['apply_to_low'][max_buy_index],
			'apply_to_high': chromosome_buy['apply_to_high'][max_buy_index],
			'signal': chromosome_buy['signal'][max_buy_index],
			'score_buy': chromosome_buy['score_buy'][max_buy_index],
			'score_sell': chromosome_buy['score_buy'][max_buy_index]
		})
	
	sell.update(
		{
			'high_period': chromosome_sell['high_period'][max_sell_index],
			'low_period': chromosome_sell['low_period'][max_sell_index],
			'apply_to_low': chromosome_sell['apply_to_low'][max_sell_index],
			'apply_to_high': chromosome_sell['apply_to_high'][max_sell_index],
			'signal': chromosome_sell['signal'][max_sell_index],
			'score_buy': chromosome_sell['score_buy'][max_sell_index],
			'score_sell': chromosome_sell['score_sell'][max_sell_index]
		})

	return buy, sell


#@stTime
def gen_creator(Chromosome):

	Chromosome_Cutter = randint(0, 3)

	Chromosome_selector = randint(0, 19)

	baby = {}

	#print('Generate Baby')
	chrom_creator_counter = 0
	baby_counter = 0

	baby_counter_create = 0

	while (baby_counter_create < (len(Chromosome) * 2)):
		baby[baby_counter_create] = {
			'high_period': randint(30, 400),
			'low_period': randint(10, 400),
			'apply_to_low': np.random.choice(apply_to_list_ga),
			'apply_to_high': np.random.choice(apply_to_list_ga),
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
		}

		baby_counter_create += 1

	scr = []
	for k,v in zip(Chromosome.keys(), Chromosome.values()):
		scr.append([k, (v.get('score_buy') + v.get('score_sell'))/2])

	scr_idx = sorted(scr, key=takeSecond, reverse=True)[:int(len(Chromosome)/2)]

	while chrom_creator_counter < len(Chromosome):

		#********************************************* Baby ***********************************************************
		
		
		Chromosome_selector_1 = np.random.choice(len(scr_idx), size=1)[0]
		Chromosome_selector_2 = np.random.choice(len(scr_idx), size=1)[0]

		res_1 = list(Chromosome[Chromosome_selector_1].keys())
		res_2 = list(Chromosome[Chromosome_selector_2].keys())

		Chromosome_Cutter = randint(0, 3)
		change_chrom_counter = 0

		while change_chrom_counter < Chromosome_Cutter:
						#print(change_chrom_counter)
			baby[baby_counter].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})

			change_chrom_counter += 1

		change_chrom_counter = Chromosome_Cutter

		while change_chrom_counter < 4:
			baby[baby_counter].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			change_chrom_counter += 1

		baby_counter = baby_counter + 2

					#********************************************///////***************************************************************************
		chrom_creator_counter += 1

	i = 0
	limit_counter = len(Chromosome) * 2 
	while i < (limit_counter):
		Chromosome[i] = {
			'high_period': randint(30, 400),
			'low_period': randint(10, 400),
			'apply_to_low': np.random.choice(apply_to_list_ga),
			'apply_to_high': np.random.choice(apply_to_list_ga),
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
		}

		if (Chromosome[i]['high_period'] < Chromosome[i]['low_period']): continue
		i += 1

	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome[re_counter]['high_period'] = baby[re_counter]['high_period']
		Chromosome[re_counter]['low_period'] = baby[re_counter]['low_period']
		Chromosome[re_counter]['apply_to_low'] = baby[re_counter]['apply_to_low']
		Chromosome[re_counter]['apply_to_high'] = baby[re_counter]['apply_to_high']
		Chromosome[re_counter]['signal'] = baby[re_counter]['signal']
		Chromosome[re_counter]['score_buy'] = baby[re_counter]['score_buy']
		Chromosome[re_counter]['score_sell'] = baby[re_counter]['score_sell']
		re_counter += 1
		#print(Chromosome_5M[6])

	return Chromosome

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#***************************************** Genetic Algorithm **************************************************************

#@stTime
def genetic_buy_algo(symbol_data_5M,symbol,num_turn,max_score_ga_buy,max_score_ga_sell):

	#*************************** Algorithm *************************************************//
	trun_counter = 0
	Chromosome = initilize_values_genetic()

	print('**************************** START Genetic BUY ',symbol,'****************************')
	print('\n')

	now = datetime.now()

	logs('===============> {}'.format(symbol))

	if os.path.exists("GA/SMA/BUY/"+symbol+'.csv'):
		with open("GA/SMA/BUY/"+symbol+'.csv', 'r', newline='') as myfile:
			for line in csv.DictReader(myfile):
				Chromosome[19] = line
				Chromosome[19]['high_period'] = float(Chromosome[19]['high_period'])
				Chromosome[19]['low_period'] = float(Chromosome[19]['low_period'])
				Chromosome[19]['apply_to_low'] = Chromosome[19]['apply_to_low']
				Chromosome[19]['apply_to_high'] = Chromosome[19]['apply_to_high']
				Chromosome[19]['signal'] = Chromosome[19]['signal']
				Chromosome[19]['score_buy'] = float(Chromosome[19]['score_buy'])
				Chromosome[19]['score_sell'] = float(Chromosome[19]['score_sell'])
				max_score_ga_buy = float(Chromosome[19]['score_buy'])

	if os.path.exists("GA/SMA/SELL/"+symbol+'.csv'):
		with open("GA/SMA/SELL/"+symbol+'.csv', 'r', newline='') as myfile:
			for line in csv.DictReader(myfile):
				Chromosome[18] = line
				Chromosome[18]['high_period'] = float(Chromosome[18]['high_period'])
				Chromosome[18]['low_period'] = float(Chromosome[18]['low_period'])
				Chromosome[18]['apply_to_low'] = Chromosome[18]['apply_to_low']
				Chromosome[18]['apply_to_high'] = Chromosome[18]['apply_to_high']
				Chromosome[18]['signal'] = Chromosome[18]['signal']
				Chromosome[18]['score_buy'] = float(Chromosome[18]['score_buy'])
				Chromosome[18]['score_sell'] = float(Chromosome[18]['score_sell'])
				max_score_ga_sell = float(Chromosome[18]['score_sell'])


	chromosome_buy = pd.DataFrame()

	chromosome_sell = pd.DataFrame()

	chrom_counter = 0

	with tqdm(total=num_turn) as pbar:
		while chrom_counter < len(Chromosome):

			try:
				buy_data,sell_data = golden_cross(
					dataset=symbol_data_5M[symbol],
					Low_Period=Chromosome[chrom_counter]['low_period'],
					High_Period=Chromosome[chrom_counter]['high_period'],
					Low_ApplyTo=Chromosome[chrom_counter]['apply_to_low'],
					High_ApplyTo=Chromosome[chrom_counter]['apply_to_high']
					)
				flag_golden_cross = False
			except Exception as ex:
				print('getting error: ', ex)
				flag_golden_cross = True
				logging.debug(Chromosome[chrom_counter])

			if flag_golden_cross:
				logging.debug(Chromosome[chrom_counter])
				Chromosome.pop(chrom_counter)
				high_period = randint(30, 400)
				low_period = randint(10, 400)
				while high_period < low_period:
					high_period = randint(30, 400)
					low_period = randint(10, 400)

				Chromosome[chrom_counter] = {
					'high_period': high_period,
					'low_period': low_period,
					'apply_to_low': np.random.choice(apply_to_list_ga),
					'apply_to_high': np.random.choice(apply_to_list_ga),
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				continue

			score_buy,score_sell = scoring(buy_data,sell_data)

			#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				#logs('=======> BUY = {}'.format(buy_data))

			#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				#logs('=======> SELL = {}'.format(sell_data))

			if (
				score_buy < max_score_ga_buy
				):
					
				bad_buy = True
			else:
				Chromosome[chrom_counter]['signal'] = ('buy' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
				Chromosome[chrom_counter].update({'score_buy': score_buy })
				chromosome_buy = chromosome_buy.append(Chromosome[chrom_counter], ignore_index=True)
				


				bad_buy = False

			if (
				score_sell < max_score_ga_sell
				):
					
				bad_sell = True
			else:
				Chromosome[chrom_counter]['signal'] = ('sell' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
				Chromosome[chrom_counter].update({'score_sell': score_sell })
				chromosome_sell = chromosome_sell.append(Chromosome[chrom_counter], ignore_index=True)
				

				bad_sell = False

			if bad_buy == True or bad_sell == True:

				Chromosome.pop(chrom_counter)
				high_period = randint(30, 400)
				low_period = randint(10, 400)
				while high_period < low_period:
					high_period = randint(30, 400)
					low_period = randint(10, 400)



				Chromosome[chrom_counter] = {
					'high_period': high_period,
					'low_period': low_period,
					'apply_to_low': np.random.choice(apply_to_list_ga),
					'apply_to_high': np.random.choice(apply_to_list_ga),
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}

			logs('**************** num buy *****************')
			logs('=======> num buy = {}'.format(len(chromosome_buy)))

			logs('**************** num sell *****************')
			logs('=======> num sell = {}'.format(len(chromosome_sell)))
			

			pbar.update(int((len(chromosome_buy) + len(chromosome_sell))/2))

			if (trun_counter >= num_turn*5): 
				if (
					len(chromosome_buy) == 0 or
					len(chromosome_sell) == 0
					):
					return
				else:
					break
			trun_counter += 1

			if (
				len(chromosome_buy) >= int(num_turn/20) and
				len(chromosome_sell) >= int(num_turn/20)
				):
				break

			if (
				len(chromosome_buy) >= int(num_turn/12) or
				len(chromosome_sell) >= int(num_turn/12)
				):
				if (len(chromosome_buy) >= int(num_turn/12)) and (len(chromosome_sell) >= 1): break
				if (len(chromosome_sell) >= int(num_turn/12)) and (len(chromosome_buy) >= 1): break

			if Chromosome[chrom_counter]['signal'] is None: continue

			chrom_counter += 1
			if (chrom_counter >= ((len(Chromosome)))):
				chrom_counter = 0
				Chromosome = gen_creator(Chromosome)
				continue

			
	
	#**************************** Best Find *********************************************************

	#************ Best Find:
	bcb,bcs = find_max_score(chromosome_buy,chromosome_sell)
	best_chromosome_buy = pd.DataFrame()
	best_chromosome_sell = pd.DataFrame()

	best_chromosome_buy = best_chromosome_buy.append(bcb, ignore_index=True)
	best_chromosome_sell = best_chromosome_sell.append(bcs, ignore_index=True)
	#*************************** Save to TXT File ***************************************************************
	buy_path = "GA/SMA/BUY/" + symbol + '.csv'
	sell_path = "GA/SMA/SELL/" + symbol + '.csv'
	try:
		if os.path.exists(buy_path):
			os.remove(buy_path)

		best_chromosome_buy.to_csv(buy_path)		
	except Exception as ex:
		print('some thing wrong: ', ex)


	try:
		if os.path.exists(sell_path):
			os.remove(sell_path)

		best_chromosome_sell.to_csv(sell_path)
	except Exception as ex:
		print('some thing wrong: ', ex)

	print('/////////////////////// Finish Genetic BUY ',symbol,'///////////////////////////////////')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#********************** read GA result ****************************************************************************

#@stTime
def read_ga_result(symbol):
	buy_path = "GA/SMA/BUY/" + symbol + '.csv'
	sell_path = "GA/SMA/SELL/" + symbol + '.csv'
	if os.path.exists(buy_path):
		ga_result_buy = pd.read_csv(buy_path)

	if os.path.exists(sell_path):
		ga_result_sell = pd.read_csv(sell_path)

	return ga_result_buy, ga_result_sell
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Scalpe *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Find Best Intervals *******************************************************
def Find_Best_interval(dataset,period_low,period_high,Low_ApplyTo,High_ApplyTo,max_profit_buy,max_profit_sell,alpha_sell,alpha_buy):
	signal_buy,signal_sell = Golden_Cross_SMA(dataset=dataset,Low_Period=period_low,High_Period=period_high,Low_ApplyTo=Low_ApplyTo,High_ApplyTo=High_ApplyTo)

	signal_buy_good = signal_buy.drop(np.where(signal_buy['profit']<max_profit_buy)[0])
	signal_sell_good = signal_sell.drop(np.where(signal_sell['profit']<max_profit_sell)[0])

	SMA_Low = ind.sma(dataset[Low_ApplyTo], length = period_low)
	SMA_High = ind.sma(dataset[High_ApplyTo], length = period_high)

	ofset_buy = 1.000 + (max_profit_buy/100)
	ofset_sell = 1.000 - (max_profit_sell/100)

	#timeout = time.time() + 20  # timeout_break Sec from now
	while True:

		if (len(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))])-1) > (len(signal_buy_good['values'].to_numpy()) - 1):
			if (len(signal_buy_good['values'].to_numpy()) - 1) >= 10:
				n_clusters_buy = 10
			else:
				n_clusters_buy = len(signal_buy_good['values'].to_numpy()) - 1
		else:
			n_clusters_buy = len(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))])-1
		

		if (len(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))])-1) > (len(signal_sell_good['values'].to_numpy()) - 1):
			if (len(signal_sell_good['values'].to_numpy()) - 1) >= 10:
				n_clusters_sell = 10
			else:
				n_clusters_sell = len(signal_sell_good['values'].to_numpy()) - 1
		else:
			n_clusters_sell = len(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))])-1

		kmeans_sell = KMeans(n_clusters=n_clusters_sell, random_state=0,init='k-means++',n_init=10,max_iter=100)
		kmeans_buy = KMeans(n_clusters=n_clusters_buy, random_state=0,init='k-means++',n_init=10,max_iter=100)
		#Model Fitting
		kmeans_sell = kmeans_sell.fit(signal_sell_good['values'].to_numpy().reshape(-1,1), sample_weight= signal_sell_good['profit'].to_numpy())
		kmeans_buy = kmeans_buy.fit(signal_buy_good['values'].to_numpy().reshape(-1,1), sample_weight= signal_buy_good['profit'].to_numpy())
		
		Y_sell = kmeans_sell.cluster_centers_
		Y_buy = kmeans_buy.cluster_centers_

		#Power_low = kmeans_low.labels_
	
		Power_sell = kmeans_sell.fit_predict(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))].reshape(-1,1))
		#SMA_Low.dropna().to_numpy()[np.where(SMA_Low.dropna()>=(SMA_Low.dropna()[len(SMA_Low.dropna())-1] * ofset_sell))]
		Power_buy = kmeans_buy.fit_predict(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))].reshape(-1,1))
		#SMA_Low.dropna().to_numpy()[np.where(SMA_Low.dropna()<=(SMA_Low.dropna()[len(SMA_Low.dropna())-1] * ofset_buy))]
		#[np.where(y4>=y3[len(y3)-1])]

		
		X_sell = kmeans_sell.cluster_centers_
		X_buy = kmeans_buy.cluster_centers_

		Power_sell = np.bincount(Power_sell)
		Power_buy = np.bincount(Power_buy)

		if ((len(Y_sell) != len(X_sell)) | ((len(Y_buy) != len(X_buy)))):
			timeout = time.time() + timeout_break
			continue
		#if (time.time() > timeout):
			#return 'timeout.error'
		if ((len(Y_sell) == len(X_sell)) & ((len(Y_buy) == len(X_buy)))): break

	signal_sell_final = pd.DataFrame(X_sell, columns=['X'])
	signal_sell_final['Y'] = Y_sell
	signal_sell_final['power'] = Power_sell
	signal_sell_final = signal_sell_final.sort_values(by = ['X'])


	signal_buy_final = pd.DataFrame(X_buy, columns=['X'])
	signal_buy_final['Y'] = Y_buy
	signal_buy_final['power'] = Power_buy
	signal_buy_final = signal_buy_final.sort_values(by = ['X'])


	#Fitting Model Finding ****************************
	data_X_buy=np.zeros(np.sum(signal_buy_final['power']))
	data_X_sell=np.zeros(np.sum(signal_sell_final['power']))

	j = 0
	z = 0
	for elm in signal_sell_final['X']:
		k = 0
		while k < signal_sell_final['power'].to_numpy()[j]:
			data_X_sell[z] = elm
			k += 1
			z += 1
		j += 1

	j = 0
	z = 0
	for elm in signal_buy_final['X']:
		k = 0
		while k < signal_buy_final['power'].to_numpy()[j]:
			data_X_buy[z] = elm
			k += 1
			z += 1
		j += 1

	data_X_sell = np.sort(data_X_sell)
	data_X_buy = np.sort(data_X_buy)

	distributions_sell = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
	distributions_buy = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']

	#************************************ Finding Sell's ****************************

	while True:
		
		f_sell = Fitter(data = data_X_sell, xmin=np.min(data_X_sell), xmax=np.max(data_X_sell), bins = len(signal_sell_final['X']), distributions = distributions_sell, timeout=30, density=True)

		f_sell.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_sell = list(f_sell.get_best(method = 'sumsquare_error').items())
		dist_name_sell = items_sell[0][0]
		dist_parameters = items_sell[0][1]

		if dist_name_sell == 'foldnorm':
			Y = f_sell.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'dweibull':
			Y = f_sell.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
		
		elif dist_name_sell == 'rayleigh':
			Y = f_sell.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'expon':
			Y = f_sell.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'nakagami':
			Y = f_sell.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_sell, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_sell, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'norm':
			Y = f_sell.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_sell == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line_sell <= Upper_Line_sell)&(Mid_Line_sell >= Lower_Line_sell)): 
			break
		else:
			distributions_sell.remove(dist_name_sell)
			if (distributions_sell == None):
				#return 'timeout.error'
				pass

	#//////////////////////////////////////////////////////////////////////////////////////

	#timeout = time.time() + timeout_break  # timeout_break Sec from now
	#************************************ Finding High *************************************
	while True:
		
		f_buy = Fitter(data = data_X_buy, xmin=np.min(data_X_buy), xmax=np.max(data_X_buy), bins = len(signal_buy_final['X']), distributions = distributions_buy, timeout=30, density=True)

		f_buy.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_buy = list(f_buy.get_best(method = 'sumsquare_error').items())
		dist_name_buy = items_buy[0][0]
		dist_parameters = items_buy[0][1]

		if dist_name_buy == 'foldnorm':
			Y = f_buy.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
	
		elif dist_name_buy == 'dweibull':
			Y = f_buy.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'rayleigh':
			Y = f_buy.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'expon':
			Y = f_buy.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'nakagami':
			Y = f_buy.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_buy, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_buy, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'norm':
			Y = f_buy.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_buy == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line_buy <= Upper_Line_buy)&(Mid_Line_buy >= Lower_Line_buy)): 
			break
		else:
			distributions_buy.remove(dist_name_buy)
			if (distributions_buy == None):
				#return 'timeout.error'
				pass

	best_signals_interval = pd.DataFrame()
	best_signals_interval['buy'] = [Upper_Line_buy,Mid_Line_buy,Lower_Line_buy]
	best_signals_interval['power_buy'] = [Power_Upper_Line_buy,Power_Mid_Line_buy,Power_Lower_Line_buy]
	best_signals_interval['alpha_buy'] = [alpha_buy,alpha_buy,alpha_buy]

	best_signals_interval['sell'] = [Upper_Line_sell,Mid_Line_sell,Lower_Line_sell]
	best_signals_interval['power_sell'] = [Power_Upper_Line_sell,Power_Mid_Line_sell,Power_Lower_Line_sell]
	best_signals_interval['alpha_sell'] = [alpha_sell,alpha_sell,alpha_sell]

	return best_signals_interval,signal_buy,signal_sell

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#************************************************** Last Signals With Weight ******************************************************************************
def last_signal_sma(dataset,symbol):
	#**** 
	#the inputs of Functions Must read From Data Base Number's

	buy_path = "GA/SMA/BUY/" + symbol + '.csv'
	sell_path = "GA/SMA/SELL/" + symbol + '.csv'

	if os.path.exists(buy_path):
		ga_result_buy, ga_result_sell = read_ga_result(symbol=symbol)
	else:
		return 0

	buy_signal, _ = golden_cross(
					dataset=dataset,
					Low_Period=ga_result_buy['low_period'][0],
					High_Period=ga_result_buy['high_period'][0],
					Low_ApplyTo=ga_result_buy['apply_to_low'][0],
					High_ApplyTo=ga_result_buy['apply_to_high'][0]
					)

	_, sell_signal = golden_cross(
					dataset=dataset,
					Low_Period=ga_result_sell['low_period'][0],
					High_Period=ga_result_sell['high_period'][0],
					Low_ApplyTo=ga_result_sell['apply_to_low'][0],
					High_ApplyTo=ga_result_sell['apply_to_high'][0]
					)

	signal = pd.DataFrame(np.zeros(1))
	signal['signal'] = np.nan
	#signal['power'] = np.nan
	signal['index'] = np.nan

	signal['signal'][0] = 'no_flag'
	#signal['power'][0] = 0
	signal['index'][0] = -1

	if True:#len(buy_signal) > 1 and len(sell_signal) > 1:
		if (buy_signal['index'].iloc[-1] > sell_signal['index'].iloc[-1]):
			signal['signal'][0] = 'buy'
			signal['index'][0] = buy_signal['index'].iloc[-1]

			#if ((buy_signal['values'][len(buy_signal)-1] <= best_signals['buy'][0]) & (buy_signal['values'][len(buy_signal)-1] >= best_signals['buy'][2])):
				#signal['power'] = np.mean(best_signals['power_buy']) * (2/(len_price - buy_signal['index'][len(buy_signal)-1] + 1))
			#else:
				#signal['power'] = np.mean(best_signals['power_buy']) * (1 - best_signals['alpha_buy']) * (2/(len_price - buy_signal['index'][len(buy_signal)-1] + 1))
	
		elif (buy_signal['index'].iloc[-1] < sell_signal['index'].iloc[-1]):
			signal['signal'][0] = 'sell'
			signal['index'][0] = sell_signal['index'].iloc[-1]

			#if ((sell_signal['values'][len(sell_signal)-1] <= best_signals['sell'][0]) & (sell_signal['values'][len(sell_signal)-1] >= best_signals['sell'][2])):
				#signal['power'] = np.mean(best_signals['power_sell']) * (2/(len_price - sell_signal['index'][len(sell_signal)-1] + 1))
			#else:
				#signal['power'] = np.mean(best_signals['power_sell']) * (1 - best_signals['alpha_sell']) * (2/(len_price - sell_signal['index'][len(sell_signal)-1] + 1))

		else:
			signal['signal'][0] = 'no_flag'
			signal['index'][0] = -1

	else:
		signal['signal'][0] = 'no_flag'
		signal['index'][0] = -1
		#Add Interval From Index Last to Signal For Power Decreasing
	return signal

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#************************************************** USE OF Funcyions ******************************************************************************

"""

symbol_data_5M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,48000)
print('get data')
#best_signals,buy_signal,sell_signal = Find_Best_interval(dataset = symbol_data_5M['AUDCAD_i'],period_low=2,period_high=5,Low_ApplyTo='close',High_ApplyTo='close',max_profit_buy=0.06,max_profit_sell=0.06,alpha_sell=0.1,alpha_buy=0.1)

#signal = Signal(best_signals=best_signals ,buy_signal = buy_signal ,sell_signal = sell_signal,len_price=len(y1)-1)

symbol_black_list = np.array(
	[
		'WSt30_m_i','SPX500_m_i','NQ100_m_i','GER40_m_i',
		'GER40_i','USDRUR','USDRUR_i','USDRUB','USDRUB_i',
		'USDHKD','WTI_i','BRN_i','STOXX50_i','NQ100_i',
		'NG_i','HSI50_i','CAC40_i','ASX200_i','SPX500_i',
		'NIKK225_i','IBEX35_i','FTSE100_i','RUBRUR',
		'EURDKK_i','DAX30_i','XRPUSD_i','XBNUSD_i',
		'LTCUSD_i','ETHUSD_i','BTCUSD_i','_DXY','_DJI',
		'EURTRY_i','USDTRY_i','USDDKK_i','EURRUB_i'
	])

for sym in symbol:

	if sym.name == 'AUDCAD_i': continue
	if sym.name == 'AUDCHF_i': continue
	if sym.name == 'AUDJPY_i': continue
	if sym.name == 'AUDNZD_i': continue
	if sym.name == 'AUDUSD_i': continue
	if sym.name == 'CADCHF_i': continue
	if sym.name == 'CADJPY_i': continue
	if sym.name == 'CHFJPY_i': continue
	if sym.name == 'EURAUD_i': continue
	if sym.name == 'EURCAD_i': continue
	if sym.name == 'EURCHF_i': continue
	if sym.name == 'EURGBP_i': continue
	if sym.name == 'EURJPY_i': continue
	if sym.name == 'EURNZD_i': continue
	if sym.name == 'EURUSD_i': continue
	if sym.name == 'GBPAUD_i': continue
	if sym.name == 'GBPCAD_i': continue
	if sym.name == 'GBPCHF_i': continue


	if np.where(sym.name == symbol_black_list)[0].size != 0: continue

	try:
		genetic_buy_algo(
			symbol_data_5M=symbol_data_5M,
			symbol=sym.name,
			num_turn=80,
			max_score_ga_buy=10,
			max_score_ga_sell=10
			)
	except Exception as ex:
		print('ex = ',ex)

"""