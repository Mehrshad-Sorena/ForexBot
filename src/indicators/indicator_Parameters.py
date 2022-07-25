import pandas as pd

class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{
							
							#*********** Divergence:

							'Divergence' + '_num_exteremes_min': 5,
							'Divergence' + '_num_exteremes_max': 5,

							'Divergence' + '_diff_extereme': 6,

							#///////////////////////

							#BestFinder:

							'BestFinder' + '_n_clusters': 5,
							'BestFinder' + '_alpha': 0.1,

							#//////////////////////


							#*********** Global:

							'symbol': 'XAUUSD_i',
							'dataset_5M': pd.DataFrame(),
							'dataset_1H': pd.DataFrame(),

							#//////////////////
							})