from scipy.signal import argrelextrema
from pr_Parameters import Parameters
from pr_Config import Config

from timer import stTime

import matplotlib.pyplot as plt
import warnings as warnings
import mplfinance as mpf
import numpy as np
import sys
warnings.filterwarnings("ignore")

try:
	import cudf as pd
except:
	try:
		import os
		os.environ["MODIN_ENGINE"] = "ray"  # Modin will use Ray
		import modin.pandas as pd
		import ray
		ray.init()
	except:
		import pandas as pd


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
	
	#@stTime
	def get(self, timeframe):

		#Finding Extremes From Time Frame
		local_extreme = pd.DataFrame(columns=['extreme','power'])
		
		if (
			self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
			self.cfg[__class__.__name__ + '_status'] == True
			):
			local_extreme['extreme'] = pd.DataFrame(
														finder(
																high = self.elements['dataset_' + timeframe].high,
																low = self.elements['dataset_' + timeframe].low,
																number_min = self.elements[__class__.__name__ + '_num_min_' + timeframe],
																number_max = self.elements[__class__.__name__ + '_num_max_' + timeframe]
																).extreme
														)

			local_extreme['power'] = np.ones(len(local_extreme)) * self.elements[__class__.__name__ + '_weight_' + timeframe]

		else:
			local_extreme = pd.DataFrame(np.nan, index = [0], columns=['extreme','power'])

		return local_extreme

	def runner(self, timeframe):

		extreme_name = 'extreme_' + timeframe
		if (
			self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
			self.cfg[__class__.__name__ + '_status'] == True
			):
			try:
				globals()[extreme_name] = self.get(timeframe = timeframe)
			except Exception as ex:
				globals()[extreme_name] = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])

		else:
			globals()[extreme_name] = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])

		if timeframe == '5M':
			return extreme_5M

		if timeframe == '1H':
			return extreme_1H

	def ploter(self):

		if self.cfg[__class__.__name__ + '_T_5M'] == True:
			local_5M = self.get(timeframe='5M')

			dataset = self.elements['dataset_5M'].copy(deep = True)
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

			dataset = self.elements['dataset_1H'].copy(deep = True)
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

def finder(
			high,
			low,
			number_min,
			number_max
			):

	extremes = pd.DataFrame({
							'low': low,
							'high': high,
							})

	#Finding Extreme Points
	#Finding Minimum Points:

	extremes['min'] = extremes.iloc[
									argrelextrema(
													extremes.low.values, 
													comparator = np.less,
													order = number_min,
													mode='wrap'
													)[0]
									]['low']

	#Finding Maximum Points:
	extremes['max'] = extremes.iloc[
									argrelextrema(
													extremes.high.values, 
													comparator = np.greater,
													order = number_max,
													mode='wrap'
													)[0]
									]['high']

	#Concatenate Max And Min Points to One DataFrame:
	#exterm_point = pd.DataFrame(columns=['extreme','max','min'])
	exterm_point = pd.DataFrame(
								np.concatenate(
												(
													extremes['max'].dropna().to_numpy(),
													extremes['min'].dropna().to_numpy()
												),
												axis=None
												),columns=['extreme']
								)

	if len(exterm_point.extreme) >= len(extremes['max'].dropna(inplace=False)):
		exterm_point_max = pd.DataFrame(
										np.concatenate(
														(
															extremes['max'].dropna(inplace=False).to_numpy(),
															np.zeros(len(exterm_point.extreme) - len(extremes['max'].dropna()), dtype=np.int32)/0
														),
														axis=None
														),columns=['max']
										)

		index_exterm_point_max = pd.DataFrame(
										np.concatenate(
														(
															extremes['max'].dropna(inplace=False).index.to_numpy(),
															np.zeros(len(exterm_point.extreme) - len(extremes['max'].dropna()), dtype=np.int32)/0
														),
														axis=None
														),columns=['index_max']
										)

	if len(exterm_point.extreme) >= len(extremes['min'].dropna(inplace=False)):
		exterm_point_min = pd.DataFrame(
										np.concatenate(
														(
															extremes['min'].dropna(inplace=False).to_numpy(),
															np.zeros(len(exterm_point.extreme) - len(extremes['min'].dropna()), dtype=np.int32)/0
														),
														axis=None
														),columns=['min']
										)

		index_exterm_point_min = pd.DataFrame(
										np.concatenate(
														(
															extremes['min'].dropna(inplace=False).index.to_numpy(),
															np.zeros(len(exterm_point.extreme) - len(extremes['min'].dropna()), dtype=np.int32)/0
														),
														axis=None
														),columns=['index_min']
										)
		
	exterm_point = exterm_point.assign(
										max = exterm_point_max,
										min = exterm_point_min,
										index_max = index_exterm_point_max,
										index_min = index_exterm_point_min
										)
	return exterm_point