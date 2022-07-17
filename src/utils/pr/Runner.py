import pandas as pd
import pandas_ta as ind
import numpy as np
import matplotlib.pyplot as plt
import math

from BestFinder import best_extreme_finder
from RampLineFinder import extreme_points_ramp_lines
from FlatLinesIchimoku import flat_lines_ichimoko
from ExtremePoints import extreme_points
import Parameters
import Config

#from matplotlib.collections import LineCollection
#from scipy.interpolate import interp1d
#from sklearn.linear_model import LinearRegression
#from sklearn.isotonic import IsotonicRegression
#from sklearn.utils import check_random_state
#from timer import stTime


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ta.ichimoku)

#***************** Function Names ***********
# extreme_points()
# flat_lines_ichimoko()
# extreme_points_ramp_lines()
# best_extreme_finder()
# protect_resist()
#//////////////////////////////////////////////

#***************************** Protect Resist Finder **************************************************************
class Runner:

	
	#@stTime
	def __init__(
				self,
				number_max_5m,
				number_min_5m,
				weight_extreme_5m,

				trend_short_length_1,
				trend_short_length_2,
				trend_mid_length,
				trend_long_length,

				trend_num_max_short_1,
				trend_num_min_short_1,

				trend_num_max_short_2,
				trend_num_min_short_2,

				trend_num_max_mid,
				trend_num_min_mid,
					
				trend_num_max_long,
				trend_num_min_long,

				tenkan_5m,
				kijun_5m,
				senkou_5m,
				culster_ichi_5m,
				weight_ichi_5m,

				number_max_1h,
				number_min_1h,
				weight_extreme_1h,
				tenkan_1h,
				kijun_1h,
				senkou_1h,
				culster_ichi_1h,
				weight_ichi_1h,

				n_clusters_best_low,
				n_clusters_best_high,
				alpha_low,
				alpha_high,

				dataset_5M,
				dataset_1H,
				):
		self.number_max_5m = number_max_5m
		self.number_min_5m = number_min_5m
		self.weight_extreme_5m = weight_extreme_5m

		self.trend_short_length_1=trend_short_length_1
		self.trend_short_length_2=trend_short_length_2
		self.trend_mid_length=trend_mid_length
		self.trend_long_length=trend_long_length

		self.trend_num_max_short_1=trend_num_max_short_1
		self.trend_num_min_short_1=trend_num_min_short_1

		self.trend_num_max_short_2=trend_num_max_short_2
		self.trend_num_min_short_2=trend_num_min_short_2

		self.trend_num_max_mid=trend_num_max_mid
		self.trend_num_min_mid=trend_num_min_mid
					
		self.trend_num_max_long=trend_num_max_long
		self.trend_num_min_long=trend_num_min_long

		self.tenkan_5m=tenkan_5m
		self.kijun_5m=kijun_5m
		self.senkou_5m=senkou_5m
		self.culster_ichi_5m=culster_ichi_5m
		self.weight_ichi_5m=weight_ichi_5m

		self.number_max_1h=number_max_1h
		self.number_min_1h=number_min_1h
		self.weight_extreme_1h=weight_extreme_1h
		self.tenkan_1h=tenkan_1h
		self.kijun_1h=kijun_1h
		self.senkou_1h=senkou_1h
		self.culster_ichi_1h=culster_ichi_1h
		self.weight_ichi_1h=weight_ichi_1h

		self.n_clusters_best_low=n_clusters_best_low
		self.n_clusters_best_high=n_clusters_best_high
		self.alpha_low=alpha_low
		self.alpha_high=alpha_high

		self.dataset_5M = dataset_5M
		self.dataset_1H = dataset_1H


	#This Function Calculate Tp And St With Above Function And Out Best Tp And St With Best_Extreme_Finder:
	def start(pr_param):

		#****************** Extreme Points Finder Function: Finding Top Down Points *********************
		local_extreme_5M, local_extreme_1H = exterm_point_get(param = pr_input)
		#//////////////////////////////////////////////////////////////////////////////////////////////////



		#**************************** Trend Line Extreme Finder Function **************************************
		if (pr_input.T_5M == True):
			trend_local_extreme_5M_long = trend_line_get(
														dataset_5M = dataset_5M,
														length = 'long',
														parameters = parameters
														)

			trend_local_extreme_5M_mid = trend_line_get(
														dataset_5M = dataset_5M,
														length = 'mid',
														parameters = parameters
														)

			trend_local_extreme_5M_short_1 = trend_line_get(
															dataset_5M = dataset_5M,
															length = 'short_length_1',
															parameters = parameters
															)

			trend_local_extreme_5M_short_1 = trend_line_get(
															dataset_5M = dataset_5M,
															length = 'short_length_2',
															parameters = parameters
															)

		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#*************************************** ichi Extreme Finder Function ********************************************************
		#flat_lines_ichi_get(

							#)
		#Finding From 5M TimeFrame:
		ichi_local_extreme_5M = pd.DataFrame()
		ichi_local_extreme_5M['extreme'] = np.nan
		ichi_local_extreme_5M['power'] = np.nan
		if (T_5M == True):
			ichi_local_extreme_5M = Extreme_points_ichimoko(
															dataset_5M['high'],
															dataset_5M['low'],
															dataset_5M['close'],
															tenkan=parameters['tenkan_5m'][0],
															kijun=parameters['kijun_5m'][0],
															senkou=parameters['senkou_5m'][0],
															n_clusters=parameters['culster_ichi_5m'][0],
															weight=parameters['weight_ichi_5m'][0]
															)

		#Finding From 1H TimeFrame:
		ichi_local_extreme_1H = pd.DataFrame()
		ichi_local_extreme_1H['extreme'] = np.nan
		ichi_local_extreme_1H['power'] = np.nan
		if (T_1H == True):
			ichi_local_extreme_1H = Extreme_points_ichimoko(
															dataset_1H['high'],
															dataset_1H['low'],
															dataset_1H['close'],
															tenkan=parameters['tenkan_1h'][0],
															kijun=parameters['kijun_1h'][0],
															senkou=parameters['senkou_1h'][0],
															n_clusters=parameters['culster_ichi_1h'][0],
															weight=parameters['weight_ichi_1h'][0]
															)

		#//////////////////////////////////////////////////////////////////////////////////////////////////////////

		#***************** Concatenate All of Extremes That Finded **************************

		exterm_point = pd.DataFrame(
									np.concatenate(
												(
												local_extreme_5M['extreme'].to_numpy(), 
												local_extreme_1H['extreme'].to_numpy(),
												trend_local_extreme_5M_long['min'].to_numpy(),
												trend_local_extreme_5M_long['max'].to_numpy(),
												trend_local_extreme_5M_mid['min'].to_numpy(),
												trend_local_extreme_5M_mid['max'].to_numpy(),
												trend_local_extreme_5M_short_1['min'].to_numpy(),
												trend_local_extreme_5M_short_1['max'].to_numpy(),
												trend_local_extreme_5M_short_2['min'].to_numpy(),
												trend_local_extreme_5M_short_2['max'].to_numpy(),
												ichi_local_extreme_5M['extreme'].to_numpy(),
												ichi_local_extreme_1H['extreme'].to_numpy(),
												), 
												axis=None
												),
									columns=['extremes']
									)

		exterm_point['power'] = np.concatenate(
											(
											local_extreme_5M['power'].to_numpy(), 
											local_extreme_1H['power'].to_numpy(),
											trend_local_extreme_5M_long['power'].to_numpy(),
											trend_local_extreme_5M_long['power'].to_numpy(),
											trend_local_extreme_5M_mid['power'].to_numpy(),
											trend_local_extreme_5M_mid['power'].to_numpy(),
											trend_local_extreme_5M_short_1['power'].to_numpy(),
											trend_local_extreme_5M_short_1['power'].to_numpy(),
											trend_local_extreme_5M_short_2['power'].to_numpy(),
											trend_local_extreme_5M_short_2['power'].to_numpy(),
											ichi_local_extreme_5M['power'].to_numpy(),
											ichi_local_extreme_1H['power'].to_numpy(),
											), 
											axis=None
											)
		#Delete Nan Data:
		exterm_point = exterm_point.dropna()

		#Using Best Extreme Finder To Find Best Tp And St Points:
		extereme = pd.DataFrame()
		extereme = Best_Extreme_Finder(
										exterm_point=exterm_point,
										high=dataset_5M['high'],
										low=dataset_5M['low'],
										n_clusters_low=parameters['n_clusters_best_low'][0],
										n_clusters_high=parameters['n_clusters_best_high'][0],
										alpha_low=parameters['alpha_low'][0],
										alpha_high=parameters['alpha_high'][0],
										timeout_break=1
										)
		#Add Name Of Trends To OutPut DataFrame:
		if T_5M == True:
			extereme['trend_long'] = [
									trend_local_extreme_5M_long['trend'][0],
									trend_local_extreme_5M_long['trend'][0],
									trend_local_extreme_5M_long['trend'][0]
									]

			extereme['trend_mid'] = [
									trend_local_extreme_5M_mid['trend'][0],
									trend_local_extreme_5M_mid['trend'][0],
									trend_local_extreme_5M_mid['trend'][0]
									]

			extereme['trend_short1'] = [
										trend_local_extreme_5M_short_1['trend'][0],
										trend_local_extreme_5M_short_1['trend'][0],
										trend_local_extreme_5M_short_1['trend'][0]
										]

			extereme['trend_short2'] = [
										trend_local_extreme_5M_short_2['trend'][0],
										trend_local_extreme_5M_short_2['trend'][0],
										trend_local_extreme_5M_short_2['trend'][0]
										]


		if (plot == True):
			fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))
			ax0.axhline(y = extereme['high'][0], color = 'r', linestyle = '-')
			ax0.axhline(y = extereme['high'][1], color = 'g', linestyle = '-')
			ax0.axhline(y = extereme['high'][2], color = 'r', linestyle = '-')

			ax0.axhline(y = extereme['low'][0], color = 'g', linestyle = '-')
			ax0.axhline(y = extereme['low'][1], color = 'b', linestyle = '-')
			ax0.axhline(y = extereme['low'][2], color = 'g', linestyle = '-')

			end = len(dataset_5M['close']) - 1

			ax0.axvline(x = end, color = 'r', linestyle = '-')
			ax1.axvline(x = end, color = 'r', linestyle = '-')

			ax0.plot(dataset_5M['close'].index[end-100:end],dataset_5M['close'][end-100:end],'b')
			ax1.plot(dataset_5M['close'].index[end-10:end+300],dataset_5M['close'][end-10:end+300],'b')
			plt.show()

		return extereme
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*******************

