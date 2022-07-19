import matplotlib.pyplot as plt
from timer import stTime
import pandas as pd
import numpy as np
#import math
import matplotlib.pyplot as plt
from DataChanger import DataChanger
from pr_BestFinder import BestFinder
from pr_TrendLines import TrendLines
from pr_IchimokouFlatLines import IchimokouFlatLines
from pr_ExtremePoints import ExtremePoints
import mplfinance as mpf

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
							#Elemns For Runner Module:

							__class__.__name__ + '_methode1_' + '_lenght_data_5M': parameters.elements[__class__.__name__ + '_methode1_' + '_lenght_data_5M'],
							__class__.__name__ + '_methode1_' + '_lenght_data_1H': parameters.elements[__class__.__name__ + '_methode1_' + '_lenght_data_1H'],

							#/////////////////////////////////


							#Elemns For ExtremePoints Module:

							'ExtremePoints_num_max_5M': parameters.elements['ExtremePoints_num_max_5M'],
							'ExtremePoints_num_min_5M': parameters.elements['ExtremePoints_num_min_5M'],
							'ExtremePoints_weight_5M': parameters.elements['ExtremePoints_weight_5M'],

							'ExtremePoints_num_max_1H': parameters.elements['ExtremePoints_num_max_1H'],
							'ExtremePoints_num_min_1H': parameters.elements['ExtremePoints_num_min_1H'],
							'ExtremePoints_weight_1H': parameters.elements['ExtremePoints_weight_1H'],

							#/////////////////////////////////


							#Elemns For TrendingLines Module

							'TrendLines_num_max_5M': parameters.elements['TrendLines_num_max_5M'],
							'TrendLines_num_min_5M': parameters.elements['TrendLines_num_min_5M'],
							'TrendLines_weight_5M': parameters.elements['TrendLines_weight_5M'],

							'TrendLines_num_max_1H': parameters.elements['TrendLines_num_max_1H'],
							'TrendLines_num_min_1H': parameters.elements['TrendLines_num_min_1H'],
							'TrendLines_weight_1H': parameters.elements['TrendLines_weight_1H'],

							'TrendLines_length_long_5M': parameters.elements['TrendLines_length_long_5M'],
							'TrendLines_length_mid_5M': parameters.elements['TrendLines_length_mid_5M'],
							'TrendLines_length_short1_5M': parameters.elements['TrendLines_length_short1_5M'],
							'TrendLines_length_short2_5M': parameters.elements['TrendLines_length_short2_5M'],
							
							'TrendLines_length_long_1H': parameters.elements['TrendLines_length_long_1H'],
							'TrendLines_length_mid_1H': parameters.elements['TrendLines_length_mid_1H'],
							'TrendLines_length_short1_1H': parameters.elements['TrendLines_length_short1_1H'],
							'TrendLines_length_short2_1H': parameters.elements['TrendLines_length_short2_1H'],

							'TrendLines_power_long_5M': parameters.elements['TrendLines_power_long_5M'],
							'TrendLines_power_mid_5M': parameters.elements['TrendLines_power_mid_5M'],
							'TrendLines_power_short1_5M': parameters.elements['TrendLines_power_short1_5M'],
							'TrendLines_power_short2_5M': parameters.elements['TrendLines_power_short2_5M'],
							
							'TrendLines_power_long_1H': parameters.elements['TrendLines_power_long_1H'],
							'TrendLines_power_mid_1H': parameters.elements['TrendLines_power_mid_1H'],
							'TrendLines_power_short1_1H': parameters.elements['TrendLines_power_short1_1H'],
							'TrendLines_power_short2_1H': parameters.elements['TrendLines_power_short2_1H'],

							#/////////////////////////////////


							#Elemns For IchimokuFlatLines Module:
							
							'IchimokouFlatLines_tenkan_5M': parameters.elements['IchimokouFlatLines_tenkan_5M'],
							'IchimokouFlatLines_kijun_5M': parameters.elements['IchimokouFlatLines_kijun_5M'],
							'IchimokouFlatLines_senkou_5M': parameters.elements['IchimokouFlatLines_senkou_5M'],

							'IchimokouFlatLines_n_cluster_5M': parameters.elements['IchimokouFlatLines_n_cluster_5M'],

							'IchimokouFlatLines_weight_5M': parameters.elements['IchimokouFlatLines_weight_5M'],

							'IchimokouFlatLines_tenkan_1H': parameters.elements['IchimokouFlatLines_tenkan_1H'],
							'IchimokouFlatLines_kijun_1H': parameters.elements['IchimokouFlatLines_kijun_1H'],
							'IchimokouFlatLines_senkou_1H': parameters.elements['IchimokouFlatLines_senkou_1H'],

							'IchimokouFlatLines_n_cluster_1H': parameters.elements['IchimokouFlatLines_n_cluster_1H'],

							'IchimokouFlatLines_weight_1H': parameters.elements['IchimokouFlatLines_weight_1H'],

							#/////////////////////////////////


							#Elemns For BestFinder Module:

							'BestFinder_n_cluster_low': parameters.elements['BestFinder_n_cluster_low'],
							'BestFinder_n_cluster_high': parameters.elements['BestFinder_n_cluster_high'],

							'BestFinder_alpha_low': parameters.elements['BestFinder_alpha_low'],
							'BestFinder_alpha_high': parameters.elements['BestFinder_alpha_high'],

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

							#Config For TrendLines:
							'TrendLines_status': config.cfg['TrendLines_status'],
							
							'TrendLines_T_5M': config.cfg['TrendLines_T_5M'],

							'TrendLines_long_T_5M': config.cfg['TrendLines_long_T_5M'],
							'TrendLines_mid_T_5M': config.cfg['TrendLines_mid_T_5M'],
							'TrendLines_short1_T_5M': config.cfg['TrendLines_short1_T_5M'],
							'TrendLines_short2_T_5M': config.cfg['TrendLines_short2_T_5M'],

							'TrendLines_T_1H': config.cfg['TrendLines_T_1H'],

							'TrendLines_long_T_1H': config.cfg['TrendLines_long_T_1H'],
							'TrendLines_mid_T_1H': config.cfg['TrendLines_mid_T_1H'],
							'TrendLines_short1_T_1H': config.cfg['TrendLines_short1_T_1H'],
							'TrendLines_short2_T_1H': config.cfg['TrendLines_short2_T_1H'],

							'TrendLines_plot': config.cfg['TrendLines_plot'],
							#///////////////////////////

							#Config For IchimokouFlatLines:

							'IchimokouFlatLines_T_5M': config.cfg['IchimokouFlatLines_T_5M'],
							'IchimokouFlatLines_T_1H': config.cfg['IchimokouFlatLines_T_1H'],
							'IchimokouFlatLines_status': config.cfg['IchimokouFlatLines_status'],

							'IchimokouFlatLines_plot': config.cfg['IchimokouFlatLines_plot'],

							#//////////////////////////


							
							'plot': config.cfg['plot'],
							}
						)
						


	#This Function Calculate Tp And St With Above Function And Out Best Tp And St With Best_Extreme_Finder:
	@stTime
	def start(self,dataset_5M,dataset_1H,loc_end_5M):

		datachanger = DataChanger()
		self.elements['dataset_' + '5M'], self.elements['dataset_' + '1H'] = datachanger.SpliterSyncPR(
																							dataset_5M = dataset_5M,
																							dataset_1H = dataset_1H,
																							loc_end_5M = loc_end_5M,
																							length_5M = self.elements[__class__.__name__ + '_methode1_' + '_lenght_data_5M'],
																							length_1H = self.elements[__class__.__name__ + '_methode1_' + '_lenght_data_1H']
																							)
		

		#****************** Extreme Points Finder Function: Finding Top Down Points *********************
		extreme_points = ExtremePoints(parameters = self, config = self)
		
		extreme_5M = extreme_points.runner(timeframe = '5M')
		extreme_1H = extreme_points.runner(timeframe = '1H')

		#//////////////////////////////////////////////////////////////////////////////////////////////////



		#**************************** Trend Line Extreme Finder Function **************************************

		trendlines = TrendLines(parameters = self, config = self)

		trend_5M_long, trend_5M_mid, trend_5M_short1, trend_5M_short2  = trendlines.runner(timeframe='5M')
		trend_1H_long, trend_1H_mid, trend_1H_short1, trend_1H_short2  = trendlines.runner(timeframe='1H')

		#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		#*************************************** ichi Extreme Finder Function ********************************************************
		
		ichiflatlines = IchimokouFlatLines(parameters = self, config = self)
		ichi_lines_5M = ichiflatlines.get(timeframe='5M')
		ichi_lines_1H = ichiflatlines.get(timeframe='1H')
		#//////////////////////////////////////////////////////////////////////////////////////////////////////////

		#***************** Concatenate All of Extremes That Finded **************************

		exterm_point = pd.DataFrame(
									np.concatenate(
												(
												extreme_5M['extreme'].to_numpy(), 
												extreme_1H['extreme'].to_numpy(),

												trend_5M_long['min'].to_numpy(),
												trend_5M_long['max'].to_numpy(),
												trend_5M_mid['min'].to_numpy(),
												trend_5M_mid['max'].to_numpy(),
												trend_5M_short1['min'].to_numpy(),
												trend_5M_short1['max'].to_numpy(),
												trend_5M_short2['min'].to_numpy(),
												trend_5M_short2['max'].to_numpy(),

												trend_1H_long['min'].to_numpy(),
												trend_1H_long['max'].to_numpy(),
												trend_1H_mid['min'].to_numpy(),
												trend_1H_mid['max'].to_numpy(),
												trend_1H_short1['min'].to_numpy(),
												trend_1H_short1['max'].to_numpy(),
												trend_1H_short2['min'].to_numpy(),
												trend_1H_short2['max'].to_numpy(),

												ichi_lines_5M['extreme'].to_numpy(),
												ichi_lines_1H['extreme'].to_numpy(),
												), 
												axis=None
												),
									columns=['extremes']
									)

		exterm_point['power'] = np.concatenate(
											(
											extreme_5M['power'].to_numpy(), 
											extreme_1H['power'].to_numpy(),

											trend_5M_long['power'].to_numpy(),
											trend_5M_long['power'].to_numpy(),
											trend_5M_mid['power'].to_numpy(),
											trend_5M_mid['power'].to_numpy(),
											trend_5M_short1['power'].to_numpy(),
											trend_5M_short1['power'].to_numpy(),
											trend_5M_short2['power'].to_numpy(),
											trend_5M_short2['power'].to_numpy(),

											trend_1H_long['power'].to_numpy(),
											trend_1H_long['power'].to_numpy(),
											trend_1H_mid['power'].to_numpy(),
											trend_1H_mid['power'].to_numpy(),
											trend_1H_short1['power'].to_numpy(),
											trend_1H_short1['power'].to_numpy(),
											trend_1H_short2['power'].to_numpy(),
											trend_1H_short2['power'].to_numpy(),

											ichi_lines_5M['power'].to_numpy(),
											ichi_lines_1H['power'].to_numpy(),
											), 
											axis=None
											)
		#Delete Nan Data:
		exterm_point = exterm_point.dropna()

		#Using Best Extreme Finder To Find Best Tp And St Points:
		bestfinder = BestFinder(parameters = self, config = self)
		
		try:
			extereme = bestfinder.finder(
										extermpoint = exterm_point,
										timeframe = '5M'
										)
		except Exception as ex:
			extereme = pd.DataFrame()
			extereme['high'] = [0, 0, 0]
			extereme['power_high'] = [0, 0, 0]
			extereme['low'] = [0, 0, 0]
			extereme['power_low'] = [0, 0, 0]

		#Add Name Of Trends To OutPut DataFrame:
		if self.cfg['TrendLines_long_T_5M'] == True:
			extereme['trend_long'] = [
									trend_5M_long['trend'][0],
									trend_5M_long['trend'][0],
									trend_5M_long['trend'][0]
									]
		if self.cfg['TrendLines_mid_T_5M'] == True:
			extereme['trend_mid'] = [
									trend_5M_mid['trend'][0],
									trend_5M_mid['trend'][0],
									trend_5M_mid['trend'][0]
									]
		if self.cfg['TrendLines_short1_T_5M'] == True:
			extereme['trend_short1'] = [
										trend_5M_short1['trend'][0],
										trend_5M_short1['trend'][0],
										trend_5M_short1['trend'][0]
										]
		if self.cfg['TrendLines_short2_T_5M'] == True:
			extereme['trend_short2'] = [
										trend_5M_short2['trend'][0],
										trend_5M_short2['trend'][0],
										trend_5M_short2['trend'][0]
										]

		return extereme
	#/////////////////////////////


	#************* Ploter
	def ploter(self,dataset_5M,dataset_1H,loc_end_5M):
		



		if self.cfg['plot'] == True:

			extereme = self.start(dataset_5M = dataset_5M, dataset_1H = dataset_1H, loc_end_5M = loc_end_5M)

			dataset = self.elements['dataset_5M'].copy(deep = True)
			dataset.index.name = 'Time'
			dataset.index = self.elements['dataset_5M'].time
			dataset.head(3)
			dataset.tail(3)

			mc = mpf.make_marketcolors(
										base_mpf_style='yahoo',
										up='green',
										down='red',
										vcdopcod = True,
										alpha = 0.0001
										)
			mco = [mc]*len(dataset)

			low_1 = float(extereme.low.values[0])
			low_2 = float(extereme.low.values[1])
			low_3 = float(extereme.low.values[2])

			high_1 = float(extereme.high.values[0])
			high_2 = float(extereme.high.values[1])
			high_3 = float(extereme.high.values[2])

			mpf.plot(
					dataset,
					type='candle',
					volume=True,
					style='yahoo',
					figscale=1,
					title='5M Protect Resist',
					hlines=dict(hlines=[low_1,low_2,low_3,high_1,high_2,high_3],colors=['g', 'r', 'g', 'b', 'r', 'b'],linestyle='-.'),
					#if config.savefig_5M savefig=dict(fname=config.path_5M,dpi=600,pad_inches=0.25) else None,
					marketcolor_overrides=mco
					)
			#plt.axhline(y = extereme['high'][0], color = 'r', linestyle = '-')
			#plt.axhline(y = extereme['high'][1], color = 'g', linestyle = '-')
			#plt.axhline(y = extereme['high'][2], color = 'r', linestyle = '-')

			# plt.axhline(y = extereme['low'][0], color = 'g', linestyle = '-')
			# plt.axhline(y = extereme['low'][1], color = 'b', linestyle = '-')
			# plt.axhline(y = extereme['low'][2], color = 'g', linestyle = '-')

			# end = len(dataset_5M['close']) - 1

			# #plt.axvline(x = end, color = 'r', linestyle = '-')

			# plt.plot(dataset_5M['close'].index[end-100:end],dataset_5M['close'][end-100:end],'b')
			# plt.show()
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