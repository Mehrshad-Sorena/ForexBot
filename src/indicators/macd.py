from F_I_RESIST_PROTECT import Extreme_points, Extreme_points_ichimoko, extreme_points_ramp_lines, Best_Extreme_Finder, protect_resist
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from fitter import Fitter, get_common_distributions, get_distributions
from shapely.geometry import LineString
from scipy.signal import argrelextrema
from sklearn.cluster import KMeans
from scipy.optimize import fsolve
from sma import last_signal_sma
import matplotlib.pyplot as plt
from datetime import datetime
from random import randint
from log_get_data import *
from timer import stTime
from scipy import stats
from random import seed
import pandas_ta as ind
from tqdm import tqdm
import pandas as pd
import logging
import fitter
import math
import time
import csv
import sys
import os
import warnings
warnings.filterwarnings("ignore")


#******************* Functions:

#divergence_macd()
#tester_div_macd()
#Find_Best_intervals()
#initilize_values_genetic()
#gen_creator()
#genetic_algo_div_macd()
#macd_div_tester_for_permit()
#last_signal_macd_div()

#/////////////////////////////////////////


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ta.macd)

#**************************************************** Golden Cross Strategy *******************************************************
def golden_cross(dataset,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,mode='optimize',plot=False):

	#Mode:
	#optimize
	#online
	macd_read = ind.macd(dataset[symbol][Apply_to],fast = macd_fast,slow = macd_slow,signal = macd_signal)

	macd = pd.DataFrame()
	column = macd_read.columns[0]
	macd['macd'] = pd.DataFrame(macd_read, columns=[column])
	column = macd_read.columns[2]
	macd['macds'] = pd.DataFrame(macd_read, columns=[column])
	macd = macd.dropna(inplace=False)
	
	if(plot == True):
		plt.plot(macd.index,macd.macd,c = 'b')
		plt.plot(macd.index,macd.macds,c = 'r')

	first_line = LineString(np.column_stack((macd.macd.index, macd.macd)))
	second_line = LineString(np.column_stack((macd.macd.index, macd.macds)))

	intersection = first_line.intersection(second_line)

	if intersection.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection).xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index

		if (plot == True):
			plt.plot(cross['index'],cross['values'], 'o',c='g')
    
	elif intersection.geom_type == 'Point':
		cross = pd.DataFrame(*intersection.xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index
		if (plot == True):
			plt.plot(cross['index'],cross['values'], 'o',c='g')

	if(mode == 'online'):
		signal_buy = pd.DataFrame(np.zeros(len(cross)))
		signal_buy['signal'] = np.nan
		signal_buy['values'] = np.nan
		signal_buy['index'] = np.nan

		signal_sell = pd.DataFrame(np.zeros(len(cross)))
		signal_sell['signal'] = np.nan
		signal_sell['values'] = np.nan
		signal_sell['index'] = np.nan

		try:
			buy_indexes = cross['index'][np.where(((macd.macds[cross['index']-1].to_numpy()>macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()<macd.macd[cross['index']+1].to_numpy())))[0]]
			buy_cross_indexes = np.where(((macd.macds[cross['index']-1].to_numpy()>macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()<macd.macd[cross['index']+1].to_numpy())))[0]
			signal_buy['signal'][buy_cross_indexes] = 'buy'
			signal_buy['values'] = cross['values'][buy_cross_indexes]
			signal_buy['index'][buy_cross_indexes] = buy_indexes
		except:
			buy_indexes = cross['index'][np.where(((macd.macds[cross['index'][1:-1]-1].to_numpy()>macd.macd[cross['index'][1:-1]-1].to_numpy())&(macd.macds[cross['index'][1:-1]+1].to_numpy()<macd.macd[cross['index'][1:-1]+1].to_numpy())))[0]]
			buy_cross_indexes = np.where(((macd.macds[cross['index'][1:-1]-1].to_numpy()>macd.macd[cross['index'][1:-1]-1].to_numpy())&(macd.macds[cross['index'][1:-1]+1].to_numpy()<macd.macd[cross['index'][1:-1]+1].to_numpy())))[0]
			signal_buy['signal'][buy_cross_indexes] = 'buy'
			signal_buy['values'] = cross['values'][buy_cross_indexes]
			signal_buy['index'][buy_cross_indexes] = buy_indexes

		try:
			sell_indexes = cross['index'][np.where(((macd.macds[cross['index']-1].to_numpy()<macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()>macd.macd[cross['index']+1].to_numpy())))[0]]
			sell_cross_indexes = np.where(((macd.macds[cross['index']-1].to_numpy()<macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()>macd.macd[cross['index']+1].to_numpy())))[0]
			signal_sell['signal'][sell_cross_indexes] = 'sell'
			signal_sell['values'] = cross['values'][sell_cross_indexes]
			signal_sell['index'][sell_cross_indexes] = sell_indexes
		except:
			sell_indexes = cross['index'][np.where(((macd.macds[cross['index'][1:-1]-1].to_numpy()<macd.macd[cross['index'][1:-1]-1].to_numpy())&(macd.macds[cross['index'][1:-1]+1].to_numpy()>macd.macd[cross['index'][1:-1]+1].to_numpy())))[0]]
			sell_cross_indexes = np.where(((macd.macds[cross['index'][1:-1]-1].to_numpy()<macd.macd[cross['index'][1:-1]-1].to_numpy())&(macd.macds[cross['index'][1:-1]+1].to_numpy()>macd.macd[cross['index'][1:-1]+1].to_numpy())))[0]
			signal_sell['signal'][sell_cross_indexes] = 'sell'
			signal_sell['values'] = cross['values'][sell_cross_indexes]
			signal_sell['index'][sell_cross_indexes] = sell_indexes

	#print(buy_indexes)
	#print(signal_buy)

	#
	i = 0
	j = 0
	k = 0

	if(mode == 'optimize'):
		signal_buy = pd.DataFrame(np.zeros(len(cross)))
		signal_buy['signal'] = np.nan
		signal_buy['values'] = np.nan
		signal_buy['index'] = np.nan
		signal_buy['profit'] = np.nan

		signal_sell = pd.DataFrame(np.zeros(len(cross)))
		signal_sell['signal'] = np.nan
		signal_sell['values'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['profit'] = np.nan

		for elm in cross['index']:
			if ((macd.macds[elm-1]>macd.macd[elm-1])&(macd.macds[elm+1]<macd.macd[elm+1])):
				signal_buy['signal'][i] = 'buy'
				signal_buy['values'][i] = cross['values'][j]
				signal_buy['index'][i] = elm

				if ((j+1) < len(cross)):
					signal_buy['profit'][i] = (np.max(dataset[symbol]['close'][elm:cross['index'][j+1]] - dataset[symbol]['close'][elm])/dataset[symbol]['close'][elm]) * 100
				else:
					signal_buy['profit'][i] = (np.max(dataset[symbol]['close'][elm:-1] - dataset[symbol]['close'][elm])/dataset[symbol]['close'][elm]) * 100
				i += 1

			if ((macd.macds[elm-1]<macd.macd[elm-1])&(macd.macds[elm+1]>macd.macd[elm+1])):
				signal_sell['signal'][k] = 'sell'
				signal_sell['values'][k] = cross['values'][j]
				signal_sell['index'][k] = elm
				if ((j+1) < len(cross)):
					signal_sell['profit'][k] = (np.max(dataset[symbol]['close'][elm] - dataset[symbol]['close'][elm:cross['index'][j+1]])/np.min(dataset[symbol]['close'][elm:cross['index'][j+1]])) * 100
				else:
					signal_sell['profit'][k] = (np.max(dataset[symbol]['close'][elm] - dataset[symbol]['close'][elm:-1])/np.min(dataset[symbol]['close'][elm:-1])) * 100
				#print('elm_sell = ',elm)
				k += 1
			j += 1

	if (plot == True):
		plt.show()

	signal_buy = signal_buy.drop(columns = 0)
	signal_sell = signal_sell.drop(columns = 0)

	signal_buy = signal_buy.dropna(inplace = False)
	signal_sell = signal_sell.dropna(inplace = False)

	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_sell = signal_sell.sort_values(by = ['index'])

	return signal_buy,signal_sell

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Divergence Strategy *******************************************************
@stTime
def divergence_macd(
				dataset,
				dataset_15M,
				dataset_1H,
				Apply_to,
				symbol,
				macd_fast=12,
				macd_slow=26,
				macd_signal=9,
				mode='online',
				plot=False,
				buy_doing=False,
				sell_doing=False,
				primary_doing=False,
				secondry_doing=False,
				name_stp_pr=False,
				name_stp_minmax=True,
				st_percent_buy_max = 0.1,
				st_percent_buy_min = 0.1,
				st_percent_sell_max = 0.1,
				st_percent_sell_min = 0.5,
				tp_percent_buy_max = 0.5,
				tp_percent_buy_min = 0.5,
				tp_percent_sell_max = 0,
				tp_percent_sell_min = 0,
				alpha=0.05,
				num_exteremes=5,
				diff_extereme=100,
				real_test=False,
				flag_learning=False
				):

	#*************** OutPuts:
	#Four Panda DataFrams: signal_buy_primary, signal_buy_secondry, signal_sell_primary, signal_sell_secondry
	#signal = buy_primary, buy_secondry, sell_primary, sell_secondry
	#value_front: the value of last index of Divergence
	#value_back: the value of before index of Divergence
	#index: the index of last index of Divergence
	#ramp_macd
	#ramp_candle
	#coef_ramps
	#diff_ramps
	#beta
	#danger_line
	#diff_min_max_macd
	#diff_min_max_candle
	#** Just in optimize mode:
	#tp_min_max_index
	#tp_min_max
	#st_min_max_index
	#st_min_max
	#flag_min_max: st or tp
	#tp_pr_index
	#tp_pr
	#st_pr_index
	#st_pr
	#flag_pr: st or tp
	#diff_pr_top
	#diff_pr_down
	#/////////////////////////////

	#***************************** Initialize Inputs ************************

	macd_read = ind.macd(dataset[symbol][Apply_to],fast = macd_fast,slow = macd_slow,signal = macd_signal)

	macd = pd.DataFrame()
	column = macd_read.columns[2]
	macd['macds'] = pd.DataFrame(macd_read, columns=[column])
	macd = macd.dropna(inplace=False)

	n = num_exteremes
	
	min_ex = macd.iloc[argrelextrema(
									macd.macds.values, 
									comparator = np.less,
									order=n,
									mode='wrap'
									)[0]]['macds']

	extreme_min = pd.DataFrame()
	extreme_min['value'] = min_ex.values
	extreme_min['index'] = min_ex.index
	extreme_min = extreme_min.dropna(inplace=False)
	extreme_min = extreme_min.sort_values(by = ['index'])

	
	max_ex = macd.iloc[argrelextrema(
									macd.macds.values, 
									comparator = np.greater,
									order=n,
									mode='wrap'
									)[0]]['macds']

	extreme_max = pd.DataFrame()
	extreme_max['value'] = max_ex.values
	extreme_max['index'] = max_ex.index
	extreme_max = extreme_max.dropna(inplace=False)
	extreme_max = extreme_max.sort_values(by = ['index'])

	#num_exteremes = 0

	

	#plot = True

	if (plot == True):
		fig, (ax1, ax0) = plt.subplots(nrows=2, figsize=(12, 6))
		ax0.plot(extreme_min['index'],extreme_min['value'], 'o',c='g')
		ax0.plot(extreme_max['index'],extreme_max['value'], 'o',c='r')
		ax0.plot(macd.index,macd.macds,c='b')
		ax1.plot(dataset[symbol]['close'].index,dataset[symbol]['close'],c='b')
		#plt.show()

	#//////////////////////////////////////////////////////////////////////

	#******************************* Optimize Mode **************************

	my_money = 100

	if ((mode == 'optimize') | (mode == 'online')):
		signal_buy_primary = pd.DataFrame(np.zeros(len(extreme_min)))
		signal_buy_primary['signal'] = np.nan
		signal_buy_primary['value_front'] = np.nan
		signal_buy_primary['value_back'] = np.nan
		signal_buy_primary['index'] = np.nan
		#signal_buy_primary['ramp_macd'] = np.nan
		#signal_buy_primary['ramp_candle'] = np.nan
		#signal_buy_primary['coef_ramps'] = np.nan
		#signal_buy_primary['diff_ramps'] = np.nan
		#signal_buy_primary['beta'] = np.nan
		#signal_buy_primary['danger_line'] = np.nan
		#signal_buy_primary['diff_min_max_macd'] = np.nan
		#signal_buy_primary['diff_min_max_candle'] = np.nan
		#signal_buy_primary['value_min_max_candle'] = np.nan
		#signal_buy_primary['st_point'] = np.nan
		#signal_buy_primary['st_percent'] = np.nan
		#signal_buy_primary['ramp_vol'] = np.nan
		signal_buy_primary['num_diff_to_extremes'] = np.nan
		signal_buy_primary['num_extreme'] = np.nan

		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_buy_primary['tp_min_max_index'] = np.nan
				signal_buy_primary['tp_min_max'] = np.nan
				signal_buy_primary['st_min_max_index'] = np.nan
				signal_buy_primary['st_min_max'] = np.nan
				signal_buy_primary['flag_min_max'] = np.nan
				

			if (name_stp_pr == True):
				signal_buy_primary['tp_pr_index'] = np.nan
				signal_buy_primary['tp_pr'] = np.nan
				signal_buy_primary['st_pr_index'] = np.nan
				signal_buy_primary['st_pr'] = np.nan
				signal_buy_primary['flag_pr'] = np.nan
				signal_buy_primary['diff_pr_top'] = np.nan
				signal_buy_primary['diff_pr_down'] = np.nan
				signal_buy_primary['flag_pr_index'] = np.nan
				signal_buy_primary['money'] = np.nan
				#signal_buy_primary['st_line'] = np.nan
				#signal_buy_primary['tp_line'] = np.nan
				#signal_buy_primary['power_pr_high'] = np.nan
				#signal_buy_primary['power_pr_low'] = np.nan
				signal_buy_primary['money'][0] = my_money

		signal_buy_secondry = pd.DataFrame(np.zeros(len(extreme_min)))
		signal_buy_secondry['signal'] = np.nan
		signal_buy_secondry['value_front'] = np.nan
		signal_buy_secondry['value_back'] = np.nan
		signal_buy_secondry['index'] = np.nan
		signal_buy_secondry['ramp_macd'] = np.nan
		signal_buy_secondry['ramp_candle'] = np.nan
		signal_buy_secondry['coef_ramps'] = np.nan
		signal_buy_secondry['diff_ramps'] = np.nan
		signal_buy_secondry['beta'] = np.nan
		signal_buy_secondry['danger_line'] = np.nan
		signal_buy_secondry['diff_min_max_macd'] = np.nan
		signal_buy_secondry['diff_min_max_candle'] = np.nan
		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_buy_secondry['tp_min_max_index'] = np.nan
				signal_buy_secondry['tp_min_max'] = np.nan
				signal_buy_secondry['st_min_max_index'] = np.nan
				signal_buy_secondry['st_min_max'] = np.nan
				signal_buy_secondry['flag_min_max'] = np.nan

			if (name_stp_pr == True):
				signal_buy_secondry['tp_pr_index'] = np.nan
				signal_buy_secondry['tp_pr'] = np.nan
				signal_buy_secondry['st_pr_index'] = np.nan
				signal_buy_secondry['st_pr'] = np.nan
				signal_buy_secondry['flag_pr'] = np.nan
				signal_buy_secondry['diff_pr_top'] = np.nan
				signal_buy_secondry['diff_pr_down'] = np.nan


		signal_sell_primary = pd.DataFrame(np.zeros(len(extreme_max)))
		signal_sell_primary['signal'] = np.nan
		signal_sell_primary['value_front'] = np.nan
		signal_sell_primary['value_back'] = np.nan
		signal_sell_primary['index'] = np.nan
		#signal_sell_primary['ramp_macd'] = np.nan
		#signal_sell_primary['ramp_candle'] = np.nan
		#signal_sell_primary['coef_ramps'] = np.nan
		#signal_sell_primary['diff_ramps'] = np.nan
		#signal_sell_primary['beta'] = np.nan
		#signal_sell_primary['danger_line'] = np.nan
		#signal_sell_primary['diff_min_max_macd'] = np.nan
		#signal_sell_primary['diff_min_max_candle'] = np.nan
		signal_sell_primary['num_diff_to_extremes'] = np.nan
		signal_sell_primary['num_extreme'] = np.nan

		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_sell_primary['tp_min_max_index'] = np.nan
				signal_sell_primary['tp_min_max'] = np.nan
				signal_sell_primary['st_min_max_index'] = np.nan
				signal_sell_primary['st_min_max'] = np.nan
				signal_sell_primary['flag_min_max'] = np.nan

			if (name_stp_pr == True):
				signal_sell_primary['tp_pr_index'] = np.nan
				signal_sell_primary['tp_pr'] = np.nan
				signal_sell_primary['st_pr_index'] = np.nan
				signal_sell_primary['st_pr'] = np.nan
				signal_sell_primary['flag_pr'] = np.nan
				signal_sell_primary['diff_pr_top'] = np.nan
				signal_sell_primary['diff_pr_down'] = np.nan
				signal_sell_primary['flag_pr_index'] = np.nan
				signal_sell_primary['money'] = np.nan
				signal_sell_primary['money'][0] = my_money

		signal_sell_secondry = pd.DataFrame(np.zeros(len(extreme_max)))
		signal_sell_secondry['signal'] = np.nan
		signal_sell_secondry['value_front'] = np.nan
		signal_sell_secondry['value_back'] = np.nan
		signal_sell_secondry['index'] = np.nan
		signal_sell_secondry['ramp_macd'] = np.nan
		signal_sell_secondry['ramp_candle'] = np.nan
		signal_sell_secondry['coef_ramps'] = np.nan
		signal_sell_secondry['diff_ramps'] = np.nan
		signal_sell_secondry['beta'] = np.nan
		signal_sell_secondry['danger_line'] = np.nan
		signal_sell_secondry['diff_min_max_macd'] = np.nan
		signal_sell_secondry['diff_min_max_candle'] = np.nan
		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_sell_secondry['tp_min_max_index'] = np.nan
				signal_sell_secondry['tp_min_max'] = np.nan
				signal_sell_secondry['st_min_max_index'] = np.nan
				signal_sell_secondry['st_min_max'] = np.nan
				signal_sell_secondry['flag_min_max'] = np.nan

			if (name_stp_pr == True):
				signal_sell_secondry['tp_pr_index'] = np.nan
				signal_sell_secondry['tp_pr'] = np.nan
				signal_sell_secondry['st_pr_index'] = np.nan
				signal_sell_secondry['st_pr'] = np.nan
				signal_sell_secondry['flag_pr'] = np.nan
				signal_sell_secondry['diff_pr_top'] = np.nan
				signal_sell_secondry['diff_pr_down'] = np.nan

		primary_counter = 0
		secondry_counter = 0

		print('exterme finded ======> ',len(extreme_min['index']))
		print('len dataset =========> ',len(dataset[symbol]['low']))

		print('last max finded ======> ',extreme_max['index'].iloc[-1])
		print('last min finded ======> ',extreme_min['index'].iloc[-1])

		mehrshad = 0
		

		#***************************** Buy Find Section ***********************************************
		for elm in extreme_min.index:
			#print(int((elm/extreme_min.index[-1])*100),'%')
			if (buy_doing == False): break
			if (primary_doing == False): break
			#+++++++++++++++++++++++++++++++++++++ Primary +++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Primary Buy ********************************* = 1

			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 2

			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 3
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 4
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 5
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 6
			
			if (
				len(
					(extreme_min['value'][elm] > extreme_min['value'][elm-diff_extereme:elm]).to_numpy() &
					(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-diff_extereme:elm]]).to_numpy()
					) >= 1
				):

				list_elm = diff_extereme - np.where(
													(extreme_min['value'][elm] > extreme_min['value'][elm-diff_extereme:elm]).to_numpy() &
													(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-diff_extereme:elm]]).to_numpy()
													)[0]

				if len(list_elm) > 1:
					diff_extereme_buy = round(np.max(list_elm))
				elif len(list_elm) == 1:
					diff_extereme_buy = list_elm[0]
				else:
					continue 
			else:
				if (elm - 1 < 0): continue
				diff_extereme_buy = 1
				list_elm = [1]

			#print(list_elm)

			

			if (elm - diff_extereme_buy < 0): continue

			#print(
				#(extreme_min['value'][elm] > extreme_min['value'][elm-diff_extereme_buy]) &
				#(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-diff_extereme_buy]])
				#)

			if (
				(extreme_min['value'][elm] > extreme_min['value'][elm-diff_extereme_buy]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-diff_extereme_buy]])
				):

				signal_buy_primary['signal'][primary_counter] = 'buy_primary'
				signal_buy_primary['value_front'][primary_counter] = extreme_min['value'][elm]
				signal_buy_primary['value_back'][primary_counter] = extreme_min['value'][elm-diff_extereme_buy]
				signal_buy_primary['index'][primary_counter] = extreme_min['index'][elm]
				#signal_buy_primary['ramp_macd'][primary_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-3])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				#signal_buy_primary['ramp_candle'][primary_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-3]])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				#signal_buy_primary['coef_ramps'][primary_counter] = signal_buy_primary['ramp_macd'][primary_counter]/abs(signal_buy_primary['ramp_candle'][primary_counter])
				#signal_buy_primary['diff_ramps'][primary_counter] = abs(signal_buy_primary['ramp_candle'][primary_counter]) - signal_buy_primary['ramp_macd'][primary_counter]
				#signal_buy_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				#signal_buy_primary['danger_line'][primary_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_primary['beta'][primary_counter])/100)
				#signal_buy_primary['diff_min_max_macd'][primary_counter] = ((np.max(macd.macds[extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) / np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) * 100
				#signal_buy_primary['diff_min_max_candle'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) * 100

				#signal_buy_primary['value_min_max_candle'][primary_counter] = np.max(dataset[symbol]['high'][int(extreme_min['index'][elm-3]):int(extreme_min['index'][elm])])
				#signal_buy_primary['st_point'][primary_counter] = np.min(dataset[symbol]['low'][int(extreme_min['index'][elm-3]):int(extreme_min['index'][elm])])
				#signal_buy_primary['st_percent'][primary_counter] = ((dataset[symbol]['low'][int(extreme_min['index'][elm])] - signal_buy_primary['st_point'][primary_counter])/dataset[symbol]['low'][int(extreme_min['index'][elm])]) * 100

				#signal_buy_primary['ramp_vol'][primary_counter] = (dataset[symbol]['volume'][extreme_min['index'][elm]] - dataset[symbol]['volume'][extreme_min['index'][elm-3]])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				
				signal_buy_primary['num_diff_to_extremes'][primary_counter] = diff_extereme_buy
				signal_buy_primary['num_extreme'][primary_counter] = len(extreme_min['index'])

				#print(extreme_min['index'][elm])
				#print(extreme_min['index'][elm-diff_extereme_buy])
				#print(extreme_min['index'][elm] - extreme_min['index'][elm-diff_extereme_buy])
				#print()

				#print()
				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_pr == True):

						if (
							flag_learning == True and
							my_money <= 0.1
							):
							break

						if primary_counter >= 1:
							if (
								real_test == True and
								int(extreme_min['index'][elm] + 1) <= signal_buy_primary['flag_pr_index'][primary_counter-1]
								):
								if int(extreme_min['index'][elm]) + 1 >= int(extreme_min['index'].iloc[-1]): break
								continue

						#Calculate ST and TP With Protect Resist Function
						if (int(extreme_min['index'][elm]) < 600): continue

						dataset_pr_5M = pd.DataFrame()
						dataset_pr_1H = pd.DataFrame()

						cut_first = 0
						if (extreme_min['index'][elm] > 600):
							cut_first = extreme_min['index'][elm] - 600
						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(extreme_min['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(extreme_min['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(extreme_min['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(extreme_min['index'][elm])].reset_index(drop=True)

						#loc_1H = 0
						location_1H = -1
						#for ti in dataset_1H[symbol]['time']:
							#print('1H===> ',ti.year)
							#if (
								#ti.year == dataset[symbol]['time'][int(extreme_min['index'][elm])].year and
								#ti.month == dataset[symbol]['time'][int(extreme_min['index'][elm])].month and
								#ti.day == dataset[symbol]['time'][int(extreme_min['index'][elm])].day and
								#ti.hour == dataset[symbol]['time'][int(extreme_min['index'][elm])].hour
								#):
								#location_1H = loc_1H

							#loc_1H += 1

						list_time = np.where(
											(dataset_1H[symbol]['time'].dt.year.to_numpy() == dataset[symbol]['time'][int(extreme_min['index'][elm])].year) &
											(dataset_1H[symbol]['time'].dt.month.to_numpy() == dataset[symbol]['time'][int(extreme_min['index'][elm])].month) &
											(dataset_1H[symbol]['time'].dt.day.to_numpy() == dataset[symbol]['time'][int(extreme_min['index'][elm])].day) &
											(dataset_1H[symbol]['time'].dt.hour.to_numpy() == dataset[symbol]['time'][int(extreme_min['index'][elm])].hour)
											)[0]
						try:
							location_1H = list_time[0] + 1
						except:
							location_1H = 0

						if location_1H < 500: continue

						cut_first_1H = 0
						if location_1H >= 500:
							cut_first_1H = location_1H - 500

						dataset_pr_1H['low'] = dataset_1H[symbol]['low'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['high'] = dataset_1H[symbol]['high'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['close'] = dataset_1H[symbol]['close'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['open'] = dataset_1H[symbol]['open'][cut_first_1H:location_1H].reset_index(drop=True)


						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(
													T_5M=True,
													T_15M=False,
													T_1H=True,
													T_4H=False,
													T_1D=False,
													dataset_5M=dataset_pr_5M,
													dataset_15M=dataset_pr_1H,
													dataset_1H=dataset_pr_1H,
													dataset_4H=dataset_pr_1H,
													dataset_1D=dataset_pr_1H,
													plot=False,
													alpha=alpha
													)
						except:
							res_pro['high'] = [dataset[symbol]['high'][int(extreme_min['index'][elm])]*(1+(tp_percent_buy_min/100)),0,0]#res_pro['high'] = 'nan'
							res_pro['low'] = [0,0,dataset[symbol]['low'][int(extreme_min['index'][elm])] * (1-(st_percent_buy_min/100))]#res_pro['low'] = 'nan'

						if (res_pro.empty == False):
							signal_buy_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							signal_buy_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

							#signal_buy_primary['power_pr_high'][primary_counter] = res_pro['power_high'][0]
							#signal_buy_primary['power_pr_low'][primary_counter] = res_pro['power_low'][2]

							#if signal_buy_primary['diff_pr_top'][primary_counter] > tp_percent_minmax_buy_max:
								#signal_buy_primary['diff_pr_top'][primary_counter] = tp_percent_minmax_buy_max
								#res_pro['high'][0] = dataset[symbol]['high'][int(extreme_min['index'][elm])]*(1+(tp_percent_minmax_buy_max/100))
							

							#signal_buy_primary['tp_line'][primary_counter] = res_pro['high'][0]
							#signal_buy_primary['st_line'][primary_counter] = res_pro['low'][2]


							#if signal_buy_primary['diff_pr_down'][primary_counter] > st_percent_minmax_buy:
							#signal_buy_primary['diff_pr_down'][primary_counter] = st_percent_minmax_buy
							#res_pro['low'][2] = dataset[symbol]['low'][int(extreme_min['index'][elm])] * (1-(st_percent_minmax_buy/100))


							if signal_buy_primary['diff_pr_down'][primary_counter] < st_percent_buy_min:#signal_buy['diff_pr_top'][buy_counter]:
								signal_buy_primary['diff_pr_down'][primary_counter] = st_percent_buy_min
								res_pro['low'][2] = dataset[symbol]['low'][int(extreme_min['index'][elm])] * (1-(st_percent_buy_min/100))

							if signal_buy_primary['diff_pr_down'][primary_counter] > st_percent_buy_max:
								signal_buy_primary['diff_pr_down'][primary_counter] = st_percent_buy_max
								res_pro['low'][2] = dataset[symbol]['low'][int(extreme_min['index'][elm])] * (1-(st_percent_buy_max/100))
								
							if signal_buy_primary['diff_pr_top'][primary_counter] < tp_percent_buy_min:
								signal_buy_primary['diff_pr_top'][primary_counter] = tp_percent_buy_min
								res_pro['high'][0] = dataset[symbol]['high'][int(extreme_min['index'][elm])]*(1+(tp_percent_buy_min/100))

							if signal_buy_primary['diff_pr_top'][primary_counter] > tp_percent_buy_max:
								signal_buy_primary['diff_pr_top'][primary_counter] = tp_percent_buy_max
								res_pro['high'][0] = dataset[symbol]['high'][int(extreme_min['index'][elm])]*(1+(tp_percent_buy_max/100))

							if int(extreme_min['index'][elm] + 1) >= len(dataset[symbol]['low']): break

							if (
								dataset[symbol]['low'][int(extreme_min['index'][elm] + 1)] > res_pro['low'][2] and
								dataset[symbol]['high'][int(extreme_min['index'][elm] + 1)] * 1.0004 < res_pro['high'][0] and
								True#dataset[symbol]['HL/2'][int(extreme_min['index'][elm] + 1)] - dataset[symbol]['HL/2'][int(extreme_min['index'][elm])] > 0
								):


								if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm] + 1:-1].values) >= (res_pro['high'][0])))[0])) > 1):
									signal_buy_primary['tp_pr_index'][primary_counter] = extreme_min['index'][elm] + 1 + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm] + 1:-1].values) >= (res_pro['high'][0])))[0])
									signal_buy_primary['tp_pr'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_pr_index'][primary_counter]] - (dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004))/(dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004)) * 100#signal_buy_primary['diff_pr_top'][primary_counter]
									
									if signal_buy_primary['tp_pr'][primary_counter] > signal_buy_primary['diff_pr_top'][primary_counter]: 
										signal_buy_primary['tp_pr'][primary_counter] = signal_buy_primary['diff_pr_top'][primary_counter]

								elif ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm] + 1:-1].values) >= (res_pro['high'][0])))[0])) == 1):
									signal_buy_primary['tp_pr_index'][primary_counter] = extreme_min['index'][elm] + 1 + np.where(((dataset[symbol]['high'][extreme_min['index'][elm] + 1:-1].values) >= (res_pro['high'][0])))[0]
									signal_buy_primary['tp_pr'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_pr_index'][primary_counter]] - (dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004))/(dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004)) * 100#signal_buy_primary['diff_pr_top'][primary_counter]

									if signal_buy_primary['tp_pr'][primary_counter] > signal_buy_primary['diff_pr_top'][primary_counter]: 
										signal_buy_primary['tp_pr'][primary_counter] = signal_buy_primary['diff_pr_top'][primary_counter]

								else:	
									signal_buy_primary['tp_pr_index'][primary_counter] = -1
									signal_buy_primary['tp_pr'][primary_counter] = 0

								if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm] + 1:-1]).values) <= (res_pro['low'][2])))[0])) > 1):
									signal_buy_primary['st_pr_index'][primary_counter] = extreme_min['index'][elm] + 1 + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm] + 1:-1]).values) <= (res_pro['low'][2])))[0])
									signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm] + 1] - dataset[symbol]['low'][signal_buy_primary['st_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm] + 1]) * 100#signal_buy_primary['diff_pr_down'][primary_counter]

									if signal_buy_primary['st_pr'][primary_counter] > signal_buy_primary['diff_pr_down'][primary_counter]: 
										signal_buy_primary['st_pr'][primary_counter] = signal_buy_primary['diff_pr_down'][primary_counter]

								elif ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm] + 1:-1]).values) <= (res_pro['low'][2])))[0])) == 1):
									signal_buy_primary['st_pr_index'][primary_counter] = extreme_min['index'][elm] + 1 + np.where((((dataset[symbol]['low'][extreme_min['index'][elm] + 1:-1]).values) <= (res_pro['low'][2])))[0]
									signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm] + 1] - dataset[symbol]['low'][signal_buy_primary['st_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm] + 1]) * 100#signal_buy_primary['diff_pr_down'][primary_counter]

									if signal_buy_primary['st_pr'][primary_counter] > signal_buy_primary['diff_pr_down'][primary_counter]: 
										signal_buy_primary['st_pr'][primary_counter] = signal_buy_primary['diff_pr_down'][primary_counter]

								else:
									signal_buy_primary['st_pr_index'][primary_counter] = -1
									signal_buy_primary['st_pr'][primary_counter] = 0



								if (signal_buy_primary['st_pr_index'][primary_counter] < signal_buy_primary['tp_pr_index'][primary_counter]) & (signal_buy_primary['st_pr_index'][primary_counter] != -1):
									signal_buy_primary['flag_pr'][primary_counter] = 'st'
									signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['st_pr_index'][primary_counter]

									my_money = my_money - ((my_money/10) * signal_buy_primary['st_pr'][primary_counter])
									signal_buy_primary['money'][primary_counter] = my_money
									#print('st front 3 ===> ',signal_buy_primary['value_front'][primary_counter])
									#print('st back 3 ===> ',signal_buy_primary['value_back'][primary_counter])
									signal_buy_primary['tp_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm] + 1:int(signal_buy_primary['st_pr_index'][primary_counter])]) - (dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004))/(dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004)) * 100

									if signal_buy_primary['tp_pr'][primary_counter] > signal_buy_primary['diff_pr_top'][primary_counter]: 
										signal_buy_primary['tp_pr'][primary_counter] = signal_buy_primary['diff_pr_top'][primary_counter]

								else:
								
									if (signal_buy_primary['tp_pr_index'][primary_counter] != -1):
										signal_buy_primary['flag_pr'][primary_counter] = 'tp'
										signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['tp_pr_index'][primary_counter]

										my_money = my_money + ((my_money/10) * signal_buy_primary['tp_pr'][primary_counter])
										signal_buy_primary['money'][primary_counter] = my_money

										#print('tp front 3 ===> ',signal_buy_primary['value_front'][primary_counter])
										#print('tp back 3 ===> ',signal_buy_primary['value_back'][primary_counter])
										signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm] + 1] - np.min(dataset[symbol]['low'][extreme_min['index'][elm] + 1:int(signal_buy_primary['tp_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm] + 1]) * 100
										
										if signal_buy_primary['st_pr'][primary_counter] > signal_buy_primary['diff_pr_down'][primary_counter]: 
											signal_buy_primary['st_pr'][primary_counter] = signal_buy_primary['diff_pr_down'][primary_counter]

									if (signal_buy_primary['tp_pr_index'][primary_counter] == -1) & (signal_buy_primary['st_pr_index'][primary_counter] != -1):
										signal_buy_primary['flag_pr'][primary_counter] = 'st'
										signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['st_pr_index'][primary_counter]

										my_money = my_money - ((my_money/10) * signal_buy_primary['st_pr'][primary_counter])
										signal_buy_primary['money'][primary_counter] = my_money

										#print('st front 3 ===> ',signal_buy_primary['value_front'][primary_counter])
										#print('st back 3 ===> ',signal_buy_primary['value_back'][primary_counter])
										signal_buy_primary['tp_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm] + 1:int(signal_buy_primary['st_pr_index'][primary_counter])]) - (dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004))/(dataset[symbol]['high'][extreme_min['index'][elm] + 1]*1.0004)) * 100

										if signal_buy_primary['tp_pr'][primary_counter] > signal_buy_primary['diff_pr_top'][primary_counter]: 
											signal_buy_primary['tp_pr'][primary_counter] = signal_buy_primary['diff_pr_top'][primary_counter]

							else:
								signal_buy_primary['tp_pr_index'][primary_counter] = -1
								signal_buy_primary['tp_pr'][primary_counter] = 0
								signal_buy_primary['st_pr_index'][primary_counter] = -1
								signal_buy_primary['st_pr'][primary_counter] = 0
								signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'

								if primary_counter > 0:
									signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['flag_pr_index'][primary_counter-1]
								else:
									signal_buy_primary['flag_pr_index'][primary_counter] = -1
						else:
							signal_buy_primary['tp_pr_index'][primary_counter] = -1
							signal_buy_primary['tp_pr'][primary_counter] = 0
							signal_buy_primary['st_pr_index'][primary_counter] = -1
							signal_buy_primary['st_pr'][primary_counter] = 0
							signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'
							
							if primary_counter > 0:
								signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['flag_pr_index'][primary_counter-1]
							else:
								signal_buy_primary['flag_pr_index'][primary_counter] = -1


						if np.isnan(signal_buy_primary['tp_pr'][primary_counter]): 
							signal_buy_primary['tp_pr'][primary_counter] = 0
							signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'
						if np.isnan(signal_buy_primary['st_pr'][primary_counter]): signal_buy_primary['st_pr'][primary_counter] = 0
						if np.isnan(signal_buy_primary['tp_pr_index'][primary_counter]): signal_buy_primary['tp_pr_index'][primary_counter] = -1
						if np.isnan(signal_buy_primary['st_pr_index'][primary_counter]): signal_buy_primary['st_pr_index'][primary_counter] = -1

						if primary_counter > 0:
							if np.isnan(signal_buy_primary['flag_pr_index'][primary_counter]): signal_buy_primary['flag_pr_index'][primary_counter] = signal_buy_primary['flag_pr_index'][primary_counter-1]
						else:
							if np.isnan(signal_buy_primary['flag_pr_index'][primary_counter]): signal_buy_primary['flag_pr_index'][primary_counter] = -1
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-diff_extereme_buy],extreme_min['index'][elm]],[extreme_min['value'][elm-diff_extereme_buy],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-diff_extereme_buy],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-diff_extereme_buy]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue
					
			#///////////////////////////////////////////////////////
			#---------------------------------------------------------------------------------------------------

		for elm in extreme_min.index:
			if (buy_doing == False): break
			if (secondry_doing == False): break
			#+++++++++++++++++++++++++++++++++++++ Secondry ++++++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Secondry Buy ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_min['value'][elm] < extreme_min['value'][elm-1]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] > dataset[symbol]['low'][extreme_min['index'][elm-1]])):
				signal_buy_secondry['signal'][secondry_counter] = 'buy_secondry'
				signal_buy_secondry['value_front'][secondry_counter] = extreme_min['value'][elm]
				signal_buy_secondry['value_back'][secondry_counter] = extreme_min['value'][elm-1]
				signal_buy_secondry['index'][secondry_counter] = extreme_min['index'][elm]
				signal_buy_secondry['ramp_macd'][secondry_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-1])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-1]])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy_secondry['coef_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter]/signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['diff_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter] - signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_secondry['danger_line'][secondry_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_secondry['beta'][secondry_counter])/100)
				signal_buy_secondry['diff_min_max_macd'][secondry_counter] = ((np.max(macd.macd[extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) / np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) * 100
				signal_buy_secondry['diff_min_max_candle'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_secondry['diff_min_max_candle'][secondry_counter])))[0]) - 1) > 1):
							signal_buy_secondry['tp_min_max_index'][secondry_counter] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_secondry['diff_min_max_candle'][secondry_counter])))[0])
							signal_buy_secondry['tp_min_max'][secondry_counter] = ((dataset[symbol]['high'][signal_buy_secondry['tp_min_max_index'][secondry_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_secondry['tp_min_max_index'][secondry_counter] = -1
							signal_buy_secondry['tp_min_max'][secondry_counter] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
							signal_buy_secondry['st_min_max_index'][secondry_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
							signal_buy_secondry['st_min_max'][secondry_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_secondry['st_min_max_index'][secondry_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_secondry['st_min_max_index'][secondry_counter] = -1
							signal_buy_secondry['st_min_max'][secondry_counter] = 0

						if (signal_buy_secondry['st_min_max_index'][secondry_counter] < signal_buy_secondry['tp_min_max_index'][secondry_counter]):
							signal_buy_secondry['flag_min_max'][secondry_counter] = 'st'
							if (signal_buy_secondry['st_min_max_index'][secondry_counter] != -1):
								signal_buy_secondry['tp_min_max'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_secondry['st_min_max_index'][secondry_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_secondry['flag_min_max'][secondry_counter] = 'tp'
							if (signal_buy_secondry['tp_min_max_index'][secondry_counter] != -1):
								signal_buy_secondry['st_min_max'][secondry_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_secondry['tp_min_max_index'][secondry_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

						#///////////////////////////////////////////////////

					if (name_stp_pr == True):
						#Calculate ST and TP With Protect Resist Function
						dataset_pr_5M = pd.DataFrame()
						dataset_pr_15M = pd.DataFrame()
						cut_first = 0
						if (extreme_min['index'][elm] > 2000):
							cut_first = extreme_min['index'][elm] - 2000
						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:extreme_min['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:extreme_min['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:extreme_min['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:extreme_min['index'][elm]].reset_index(drop=True)

						dataset_pr_15M['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(extreme_min['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(extreme_min['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(extreme_min['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(extreme_min['index'][elm]/3)].reset_index(drop=True)

						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,dataset_5M=dataset_pr_5M,dataset_15M=dataset_pr_15M,dataset_1H=dataset_pr_15M,dataset_4H=dataset_pr_5M,dataset_1D=dataset_pr_5M,plot=False)
						except:
							res_pro['high'] = 'nan'
							res_pro['low'] = 'nan'

						if (res_pro.empty == False):
							signal_buy_secondry['diff_pr_top'][secondry_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							signal_buy_secondry['diff_pr_down'][secondry_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
								signal_buy_secondry['tp_pr_index'][secondry_counter] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
								signal_buy_secondry['tp_pr'][secondry_counter] = ((dataset[symbol]['high'][signal_buy_secondry['tp_pr_index'][secondry_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_secondry['tp_pr_index'][secondry_counter] = -1
								signal_buy_secondry['tp_pr'][secondry_counter] = 0

							if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
								signal_buy_secondry['st_pr_index'][secondry_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
								signal_buy_secondry['st_pr'][secondry_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_secondry['st_pr_index'][secondry_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_secondry['st_pr_index'][secondry_counter] = -1
								signal_buy_secondry['st_pr'][secondry_counter] = 0

							if (signal_buy_secondry['st_pr_index'][secondry_counter] < signal_buy_secondry['tp_pr_index'][secondry_counter]):
								signal_buy_secondry['flag_pr'][secondry_counter] = 'st'
								if (signal_buy_secondry['st_pr_index'][secondry_counter] != -1):
									signal_buy_secondry['tp_pr'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_secondry['st_pr_index'][secondry_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_secondry['flag_pr'][secondry_counter] = 'tp'
								if (signal_buy_secondry['tp_pr_index'][secondry_counter] != -1):
									signal_buy_secondry['st_pr'][secondry_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_secondry['tp_pr_index'][secondry_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
						else:
							signal_buy_secondry['tp_pr_index'][secondry_counter] = -1
							signal_buy_secondry['tp_pr'][secondry_counter] = 0
							signal_buy_secondry['st_pr_index'][secondry_counter] = -1
							signal_buy_secondry['st_pr'][secondry_counter] = 0
							signal_buy_secondry['flag_pr'][secondry_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[extreme_min['value'][elm-1],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-1]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1	
				continue	
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 2
			
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 3
			
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 4
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 5
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 6
					
			#///////////////////////////////////////////////////////
			#--------------------------------------------------------------------------------------------------

		#///////////////////////////////////////////////////////////////////////////////////////////////

		#***************************** Sell Find Section ***********************************************
		primary_counter = 0
		secondry_counter = 0
		for elm in extreme_max.index:
			if (sell_doing == False): break
			if (primary_doing == False): break
			#++++++++++++++++++++++++++++++++++++ Primary ++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Primary Sell ********************************* = 1

			if (
				len(
					(extreme_max['value'][elm] < extreme_max['value'][elm-diff_extereme:elm]).to_numpy() &
					(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-diff_extereme:elm]]).to_numpy()
					) >= 1
				):

				list_elm = diff_extereme - np.where(
													(extreme_max['value'][elm] < extreme_max['value'][elm-diff_extereme:elm]).to_numpy() &
													(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-diff_extereme:elm]]).to_numpy()
													)[0]

				if len(list_elm) > 1:
					diff_extereme_sell = round(np.max(list_elm))
				elif len(list_elm) == 1:
					diff_extereme_sell = list_elm[0]
				else:
					continue
			else:
				diff_extereme_sell = 1

			

			if (elm - diff_extereme_sell < 0): continue

			if (
				(extreme_max['value'][elm] < extreme_max['value'][elm-diff_extereme_sell]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-diff_extereme_sell]])
				):

				signal_sell_primary['signal'][primary_counter] = 'sell_primary'
				signal_sell_primary['value_front'][primary_counter] = extreme_max['value'][elm]
				signal_sell_primary['value_back'][primary_counter] = extreme_max['value'][elm-diff_extereme_sell]
				signal_sell_primary['index'][primary_counter] = extreme_max['index'][elm]
				#signal_sell_primary['ramp_macd'][primary_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-1])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				#signal_sell_primary['ramp_candle'][primary_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-1]])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				#signal_sell_primary['coef_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter]/signal_sell_primary['ramp_candle'][primary_counter]
				#signal_sell_primary['diff_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter] - signal_sell_primary['ramp_candle'][primary_counter]
				#signal_sell_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				#signal_sell_primary['danger_line'][primary_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_primary['beta'][primary_counter])/100)
				#signal_sell_primary['diff_min_max_macd'][primary_counter] = (-1 * (np.min(macd.macds[extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) / np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) * 100
				#signal_sell_primary['diff_min_max_candle'][primary_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) * 100

				signal_sell_primary['num_diff_to_extremes'][primary_counter] = diff_extereme_sell
				signal_sell_primary['num_extreme'][primary_counter] = len(extreme_max['index'])

				#print('value front 1 = ',signal_sell_primary['value_front'][primary_counter])
				#print('value back 1 = ',signal_sell_primary['value_back'][primary_counter])
				#print()
				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell_primary['diff_min_max_candle'][primary_counter])))[0]) - 1) > 1):
							signal_sell_primary['tp_min_max_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell_primary['diff_min_max_candle'][primary_counter])))[0])
							signal_sell_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_primary['tp_min_max_index'][primary_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['tp_min_max_index'][primary_counter] = -1
							signal_sell_primary['tp_min_max'][primary_counter] = 0

						if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])-1) > 1):
							signal_sell_primary['st_min_max_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])
							signal_sell_primary['st_min_max'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_min_max_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['st_min_max_index'][primary_counter] = -1
							signal_sell_primary['st_min_max'][primary_counter] = 0

						if (signal_sell_primary['st_min_max_index'][primary_counter] < signal_sell_primary['tp_min_max_index'][primary_counter]):
							signal_sell_primary['flag_min_max'][primary_counter] = 'st'
							signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['st_pr_index'][primary_counter]

							if (signal_sell_primary['st_min_max_index'][primary_counter] != -1):
								signal_sell_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['flag_min_max'][primary_counter] = 'tp'
							signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['st_pr_index'][primary_counter]

							if (signal_sell_primary['tp_min_max_index'][primary_counter] != -1):
								signal_sell_primary['st_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

						#///////////////////////////////////////////////////
					if (name_stp_pr == True):
						#Calculate ST and TP With Protect Resist Function

						if (
							flag_learning == True and
							my_money <= 0.1
							):
							break

						if primary_counter >= 1:
							if (
								real_test == True and
								int(extreme_max['index'][elm]) + 1 <= signal_sell_primary['flag_pr_index'][primary_counter-1]
								):
								if int(extreme_max['index'][elm]) + 1 >= int(extreme_max['index'].iloc[-1]): break
								continue

						if (int(extreme_max['index'][elm]) < 600): continue

						dataset_pr_5M = pd.DataFrame()
						dataset_pr_1H = pd.DataFrame()

						cut_first = 0
						if (extreme_max['index'][elm] > 600):
							cut_first = extreme_max['index'][elm] - 600
						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(extreme_max['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(extreme_max['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(extreme_max['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(extreme_max['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['time'] = dataset[symbol]['time'][cut_first:int(extreme_max['index'][elm])].reset_index(drop=True)

						#loc_1H = 0
						location_1H = -1
						#for ti in dataset_1H[symbol]['time']:
							#print('1H===> ',ti.year)
							#if (
								#ti.year == dataset[symbol]['time'][int(extreme_min['index'][elm])].year and
								#ti.month == dataset[symbol]['time'][int(extreme_min['index'][elm])].month and
								#ti.day == dataset[symbol]['time'][int(extreme_min['index'][elm])].day and
								#ti.hour == dataset[symbol]['time'][int(extreme_min['index'][elm])].hour
								#):
								#location_1H = loc_1H

							#loc_1H += 1

						list_time = np.where(
											(dataset_1H[symbol]['time'].dt.year.to_numpy() == dataset[symbol]['time'][int(extreme_max['index'][elm])].year) &
											(dataset_1H[symbol]['time'].dt.month.to_numpy() == dataset[symbol]['time'][int(extreme_max['index'][elm])].month) &
											(dataset_1H[symbol]['time'].dt.day.to_numpy() == dataset[symbol]['time'][int(extreme_max['index'][elm])].day) &
											(dataset_1H[symbol]['time'].dt.hour.to_numpy() == dataset[symbol]['time'][int(extreme_max['index'][elm])].hour)
											)[0]

						try:
							location_1H = list_time[0] + 1
						except:
							location_1H = 0

						if location_1H < 500: continue

						cut_first_1H = 0
						if location_1H >= 500:
							cut_first_1H = location_1H - 500

						dataset_pr_1H['low'] = dataset_1H[symbol]['low'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['high'] = dataset_1H[symbol]['high'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['close'] = dataset_1H[symbol]['close'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['open'] = dataset_1H[symbol]['open'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['time'] = dataset_1H[symbol]['time'][cut_first_1H:location_1H].reset_index(drop=True)

						#print(dataset_pr_5M['time'].iloc[-1])
						#print(dataset_pr_1H['time'].iloc[-1])

						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(
													T_5M=True,
													T_15M=False,
													T_1H=True,
													T_4H=False,
													T_1D=False,
													dataset_5M=dataset_pr_5M,
													dataset_15M=dataset_pr_1H,
													dataset_1H=dataset_pr_1H,
													dataset_4H=dataset_pr_1H,
													dataset_1D=dataset_pr_1H,
													plot=False,
													alpha=alpha
													)
						except:
							res_pro['high'] = [dataset[symbol]['high'][int(extreme_max['index'][elm])] * (1+(st_percent_sell_min/100)),0,0]#res_pro['high'] = 'nan'
							res_pro['low'] = [0,0,dataset[symbol]['low'][int(extreme_max['index'][elm])]*(1-(tp_percent_sell_min/100))]#res_pro['low'] = 'nan'

						if (res_pro.empty == False):
							signal_sell_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							signal_sell_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

							mehrshad += 1

							if signal_sell_primary['diff_pr_top'][primary_counter] < st_percent_sell_min:#signal_buy['diff_pr_top'][buy_counter]:
								signal_sell_primary['diff_pr_top'][primary_counter] = st_percent_sell_min
								res_pro['high'][0] = dataset[symbol]['high'][int(extreme_max['index'][elm])] * (1+(st_percent_sell_min/100))

							if signal_sell_primary['diff_pr_top'][primary_counter] > st_percent_sell_max:
								signal_sell_primary['diff_pr_top'][primary_counter] = st_percent_sell_max
								res_pro['high'][0] = dataset[symbol]['high'][int(extreme_max['index'][elm])] * (1+(st_percent_sell_max/100))
								
							if signal_sell_primary['diff_pr_down'][primary_counter] < tp_percent_sell_min:
								signal_sell_primary['diff_pr_down'][primary_counter] = tp_percent_sell_min
								res_pro['low'][2] = dataset[symbol]['low'][int(extreme_max['index'][elm])]*(1-(tp_percent_sell_min/100))

							if signal_sell_primary['diff_pr_down'][primary_counter] > tp_percent_sell_max:
								signal_sell_primary['diff_pr_down'][primary_counter] = tp_percent_sell_max
								res_pro['low'][2] = dataset[symbol]['low'][int(extreme_max['index'][elm])]*(1-(tp_percent_sell_max/100))



							if int(extreme_max['index'][elm] + 1) >= len(dataset[symbol]['low']): break

							if (
								dataset[symbol]['low'][int(extreme_max['index'][elm]) + 1] > res_pro['low'][2] and
								dataset[symbol]['high'][int(extreme_max['index'][elm]) + 1] < res_pro['high'][0] and
								True#dataset[symbol]['HL/2'][int(extreme_max['index'][elm]) + 1] - dataset[symbol]['HL/2'][int(extreme_max['index'][elm])] < 0
								):


								if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm] + 1:-1].values * 1.0004) <= (res_pro['low'][2])))[0])) > 1):
									signal_sell_primary['tp_pr_index'][primary_counter] = extreme_max['index'][elm] + 1 + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm] + 1:-1].values * 1.0004) <= (res_pro['low'][2])))[0])
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm] + 1] - (dataset[symbol]['low'][signal_sell_primary['tp_pr_index'][primary_counter]]*1.0004))/dataset[symbol]['low'][extreme_max['index'][elm] + 1]) * 100#signal_sell_primary['diff_pr_down'][primary_counter]
									
									if signal_sell_primary['tp_pr'][primary_counter] > signal_sell_primary['diff_pr_down'][primary_counter]:
										signal_sell_primary['tp_pr'][primary_counter] = signal_sell_primary['diff_pr_down'][primary_counter]

								elif ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm] + 1:-1].values * 1.0004) <= (res_pro['low'][2])))[0])) == 1):
									signal_sell_primary['tp_pr_index'][primary_counter] = extreme_max['index'][elm] + 1 + np.where(((dataset[symbol]['low'][extreme_max['index'][elm] + 1:-1].values * 1.0004) <= (res_pro['low'][2])))[0]
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm] + 1] - (dataset[symbol]['low'][signal_sell_primary['tp_pr_index'][primary_counter]]*1.0004))/dataset[symbol]['low'][extreme_max['index'][elm] + 1]) * 100#signal_sell_primary['diff_pr_down'][primary_counter]

									if signal_sell_primary['tp_pr'][primary_counter] > signal_sell_primary['diff_pr_down'][primary_counter]:
										signal_sell_primary['tp_pr'][primary_counter] = signal_sell_primary['diff_pr_down'][primary_counter]

								else:
									signal_sell_primary['tp_pr_index'][primary_counter] = -1
									signal_sell_primary['tp_pr'][primary_counter] = 0

								if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm] + 1:-1]).values*1.0004) >= (res_pro['high'][0])))[0])) > 1):
									signal_sell_primary['st_pr_index'][primary_counter] = extreme_max['index'][elm] + 1 + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm] + 1:-1]).values*1.0004) >= (res_pro['high'][0])))[0])
									signal_sell_primary['st_pr'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm] + 1])/dataset[symbol]['high'][extreme_max['index'][elm] + 1]) * 100#signal_sell_primary['diff_pr_top'][primary_counter]
									
									if signal_sell_primary['st_pr'][primary_counter] > signal_sell_primary['diff_pr_top'][primary_counter]:
										signal_sell_primary['st_pr'][primary_counter] = signal_sell_primary['diff_pr_top'][primary_counter]

								elif ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm] + 1:-1]).values*1.0004) >= (res_pro['high'][0])))[0])) == 1):
									signal_sell_primary['st_pr_index'][primary_counter] = extreme_max['index'][elm] + 1 + np.where((((dataset[symbol]['high'][extreme_max['index'][elm] + 1:-1]).values*1.0004) >= (res_pro['high'][0])))[0]
									signal_sell_primary['st_pr'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm] + 1])/dataset[symbol]['high'][extreme_max['index'][elm] + 1]) * 100#signal_sell_primary['diff_pr_top'][primary_counter]
									
									if signal_sell_primary['st_pr'][primary_counter] > signal_sell_primary['diff_pr_top'][primary_counter]:
										signal_sell_primary['st_pr'][primary_counter] = signal_sell_primary['diff_pr_top'][primary_counter]

								else:
									signal_sell_primary['st_pr_index'][primary_counter] = -1
									signal_sell_primary['st_pr'][primary_counter] = 0

								if (signal_sell_primary['st_pr_index'][primary_counter] < signal_sell_primary['tp_pr_index'][primary_counter]) & (signal_sell_primary['st_pr_index'][primary_counter] != -1):
									signal_sell_primary['flag_pr'][primary_counter] = 'st'
									signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['st_pr_index'][primary_counter]

									my_money = my_money - ((my_money/10) * signal_sell_primary['st_pr'][primary_counter])
									signal_sell_primary['money'][primary_counter] = my_money

									#print('flag ====> st')
									#print()
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm] + 1] - (np.min(dataset[symbol]['low'][extreme_max['index'][elm] + 1:int(signal_sell_primary['st_pr_index'][primary_counter])])*1.0004))/dataset[symbol]['low'][extreme_max['index'][elm] + 1]) * 100
									
									if signal_sell_primary['tp_pr'][primary_counter] > signal_sell_primary['diff_pr_down'][primary_counter]:
										signal_sell_primary['tp_pr'][primary_counter] = signal_sell_primary['diff_pr_down'][primary_counter]

								else:
								
									if (signal_sell_primary['tp_pr_index'][primary_counter] != -1):
										signal_sell_primary['flag_pr'][primary_counter] = 'tp'
										signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['tp_pr_index'][primary_counter]

										my_money = my_money + ((my_money/10) * signal_sell_primary['tp_pr'][primary_counter])
										signal_sell_primary['money'][primary_counter] = my_money

										#print('flag ====> tp')
										#print()
										signal_sell_primary['st_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm] + 1:int(signal_sell_primary['tp_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm] + 1])/dataset[symbol]['high'][extreme_max['index'][elm] + 1]) * 100
										
										if signal_sell_primary['st_pr'][primary_counter] > signal_sell_primary['diff_pr_top'][primary_counter]:
											signal_sell_primary['st_pr'][primary_counter] = signal_sell_primary['diff_pr_top'][primary_counter]

									if (signal_sell_primary['tp_pr_index'][primary_counter] == -1) & (signal_sell_primary['st_pr_index'][primary_counter] != -1):
										signal_sell_primary['flag_pr'][primary_counter] = 'st'
										signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['st_pr_index'][primary_counter]

										my_money = my_money - ((my_money/10) * signal_sell_primary['st_pr'][primary_counter])
										signal_sell_primary['money'][primary_counter] = my_money

										#print('flag ====> st')
										#print()
										signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm] + 1] - (np.min(dataset[symbol]['low'][extreme_max['index'][elm] + 1:int(signal_sell_primary['st_pr_index'][primary_counter])])*1.0004))/dataset[symbol]['low'][extreme_max['index'][elm] + 1]) * 100
										
										if signal_sell_primary['tp_pr'][primary_counter] > signal_sell_primary['diff_pr_down'][primary_counter]:
											signal_sell_primary['tp_pr'][primary_counter] = signal_sell_primary['diff_pr_down'][primary_counter]
							else:
								signal_sell_primary['tp_pr_index'][primary_counter] = -1
								signal_sell_primary['tp_pr'][primary_counter] = 0
								signal_sell_primary['st_pr_index'][primary_counter] = -1
								signal_sell_primary['st_pr'][primary_counter] = 0
								signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'

								if primary_counter > 0:
									signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['flag_pr_index'][primary_counter-1]
								else:
									signal_sell_primary['flag_pr_index'][primary_counter] = -1
						else:
							signal_sell_primary['tp_pr_index'][primary_counter] = -1
							signal_sell_primary['tp_pr'][primary_counter] = 0
							signal_sell_primary['st_pr_index'][primary_counter] = -1
							signal_sell_primary['st_pr'][primary_counter] = 0
							signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'
							
							if primary_counter > 0:
								signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['flag_pr_index'][primary_counter-1]
							else:
								signal_sell_primary['flag_pr_index'][primary_counter] = -1

						if np.isnan(signal_sell_primary['tp_pr'][primary_counter]): 
							signal_sell_primary['tp_pr'][primary_counter] = 0
							signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'
						if np.isnan(signal_sell_primary['st_pr'][primary_counter]): signal_sell_primary['st_pr'][primary_counter] = 0
						if np.isnan(signal_sell_primary['tp_pr_index'][primary_counter]): signal_sell_primary['tp_pr_index'][primary_counter] = -1
						if np.isnan(signal_sell_primary['st_pr_index'][primary_counter]): signal_sell_primary['st_pr_index'][primary_counter] = -1

						if primary_counter > 0:
							if np.isnan(signal_sell_primary['flag_pr_index'][primary_counter]): signal_sell_primary['flag_pr_index'][primary_counter] = signal_sell_primary['flag_pr_index'][primary_counter-1]
						else:
							if np.isnan(signal_sell_primary['flag_pr_index'][primary_counter]): signal_sell_primary['flag_pr_index'][primary_counter] = -1

					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-diff_extereme_sell],extreme_max['index'][elm]],[extreme_max['value'][elm-diff_extereme_sell],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-diff_extereme_sell],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-diff_extereme_sell]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue		
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 2
			
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 3
			
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 4
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 5

			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 6

			#///////////////////////////////////////////////////////
			#---------------------------------------------------------------------------------------------------
		for elm in extreme_max.index:
			if (sell_doing == False): break
			if (secondry_doing == False): break
			#++++++++++++++++++++++++++++++++++++++ Secondry +++++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Secondry Sell ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_max['value'][elm] > extreme_max['value'][elm-1]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] < dataset[symbol]['high'][extreme_max['index'][elm-1]])):
				signal_sell_secondry['signal'][secondry_counter] = 'sell_secondry'
				signal_sell_secondry['value_front'][secondry_counter] = extreme_max['value'][elm]
				signal_sell_secondry['value_back'][secondry_counter] = extreme_max['value'][elm-1]
				signal_sell_secondry['index'][secondry_counter] = extreme_max['index'][elm]
				signal_sell_secondry['ramp_macd'][secondry_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-1])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-1]])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell_secondry['coef_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter]/signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['diff_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter] - signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_secondry['danger_line'][secondry_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_secondry['beta'][secondry_counter])/100)
				signal_sell_secondry['diff_min_max_macd'][secondry_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) / np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) * 100
				signal_sell_secondry['diff_min_max_candle'][secondry_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell_secondry['diff_min_max_candle'][secondry_counter])))[0]) - 1) > 1):
							signal_sell_secondry['tp_min_max_index'][secondry_counter] = extreme_max['index'][elm] + np.min(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell_secondry['diff_min_max_candle'][secondry_counter])))[0])
							signal_sell_secondry['tp_min_max'][secondry_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_secondry['tp_min_max_index'][secondry_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_secondry['tp_min_max_index'][secondry_counter] = -1
							signal_sell_secondry['tp_min_max'][secondry_counter] = 0

						if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])-1) > 1):
							signal_sell_secondry['st_min_max_index'][secondry_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])
							signal_sell_secondry['st_min_max'][secondry_counter] = ((dataset[symbol]['high'][signal_sell_secondry['st_min_max_index'][secondry_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_secondry['st_min_max_index'][secondry_counter] = -1
							signal_sell_secondry['st_min_max'][secondry_counter] = 0

						if (signal_sell_secondry['st_min_max_index'][secondry_counter] < signal_sell_secondry['tp_min_max_index'][secondry_counter]):
							signal_sell_secondry['flag_min_max'][secondry_counter] = 'st'
							if (signal_sell_secondry['st_min_max_index'][secondry_counter] != -1):
								signal_sell_secondry['tp_min_max'][secondry_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_secondry['st_min_max_index'][secondry_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_secondry['flag_min_max'][secondry_counter] = 'tp'
							if (signal_sell_secondry['tp_min_max_index'][secondry_counter] != -1):
								signal_sell_secondry['st_min_max'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_secondry['tp_min_max_index'][secondry_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

						#///////////////////////////////////////////////////

					if (name_stp_pr == True):
						#Calculate ST and TP With Protect Resist Function
						dataset_pr_5M = pd.DataFrame()
						dataset_pr_15M = pd.DataFrame()
						cut_first = 0
						if (extreme_max['index'][elm] > 2000):
							cut_first = extreme_max['index'][elm] - 2000
						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:extreme_max['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:extreme_max['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:extreme_max['index'][elm]].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:extreme_max['index'][elm]].reset_index(drop=True)

						dataset_pr_15M['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(extreme_max['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(extreme_max['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(extreme_max['index'][elm]/3)].reset_index(drop=True)
						dataset_pr_15M['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(extreme_max['index'][elm]/3)].reset_index(drop=True)

						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,dataset_5M=dataset_pr_5M,dataset_15M=dataset_pr_15M,dataset_1H=dataset_pr_15M,dataset_4H=dataset_pr_5M,dataset_1D=dataset_pr_5M,plot=False)
						except:
							res_pro['high'] = 'nan'
							res_pro['low'] = 'nan'

						if (res_pro.empty == False):
							signal_sell_secondry['diff_pr_top'][secondry_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							signal_sell_secondry['diff_pr_down'][secondry_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
								signal_sell_secondry['tp_pr_index'][secondry_counter] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
								signal_sell_secondry['tp_pr'][secondry_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_secondry['tp_pr_index'][secondry_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_secondry['tp_pr_index'][secondry_counter] = -1
								signal_sell_secondry['tp_pr'][secondry_counter] = 0

							if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
								signal_sell_secondry['st_pr_index'][secondry_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
								signal_sell_secondry['st_pr'][secondry_counter] = ((dataset[symbol]['high'][signal_sell_secondry['st_pr_index'][secondry_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_secondry['st_pr_index'][secondry_counter] = -1
								signal_sell_secondry['st_pr'][secondry_counter] = 0

							if (signal_sell_secondry['st_pr_index'][secondry_counter] < signal_sell_secondry['tp_pr_index'][secondry_counter]):
								signal_sell_secondry['flag_pr'][secondry_counter] = 'st'
								if (signal_sell_secondry['st_pr_index'][secondry_counter] != -1):
									signal_sell_secondry['tp_pr'][secondry_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_secondry['st_pr_index'][secondry_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_secondry['flag_pr'][secondry_counter] = 'tp'
								if (signal_sell_secondry['tp_pr_index'][secondry_counter] != -1):
									signal_sell_secondry['st_pr'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_secondry['tp_pr_index'][secondry_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
						else:
							signal_sell_secondry['tp_pr_index'][secondry_counter] = -1
							signal_sell_secondry['tp_pr'][secondry_counter] = 0
							signal_sell_secondry['st_pr_index'][secondry_counter] = -1
							signal_sell_secondry['st_pr'][secondry_counter] = 0
							signal_sell_secondry['flag_pr'][secondry_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[extreme_max['value'][elm-1],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-1]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1
				continue
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 2
			
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 3
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 4
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 5
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 6
					
			#///////////////////////////////////////////////////////
			#----------------------------------------------------------------------------------------------------

	#/////////////////////////////////////////////////////////////////////////////

	#*************************** OutPuts ***************************************

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		#print('=======> signal_buy_primary before = ',signal_buy_primary)

	print('mehrshad =====> ',mehrshad)

	signal_buy_primary = signal_buy_primary.drop(columns=0)
	signal_buy_primary = signal_buy_primary.dropna()
	signal_buy_primary = signal_buy_primary.sort_values(by = ['index'])
	signal_buy_primary = signal_buy_primary.reset_index(drop=True)

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		#print('=======> signal_buy_primary after = ',signal_buy_primary)

	signal_buy_secondry = signal_buy_secondry.drop(columns=0)
	signal_buy_secondry = signal_buy_secondry.dropna()
	signal_buy_secondry = signal_buy_secondry.sort_values(by = ['index'])
	signal_buy_secondry = signal_buy_secondry.reset_index(drop=True)

	signal_sell_primary = signal_sell_primary.drop(columns=0)
	signal_sell_primary = signal_sell_primary.dropna()
	signal_sell_primary = signal_sell_primary.sort_values(by = ['index'])
	signal_sell_primary = signal_sell_primary.reset_index(drop=True)

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		#print('=======> signal_sell_primary after = ',signal_sell_primary)

	signal_sell_secondry = signal_sell_secondry.drop(columns=0)
	signal_sell_secondry = signal_sell_secondry.dropna()
	signal_sell_secondry = signal_sell_secondry.sort_values(by = ['index'])
	signal_sell_secondry = signal_sell_secondry.reset_index(drop=True)
	
	print('*********************** Buy *********************************')
	#print(signal_buy_primary)
	#print(signal_buy_secondry)
	if False:#(mode == 'optimize'):
		print('***************** Primary ****')
		print('mean tp pr = ',np.mean(signal_buy_primary['tp_pr']))
		print('mean st pr = ',np.mean(signal_buy_primary['st_pr']))
		print('mean tp min_max = ',np.mean(signal_buy_primary['tp_min_max']))
		print('mean st min_max = ',np.mean(signal_buy_primary['st_min_max']))

		print('max tp pr = ',np.max(signal_buy_primary['tp_pr']))
		print('max st pr = ',np.max(signal_buy_primary['st_pr']))
		print('max tp min_max = ',np.max(signal_buy_primary['tp_min_max']))
		print('max st min_max = ',np.max(signal_buy_primary['st_min_max']))

		print('tp pr = ',np.bincount(signal_buy_primary['flag_pr'] == 'tp'))
		print('st pr = ',np.bincount(signal_buy_primary['flag_pr'] == 'st'))
		print('tp min_max = ',np.bincount(signal_buy_primary['flag_min_max'] == 'tp'))
		print('st min_max = ',np.bincount(signal_buy_primary['flag_min_max'] == 'st'))

		print('sum st pr = ',np.sum(signal_buy_primary['st_pr'][np.where(signal_buy_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('sum tp pr = ',np.sum(signal_buy_primary['tp_pr'][np.where(signal_buy_primary['flag_pr'] == 'tp')[0]].to_numpy()))

		print('sum st min_max = ',np.sum(signal_buy_primary['st_min_max'][np.where(signal_buy_primary['flag_min_max'] == 'st')[0]].to_numpy()))
		print('sum tp min_max = ',np.sum(signal_buy_primary['tp_min_max'][np.where(signal_buy_primary['flag_min_max'] == 'tp')[0]].to_numpy()))

		print('max down = ',np.max(signal_buy_primary['diff_pr_down'][np.where(signal_buy_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('min down = ',np.min(signal_buy_primary['diff_pr_down'][np.where(signal_buy_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('mean down = ',np.mean(signal_buy_primary['diff_pr_down'][np.where(signal_buy_primary['flag_pr'] == 'st')[0]].to_numpy()))

		print('+++++++++++++++++++')
		print('*************** secondry *****')

		print('mean tp pr = ',np.mean(signal_buy_secondry['tp_pr']))
		print('mean st pr = ',np.mean(signal_buy_secondry['st_pr']))
		print('mean tp min_max = ',np.mean(signal_buy_secondry['tp_min_max']))
		print('mean st min_max = ',np.mean(signal_buy_secondry['st_min_max']))

		print('max tp pr = ',np.max(signal_buy_secondry['tp_pr']))
		print('max st pr = ',np.max(signal_buy_secondry['st_pr']))
		print('max tp min_max = ',np.max(signal_buy_secondry['tp_min_max']))
		print('max st min_max = ',np.max(signal_buy_secondry['st_min_max']))

		print('tp pr = ',np.bincount(signal_buy_secondry['flag_pr'] == 'tp'))
		print('st pr = ',np.bincount(signal_buy_secondry['flag_pr'] == 'st'))
		print('tp min_max = ',np.bincount(signal_buy_secondry['flag_min_max'] == 'tp'))
		print('st min_max = ',np.bincount(signal_buy_secondry['flag_min_max'] == 'st'))

		print('sum st pr = ',np.sum(signal_buy_secondry['st_pr'][np.where(signal_buy_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('sum tp pr = ',np.sum(signal_buy_secondry['tp_pr'][np.where(signal_buy_secondry['flag_pr'] == 'tp')[0]].to_numpy()))

		print('sum st min_max = ',np.sum(signal_buy_secondry['st_min_max'][np.where(signal_buy_secondry['flag_min_max'] == 'st')[0]].to_numpy()))
		print('sum tp min_max = ',np.sum(signal_buy_secondry['tp_min_max'][np.where(signal_buy_secondry['flag_min_max'] == 'tp')[0]].to_numpy()))

		print('max down = ',np.max(signal_buy_secondry['diff_pr_down'][np.where(signal_buy_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('min down = ',np.min(signal_buy_secondry['diff_pr_down'][np.where(signal_buy_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('mean down = ',np.mean(signal_buy_secondry['diff_pr_down'][np.where(signal_buy_secondry['flag_pr'] == 'st')[0]].to_numpy()))

	print('/////////////////////////////////////////////////////////////////')

	print('*************************** Sell ***********************************')
	#print(signal_sell_primary)
	#print(signal_sell_secondry)
	if False:#(mode == 'optimize'):	
		print('************ Primary ***')
		print('mean tp pr = ',np.mean(signal_sell_primary['tp_pr']))
		print('mean st pr = ',np.mean(signal_sell_primary['st_pr']))
		print('mean tp min_max = ',np.mean(signal_sell_primary['tp_min_max']))
		print('mean st min_max = ',np.mean(signal_sell_primary['st_min_max']))

		print('max tp pr = ',np.max(signal_sell_primary['tp_pr']))
		print('max st pr = ',np.max(signal_sell_primary['st_pr']))
		print('max tp min_max = ',np.max(signal_sell_primary['tp_min_max']))
		print('max st min_max = ',np.max(signal_sell_primary['st_min_max']))

		print('tp pr = ',np.bincount(signal_sell_primary['flag_pr'] == 'tp'))
		print('st pr = ',np.bincount(signal_sell_primary['flag_pr'] == 'st'))
		print('tp min_max = ',np.bincount(signal_sell_primary['flag_min_max'] == 'tp'))
		print('st min_max = ',np.bincount(signal_sell_primary['flag_min_max'] == 'st'))

		print('sum st pr = ',np.sum(signal_sell_primary['st_pr'][np.where(signal_sell_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('sum tp pr = ',np.sum(signal_sell_primary['tp_pr'][np.where(signal_sell_primary['flag_pr'] == 'tp')[0]].to_numpy()))

		print('sum st min_max = ',np.sum(signal_sell_primary['st_min_max'][np.where(signal_sell_primary['flag_min_max'] == 'st')[0]].to_numpy()))
		print('sum tp min_max = ',np.sum(signal_sell_primary['tp_min_max'][np.where(signal_sell_primary['flag_min_max'] == 'tp')[0]].to_numpy()))

		print('max down = ',np.max(signal_sell_primary['diff_pr_down'][np.where(signal_sell_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('min down = ',np.min(signal_sell_primary['diff_pr_down'][np.where(signal_sell_primary['flag_pr'] == 'st')[0]].to_numpy()))
		print('mean down = ',np.mean(signal_sell_primary['diff_pr_down'][np.where(signal_sell_primary['flag_pr'] == 'st')[0]].to_numpy()))

		print('+++++++++++++++++++++++++')
		print('************ Secondry ***')
		print('mean tp pr = ',np.mean(signal_sell_secondry['tp_pr']))
		print('mean st pr = ',np.mean(signal_sell_secondry['st_pr']))
		print('mean tp min_max = ',np.mean(signal_sell_secondry['tp_min_max']))
		print('mean st min_max = ',np.mean(signal_sell_secondry['st_min_max']))

		print('max tp pr = ',np.max(signal_sell_secondry['tp_pr']))
		print('max st pr = ',np.max(signal_sell_secondry['st_pr']))
		print('max tp min_max = ',np.max(signal_sell_secondry['tp_min_max']))
		print('max st min_max = ',np.max(signal_sell_secondry['st_min_max']))

		print('tp pr = ',np.bincount(signal_sell_secondry['flag_pr'] == 'tp'))
		print('st pr = ',np.bincount(signal_sell_secondry['flag_pr'] == 'st'))
		print('tp min_max = ',np.bincount(signal_sell_secondry['flag_min_max'] == 'tp'))
		print('st min_max = ',np.bincount(signal_sell_secondry['flag_min_max'] == 'st'))

		print('sum st pr = ',np.sum(signal_sell_secondry['st_pr'][np.where(signal_sell_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('sum tp pr = ',np.sum(signal_sell_secondry['tp_pr'][np.where(signal_sell_secondry['flag_pr'] == 'tp')[0]].to_numpy()))

		print('sum st min_max = ',np.sum(signal_sell_secondry['st_min_max'][np.where(signal_sell_secondry['flag_min_max'] == 'st')[0]].to_numpy()))
		print('sum tp min_max = ',np.sum(signal_sell_secondry['tp_min_max'][np.where(signal_sell_secondry['flag_min_max'] == 'tp')[0]].to_numpy()))

		print('max down = ',np.max(signal_sell_secondry['diff_pr_down'][np.where(signal_sell_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('min down = ',np.min(signal_sell_secondry['diff_pr_down'][np.where(signal_sell_secondry['flag_pr'] == 'st')[0]].to_numpy()))
		print('mean down = ',np.mean(signal_sell_secondry['diff_pr_down'][np.where(signal_sell_secondry['flag_pr'] == 'st')[0]].to_numpy()))
	if (plot == True):
		plt.show()

	return signal_buy_primary, signal_buy_secondry, signal_sell_primary, signal_sell_secondry

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Find Best Intervals *******************************************************
def Find_Best_intervals(signals,apply_to, min_tp=0.1, max_st=0.1, name_stp='flag_min_max', alpha=0.1):

	if (name_stp == 'flag_min_max'):
		signal_good = signals.drop(
									np.where(
											(signals[name_stp]=='st')|
											(signals['st_min_max']>max_st)|
											(signals['tp_min_max']<min_tp)
											)[0])
		if (signal_good.empty == True): 
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval

	if (name_stp == 'flag_pr'):
		if (
			apply_to == 'tp_pr' or
			apply_to == 'st_pr' 
			):
			signal_good = signals.drop(
									np.where(
											#(signals[name_stp]=='st')|
											(signals[name_stp]=='no_flag')
											#(signals['st_pr']>max_st)|
											#(signals['tp_pr']<min_tp)
											)[0])
		else:
			signal_good = signals.drop(
									np.where(
											(signals[name_stp]=='st')|
											(signals[name_stp]=='no_flag')
											#(signals['st_pr']>max_st)|
											#(signals['tp_pr']<min_tp)
											)[0])

		if (signal_good.empty == True): 
			print('no good signal 1')
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval

	signal_good = signal_good.sort_values(by = ['index'])
	signal_good = signal_good.reset_index(drop=True)

	#timeout = time.time() + 20  # timeout_break Sec from now
	try:

		if (len(signal_good[apply_to].to_numpy()) - 1) >= 25:
			n_clusters = 5
		else:
			n_clusters = int(len(signal_good[apply_to].to_numpy())/4)
			if (n_clusters <= 0):
				best_signals_interval = pd.DataFrame()
				best_signals_interval['interval'] = [0,0,0]
				best_signals_interval['power'] = [0,0,0]
				best_signals_interval['alpha'] = [alpha,alpha,alpha]
				best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
				return best_signals_interval

		kmeans = KMeans(n_clusters=n_clusters, random_state=0,init='k-means++',n_init=5,max_iter=5)
		#Model Fitting
		kmeans = kmeans.fit(signal_good[apply_to].to_numpy().reshape(-1,1))

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		#if ((len(Y) != len(Power))):
			#timeout = time.time() + timeout_break
			#continue
		#if ((len(Y) == len(Power))): break

		signal_final = pd.DataFrame(Y, columns=['Y'])
		signal_final['power'] = Power
		signal_final = signal_final.sort_values(by = ['Y'])

	except Exception as ex:
		print('no good signal 1')
		best_signals_interval = pd.DataFrame()
		best_signals_interval['interval'] = [0,0,0]
		best_signals_interval['power'] = [0,0,0]
		best_signals_interval['alpha'] = [alpha,alpha,alpha]
		best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
		return best_signals_interval

	#Fitting Model Finding ****************************
	data_X = np.zeros(np.sum(signal_final['power']))

	j = 0
	z = 0
	for elm in signal_final['Y']:
		k = 0
		while k < signal_final['power'].to_numpy()[j]:
			data_X[z] = elm
			k += 1
			z += 1
		j += 1

	data_X = np.sort(data_X)

	distributions = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']

	#************************************ Finding Sell's ****************************

	while True:

		if (len(signal_final['Y'])-1 <= 0): 
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval
		
		f = Fitter(
				data = data_X,
				xmin=np.min(data_X),
				xmax=np.max(data_X),
				bins = len(signal_final['Y'])-1,
				distributions = distributions,
				timeout=1,
				density=True
				)

		f.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items = list(f.get_best(method = 'sumsquare_error').items())
		dist_name = items[0][0]
		dist_parameters = items[0][1]

		if dist_name == 'foldnorm':
			Y = f.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'dweibull':
			Y = f.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
		
		elif dist_name == 'rayleigh':
			Y = f.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'expon':
			Y = f.fitted_pdf['expon']
			Y = expon.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'nakagami':
			Y = f.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'norm':
			Y = f.fitted_pdf['norm']
			Y = norm.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_sell == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line <= Upper_Line)&(Mid_Line >= Lower_Line)&(Upper_Line>Lower_Line)): 
			break
		else:
			distributions.remove(dist_name)
			if (distributions == None):
				#return 'timeout.error'
				pass

	#//////////////////////////////////////////////////////////////////////////////////////

	best_signals_interval = pd.DataFrame()
	best_signals_interval['interval'] = [Upper_Line,Mid_Line,Lower_Line]
	best_signals_interval['power'] = [Power_Upper_Line,Power_Mid_Line,Power_Lower_Line]
	best_signals_interval['alpha'] = [alpha,alpha,alpha]
	best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]

	return best_signals_interval

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************************************** Tester For Divergence ****************************************************************************
def tester_div_macd(
					signal_buy,
					signal_sell,
					min_tp,
					max_st,
					alpha,
					name_stp_minmax,
					name_stp_pr,
					flag_trade
					):

	upper = 0
	mid = 1
	lower = 2

	#print('flag =====> ',flag_trade)

	#*********** Methode 1 Profits With MinMax Buy:
	if flag_trade == 'buy':
		
		output_buy = pd.DataFrame()

		if name_stp_minmax == True:

			ramp_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='ramp_macd',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			ramp_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='ramp_candle',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			diff_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_ramps',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			coef_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='coef_ramps',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			diff_min_max_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_macd',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			diff_min_max_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_candle',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			beta_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='beta',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			danger_line_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='danger_line',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			value_front_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='value_front',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			value_back_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='value_back',
 			min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

			#print('ramp_macd_intervals_minmax = ',ramp_macd_intervals_minmax)
			#print('ramp_candle_intervals_minmax = ',ramp_candle_intervals_minmax)
			#print('diff_ramps_intervals_minmax = ',diff_ramps_intervals_minmax)
			#print('coef_ramps_intervals_minmax = ',coef_ramps_intervals_minmax)
			#print('diff_min_max_macd_intervals_minmax = ',diff_min_max_macd_intervals_minmax)
			#print('diff_min_max_candle_intervals_minmax = ',diff_min_max_candle_intervals_minmax)
			#print('beta_intervals_minmax = ',beta_intervals_minmax)
			#print('danger_line_intervals_minmax = ',danger_line_intervals_minmax)
			#print('value_back_intervals_minmax = ',value_back_intervals_minmax)
			#print('value_front_intervals_minmax = ',value_front_intervals_minmax)


			list_index_ok = np.where(
				(signal_buy['ramp_macd'].to_numpy()>=-100) & 
				#((signal_buy['ramp_macd'].to_numpy()>=ramp_macd_intervals_minmax['interval'][lower]))&
				#((signal_buy['ramp_candle'].to_numpy()<=ramp_candle_intervals_minmax['interval'][upper]))&
				#((signal_buy['diff_ramps'].to_numpy()>=diff_ramps_intervals_minmax['interval'][lower]))&
				#((signal_buy['coef_ramps'].to_numpy()>=coef_ramps_intervals_minmax['interval'][lower]))&
				#((signal_buy['diff_min_max_macd'].to_numpy()<=diff_min_max_macd_intervals_minmax['interval'][upper]))&
				#((signal_buy['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax['interval'][upper]))&
				#((signal_buy['beta'].to_numpy()<=2*beta_intervals_minmax['interval'][upper]))&
				##((signal_buy_primary['danger_line'].to_numpy()<=danger_line_intervals_minmax['interval'][upper]))&
				#((signal_buy['value_back'].to_numpy()<=value_back_intervals_minmax['interval'][upper]))&
				#((signal_buy['value_front'].to_numpy()<=value_front_intervals_minmax['interval'][upper]))
				True)[0]

			print('list index = ',list_index_ok)

			output_buy['mean_tp_min_max'] = [np.mean(signal_buy['tp_min_max'][list_index_ok])]
			output_buy['mean_st_min_max'] = [np.mean(signal_buy['st_min_max'][list_index_ok])]

			output_buy['max_tp_min_max'] = [np.max(signal_buy['tp_min_max'][list_index_ok])]
			output_buy['max_st_min_max'] = [np.max(signal_buy['st_min_max'][list_index_ok])]
	
			try:
				output_buy['sum_st_min_max'] = [np.sum(signal_buy['st_min_max'][list_index_ok[np.where(signal_buy['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_buy['sum_tp_min_max'] = [np.sum(signal_buy['tp_min_max'][list_index_ok[np.where(signal_buy['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
			except Exception as ex:
				print('tester minmax buy: ',ex)
				output_buy['sum_st_min_max'] = 0
				output_buy['sum_tp_min_max'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_buy['flag_min_max'][list_index_ok]:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_buy['num_tp_min_max'] = [tp_counter]
			output_buy['num_st_min_max'] = [st_counter]
			output_buy['num_trade_min_max'] = [st_counter + tp_counter]
	#output_buy['ramp_low_upper_min_max'] = [ramp_low_intervals_minmax_buy['interval'][upper]]
	#output_buy['ramp_low_lower_min_max'] = [ramp_low_intervals_minmax_buy['interval'][lower]]
	#output_buy['ramp_high_upper_min_max'] = [ramp_high_intervals_minmax_buy['interval'][upper]]
	#output_buy['ramp_high_lower_min_max'] = [ramp_high_intervals_minmax_buy['interval'][lower]]
	#output_buy['diff_min_max_cci_upper_min_max'] = [diff_min_max_cci_intervals_minmax_buy['interval'][upper]]
	#output_buy['diff_min_max_cci_lower_min_max'] = [diff_min_max_cci_intervals_minmax_buy['interval'][lower]]
	#output_buy['diff_min_max_candle_upper_min_max'] = [diff_min_max_candle_intervals_minmax_buy['interval'][upper]]
	#output_buy['diff_min_max_candle_lower_min_max'] = [diff_min_max_candle_intervals_minmax_buy['interval'][lower]]
			#output_buy['value_max_lower_cci_min_max'] = [value_max_cci_minmax_buy['interval'][lower]]
			#output_buy['value_min_upper_cci_min_max'] = [value_min_cci_minmax_buy['interval'][upper]]

			#print('==== value min 2 ==> ',output_buy['value_min_upper_cci_min_max'])
			#print('==== value max 2 ==> ',output_buy['value_max_lower_cci_min_max'])

			if output_buy['num_trade_min_max'][0] != 0:
				if output_buy['num_st_min_max'][0] != 0:
					score_num_tp = (tp_counter-output_buy['num_st_min_max'][0])

					if (tp_counter-output_buy['num_st_min_max'][0]) == 0:
						score_num_tp = 8

					if (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_buy['max_st_min_max'][0] != 0:
				score_max_tp = (output_buy['max_tp_min_max'][0]-output_buy['max_st_min_max'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_buy['max_tp_min_max'][0]
				if (output_buy['max_tp_min_max'][0] != 0):
					score_max_tp = output_buy['max_tp_min_max'][0] * 10

			if (output_buy['mean_st_min_max'][0] != 0):
				score_mean_tp = (output_buy['mean_tp_min_max'][0]-output_buy['mean_st_min_max'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_buy['mean_tp_min_max'][0]
				if (output_buy['mean_tp_min_max'][0] != 0):
					score_mean_tp = output_buy['mean_tp_min_max'][0] * 10

			if (output_buy['sum_st_min_max'][0] != 0):
				score_sum_tp = (output_buy['sum_tp_min_max'][0]-output_buy['sum_st_min_max'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 1
			else:
				score_sum_tp = output_buy['sum_tp_min_max'][0]
				if (output_buy['sum_tp_min_max'][0] != 0):
					score_sum_tp = output_buy['sum_tp_min_max'][0] * 10

			output_buy['score_min_max'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]
			output_buy['score_pr'] = [0]
		else:
			output_buy['score_min_max'] = [0]
			output_buy['score_pr'] = [0]

		#///////////////////////////////////////////////

	#*********** Methode 1 Profits With MinMax Sell:
	if flag_trade == 'sell':

		output_sell = pd.DataFrame()

		if name_stp_minmax == True:

			#ramp_high_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_high',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#ramp_low_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_low',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_cci_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_cci',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_candle_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_candle',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#value_min_cci_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_min_cci',
			 #min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			#value_max_cci_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_max_cci',
			 #min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			list_index_ok = np.where(
				#((signal_sell['ramp_high'].to_numpy()<=ramp_high_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['ramp_low'].to_numpy()<=ramp_low_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['value_min_cci'].to_numpy()<=value_min_cci_minmax_sell['interval'][upper])) &
				#((signal_sell['value_max_cci'].to_numpy()>=value_max_cci_minmax_sell['interval'][lower]))
				True)[0]

			#list_index_ok = range(0,len(signal_sell))
		
			output_sell['mean_tp_min_max'] = [np.mean(signal_sell['tp_min_max'][list_index_ok])]
			output_sell['mean_st_min_max'] = [np.mean(signal_sell['st_min_max'][list_index_ok])]
			output_sell['max_tp_min_max'] = [np.max(signal_sell['tp_min_max'][list_index_ok])]
			output_sell['max_st_min_max'] = [np.max(signal_sell['st_min_max'][list_index_ok])]
			try:
				output_sell['sum_st_min_max'] = [np.sum(signal_sell['st_min_max'][list_index_ok[np.where(signal_sell['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_sell['sum_tp_min_max'] = [np.sum(signal_sell['tp_min_max'][list_index_ok[np.where(signal_sell['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
			except Exception as ex:
				print('tester minmax sell: ',ex)
				output_sell['sum_st_min_max'] = 0
				output_sell['sum_tp_min_max'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_sell['flag_min_max'][list_index_ok]:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_sell['num_tp_min_max'] = [tp_counter]
			output_sell['num_st_min_max'] = [st_counter]
			output_sell['num_trade_min_max'] = [st_counter + tp_counter]
	#output_sell['ramp_low_upper_min_max'] = [ramp_low_intervals_minmax_sell['interval'][upper]]
	#output_sell['ramp_low_lower_min_max'] = [ramp_low_intervals_minmax_sell['interval'][lower]]
	#output_sell['ramp_high_upper_min_max'] = [ramp_high_intervals_minmax_sell['interval'][upper]]
	#output_sell['ramp_high_lower_min_max'] = [ramp_high_intervals_minmax_sell['interval'][lower]]
	#output_sell['diff_min_max_cci_upper_min_max'] = [diff_min_max_cci_intervals_minmax_sell['interval'][upper]]
	#output_sell['diff_min_max_cci_lower_min_max'] = [diff_min_max_cci_intervals_minmax_sell['interval'][lower]]
	#output_sell['diff_min_max_candle_upper_min_max'] = [diff_min_max_candle_intervals_minmax_sell['interval'][upper]]
	#output_sell['diff_min_max_candle_lower_min_max'] = [diff_min_max_candle_intervals_minmax_sell['interval'][lower]]
			#output_sell['value_max_lower_cci_min_max'] = [value_max_cci_minmax_sell['interval'][lower]]
			#output_sell['value_min_upper_cci_min_max'] = [value_min_cci_minmax_sell['interval'][upper]]

			if output_sell['num_trade_min_max'][0] != 0:

				if output_sell['num_st_min_max'][0] != 0:
					score_num_tp = (tp_counter-output_sell['num_st_min_max'][0])

					if (tp_counter-output_sell['num_st_min_max'][0]) == 0:
						score_num_tp = 8

					if (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_sell['max_st_min_max'][0] != 0:
				score_max_tp = (output_sell['max_tp_min_max'][0]-output_sell['max_st_min_max'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_sell['max_tp_min_max'][0]
				if (output_sell['max_tp_min_max'][0] != 0):
					score_max_tp = output_sell['max_tp_min_max'][0] * 10

			if (output_sell['mean_st_min_max'][0] != 0):
				score_mean_tp = (output_sell['mean_tp_min_max'][0]-output_sell['mean_st_min_max'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_sell['mean_tp_min_max'][0]
				if (output_sell['mean_tp_min_max'][0] != 0):
					score_mean_tp = output_sell['mean_tp_min_max'][0] * 10

			if (output_sell['sum_st_min_max'][0] != 0):
				score_sum_tp = (output_sell['sum_tp_min_max'][0]-output_sell['sum_st_min_max'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 1
			else:
				score_sum_tp = output_sell['sum_tp_min_max'][0]
				if (output_sell['sum_tp_min_max'][0] != 0):
					score_sum_tp = output_sell['sum_tp_min_max'][0] * 10

			output_sell['score_min_max'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]
			output_sell['score_pr'] = [0]
		else:
			output_sell['score_min_max'] = [0]
			output_sell['score_pr'] = [0]

		#///////////////////////////////////////////////
	
	#*********** Methode 2 Profits With PR Buy:
	if flag_trade == 'buy':
		if name_stp_pr == True:

			#alpha = 0.2

			"""
			
			ramp_macd_intervals_pr = Find_Best_intervals(
															signals=signal_buy,
															apply_to='ramp_macd',
															min_tp=0.0, 
															max_st=0.0, 
															name_stp='flag_pr',
															alpha=alpha
															)

			ramp_candle_intervals_pr = Find_Best_intervals(
															signals=signal_buy,
															apply_to='ramp_candle',
															min_tp=0.0, 
															max_st=0.0, 
															name_stp='flag_pr',
															alpha=alpha
															)

			#diff_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_ramps',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#coef_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='coef_ramps',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#diff_min_max_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_macd',
				#min_tp=0.0, max_st=0.0, name_stp='flag_pr',alpha=0.5)

			#diff_min_max_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_candle',
				#min_tp=0.0, max_st=0.0, name_stp='flag_pr',alpha=0.5)

			#beta_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='beta',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#danger_line_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='danger_line',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

 			"""

			value_front_intervals_pr = Find_Best_intervals(
															signals=signal_buy,
															apply_to='value_front',
															min_tp=0.0,
															max_st=0.0,
															name_stp='flag_pr',
															alpha=alpha
															)

			value_back_intervals_pr = Find_Best_intervals(
														signals=signal_buy,
														apply_to='value_back',
														min_tp=0.0, 
														max_st=0.0, 
														name_stp='flag_pr',
														alpha=alpha
														)


			diff_top_pr_buy = Find_Best_intervals(
													signals=signal_buy,
													apply_to='tp_pr',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)

			diff_down_pr_buy = Find_Best_intervals(
													signals=signal_buy,
													apply_to='st_pr',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)

			diff_extereme_pr_buy = Find_Best_intervals(
													signals=signal_buy,
													apply_to='num_diff_to_extremes',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)


			list_index_ok = np.where(
				#((signal_buy['ramp_low'].to_numpy()>=ramp_low_intervals_pr_buy['interval'][lower]))&
				#((signal_buy['ramp_high'].to_numpy()>=ramp_high_intervals_pr_buy['interval'][lower]))&
				#(signal_buy['value_front'].to_numpy() <= value_front_intervals_pr['interval'][upper]) &
				#(signal_buy['value_back'].to_numpy() <= value_back_intervals_pr['interval'][upper]) 
				#(signal_buy['ramp_vol'].to_numpy() >= ramp_volume_intervals_pr['interval'][lower]) &
				#(signal_buy['power_pr_high'].to_numpy() >= power_high_pr_buy['interval'][lower]) &
				#(signal_buy['power_pr_low'].to_numpy() >= power_low_pr_buy['interval'][lower])
				#(signal_buy['ramp_candle'].to_numpy() <= ramp_candle_intervals_pr['interval'][upper]) &
				#(signal_buy['ramp_macd'].to_numpy() >= ramp_macd_intervals_pr['interval'][lower])
				True)[0]

			output_buy['mean_tp_pr'] = [np.mean(signal_buy['tp_pr'][np.where(signal_buy['flag_pr'] != 'no_flag')[0]])]
			output_buy['mean_st_pr'] = [np.mean(signal_buy['st_pr'][np.where(signal_buy['flag_pr'] != 'no_flag')[0]])]
			output_buy['max_tp_pr'] = [np.max(signal_buy['tp_pr'])]
			output_buy['max_st_pr'] = [np.max(signal_buy['st_pr'])]
			try:
				output_buy['sum_st_pr'] = [np.sum(signal_buy['st_pr'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy())]
				output_buy['sum_tp_pr'] = [np.sum(signal_buy['tp_pr'][np.where(signal_buy['flag_pr'] == 'tp')[0]].to_numpy())]
			except Exception as ex:
				print('error tester pr buy: ',ex)
				output_buy['sum_st_pr'] = 0
				output_buy['sum_tp_pr'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_buy['flag_pr']:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_buy['num_tp_pr'] = [tp_counter]
			output_buy['num_st_pr'] = [st_counter]
			output_buy['num_trade_pr'] = [st_counter + tp_counter]

			output_buy['max_st'] = [round(diff_down_pr_buy['interval'][upper],2)]
			output_buy['min_st'] = [round(diff_down_pr_buy['interval'][lower],2)]
			output_buy['max_tp'] = [round(diff_top_pr_buy['interval'][upper],2)]
			output_buy['min_tp'] = [round(diff_top_pr_buy['interval'][lower],2)]

			#output_buy['value_front_intervals_pr_upper'] = [value_front_intervals_pr['interval'][upper]]
			#output_buy['value_front_intervals_pr_lower'] = [value_front_intervals_pr['interval'][lower]]
			#output_buy['value_back_intervals_pr_upper'] = [value_back_intervals_pr['interval'][upper]]
			#output_buy['value_back_intervals_pr_lower'] = [value_back_intervals_pr['interval'][lower]]
			
			output_buy['diff_extereme_pr'] = [round(diff_extereme_pr_buy['interval'][upper])]

			#output_buy['ramp_vol'] = [ramp_volume_intervals_pr['interval'][lower]]
			#output_buy['value_back'] = [value_back_intervals_pr['interval'][upper]]
			#output_buy['value_front'] = [value_front_intervals_pr['interval'][upper]]

			#output_buy['power_pr_high'] = [power_high_pr_buy['interval'][lower]]
			#output_buy['power_pr_low'] = [power_low_pr_buy['interval'][lower]]

			#output_buy['ramp_macd'] = [ramp_macd_intervals_pr['interval'][lower]]
			#output_buy['ramp_candle'] = [ramp_candle_intervals_pr['interval'][upper]]


			if output_buy['num_trade_pr'][0] != 0:

				if output_buy['num_st_pr'][0] != 0:
					score_num_tp = (tp_counter-output_buy['num_st_pr'][0])

					if (tp_counter-output_buy['num_st_pr'][0]) == 0:
						score_num_tp = 1.5

					elif (score_num_tp > 0):
						score_num_tp = 2#score_num_tp * 0.9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = 2.5#tp_counter * 1
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_buy['max_st_pr'][0] != 0:
				score_max_tp = (output_buy['max_tp_pr'][0]-output_buy['max_st_pr'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_buy['max_tp_pr'][0]
				if (output_buy['max_tp_pr'][0] != 0):
					score_max_tp = output_buy['max_tp_pr'][0] * 10

			if (output_buy['mean_st_pr'][0] != 0):
				score_mean_tp = (output_buy['mean_tp_pr'][0]-output_buy['mean_st_pr'][0])

				if (score_mean_tp > 0):
					score_mean_tp = 2#score_mean_tp * 100
				elif (score_mean_tp == 0):
					score_mean_tp = 1.5
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_buy['mean_tp_pr'][0]
				if (output_buy['mean_tp_pr'][0] != 0):
					score_mean_tp = 2.5#output_buy['mean_tp_pr'][0] * 200

			if (output_buy['sum_st_pr'][0] != 0):
				score_sum_tp = (output_buy['sum_tp_pr'][0]-output_buy['sum_st_pr'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 0.1
			else:
				score_sum_tp = output_buy['sum_tp_pr'][0]
				if (output_buy['sum_tp_pr'][0] != 0):
					score_sum_tp = output_buy['sum_tp_pr'][0] * 10

			score_money = round(((signal_buy['money'].iloc[-1] - signal_buy['money'][0])/signal_buy['money'][0]),2) * 100

			output_buy['money'] = [score_money]

			if score_money <= 0 : score_money = 1

			output_buy['score_pr'] = [(score_sum_tp*score_mean_tp*score_num_tp*score_money)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

			if name_stp_minmax != True:
				output_buy['score_min_max'] = [0]
	
		else:
			output_buy['score_pr'] = [0]

			if name_stp_minmax != True:
				output_buy['score_min_max'] = [0]

		if np.isnan(output_buy['score_pr'][0]) : output_buy['score_pr'][0] = 0
		if np.isnan(output_buy['score_min_max'][0]) : output_buy['score_min_max'][0] = 0

		if (output_buy['score_pr'][0] > output_buy['score_min_max'][0]):
			output_buy['methode'] = ['pr']

		if (output_buy['score_min_max'][0] >= output_buy['score_pr'][0]):
			output_buy['methode'] = ['min_max']

		if (output_buy['score_pr'][0] == 0) and (output_buy['score_min_max'][0] == 0):
			output_buy['methode'] = ['no_trade']

	#///////////////////////////////////////////////
	
	#*********** Methode 2 Profits With PR Sell:
	if flag_trade == 'sell':
		if name_stp_pr == True:
			value_front_intervals_pr = Find_Best_intervals(
															signals=signal_sell,
															apply_to='value_front',
															min_tp=0.0,
															max_st=0.0,
															name_stp='flag_pr',
															alpha=alpha
															)
			value_back_intervals_pr = Find_Best_intervals(
														signals=signal_sell,
														apply_to='value_back',
														min_tp=0.0, 
														max_st=0.0, 
														name_stp='flag_pr',
														alpha=alpha
														)
			diff_top_pr_sell = Find_Best_intervals(
													signals=signal_sell,
													apply_to='tp_pr',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)
			diff_down_pr_sell = Find_Best_intervals(
													signals=signal_sell,
													apply_to='st_pr',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)

			diff_extereme_pr_sell = Find_Best_intervals(
													signals=signal_sell,
													apply_to='num_diff_to_extremes',
													min_tp=0.0, 
													max_st=0, 
													name_stp='flag_pr',
													alpha=alpha
													)
			list_index_ok = np.where(
				#((signal_sell['ramp_low'].to_numpy()<=ramp_low_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['ramp_high'].to_numpy()<=ramp_high_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['diff_pr_top'].to_numpy()<=diff_top_intervals_pr_sell['interval'][upper]))&
				#(signal_sell['diff_pr_down'].to_numpy()<=diff_down_intervals_pr_sell['interval'][upper])&
				#((signal_sell['trend_long'].to_numpy()!='buy')&
				#((signal_sell['trend_mid'].to_numpy()!='buy')&
				#(signal_sell['trend_short1'].to_numpy()=='sell')&
				#(signal_sell['trend_short2'].to_numpy()=='sell')))
				#((signal_sell['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['value_min_cci'].to_numpy()<=value_min_cci_pr_sell['interval'][upper]))&
				#((signal_sell['value_max_cci'].to_numpy()>=value_max_cci_pr_sell['interval'][lower]))
				True)[0]

			output_sell['mean_tp_pr'] = [np.mean(signal_sell['tp_pr'][np.where(signal_sell['flag_pr'] != 'no_flag')[0]])]
			output_sell['mean_st_pr'] = [np.mean(signal_sell['st_pr'][np.where(signal_sell['flag_pr'] != 'no_flag')[0]])]
			output_sell['max_tp_pr'] = [np.max(signal_sell['tp_pr'])]
			output_sell['max_st_pr'] = [np.max(signal_sell['st_pr'])]

			try:
				output_sell['sum_st_pr'] = [np.sum(signal_sell['st_pr'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy())]
				output_sell['sum_tp_pr'] = [np.sum(signal_sell['tp_pr'][np.where(signal_sell['flag_pr'] == 'tp')[0]].to_numpy())]
			except Exception as ex:
				print('error tester pr sell: ',ex)
				output_sell['sum_st_pr'] = 0
				output_sell['sum_tp_pr'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_sell['flag_pr']:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1

			output_sell['num_tp_pr'] = [tp_counter]
			output_sell['num_st_pr'] = [st_counter]
			output_sell['num_trade_pr'] = [st_counter + tp_counter]

			output_sell['max_st'] = [round(diff_down_pr_sell['interval'][upper],2)]
			output_sell['min_st'] = [round(diff_down_pr_sell['interval'][lower],2)]
			output_sell['max_tp'] = [round(diff_top_pr_sell['interval'][upper],2)]
			output_sell['min_tp'] = [round(diff_top_pr_sell['interval'][lower],2)]

			#output_sell['value_front_intervals_pr_upper'] = [value_front_intervals_pr['interval'][upper]]
			#output_sell['value_front_intervals_pr_lower'] = [value_front_intervals_pr['interval'][lower]]
			#output_sell['value_back_intervals_pr_upper'] = [value_back_intervals_pr['interval'][upper]]
			#output_sell['value_back_intervals_pr_lower'] = [value_back_intervals_pr['interval'][lower]]

			output_sell['diff_extereme_pr'] = [round(diff_extereme_pr_sell['interval'][upper])]

			if output_sell['num_trade_pr'][0] != 0:

				if output_sell['num_st_pr'][0] != 0:
					score_num_tp = (tp_counter-output_sell['num_st_pr'][0])

					if (tp_counter-output_sell['num_st_pr'][0] == 0):
						score_num_tp = 1.5

					elif (score_num_tp > 0):
						score_num_tp = 2
					else:
						score_num_tp = 1

				else:
					if tp_counter != 0:
						score_num_tp = 2.5
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_sell['max_st_pr'][0] != 0:
				score_max_tp = (output_sell['max_tp_pr'][0]-output_sell['max_st_pr'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1

			else:
				score_max_tp = output_sell['max_tp_pr'][0]
				if (output_sell['max_tp_pr'][0] != 0):
					score_max_tp = output_sell['max_tp_pr'][0] * 10


			if (output_sell['mean_st_pr'][0] != 0):
				score_mean_tp = (output_sell['mean_tp_pr'][0]-output_sell['mean_st_pr'][0])

				if (score_mean_tp > 0):
					score_mean_tp = 2#score_mean_tp * 100
				elif (score_mean_tp == 0):
					score_mean_tp = 1.5
				else:
					score_mean_tp = 1

			else:
				score_mean_tp = output_sell['mean_tp_pr'][0]
				if (output_sell['mean_tp_pr'][0] != 0):
					score_mean_tp = 2.5#output_sell['mean_tp_pr'][0] * 200


			if (output_sell['sum_st_pr'][0] != 0):
				score_sum_tp = (output_sell['sum_tp_pr'][0]-output_sell['sum_st_pr'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 0.1

			else:
				score_sum_tp = output_sell['sum_tp_pr'][0]
				if (output_sell['sum_tp_pr'][0] != 0):
					score_sum_tp = output_sell['sum_tp_pr'][0] * 10

			score_money = round(((signal_sell['money'].iloc[-1] - signal_sell['money'][0])/signal_sell['money'][0]),2) * 100

			output_sell['money'] = [score_money]

			if score_money <= 0 : score_money = 1

			output_sell['score_pr'] = [(score_num_tp*score_sum_tp*score_mean_tp*score_money)]

			if name_stp_minmax != True:
				output_sell['score_min_max'] = [0]

		else: 
			output_sell['score_pr'] = [0]
			if name_stp_minmax != True:
				output_sell['score_min_max'] = [0]

		if np.isnan(output_sell['score_pr'][0]) : output_sell['score_pr'][0] = 0
		if np.isnan(output_sell['score_min_max'][0]) : output_sell['score_min_max'][0] = 0

		if (output_sell['score_pr'][0] > output_sell['score_min_max'][0]):
			output_sell['methode'] = ['pr']

		if (output_sell['score_min_max'][0] >= output_sell['score_pr'][0]):
			output_sell['methode'] = ['min_max']

		if (output_sell['score_pr'][0] == 0) and (output_sell['score_min_max'][0] == 0):
			output_sell['methode'] = ['no_trade']

	if flag_trade == 'buy':
		output_sell = pd.DataFrame()

	if flag_trade == 'sell':
		output_buy = pd.DataFrame()

	return output_buy,output_sell
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

#**************************************************** Create First Cromosomes *******************************************************
#@stTime
def initilize_values_genetic(
							fast_period_upper,
							fast_period_lower,
							slow_period_upper,
							slow_period_lower,
							signal_period_upper,
							signal_period_lower
							):
	#************************** initialize Values ******************************************************
	Chromosome = {}

	Chromosome[0] = {
	'fast_period': fast_period_upper,
	'slow_period': slow_period_upper,
	'signal_period': signal_period_lower,
	'apply_to': 'HLCC/4',
	'alpha': 0.5,
	'num_extreme': int(fast_period_upper/10),#fast_period_upper,#int(randint(50,500)/10),#slow_period_upper - fast_period_upper,
	'diff_extereme': 25,#slow_period_upper,
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}

	Chromosome[1] = {
	'fast_period': fast_period_lower,
	'slow_period': slow_period_lower,
	'signal_period': signal_period_upper,
	'apply_to': 'open',
	'alpha': 0.1,
	'num_extreme': int(fast_period_lower/10),#fast_period_lower*6,#int(randint(50,500)/10),#slow_period_lower - fast_period_lower,
	'diff_extereme': 25,#slow_period_lower,
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}
	i = 2
	
	while i < 5:
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		
		#while max_tp < max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		Chromosome[i] = {
			'fast_period': randint(fast_period_lower, fast_period_upper),
			'slow_period': randint(slow_period_lower, slow_period_upper),
			'signal_period': randint(signal_period_lower, signal_period_upper),
			'apply_to': np.random.choice(apply_to_list_ga),
			'alpha': randint(1, 50)/100,
			'num_extreme': int(fast_period_upper/10),#int(randint(50,500)/10),#randint(int(fast_period_lower*0.25),(slow_period_upper-fast_period_lower)),
			'diff_extereme': 25,#randint(1,slow_period_upper),
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
			}

		if (Chromosome[i]['slow_period'] <= Chromosome[i]['fast_period'] * 2): continue
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

#@stTime
def gen_creator(
				Chromosome,
				fast_period_upper,
				fast_period_lower,
				slow_period_upper,
				slow_period_lower,
				signal_period_upper,
				signal_period_lower
				):

	Chromosome_Cutter = randint(0, 6)

	Chromosome_selector = randint(0, 5)

	baby = {}

	#print('Generate Baby')
	chrom_creator_counter = 0
	baby_counter = 0

	baby_counter_create = 0

	while (baby_counter_create < (len(Chromosome) * 2)):
		
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		#while max_tp <= max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		baby[baby_counter_create] = {
			'fast_period': randint(fast_period_lower, fast_period_upper),
			'slow_period': randint(slow_period_lower, slow_period_upper),
			'signal_period': randint(signal_period_lower, signal_period_upper),
			'apply_to': np.random.choice(apply_to_list_ga),
			'alpha': randint(1, 50)/100,
			'num_extreme': int(randint(50,500)/10),#randint(int(fast_period_lower*0.25),(slow_period_upper-fast_period_lower)),
			'diff_extereme': 25,#slow_period_upper,
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

		Chromosome_Cutter = randint(0, 6)
		change_chrom_counter = 0

		while change_chrom_counter < Chromosome_Cutter:
						#print(change_chrom_counter)
			baby[baby_counter].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})

			change_chrom_counter += 1

		change_chrom_counter = Chromosome_Cutter

		while change_chrom_counter < 6:
			baby[baby_counter].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			change_chrom_counter += 1

		baby_counter = baby_counter + 2

					#********************************************///////***************************************************************************
		chrom_creator_counter += 1

	i = 0
	limit_counter = len(Chromosome) * 2 
	while i < (limit_counter):
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		#while max_tp <= max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		Chromosome[i] = {
			'fast_period': randint(fast_period_lower, fast_period_upper),
			'slow_period': randint(slow_period_lower, slow_period_upper),
			'signal_period': randint(signal_period_lower, signal_period_upper),
			'apply_to': np.random.choice(apply_to_list_ga),
			'alpha': randint(1, 50)/100,
			'num_extreme': int(randint(50,500)/10),#randint(int(fast_period_lower*0.25),(slow_period_upper-fast_period_lower)),
			'diff_extereme': 25,#slow_period_upper,
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
			}

		if (Chromosome[i]['slow_period'] <= Chromosome[i]['fast_period'] * 2): continue
		i += 1

	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome[re_counter]['fast_period'] = baby[re_counter]['fast_period']
		Chromosome[re_counter]['slow_period'] = baby[re_counter]['slow_period']
		Chromosome[re_counter]['signal_period'] = baby[re_counter]['signal_period']
		Chromosome[re_counter]['apply_to'] = baby[re_counter]['apply_to']
		Chromosome[re_counter]['alpha'] = baby[re_counter]['alpha']
		Chromosome[re_counter]['num_extreme'] = baby[re_counter]['num_extreme']
		Chromosome[re_counter]['diff_extereme'] = baby[re_counter]['diff_extereme']
		Chromosome[re_counter]['signal'] = baby[re_counter]['signal']
		Chromosome[re_counter]['score_buy'] = baby[re_counter]['score_buy']
		Chromosome[re_counter]['score_sell'] = baby[re_counter]['score_sell']

		if (Chromosome[re_counter]['slow_period'] <= Chromosome[re_counter]['fast_period'] * 2):
			slow_period = randint(slow_period_lower, slow_period_upper) 
			fast_period = randint(fast_period_lower, fast_period_upper)
			while slow_period <= fast_period * 2:
				slow_period = randint(slow_period_lower, slow_period_upper) 
				fast_period = randint(fast_period_lower, fast_period_upper)

			Chromosome[re_counter] = {
						'fast_period': fast_period,
						'slow_period': slow_period,
						'signal_period': randint(signal_period_lower, signal_period_upper),
						'apply_to': np.random.choice(apply_to_list_ga),
						'alpha': randint(1, 50)/100,
						'num_extreme': int(fast_period/10),#int(randint(50,500)/10),#randint(int(fast_period*0.25),(slow_period-fast_period)),
						'diff_extereme': 25,#slow_period,
						'signal': None,
						'score_buy': 0,
						'score_sell': 0
						}
		re_counter += 1

	for key in Chromosome.keys():
		i = 0
		while i < len(Chromosome):
			if key == i:
				i += 1
				continue
			if (
				Chromosome[key]['fast_period'] == Chromosome[i]['fast_period'] and
				Chromosome[key]['slow_period'] == Chromosome[i]['slow_period'] and
				Chromosome[key]['signal_period'] == Chromosome[i]['signal_period'] and
				Chromosome[key]['apply_to'] == Chromosome[i]['apply_to'] and
				Chromosome[key]['alpha'] == Chromosome[i]['alpha'] and
				Chromosome[key]['num_extreme'] == Chromosome[i]['num_extreme'] and
				Chromosome[key]['diff_extereme'] == Chromosome[i]['diff_extereme']
				):

				#max_tp = randint(10, 80)/100
				#max_st = randint(10, 70)/100
		
				#while max_tp < max_st:
					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100

				slow_period = randint(slow_period_lower, slow_period_upper) 
				fast_period = randint(fast_period_lower, fast_period_upper)
				while slow_period <= fast_period * 2:
					slow_period = randint(slow_period_lower, slow_period_upper) 
					fast_period = randint(fast_period_lower, fast_period_upper)

				Chromosome[i] = {
							'fast_period': fast_period,
							'slow_period': slow_period,
							'signal_period': randint(signal_period_lower, signal_period_upper),
							'apply_to': np.random.choice(apply_to_list_ga),
							'alpha': randint(1, 50)/100,
							'num_extreme': int(fast_period/10),#int(randint(50,500)/10),#randint(int(fast_period*0.25),(slow_period-fast_period)),
							'diff_extereme': 25,#slow_period,
							'signal': None,
							'score_buy': 0,
							'score_sell': 0
							}
			i += 1
		#print(Chromosome_5M[6])

	return Chromosome

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#***************************************** Genetic Algorithm **************************************************************

#@stTime
#@cuda.jit()
def genetic_algo_div_macd(
							symbol_data_5M,
							symbol_data_15M,
							dataset_1H,
							dataset_4H,
							symbol,
							num_turn,
							max_score_ga_buy,
							max_score_ga_sell,
							flag_trade,
							primary_doing,
							secondry_doing
							):

	#*************************** Algorithm *************************************************//

	fast_period_upper = 800
	fast_period_lower = 60

	slow_period_upper = 1500
	slow_period_lower = 140

	signal_period_upper = 25
	signal_period_lower = 1

	Chromosome = initilize_values_genetic(
										fast_period_upper=fast_period_upper,
										fast_period_lower=fast_period_lower,
										slow_period_upper=slow_period_upper,
										slow_period_lower=slow_period_lower,
										signal_period_upper=signal_period_upper,
										signal_period_lower=signal_period_lower
										)

	if flag_trade == 'buy':
		if primary_doing == True:
			buy_path = 'GA/MACD/primary/buy/'+symbol+'.csv'
		if secondry_doing == True:
			buy_path = 'GA/MACD/secondry/buy/'+symbol+'.csv'

	if flag_trade == 'sell':
		if primary_doing == True:
			sell_path = 'GA/MACD/primary/sell/'+symbol+'.csv'
		if secondry_doing == True:
			sell_path = 'GA/MACD/secondry/sell/'+symbol+'.csv'

	if False:#flag_trade == 'buy':
		if os.path.exists(buy_path):
			with open(buy_path, 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					chrom_get = line

					Chromosome[0]['fast_period'] = int(float(chrom_get['fast_period']))
					Chromosome[0]['slow_period'] = int(float(chrom_get['slow_period']))

					if flag_trade == 'buy':
						fast_period_upper = Chromosome[0]['fast_period'] + int(Chromosome[0]['fast_period']/2)
						fast_period_lower = Chromosome[0]['fast_period'] - int(Chromosome[0]['fast_period']/2)

						if fast_period_lower <= 0: fast_period_lower = 1

						slow_period_upper = Chromosome[0]['slow_period'] + int(Chromosome[0]['slow_period']/2)
						slow_period_lower = Chromosome[0]['slow_period'] - int(Chromosome[0]['slow_period']/2)

						if slow_period_lower <= 0: slow_period_lower = 1

						signal_period_upper = Chromosome[0]['signal_period'] + int(Chromosome[0]['signal_period']/2)
						signal_period_lower = Chromosome[0]['signal_period'] - int(Chromosome[0]['signal_period']/2)

						if signal_period_lower <= 0: signal_period_lower = 1

	if False:#flag_trade == 'sell':
		if os.path.exists(sell_path):
			with open(sell_path, 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					chrom_get = line

					Chromosome[0]['fast_period'] = int(float(chrom_get['fast_period']))
					Chromosome[0]['slow_period'] = int(float(chrom_get['slow_period']))

					if flag_trade == 'sell':
						fast_period_upper = 20#Chromosome[0]['fast_period'] + int(Chromosome[0]['fast_period']/2)
						fast_period_lower = 5#Chromosome[0]['fast_period'] - int(Chromosome[0]['fast_period']/2)

						if fast_period_lower <= 0: fast_period_lower = 1

						slow_period_upper = 40#Chromosome[0]['slow_period'] + int(Chromosome[0]['slow_period']/2)
						slow_period_lower = 10#Chromosome[0]['slow_period'] - int(Chromosome[0]['slow_period']/2)

						if slow_period_lower <= 0: slow_period_lower = 1

						signal_period_upper = Chromosome[0]['signal_period'] + int(Chromosome[0]['signal_period']/2)
						signal_period_lower = Chromosome[0]['signal_period'] - int(Chromosome[0]['signal_period']/2)

						if signal_period_lower <= 0: signal_period_lower = 1

	Chromosome = initilize_values_genetic(
										fast_period_upper=fast_period_upper,
										fast_period_lower=fast_period_lower,
										slow_period_upper=slow_period_upper,
										slow_period_lower=slow_period_lower,
										signal_period_upper=signal_period_upper,
										signal_period_lower=signal_period_lower
										)

	print('================================ START Genetic BUY ==> ',symbol)
	print('\n')

	now = datetime.now()

	if flag_trade == 'buy':
		if os.path.exists(buy_path):
			if primary_doing == True:
				ga_result_buy, _, _, _ = read_ga_result(symbol=symbol)

			if secondry_doing == True:
				_, ga_result_buy, _, _ = read_ga_result(symbol=symbol)

			max_st_buy = ga_result_buy['max_st'][0]
			min_st_buy = ga_result_buy['min_st'][0]
			max_tp_buy = ga_result_buy['max_tp'][0]
			min_tp_buy = ga_result_buy['min_tp'][0]
			flag_learning = True

		else:
			max_st_buy = randint(80, 100)/100
			min_st_buy = randint(80, 100)/100
			max_tp_buy = randint(80, 100)/100
			min_tp_buy = randint(80, 100)/100

			flag_learning = False

			while max_tp_buy < max_st_buy:
				max_st_buy = randint(80, 100)/100
				min_st_buy = randint(80, 100)/100
				max_tp_buy = randint(80, 100)/100

	if flag_trade == 'sell':
		if os.path.exists(sell_path):
			if primary_doing == True:
				_, _, ga_result_sell, _ = read_ga_result(symbol=symbol)

			if secondry_doing == True:
				_, _, _, ga_result_sell = read_ga_result(symbol=symbol)

			max_st_sell = ga_result_sell['max_st'][0]
			min_st_sell = ga_result_sell['min_st'][0]
			max_tp_sell = ga_result_sell['max_tp'][0]
			min_tp_sell = ga_result_sell['min_tp'][0]
			flag_learning = True

		else:
			max_st_sell = randint(80, 100)/100
			min_st_sell = randint(80, 100)/100
			max_tp_sell = randint(80, 100)/100
			min_tp_sell = randint(80, 100)/100

			flag_learning = False

			while max_tp_sell < max_st_sell:
				max_st_sell = randint(80, 100)/100
				min_st_sell = randint(80, 100)/100
				max_tp_sell = randint(80, 100)/100
				min_tp_sell = randint(80, 100)/100

	#print('===============> ',symbol)

	if flag_trade == 'buy':
		if os.path.exists(buy_path):
			with open(buy_path, 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					chrom_get = line

					Chromosome[0]['fast_period'] = int(float(chrom_get['fast_period']))
					Chromosome[0]['slow_period'] = int(float(chrom_get['slow_period']))
					Chromosome[0]['signal_period'] = int(float(chrom_get['signal_period']))
					Chromosome[0]['apply_to'] = chrom_get['apply_to']
					Chromosome[0]['alpha'] = float(chrom_get['alpha'])
					Chromosome[0]['num_extreme'] = int(float(chrom_get['num_extreme']))
					Chromosome[0]['diff_extereme'] = int(float(chrom_get['diff_extereme']))
					Chromosome[0]['signal'] = chrom_get['signal']
					Chromosome[0]['score_buy'] = float(chrom_get['score_buy'])
					Chromosome[0]['score_sell'] = float(chrom_get['score_sell'])

					if flag_trade == 'buy':
						if primary_doing == True:
							ga_result_buy, _, _, _ = read_ga_result(symbol=symbol)

						if secondry_doing == True:
							_, ga_result_buy, _, _ = read_ga_result(symbol=symbol)

						if ga_result_buy['methode'][0] == 'min_max':
							max_score_ga_buy = float(chrom_get['score_min_max'])

						if ga_result_buy['methode'][0] == 'pr':
							max_score_ga_buy = float(chrom_get['score_pr'])
					print(Chromosome[0])

	if flag_trade == 'sell':
		if os.path.exists(sell_path):
			with open(sell_path, 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					chrom_get = line
					Chromosome[0]['fast_period'] = int(float(chrom_get['fast_period']))
					Chromosome[0]['slow_period'] = int(float(chrom_get['slow_period']))
					Chromosome[0]['signal_period'] = int(float(chrom_get['signal_period']))
					Chromosome[0]['apply_to'] = chrom_get['apply_to']
					Chromosome[0]['alpha'] = float(chrom_get['alpha'])
					Chromosome[0]['num_extreme'] = int(float(chrom_get['num_extreme']))
					Chromosome[0]['diff_extereme'] = int(float(chrom_get['diff_extereme']))
					Chromosome[0]['signal'] = chrom_get['signal']
					Chromosome[0]['score_buy'] = float(chrom_get['score_buy'])
					Chromosome[0]['score_sell'] = float(chrom_get['score_sell'])

					if flag_trade == 'sell':
						if primary_doing == True:
							_, _, ga_result_sell, _ = read_ga_result(symbol=symbol)

						if secondry_doing == True:
							_, _, _, ga_result_sell = read_ga_result(symbol=symbol)

						if ga_result_sell['methode'][0] == 'min_max':
							max_score_ga_sell = float(chrom_get['score_min_max'])

						if ga_result_sell['methode'][0] == 'pr':
							max_score_ga_sell = float(chrom_get['score_pr'])
					print(Chromosome[0])

				

	result_buy = pd.DataFrame()
	chromosome_buy = pd.DataFrame()

	result_sell = pd.DataFrame()
	chromosome_sell = pd.DataFrame()

	chrom_counter = 0
	all_chorms = 0
	chorm_reset_counter = 0
	bad_score_counter_buy = 0
	bad_score_counter_buy_2 = 0
	score_buy = max_score_ga_buy
	score_for_reset = 0

	bad_score_counter_sell = 0
	bad_score_counter_sell_2 = 0
	score_sell = max_score_ga_sell
	score_for_reset_sell = 0

	learning_interval_counter = 0
	learn_counter = 1

	with tqdm(total=num_turn) as pbar:
		while chrom_counter < len(Chromosome):

			#print('==== flag trade===> ', flag_trade)
			print()

			if flag_trade == 'buy':
				print()
				print('================== Num BUY Symbol ==>',symbol)
				print()
				print('================== Num BUY =========> ',len(chromosome_buy))

			if flag_trade == 'sell':
				print()
				print('================== Num SELL Symbol =>',symbol)
				print()
				print('================== Num SELL ========> ',len(chromosome_sell))

			print('================== Num Chroms ======> ',chrom_counter)
			print('================== All Chorms ======> ',all_chorms)
			print('================== Chorm Reseter ===> ',chorm_reset_counter)
			print('================== AI Turn =========> ',learn_counter-1)

			if flag_trade == 'buy':
				print('===== bad score counter buy ========> ',bad_score_counter_buy)
				print('===== bad score counter buy 2 ======> ',bad_score_counter_buy_2)

			if flag_trade == 'sell':
				print('===== bad score counter buy ========> ',bad_score_counter_sell)
				print('===== bad score counter buy 2 ======> ',bad_score_counter_sell_2)

			print()
			pbar_numbers = int((len(chromosome_buy) + len(chromosome_sell))/2)
			pbar.update(pbar_numbers)

			print()
			

			if (chorm_reset_counter >= 50):
				chorm_reset_counter = 0
				Chromosome.pop(chrom_counter)

				slow_period = randint(slow_period_lower, slow_period_upper) 
				fast_period = randint(fast_period_lower, fast_period_upper)
				while slow_period <= fast_period * 1.3:
					slow_period = randint(slow_period_lower, slow_period_upper) 
					fast_period = randint(fast_period_lower, fast_period_upper)

				max_st_buy = randint(80, 100)/100
				min_st_buy = randint(80, 100)/100
				max_tp_buy = randint(80, 100)/100
				min_tp_buy = randint(80, 100)/100

				flag_learning = False

				while max_tp_buy < max_st_buy:
					max_st_buy = randint(80, 100)/100
					min_st_buy = randint(80, 100)/100
					max_tp_buy = randint(80, 100)/100

				max_st_sell = randint(80, 100)/100
				min_st_sell = randint(80, 100)/100
				max_tp_sell = randint(80, 100)/100
				min_tp_sell = randint(80, 100)/100

				flag_learning = False

				while max_tp_sell < max_st_sell:
					max_st_sell = randint(80, 100)/100
					min_st_sell = randint(80, 100)/100
					max_tp_sell = randint(80, 100)/100

				Chromosome[chrom_counter] = {
					'fast_period': fast_period,
					'slow_period': slow_period,
					'signal_period': randint(signal_period_lower, signal_period_upper),
					'apply_to': np.random.choice(apply_to_list_ga),
					'alpha': randint(1, 50)/100,
					'num_extreme': int(fast_period/10),#int(randint(50,500)/10),#randint(int(fast_period*0.25),(slow_period-fast_period)),
					'diff_extereme': 25,
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				#all_chorms += 1
				#continue

			if False:#learning_interval_counter >= 100:

				learning_interval_counter = 0

				if learn_counter >= 5: break

				low_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))
				high_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))

				while (high_distance < low_distance) or (high_distance - low_distance != 10000):

					low_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))
					high_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))

				print('==== High Distance =============> ',high_distance)
				print('==== Low Distance ==============> ',low_distance)

				print('==== Symbol ====================> ',symbol)

				print('==== AI Turn ===================> ',learn_counter)
				print('==== Length Dataset ============> ',high_distance - low_distance)
				

				dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, _ = read_dataset_csv(
																									sym=symbol,
																									num_5M=99000,
																									num_15M=1,
																									num_1H=8250,
																									num_4H=1
																									)
				symbol_data_5M,symbol_data_1H = dataset_spliter(
															symbol=symbol,
															dataset_5M=dataset_5M,
															dataset_1H=dataset_1H,
															spliter_5M_end=high_distance,
															spliter_5M_first=low_distance
															)
				learn_counter += 1

			chorm_reset_counter += 1
			all_chorms += 1

			with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				print('======== Chorme ================> ')
				print()
				print('........................................................')
				print(Chromosome[chrom_counter])
				print('........................................................')
				print()

			if flag_trade == 'buy':
				print('======== max st tp ================> ')
				print()
				print('........................................................')
				print('======== max tp ===================> ',max_tp_buy)
				print('======== min tp ===================> ',min_tp_buy)
				print('======== max st ===================> ',max_st_buy)
				print('======== min st ===================> ',min_st_buy)
				print('........................................................')
				print()

			if flag_trade == 'sell':
				print('======== max st tp ================> ')
				print()
				print('........................................................')
				print('======== max tp ===================> ',max_tp_sell)
				print('======== min tp ===================> ',min_tp_sell)
				print('======== max st ===================> ',max_st_sell)
				print('======== min st ===================> ',min_st_sell)
				print('........................................................')
				print()

			try:
				if flag_trade == 'buy':
					if primary_doing == True:
						buy_data, _, _, _ = divergence_macd(
															dataset=symbol_data_5M,
															dataset_15M=symbol_data_15M,
															dataset_1H=dataset_1H,
															Apply_to=Chromosome[chrom_counter]['apply_to'],
															symbol=symbol,
															macd_fast=Chromosome[chrom_counter]['fast_period'],
															macd_slow=Chromosome[chrom_counter]['slow_period'],
															macd_signal=Chromosome[chrom_counter]['signal_period'],
															mode='optimize',
															plot=False,
															buy_doing=True,
															sell_doing=False,
															primary_doing=True,
															secondry_doing=False,
															name_stp_pr=True,
															name_stp_minmax=False,
															st_percent_buy_max = max_st_buy,
															st_percent_buy_min = min_st_buy,
															st_percent_sell_max = 0,
															st_percent_sell_min = 0,
															tp_percent_buy_max = max_tp_buy,
															tp_percent_buy_min = min_tp_buy,
															tp_percent_sell_max = 0,
															tp_percent_sell_min = 0,
															alpha=Chromosome[chrom_counter]['alpha'],
															num_exteremes=Chromosome[chrom_counter]['num_extreme'],
															diff_extereme=Chromosome[chrom_counter]['diff_extereme'],
															real_test = True,
															flag_learning=flag_learning
															)
					if secondry_doing == True:
						_, buy_data, _, _ = divergence_macd(
															dataset=symbol_data_5M,
															dataset_15M=symbol_data_15M,
															dataset_1H=dataset_1H,
															Apply_to=Chromosome[chrom_counter]['apply_to'],
															symbol=symbol,
															macd_fast=Chromosome[chrom_counter]['fast_period'],
															macd_slow=Chromosome[chrom_counter]['slow_period'],
															macd_signal=Chromosome[chrom_counter]['signal_period'],
															mode='optimize',
															plot=False,
															buy_doing=True,
															sell_doing=False,
															primary_doing=False,
															secondry_doing=True,
															name_stp_pr=True,
															name_stp_minmax=False,
															st_percent_minmax_buy = max_st_buy,
															st_percent_minmax_sell = 0.9,
															tp_percent_minmax_sell_max = 0.9,
															tp_percent_minmax_buy_max = max_tp_buy
															)
					#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						#print('=======> buy_data = ',buy_data))

				if flag_trade == 'sell':
					if primary_doing == True:
						_, _, sell_data, _ = divergence_macd(
															dataset=symbol_data_5M,
															dataset_15M=symbol_data_15M,
															dataset_1H=dataset_1H,
															Apply_to=Chromosome[chrom_counter]['apply_to'],
															symbol=symbol,
															macd_fast=Chromosome[chrom_counter]['fast_period'],
															macd_slow=Chromosome[chrom_counter]['slow_period'],
															macd_signal=Chromosome[chrom_counter]['signal_period'],
															mode='optimize',
															plot=False,
															buy_doing=False,
															sell_doing=True,
															primary_doing=True,
															secondry_doing=False,
															name_stp_pr=True,
															name_stp_minmax=False,
															st_percent_buy_max=0,
															st_percent_buy_min=0,
															st_percent_sell_max=max_st_sell,
															st_percent_sell_min=min_st_sell,
															tp_percent_buy_max=0,
															tp_percent_buy_min=0,
															tp_percent_sell_max=max_tp_sell,
															tp_percent_sell_min=min_tp_sell,
															alpha=Chromosome[chrom_counter]['alpha'],
															num_exteremes=Chromosome[chrom_counter]['num_extreme'],
															diff_extereme=Chromosome[chrom_counter]['diff_extereme'],
															real_test = True,
															flag_learning=flag_learning
															)

					if secondry_doing == True:
						_, _, _, sell_data = divergence_macd(
															dataset=symbol_data_5M,
															dataset_15M=symbol_data_15M,
															dataset_1H=dataset_1H,
															Apply_to=Chromosome[chrom_counter]['apply_to'],
															symbol=symbol,
															macd_fast=Chromosome[chrom_counter]['fast_period'],
															macd_slow=Chromosome[chrom_counter]['slow_period'],
															macd_signal=Chromosome[chrom_counter]['signal_period'],
															mode='optimize',
															plot=False,
															buy_doing=False,
															sell_doing=True,
															primary_doing=False,
															secondry_doing=True,
															name_stp_pr=True,
															name_stp_minmax=False,
															st_percent_minmax_buy = 0.9,
															st_percent_minmax_sell = max_st_buy,
															tp_percent_minmax_sell_max = max_tp_buy,
															tp_percent_minmax_buy_max = 0.9
															)
					#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						#print('=======> sell_data = ',sell_data))

	
				flag_golden_cross = False

				if flag_trade == 'buy' and buy_data.empty==True:
					flag_golden_cross = True

				if flag_trade == 'sell' and sell_data.empty==True:
					flag_golden_cross = True

			except Exception as ex:
				print('getting error GA Golden Cross: ', ex)
				flag_golden_cross = True

			if flag_golden_cross:

				Chromosome[chrom_counter] = {
					'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
					'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
					'signal_period': randint(signal_period_lower, signal_period_upper),
					'apply_to': np.random.choice(apply_to_list_ga),
					'alpha': randint(1, 50)/100,
					'num_extreme': randint(5,int(Chromosome[chrom_counter]['num_extreme'])),#int(randint(50,500)/10),#randint(int(Chromosome[chrom_counter]['fast_period']*0.25),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
					'diff_extereme': 25,#randint(2,Chromosome[chrom_counter]['diff_extereme']),
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				continue

			try:
				if flag_trade == 'buy':
					output_buy, _ = tester_div_macd(
													signal_buy=buy_data,
													signal_sell=buy_data,
													min_tp=0,
													max_st=0,
													alpha=Chromosome[chrom_counter]['alpha'],
													name_stp_minmax=False,
													name_stp_pr=True,
													flag_trade='buy'
													)
					with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						print('======== Output Buy =======> ')
						print()
						print('........................................................')
						print(output_buy)
						print('........................................................')
						print()

				if flag_trade == 'sell':
					_, output_sell = tester_div_macd(
													signal_buy=sell_data,
													signal_sell=sell_data,
													min_tp=0,
													max_st=0,
													alpha=Chromosome[chrom_counter]['alpha'],
													name_stp_minmax=False,
													name_stp_pr=True,
													flag_trade='sell'
													)
					with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						print('======== Output SELL ======> ')
						print()
						print('........................................................')
						print(output_sell)
						print('........................................................')
						print()

				flag_tester = False
			except Exception as ex:
				print('GA tester: ',ex)
				flag_tester = True

			if flag_tester:

				Chromosome[chrom_counter] = {
					'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
					'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
					'signal_period': randint(signal_period_lower, signal_period_upper),
					'apply_to': np.random.choice(apply_to_list_ga),
					'alpha': randint(1, 50)/100,
					'num_extreme': int(Chromosome[chrom_counter]['fast_period']/10),#int(randint(50,500)/10),#randint(int(Chromosome[chrom_counter]['fast_period']*0.25),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
					'diff_extereme': 25,#Chromosome[chrom_counter]['slow_period'],
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				continue

			if flag_trade == 'buy':
				if not np.isnan(output_buy['score_pr'][0]) or not np.isnan(output_buy['score_min_max'][0]):
					if (
						(
							output_buy['score_pr'][0] >= max_score_ga_buy * 0.99 and
							np.isnan(output_buy['score_pr'][0]) == False
						) or						
						(
							output_buy['score_min_max'][0] >= max_score_ga_buy * 0.99 and
							np.isnan(output_buy['score_min_max'][0]) == False
						)
						):

						max_st_last_buy = max_st_buy
						min_st_last_buy = min_st_buy
						max_tp_last_buy = max_tp_buy
						min_tp_last_buy = min_tp_buy

						if output_buy['max_tp'][0] >= 0.1:
							max_tp_buy = output_buy['max_tp'][0]
						else:
							max_tp_buy = output_buy['max_tp_pr'][0]#randint(50, 100)/100

						if output_buy['min_tp'][0] >= 0.1:
							min_tp_buy = output_buy['min_tp'][0]
						else:
							min_tp_buy = output_buy['mean_tp_pr'][0]


						if output_buy['max_st'][0] >= 0.1:
							max_st_buy = output_buy['max_st'][0]

							#if max_st_buy > max_tp_buy:
								#max_st_buy = max_tp_buy
						else:
							max_st_buy = output_buy['max_st_pr'][0]#randint(50, 100)/100

							#while max_tp_buy < max_st_buy:
								#max_st_buy = randint(15, 100)/100

						if output_buy['min_st'][0] >= 0.1:
							min_st_buy = output_buy['min_st'][0]

						else:
							min_st_buy = output_buy['mean_st_pr'][0]#randint(50, 100)/100

						if flag_learning == True:

							output_buy['max_tp'][0] = max_tp_last_buy
							output_buy['max_st'][0] = max_st_last_buy
							output_buy['min_st'][0] = min_st_last_buy
							output_buy['min_tp'][0] = min_tp_last_buy
						
							Chromosome[chrom_counter]['signal'] = ('buy' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
							result_buy = result_buy.append(output_buy, ignore_index=True)
							score_buy = (output_buy['score_pr'][0])


							if os.path.exists(buy_path):
								max_score_ga_buy_before = ga_result_buy['score_pr'][0] #* 0.9
							else:
								max_score_ga_buy_before = max_score_ga_buy #* 0.9

							max_score_ga_buy = (output_buy['score_pr'][0])

							if (max_score_ga_buy >= 90000):
								if (
									os.path.exists(buy_path) and
									max_score_ga_buy > max_score_ga_buy_before
									):
									max_score_ga_buy = max_score_ga_buy_before #* 0.9
								else:
									if os.path.exists(buy_path): max_score_ga_buy = ga_result_buy['score_pr'][0] #* 0.9
									if not os.path.exists(buy_path): max_score_ga_buy = 90000

							Chromosome[chrom_counter].update({'score_buy': score_buy })
							chromosome_buy = chromosome_buy.append(Chromosome[chrom_counter], ignore_index=True)
							chorm_reset_counter = 0

							bad_score_counter_buy = 0

							score_for_reset = 0

							max_st_buy = randint(80, 100)/100
							min_st_buy = randint(80, 100)/100
							max_tp_buy = randint(80, 100)/100
							min_tp_buy = randint(80, 100)/100

							if output_buy['diff_extereme_pr'][0] != 0:
								diff_extereme_pr_buy = output_buy['diff_extereme_pr'][0]
							else:
								diff_extereme_pr_buy = randint(1,Chromosome[chrom_counter]['slow_period'])

							flag_learning = False

							while max_tp_buy < max_st_buy:
								max_st_buy = randint(80, 100)/100
								max_tp_buy = randint(80, 100)/100
						#max_score_ga_buy = np.max(chromosome_buy['score_pr'],1)
						#print('MMMMMMMMMaxxxxxxx ==========> ',max_score_ga_buy)

							bad_buy = False
						else:
							bad_score_counter_buy += 1
							bad_buy = True
							flag_learning = True
							score_for_reset = (output_buy['score_pr'][0])

							if output_buy['diff_extereme_pr'][0] != 0:
								diff_extereme_pr_buy = output_buy['diff_extereme_pr'][0]
							else:
								diff_extereme_pr_buy = randint(1,Chromosome[chrom_counter]['slow_period'])

					else:
						bad_buy = True

						bad_score_counter_buy += 1

						if (
							output_buy['max_tp'][0] >= 0.1 and
							output_buy['score_pr'][0] >= score_for_reset and
							output_buy['max_tp'][0] > output_buy['min_st'][0]*1.2
							):
							max_tp_buy = output_buy['max_tp'][0]
							flag_learning = True
						else:
							if (
								output_buy['score_pr'][0] >= score_for_reset and
								output_buy['min_st'][0] >= 0.1 and
								output_buy['max_st'][0] >= 0.1
								):
								max_tp_buy = randint(int((output_buy['max_st'][0]/2)*100), int(output_buy['max_st'][0]*100)*2)/100

								while max_tp_buy <= output_buy['min_st'][0]:
									max_tp_buy = randint(int((output_buy['max_st'][0]/2)*100), int(output_buy['max_st'][0]*100)*2)/100

								flag_learning = True
							else:
								if (
									output_buy['max_tp'][0] == 0 and
									output_buy['min_tp'][0] == 0 and
									output_buy['max_st'][0] == 0 and
									output_buy['min_st'][0] == 0
									):
									max_tp_buy = output_buy['max_tp_pr'][0]
									flag_learning = True
								else:
									max_tp_buy = randint(80, 100)/100
									flag_learning = False

						if (
							output_buy['score_pr'][0] >= score_for_reset and
							output_buy['min_tp'][0] >= 0.1
							):
							min_tp_buy = output_buy['min_tp'][0]
							flag_learning = True
						else:
							if (
								output_buy['max_tp'][0] == 0 and
								output_buy['min_tp'][0] == 0 and
								output_buy['max_st'][0] == 0 and
								output_buy['min_st'][0] == 0
								):
								min_tp_buy = output_buy['mean_tp_pr'][0]
								flag_learning = True
							else:
								min_tp_buy = randint(80, 100)/100
								flag_learning = False

						if (
							output_buy['score_pr'][0] >= score_for_reset and
							output_buy['max_st'][0] >= 0.1
							):
							max_st_buy = output_buy['max_st'][0]
							flag_learning = True

						else:
							if (
								output_buy['max_tp'][0] == 0 and
								output_buy['min_tp'][0] == 0 and
								output_buy['max_st'][0] == 0 and
								output_buy['min_st'][0] == 0
								):
								max_st_buy = output_buy['max_st_pr'][0]
								flag_learning = True
							else:
								max_st_buy = randint(80, 100)/100
								flag_learning = False

							#while max_tp_buy < max_st_buy:
								#max_st_buy = randint(int((max_tp_buy/2)*100), 100)/100

						if (
							output_buy['score_pr'][0] >= score_for_reset and
							output_buy['min_st'][0] >= 0.1
							):
							min_st_buy = output_buy['min_st'][0]
							flag_learning = True

						else:
							if (
								output_buy['max_tp'][0] == 0 and
								output_buy['min_tp'][0] == 0 and
								output_buy['max_st'][0] == 0 and
								output_buy['min_st'][0] == 0
								):
								min_st_buy = output_buy['mean_st_pr'][0]
								flag_learning = True
							else:
								min_st_buy = randint(80, 100)/100
								flag_learning = False

								while max_tp_buy < min_st_buy:
									min_st_buy = randint(int((max_tp_buy/2)*100), 100)/100

						if output_buy['diff_extereme_pr'][0] != 0:
							diff_extereme_pr_buy = output_buy['diff_extereme_pr'][0]
						else:
							diff_extereme_pr_buy = randint(1,Chromosome[chrom_counter]['slow_period'])

						score_for_reset = output_buy['score_pr'][0]

			print('== Max Score Buy Must Be ====> ',max_score_ga_buy)

			if flag_trade == 'sell':
				if not np.isnan(output_sell['score_pr'][0]) or not np.isnan(output_sell['score_min_max'][0]):
					if (
						(
							output_sell['score_pr'][0] >= max_score_ga_sell * 0.99 and
							np.isnan(output_sell['score_pr'][0]) == False
						) or
						(
							output_sell['score_min_max'][0] >= max_score_ga_sell * 0.99 and
							np.isnan(output_sell['score_min_max'][0]) == False
						)
						):

						max_st_last_sell = max_st_sell
						min_st_last_sell = min_st_sell
						max_tp_last_sell = max_tp_sell
						min_tp_last_sell = min_tp_sell

						if output_sell['max_tp'][0] >= 0.1:
							max_tp_sell = output_sell['max_tp'][0]
						else:
							max_tp_sell = output_sell['max_tp_pr'][0]#randint(50, 100)/100

						if output_sell['min_tp'][0] >= 0.1:
							min_tp_sell = output_sell['min_tp'][0]
						else:
							min_tp_sell = output_sell['mean_tp_pr'][0]


						if output_sell['max_st'][0] >= 0.1:
							max_st_sell = output_sell['max_st'][0]

							#if max_st_buy > max_tp_buy:
								#max_st_buy = max_tp_buy
						else:
							max_st_sell = output_sell['max_st_pr'][0]#randint(50, 100)/100

							#while max_tp_buy < max_st_buy:
								#max_st_buy = randint(15, 100)/100

						if output_sell['min_st'][0] >= 0.1:
							min_st_sell = output_sell['min_st'][0]

						else:
							min_st_sell = output_sell['mean_st_pr'][0]#randint(50, 100)/100

						if flag_learning == True:

							output_sell['max_tp'][0] = max_tp_last_sell
							output_sell['max_st'][0] = max_st_last_sell
							output_sell['min_st'][0] = min_st_last_sell
							output_sell['min_tp'][0] = min_tp_last_sell
						
							Chromosome[chrom_counter]['signal'] = ('sell' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
							result_sell = result_sell.append(output_sell, ignore_index=True)
							score_sell = output_sell['score_pr'][0]


							if os.path.exists(sell_path):
								max_score_ga_sell_before = ga_result_sell['score_pr'][0] #* 0.9
							else:
								max_score_ga_sell_before = max_score_ga_sell #* 0.9

							max_score_ga_sell = (output_sell['score_pr'][0])

							if (max_score_ga_sell >= 90000):
								if (
									os.path.exists(sell_path) and
									max_score_ga_sell > max_score_ga_sell_before
									):
									max_score_ga_sell = max_score_ga_sell_before #* 0.9
								else:
									if os.path.exists(sell_path): max_score_ga_sell = ga_result_sell['score_pr'][0] #* 0.9
									if not os.path.exists(sell_path): max_score_ga_sell = 90000

							Chromosome[chrom_counter].update({'score_sell': score_sell })
							chromosome_sell = chromosome_sell.append(Chromosome[chrom_counter], ignore_index=True)
							chorm_reset_counter = 0

							bad_score_counter_sell = 0

							score_for_reset_sell = 0

							max_st_sell = randint(80, 100)/100
							min_st_sell = randint(80, 100)/100
							max_tp_sell = randint(80, 100)/100
							min_tp_sell = randint(80, 100)/100

							if output_sell['diff_extereme_pr'][0] != 0:
								diff_extereme_pr_sell = output_sell['diff_extereme_pr'][0]
							else:
								diff_extereme_pr_sell = randint(1,Chromosome[chrom_counter]['slow_period'])

							flag_learning = False

							while max_tp_sell < max_st_sell:
								max_st_sell = randint(80, 100)/100
								max_tp_sell = randint(80, 100)/100
						#max_score_ga_buy = np.max(chromosome_buy['score_pr'],1)
						#print('MMMMMMMMMaxxxxxxx ==========> ',max_score_ga_buy)

							bad_sell = False
						else:
							bad_score_counter_sell += 1
							bad_sell = True
							flag_learning = True
							score_for_reset_sell = (output_sell['score_pr'][0])

							if output_sell['diff_extereme_pr'][0] != 0:
								diff_extereme_pr_sell = output_sell['diff_extereme_pr'][0]
							else:
								diff_extereme_pr_sell = randint(1,Chromosome[chrom_counter]['slow_period'])
					else:
						bad_sell = True

						bad_score_counter_sell += 1

						if (
							output_sell['max_tp'][0] >= 0.1 and
							output_sell['score_pr'][0] >= score_for_reset_sell and
							output_sell['max_tp'][0] > output_sell['min_st'][0]*1.2
							):
							max_tp_sell = output_sell['max_tp'][0]
							flag_learning = True
						else:
							if (
								output_sell['score_pr'][0] >= score_for_reset_sell and
								output_sell['min_st'][0] >= 0.1 and
								output_sell['max_st'][0] >= 0.1
								):
								max_tp_sell = randint(int((output_sell['max_st'][0]/2)*100), int(output_sell['max_st'][0]*100)*2)/100

								while max_tp_sell <= output_sell['min_st'][0]:
									max_tp_sell = randint(int((output_sell['max_st'][0]/2)*100), int(output_sell['max_st'][0]*100)*2)/100

								flag_learning = True
							else:
								if (
									output_sell['max_tp'][0] == 0 and
									output_sell['min_tp'][0] == 0 and
									output_sell['max_st'][0] == 0 and
									output_sell['min_st'][0] == 0
									):
									max_tp_sell = output_sell['max_tp_pr'][0]
									flag_learning = True
								else:
									max_tp_sell = randint(80, 100)/100
									flag_learning = False

						if (
							output_sell['score_pr'][0] >= score_for_reset_sell and
							output_sell['min_tp'][0] >= 0.1
							):
							min_tp_sell = output_sell['min_tp'][0]
							flag_learning = True
						else:
							if (
								output_sell['max_tp'][0] == 0 and
								output_sell['min_tp'][0] == 0 and
								output_sell['max_st'][0] == 0 and
								output_sell['min_st'][0] == 0
								):
								min_tp_sell = output_sell['mean_tp_pr'][0]
								flag_learning = True
							else:
								min_tp_sell = randint(80, 100)/100
								flag_learning = False

						if (
							output_sell['score_pr'][0] >= score_for_reset_sell and
							output_sell['max_st'][0] >= 0.1
							):
							max_st_sell = output_sell['max_st'][0]
							flag_learning = True

						else:
							if (
								output_sell['max_tp'][0] == 0 and
								output_sell['min_tp'][0] == 0 and
								output_sell['max_st'][0] == 0 and
								output_sell['min_st'][0] == 0
								):
								max_st_sell = output_sell['max_st_pr'][0]
								flag_learning = True
							else:
								max_st_sell = randint(80, 100)/100
								flag_learning = False

							#while max_tp_buy < max_st_buy:
								#max_st_buy = randint(int((max_tp_buy/2)*100), 100)/100

						if (
							output_sell['score_pr'][0] >= score_for_reset_sell and
							output_sell['min_st'][0] >= 0.1
							):
							min_st_sell = output_sell['min_st'][0]
							flag_learning = True

						else:
							if (
								output_sell['max_tp'][0] == 0 and
								output_sell['min_tp'][0] == 0 and
								output_sell['max_st'][0] == 0 and
								output_sell['min_st'][0] == 0
								):
								min_st_sell = output_sell['mean_st_pr'][0]
								flag_learning = True
							else:
								min_st_sell = randint(80, 100)/100
								flag_learning = False

								while max_tp_sell < min_st_sell:
									min_st_sell = randint(int((max_tp_sell/2)*100), 100)/100

						if output_sell['diff_extereme_pr'][0] != 0:
							diff_extereme_pr_sell = output_sell['diff_extereme_pr'][0]
						else:
							diff_extereme_pr_sell = randint(1,Chromosome[chrom_counter]['slow_period'])

						score_for_reset_sell = output_sell['score_pr'][0]

			print('== Max Score Sell Must Be =====> ',max_score_ga_sell)

			if flag_trade == 'buy':
				if (
					len(chromosome_buy) >= int(num_turn/20)
					):
					break

			if flag_trade == 'sell':
				if (
					len(chromosome_sell) >= int(num_turn/20)
					):
					break

			#if (
				#len(chromosome_buy) >= int(num_turn/12) or
				#len(chromosome_sell) >= int(num_turn/12)
				#):
				#if (len(chromosome_buy) >= int(num_turn/12)) and (len(chromosome_sell) >= 4): break
				#if (len(chromosome_sell) >= int(num_turn/12)) and (len(chromosome_buy) >= 4): break

			if flag_trade == 'buy':
				if bad_buy == True:

					if bad_score_counter_buy < 4:
						Chromosome[chrom_counter] = {
										'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': Chromosome[chrom_counter]['signal_period'],#randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha': randint(1, 50)/100,
										'num_extreme': Chromosome[chrom_counter]['num_extreme'],#int(buy_data['num_extreme'][0]),#Chromosome[chrom_counter]['num_extreme'],#randint(int(Chromosome[chrom_counter]['fast_period']*0.5),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
										'diff_extereme': diff_extereme_pr_buy,
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}

					else:
						if (
							bad_score_counter_buy_2 >= 3
							):

							score_for_reset = 0

							bad_score_counter_buy = 0
							bad_score_counter_buy_2 = 0

							max_st_buy = randint(80, 100)/100
							min_st_buy = randint(80, 100)/100
							max_tp_buy = randint(80, 100)/100
							min_tp_buy = randint(80, 100)/100

							flag_learning = False

							while max_tp_buy < max_st_buy:
								max_st_buy = randint(70, 100)/100
								max_tp_buy = randint(80, 100)/100

							fast_period = randint(fast_period_lower,fast_period_upper)
							while Chromosome[chrom_counter]['slow_period'] < fast_period * 2:
								fast_period = randint(fast_period_lower,fast_period_upper)
								if (fast_period == Chromosome[chrom_counter]['fast_period']): continue

							Chromosome[chrom_counter] = {
										'fast_period': fast_period,#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha': randint(1, 50)/100,
										'num_extreme': int(fast_period/10),#randint(int(fast_period/2),fast_period*5),#int(randint(50,500)/10),#randint(int(fast_period*0.25),(Chromosome[chrom_counter]['slow_period']-fast_period)),
										'diff_extereme': 25,#Chromosome[chrom_counter]['slow_period'],
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}
						else:
							score_for_reset = 0

							bad_score_counter_buy_2 += 1
							bad_score_counter_buy = 0

							max_st_buy = randint(80, 100)/100
							min_st_buy = randint(80, 100)/100
							max_tp_buy = randint(80, 100)/100
							min_tp_buy = randint(80, 100)/100

							flag_learning = False

							while max_tp_buy < max_st_buy:
								max_st_buy = randint(70, 100)/100
								max_tp_buy = randint(80, 100)/100

							Chromosome[chrom_counter] = {
										'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha': randint(1, 50)/100,
										'num_extreme': int(buy_data['num_extreme'][0]),#randint(int(Chromosome[chrom_counter]['fast_period']/2),Chromosome[chrom_counter]['fast_period']*5),#int(randint(50,500)/10),#randint(int(Chromosome[chrom_counter]['fast_period']*0.25),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
										'diff_extereme': 25,#Chromosome[chrom_counter]['slow_period'],
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}

					continue


			if flag_trade == 'sell':
				if bad_sell == True:

					if bad_score_counter_sell < 4:
						Chromosome[chrom_counter] = {
										'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': Chromosome[chrom_counter]['signal_period'],#randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha': randint(1, 50)/100,
										'num_extreme': Chromosome[chrom_counter]['num_extreme'],#int(sell_data['num_extreme'][0]),#Chromosome[chrom_counter]['num_extreme'],#randint(int(Chromosome[chrom_counter]['fast_period']*0.5),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
										'diff_extereme': diff_extereme_pr_sell,
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}

					else:
						if (
							bad_score_counter_sell_2 >= 3
							):

							score_for_reset_sell = 0

							bad_score_counter_sell = 0
							bad_score_counter_sell_2 = 0

							max_st_sell = randint(80, 100)/100
							min_st_sell = randint(80, 100)/100
							max_tp_sell = randint(80, 100)/100
							min_tp_sell = randint(80, 100)/100

							flag_learning = False

							while max_tp_sell < max_st_sell:
								max_st_sell = randint(70, 100)/100
								max_tp_sell = randint(80, 100)/100

							fast_period = randint(fast_period_lower,fast_period_upper)
							while Chromosome[chrom_counter]['slow_period'] < fast_period * 2:
								fast_period = randint(fast_period_lower,fast_period_upper)
								if (fast_period == Chromosome[chrom_counter]['fast_period']): continue

							Chromosome[chrom_counter] = {
										'fast_period': fast_period,#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha': randint(1, 50)/100,
										'num_extreme': int(fast_period/10),#randint(int(fast_period/2),fast_period*2),#int(randint(50,500)/10),#randint(int(fast_period*0.25),(Chromosome[chrom_counter]['slow_period']-fast_period)),
										'diff_extereme': 25,#Chromosome[chrom_counter]['slow_period'],
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}
						else:
							score_for_reset_sell = 0

							bad_score_counter_sell_2 += 1
							bad_score_counter_sell = 0

							max_st_sell = randint(80, 100)/100
							min_st_sell = randint(80, 100)/100
							max_tp_sell = randint(80, 100)/100
							min_tp_sell = randint(80, 100)/100

							flag_learning = False

							while max_tp_sell < max_st_sell:
								max_st_sell = randint(70, 100)/100
								max_tp_sell = randint(80, 100)/100

							Chromosome[chrom_counter] = {
										'fast_period': Chromosome[chrom_counter]['fast_period'],#high_period,
										'slow_period': Chromosome[chrom_counter]['slow_period'],#low_period,
										'signal_period': randint(signal_period_lower, signal_period_upper),
										'apply_to': np.random.choice(apply_to_list_ga),
										'alpha':  randint(1, 50)/100,
										'num_extreme': int(sell_data['num_extreme'][0]),#randint(int(Chromosome[chrom_counter]['fast_period']/2),Chromosome[chrom_counter]['fast_period']*2),#randint(int(Chromosome[chrom_counter]['fast_period']*0.25),(Chromosome[chrom_counter]['slow_period']-Chromosome[chrom_counter]['fast_period'])),
										'diff_extereme': 25,#Chromosome[chrom_counter]['slow_period'],
										'signal': None,
										'score_buy': 0,
										'score_sell': 0
										}

					continue

			if Chromosome[chrom_counter]['signal'] is None: continue

			chrom_counter += 1
			learning_interval_counter += 1
			if (chrom_counter >= ((len(Chromosome)))):
				chrom_counter = 0
				Chromosome = gen_creator(
										Chromosome=Chromosome,
										fast_period_upper=fast_period_upper,
										fast_period_lower=fast_period_lower,
										slow_period_upper=slow_period_upper,
										slow_period_lower=slow_period_lower,
										signal_period_upper=signal_period_upper,
										signal_period_lower=signal_period_lower
										)
				continue

			
	
	#**************************** Best Find *********************************************************

	#************ Buy Find:
	if flag_trade == 'buy':

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print('=======> Chorme ===> ')
			print()
			print('........................................................')
			print(chromosome_buy)
			print('........................................................')
			print()

		best_buy = pd.DataFrame()
		max_score_buy_pr = np.max(result_buy['score_pr'].dropna())
		max_score_buy_min_max = np.max(result_buy['score_min_max'].dropna())
		max_score_buy = max(max_score_buy_pr,max_score_buy_min_max)
		best_buy_score_index = np.where((result_buy['score_pr']==max_score_buy) | (result_buy['score_min_max'] == max_score_buy))[0]
		best_dict = dict()
		for idx in best_buy_score_index:
			for clm in result_buy.columns:
				best_dict.update(
					{
					clm: result_buy[clm][idx]
					})
			for clm in chromosome_buy.columns:
				best_dict.update(
					{
					clm: chromosome_buy[clm][idx]
					})

			best_buy = best_buy.append(best_dict, ignore_index=True)
	#//////////////////////
	#********** Sell Find:
	if flag_trade == 'sell':

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print('=======> Chorme ===> ')
			print()
			print('........................................................')
			print(chromosome_sell)
			print('........................................................')
			print()

		best_sell = pd.DataFrame()
		max_score_sell_pr = np.max(result_sell['score_pr'].dropna())
		max_score_sell_min_max = np.max(result_sell['score_min_max'].dropna())
		max_score_sell = max(max_score_sell_pr,max_score_sell_min_max)
		best_sell_score_index = np.where((result_sell['score_pr']==max_score_sell) | (result_sell['score_min_max'] == max_score_sell))[0]
		best_dict = dict()
		for idx in best_sell_score_index:
			for clm in result_sell.columns:
				best_dict.update(
					{
					clm: result_sell[clm][idx]
					})
			for clm in chromosome_sell.columns:
				best_dict.update(
					{
					clm: chromosome_sell[clm][idx]
					})

			best_sell = best_sell.append(best_dict, ignore_index=True)
	#//////////////////////

	#********************************///////////////****************************************************************

	#*************************** Save to TXT File ***************************************************************

	if flag_trade == 'buy':
		try:
			if os.path.exists(buy_path):
				os.remove(buy_path)

			with open(buy_path, 'w', newline='') as myfile:
				fields = best_buy.columns.to_list()
				writer = csv.DictWriter(myfile, fieldnames=fields)
				writer.writeheader()
	
				for idx in range(len(best_buy)):
					rows = dict()
					for clm in best_buy.columns:
						rows.update({clm: best_buy[clm][idx]})
					writer.writerow(rows)
					
		except Exception as ex:
			print('some thing wrong: ', ex)

	if flag_trade == 'sell':
		try:
			if os.path.exists(sell_path):
				os.remove(sell_path)

			with open(sell_path, 'w', newline='') as myfile:
				fields = best_sell.columns.to_list()
				writer = csv.DictWriter(myfile, fieldnames=fields)
				writer.writeheader()
	
				for idx in range(len(best_sell)):
					rows = dict()
					for clm in best_sell.columns:
						rows.update({clm: best_sell[clm][idx]})
					writer.writerow(rows)
					
		except Exception as ex:
			print('some thing wrong: ', ex)

	print('/////////////////////// Finish Genetic BUY ',symbol,'///////////////////////////////////')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#********************** read GA result ****************************************************************************

@stTime
def read_ga_result(symbol):

	if os.path.exists('GA/MACD/primary/buy/'+symbol+'.csv'):
		ga_result_buy_primary = pd.read_csv('GA/MACD/primary/buy/'+symbol+'.csv')
	else:
		ga_result_buy_primary = pd.DataFrame()

	if os.path.exists('GA/MACD/secondry/buy/'+symbol+'.csv'):
		ga_result_buy_scondry = pd.read_csv('GA/MACD/secondry/buy/'+symbol+'.csv')
	else:
		ga_result_buy_scondry = pd.DataFrame()

	if os.path.exists('GA/MACD/primary/sell/'+symbol+'.csv'):
		ga_result_sell_primary = pd.read_csv('GA/MACD/primary/sell/'+symbol+'.csv')
	else:
		ga_result_sell_primary = pd.DataFrame()

	if os.path.exists('GA/MACD/secondry/sell/'+symbol+'.csv'):
		ga_result_sell_secondry = pd.read_csv('GA/MACD/secondry/sell/'+symbol+'.csv')
	else:
		ga_result_sell_secondry = pd.DataFrame()

	return ga_result_buy_primary, ga_result_buy_scondry, ga_result_sell_primary, ga_result_sell_secondry
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************** Tester For Permit ***********************************


def macd_div_tester_for_permit(
								dataset,
								dataset_15M,
								symbol_data_1H,
								symbol_data_4H,
								symbol,
								flag_trade,
								primary_doing,
								secondry_doing
								):

	upper = 0
	mid = 1
	lower = 2

	print('=================> ',symbol)

	if flag_trade == 'buy':
		if primary_doing == True:
			buy_path = 'GA/MACD/primary/buy/'+symbol+'.csv'
		if secondry_doing == True:
			buy_path = 'GA/MACD/secondry/buy/'+symbol+'.csv'

	if flag_trade == 'sell':
		if primary_doing == True:
			sell_path = 'GA/MACD/primary/sell/'+symbol+'.csv'
		if secondry_doing == True:
			sell_path = 'GA/MACD/secondry/sell/'+symbol+'.csv'

	if flag_trade == 'buy':
		if os.path.exists(buy_path):
			if primary_doing == True:
				ga_result_buy, _, _, _ = read_ga_result(symbol=symbol)

			if secondry_doing == True:
				_, ga_result_buy, _, _ = read_ga_result(symbol=symbol)

	if flag_trade == 'sell':
		if os.path.exists(sell_path):
			if primary_doing == True:
				_, _, ga_result_sell, _ = read_ga_result(symbol=symbol)

			if secondry_doing == True:
				_, _, _, ga_result_sell = read_ga_result(symbol=symbol)

	#********************************************** Buy Test:

	if flag_trade == 'buy':
		if ga_result_buy['methode'][0] != 'no_trade':
			if ga_result_buy['methode'][0] == 'pr':
				name_stp_pr = True
				name_stp_minmax = False
			elif ga_result_buy['methode'][0] == 'min_max':
				name_stp_pr = False
				name_stp_minmax = True

			print('******************* BUY *************************')
			if primary_doing == True:
				buy_data, _, _, _ = divergence_macd(
													dataset=dataset,
													dataset_15M=dataset_15M,
													dataset_1H=symbol_data_1H,
													Apply_to=ga_result_buy['apply_to'][0],
													symbol=symbol,
													macd_fast=ga_result_buy['fast_period'][0],
													macd_slow=ga_result_buy['slow_period'][0],
													macd_signal=ga_result_buy['signal_period'][0],
													mode='optimize',
													plot=False,
													buy_doing=True,
													sell_doing=False,
													primary_doing=True,
													secondry_doing=False,
													name_stp_pr=True,
													name_stp_minmax=False,
													st_percent_buy_max = ga_result_buy['max_st'][0],
													st_percent_buy_min = ga_result_buy['min_st'][0],
													st_percent_sell_max = 0,
													st_percent_sell_min = 0,
													tp_percent_buy_max = ga_result_buy['max_tp'][0],
													tp_percent_buy_min = ga_result_buy['min_tp'][0],
													tp_percent_sell_max=0,
													tp_percent_sell_min=0,
													alpha=ga_result_buy['alpha'][0],
													num_exteremes = ga_result_buy['num_extreme'][0],
													diff_extereme = ga_result_buy['diff_extereme'][0],
													real_test = True,
													flag_learning=True
													)
			if secondry_doing == True:
				_, buy_data, _, _ = divergence_macd(
													dataset=symbol_data_5M,
													dataset_15M=symbol_data_15M,
													dataset_1H=dataset_1H,
													Apply_to=Chromosome[chrom_counter]['apply_to'],
													symbol=symbol,
													macd_fast=Chromosome[chrom_counter]['fast_period'],
													macd_slow=Chromosome[chrom_counter]['slow_period'],
													macd_signal=Chromosome[chrom_counter]['signal_period'],
													mode='optimize',
													plot=False,
													buy_doing=True,
													sell_doing=False,
													primary_doing=False,
													secondry_doing=True,
													name_stp_pr=True,
													name_stp_minmax=False,
													st_percent_minmax_buy = max_st_buy,
													st_percent_minmax_sell = 0.9,
													tp_percent_minmax_sell_max = 0.9,
													tp_percent_minmax_buy_max = max_tp_buy
													)
					#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						#print('=======> buy_data = ',buy_data))

			#*********************** PR Methode BUY:
			if ga_result_buy['methode'][0] == 'pr':

				"""
				ramp_macd_intervals_pr = Find_Best_intervals(
															signals=buy_data,
															apply_to='ramp_macd',
															min_tp=0.0, 
															max_st=0.0, 
															name_stp='flag_pr',
															alpha=ga_result_buy['alpha'][0]
															)

				ramp_candle_intervals_pr = Find_Best_intervals(
																signals=buy_data,
																apply_to='ramp_candle',
																min_tp=0.0, 
																max_st=0.0, 
																name_stp='flag_pr',
																alpha=ga_result_buy['alpha'][0]
																)

			#diff_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_ramps',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#coef_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='coef_ramps',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#diff_min_max_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_macd',
				#min_tp=0.0, max_st=0.0, name_stp='flag_pr',alpha=0.5)

			#diff_min_max_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_candle',
				#min_tp=0.0, max_st=0.0, name_stp='flag_pr',alpha=0.5)

			#beta_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='beta',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

			#danger_line_intervals_minmax = Find_Best_intervals(signals=signal_buy,apply_to='danger_line',
 			#min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

				value_front_intervals_pr = Find_Best_intervals(
																signals=buy_data,
																apply_to='value_front',
																min_tp=0.0,
																max_st=0.0,
																name_stp='flag_pr',
																alpha=ga_result_buy['alpha'][0]
																)

				value_back_intervals_pr = Find_Best_intervals(
															signals=buy_data,
															apply_to='value_back',
															min_tp=0.0, 
															max_st=0.0, 
															name_stp='flag_pr',
															alpha=ga_result_buy['alpha'][0]
															)

				ramp_volume_intervals_pr = Find_Best_intervals(
 																signals=buy_data,
 																apply_to='ramp_vol',
 																min_tp=0.0, 
 																max_st=0.0, 
 																name_stp='flag_pr',
 																alpha=ga_result_buy['alpha'][0]
 																)

				print('value_front_intervals_pr = ',value_front_intervals_pr)
				print('value_back_intervals_pr = ',value_back_intervals_pr)
				print('ramp_macd_intervals_pr = ',ramp_macd_intervals_pr)
				print('ramp_candle_intervals_pr = ',ramp_candle_intervals_pr)

				list_index_ok = np.where(
					(buy_data['value_front'].to_numpy()<= -1.361925)&#value_front_intervals_pr['interval'][upper]) &
					(buy_data['value_front'].to_numpy()>= -1.979887)&#value_front_intervals_pr['interval'][lower]) &
					(buy_data['value_back'].to_numpy()<= -2.540192)&#value_back_intervals_pr['interval'][upper]) &
					(buy_data['value_back'].to_numpy()>= -3.493296)#value_back_intervals_pr['interval'][lower])
					#(buy_data['power_pr_low'].to_numpy()>=ga_result_buy['power_pr_low'][0])
					)[0]

				"""

				output_buy = pd.DataFrame()
				output_buy['mean_tp_pr'] = [np.mean(buy_data['tp_pr'][np.where(buy_data['flag_pr'] != 'no_flag')[0]])]
				output_buy['mean_st_pr'] = [np.mean(buy_data['st_pr'][np.where(buy_data['flag_pr'] != 'no_flag')[0]])]
				output_buy['max_tp_pr'] = [np.max(buy_data['tp_pr'])]
				output_buy['max_st_pr'] = [np.max(buy_data['st_pr'])]
				output_buy['sum_st_pr'] = [np.sum(buy_data['st_pr'][np.where(buy_data['flag_pr'] == 'st')[0]].to_numpy())]
				output_buy['sum_tp_pr'] = [np.sum(buy_data['tp_pr'][np.where(buy_data['flag_pr'] == 'tp')[0]].to_numpy())]

				tp_counter = 0
				st_counter = 0
				for elm in buy_data['flag_pr']:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_buy['num_tp_pr'] = [tp_counter]
				output_buy['num_st_pr'] = [st_counter]
				output_buy['num_trade_pr'] = [st_counter + tp_counter]
			

				if output_buy['num_trade_pr'][0] != 0:

					if output_buy['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_buy['num_st_pr'][0])

						if (tp_counter-output_buy['num_st_pr'][0]) == 0:
							score_num_tp = 1.5

						elif (score_num_tp > 0):
							score_num_tp = 2#score_num_tp * 0.9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = 2.5#tp_counter * 1
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_buy['max_st_pr'][0] != 0:
					score_max_tp = (output_buy['max_tp_pr'][0]-output_buy['max_st_pr'][0])

					if (score_max_tp > 0):
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1
				else:
					score_max_tp = output_buy['max_tp_pr'][0]
					if (output_buy['max_tp_pr'][0] != 0):
						score_max_tp = output_buy['max_tp_pr'][0] * 10

				if (output_buy['mean_st_pr'][0] != 0):
					score_mean_tp = (output_buy['mean_tp_pr'][0]-output_buy['mean_st_pr'][0])

					if (score_mean_tp > 0):
						score_mean_tp = 2#score_mean_tp * 100
					elif (score_mean_tp == 0):
						score_mean_tp = 1.5
					else:
						score_mean_tp = 1
				else:
					score_mean_tp = output_buy['mean_tp_pr'][0]
					if (output_buy['mean_tp_pr'][0] != 0):
						score_mean_tp = 2.5#output_buy['mean_tp_pr'][0] * 200

				if (output_buy['sum_st_pr'][0] != 0):
					score_sum_tp = (output_buy['sum_tp_pr'][0]-output_buy['sum_st_pr'][0])

					if (score_sum_tp > 0):
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 0.1
				else:
					score_sum_tp = output_buy['sum_tp_pr'][0]
					if (output_buy['sum_tp_pr'][0] != 0):
						score_sum_tp = output_buy['sum_tp_pr'][0] * 10

				score_money = round(((buy_data['money'].iloc[-1] - buy_data['money'][0])/buy_data['money'][0]),2) * 100

				output_buy['money'] = [score_money]
			
				if score_money <= 0 : score_money = 1


				output_buy['score_pr'] = [(score_sum_tp*score_mean_tp*score_num_tp*score_money)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_buy['score_pr'][0]) : output_buy['score_pr'][0] = 0

				print('=========> one year Buy: ',symbol)

				print('mean_tp_pr= ',output_buy['mean_tp_pr'][0])
				print('mean_st_pr= ',output_buy['mean_st_pr'][0])
				print('max_tp_pr= ',output_buy['max_tp_pr'][0])
				print('max_st_pr= ',output_buy['max_st_pr'][0])
				print('sum_st_pr= ',output_buy['sum_st_pr'][0])
				print('sum_tp_pr= ',output_buy['sum_tp_pr'][0])
				print('num_tp_pr= ',output_buy['num_tp_pr'][0])
				print('num_st_pr= ',output_buy['num_st_pr'][0])
				print('num_trade_pr= ',output_buy['num_trade_pr'][0])
				print('score_pr= ',output_buy['score_pr'][0])
				print('score_pr ga= ',ga_result_buy['score_pr'][0])

				for idx in buy_data['index'][np.where(buy_data['flag_pr'] == 'tp')[0]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in buy_data['index'][np.where(buy_data['flag_pr'] == 'st')[0]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if output_buy['score_pr'][0] * 10 >= ga_result_buy['score_pr'][0]*0.99: 
					ga_result_buy['permit'] = True
					#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

					if os.path.exists(buy_path):
						os.remove(buy_path)

					ga_result_buy.to_csv(buy_path)
				else:
					ga_result_buy['permit'] = False
					#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

					if os.path.exists(buy_path):
						os.remove(buy_path)

					ga_result_buy.to_csv(buy_path)

	#///////////////////////////////////////////////////////////////////////////////////////////////

	#********************************************** Sell Test:
	if flag_trade == 'sell':
		if ga_result_sell['methode'][0] != 'no_trade':
			if ga_result_sell['methode'][0] == 'pr':
				name_stp_pr = True
				name_stp_minmax = False
			elif ga_result_sell['methode'][0] == 'min_max':
				name_stp_pr = False
				name_stp_minmax = True

			print('******************* SELL *************************')

			_, _, sell_data, _ = divergence_macd(
												dataset=dataset,
												dataset_15M=dataset_15M,
												dataset_1H=symbol_data_1H,
												Apply_to=ga_result_sell['apply_to'][0],
												symbol=symbol,
												macd_fast=ga_result_sell['fast_period'][0],
												macd_slow=ga_result_sell['slow_period'][0],
												macd_signal=ga_result_sell['signal_period'][0],
												mode='optimize',
												plot=False,
												buy_doing=False,
												sell_doing=True,
												primary_doing=True,
												secondry_doing=False,
												name_stp_pr=True,
												name_stp_minmax=False,
												st_percent_buy_max = 0,
												st_percent_buy_min = 0,
												st_percent_sell_max=ga_result_sell['max_st'][0],
												st_percent_sell_min=ga_result_sell['min_st'][0],
												tp_percent_buy_max = 0,
												tp_percent_buy_min = 0,
												tp_percent_sell_max=ga_result_sell['max_tp'][0],
												tp_percent_sell_min=ga_result_sell['min_tp'][0],
												alpha=ga_result_sell['alpha'][0],
												num_exteremes = ga_result_sell['num_extreme'][0],
												diff_extereme = ga_result_sell['diff_extereme'][0],
												real_test = True,
												flag_learning=True
												)
			if secondry_doing == True:
				_, _, _, sell_data = divergence_macd(
													dataset=symbol_data_5M,
													dataset_15M=symbol_data_15M,
													dataset_1H=dataset_1H,
													Apply_to=ga_result_sell['apply_to'][0],
													symbol=symbol,
													macd_fast=ga_result_sell['fast_period'][0],
													macd_slow=ga_result_sell['slow_period'][0],
													macd_signal=ga_result_sell['signal_period'][0],
													mode='optimize',
													plot=False,
													buy_doing=False,
													sell_doing=True,
													primary_doing=False,
													secondry_doing=True,
													name_stp_pr=True,
													name_stp_minmax=False,
													st_percent_buy_max = 0,
													st_percent_buy_min = 0,
													st_percent_sell_max=ga_result_sell['max_st'][0],
													st_percent_sell_min=ga_result_sell['min_st'][0],
													tp_percent_buy_max = 0,
													tp_percent_buy_min = 0,
													tp_percent_sell_max=ga_result_sell['max_tp'][0],
													tp_percent_sell_min=ga_result_sell['min_tp'][0],
													alpha=ga_result_sell['alpha'][0],
													num_exteremes = ga_result_sell['num_extreme'][0]
													)

		#*********************** PR Methode:
			if ga_result_sell['methode'][0] == 'pr':

				output_sell = pd.DataFrame()

				with pd.option_context('display.max_rows', None, 'display.max_columns', None):
					print(sell_data)

				list_index_ok = np.where(
					#(sell_data['value_max_cci'].to_numpy()>=ga_result_sell['value_max_lower_cci_pr'][0]) &
					#(sell_data['power_pr_high'].to_numpy()>=ga_result_sell['power_pr_high'][0]) &
					#(sell_data['power_pr_low'].to_numpy()>=ga_result_sell['power_pr_low'][0])
					True)[0]

				output_sell = pd.DataFrame()
				output_sell['mean_tp_pr'] = [np.mean(sell_data['tp_pr'][np.where(sell_data['flag_pr'] != 'no_flag')[0]])]
				output_sell['mean_st_pr'] = [np.mean(sell_data['st_pr'][np.where(sell_data['flag_pr'] != 'no_flag')[0]])]
				output_sell['max_tp_pr'] = [np.max(sell_data['tp_pr'])]
				output_sell['max_st_pr'] = [np.max(sell_data['st_pr'])]
				output_sell['sum_st_pr'] = [np.sum(sell_data['st_pr'][np.where(sell_data['flag_pr'] == 'st')[0]].to_numpy())]
				output_sell['sum_tp_pr'] = [np.sum(sell_data['tp_pr'][np.where(sell_data['flag_pr'] == 'tp')[0]].to_numpy())]

				tp_counter = 0
				st_counter = 0
				for elm in sell_data['flag_pr']:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_sell['num_tp_pr'] = [tp_counter]
				output_sell['num_st_pr'] = [st_counter]
				output_sell['num_trade_pr'] = [st_counter + tp_counter]

				if output_sell['num_trade_pr'][0] != 0:

					if output_sell['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_sell['num_st_pr'][0])

						if (tp_counter-output_sell['num_st_pr'][0]) == 0:
							score_num_tp = 1.5

						elif (score_num_tp > 0):
							score_num_tp = 2#score_num_tp * 0.9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = 2.5#tp_counter * 1
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_sell['max_st_pr'][0] != 0:

					score_max_tp = (output_sell['max_tp_pr'][0]-output_sell['max_st_pr'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_sell['max_tp_pr'][0]
					if (output_sell['max_tp_pr'][0] != 0):
						score_max_tp = output_sell['max_tp_pr'][0] * 10

				if (output_sell['mean_st_pr'][0] != 0):

					score_mean_tp = (output_sell['mean_tp_pr'][0]-output_sell['mean_st_pr'][0])

					if (score_mean_tp > 0):
						score_mean_tp = 2#score_mean_tp * 100
					elif (score_mean_tp == 0):
						score_mean_tp = 1.5
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_sell['mean_tp_pr'][0]
					if (output_sell['mean_tp_pr'][0] != 0):
						score_mean_tp = 2.5#output_sell['mean_tp_pr'][0] * 200

				if (output_sell['sum_st_pr'][0] != 0):

					score_sum_tp = (output_sell['sum_tp_pr'][0]-output_sell['sum_st_pr'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 1

				else:
					score_sum_tp = output_sell['sum_tp_pr'][0]
					if (output_sell['sum_tp_pr'][0] != 0):
						score_sum_tp = output_sell['sum_tp_pr'][0] * 10

				score_money = round(((sell_data['money'].iloc[-1] - sell_data['money'][0])/sell_data['money'][0]),2) * 100

				output_sell['money'] = [score_money]
			
				if score_money <= 0 : score_money = 1


				output_sell['score_pr'] = [(score_num_tp*score_mean_tp*score_sum_tp*score_money)]

				if np.isnan(output_sell['score_pr'][0]) : output_sell['score_pr'][0] = 0

				print('=========> one year Sell: ',symbol)

				print('mean_tp_pr= ',output_sell['mean_tp_pr'][0])
				print('mean_st_pr= ',output_sell['mean_st_pr'][0])
				print('max_tp_pr= ',output_sell['max_tp_pr'][0])
				print('max_st_pr= ',output_sell['max_st_pr'][0])
				print('sum_st_pr= ',output_sell['sum_st_pr'][0])
				print('sum_tp_pr= ',output_sell['sum_tp_pr'][0])
				print('num_tp_pr= ',output_sell['num_tp_pr'][0])
				print('num_st_pr= ',output_sell['num_st_pr'][0])
				print('num_trade_pr= ',output_sell['num_trade_pr'][0])
				print('score_pr= ',output_sell['score_pr'][0])
				print('score_pr ga= ',ga_result_sell['score_pr'][0])

				for idx in sell_data['index'][np.where(sell_data['flag_pr'] == 'tp')[0]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in sell_data['index'][np.where(sell_data['flag_pr'] == 'st')[0]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if output_sell['score_pr'][0] * 10 >= ga_result_sell['score_pr'][0]*0.99:
					ga_result_sell['permit'] = True
					#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]

					if os.path.exists(sell_path):
						os.remove(sell_path)

					ga_result_sell.to_csv(sell_path)
				else:
					ga_result_sell['permit'] = False
					#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]
					
					if os.path.exists(sell_path):
						os.remove(sell_path)

					ga_result_sell.to_csv(sell_path)
		#////////////////////////////////////////
	print('//////////////////////////////////////////')

	if flag_trade == 'buy':
		output_sell = pd.DataFrame()

	if flag_trade == 'sell':
		output_buy = pd.DataFrame()

	return output_buy, output_sell

#///////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************** Last Signal Out ******************************************************

#@stTime
def last_signal_macd_div(
						dataset,
						dataset_1H,
						symbol
						):
	""" Last signal out """
	buy_path_primary = 'GA/MACD/primary/buy/'+symbol+'.csv'
	buy_path_secondry = 'GA/MACD/secondry/buy/'+symbol+'.csv'

	sell_path_primary = 'GA/MACD/primary/sell/'+symbol+'.csv'
	sell_path_secondry = 'GA/MACD/secondry/sell/'+symbol+'.csv'

	if os.path.exists(buy_path_primary):
		ga_result_buy_primary = pd.read_csv(buy_path_primary)

		if ga_result_buy_primary['permit'][0]:
			cross_cut_len_buy_primary = ga_result_buy_primary['slow_period'][0]
		else:
			cross_cut_len_buy_primary = 0
	else:
		cross_cut_len_buy_primary = 0

	if os.path.exists(buy_path_secondry):
		ga_result_buy_secondry = pd.read_csv(buy_path_secondry)

		if ga_result_buy_secondry['permit'][0]:
			cross_cut_len_buy_secondry = ga_result_buy_secondry['slow_period'][0]
		else:
			cross_cut_len_buy_secondry = 0
	else:
		cross_cut_len_buy_secondry = 0

	if os.path.exists(sell_path_primary):
		ga_result_sell_primary = pd.read_csv(sell_path_primary)

		if ga_result_sell_primary['permit'][0]:
			cross_cut_len_sell_primary = ga_result_sell_primary['slow_period'][0]
		else:
			cross_cut_len_sell_primary = 0
	else:
		cross_cut_len_sell_primary = 0

	if os.path.exists(sell_path_secondry):
		ga_result_sell_secondry = pd.read_csv(sell_path_secondry)

		if ga_result_sell_secondry['permit'][0]:
			cross_cut_len_sell_secondry = ga_result_sell_secondry['slow_period'][0]
		else:
			cross_cut_len_sell_secondry = 0
	else:
		cross_cut_len_sell_secondry = 0



	cross_cut_len_cutter = int(np.max(
									[
									cross_cut_len_buy_primary,
									cross_cut_len_buy_secondry,
									cross_cut_len_sell_primary,
									cross_cut_len_sell_secondry
									]))

	resist = protect = 0


	if os.path.exists(buy_path_primary):
		ga_result_buy_primary = pd.read_csv(buy_path_primary)

		if ga_result_buy_primary['permit'][0]:
			#cross_cut_len = 2 * cross_cut_len_cutter + 200
			#cut_first = 0
			#if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
				#cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

			#print(cut_first)
			#dataset_5M_cross = {
								#symbol: dataset[symbol].copy()
								#}

			#dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HL/2'] = dataset_5M_cross[symbol]['HL/2'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HL/2'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLCC/4'] = dataset_5M_cross[symbol]['HLCC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLCC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['OHLC/4'] = dataset_5M_cross[symbol]['OHLC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['OHLC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['volume'] = dataset_5M_cross[symbol]['volume'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['volume'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['time'] = dataset_5M_cross[symbol]['time'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['time'])-1)].reset_index(drop=True)


			buy_data_primary, _, _, _ = divergence_macd(
														dataset=dataset,
														dataset_15M=dataset,
														dataset_1H=dataset_1H,
														Apply_to=ga_result_buy_primary['apply_to'][0],
														symbol=symbol,
														macd_fast= int(ga_result_buy_primary['fast_period'][0]),
														macd_slow= int(ga_result_buy_primary['slow_period'][0]),
														macd_signal= int(ga_result_buy_primary['signal_period'][0]),
														mode='online',
														plot=False,
														buy_doing=True,
														sell_doing=False,
														primary_doing=True,
														secondry_doing=False,
														name_stp_pr=True,
														name_stp_minmax=False,
														st_percent_buy_max = ga_result_buy_primary['max_st'][0],
														st_percent_buy_min = ga_result_buy_primary['min_st'][0],
														st_percent_sell_max = 0,
														st_percent_sell_min = 0,
														tp_percent_buy_max = ga_result_buy_primary['max_tp'][0],
														tp_percent_buy_min = ga_result_buy_primary['min_tp'][0],
														tp_percent_sell_max = 0,
														tp_percent_sell_min = 0,
														alpha= ga_result_buy_primary['alpha'][0],
														num_exteremes= int(ga_result_buy_primary['num_extreme'][0]),
														diff_extereme = int(ga_result_buy_primary['diff_extereme'][0])
														)
			if (buy_data_primary.empty == False):
				lst_idx_buy_primary = int(buy_data_primary['index'].iloc[-1])#cut_first + 1
			else:
				lst_idx_buy_primary = 0
		else:
			lst_idx_buy_primary = 0
	else:
		signal = 'no_trade'
		lst_idx_buy_primary = 0


	if os.path.exists(buy_path_secondry):
		ga_result_buy_secondry = pd.read_csv(buy_path_secondry)

		if ga_result_buy_secondry['permit'][0]:

			#cross_cut_len = 2 * cross_cut_len_cutter + 200
			#cut_first = 0
			#if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
				#cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

			#dataset_5M_cross = {
								#symbol: dataset[symbol].copy()
								#}

			#dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HL/2'] = dataset_5M_cross[symbol]['HL/2'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HL/2'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLCC/4'] = dataset_5M_cross[symbol]['HLCC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLCC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['OHLC/4'] = dataset_5M_cross[symbol]['OHLC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['OHLC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['volume'] = dataset_5M_cross[symbol]['volume'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['volume'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['time'] = dataset_5M_cross[symbol]['time'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['time'])-1)].reset_index(drop=True)


			_, buy_data_secondry, _, _ = divergence_macd(
														dataset=dataset,
														dataset_15M=dataset,
														dataset_1H=dataset_1H,
														Apply_to=ga_result_buy_secondry['apply_to'][0],
														symbol=symbol,
														macd_fast= int(ga_result_buy_secondry['fast_period'][0]),
														macd_slow= int(ga_result_buy_secondry['slow_period'][0]),
														macd_signal= int(ga_result_buy_secondry['signal_period'][0]),
														mode='online',
														plot=False,
														buy_doing=True,
														sell_doing=False,
														primary_doing=False,
														secondry_doing=True,
														name_stp_pr=True,
														name_stp_minmax=False,
														#***************** Not Doing Yet *****************************
														st_percent_buy_max = ga_result_buy_secondry['max_st'][0],
														st_percent_buy_min = ga_result_buy_secondry['min_st'][0],
														st_percent_minmax_sell = 0.9,
														tp_percent_minmax_sell_max = 0.9,
														tp_percent_buy_max = ga_result_buy_secondry['max_tp'][0],
														tp_percent_buy_min = ga_result_buy_secondry['min_tp'][0],
														alpha= ga_result_buy_secondry['alpha'][0],
														num_exteremes= int(ga_result_buy_secondry['num_extreme'][0])
														)

			if (buy_data_secondry.empty == False):
				lst_idx_buy_secondry = int(buy_data_secondry['index'].iloc[-1])#cut_first + 1
			else:
				lst_idx_buy_secondry = 0
		else:
			lst_idx_buy_secondry = 0
	else:
		signal = 'no_trade'
		lst_idx_buy_secondry = 0


	if os.path.exists(sell_path_primary):
		ga_result_sell_primary = pd.read_csv(sell_path_primary)

		if ga_result_sell_primary['permit'][0] == True:

			#print(cross_cut_len_cutter)

			#cross_cut_len = 2 * cross_cut_len_cutter + 400
			#cut_first = 0
			#if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
				#cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

			#dataset_5M_cross = {
								#symbol: dataset[symbol].copy()
								#}

			#print('cut first = ',int(len(dataset_5M_cross[symbol]['low'])) - cut_first)

			#dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HL/2'] = dataset_5M_cross[symbol]['HL/2'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HL/2']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLCC/4'] = dataset_5M_cross[symbol]['HLCC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLCC/4']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['OHLC/4'] = dataset_5M_cross[symbol]['OHLC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['OHLC/4']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['volume'] = dataset_5M_cross[symbol]['volume'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['volume']))].reset_index(drop=True)
			#dataset_5M_cross[symbol]['time'] = dataset_5M_cross[symbol]['time'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['time']))].reset_index(drop=True)

			#print(dataset_5M_cross[symbol]['low'])

			_, _, sell_data_primary, _ = divergence_macd(
														dataset=dataset,
														dataset_15M=dataset,
														dataset_1H=dataset_1H,
														Apply_to=ga_result_sell_primary['apply_to'][0],
														symbol=symbol,
														macd_fast= int(ga_result_sell_primary['fast_period'][0]),
														macd_slow= int(ga_result_sell_primary['slow_period'][0]),
														macd_signal= int(ga_result_sell_primary['signal_period'][0]),
														mode='online',
														plot=False,
														buy_doing=False,
														sell_doing=True,
														primary_doing=True,
														secondry_doing=False,
														name_stp_pr=True,
														name_stp_minmax=False,
														st_percent_buy_max = 0,
														st_percent_buy_min = 0,
														st_percent_sell_max = ga_result_sell_primary['max_st'][0],
														st_percent_sell_min = ga_result_sell_primary['min_st'][0],
														tp_percent_buy_max = 0,
														tp_percent_buy_min = 0,
														tp_percent_sell_max = ga_result_sell_primary['max_tp'][0],
														tp_percent_sell_min = ga_result_sell_primary['min_tp'][0],
														alpha= ga_result_sell_primary['alpha'][0],
														num_exteremes= int(ga_result_sell_primary['num_extreme'][0]),
														diff_extereme = int(ga_result_sell_primary['diff_extereme'][0])
														)

			if (sell_data_primary.empty == False):
				lst_idx_sell_primary = int(sell_data_primary['index'].iloc[-1])
			else:
				lst_idx_sell_primary = 0
		else:
			lst_idx_sell_primary = 0
	else:
		signal = 'no_trade'
		lst_idx_sell_primary = 0
		

	if os.path.exists(sell_path_secondry):
		ga_result_sell_secondry = pd.read_csv(sell_path_secondry)

		if ga_result_sell_secondry['permit'][0]:

			#cross_cut_len = 2 * cross_cut_len_cutter + 200
			#cut_first = 0
			#if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
				#cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

			#dataset_5M_cross = {
			#					#symbol: dataset[symbol].copy()
								#}

			#dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HL/2'] = dataset_5M_cross[symbol]['HL/2'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HL/2'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['HLCC/4'] = dataset_5M_cross[symbol]['HLCC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLCC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['OHLC/4'] = dataset_5M_cross[symbol]['OHLC/4'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['OHLC/4'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['volume'] = dataset_5M_cross[symbol]['volume'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['volume'])-1)].reset_index(drop=True)
			#dataset_5M_cross[symbol]['time'] = dataset_5M_cross[symbol]['time'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['time'])-1)].reset_index(drop=True)


			_, _, _, sell_data_secondry = divergence_macd(
														dataset=dataset,
														dataset_15M=dataset,
														dataset_1H=dataset_1H,
														Apply_to=ga_result_sell_secondry['apply_to'][0],
														symbol=symbol,
														macd_fast= int(ga_result_sell_secondry['fast_period'][0]),
														macd_slow= int(ga_result_sell_secondry['slow_period'][0]),
														macd_signal= int(ga_result_sell_secondry['signal_period'][0]),
														mode='online',
														plot=False,
														buy_doing=False,
														sell_doing=True,
														primary_doing=True,
														secondry_doing=False,
														name_stp_pr=True,
														name_stp_minmax=False,
														#******** Dont Doing Not Yet ********************************
														st_percent_buy_max = ga_result_sell_secondry['max_st'][0],
														st_percent_buy_min = ga_result_sell_secondry['min_st'][0],
														st_percent_minmax_sell = 0.9,
														tp_percent_minmax_sell_max = 0.9,
														tp_percent_buy_max = ga_result_sell_secondry['max_tp'][0],
														tp_percent_buy_min = ga_result_sell_secondry['min_tp'][0],
														alpha= ga_result_sell_secondry['alpha'][0],
														num_exteremes= int(ga_result_sell_secondry['num_extreme'][0])
														)

			if (sell_data_secondry.empty == False):
				lst_idx_sell_secondry = int(sell_data_secondry['index'].iloc[-1])#cut_first + 1
			else:
				lst_idx_sell_secondry = 0
		else:
			lst_idx_sell_secondry = 0
	else:
		signal = 'no_trade'	
		lst_idx_sell_secondry = 0
		#return signal, resist, protect


	print('lst_idx_buy_primary =====> ',lst_idx_buy_primary)
	print('lst_idx_sell_primary =======> ',lst_idx_sell_primary)
	#print(buy_data_primary)

	#***** Last Signal:

	if (
		lst_idx_buy_primary > lst_idx_sell_primary and
		lst_idx_buy_primary > lst_idx_sell_secondry and
		lst_idx_buy_primary > lst_idx_buy_secondry and
		(len(dataset[symbol]['close']) - 1 - lst_idx_buy_primary) <= 1#ga_result_buy_primary['num_extreme'][0]
		):

		print('======> last signal buy ',symbol)
		print('dataset length: ',len(dataset[symbol]['close']))
		print('ga result buy methode: ',ga_result_buy_primary['methode'][0])
		print('last index: ',lst_idx_buy_primary)
		

		if ga_result_buy_primary['methode'][0] == 'pr':

			if lst_idx_buy_primary != 0:

				dataset_pr_5M = pd.DataFrame()

				cut_first = 0
				if (lst_idx_buy_primary > 600):
					cut_first = lst_idx_buy_primary - 600

				dataset_pr_5M = {
								symbol: dataset[symbol].copy()
								}

				dataset_pr_5M[symbol]['low'] = dataset_pr_5M[symbol]['low'][cut_first:int(lst_idx_buy_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['high'] = dataset_pr_5M[symbol]['high'][cut_first:int(lst_idx_buy_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['close'] = dataset_pr_5M[symbol]['close'][cut_first:int(lst_idx_buy_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['open'] = dataset_pr_5M[symbol]['open'][cut_first:int(lst_idx_buy_primary)].reset_index(drop=True)


				res_pro_buy_primary = pd.DataFrame()
				try:
					res_pro_buy_primary = protect_resist(
														T_5M=True,
														T_15M=False,
														T_1H=True,
														T_4H=False,
														T_1D=False,
														dataset_5M=dataset_pr_5M[symbol],
														dataset_15M=dataset_1H[symbol],
														dataset_1H=dataset_1H[symbol],
														dataset_4H=dataset_1H[symbol],
														dataset_1D=dataset_1H[symbol],
														plot=False,
														alpha = ga_result_buy_primary['alpha'][0]
														)
				except Exception as ex:
					#print('ERROR PR Last Signal: ',ex)
					res_pro_buy_primary['high'] = [dataset[symbol]['high'][int(lst_idx_buy_primary)] * (1+(ga_result_buy_primary['min_tp'][0]/100)),0,0]#res_pro_buy_primary['high'] = 'nan'
					res_pro_buy_primary['low'] = [0,0,dataset[symbol]['low'][int(lst_idx_buy_primary)] * (1-(ga_result_buy_primary['min_st'][0]/100))]


				if (res_pro_buy_primary.empty == False):
					diff_pr_top_buy_primary = (((res_pro_buy_primary['high'][0]) - dataset[symbol]['high'][int(lst_idx_buy_primary)])/dataset[symbol]['high'][int(lst_idx_buy_primary)]) * 100
					diff_pr_down_buy_primary = ((dataset[symbol]['low'][int(lst_idx_buy_primary)] - (res_pro_buy_primary['low'][2]))/dataset[symbol]['low'][int(lst_idx_buy_primary)]) * 100

					if diff_pr_down_buy_primary < ga_result_buy_primary['min_st'][0]:
						diff_pr_down_buy_primary = ga_result_buy_primary['min_st'][0]
						res_pro_buy_primary['low'][2] = dataset[symbol]['low'][int(lst_idx_buy_primary)] * (1-(ga_result_buy_primary['min_st'][0]/100))


					if diff_pr_down_buy_primary > ga_result_buy_primary['max_st'][0]:
						diff_pr_down_buy_primary = ga_result_buy_primary['max_st'][0]
						res_pro_buy_primary['low'][2] = dataset[symbol]['low'][int(lst_idx_buy_primary)] * (1-(ga_result_buy_primary['max_st'][0]/100))

					if diff_pr_top_buy_primary < ga_result_buy_primary['min_tp'][0]:
						diff_pr_top_buy_primary = ga_result_buy_primary['min_tp'][0]
						res_pro_buy_primary['high'][0] = dataset[symbol]['high'][int(lst_idx_buy_primary)] * (1+(ga_result_buy_primary['min_tp'][0]/100))
					
					if diff_pr_top_buy_primary > ga_result_buy_primary['max_tp'][0]:
						diff_pr_top_buy_primary = ga_result_buy_primary['max_tp'][0]
						res_pro_buy_primary['high'][0] = dataset[symbol]['high'][int(lst_idx_buy_primary)] * (1+(ga_result_buy_primary['max_tp'][0]/100))
					#trend_long_buy = res_pro['trend_long'][0].values[0]
					#trend_mid_buy = res_pro['trend_mid'][0].values[0]
					#trend_short_1_buy = res_pro['trend_short1'][0].values[0]
					#trend_short_2_buy = res_pro['trend_short2'][0].values[0]

					#if trend_long_buy is np.nan: trend_long_buy = 'parcham'
					#if trend_mid_buy is np.nan: trend_mid_buy = 'parcham'
					#if trend_short_1_buy is np.nan: trend_short_1_buy = 'parcham'
					#if trend_short_2_buy is np.nan: trend_short_2_buy = 'parcham'

					resist_buy = (res_pro_buy_primary['high'][0])
					protect_buy = (res_pro_buy_primary['low'][2])

					signal = 'buy_primary'

				else:
					diff_pr_top_buy = 0
					diff_pr_down_buy = 0
					diff_pr_top_buy_power = 0
					diff_pr_down_buy_power = 0

					resist_buy = 0
					protect_buy = 0

					signal = 'no_trade'			

		print('================================')\

	#lst_idx_sell_primary = 5999

	
	elif (
		lst_idx_sell_primary > lst_idx_buy_primary and
		lst_idx_sell_primary > lst_idx_sell_secondry and
		lst_idx_sell_primary > lst_idx_buy_secondry and
		(len(dataset[symbol]['close']) - 1 - lst_idx_sell_primary) <= 1#ga_result_sell_primary['num_extreme'][0]
		):

		print('======> last signal buy ',symbol)
		print('dataset length: ',len(dataset[symbol]['close']))
		print('ga result buy methode: ',ga_result_sell_primary['methode'][0])
		print('last index: ',lst_idx_sell_primary)
		

		if ga_result_sell_primary['methode'][0] == 'pr':

			if lst_idx_sell_primary != 0:

				dataset_pr_5M = pd.DataFrame()

				cut_first = 0
				if (int(lst_idx_sell_primary) > 600):
					cut_first = int(lst_idx_sell_primary) - 600

				dataset_pr_5M = {
								symbol: dataset[symbol].copy()
								}

				dataset_pr_5M[symbol]['low'] = dataset_pr_5M[symbol]['low'][cut_first:int(lst_idx_sell_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['high'] = dataset_pr_5M[symbol]['high'][cut_first:int(lst_idx_sell_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['close'] = dataset_pr_5M[symbol]['close'][cut_first:int(lst_idx_sell_primary)].reset_index(drop=True)
				dataset_pr_5M[symbol]['open'] = dataset_pr_5M[symbol]['open'][cut_first:int(lst_idx_sell_primary)].reset_index(drop=True)


				res_pro_sell_primary = pd.DataFrame()
				try:
					res_pro_sell_primary = protect_resist(
														T_5M=True,
														T_15M=False,
														T_1H=True,
														T_4H=False,
														T_1D=False,
														dataset_5M=dataset_pr_5M[symbol],
														dataset_15M=dataset_1H[symbol],
														dataset_1H=dataset_1H[symbol],
														dataset_4H=dataset_1H[symbol],
														dataset_1D=dataset_1H[symbol],
														plot=False,
														alpha = ga_result_sell_primary['alpha'][0]
														)
				except Exception as ex:
					#print('ERROR PR Last Signal: ',ex)
					res_pro_sell_primary['high'] = [dataset[symbol]['high'][int(lst_idx_sell_primary)] * (1+(ga_result_sell_primary['min_st'][0]/100)),0,0]#res_pro_sell_primary['high'] = 'nan'
					res_pro_sell_primary['low'] = [0,0,dataset[symbol]['low'][int(lst_idx_sell_primary)] * (1-(ga_result_sell_primary['min_tp'][0]/100))]#res_pro_sell_primary['low'] = 'nan'


				if (res_pro_sell_primary.empty == False):
					diff_pr_top_sell_primary = (((res_pro_sell_primary['high'][0]) - dataset[symbol]['high'][int(lst_idx_sell_primary)])/dataset[symbol]['high'][int(lst_idx_sell_primary)]) * 100
					diff_pr_down_sell_primary = ((dataset[symbol]['low'][int(lst_idx_sell_primary)] - (res_pro_sell_primary['low'][2]))/dataset[symbol]['low'][int(lst_idx_sell_primary)]) * 100

					if diff_pr_top_sell_primary < ga_result_sell_primary['min_st'][0]:
						diff_pr_top_sell_primary = ga_result_sell_primary['min_st'][0]
						res_pro_sell_primary['high'][0] = dataset[symbol]['high'][int(lst_idx_sell_primary)] * (1+(ga_result_sell_primary['min_st'][0]/100))


					if diff_pr_top_sell_primary > ga_result_sell_primary['max_st'][0]:
						diff_pr_top_sell_primary = ga_result_sell_primary['max_st'][0]
						res_pro_sell_primary['high'][0] = dataset[symbol]['high'][int(lst_idx_sell_primary)] * (1+(ga_result_sell_primary['max_st'][0]/100))

					if diff_pr_down_sell_primary < ga_result_sell_primary['min_tp'][0]:
						diff_pr_down_sell_primary = ga_result_sell_primary['min_tp'][0]
						res_pro_sell_primary['low'][2] = dataset[symbol]['low'][int(lst_idx_sell_primary)] * (1-(ga_result_sell_primary['min_tp'][0]/100))
					
					if diff_pr_down_sell_primary > ga_result_sell_primary['max_tp'][0]:
						diff_pr_down_sell_primary = ga_result_sell_primary['max_tp'][0]
						res_pro_sell_primary['low'][2] = dataset[symbol]['high'][int(lst_idx_sell_primary)] * (1-(ga_result_sell_primary['max_tp'][0]/100))
					#trend_long_buy = res_pro['trend_long'][0].values[0]
					#trend_mid_buy = res_pro['trend_mid'][0].values[0]
					#trend_short_1_buy = res_pro['trend_short1'][0].values[0]
					#trend_short_2_buy = res_pro['trend_short2'][0].values[0]

					#if trend_long_buy is np.nan: trend_long_buy = 'parcham'
					#if trend_mid_buy is np.nan: trend_mid_buy = 'parcham'
					#if trend_short_1_buy is np.nan: trend_short_1_buy = 'parcham'
					#if trend_short_2_buy is np.nan: trend_short_2_buy = 'parcham'

					resist_sell = (res_pro_sell_primary['high'][0])
					protect_sell = (res_pro_sell_primary['low'][2])

					signal = 'sell_primary'

				else:
					diff_pr_top_sell_primary = 0
					diff_pr_down_sell_primary = 0

					resist_sell = 0
					protect_sell = 0

					signal = 'no_trade'			

		print('================================')

	elif (
			lst_idx_buy_secondry > lst_idx_buy_primary and
			lst_idx_buy_secondry > lst_idx_sell_primary and
			lst_idx_buy_secondry > lst_idx_sell_secondry and
			(len(dataset[symbol]['close']) - 1 - lst_idx_buy_secondry) <= 1
			):

		print('======> last signal sell ',symbol)
		print('dataset length: ',len(dataset[symbol]['close']))
		print('ga result sell: ',ga_result_sell['distance_lines'][0])
		print('ga result sell methode: ',ga_result_sell['methode'][0])
		print('last index: ',lst_idx_sell)
		

		if ga_result_sell['methode'][0] == 'pr':

			if ga_result_sell['methode'][0] == 'pr' and lst_idx_sell != 0:

				res_pro = pd.DataFrame()
				try:
					res_pro = protect_resist(
						T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,
						dataset_5M=dataset[symbol],
						dataset_15M=dataset_15M[symbol],
						dataset_1H=dataset_1H[symbol],
						dataset_4H=dataset_4H[symbol],
						dataset_1D=dataset_1D[symbol],
						plot=False
						)
				except:
					res_pro['high'] = 'nan'
					res_pro['low'] = 'nan'
					res_pro['power_high'] = 0
					res_pro['power_low'] = 0

				if (res_pro.empty == False):
					diff_pr_top_sell = (((res_pro['high'][0] * 1.0005) - dataset[symbol]['high'][lst_idx_sell])/dataset[symbol]['high'][lst_idx_sell]) * 100
					diff_pr_down_sell = ((dataset[symbol]['low'][lst_idx_sell] - (res_pro['low'][0] * 1.0005))/dataset[symbol]['low'][lst_idx_sell]) * 100


					resist_sell = (res_pro['high'][0] * 1.0005)
					protect_sell = (res_pro['low'][2] * 1.0005)
				else:
					diff_pr_top_sell = 0
					diff_pr_down_sell = 0
					diff_pr_top_sell_power = 0
					diff_pr_down_sell_power = 0

					trend_long_sell = 'no_flag'
					trend_mid_sell = 'no_flag'
					trend_short_1_sell = 'no_flag'
					trend_short_2_sell = 'no_flag'

					resist_sell = 0
					protect_sell = 0

			print('trend_long_sell: ',trend_long_sell)
			print('trend_mid_sell: ',trend_mid_sell)
			print('trend_short_1_sell: ',trend_short_1_sell)
			print('trend_short_2_sell: ',trend_short_2_sell)
			if (
				#sell_data['ramp_low'].iloc[-1]<=ga_result_sell['ramp_low_upper_pr'][0] and
				#sell_data['ramp_high'].iloc[-1]<=ga_result_sell['ramp_high_upper_pr'][0] and
				#diff_pr_top_sell<=ga_result_sell['diff_top_upper_pr'][0] and
				#diff_pr_down_sell <= ga_result_sell['diff_down_upper_pr'][0] and
				dataset[symbol]['high'].iloc[-1] < resist_sell and
				dataset[symbol]['low'].iloc[-1] > protect_sell and
				diff_pr_down_sell >= diff_pr_top_sell and
				diff_pr_top_sell <= 0.4 and
				((trend_long_sell != 'buy') and
				((trend_mid_sell != 'buy') and
				(trend_short_1_sell == 'sell') and
				(trend_short_2_sell == 'sell')))  
				#sell_data['diff_min_max_cci'].iloc[-1]<=ga_result_sell['diff_min_max_cci_upper_pr'][0] and
				#sell_data['diff_min_max_candle'].iloc[-1]<=ga_result_sell['diff_min_max_candle_upper_pr'][0]
				):

				signal = 'sell'

			else:
				signal = 'no_trade'

		print('================================')
	else:
		signal = 'no_trade'
		resist_sell = 0
		protect_sell = 0

	if (
		signal == 'buy_primary' or
		signal == 'buy_secondry'
		):
		return signal, resist_buy, protect_buy
	elif (
		signal == 'sell_primary' or
		signal == 'sell_secondry'
		):
		return signal, protect_sell, resist_sell
	else:
		return signal, 0, 0

#//////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************************** How To Use Funcs ************************************************************
"""
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,6000)
#symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,4000)
symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,510)

print(last_signal_macd_div(
						dataset=symbol_data_5M,
						dataset_1H=symbol_data_1H, 
						symbol='AUDCHF_i'
						))
"""
"""

symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																						sym='AUDCAD_i',
																						num_5M=20000,
																						num_15M=1,
																						num_1H=8250,
																						num_4H=1
																						)
print('get data')
time_first = time.time()
#signal_buy,signal_sell = golden_cross(dataset=symbol_data_5M,Apply_to='close',symbol='AUDCAD_i',
#	macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False)
#print('time Cross = ',time.time() - time_first)
#print(signal_buy)
#print(signal_sell)

#print('my index = ',symbol_data_5M['AUDCAD_i']['time'][11000].hour)
#print(symbol_data_15M['AUDCAD_i']['time'][0:-1])
#inndex_my = np.where((symbol_data_5M['AUDCAD_i']['time'][11000].hour == symbol_data_15M['AUDCAD_i']['time'].hour)&
	#(symbol_data_5M['AUDCAD_i']['time'][11000].minute >= symbol_data_15M['AUDCAD_i']['time'].minute)&
	#(symbol_data_5M['AUDCAD_i']['time'][11000].day == symbol_data_15M['AUDCAD_i']['time'].day)&
	#(symbol_data_5M['AUDCAD_i']['time'][11000].month == symbol_data_15M['AUDCAD_i']['time'].month)&
	#(symbol_data_5M['AUDCAD_i']['time'][11000].year == symbol_data_15M['AUDCAD_i']['time'].year))
#print(inndex_my)

time_first = time.time()
signal_buy_primary,signal_buy_secondry,signal_sell_primary,signal_sell_secondry = divergence_macd(
																							dataset=symbol_data_5M,
																							dataset_15M=symbol_data_15M,
																							dataset_1H=symbol_data_1H,
																							Apply_to='close',
																							symbol='AUDCAD_i',
																							macd_fast=12,
																							macd_slow=26,
																							macd_signal=9,
																							mode='optimize',
																							plot=False,
																							buy_doing=True,
																							sell_doing=False,
																							primary_doing=True,
																							secondry_doing=False,
																							name_stp_pr=True,
																							name_stp_minmax=False,
																							st_percent_minmax_buy = 0.56,
																							st_percent_minmax_sell = 0.9,
																							tp_percent_minmax_sell_max = 0.9,
																							tp_percent_minmax_buy_max = 0.38
																							)



out_buy,_ = tester_div_macd(
							signal_buy=signal_buy_primary,
							signal_sell=signal_buy_primary,
							min_tp=0,
							max_st=0,
							alpha=0.5,
							name_stp_minmax=False,
							name_stp_pr=True,
							flag_trade='buy'
							)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print('=======> out_buy = ',out_buy)

print('time Dive = ',time.time() - time_first)

print('*************** Profits Min Max:')


print('/////////////////////////////////////////////////////')

print('*************** Profits PR:')

signal_buy_primary,signal_buy_secondry,signal_sell_primary,signal_sell_secondry = divergence(dataset=symbol_data_5M,dataset_15M=symbol_data_15M,Apply_to='close',symbol='AUDCAD_i',
	macd_fast=2,macd_slow=4,macd_signal=20,mode='optimize',plot=False,
	buy_doing=True,sell_doing=False,primary_doing=True,secondry_doing=False,
	name_stp_pr=True,name_stp_minmax=True)
print('time Dive = ',time.time() - time_first)

ramp_macd_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='ramp_macd',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

ramp_candle_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='ramp_candle',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

diff_ramps_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_ramps',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

coef_ramps_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='coef_ramps',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

diff_min_max_macd_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_min_max_macd',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

diff_min_max_candle_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_min_max_candle',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

beta_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='beta',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

danger_line_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='danger_line',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

value_front_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='value_front',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

value_back_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='value_back',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

diff_top_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_pr_top',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

diff_down_intervals_pr = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_pr_down',
 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

print('ramp_macd_intervals_pr = ',ramp_macd_intervals_pr)
print('ramp_candle_intervals_pr = ',ramp_candle_intervals_pr)
print('diff_ramps_intervals_pr = ',diff_ramps_intervals_pr)
print('coef_ramps_intervals_pr = ',coef_ramps_intervals_pr)
print('diff_min_max_macd_intervals_pr = ',diff_min_max_macd_intervals_pr)
print('diff_min_max_candle_intervals_pr = ',diff_min_max_candle_intervals_pr)
print('beta_intervals_pr = ',beta_intervals_pr)
print('danger_line_intervals_pr = ',danger_line_intervals_pr)
print('value_back_intervals_pr = ',value_back_intervals_pr)
print('value_front_intervals_pr = ',value_front_intervals_pr)
print('diff_top_intervals_pr = ',diff_top_intervals_pr)
print('diff_down_intervals_pr = ',diff_down_intervals_pr)

upper = 0
mid = 1
lower = 2

list_index_ok = np.where(((signal_buy_primary['ramp_macd'].to_numpy()>=ramp_macd_intervals_pr['interval'][lower]))&
	((signal_buy_primary['ramp_candle'].to_numpy()<=ramp_candle_intervals_pr['interval'][upper]))&
	((signal_buy_primary['diff_ramps'].to_numpy()>=diff_ramps_intervals_pr['interval'][lower]))&
	((signal_buy_primary['coef_ramps'].to_numpy()>=coef_ramps_intervals_pr['interval'][lower]))&
	((signal_buy_primary['diff_pr_top'].to_numpy()<=diff_top_intervals_pr['interval'][upper]))&
	((signal_buy_primary['diff_pr_down'].to_numpy()<=diff_down_intervals_pr['interval'][upper]))&
	((signal_buy_primary['beta'].to_numpy()<=2*beta_intervals_pr['interval'][upper]))&
	((signal_buy_primary['diff_min_max_macd'].to_numpy()<=diff_min_max_macd_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax['interval'][upper]))&
	#((signal_buy_primary['danger_line'].to_numpy()<=danger_line_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['value_back'].to_numpy()<=value_back_intervals_pr['interval'][upper]))&
	((signal_buy_primary['value_front'].to_numpy()<=value_front_intervals_pr['interval'][upper]))
	)[0]



print('mean tp pr = ',np.mean(signal_buy_primary['tp_pr'][list_index_ok]))
print('mean st pr = ',np.mean(signal_buy_primary['st_pr'][list_index_ok]))

print('max tp pr = ',np.max(signal_buy_primary['tp_pr'][list_index_ok]))
print('max st pr = ',np.max(signal_buy_primary['st_pr'][list_index_ok]))

print('tp pr = ',np.bincount(signal_buy_primary['flag_pr'][list_index_ok] == 'tp'))
print('st pr = ',np.bincount(signal_buy_primary['flag_pr'][list_index_ok] == 'st'))


print('sum st pr = ',np.sum(signal_buy_primary['st_pr'][np.where(signal_buy_primary['flag_pr'][list_index_ok] == 'st')[0]].to_numpy()))
print('sum tp pr = ',np.sum(signal_buy_primary['tp_pr'][np.where(signal_buy_primary['flag_pr'][list_index_ok] == 'tp')[0]].to_numpy()))

print('mean tp min_max = ',np.mean(signal_buy_primary['tp_min_max'][list_index_ok]))
print('mean st min_max = ',np.mean(signal_buy_primary['st_min_max'][list_index_ok]))

print('max tp min_max = ',np.max(signal_buy_primary['tp_min_max'][list_index_ok]))
print('max st min_max = ',np.max(signal_buy_primary['st_min_max'][list_index_ok]))

print('tp min_max = ',np.bincount(signal_buy_primary['flag_min_max'][list_index_ok] == 'tp'))
print('st min_max = ',np.bincount(signal_buy_primary['flag_min_max'][list_index_ok] == 'st'))


print('sum st min_max = ',np.sum(signal_buy_primary['st_min_max'][np.where(signal_buy_primary['flag_min_max'][list_index_ok] == 'st')[0]].to_numpy()))
print('sum tp min_max = ',np.sum(signal_buy_primary['tp_min_max'][np.where(signal_buy_primary['flag_min_max'][list_index_ok] == 'tp')[0]].to_numpy()))

print('/////////////////////////////////////////////////////')

#Four Panda DataFrams: signal_buy_primary, signal_buy_secondry, signal_sell_primary, signal_sell_secondry
	#signal = buy_primary, buy_secondry, sell_primary, sell_secondry
	#value_front: the value of last index of Divergence
	#value_back: the value of before index of Divergence
	#index: the index of last index of Divergence
	#ramp_macd
	#ramp_candle
	#coef_ramps
	#diff_ramps
	#beta
	#danger_line
	#diff_min_max_macd
	#diff_min_max_candle
	#** Just in optimize mode:
	#tp_min_max_index
	#tp_min_max
	#st_min_max_index
	#st_min_max
	#flag_min_max: st or tp
	#tp_pr_index
	#tp_pr
	#st_pr_index
	#st_pr
	#flag_pr: st or tp
	#diff_pr_top
	#diff_pr_down
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

"""