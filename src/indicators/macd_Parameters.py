import pandas as pd

class Parameters:

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		return obj

	def __init__(self):

		self.elements = dict(
							{
							
							#*********** Divergence:

							'MACD' + '_apply_to': 'close',

							'MACD' + '_fast': 12,
							'MACD' + '_slow': 26,
							'MACD' + '_signal': 9,

							#///////////////////////


							#ST TP Limits:

							'st_percent_up': 100,
							'st_percent_down': 80,
							'tp_percent_up': 100,
							'tp_percent_down': 80,

							#////////////////////


							#*********** Global:

							'symbol': 'XAUUSD_i',

							#//////////////////
							})