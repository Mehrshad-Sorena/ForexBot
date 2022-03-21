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
from scipy.signal import argrelextrema
import time

from F_I_RESIST_PROTECT import Extreme_points, Extreme_points_ichimoko, extreme_points_ramp_lines, Best_Extreme_Finder, protect_resist

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

def divergence(dataset,dataset_15M,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False,buy_doing=False,sell_doing=False,primary_doing=False,secondry_doing=False,name_stp_pr=False,name_stp_minmax=True):

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
	column = macd_read.columns[0]
	macd['macd'] = pd.DataFrame(macd_read, columns=[column])
	macd = macd.dropna(inplace=False)

	n = 5
	
	min_ex = macd.iloc[argrelextrema(macd.macd.values, comparator = np.less,
                    order=n)[0]]['macd']
	max_ex = macd.iloc[argrelextrema(macd.macd.values, comparator = np.greater,
                    order=n)[0]]['macd']

	extreme_min = pd.DataFrame()
	extreme_min['value'] = min_ex.values
	extreme_min['index'] = min_ex.index
	extreme_min = extreme_min.dropna(inplace=False)
	extreme_min = extreme_min.sort_values(by = ['index'])

	extreme_max = pd.DataFrame()
	extreme_max['value'] = max_ex.values
	extreme_max['index'] = max_ex.index
	extreme_max = extreme_max.dropna(inplace=False)
	extreme_max = extreme_max.sort_values(by = ['index'])

	if(plot == True):
		fig, (ax1, ax0) = plt.subplots(nrows=2, figsize=(12, 6))
		ax0.plot(extreme_min['index'],extreme_min['value'], 'o',c='g')
		ax0.plot(extreme_max['index'],extreme_max['value'], 'o',c='r')
		ax0.plot(macd.index,macd.macd,c='b')
		ax1.plot(dataset[symbol]['close'].index,dataset[symbol]['close'],c='b')

	#//////////////////////////////////////////////////////////////////////

	#******************************* Optimize Mode **************************
	if ((mode == 'optimize') | (mode == 'online')):
		signal_buy_primary = pd.DataFrame(np.zeros(len(extreme_min)))
		signal_buy_primary['signal'] = np.nan
		signal_buy_primary['value_front'] = np.nan
		signal_buy_primary['value_back'] = np.nan
		signal_buy_primary['index'] = np.nan
		signal_buy_primary['ramp_macd'] = np.nan
		signal_buy_primary['ramp_candle'] = np.nan
		signal_buy_primary['coef_ramps'] = np.nan
		signal_buy_primary['diff_ramps'] = np.nan
		signal_buy_primary['beta'] = np.nan
		signal_buy_primary['danger_line'] = np.nan
		signal_buy_primary['diff_min_max_macd'] = np.nan
		signal_buy_primary['diff_min_max_candle'] = np.nan
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
		signal_sell_primary['ramp_macd'] = np.nan
		signal_sell_primary['ramp_candle'] = np.nan
		signal_sell_primary['coef_ramps'] = np.nan
		signal_sell_primary['diff_ramps'] = np.nan
		signal_sell_primary['beta'] = np.nan
		signal_sell_primary['danger_line'] = np.nan
		signal_sell_primary['diff_min_max_macd'] = np.nan
		signal_sell_primary['diff_min_max_candle'] = np.nan
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

		#***************************** Buy Find Section ***********************************************
		for elm in extreme_min.index:
			print(int((elm/extreme_min.index[-1])*100),'%')
			if (buy_doing == False): break
			if (primary_doing == False): break
			#+++++++++++++++++++++++++++++++++++++ Primary +++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Primary Buy ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_min['value'][elm] > extreme_min['value'][elm-1]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-1]])):
				signal_buy_primary['signal'][primary_counter] = 'buy_primary'
				signal_buy_primary['value_front'][primary_counter] = extreme_min['value'][elm]
				signal_buy_primary['value_back'][primary_counter] = extreme_min['value'][elm-1]
				signal_buy_primary['index'][primary_counter] = extreme_min['index'][elm]
				signal_buy_primary['ramp_macd'][primary_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-1])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy_primary['ramp_candle'][primary_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-1]])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy_primary['coef_ramps'][primary_counter] = signal_buy_primary['ramp_macd'][primary_counter]/abs(signal_buy_primary['ramp_candle'][primary_counter])
				signal_buy_primary['diff_ramps'][primary_counter] = abs(signal_buy_primary['ramp_candle'][primary_counter]) - signal_buy_primary['ramp_macd'][primary_counter]
				signal_buy_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_primary['danger_line'][primary_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_primary['beta'][primary_counter])/100)
				signal_buy_primary['diff_min_max_macd'][primary_counter] = ((np.max(macd.macd[extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) / np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) * 100
				signal_buy_primary['diff_min_max_candle'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0]) - 1) > 1):
							signal_buy_primary['tp_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0])
							signal_buy_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_min_max_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['tp_min_max_index'][primary_counter] = -1
							signal_buy_primary['tp_min_max'][primary_counter] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
							signal_buy_primary['st_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
							signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_min_max_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['st_min_max_index'][primary_counter] = -1
							signal_buy_primary['st_min_max'][primary_counter] = 0

						if (signal_buy_primary['st_min_max_index'][primary_counter] < signal_buy_primary['tp_min_max_index'][primary_counter]):
							signal_buy_primary['flag_min_max'][primary_counter] = 'st'
							if (signal_buy_primary['st_min_max_index'][primary_counter] != -1):
								signal_buy_primary['tp_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_buy_primary['tp_min_max_index'][primary_counter] != -1):
								signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

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
							signal_buy_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							signal_buy_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
								signal_buy_primary['tp_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
								signal_buy_primary['tp_pr'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['tp_pr_index'][primary_counter] = -1
								signal_buy_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
								signal_buy_primary['st_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
								signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['st_pr_index'][primary_counter] = -1
								signal_buy_primary['st_pr'][primary_counter] = 0

							if (signal_buy_primary['st_pr_index'][primary_counter] < signal_buy_primary['tp_pr_index'][primary_counter]):
								signal_buy_primary['flag_pr'][primary_counter] = 'st'
								if (signal_buy_primary['st_pr_index'][primary_counter] != -1):
									signal_buy_primary['tp_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_buy_primary['tp_pr_index'][primary_counter] != -1):
									signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
						else:
							signal_buy_primary['tp_pr_index'][primary_counter] = -1
							signal_buy_primary['tp_pr'][primary_counter] = 0
							signal_buy_primary['st_pr_index'][primary_counter] = -1
							signal_buy_primary['st_pr'][primary_counter] = 0
							signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[extreme_min['value'][elm-1],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-1]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 2
			if (elm - 2 < 0): continue
			if ((extreme_min['value'][elm] > extreme_min['value'][elm-2]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-2]])):
				signal_buy_primary['signal'][primary_counter] = 'buy_primary'
				signal_buy_primary['value_front'][primary_counter] = extreme_min['value'][elm]
				signal_buy_primary['value_back'][primary_counter] = extreme_min['value'][elm-2]
				signal_buy_primary['index'][primary_counter] = extreme_min['index'][elm]
				signal_buy_primary['ramp_macd'][primary_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-2])/(extreme_min['index'][elm] - extreme_min['index'][elm-2])
				signal_buy_primary['ramp_candle'][primary_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-2]])/(extreme_min['index'][elm] - extreme_min['index'][elm-2])
				signal_buy_primary['coef_ramps'][primary_counter] = signal_buy_primary['ramp_macd'][primary_counter]/abs(signal_buy_primary['ramp_candle'][primary_counter])
				signal_buy_primary['diff_ramps'][primary_counter] = abs(signal_buy_primary['ramp_candle'][primary_counter]) - signal_buy_primary['ramp_macd'][primary_counter]
				signal_buy_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_primary['danger_line'][primary_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_primary['beta'][primary_counter])/100)
				signal_buy_primary['diff_min_max_macd'][primary_counter] = ((np.max(macd.macd[extreme_min['index'][elm-2]:extreme_min['index'][elm]]) - np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) / np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) * 100
				signal_buy_primary['diff_min_max_candle'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-2]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-2]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-2]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0]) - 1) > 1):
							signal_buy_primary['tp_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0])
							signal_buy_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_min_max_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['tp_min_max_index'][primary_counter] = -1
							signal_buy_primary['tp_min_max'][primary_counter] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
							signal_buy_primary['st_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
							signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_min_max_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['st_min_max_index'][primary_counter] = -1
							signal_buy_primary['st_min_max'][primary_counter] = 0

						if (signal_buy_primary['st_min_max_index'][primary_counter] < signal_buy_primary['tp_min_max_index'][primary_counter]):
							signal_buy_primary['flag_min_max'][primary_counter] = 'st'
							if (signal_buy_primary['st_min_max_index'][primary_counter] != -1):
								signal_buy_primary['tp_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_buy_primary['tp_min_max_index'][primary_counter] != -1):
								signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

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
							signal_buy_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							signal_buy_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
								signal_buy_primary['tp_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
								signal_buy_primary['tp_pr'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['tp_pr_index'][primary_counter] = -1
								signal_buy_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
								signal_buy_primary['st_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
								signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['st_pr_index'][primary_counter] = -1
								signal_buy_primary['st_pr'][primary_counter] = 0

							if (signal_buy_primary['st_pr_index'][primary_counter] < signal_buy_primary['tp_pr_index'][primary_counter]):
								signal_buy_primary['flag_pr'][primary_counter] = 'st'
								if (signal_buy_primary['st_pr_index'][primary_counter] != -1):
									signal_buy_primary['tp_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_buy_primary['tp_pr_index'][primary_counter] != -1):
									signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
						else:
							signal_buy_primary['tp_pr_index'][primary_counter] = -1
							signal_buy_primary['tp_pr'][primary_counter] = 0
							signal_buy_primary['st_pr_index'][primary_counter] = -1
							signal_buy_primary['st_pr'][primary_counter] = 0
							signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-2],extreme_min['index'][elm]],[extreme_min['value'][elm-2],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-2],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-2]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue

			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 3
			if (elm - 3 < 0): continue
			if ((extreme_min['value'][elm] > extreme_min['value'][elm-3]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] < dataset[symbol]['low'][extreme_min['index'][elm-3]])):
				signal_buy_primary['signal'][primary_counter] = 'buy_primary'
				signal_buy_primary['value_front'][primary_counter] = extreme_min['value'][elm]
				signal_buy_primary['value_back'][primary_counter] = extreme_min['value'][elm-3]
				signal_buy_primary['index'][primary_counter] = extreme_min['index'][elm]
				signal_buy_primary['ramp_macd'][primary_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-3])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				signal_buy_primary['ramp_candle'][primary_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-3]])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				signal_buy_primary['coef_ramps'][primary_counter] = signal_buy_primary['ramp_macd'][primary_counter]/abs(signal_buy_primary['ramp_candle'][primary_counter])
				signal_buy_primary['diff_ramps'][primary_counter] = abs(signal_buy_primary['ramp_candle'][primary_counter]) - signal_buy_primary['ramp_macd'][primary_counter]
				signal_buy_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_primary['danger_line'][primary_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_primary['beta'][primary_counter])/100)
				signal_buy_primary['diff_min_max_macd'][primary_counter] = ((np.max(macd.macd[extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) / np.min([signal_buy_primary['value_back'][primary_counter],signal_buy_primary['value_front'][primary_counter]])) * 100
				signal_buy_primary['diff_min_max_candle'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:

						if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0]) - 1) > 1):
							signal_buy_primary['tp_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy_primary['diff_min_max_candle'][primary_counter])))[0])
							signal_buy_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_min_max_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['tp_min_max_index'][primary_counter] = -1
							signal_buy_primary['tp_min_max'][primary_counter] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
							signal_buy_primary['st_min_max_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
							signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_min_max_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['st_min_max_index'][primary_counter] = -1
							signal_buy_primary['st_min_max'][primary_counter] = 0

						if (signal_buy_primary['st_min_max_index'][primary_counter] < signal_buy_primary['tp_min_max_index'][primary_counter]):
							signal_buy_primary['flag_min_max'][primary_counter] = 'st'
							if (signal_buy_primary['st_min_max_index'][primary_counter] != -1):
								signal_buy_primary['tp_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_buy_primary['tp_min_max_index'][primary_counter] != -1):
								signal_buy_primary['st_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

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
							signal_buy_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							signal_buy_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
								signal_buy_primary['tp_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
								signal_buy_primary['tp_pr'][primary_counter] = ((dataset[symbol]['high'][signal_buy_primary['tp_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['tp_pr_index'][primary_counter] = -1
								signal_buy_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
								signal_buy_primary['st_pr_index'][primary_counter] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
								signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy_primary['st_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['st_pr_index'][primary_counter] = -1
								signal_buy_primary['st_pr'][primary_counter] = 0

							if (signal_buy_primary['st_pr_index'][primary_counter] < signal_buy_primary['tp_pr_index'][primary_counter]):
								signal_buy_primary['flag_pr'][primary_counter] = 'st'
								if (signal_buy_primary['st_pr_index'][primary_counter] != -1):
									signal_buy_primary['tp_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy_primary['st_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
							else:
								signal_buy_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_buy_primary['tp_pr_index'][primary_counter] != -1):
									signal_buy_primary['st_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy_primary['tp_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
						else:
							signal_buy_primary['tp_pr_index'][primary_counter] = -1
							signal_buy_primary['tp_pr'][primary_counter] = 0
							signal_buy_primary['st_pr_index'][primary_counter] = -1
							signal_buy_primary['st_pr'][primary_counter] = 0
							signal_buy_primary['flag_pr'][primary_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-3],extreme_min['index'][elm]],[extreme_min['value'][elm-3],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-3],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-3]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 4
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 5
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Buy ********************************* = 6
					
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
			if (elm - 2 < 0): continue
			if ((extreme_min['value'][elm] < extreme_min['value'][elm-2]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] > dataset[symbol]['low'][extreme_min['index'][elm-2]])):
				signal_buy_secondry['signal'][secondry_counter] = 'buy_secondry'
				signal_buy_secondry['value_front'][secondry_counter] = extreme_min['value'][elm]
				signal_buy_secondry['value_back'][secondry_counter] = extreme_min['value'][elm-2]
				signal_buy_secondry['index'][secondry_counter] = extreme_min['index'][elm]
				signal_buy_secondry['ramp_macd'][secondry_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-2])/(extreme_min['index'][elm] - extreme_min['index'][elm-2])
				signal_buy_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-2]])/(extreme_min['index'][elm] - extreme_min['index'][elm-2])
				signal_buy_secondry['coef_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter]/signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['diff_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter] - signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_secondry['danger_line'][secondry_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_secondry['beta'][secondry_counter])/100)
				signal_buy_secondry['diff_min_max_macd'][secondry_counter] = ((np.max(macd.macd[extreme_min['index'][elm-2]:extreme_min['index'][elm]]) - np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) / np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) * 100
				signal_buy_secondry['diff_min_max_candle'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-2]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-2]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-2]]])) * 100

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
					ax0.plot([extreme_min['index'][elm-2],extreme_min['index'][elm]],[extreme_min['value'][elm-2],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-2],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-2]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1
				continue
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Buy ********************************* = 3
			if (elm - 3 < 0): continue
			if ((extreme_min['value'][elm] < extreme_min['value'][elm-3]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] > dataset[symbol]['low'][extreme_min['index'][elm-3]])):
				signal_buy_secondry['signal'][secondry_counter] = 'buy_secondry'
				signal_buy_secondry['value_front'][secondry_counter] = extreme_min['value'][elm]
				signal_buy_secondry['value_back'][secondry_counter] = extreme_min['value'][elm-3]
				signal_buy_secondry['index'][secondry_counter] = extreme_min['index'][elm]
				signal_buy_secondry['ramp_macd'][secondry_counter] = (extreme_min['value'][elm] - extreme_min['value'][elm-3])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				signal_buy_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-3]])/(extreme_min['index'][elm] - extreme_min['index'][elm-3])
				signal_buy_secondry['coef_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter]/signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['diff_ramps'][secondry_counter] = signal_buy_secondry['ramp_macd'][secondry_counter] - signal_buy_secondry['ramp_candle'][secondry_counter]
				signal_buy_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy_secondry['danger_line'][secondry_counter] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy_secondry['beta'][secondry_counter])/100)
				signal_buy_secondry['diff_min_max_macd'][secondry_counter] = ((np.max(macd.macd[extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) / np.min([signal_buy_secondry['value_back'][secondry_counter],signal_buy_secondry['value_front'][secondry_counter]])) * 100
				signal_buy_secondry['diff_min_max_candle'][secondry_counter] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-3]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-3]]])) * 100

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
					ax0.plot([extreme_min['index'][elm-3],extreme_min['index'][elm]],[extreme_min['value'][elm-3],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-3],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-3]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1
				continue
					
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
			if (elm - 1 < 0): continue
			if ((extreme_max['value'][elm] < extreme_max['value'][elm-1]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-1]])):
				signal_sell_primary['signal'][primary_counter] = 'sell_primary'
				signal_sell_primary['value_front'][primary_counter] = extreme_max['value'][elm]
				signal_sell_primary['value_back'][primary_counter] = extreme_max['value'][elm-1]
				signal_sell_primary['index'][primary_counter] = extreme_max['index'][elm]
				signal_sell_primary['ramp_macd'][primary_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-1])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell_primary['ramp_candle'][primary_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-1]])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell_primary['coef_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter]/signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['diff_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter] - signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_primary['danger_line'][primary_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_primary['beta'][primary_counter])/100)
				signal_sell_primary['diff_min_max_macd'][primary_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) / np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) * 100
				signal_sell_primary['diff_min_max_candle'][primary_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) * 100

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
							if (signal_sell_primary['st_min_max_index'][primary_counter] != -1):
								signal_sell_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_sell_primary['tp_min_max_index'][primary_counter] != -1):
								signal_sell_primary['st_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

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
							signal_sell_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							signal_sell_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
								signal_sell_primary['tp_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
								signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_primary['tp_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['tp_pr_index'][primary_counter] = -1
								signal_sell_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
								signal_sell_primary['st_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
								signal_sell_primary['st_pr'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['st_pr_index'][primary_counter] = -1
								signal_sell_primary['st_pr'][primary_counter] = 0

							if (signal_sell_primary['st_pr_index'][primary_counter] < signal_sell_primary['tp_pr_index'][primary_counter]):
								signal_sell_primary['flag_pr'][primary_counter] = 'st'
								if (signal_sell_primary['st_pr_index'][primary_counter] != -1):
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_sell_primary['tp_pr_index'][primary_counter] != -1):
									signal_sell_primary['st_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
						else:
							signal_sell_primary['tp_pr_index'][primary_counter] = -1
							signal_sell_primary['tp_pr'][primary_counter] = 0
							signal_sell_primary['st_pr_index'][primary_counter] = -1
							signal_sell_primary['st_pr'][primary_counter] = 0
							signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[extreme_max['value'][elm-1],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-1]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue		
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 2
			if (elm - 2 < 0): continue
			if ((extreme_max['value'][elm] < extreme_max['value'][elm-2]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-2]])):
				signal_sell_primary['signal'][primary_counter] = 'sell_primary'
				signal_sell_primary['value_front'][primary_counter] = extreme_max['value'][elm]
				signal_sell_primary['value_back'][primary_counter] = extreme_max['value'][elm-2]
				signal_sell_primary['index'][primary_counter] = extreme_max['index'][elm]
				signal_sell_primary['ramp_macd'][primary_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-2])/(extreme_max['index'][elm] - extreme_max['index'][elm-2])
				signal_sell_primary['ramp_candle'][primary_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-2]])/(extreme_max['index'][elm] - extreme_max['index'][elm-2])
				signal_sell_primary['coef_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter]/signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['diff_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter] - signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_primary['danger_line'][primary_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_primary['beta'][primary_counter])/100)
				signal_sell_primary['diff_min_max_macd'][primary_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-2]:extreme_max['index'][elm]]) - np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) / np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) * 100
				signal_sell_primary['diff_min_max_candle'][primary_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-2]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-2]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-2]]])) * 100

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
							if (signal_sell_primary['st_min_max_index'][primary_counter] != -1):
								signal_sell_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_sell_primary['tp_min_max_index'][primary_counter] != -1):
								signal_sell_primary['st_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

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
							signal_sell_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							signal_sell_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
								signal_sell_primary['tp_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
								signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_primary['tp_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['tp_pr_index'][primary_counter] = -1
								signal_sell_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
								signal_sell_primary['st_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
								signal_sell_primary['st_pr'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['st_pr_index'][primary_counter] = -1
								signal_sell_primary['st_pr'][primary_counter] = 0

							if (signal_sell_primary['st_pr_index'][primary_counter] < signal_sell_primary['tp_pr_index'][primary_counter]):
								signal_sell_primary['flag_pr'][primary_counter] = 'st'
								if (signal_sell_primary['st_pr_index'][primary_counter] != -1):
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_sell_primary['tp_pr_index'][primary_counter] != -1):
									signal_sell_primary['st_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
						else:
							signal_sell_primary['tp_pr_index'][primary_counter] = -1
							signal_sell_primary['tp_pr'][primary_counter] = 0
							signal_sell_primary['st_pr_index'][primary_counter] = -1
							signal_sell_primary['st_pr'][primary_counter] = 0
							signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-2],extreme_max['index'][elm]],[extreme_max['value'][elm-2],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-2],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-2]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue
					
			#///////////////////////////////////////////////////////

			#****************************** Primary Sell ********************************* = 3
			if (elm - 3 < 0): continue
			if ((extreme_max['value'][elm] < extreme_max['value'][elm-3]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] > dataset[symbol]['high'][extreme_max['index'][elm-3]])):
				signal_sell_primary['signal'][primary_counter] = 'sell_primary'
				signal_sell_primary['value_front'][primary_counter] = extreme_max['value'][elm]
				signal_sell_primary['value_back'][primary_counter] = extreme_max['value'][elm-3]
				signal_sell_primary['index'][primary_counter] = extreme_max['index'][elm]
				signal_sell_primary['ramp_macd'][primary_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-3])/(extreme_max['index'][elm] - extreme_max['index'][elm-3])
				signal_sell_primary['ramp_candle'][primary_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-3]])/(extreme_max['index'][elm] - extreme_max['index'][elm-3])
				signal_sell_primary['coef_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter]/signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['diff_ramps'][primary_counter] = signal_sell_primary['ramp_macd'][primary_counter] - signal_sell_primary['ramp_candle'][primary_counter]
				signal_sell_primary['beta'][primary_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_primary['danger_line'][primary_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_primary['beta'][primary_counter])/100)
				signal_sell_primary['diff_min_max_macd'][primary_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-3]:extreme_max['index'][elm]]) - np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) / np.max([signal_sell_primary['value_back'][primary_counter],signal_sell_primary['value_front'][primary_counter]])) * 100
				signal_sell_primary['diff_min_max_candle'][primary_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-3]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-3]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-3]]])) * 100

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
							if (signal_sell_primary['st_min_max_index'][primary_counter] != -1):
								signal_sell_primary['tp_min_max'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_min_max_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell_primary['flag_min_max'][primary_counter] = 'tp'
							if (signal_sell_primary['tp_min_max_index'][primary_counter] != -1):
								signal_sell_primary['st_min_max'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_min_max_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

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
							signal_sell_primary['diff_pr_top'][primary_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							signal_sell_primary['diff_pr_down'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

							if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
								signal_sell_primary['tp_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
								signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell_primary['tp_pr_index'][primary_counter]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['tp_pr_index'][primary_counter] = -1
								signal_sell_primary['tp_pr'][primary_counter] = 0

							if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
								signal_sell_primary['st_pr_index'][primary_counter] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
								signal_sell_primary['st_pr'][primary_counter] = ((dataset[symbol]['high'][signal_sell_primary['st_pr_index'][primary_counter]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['st_pr_index'][primary_counter] = -1
								signal_sell_primary['st_pr'][primary_counter] = 0

							if (signal_sell_primary['st_pr_index'][primary_counter] < signal_sell_primary['tp_pr_index'][primary_counter]):
								signal_sell_primary['flag_pr'][primary_counter] = 'st'
								if (signal_sell_primary['st_pr_index'][primary_counter] != -1):
									signal_sell_primary['tp_pr'][primary_counter] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell_primary['st_pr_index'][primary_counter])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
							else:
								signal_sell_primary['flag_pr'][primary_counter] = 'tp'
								if (signal_sell_primary['tp_pr_index'][primary_counter] != -1):
									signal_sell_primary['st_pr'][primary_counter] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell_primary['tp_pr_index'][primary_counter])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
						else:
							signal_sell_primary['tp_pr_index'][primary_counter] = -1
							signal_sell_primary['tp_pr'][primary_counter] = 0
							signal_sell_primary['st_pr_index'][primary_counter] = -1
							signal_sell_primary['st_pr'][primary_counter] = 0
							signal_sell_primary['flag_pr'][primary_counter] = 'no_flag'
						#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-3],extreme_max['index'][elm]],[extreme_max['value'][elm-3],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-3],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-3]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				primary_counter += 1
				continue
					
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
			if (elm - 2 < 0): continue
			if ((extreme_max['value'][elm] > extreme_max['value'][elm-2]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] < dataset[symbol]['high'][extreme_max['index'][elm-2]])):
				signal_sell_secondry['signal'][secondry_counter] = 'sell_secondry'
				signal_sell_secondry['value_front'][secondry_counter] = extreme_max['value'][elm]
				signal_sell_secondry['value_back'][secondry_counter] = extreme_max['value'][elm-2]
				signal_sell_secondry['index'][secondry_counter] = extreme_max['index'][elm]
				signal_sell_secondry['ramp_macd'][secondry_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-2])/(extreme_max['index'][elm] - extreme_max['index'][elm-2])
				signal_sell_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-2]])/(extreme_max['index'][elm] - extreme_max['index'][elm-2])
				signal_sell_secondry['coef_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter]/signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['diff_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter] - signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_secondry['danger_line'][secondry_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_secondry['beta'][secondry_counter])/100)
				signal_sell_secondry['diff_min_max_macd'][secondry_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-2]:extreme_max['index'][elm]]) - np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) / np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) * 100
				signal_sell_secondry['diff_min_max_candle'][secondry_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-2]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-2]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-2]]])) * 100

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
					ax0.plot([extreme_max['index'][elm-2],extreme_max['index'][elm]],[extreme_max['value'][elm-2],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-2],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-2]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1
				continue
					
			#///////////////////////////////////////////////////////

			#****************************** Secondry Sell ********************************* = 3
			if (elm - 3 < 0): continue
			if ((extreme_max['value'][elm] > extreme_max['value'][elm-3]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] < dataset[symbol]['high'][extreme_max['index'][elm-3]])):
				signal_sell_secondry['signal'][secondry_counter] = 'sell_secondry'
				signal_sell_secondry['value_front'][secondry_counter] = extreme_max['value'][elm]
				signal_sell_secondry['value_back'][secondry_counter] = extreme_max['value'][elm-3]
				signal_sell_secondry['index'][secondry_counter] = extreme_max['index'][elm]
				signal_sell_secondry['ramp_macd'][secondry_counter] = (extreme_max['value'][elm] - extreme_max['value'][elm-3])/(extreme_max['index'][elm] - extreme_max['index'][elm-3])
				signal_sell_secondry['ramp_candle'][secondry_counter] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-3]])/(extreme_max['index'][elm] - extreme_max['index'][elm-3])
				signal_sell_secondry['coef_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter]/signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['diff_ramps'][secondry_counter] = signal_sell_secondry['ramp_macd'][secondry_counter] - signal_sell_secondry['ramp_candle'][secondry_counter]
				signal_sell_secondry['beta'][secondry_counter] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell_secondry['danger_line'][secondry_counter] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell_secondry['beta'][secondry_counter])/100)
				signal_sell_secondry['diff_min_max_macd'][secondry_counter] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-3]:extreme_max['index'][elm]]) - np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) / np.max([signal_sell_secondry['value_back'][secondry_counter],signal_sell_secondry['value_front'][secondry_counter]])) * 100
				signal_sell_secondry['diff_min_max_candle'][secondry_counter] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-3]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-3]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-3]]])) * 100

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
					ax0.plot([extreme_max['index'][elm-3],extreme_max['index'][elm]],[extreme_max['value'][elm-3],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-3],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-3]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				secondry_counter += 1
				continue
					
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
	signal_buy_primary = signal_buy_primary.drop(columns=0)
	signal_buy_primary = signal_buy_primary.dropna()
	signal_buy_primary = signal_buy_primary.sort_values(by = ['index'])
	signal_buy_primary = signal_buy_primary.reset_index(drop=True)

	signal_buy_secondry = signal_buy_secondry.drop(columns=0)
	signal_buy_secondry = signal_buy_secondry.dropna()
	signal_buy_secondry = signal_buy_secondry.sort_values(by = ['index'])
	signal_buy_secondry = signal_buy_secondry.reset_index(drop=True)

	signal_sell_primary = signal_sell_primary.drop(columns=0)
	signal_sell_primary = signal_sell_primary.dropna()
	signal_sell_primary = signal_sell_primary.sort_values(by = ['index'])
	signal_sell_primary = signal_sell_primary.reset_index(drop=True)

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
		signal_good = signals.drop(np.where((signals[name_stp]=='st')|
			(signals['st_min_max']>max_st)|
			(signals['tp_min_max']<min_tp))[0])

	if (name_stp == 'flag_pr'):
		signal_good = signals.drop(np.where((signals[name_stp]=='st')|
			(signals['st_pr']>max_st)|
			(signals['tp_pr']<min_tp))[0])
			#(signals['diff_pr_down']>max_st)

	signal_good = signal_good.sort_values(by = ['index'])
	signal_good = signal_good.reset_index(drop=True)

	#timeout = time.time() + 20  # timeout_break Sec from now
	while True:

		if (len(signal_good[apply_to].to_numpy()) - 1) >= 10:
			n_clusters = 5
		else:
			n_clusters = len(signal_good[apply_to].to_numpy()) - 1

		kmeans = KMeans(n_clusters=n_clusters, random_state=0,init='k-means++',n_init=5,max_iter=5)
		#Model Fitting
		kmeans = kmeans.fit(signal_good[apply_to].to_numpy().reshape(-1,1))

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		if ((len(Y) != len(Power))):
			timeout = time.time() + timeout_break
			continue
		if ((len(Y) == len(Power))): break

	signal_final = pd.DataFrame(Y, columns=['Y'])
	signal_final['power'] = Power
	signal_final = signal_final.sort_values(by = ['Y'])

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
		
		f = Fitter(data = data_X, xmin=np.min(data_X), xmax=np.max(data_X), bins = len(signal_final['Y']), distributions = distributions, timeout=30, density=True)

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

