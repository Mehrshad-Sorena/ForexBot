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

def divergence(dataset,dataset_15M,dataset_1H,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False):


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
		signal_buy = pd.DataFrame(np.zeros(len(extreme_min)))
		signal_buy['signal'] = np.nan
		signal_buy['value_front'] = np.nan
		signal_buy['value_back'] = np.nan
		signal_buy['index'] = np.nan
		signal_buy['ramp_macd'] = np.nan
		signal_buy['ramp_candle'] = np.nan
		signal_buy['coef_ramps'] = np.nan
		signal_buy['diff_ramps'] = np.nan
		signal_buy['beta'] = np.nan
		signal_buy['danger_line'] = np.nan
		signal_buy['diff_min_max_macd'] = np.nan
		signal_buy['diff_min_max_candle'] = np.nan
		if (mode == 'optimize'):
			signal_buy['tp_min_max_index'] = np.nan
			signal_buy['tp_min_max'] = np.nan
			signal_buy['st_min_max_index'] = np.nan
			signal_buy['st_min_max'] = np.nan
			signal_buy['flag_min_max'] = np.nan

			signal_buy['tp_pr_index'] = np.nan
			signal_buy['tp_pr'] = np.nan
			signal_buy['st_pr_index'] = np.nan
			signal_buy['st_pr'] = np.nan
			signal_buy['flag_pr'] = np.nan
			signal_buy['diff_pr_top'] = np.nan
			signal_buy['diff_pr_down'] = np.nan


		signal_sell = pd.DataFrame(np.zeros(len(extreme_max)))
		signal_sell['signal'] = np.nan
		signal_sell['value_front'] = np.nan
		signal_sell['value_back'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['ramp_macd'] = np.nan
		signal_sell['ramp_candle'] = np.nan
		signal_sell['coef_ramps'] = np.nan
		signal_sell['diff_ramps'] = np.nan
		signal_sell['beta'] = np.nan
		signal_sell['danger_line'] = np.nan
		signal_sell['diff_min_max_macd'] = np.nan
		signal_sell['diff_min_max_candle'] = np.nan
		if (mode == 'optimize'):
			signal_sell['tp_min_max_index'] = np.nan
			signal_sell['tp_min_max'] = np.nan
			signal_sell['st_min_max_index'] = np.nan
			signal_sell['st_min_max'] = np.nan
			signal_sell['flag_min_max'] = np.nan

			signal_sell['tp_pr_index'] = np.nan
			signal_sell['tp_pr'] = np.nan
			signal_sell['st_pr_index'] = np.nan
			signal_sell['st_pr'] = np.nan
			signal_sell['flag_pr'] = np.nan
			signal_sell['diff_pr_top'] = np.nan
			signal_sell['diff_pr_down'] = np.nan

		i = 0
		j = 0

		#***************************** Buy Find Section ***********************************************
		for elm in extreme_min.index:
			#+++++++++++++++++++++++++++++++++++++ Primary +++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Primary Buy ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_min['value'][elm] > extreme_min['value'][elm-1]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] <= dataset[symbol]['low'][extreme_min['index'][elm-1]])):
				signal_buy['signal'][i] = 'buy_primary'
				signal_buy['value_front'][i] = extreme_min['value'][elm]
				signal_buy['value_back'][i] = extreme_min['value'][elm-1]
				signal_buy['index'][i] = extreme_min['index'][elm]
				signal_buy['ramp_macd'][i] = (extreme_min['value'][elm] - extreme_min['value'][elm-1])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy['ramp_candle'][i] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-1]])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy['coef_ramps'][i] = signal_buy['ramp_macd'][i]/signal_buy['ramp_candle'][i]
				signal_buy['diff_ramps'][i] = signal_buy['ramp_macd'][i] - signal_buy['ramp_candle'][i]
				signal_buy['beta'][i] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy['danger_line'][i] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy['beta'][i])/100)
				signal_buy['diff_min_max_macd'][i] = ((np.max(macd.macd[extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([signal_buy['value_back'][i],signal_buy['value_front'][i]])) / np.min([signal_buy['value_back'][i],signal_buy['value_front'][i]])) * 100
				signal_buy['diff_min_max_candle'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					#Calculate With Min Max Diff From MACD:

					if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy['diff_min_max_candle'][i])))[0]) - 1) > 1):
						signal_buy['tp_min_max_index'][i] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy['diff_min_max_candle'][i])))[0])
						signal_buy['tp_min_max'][i] = ((dataset[symbol]['high'][signal_buy['tp_min_max_index'][i]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['tp_min_max_index'][i] = -1
						signal_buy['tp_min_max'][i] = 0

					if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
						signal_buy['st_min_max_index'][i] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
						signal_buy['st_min_max'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy['st_min_max_index'][i]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['st_min_max_index'][i] = -1
						signal_buy['st_min_max'][i] = 0

					if (signal_buy['st_min_max_index'][i] < signal_buy['tp_min_max_index'][i]):
						signal_buy['flag_min_max'][i] = 'st'
						if (signal_buy['st_min_max_index'][i] != -1):
							signal_buy['tp_min_max'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy['st_min_max_index'][i])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['flag_min_max'][i] = 'tp'
						if (signal_buy['tp_min_max_index'][i] != -1):
							signal_buy['st_min_max'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy['tp_min_max_index'][i])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

					#///////////////////////////////////////////////////

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
						signal_buy['diff_pr_top'][i] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						signal_buy['diff_pr_down'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

						if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
							signal_buy['tp_pr_index'][i] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
							signal_buy['tp_pr'][i] = ((dataset[symbol]['high'][signal_buy['tp_pr_index'][i]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['tp_pr_index'][i] = -1
							signal_buy['tp_pr'][i] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
							signal_buy['st_pr_index'][i] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
							signal_buy['st_pr'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy['st_pr_index'][i]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['st_pr_index'][i] = -1
							signal_buy['st_pr'][i] = 0

						if (signal_buy['st_pr_index'][i] < signal_buy['tp_pr_index'][i]):
							signal_buy['flag_pr'][i] = 'st'
							if (signal_buy['st_pr_index'][i] != -1):
								signal_buy['tp_pr'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy['st_pr_index'][i])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['flag_pr'][i] = 'tp'
							if (signal_buy['tp_pr_index'][i] != -1):
								signal_buy['st_pr'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy['tp_pr_index'][i])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
					else:
						signal_buy['tp_pr_index'][i] = -1
						signal_buy['tp_pr'][i] = 0
						signal_buy['st_pr_index'][i] = -1
						signal_buy['st_pr'][i] = 0
						signal_buy['flag_pr'][i] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[extreme_min['value'][elm-1],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-1]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				i += 1
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
					
			#///////////////////////////////////////////////////////
			#---------------------------------------------------------------------------------------------------

			#+++++++++++++++++++++++++++++++++++++ Secondry ++++++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Secondry Buy ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_min['value'][elm] < extreme_min['value'][elm-1]) &
				(dataset[symbol]['low'][extreme_min['index'][elm]] > dataset[symbol]['low'][extreme_min['index'][elm-1]])):
				signal_buy['signal'][i] = 'buy_secondry'
				signal_buy['value_front'][i] = extreme_min['value'][elm]
				signal_buy['value_back'][i] = extreme_min['value'][elm-1]
				signal_buy['index'][i] = extreme_min['index'][elm]
				signal_buy['ramp_macd'][i] = (extreme_min['value'][elm] - extreme_min['value'][elm-1])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy['ramp_candle'][i] = (dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm-1]])/(extreme_min['index'][elm] - extreme_min['index'][elm-1])
				signal_buy['coef_ramps'][i] = signal_buy['ramp_macd'][i]/signal_buy['ramp_candle'][i]
				signal_buy['diff_ramps'][i] = signal_buy['ramp_macd'][i] - signal_buy['ramp_candle'][i]
				signal_buy['beta'][i] = ((dataset[symbol]['high'][extreme_min['index'][elm]] - dataset[symbol]['low'][extreme_min['index'][elm]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
				signal_buy['danger_line'][i] = dataset[symbol]['low'][extreme_min['index'][elm]] + ((dataset[symbol]['low'][extreme_min['index'][elm]]*signal_buy['beta'][i])/100)
				signal_buy['diff_min_max_macd'][i] = ((np.max(macd.macd[extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([signal_buy['value_back'][i],signal_buy['value_front'][i]])) / np.min([signal_buy['value_back'][i],signal_buy['value_front'][i]])) * 100
				signal_buy['diff_min_max_candle'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm-1]:extreme_min['index'][elm]]) - np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) / np.min([dataset[symbol]['low'][extreme_min['index'][elm]],dataset[symbol]['low'][extreme_min['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					#Calculate With Min Max Diff From MACD:

					if ((len(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy['diff_min_max_candle'][i])))[0]) - 1) > 1):
						signal_buy['tp_min_max_index'][i] = extreme_min['index'][elm] + np.min(np.where((((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]).values) * 100) >= (signal_buy['diff_min_max_candle'][i])))[0])
						signal_buy['tp_min_max'][i] = ((dataset[symbol]['high'][signal_buy['tp_min_max_index'][i]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['tp_min_max_index'][i] = -1
						signal_buy['tp_min_max'][i] = 0

					if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])-1) > 1):
						signal_buy['st_min_max_index'][i] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9994)))[0])
						signal_buy['st_min_max'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy['st_min_max_index'][i]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['st_min_max_index'][i] = -1
						signal_buy['st_min_max'][i] = 0

					if (signal_buy['st_min_max_index'][i] < signal_buy['tp_min_max_index'][i]):
						signal_buy['flag_min_max'][i] = 'st'
						if (signal_buy['st_min_max_index'][i] != -1):
							signal_buy['tp_min_max'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy['st_min_max_index'][i])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
					else:
						signal_buy['flag_min_max'][i] = 'tp'
						if (signal_buy['tp_min_max_index'][i] != -1):
							signal_buy['st_min_max'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy['tp_min_max_index'][i])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

					#///////////////////////////////////////////////////

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
						signal_buy['diff_pr_top'][i] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						signal_buy['diff_pr_down'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100

						if ((len(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
							signal_buy['tp_pr_index'][i] = extreme_min['index'][elm] + np.min(np.where(((dataset[symbol]['high'][extreme_min['index'][elm]:-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
							signal_buy['tp_pr'][i] = ((dataset[symbol]['high'][signal_buy['tp_pr_index'][i]] - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['tp_pr_index'][i] = -1
							signal_buy['tp_pr'][i] = 0

						if ((len(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
							signal_buy['st_pr_index'][i] = extreme_min['index'][elm] + np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]:-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
							signal_buy['st_pr'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - dataset[symbol]['low'][signal_buy['st_pr_index'][i]])/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['st_pr_index'][i] = -1
							signal_buy['st_pr'][i] = 0

						if (signal_buy['st_pr_index'][i] < signal_buy['tp_pr_index'][i]):
							signal_buy['flag_pr'][i] = 'st'
							if (signal_buy['st_pr_index'][i] != -1):
								signal_buy['tp_pr'][i] = ((np.max(dataset[symbol]['high'][extreme_min['index'][elm]:int(signal_buy['st_pr_index'][i])]) - dataset[symbol]['high'][extreme_min['index'][elm]])/dataset[symbol]['high'][extreme_min['index'][elm]]) * 100
						else:
							signal_buy['flag_pr'][i] = 'tp'
							if (signal_buy['tp_pr_index'][i] != -1):
								signal_buy['st_pr'][i] = ((dataset[symbol]['low'][extreme_min['index'][elm]] - np.min(dataset[symbol]['low'][extreme_min['index'][elm]:int(signal_buy['tp_pr_index'][i])]))/dataset[symbol]['low'][extreme_min['index'][elm]]) * 100
						
					else:
						signal_buy['tp_pr_index'][i] = -1
						signal_buy['tp_pr'][i] = 0
						signal_buy['st_pr_index'][i] = -1
						signal_buy['st_pr'][i] = 0
						signal_buy['flag_pr'][i] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[extreme_min['value'][elm-1],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-1]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				i += 1		
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
		i = 0
		j = 0
		for elm in extreme_max.index:
			#++++++++++++++++++++++++++++++++++++ Primary ++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Primary Sell ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_max['value'][elm] < extreme_max['value'][elm-1]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] >= dataset[symbol]['high'][extreme_max['index'][elm-1]])):
				signal_sell['signal'][i] = 'sell_primary'
				signal_sell['value_front'][i] = extreme_max['value'][elm]
				signal_sell['value_back'][i] = extreme_max['value'][elm-1]
				signal_sell['index'][i] = extreme_max['index'][elm]
				signal_sell['ramp_macd'][i] = (extreme_max['value'][elm] - extreme_max['value'][elm-1])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell['ramp_candle'][i] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-1]])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell['coef_ramps'][i] = signal_sell['ramp_macd'][i]/signal_sell['ramp_candle'][i]
				signal_sell['diff_ramps'][i] = signal_sell['ramp_macd'][i] - signal_sell['ramp_candle'][i]
				signal_sell['beta'][i] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell['danger_line'][i] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell['beta'][i])/100)
				signal_sell['diff_min_max_macd'][i] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([signal_sell['value_back'][i],signal_sell['value_front'][i]])) / np.max([signal_sell['value_back'][i],signal_sell['value_front'][i]])) * 100
				signal_sell['diff_min_max_candle'][i] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					#Calculate With Min Max Diff From MACD:

					if ((len(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell['diff_min_max_candle'][i])))[0]) - 1) > 1):
						signal_sell['tp_min_max_index'][i] = extreme_max['index'][elm] + np.min(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell['diff_min_max_candle'][i])))[0])
						signal_sell['tp_min_max'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell['tp_min_max_index'][i]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['tp_min_max_index'][i] = -1
						signal_sell['tp_min_max'][i] = 0

					if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])-1) > 1):
						signal_sell['st_min_max_index'][i] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])
						signal_sell['st_min_max'][i] = ((dataset[symbol]['high'][signal_sell['st_min_max_index'][i]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['st_min_max_index'][i] = -1
						signal_sell['st_min_max'][i] = 0

					if (signal_sell['st_min_max_index'][i] < signal_sell['tp_min_max_index'][i]):
						signal_sell['flag_min_max'][i] = 'st'
						if (signal_sell['st_min_max_index'][i] != -1):
							signal_sell['tp_min_max'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell['st_min_max_index'][i])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['flag_min_max'][i] = 'tp'
						if (signal_sell['tp_min_max_index'][i] != -1):
							signal_sell['st_min_max'][i] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell['tp_min_max_index'][i])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

					#///////////////////////////////////////////////////

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
						signal_sell['diff_pr_top'][i] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						signal_sell['diff_pr_down'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

						if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
							signal_sell['tp_pr_index'][i] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
							signal_sell['tp_pr'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell['tp_pr_index'][i]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['tp_pr_index'][i] = -1
							signal_sell['tp_pr'][i] = 0

						if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
							signal_sell['st_pr_index'][i] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
							signal_sell['st_pr'][i] = ((dataset[symbol]['high'][signal_sell['st_pr_index'][i]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['st_pr_index'][i] = -1
							signal_sell['st_pr'][i] = 0

						if (signal_sell['st_pr_index'][i] < signal_sell['tp_pr_index'][i]):
							signal_sell['flag_pr'][i] = 'st'
							if (signal_sell['st_pr_index'][i] != -1):
								signal_sell['tp_pr'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell['st_pr_index'][i])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['flag_pr'][i] = 'tp'
							if (signal_sell['tp_pr_index'][i] != -1):
								signal_sell['st_pr'][i] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell['tp_pr_index'][i])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
					else:
						signal_sell['tp_pr_index'][i] = -1
						signal_sell['tp_pr'][i] = 0
						signal_sell['st_pr_index'][i] = -1
						signal_sell['st_pr'][i] = 0
						signal_sell['flag_pr'][i] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[extreme_max['value'][elm-1],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-1]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				i += 1		
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

			#++++++++++++++++++++++++++++++++++++++ Secondry +++++++++++++++++++++++++++++++++++++++++++++++++++
			#****************************** Secondry Sell ********************************* = 1
			if (elm - 1 < 0): continue
			if ((extreme_max['value'][elm] > extreme_max['value'][elm-1]) &
				(dataset[symbol]['high'][extreme_max['index'][elm]] < dataset[symbol]['high'][extreme_max['index'][elm-1]])):
				signal_sell['signal'][i] = 'sell_secondry'
				signal_sell['value_front'][i] = extreme_max['value'][elm]
				signal_sell['value_back'][i] = extreme_max['value'][elm-1]
				signal_sell['index'][i] = extreme_max['index'][elm]
				signal_sell['ramp_macd'][i] = (extreme_max['value'][elm] - extreme_max['value'][elm-1])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell['ramp_candle'][i] = (dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['high'][extreme_max['index'][elm-1]])/(extreme_max['index'][elm] - extreme_max['index'][elm-1])
				signal_sell['coef_ramps'][i] = signal_sell['ramp_macd'][i]/signal_sell['ramp_candle'][i]
				signal_sell['diff_ramps'][i] = signal_sell['ramp_macd'][i] - signal_sell['ramp_candle'][i]
				signal_sell['beta'][i] = ((dataset[symbol]['high'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
				signal_sell['danger_line'][i] = dataset[symbol]['high'][extreme_max['index'][elm]] + ((dataset[symbol]['high'][extreme_max['index'][elm]]*signal_sell['beta'][i])/100)
				signal_sell['diff_min_max_macd'][i] = (-1 * (np.min(macd.macd[extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([signal_sell['value_back'][i],signal_sell['value_front'][i]])) / np.max([signal_sell['value_back'][i],signal_sell['value_front'][i]])) * 100
				signal_sell['diff_min_max_candle'][i] = (-1 * (np.min(dataset[symbol]['low'][extreme_max['index'][elm-1]:extreme_max['index'][elm]]) - np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) / np.max([dataset[symbol]['high'][extreme_max['index'][elm]],dataset[symbol]['high'][extreme_max['index'][elm-1]]])) * 100

				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					#Calculate With Min Max Diff From MACD:

					if ((len(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell['diff_min_max_candle'][i])))[0]) - 1) > 1):
						signal_sell['tp_min_max_index'][i] = extreme_max['index'][elm] + np.min(np.where((((((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][extreme_max['index'][elm]:-1])/dataset[symbol]['low'][extreme_max['index'][elm]]).values) * 100) >= (signal_sell['diff_min_max_candle'][i])))[0])
						signal_sell['tp_min_max'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell['tp_min_max_index'][i]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['tp_min_max_index'][i] = -1
						signal_sell['tp_min_max'][i] = 0

					if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])-1) > 1):
						signal_sell['st_min_max_index'][i] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (dataset[symbol]['high'][extreme_max['index'][elm]] * 1.0006)))[0])
						signal_sell['st_min_max'][i] = ((dataset[symbol]['high'][signal_sell['st_min_max_index'][i]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['st_min_max_index'][i] = -1
						signal_sell['st_min_max'][i] = 0

					if (signal_sell['st_min_max_index'][i] < signal_sell['tp_min_max_index'][i]):
						signal_sell['flag_min_max'][i] = 'st'
						if (signal_sell['st_min_max_index'][i] != -1):
							signal_sell['tp_min_max'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell['st_min_max_index'][i])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
					else:
						signal_sell['flag_min_max'][i] = 'tp'
						if (signal_sell['tp_min_max_index'][i] != -1):
							signal_sell['st_min_max'][i] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell['tp_min_max_index'][i])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100

					#///////////////////////////////////////////////////

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
						signal_sell['diff_pr_top'][i] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						signal_sell['diff_pr_down'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100

						if ((len(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
							signal_sell['tp_pr_index'][i] = extreme_max['index'][elm] + np.min(np.where(((dataset[symbol]['low'][extreme_max['index'][elm]:-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
							signal_sell['tp_pr'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - dataset[symbol]['low'][signal_sell['tp_pr_index'][i]])/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['tp_pr_index'][i] = -1
							signal_sell['tp_pr'][i] = 0

						if ((len(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
							signal_sell['st_pr_index'][i] = extreme_max['index'][elm] + np.min(np.where((((dataset[symbol]['high'][extreme_max['index'][elm]:-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
							signal_sell['st_pr'][i] = ((dataset[symbol]['high'][signal_sell['st_pr_index'][i]] - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['st_pr_index'][i] = -1
							signal_sell['st_pr'][i] = 0

						if (signal_sell['st_pr_index'][i] < signal_sell['tp_pr_index'][i]):
							signal_sell['flag_pr'][i] = 'st'
							if (signal_sell['st_pr_index'][i] != -1):
								signal_sell['tp_pr'][i] = ((dataset[symbol]['low'][extreme_max['index'][elm]] - np.min(dataset[symbol]['low'][extreme_max['index'][elm]:int(signal_sell['st_pr_index'][i])]))/dataset[symbol]['low'][extreme_max['index'][elm]]) * 100
						else:
							signal_sell['flag_pr'][i] = 'tp'
							if (signal_sell['tp_pr_index'][i] != -1):
								signal_sell['st_pr'][i] = ((np.max(dataset[symbol]['high'][extreme_max['index'][elm]:int(signal_sell['tp_pr_index'][i])]) - dataset[symbol]['high'][extreme_max['index'][elm]])/dataset[symbol]['high'][extreme_max['index'][elm]]) * 100
						
					else:
						signal_sell['tp_pr_index'][i] = -1
						signal_sell['tp_pr'][i] = 0
						signal_sell['st_pr_index'][i] = -1
						signal_sell['st_pr'][i] = 0
						signal_sell['flag_pr'][i] = 'no_flag'
					#///////////////////////////////////////////////////
				if (plot == True):
					ax0.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[extreme_max['value'][elm-1],extreme_max['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_max['index'][elm-1],extreme_max['index'][elm]],[dataset[symbol]['low'][extreme_max['index'][elm-1]],dataset[symbol]['low'][extreme_max['index'][elm]]],c='r',linestyle="-")
				i += 1
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
	signal_buy = signal_buy.drop(columns=0)
	signal_buy = signal_buy.dropna()
	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_buy = signal_buy.reset_index(drop=True)

	signal_sell = signal_sell.drop(columns=0)
	signal_sell = signal_sell.dropna()
	signal_sell = signal_sell.sort_values(by = ['index'])
	signal_sell = signal_sell.reset_index(drop=True)
	

	print(signal_buy)
	print('*********************** Buy *********************************')

	print('mean tp pr = ',np.mean(signal_buy['tp_pr']))
	print('mean st pr = ',np.mean(signal_buy['st_pr']))
	print('mean tp min_max = ',np.mean(signal_buy['tp_min_max']))
	print('mean st min_max = ',np.mean(signal_buy['st_min_max']))

	print('max tp pr = ',np.max(signal_buy['tp_pr']))
	print('max st pr = ',np.max(signal_buy['st_pr']))
	print('max tp min_max = ',np.max(signal_buy['tp_min_max']))
	print('max st min_max = ',np.max(signal_buy['st_min_max']))

	print('tp pr = ',np.bincount(signal_buy['flag_pr'] == 'tp'))
	print('st pr = ',np.bincount(signal_buy['flag_pr'] == 'st'))
	print('tp min_max = ',np.bincount(signal_buy['flag_min_max'] == 'tp'))
	print('st min_max = ',np.bincount(signal_buy['flag_min_max'] == 'st'))

	print('sum st pr = ',np.sum(signal_buy['st_pr'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy()))
	print('sum tp pr = ',np.sum(signal_buy['tp_pr'][np.where(signal_buy['flag_pr'] == 'tp')[0]].to_numpy()))

	print('sum st min_max = ',np.sum(signal_buy['st_min_max'][np.where(signal_buy['flag_min_max'] == 'st')[0]].to_numpy()))
	print('sum tp min_max = ',np.sum(signal_buy['tp_min_max'][np.where(signal_buy['flag_min_max'] == 'tp')[0]].to_numpy()))

	print('max down = ',np.max(signal_buy['diff_pr_down'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy()))
	print('min down = ',np.min(signal_buy['diff_pr_down'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy()))
	print('mean down = ',np.mean(signal_buy['diff_pr_down'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy()))

	print('/////////////////////////////////////////////////////////////////')

	print(signal_sell)

	print('*************************** Sell ***********************************')

	print('mean tp pr = ',np.mean(signal_sell['tp_pr']))
	print('mean st pr = ',np.mean(signal_sell['st_pr']))
	print('mean tp min_max = ',np.mean(signal_sell['tp_min_max']))
	print('mean st min_max = ',np.mean(signal_sell['st_min_max']))

	print('max tp pr = ',np.max(signal_sell['tp_pr']))
	print('max st pr = ',np.max(signal_sell['st_pr']))
	print('max tp min_max = ',np.max(signal_sell['tp_min_max']))
	print('max st min_max = ',np.max(signal_sell['st_min_max']))

	print('tp pr = ',np.bincount(signal_sell['flag_pr'] == 'tp'))
	print('st pr = ',np.bincount(signal_sell['flag_pr'] == 'st'))
	print('tp min_max = ',np.bincount(signal_sell['flag_min_max'] == 'tp'))
	print('st min_max = ',np.bincount(signal_sell['flag_min_max'] == 'st'))

	print('sum st pr = ',np.sum(signal_sell['st_pr'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy()))
	print('sum tp pr = ',np.sum(signal_sell['tp_pr'][np.where(signal_sell['flag_pr'] == 'tp')[0]].to_numpy()))

	print('sum st min_max = ',np.sum(signal_sell['st_min_max'][np.where(signal_sell['flag_min_max'] == 'st')[0]].to_numpy()))
	print('sum tp min_max = ',np.sum(signal_sell['tp_min_max'][np.where(signal_sell['flag_min_max'] == 'tp')[0]].to_numpy()))

	print('max down = ',np.max(signal_sell['diff_pr_down'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy()))
	print('min down = ',np.min(signal_sell['diff_pr_down'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy()))
	print('mean down = ',np.mean(signal_sell['diff_pr_down'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy()))

	if (plot == True):
		plt.show()
	return 0,0

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#*********************************** How To Use Funcs ************************************************************

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,12000)
symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,4000)
symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,1000)
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
signal_buy,signal_sell = divergence(dataset=symbol_data_5M,dataset_15M=symbol_data_15M,dataset_1H=symbol_data_1H,Apply_to='close',symbol='AUDCAD_i',
	macd_fast=2,macd_slow=4,macd_signal=2,mode='optimize',plot=False)
print('time Dive = ',time.time() - time_first)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////