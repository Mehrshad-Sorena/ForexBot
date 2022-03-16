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

def divergence(dataset,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False):


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
			signal_buy['st_min_max_index'] = np.nan


		signal_sell = pd.DataFrame(np.zeros(len(extreme_max)))
		signal_sell['signal'] = np.nan
		signal_sell['values'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['profit'] = np.nan

		i = 0
		j = 0

		for elm in extreme_min.index:
			#print(extreme_min['value'][elm])
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
					#print('where = ',np.where((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['close'][extreme_min['index'][elm]])/dataset[symbol]['close'][extreme_min['index'][elm]]) * 100) >= signal_buy['diff_min_max_candle'][i])[0])
					#print('where = ',np.min(np.where((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['close'][extreme_min['index'][elm]])/dataset[symbol]['close'][extreme_min['index'][elm]]) * 100) >= signal_buy['diff_min_max_candle'][i])[0]))
					#print('elm = ',elm)
					if (len(np.where((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['close'][extreme_min['index'][elm]])/dataset[symbol]['close'][extreme_min['index'][elm]]) * 100) >= signal_buy['diff_min_max_candle'][i])[0]) != 0):
						signal_buy['tp_min_max_index'][i] = np.min(np.where((((dataset[symbol]['high'][extreme_min['index'][elm]:-1] - dataset[symbol]['close'][extreme_min['index'][elm]])/dataset[symbol]['close'][extreme_min['index'][elm]]) * 100) >= signal_buy['diff_min_max_candle'][i])[0])
						#print('where = ',signal_buy['tp_min_max_index'][i])
						#print('elm = ',elm)
					else:
						signal_buy['tp_min_max_index'][i] = 'no_tp_min_max'

					if True:#(len(np.where(((dataset[symbol]['low'][extreme_min['index'][elm]:-1] - dataset[symbol]['low'][extreme_min['index'][elm]])) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9990))[0]) != 0):
						#signal_buy['st_min_max_index'][i] = np.min(np.where(((dataset[symbol]['low'][extreme_min['index'][elm]:-1] - dataset[symbol]['low'][extreme_min['index'][elm]])) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9990))[0])
						#print('where = ',np.min((((dataset[symbol]['low'][extreme_min['index'][elm]+1:-1] - dataset[symbol]['low'][extreme_min['index'][elm]])) <= (dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9990)).index))
						print('elm = ',extreme_min['index'][elm])
						print('low1 = ',(dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9000) - dataset[symbol]['low'][extreme_min['index'][elm]])
						#print('low2 = ',dataset[symbol]['low'][extreme_min['index'][elm]])
						#print('low3 = ',(dataset[symbol]['low'][extreme_min['index'][elm]+1:-1] - dataset[symbol]['low'][extreme_min['index'][elm]]).values)
						print(np.min(np.where((((dataset[symbol]['low'][extreme_min['index'][elm]+1:-1] - dataset[symbol]['low'][extreme_min['index'][elm]]).values) <= ((dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9999) - dataset[symbol]['low'][extreme_min['index'][elm]])))[0]))
						ax1.axvline(x=np.min((((dataset[symbol]['low'][extreme_min['index'][elm]+1:-1] - dataset[symbol]['low'][extreme_min['index'][elm]]).values) <= ((dataset[symbol]['low'][extreme_min['index'][elm]] * 0.9999) - dataset[symbol]['low'][extreme_min['index'][elm]]))))
					else:
						signal_buy['st_min_max_index'][i] = 'no_st_min_max'
					#signal_buy['st'][i] = 

				if (plot == True):
					ax0.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[extreme_min['value'][elm-1],extreme_min['value'][elm]],c='r',linestyle="-")
					ax1.plot([extreme_min['index'][elm-1],extreme_min['index'][elm]],[dataset[symbol]['low'][extreme_min['index'][elm-1]],dataset[symbol]['low'][extreme_min['index'][elm]]],c='r',linestyle="-")
				i += 1

	#/////////////////////////////////////////////////////////////////////////////

	#*************************** OutPuts ***************************************
	signal_buy = signal_buy.drop(columns=0)
	signal_buy = signal_buy.dropna()
	print(signal_buy)
	if (plot == True):
		plt.show()
	return 0,0

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#*********************************** How To Use Funcs ************************************************************

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,2000)
print('get data')
time_first = time.time()
signal_buy,signal_sell = golden_cross(dataset=symbol_data_5M,Apply_to='close',symbol='AUDCAD_i',
	macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False)
print('time Cross = ',time.time() - time_first)
#print(signal_buy)
#print(signal_sell)

time_first = time.time()
signal_buy,signal_sell = divergence(dataset=symbol_data_5M,Apply_to='close',symbol='AUDCAD_i',
	macd_fast=12,macd_slow=26,macd_signal=9,mode='optimize',plot=True)
print('time Dive = ',time.time() - time_first)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////