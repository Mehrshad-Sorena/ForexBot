import pandas as pd

class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{
							
							#*********** Divergence:

							'Divergence' + '_apply_to': 'close',
							'Divergence' + '_symbol': 'XAUUSD_i',
							'Divergence' + '_out_before_buy': pd.DataFrame(),
							'Divergence' + '_out_before_sell': pd.DataFrame(),
							'Divergence' + '_macd_fast': 12,
							'Divergence' + '_macd_slow': 26,
							'Divergence' + '_macd_signal': 9,
							'Divergence' + '_st_percent_buy_max': 0,
							'Divergence' + '_st_percent_buy_min': 0,
							'Divergence' + '_st_percent_sell_max': 0,
							'Divergence' + '_st_percent_sell_min': 0,
							'Divergence' + '_tp_percent_buy_max':0,
							'Divergence' + '_tp_percent_buy_min': 0,
							'Divergence' + '_tp_percent_sell_max': 0,
							'Divergence' + '_tp_percent_sell_min': 0,
							'Divergence' + '_alpha': 0.1,
							'Divergence' + '_num_exteremes_min': 5,
							'Divergence' + '_num_exteremes_max': 5,
							'Divergence' + '_diff_extereme': 6,

							#///////////////////////


							#*********** Global:

							'dataset_5M': pd.DataFrame(),
							'dataset_1H': pd.DataFrame(),

							#//////////////////
							})