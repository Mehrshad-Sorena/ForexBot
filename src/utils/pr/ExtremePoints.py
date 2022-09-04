from scipy.signal import argrelextrema
#import src.utils.pr
from .Parameters import Parameters
from .Config import Config as config

import matplotlib.pyplot as plt
import warnings as warnings
import mplfinance as mpf
import pandas as pd
import numpy as np
import sys
warnings.filterwarnings("ignore")

config = config()

#**************************************************** extreme High Or Low Lines *******************************************************
#This function is Used For Finding Extremes Top Downs in Candles:
class ExtremePoints:

	parameters = Parameters()

	def __init__(
				self,
				parameters
				):
		
		self.number_max_5M = parameters.number_max_5M
		self.number_min_5M = parameters.number_min_5M

		self.number_max_1H = parameters.number_max_1H
		self.number_min_1H = parameters.number_min_1H

		self.weight_extreme_5M = parameters.weight_extreme_5M
		self.weight_extreme_1H = parameters.weight_extreme_1H

		self.dataset_5M = parameters.dataset_5M
		self.dataset_1H = parameters.dataset_1H


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
		
		if (getattr(config,'T_' + timeframe) == True):
			local_extreme['extreme'] = pd.DataFrame(
														self.finder(
																	high=getattr(self,'dataset_' + timeframe).high,
																	low=getattr(self,'dataset_' + timeframe).low,
																	number_min = getattr(self,'number_min_' + timeframe),
																	number_max = getattr(self,'number_max_' + timeframe)
																	).extreme
														)

			local_extreme['power'] = np.ones(len(local_extreme)) * getattr(self,'weight_extreme_' + timeframe)

		return local_extreme

	def ploter(self):

		if config.T_5M == True:
			local_5M = self.get(timeframe='5M')

			dataset = pd.DataFrame(self.dataset_5M)
			dataset.index.name = 'Time'
			dataset.index = self.dataset_5M.time
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
					#savefig=dict(fname=path_candle,dpi=600,pad_inches=0.25),
					marketcolor_overrides=mco
					)


		if config.T_1H == True:
			local_1H = self.get(timeframe='1H')

			dataset = pd.DataFrame(self.dataset_1H)
			dataset.index.name = 'Time'
			dataset.index = self.dataset_1H.time
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
					#savefig=dict(fname=path_candle,dpi=600,pad_inches=0.25),
					marketcolor_overrides=mco
					)

		if (
			config.T_1H == False and
			config.T_5M == False
			): warnings.warn('No Permit To Plot ExtremePoints, Please Check Flags in pr/Config.py')

		plt.show()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////