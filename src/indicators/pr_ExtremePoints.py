from scipy.signal import argrelextrema
#import src.utils.pr
from pr_Parameters import Parameters
from pr_Config import Config

import matplotlib.pyplot as plt
import warnings as warnings
import mplfinance as mpf
import pandas as pd
import numpy as np
import sys
warnings.filterwarnings("ignore")


#getattr(self,'dataset_' + timeframe)
#**************************************************** extreme High Or Low Lines *******************************************************
#This function is Used For Finding Extremes Top Downs in Candles:
class ExtremePoints:

	parameters = Parameters()
	config = Config()

	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict(
							{
							__class__.__name__  + '_num_max_5M': parameters.elements[__class__.__name__  + '_num_max_5M'],
							__class__.__name__  + '_num_min_5M': parameters.elements[__class__.__name__  + '_num_min_5M'],

							__class__.__name__  + '_num_max_1H': parameters.elements[__class__.__name__  + '_num_max_1H'],
							__class__.__name__  + '_num_min_1H': parameters.elements[__class__.__name__  + '_num_min_1H'],

							__class__.__name__  + '_weight_5M': parameters.elements[__class__.__name__  + '_weight_5M'],
							__class__.__name__  + '_weight_1H': parameters.elements[__class__.__name__  + '_weight_1H'],

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],
							}
							)

		self.cfg = dict(
						{
						__class__.__name__  + '_T_5M': config.cfg[__class__.__name__  + '_T_5M'],
						__class__.__name__  + '_T_1H': config.cfg[__class__.__name__  + '_T_1H'],
						__class__.__name__  + '_status': config.cfg[__class__.__name__  + '_status'],
						}
						)


	def finder(
				self,
				high,
				low,
				number_min,
				number_max
				):

		extremes = pd.DataFrame(low, columns=['low'])
		extremes['high'] = high

		#Finding Extreme Points
		#Finding Minimum Points:
		extremes['min'] = extremes.iloc[
										argrelextrema(
														extremes.low.values, 
														comparator = np.less,
														order = number_min
														)[0]
										]['low']

		#Finding Maximum Points:
		extremes['max'] = extremes.iloc[
										argrelextrema(
														extremes.high.values, 
														comparator = np.greater,
														order = number_max
														)[0]
										]['high']

		#Concatenate Max And Min Points to One DataFrame:
		exterm_point = pd.DataFrame(
									np.concatenate(
													(
														extremes['max'].dropna().to_numpy(),
														extremes['min'].dropna().to_numpy()
													),
													axis=None
													),columns=['extreme']
									)

		return exterm_point


	def get(self, timeframe):

		#Finding Extremes From Time Frame
		local_extreme = pd.DataFrame()
		local_extreme['extreme'] = np.nan
		local_extreme['power'] = np.nan
		
		if (
			self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
			self.cfg[__class__.__name__ + '_status'] == True
			):
			local_extreme['extreme'] = pd.DataFrame(
														self.finder(
																	high = self.elements['dataset_' + timeframe].high,
																	low = self.elements['dataset_' + timeframe].low,
																	number_min = self.elements[__class__.__name__ + '_num_min_' + timeframe],
																	number_max = self.elements[__class__.__name__ + '_num_max_' + timeframe]
																	).extreme
														)

			local_extreme['power'] = np.ones(len(local_extreme)) * self.elements[__class__.__name__ + '_weight_' + timeframe]

		return local_extreme

	def ploter(self):

		if self.cfg[__class__.__name__ + '_T_5M'] == True:
			local_5M = self.get(timeframe='5M')

			dataset = pd.DataFrame(self.elements['dataset_5M'])
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
			mpf.plot(
					dataset,
					type='candle',
					volume=True,
					style='yahoo',
					figscale=1,
					title='5M ExtremePoints',
					hlines=dict(hlines=list(local_5M.extreme.values),colors=['g'],linestyle='-.'),
					#if config.savefig_5M savefig=dict(fname=config.path_5M,dpi=600,pad_inches=0.25) else None,
					marketcolor_overrides=mco
					)


		if self.cfg[__class__.__name__ + '_T_1H'] == True:
			local_1H = self.get(timeframe='1H')

			dataset = pd.DataFrame(self.elements['dataset_1H'])
			dataset.index.name = 'Time'
			dataset.index = self.elements['dataset_1H'].time
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

			mpf.plot(
					dataset,
					type='candle',
					volume=True,
					style='yahoo',
					figscale=1,
					title='1H ExtremePoints',
					hlines=dict(hlines=list(local_1H.extreme.values),colors=['g'],linestyle='-.'),
					#savefig=dict(fname=config.path_1H,dpi=600,pad_inches=0.25),
					marketcolor_overrides=mco
					)

		if (
			self.cfg[__class__.__name__ + '_T_1H'] == False and
			self.cfg[__class__.__name__ + '_T_5M'] == False
			): warnings.warn("No Permit To Plot %s, Please Check Flags in pr/Config.py".format(__class__.__name__))

		plt.show()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////