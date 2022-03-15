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
#from src.utils.resist_protect import bestExtremeFinder, extremePoints

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

	signal_buy = signal_buy.dropna(inplace = False)
	signal_sell = signal_sell.dropna(inplace = False)

	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_sell = signal_sell.sort_values(by = ['index'])

	return signal_buy,signal_sell

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Divergence Strategy *******************************************************

def divergence(dataset,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False):

	macd_read = ind.macd(dataset[symbol][Apply_to],fast = macd_fast,slow = macd_slow,signal = macd_signal)

	macd = pd.DataFrame()
	column = macd_read.columns[0]
	macd['macd'] = pd.DataFrame(macd_read, columns=[column])
	macd = macd.dropna(inplace=False)

	n = 5
	extreme = pd.DataFrame()
	macd['min'] = macd.iloc[argrelextrema(macd.macd.values, comparator = np.less,
                    order=n)[0]]['macd']
	macd['max'] = macd.iloc[argrelextrema(macd.macd.values, comparator = np.greater,
                    order=n)[0]]['macd']

	plt.plot(macd['max'].dropna().index,macd['max'].dropna(), 'o',c='g')
	plt.plot(macd.index,macd.macd,c='r')
	plt.show()

	print(macd['max'].dropna())

	return signal_buy,signal_sell

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
	macd_fast=12,macd_slow=26,macd_signal=9,mode='online',plot=False)
print('time Dive = ',time.time() - time_first)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////