#*********************************** How To Use Funcs ************************************************************

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,99000)
symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,33000)
#symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,1000)
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
signal_buy_primary,signal_buy_secondry,signal_sell_primary,signal_sell_secondry = divergence(dataset=symbol_data_5M,dataset_15M=symbol_data_15M,Apply_to='close',symbol='AUDCAD_i',
	macd_fast=2,macd_slow=4,macd_signal=20,mode='optimize',plot=False,
	buy_doing=True,sell_doing=False,primary_doing=True,secondry_doing=False,
	name_stp_pr=False,name_stp_minmax=True)
print('time Dive = ',time.time() - time_first)

print('*************** Profits Min Max:')

ramp_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='ramp_macd',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

ramp_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='ramp_candle',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

diff_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_ramps',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

coef_ramps_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='coef_ramps',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

diff_min_max_macd_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_min_max_macd',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

diff_min_max_candle_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='diff_min_max_candle',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

beta_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='beta',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

danger_line_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='danger_line',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

value_front_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='value_front',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

value_back_intervals_minmax = Find_Best_intervals(signals=signal_buy_primary,apply_to='value_back',
 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

print('ramp_macd_intervals_minmax = ',ramp_macd_intervals_minmax)
print('ramp_candle_intervals_minmax = ',ramp_candle_intervals_minmax)
print('diff_ramps_intervals_minmax = ',diff_ramps_intervals_minmax)
print('coef_ramps_intervals_minmax = ',coef_ramps_intervals_minmax)
print('diff_min_max_macd_intervals_minmax = ',diff_min_max_macd_intervals_minmax)
print('diff_min_max_candle_intervals_minmax = ',diff_min_max_candle_intervals_minmax)
print('beta_intervals_minmax = ',beta_intervals_minmax)
print('danger_line_intervals_minmax = ',danger_line_intervals_minmax)
print('value_back_intervals_minmax = ',value_back_intervals_minmax)
print('value_front_intervals_minmax = ',value_front_intervals_minmax)

upper = 0
mid = 1
lower = 2

list_index_ok = np.where(((signal_buy_primary['ramp_macd'].to_numpy()>=ramp_macd_intervals_minmax['interval'][lower]))&
	((signal_buy_primary['ramp_candle'].to_numpy()<=ramp_candle_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['diff_ramps'].to_numpy()>=diff_ramps_intervals_minmax['interval'][lower]))&
	((signal_buy_primary['coef_ramps'].to_numpy()>=coef_ramps_intervals_minmax['interval'][lower]))&
	((signal_buy_primary['diff_min_max_macd'].to_numpy()<=diff_min_max_macd_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['beta'].to_numpy()<=2*beta_intervals_minmax['interval'][upper]))&
	#((signal_buy_primary['danger_line'].to_numpy()<=danger_line_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['value_back'].to_numpy()<=value_back_intervals_minmax['interval'][upper]))&
	((signal_buy_primary['value_front'].to_numpy()<=value_front_intervals_minmax['interval'][upper]))
	)[0]



print('mean tp min_max = ',np.mean(signal_buy_primary['tp_min_max'][list_index_ok]))
print('mean st min_max = ',np.mean(signal_buy_primary['st_min_max'][list_index_ok]))

print('max tp min_max = ',np.max(signal_buy_primary['tp_min_max'][list_index_ok]))
print('max st min_max = ',np.max(signal_buy_primary['st_min_max'][list_index_ok]))

print('tp min_max = ',np.bincount(signal_buy_primary['flag_min_max'][list_index_ok] == 'tp'))
print('st min_max = ',np.bincount(signal_buy_primary['flag_min_max'][list_index_ok] == 'st'))


print('sum st min_max = ',np.sum(signal_buy_primary['st_min_max'][np.where(signal_buy_primary['flag_min_max'][list_index_ok] == 'st')[0]].to_numpy()))
print('sum tp min_max = ',np.sum(signal_buy_primary['tp_min_max'][np.where(signal_buy_primary['flag_min_max'][list_index_ok] == 'tp')[0]].to_numpy()))

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