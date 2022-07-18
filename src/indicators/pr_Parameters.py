import pandas as pd
class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{
							#Elemns For ExtremePoints Module:
							'ExtremePoints_num_max_5M': 5,
							'ExtremePoints_num_min_5M': 5,
							'ExtremePoints_weight_5M': 5,

							'ExtremePoints_num_max_1H': 5,
							'ExtremePoints_num_min_1H': 5,
							'ExtremePoints_weight_1H': 30,
							#/////////////////////////////////


							#Elemns For TrendingLines Module
							'trend_short_length_1': 25,
							'trend_short_length_2': 50,
							'trend_mid_length': 100,
							'trend_long_length': 200,

							'trend_num_max_short_1': 5,
							'trend_num_min_short_1': 5,

							'trend_num_max_short_2': 5,
							'trend_num_min_short_2': 5,

							'trend_num_max_mid': 5,
							'trend_num_min_mid': 5,
					
							'trend_num_max_long': 5,
							'trend_num_min_long': 5,
							#/////////////////////////////////


							#Elemns For FlatLinesIchimoku Module:
							'tenkan_5M': 9,
							'kijun_5M': 26,
							'senkou_5M': 52,
							'culster_ichi_5M': 5,
							'weight_ichi_5M': 400,

							
							'tenkan_1H': 9,
							'kijun_1H': 26,
							'senkou_1H': 52,
							'culster_ichi_1H': 5,
							'weight_ichi_1H': 400,
							#/////////////////////////////////


							#Elemns For BestFinder Module:
							'n_clusters_best_low': 2,
							'n_clusters_best_high': 2,
							'alpha_low': 0.05,
							'alpha_high': 0.05,
							#/////////////////////////////////


							#Elemns For PrRunner and shared to pr Modules:
							'dataset_5M' :  pd.DataFrame(),
							'dataset_1H' :  pd.DataFrame(),
							#/////////////////////////////////
							}
							)

# parameters = Parameters()
# parameters.elements['num'] = 100
# from log_get_data import *
# import MetaTrader5 as mt5
# import sys

# data_5M,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)
# data_1H,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,500)

# parameters = Parameters()
# parameters.elements['dataset_5M'] = pd.DataFrame(data_5M['XAUUSD_i'])
# parameters.elements['dataset_1H'] = pd.DataFrame(data_1H['XAUUSD_i'])
# print(parameters.elements['dataset_5M'])


		