def trend_line_get(
					dataset_5M = dataset_5M,
					length = 'long',
					parameters = parameters
					):

	#This Parameters is Defined For Finding Trending Lines:(How Many Candels We want To Find Trend?)

	if length == 'long':
		length_data = parameters['trend_long_length'][0]
	elif length == 'mid':
		length_data = parameters['trend_mid_length'][0]
	elif length == 'short_length_1':
		length_data = parameters['trend_short_length_1'][0]
	elif length == 'short_length_2':
		length_data = parameters['trend_short_length_2'][0]


	trend_local_extreme_5M = pd.DataFrame()
	trend_local_extreme_5M['min'] = np.nan
	trend_local_extreme_5M['max'] = np.nan
	trend_local_extreme_5M['power'] = np.nan

	if (T_5M == True):

		#Cut Input Dataset With Len That WE Want To finding Trend Lines
		dataset_ramp_5M = pd.DataFrame()
		cut_first = 0

		if (
			int(len(dataset_5M['low'])-1) > long_length
			):

			cut_first = int(len(dataset_5M['low'])-1) - long_length

		dataset_ramp_5M['low'] = dataset_5M['low'][
													cut_first:int(len(dataset_5M['low'])-1)
													].reset_index(drop=True)

		dataset_ramp_5M['high'] = dataset_5M['high'][
													cut_first:int(len(dataset_5M['high'])-1)
													].reset_index(drop=True)

		dataset_ramp_5M['close'] = dataset_5M['close'][
													cut_first:int(len(dataset_5M['close'])-1)
													].reset_index(drop=True)

		dataset_ramp_5M['open'] = dataset_5M['open'][
													cut_first:int(len(dataset_5M['open'])-1)
													].reset_index(drop=True)


		trend_local_extreme_5M = pd.DataFrame()
		trend_local_extreme_5M = np.nan

		trend_local_extreme_5M = extreme_points_ramp_lines(
															high = dataset_ramp_5M['high'],
															low = dataset_ramp_5M['low'],
															close = dataset_ramp_5M['close'],
															length=length,
															number_min=parameters['trend_num_min_long'][0],
															number_max=parameters['trend_num_max_long'][0],
															plot=False
															)

	return trend_local_extreme_5M

