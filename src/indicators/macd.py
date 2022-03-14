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
def Golden_Cross_SMA(dataset,Apply_to,symbol,macd_fast=12,macd_slow=26,macd_signal=9,plot=False):

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

	i = 0
	j = 0
	k = 0

	print(cross['index'][32])

	plt.plot(macd.index,macd.macd,c = 'b')
	plt.plot(macd.index,macd.macds,c = 'r')

	buy_indexes = cross['index'][np.where(((macd.macds[cross['index']-1].to_numpy()>macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()<macd.macd[cross['index']+1].to_numpy())))[0]]
	buy_cross_indexes = np.where(((macd.macds[cross['index']-1].to_numpy()>macd.macd[cross['index']-1].to_numpy())&(macd.macds[cross['index']+1].to_numpy()<macd.macd[cross['index']+1].to_numpy())))[0]
	signal_buy['signal'][buy_cross_indexes] = 'buy'
	signal_buy['values'] = cross['values'][buy_cross_indexes]
	signal_buy['index'][buy_cross_indexes] = buy_indexes

	print(buy_indexes)

	#if ((buy_cross_indexes+1) < len(cross)):
	#	signal_buy['profit'] = (np.max(dataset[symbol]['close'][buy_indexes:cross['index'][buy_cross_indexes+1]] - dataset[symbol]['close'][buy_indexes])/dataset[symbol]['close'][buy_indexes]) * 100
	#else:
	close = dataset[symbol]['close']
	print('index buy = ',buy_indexes.values)
	print('index cross last = ',cross['index'][buy_cross_indexes])
	print(((close[buy_indexes.values[0]:cross['index'][buy_cross_indexes[0]+1]] - close[buy_indexes.values[0]])/dataset[symbol]['close'][buy_indexes.values[0]]))
	signal_buy['profit'] = (np.max((close[buy_indexes.values[0]:-1] - close[buy_indexes.values[0]])/dataset[symbol]['close'][buy_indexes.values[0]])) * 100

	#signal_buy['profit'][buy_cross_indexes] = (np.max(dataset[symbol]['close'][buy_indexes:cross['index'][buy_cross_indexes+1]] - dataset[symbol]['close'][buy_indexes])/dataset[symbol]['close'][buy_indexes]) * 100
	print(signal_buy)

	for a in buy_indexes:
		plt.axvline(x=a, color='g', linestyle='-')

	#plt.show()
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


	signal_buy = signal_buy.dropna(inplace = False)
	signal_sell = signal_sell.dropna(inplace = False)

	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_sell = signal_sell.sort_values(by = ['index'])

	return signal_buy,signal_sell

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Divergence Strategy *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************************** How To Use Funcs ************************************************************

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,1000)

signal = Golden_Cross_SMA(dataset=symbol_data_5M,Apply_to='close',symbol='AUDCAD_i',macd_fast=12,macd_slow=26,macd_signal=9,plot=False)
#print(signal)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////