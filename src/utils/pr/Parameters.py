import pandas as pd
class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):
		
		self.number_max_5M = 5
		self.number_min_5M=5
		self.weight_extreme_5M=5

		self.trend_short_length_1=50
		self.trend_short_length_2=50
		self.trend_mid_length=50
		self.trend_long_length=50

		self.trend_num_max_short_1=5
		self.trend_num_min_short_1=5

		self.trend_num_max_short_2=5
		self.trend_num_min_short_2=5

		self.trend_num_max_mid=5
		self.trend_num_min_mid=5
					
		self.trend_num_max_long=5
		self.trend_num_min_long=5

		self.tenkan_5M=9
		self.kijun_5M=26
		self.senkou_5M=52
		self.culster_ichi_5M=5
		self.weight_ichi_5M=400

		self.number_max_1H=5
		self.number_min_1H=5
		self.weight_extreme_1H=30
		self.tenkan_1H=9
		self.kijun_1H=26
		self.senkou_1H=52
		self.culster_ichi_1H=5
		self.weight_ichi_1H=400

		self.n_clusters_best_low=2
		self.n_clusters_best_high=2
		self.alpha_low=0.05
		self.alpha_high=0.05

		self.dataset_5M = pd.DataFrame()
		self.dataset_1H = pd.DataFrame()


		