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


							#*********** Global:

							'symbol': 'XAUUSD_i',

							#//////////////////
							})