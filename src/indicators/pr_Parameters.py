import pandas as pd


class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{

							#Elemns For Runner Module:

							'Runner' + '_methode1_' + '_lenght_data_5M': 600,
							'Runner' + '_methode1_' + '_lenght_data_1H': 500,

							#//////////////////////////////

							#Elemns For ExtremePoints Module:
							'ExtremePoints_num_max_5M': 5,
							'ExtremePoints_num_min_5M': 5,
							'ExtremePoints_weight_5M': 5,

							'ExtremePoints_num_max_1H': 5,
							'ExtremePoints_num_min_1H': 5,
							'ExtremePoints_weight_1H': 30,
							#/////////////////////////////////


							#Elemns For TrendingLines Module
							'TrendLines_num_max_5M': 5,
							'TrendLines_num_min_5M': 5,
							'TrendLines_weight_5M': 5,

							'TrendLines_num_max_1H': 5,
							'TrendLines_num_min_1H': 5,
							'TrendLines_weight_1H': 30,

							'TrendLines' + '_length_long_5M': 400,
							'TrendLines' + '_length_mid_5M': 200,
							'TrendLines' + '_length_short1_5M': 50,
							'TrendLines' + '_length_short2_5M': 25,
							
							'TrendLines' + '_length_long_1H': 200,
							'TrendLines' + '_length_mid_1H': 200,
							'TrendLines' + '_length_short1_1H': 50,
							'TrendLines' + '_length_short2_1H': 25,

							'TrendLines' + '_power_long_5M': 400,
							'TrendLines' + '_power_mid_5M': 200,
							'TrendLines' + '_power_short1_5M': 100,
							'TrendLines' + '_power_short2_5M': 100,
							
							'TrendLines' + '_power_long_1H': 400,
							'TrendLines' + '_power_mid_1H': 200,
							'TrendLines' + '_power_short1_1H': 100,
							'TrendLines' + '_power_short2_1H': 100,
							#/////////////////////////////////


							#Elemns For FlatLinesIchimoku Module:

							'IchimokouFlatLines' + '_tenkan_5M': 9,
							'IchimokouFlatLines' + '_kijun_5M': 26,
							'IchimokouFlatLines' + '_senkou_5M': 52,

							'IchimokouFlatLines' + '_n_cluster_5M': 4,

							'IchimokouFlatLines' + '_weight_5M': 200,

							'IchimokouFlatLines' + '_tenkan_1H': 9,
							'IchimokouFlatLines' + '_kijun_1H': 26,
							'IchimokouFlatLines' + '_senkou_1H': 52,

							'IchimokouFlatLines' + '_n_cluster_1H': 4,

							'IchimokouFlatLines' + '_weight_1H': 400,

							#/////////////////////////////////


							#Elemns For BestFinder Module:
							'BestFinder' + '_n_cluster_low': 5,
							'BestFinder' + '_n_cluster_high': 5,

							'BestFinder' + '_alpha_low': 0.1,
							'BestFinder' + '_alpha_high': 0.1,

							'n_clusters_best_low': 2,
							'n_clusters_best_high': 2,
							'alpha_low': 0.05,
							'alpha_high': 0.05,
							#/////////////////////////////////


							#Elemns For PrRunner and shared to pr Modules:

							'dataset_5M' :  pd.DataFrame(),
							'dataset_1H' :  pd.DataFrame(),

							#/////////////////////////////////

							#Elemns For Tester:

							'Tester_money': 100,
							'Tester_coef_money': 20,
							'Tester_spred': 0.0004,
							'Tester_index_tp': 0,
							'Tester_index_st': 0,

							'st_percent_min': 1,
							'st_percent_max': 1,

							'tp_percent_min': 1,
							'tp_percent_max': 1,

							#//////////////////
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


		