#//////////////////


#***************************** How To Use Functions **********************************************
"""
from datetime import datetime
symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																								sym='EURUSD_i',
																								num_5M=2000,
																								num_15M=1,
																								num_1H=500,
																								num_4H=1
																								)

sym = 'EURUSD_i'



#print('5M======> ',symbol_data_5M[sym]['time'][1796])


#print(symbol_data_1H[sym]['time'][location_1H])

protect_resist(
				T_5M=True,
				T_15M=False,
				T_1H=True,
				T_4H=False,
				T_1D=False,
				dataset_5M=symbol_data_5M[sym],
				dataset_15M=symbol_data_1H[sym],
				dataset_1H=symbol_data_1H[sym],
				dataset_4H=symbol_data_1H[sym],
				dataset_1D=symbol_data_1H[sym],
				plot=True
				)

"""

#symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,2000)
#symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,2000)
#symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,167)
#symbol_data_4H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,150)
#symbol_data_1D,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

#print('data get')

#x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
#y1 = symbol_data_5M['AUDCAD_i']['close']
#y2 = symbol_data_5M['AUDCAD_i']['open']
#y3 = symbol_data_5M['AUDCAD_i']['high']
#y4 = symbol_data_5M['AUDCAD_i']['low']

#print('data get')


