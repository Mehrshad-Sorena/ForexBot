import pandas as pd
import pandas_ta as ind
import numpy as np
import matplotlib.pyplot as plt
import math

from pr_BestFinder import best_extreme_finder
from pr_TrendLines import TrendLines
from pr_FlatLinesIchimoku import flat_lines_ichimoko
from pr_ExtremePoints import ExtremePoints

from pr_Parameters import Parameters
from pr_Config import Config as config

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

	parameters = Parameters()
	config = config()
	#@stTime
	def __init__(
				self,
				parameters,
				config
				):
		self.elements = dict(
							{

							#Elemns For ExtremePoints Module:
							'ExtremePoints_num_max_5M': parameters.elements['ExtremePoints_num_max_5M'],
							'ExtremePoints_num_min_5M': parameters.elements['ExtremePoints_num_min_5M'],
							'ExtremePoints_weight_5M': parameters.elements['ExtremePoints_weight_5M'],

							'ExtremePoints_num_max_1H': parameters.elements['ExtremePoints_num_max_1H'],
							'ExtremePoints_num_min_1H': parameters.elements['ExtremePoints_num_min_1H'],
							'ExtremePoints_weight_1H': parameters.elements['ExtremePoints_weight_1H'],
							#/////////////////////////////////


							#Elemns For TrendingLines Module
							'trend_short_length_1': parameters.elements['trend_short_length_1'],
							'trend_short_length_2': parameters.elements['trend_short_length_2'],
							'trend_mid_length': parameters.elements['trend_mid_length'],
							'trend_long_length': parameters.elements['trend_long_length'],

							'trend_num_max_short_1': parameters.elements['trend_num_max_short_1'],
							'trend_num_min_short_1': parameters.elements['trend_num_min_short_1'],

							'trend_num_max_short_2': parameters.elements['trend_num_max_short_2'],
							'trend_num_min_short_2': parameters.elements['trend_num_min_short_2'],

							'trend_num_max_mid': parameters.elements['trend_num_max_mid'],
							'trend_num_min_mid': parameters.elements['trend_num_min_mid'],
					
							'trend_num_max_long': parameters.elements['trend_num_max_long'],
							'trend_num_min_long': parameters.elements['trend_num_min_long'],
							#/////////////////////////////////


							#Elemns For FlatLinesIchimoku Module:
							'tenkan_5M': parameters.elements['tenkan_5M'],
							'kijun_5M': parameters.elements['kijun_5M'],
							'senkou_5M': parameters.elements['senkou_5M'],
							'culster_ichi_5M': parameters.elements['culster_ichi_5M'],
							'weight_ichi_5M': parameters.elements['weight_ichi_5M'],

							
							'tenkan_1H': parameters.elements['tenkan_1H'],
							'kijun_1H': parameters.elements['kijun_1H'],
							'senkou_1H': parameters.elements['senkou_1H'],
							'culster_ichi_1H': parameters.elements['culster_ichi_1H'],
							'weight_ichi_1H': parameters.elements['weight_ichi_1H'],
							#/////////////////////////////////


							#Elemns For BestFinder Module:
							'n_clusters_best_low': parameters.elements['n_clusters_best_low'],
							'n_clusters_best_high': parameters.elements['n_clusters_best_high'],
							'alpha_low': parameters.elements['alpha_low'],
							'alpha_high': parameters.elements['alpha_high'],
							#/////////////////////////////////


							#Elemns For PrRunner and shared to pr Modules:
							'dataset_5M' :  parameters.elements['dataset_5M'],
							'dataset_1H' :  parameters.elements['dataset_1H'],
							#/////////////////////////////////
							}
							)

		self.cfg = dict(
							{
							#Config For ExtremePoints:
							'ExtremePoints_status': config.cfg['ExtremePoints_status'],
							'ExtremePoints_T_5M': config.cfg['ExtremePoints_T_5M'],
							'ExtremePoints_T_1H': config.cfg['ExtremePoints_T_1H'],
							#/////////////////////////

							
							'plot': config.cfg['plot'],
							}
						)
						


	#This Function Calculate Tp And St With Above Function And Out Best Tp And St With Best_Extreme_Finder:
	def start(self):

		#****************** Extreme Points Finder Function: Finding Top Down Points *********************
		extreme_points = ExtremePoints(parameters = self, config = self)
		
		if (
			self.cfg['ExtremePoints_T_5M'] == True and
			self.cfg['ExtremePoints_status'] == True
			):
			local_extreme_5M = extreme_points.get(timeframe = '5M')
		else:
			local_extreme_5M = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])

		if (
			self.cfg['ExtremePoints_T_1H'] == True and
			self.cfg['ExtremePoints_status'] == True
			):
			local_extreme_1H = extreme_points.get(timeframe = '1H')
		else:
			local_extreme_1H = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])
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