class ParameterLimits:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{

							#Chromosome Limit Parameters:

							'MACD_fast_upper': 144,#800,
							'MACD_fast_lower': 4,

							'MACD_slow_upper': 312,#1500,
							'MACD_slow_lower': 4,

							'MACD_signal_upper': 50,
							'MACD_signal_lower': 4,
							
							'Divergence_num_exteremes_min_upper': 100,#250,
							'Divergence_num_exteremes_min_lower': 2,

							'Divergence_num_exteremes_max_upper': 100,#250,
							'Divergence_num_exteremes_max_lower': 2,

							'BestFinder_n_clusters_upper': 20,#50,
							'BestFinder_n_clusters_lower': 1,

							'BestFinder_alpha_upper': 40,#99,
							'BestFinder_alpha_lower': 1,

							'Runner_methode1__lenght_data_5M_upper': 3000,
							'Runner_methode1__lenght_data_5M_lower': 200,#20,

							'Runner_methode1__lenght_data_1H_upper': 1000,
							'Runner_methode1__lenght_data_1H_lower': 200,#20,
							
							'ExtremePoints_num_max_5M_upper': 100,#250,
							'ExtremePoints_num_max_5M_lower': 2,

							'ExtremePoints_num_min_5M_upper': 100,#250,
							'ExtremePoints_num_min_5M_lower': 2,

							'ExtremePoints_weight_5M_upper': 1000,
							'ExtremePoints_weight_5M_lower': 2,

							'ExtremePoints_num_max_1H_upper': 100,#250,
							'ExtremePoints_num_max_1H_lower': 2,

							'ExtremePoints_num_min_1H_upper': 100,#250,
							'ExtremePoints_num_min_1H_lower': 2,

							'ExtremePoints_weight_1H_upper': 1000,
							'ExtremePoints_weight_1H_lower': 2,

							'TrendLines_num_max_5M_upper': 100,#250,
							'TrendLines_num_max_5M_lower': 2,

							'TrendLines_num_min_5M_upper': 100,#250,
							'TrendLines_num_min_5M_lower': 2,

							'TrendLines_weight_5M_upper': 1000,
							'TrendLines_weight_5M_lower': 2,

							'TrendLines_num_max_1H_upper': 100,#250,
							'TrendLines_num_max_1H_lower': 2,

							'TrendLines_num_min_1H_upper': 100#,250,
							'TrendLines_num_min_1H_lower': 2,

							'TrendLines_weight_1H_upper': 1000,
							'TrendLines_weight_1H_lower': 2,

							'TrendLines_length_long_5M_upper': 1000,
							'TrendLines_length_long_5M_lower': 10,

							'TrendLines_length_mid_5M_upper': 1000,
							'TrendLines_length_mid_5M_lower': 10,

							'TrendLines_length_short1_5M_upper': 500,
							'TrendLines_length_short1_5M_lower': 5,

							'TrendLines_length_short2_5M_upper': 500,
							'TrendLines_length_short2_5M_lower': 5,

							'TrendLines_length_long_1H_upper': 1000,
							'TrendLines_length_long_1H_lower': 10,

							'TrendLines_length_mid_1H_upper': 1000,
							'TrendLines_length_mid_1H_lower': 10,

							'TrendLines_length_short1_1H_upper': 500,
							'TrendLines_length_short1_1H_lower': 5,

							'TrendLines_length_short2_1H_upper': 500,
							'TrendLines_length_short2_1H_lower': 5,

							'TrendLines_power_long_5M_upper': 1000,
							'TrendLines_power_long_5M_lower': 2,

							'TrendLines_power_mid_5M_upper': 1000,
							'TrendLines_power_mid_5M_lower': 2,

							'TrendLines_power_short1_5M_upper': 1000,
							'TrendLines_power_short1_5M_lower': 2,

							'TrendLines_power_short2_5M_upper': 1000,
							'TrendLines_power_short2_5M_lower': 2,

							'TrendLines_power_long_1H_upper': 1000,
							'TrendLines_power_long_1H_lower': 2,

							'TrendLines_power_mid_1H_upper': 1000,
							'TrendLines_power_mid_1H_lower': 2,

							'TrendLines_power_short1_1H_upper': 1000,
							'TrendLines_power_short1_1H_lower': 2,

							'TrendLines_power_short2_1H_upper': 1000,
							'TrendLines_power_short2_1H_lower': 2,

							'IchimokouFlatLines_tenkan_5M_upper': 108,#500,
							'IchimokouFlatLines_tenkan_5M_lower': 2,

							'IchimokouFlatLines_kijun_5M_upper': 312,#1400,
							'IchimokouFlatLines_kijun_5M_lower': 2,

							'IchimokouFlatLines_senkou_5M_upper': 624,#2500,
							'IchimokouFlatLines_senkou_5M_lower': 2,

							'IchimokouFlatLines_n_cluster_5M_upper': 20,#50,
							'IchimokouFlatLines_n_cluster_5M_lower': 1,

							'IchimokouFlatLines_weight_5M_upper': 1000,
							'IchimokouFlatLines_weight_5M_lower': 2,

							'IchimokouFlatLines_tenkan_1H_upper': 50,
							'IchimokouFlatLines_tenkan_1H_lower': 2,

							'IchimokouFlatLines_kijun_1H_upper': 110,
							'IchimokouFlatLines_kijun_1H_lower': 2,

							'IchimokouFlatLines_senkou_1H_upper': 210,
							'IchimokouFlatLines_senkou_1H_lower': 2,

							'IchimokouFlatLines_n_cluster_1H_upper': 20,#50,
							'IchimokouFlatLines_n_cluster_1H_lower': 1,

							'IchimokouFlatLines_weight_1H_upper': 1000,
							'IchimokouFlatLines_weight_1H_lower': 1,

							'BestFinder_n_cluster_low_upper': 25,#50,
							'BestFinder_n_cluster_low_lower': 1,

							'BestFinder_n_cluster_high_upper': 25,#50,
							'BestFinder_n_cluster_high_lower': 1,

							'BestFinder_alpha_low_upper': 40,#99,
							'BestFinder_alpha_low_lower': 1,

							'BestFinder_alpha_high_upper': 40,#99,
							'BestFinder_alpha_high_lower': 1,


							#///////////////////////////
							})