#exterm_point_pred = Extreme_points_ichimoko(high=y3,low=y4,close=y1,tenkan=9,kijun=26,senkou=52,n_clusters=15)
#print(exterm_point_pred)
#i = 0
#for elm in exterm_point_pred['extremes']:
#	plt.axhline(y=elm, color='g', linestyle='-')
#plt.plot(Kijun.index, Kijun,'b',Tenkan.index,Tenkan,'r',SPANA.index,SPANA,'g',SPANB.index,SPANB,'g')
#plt.plot(y1.index,y1)
#plt.show()

#time_last = time.time()
#res_pro = protect_resist(
						#T_5M=True,T_15M=False,T_1H=False,T_4H=False,T_1D=False,
						#dataset_5M=symbol_data_5M['AUDCAD_i'],
						#dataset_15M=symbol_data_15M['AUDCAD_i'],
						#dataset_1H=symbol_data_1H['AUDCAD_i'],
						#dataset_4H=symbol_data_4H['AUDCAD_i'],
						#dataset_1D=symbol_data_1D['AUDCAD_i'],
						#plot=True
						#)
#print('time left = ',time.time()-time_last)
#print(res_pro['power_high'])
#print('************************ Finish ***************************************')

#//////////////////////////////////////////////////////////////////////////////////

obj = Runner()
print(obj.start)