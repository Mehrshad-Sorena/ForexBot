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
from ExtremePoints import ExtremePoints
import mplfinance as mpf

from pr_Parameters import Parameters
from pr_Config import Config as config

from pr_Tester import Tester

import concurrent.futures


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

							#Elemns For Tester:

							'Tester_money': parameters.elements['Tester_money'],
							'Tester_coef_money': parameters.elements['Tester_coef_money'],
							'Tester_spred': parameters.elements['Tester_spred'],
							'Tester_index_tp': parameters.elements['Tester_index_tp'],
							'Tester_index_st': parameters.elements['Tester_index_st'],

							#////////////////////////////////

							#Elemns Gloal:

							'st_percent_min': parameters.elements['st_percent_min'],
							'st_percent_max': parameters.elements['st_percent_max'],

							'tp_percent_min': parameters.elements['tp_percent_min'],
							'tp_percent_max': parameters.elements['tp_percent_max'],

							#////////////////////////////////
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


							#Config For Tester:

							'Tester_flag_realtest': config.cfg['Tester_flag_realtest'],

							#/////////////////////////
							
							'plot': config.cfg['plot'],
							}
						)
						


	#This Function Calculate Tp And St With Above Function And Out Best Tp And St With Best_Extreme_Finder:
	#@stTime
	def start(self,dataset_5M, dataset_1H, loc_end_5M, sigtype, flaglearn, flagtest):

		if (
			self.elements['Tester_money'] <= 4 and
			flagtest == True and
			flaglearn == True
			):
			extereme = pd.DataFrame(
									{
									'high_upper': np.nan,
									'high_mid': np.nan,
									'high_lower': np.nan,
									'power_high_upper': np.nan,
									'power_high_mid': np.nan,
									'power_high_lower': np.nan,
									'low_upper': np.nan,
									'lowe_mid': np.nan,
									'low_lower': np.nan,
									'power_low_upper': np.nan,
									'power_low_mid': np.nan,
									'power_low_lower': np.nan,
									},
									index = [loc_end_5M]
									)
			if flagtest == True:
				extereme = extereme.assign(
									flag =  np.nan,
									tp_pr = np.nan,
									st_pr = np.nan,
									index_tp = np.nan,
									index_st = np.nan,
									money = np.nan,
									time = np.nan,
									)
			return extereme.values[0]

		if (
			flagtest == True and
			self.cfg['Tester_flag_realtest'] == True
			):
			if (
				loc_end_5M <= self.elements['Tester_index_tp'] or
				loc_end_5M <= self.elements['Tester_index_st']
				):
				extereme = pd.DataFrame(
										{
										'high_upper': np.nan,
										'high_mid': np.nan,
										'high_lower': np.nan,
										'power_high_upper': np.nan,
										'power_high_mid': np.nan,
										'power_high_lower': np.nan,
										'low_upper': np.nan,
										'lowe_mid': np.nan,
										'low_lower': np.nan,
										'power_low_upper': np.nan,
										'power_low_mid': np.nan,
										'power_low_lower': np.nan,
										},
										index = [loc_end_5M]
										)
				if flagtest == True:
					extereme = extereme.assign(
										flag =  np.nan,
										tp_pr = np.nan,
										st_pr = np.nan,
										index_tp = np.nan,
										index_st = np.nan,
										money = np.nan,
										time = np.nan,
										)
				return extereme.values[0]

		loc_end_5M = int(loc_end_5M)

		datachanger = DataChanger()
		self.elements['dataset_' + '5M'], self.elements['dataset_' + '1H'] = datachanger.SpliterSyncPR(
																							dataset_5M = dataset_5M,
																							dataset_1H = dataset_1H,
																							loc_end_5M = loc_end_5M,
																							length_5M = self.elements[__class__.__name__ + '_methode1_' + '_lenght_data_5M'],
																							length_1H = self.elements[__class__.__name__ + '_methode1_' + '_lenght_data_1H']
																							)

		if (
			self.elements['dataset_' + '5M'].empty == True or
			self.elements['dataset_' + '1H'].empty == True or
			len(self.elements['dataset_' + '1H']) <= self.elements['IchimokouFlatLines_senkou_1H'] or
			len(self.elements['dataset_' + '5M']) <= self.elements['IchimokouFlatLines_senkou_5M']
			):
			extereme = pd.DataFrame(
									{
									'high_upper': np.nan,
									'high_mid': np.nan,
									'high_lower': np.nan,
									'power_high_upper': np.nan,
									'power_high_mid': np.nan,
									'power_high_lower': np.nan,
									'low_upper': np.nan,
									'lowe_mid': np.nan,
									'low_lower': np.nan,
									'power_low_upper': np.nan,
									'power_low_mid': np.nan,
									'power_low_lower': np.nan,
									},
									index = [loc_end_5M]
									)
			if flagtest == True:
				extereme = extereme.assign(
									flag =  np.nan,
									tp_pr = np.nan,
									st_pr = np.nan,
									index_tp = np.nan,
									index_st = np.nan,
									money = np.nan,
									time = np.nan,
									)
			return extereme.values[0]
		

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
										timeframe = '5M',
										loc_end_5M = loc_end_5M
										)
		except Exception as ex:
			extereme = pd.DataFrame(
									{
									'high_upper': np.nan,
									'high_mid': np.nan,
									'high_lower': np.nan,
									'power_high_upper': np.nan,
									'power_high_mid': np.nan,
									'power_high_lower': np.nan,
									'low_upper': np.nan,
									'lowe_mid': np.nan,
									'low_lower': np.nan,
									'power_low_upper': np.nan,
									'power_low_mid': np.nan,
									'power_low_lower': np.nan,
									},
									index = [loc_end_5M]
									)

		#Add Name Of Trends To OutPut DataFrame:
		# if self.cfg['TrendLines_long_T_5M'] == True:
		# 	extereme['trend_long'] = [trend_5M_long['trend'][0]]

		# if self.cfg['TrendLines_mid_T_5M'] == True:
		# 	extereme['trend_mid'] = [trend_5M_mid['trend'][0]]
			
		# if self.cfg['TrendLines_short1_T_5M'] == True:
		# 	extereme['trend_short1'] = [trend_5M_short1['trend'][0]]

		# if self.cfg['TrendLines_short2_T_5M'] == True:
		# 	extereme['trend_short2'] = [trend_5M_short2['trend'][0]]

		if (
			sigtype == 'buy' and
			flagtest == True
			):
			
			tester = Tester(parameters = self, config = self)
			extereme = tester.FlagFinderBuy(
											dataset_5M = dataset_5M, 
											extereme = extereme, 
											flaglearn = flaglearn, 
											loc_end_5M = loc_end_5M, 
											money = self.elements['Tester_money']
											)

			self.elements['Tester_money'] = extereme['money'][loc_end_5M]



			if extereme['flag'][loc_end_5M] == 'tp':
				self.elements['Tester_index_tp'] = extereme['index_tp'][loc_end_5M]
				self.elements['Tester_index_st'] = extereme['index_tp'][loc_end_5M]
			elif extereme['flag'][loc_end_5M] == 'st':
				self.elements['Tester_index_tp'] = extereme['index_st'][loc_end_5M]
				self.elements['Tester_index_st'] = extereme['index_st'][loc_end_5M]

		elif (
			sigtype == 'sell' and
			flagtest == True
			):

			tester = Tester(parameters = self, config = self)
			extereme = tester.FlagFinderSell(
											dataset_5M = dataset_5M, 
											extereme = extereme, 
											flaglearn = flaglearn, 
											loc_end_5M = loc_end_5M, 
											money = self.elements['Tester_money']
											)

			self.elements['Tester_money'] = extereme['money'][loc_end_5M]

			if extereme['flag'][loc_end_5M] == 'tp':
				self.elements['Tester_index_tp'] = extereme['index_tp'][loc_end_5M]
				self.elements['Tester_index_st'] = extereme['index_tp'][loc_end_5M]
			elif extereme['flag'][loc_end_5M] == 'st':
				self.elements['Tester_index_tp'] = extereme['index_st'][loc_end_5M]
				self.elements['Tester_index_st'] = extereme['index_st'][loc_end_5M]
			

		return extereme.values[0]
	#/////////////////////////////

	def run(self, signals, dataset_5M, dataset_1H, sigtype, flaglearn, flagtest):

		if flagtest == False:
			pr = signals.apply(
								lambda x: pd.Series(
													self.start(
																dataset_5M = dataset_5M, 
																dataset_1H = dataset_1H,
																loc_end_5M = x['index'],
																sigtype = sigtype,
																flaglearn = flaglearn,
																flagtest = flagtest
																), 
																index = ['high_upper', 'high_mid', 'high_lower', 'power_high_upper', 
																		'power_high_mid', 'power_high_lower', 'low_upper', 'lowe_mid', 
																		'low_lower','power_low_upper', 'power_low_mid', 'power_low_lower']
													),
								axis = 1,
								result_type = 'expand'
								)

		else:

			pr = signals.apply(
								lambda x: pd.Series(
													self.start(
																dataset_5M = dataset_5M, 
																dataset_1H = dataset_1H,
																loc_end_5M = x['index'],
																sigtype = sigtype,
																flaglearn = flaglearn,
																flagtest = flagtest
																), 
																index = ['high_upper', 'high_mid', 'high_lower', 'power_high_upper', 
																		'power_high_mid', 'power_high_lower', 'low_upper', 'lowe_mid', 
																		'low_lower','power_low_upper', 'power_low_mid', 'power_low_lower',
																		'flag','tp_pr','st_pr','index_tp','index_st','money','time']
													),
								axis = 1,
								result_type = 'expand'
								)

		signals = signals.join(pr)

		return signals

	#////////////////////////////////////


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