from macd_Parameters import Parameters
from macd_Config import Config
import pandas_ta as ind
import pandas as pd

class MACD:

	parameters = Parameters()
	config = Config()
	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({
							#*********************

							__class__.__name__ + '_fast': parameters.elements[__class__.__name__ + '_fast'],
							__class__.__name__ + '_slow': parameters.elements[__class__.__name__ + '_slow'],
							__class__.__name__ + '_signal': parameters.elements[__class__.__name__ + '_signal'],

							__class__.__name__ + '_apply_to': parameters.elements[__class__.__name__ + '_apply_to'],

							'symbol': parameters.elements['symbol'],

							#///////////////////////

							#Globals:

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],

							#/////////////////////////
							})

		self.cfg = dict({

						})


	def calculator_macd(self):

		symbol = self.elements['symbol']
		apply_to = self.elements[__class__.__name__ + '_apply_to']
		macd_read = ind.macd(
							self.elements['dataset_5M'][symbol][apply_to],
							fast = self.elements[__class__.__name__ + '_fast'],
							slow = self.elements[__class__.__name__ + '_slow'],
							signal = self.elements[__class__.__name__ + '_signal']
							)

		column_macds = macd_read.columns[2]
		column_macd = macd_read.columns[0]
		column_macdh = macd_read.columns[1]

		macd = pd.DataFrame(
							{
								'macds': macd_read[column_macds],
								'macd': macd_read[column_macd],
								'macdh': macd_read[column_macdh],
							}
							).dropna(inplace = False)
		
		return macd