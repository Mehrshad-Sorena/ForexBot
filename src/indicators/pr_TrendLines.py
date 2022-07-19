from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from pr_ExtremePoints import ExtremePoints
from scipy.signal import argrelextrema
from scipy.interpolate import interp1d
from pr_Parameters import Parameters
from DataChanger import DataChanger
import matplotlib.pyplot as plt
from pr_Config import Config
import mplfinance as mpf
import pandas as pd
import numpy as np

from timer import stTime

#**************************************************** Ramp Lines *******************************************************
class TrendLines:
	#This Function Used For Finding Trending Lines and Protect Resist of Trending Lines:

	parameters = Parameters()
	config = Config()

	def __init__(
				self,
				parameters,
				config
				):
		self.elements = dict(
							{
							'ExtremePoints'  + '_num_max_5M': parameters.elements[__class__.__name__  + '_num_max_5M'],
							'ExtremePoints'  + '_num_min_5M': parameters.elements[__class__.__name__  + '_num_min_5M'],

							'ExtremePoints'  + '_num_max_1H': parameters.elements[__class__.__name__  + '_num_max_1H'],
							'ExtremePoints'  + '_num_min_1H': parameters.elements[__class__.__name__  + '_num_min_1H'],

							'ExtremePoints'  + '_weight_5M': parameters.elements[__class__.__name__  + '_weight_5M'],
							'ExtremePoints'  + '_weight_1H': parameters.elements[__class__.__name__  + '_weight_1H'],


							__class__.__name__ + '_length_long_5M': parameters.elements[__class__.__name__  + '_length_long_5M'],
							__class__.__name__ + '_length_mid_5M': parameters.elements[__class__.__name__  + '_length_mid_5M'],
							__class__.__name__ + '_length_short1_5M': parameters.elements[__class__.__name__  + '_length_short1_5M'],
							__class__.__name__ + '_length_short2_5M': parameters.elements[__class__.__name__  + '_length_short2_5M'],
							
							__class__.__name__ + '_length_long_1H': parameters.elements[__class__.__name__  + '_length_long_1H'],
							__class__.__name__ + '_length_mid_1H': parameters.elements[__class__.__name__  + '_length_mid_1H'],
							__class__.__name__ + '_length_short1_1H': parameters.elements[__class__.__name__  + '_length_short1_1H'],
							__class__.__name__ + '_length_short2_1H': parameters.elements[__class__.__name__  + '_length_short2_1H'],

							__class__.__name__ + '_power_long_5M': parameters.elements[__class__.__name__  + '_power_long_5M'],
							__class__.__name__ + '_power_mid_5M': parameters.elements[__class__.__name__  + '_power_mid_5M'],
							__class__.__name__ + '_power_short1_5M': parameters.elements[__class__.__name__  + '_power_short1_5M'],
							__class__.__name__ + '_power_short2_5M': parameters.elements[__class__.__name__  + '_power_short2_5M'],
							
							__class__.__name__ + '_power_long_1H': parameters.elements[__class__.__name__  + '_power_long_1H'],
							__class__.__name__ + '_power_mid_1H': parameters.elements[__class__.__name__  + '_power_mid_1H'],
							__class__.__name__ + '_power_short1_1H': parameters.elements[__class__.__name__  + '_power_short1_1H'],
							__class__.__name__ + '_power_short2_1H': parameters.elements[__class__.__name__  + '_power_short2_1H'],


							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],
							}
							)

		self.cfg = dict(
						{
						'ExtremePoints'  + '_T_5M': config.cfg[__class__.__name__  + '_T_5M'],
						'ExtremePoints'  + '_T_1H': config.cfg[__class__.__name__  + '_T_1H'],
						'ExtremePoints'  + '_status': config.cfg[__class__.__name__  + '_status'],

						__class__.__name__ + '_status': config.cfg[__class__.__name__  + '_status'],

						__class__.__name__ + '_T_5M': config.cfg[__class__.__name__  + '_T_5M'],

						__class__.__name__ + '_long_T_5M': config.cfg[__class__.__name__  + '_long_T_5M'],
						__class__.__name__ + '_mid_T_5M': config.cfg[__class__.__name__  + '_mid_T_5M'],
						__class__.__name__ + '_short1_T_5M': config.cfg[__class__.__name__  + '_short1_T_5M'],
						__class__.__name__ + '_short2_T_5M': config.cfg[__class__.__name__  + '_short2_T_5M'],

						__class__.__name__ + '_T_1H': config.cfg[__class__.__name__  + '_T_1H'],

						__class__.__name__ + '_long_T_1H': config.cfg[__class__.__name__  + '_long_T_1H'],
						__class__.__name__ + '_mid_T_1H': config.cfg[__class__.__name__  + '_mid_T_1H'],
						__class__.__name__ + '_short1_T_1H': config.cfg[__class__.__name__  + '_short1_T_1H'],
						__class__.__name__ + '_short2_T_1H': config.cfg[__class__.__name__  + '_short2_T_1H'],

						__class__.__name__ + '_plot': config.cfg[__class__.__name__ + '_plot'],
						}
						)

	#*********************************

	def optimizer(
					self,
					data,
					data_close,
					index_exterm_point,
					exterm_point_pred,
					timeframe
					):

		index = index_exterm_point
		#******* DataSet High *********************
		n = len(exterm_point_pred)
		x = index
		y = exterm_point_pred.reshape(len(exterm_point_pred))
		#////////////////

		#***** Model Fitting High *****************
		lr = LinearRegression(
								fit_intercept=True, 
								copy_X=True, 
								n_jobs=-1, 
								positive=False
								)

		lr.fit(
				x.to_numpy().reshape(-1,1), 
				y
				) # x needs to be 2d for LinearRegression

		x = data_close.index

		if (self.cfg[__class__.__name__ + '_plot'] == True):
			plt.plot(
					x, 
					lr.predict(x.to_numpy().reshape(-1,1)), 
					"C0-",
					c='r'
					)
		

		#Finding interpolation Points For X_High and High Points:
		x1 = data[x]
		y = lr.predict(x.to_numpy().reshape(-1,1))
		f = interp1d(x1, y)


		if (self.cfg[__class__.__name__ + '_plot'] == True):
			plt.axhline(
						y= f(data[data.index[0] + len(data)-1]), 
						color = 'b', 
						linestyle = '-'
						)
			#plt.show()

		return f

	#*******************************

	def checker(
				self,
				f_low,
				f_high,
				low,
				high,
				length,
				timeframe
				):

		#finding Trend and Powers
		if (
			f_low(low[low.index[0] + len(low)-1]) > f_low(low[np.min(low.index)])
			): 
			ramp_low = 'pos'

		elif (
			f_low(low[low.index[0] + len(low)-1]) < f_low(low[np.min(low.index)])
			):

			ramp_low = 'neg'

		else:
			ramp_low = 'none'


		if (
			f_high(high[high.index[0] + len(high)-1]) > f_high(high[np.min(high.index)])
			):

			ramp_high = 'pos'

		elif (
			f_high(high[high.index[0] + len(high)-1]) < f_high(high[np.min(high.index)])
			):

			ramp_high = 'neg'

		else:
			ramp_high = 'none'

		#Define DataFrame For Trending OutPuts:
		trend_lines = pd.DataFrame(np.zeros(1))
		trend_lines['trend'] = np.nan
		trend_lines['power'] = np.nan
		trend_lines['min'] = np.nan
		trend_lines['max'] = np.nan

		#Finding Increasing Or Decreasing Trends:
		#Buy: Increasing
		#Sell: Decreasing
		if (
			(ramp_high == 'pos') & 
			(ramp_low == 'pos')
			):
			trend_lines['trend'] = ['buy']
			trend_lines['power'] = [self.elements[__class__.__name__ + '_power_' + length + '_' + timeframe]]

			#Value Of Protect Or Resist Finding With Interpolated Functions:
			trend_lines['min'] = [f_low(low[low.index[0] + len(low)-1])]
			trend_lines['max'] = [f_high(high[high.index[0] + len(high)-1])]

		elif (
				(ramp_high == 'neg') & 
				(ramp_low == 'neg')
			):
			trend_lines['trend'] = ['sell']
			trend_lines['power'] = [self.elements[__class__.__name__ + '_power_' + length + '_' + timeframe]]

			#Value Of Protect Or Resist Finding With Interpolated Functions:
			trend_lines['min'] = [f_low(low[low.index[0] + len(low)-1])]
			trend_lines['max'] = [f_high(high[high.index[0] + len(high)-1])]

		elif (
				(ramp_high == 'neg') & 
				(
					(ramp_low == 'pos')|
					(ramp_low == 'none') 
				)
			):

			if (
				f_high(high[np.min(high.index)]) > f_low(low[np.min(low.index)])
				):
				trend_lines['trend'] = ['parcham']
				trend_lines['power'] = [self.elements[__class__.__name__ + '_power_' + length + '_' + timeframe]]

				#Value Of Protect Or Resist Finding With Interpolated Functions:
				trend_lines['min'] = [f_low(low[low.index[0] + len(low)-1])]
				trend_lines['max'] = [f_high(high[high.index[0] + len(high)-1])]
		
		else:
			trend_lines['trend'] = ['no_flag']
			trend_lines['power'] = [0]
			trend_lines['min'] = [0]
			trend_lines['max'] = [0]

		return trend_lines

	#//////////////////////////////

	def finder(
				self,
				dataset,
				length,
				timeframe
				):
	
		#length: How Many Candles We Want To See For Finding Trending Lines?'short', 'mid', 'long'

		#Finding Extreme Points:
		extreme_points = ExtremePoints(parameters = self, config = self)
		extreme_point = extreme_points.finder(
												high = dataset.high,
												low = dataset.low,
												number_min = self.elements['ExtremePoints' + '_num_min_' + timeframe],
												number_max = self.elements['ExtremePoints' + '_num_max_' + timeframe]
												)

		#Model Fitting:
		f_low = self.optimizer(
								data = dataset.low,
								data_close = dataset['close'],
								index_exterm_point = extreme_point['index_min'].dropna(),
								exterm_point_pred = extreme_point['min'].dropna().to_numpy(),
								timeframe = timeframe
								)

		f_high = self.optimizer(
								data = dataset.high,
								data_close = dataset['close'],
								index_exterm_point = extreme_point['index_max'].dropna(),
								exterm_point_pred = extreme_point['max'].dropna().to_numpy(),
								timeframe = timeframe
								)

		trend_lines = self.checker(
									f_low = f_low,
									f_high = f_high,
									low = dataset.low,
									high = dataset.high,
									length = length,
									timeframe = timeframe
									)

		return trend_lines

	#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	#*********************************
	#@stTime
	def get(
			self,
			length,
			timeframe
			):
		#This Parameters is Defined For Finding Trending Lines:(How Many Candels We want To Find Trend?)

		length_data = self.elements[__class__.__name__ + '_length_' + length + '_' + timeframe]


		trend_local_extreme = pd.DataFrame()
		trend_local_extreme['min'] = np.nan
		trend_local_extreme['max'] = np.nan
		trend_local_extreme['power'] = np.nan

		if (
			self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
			self.cfg[__class__.__name__ + '_status'] == True
			):

			#Cut Input Dataset With Len That WE Want To finding Trend Lines
			datachanger = DataChanger()
			dataset_ramp = datachanger.Spliter(
												data = self.elements['dataset_' + timeframe],
												length = length_data
												)

			trend_local_extreme = pd.DataFrame()
			trend_local_extreme = np.nan

			trend_local_extreme = self.finder(
												dataset = dataset_ramp,
												length=length,
												timeframe=timeframe
											)

		return trend_local_extreme

	def runner(self,timeframe):
		length = ['long','mid','short1','short2']
		trendline_name = []

		i = 0
		for ln in length:
			trendline_name.append('trendline_' + ln + '_' + timeframe)
			if (
				self.cfg[__class__.__name__ + '_' + ln + '_T_' + timeframe] == True and
				self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
				self.cfg[__class__.__name__ + '_status'] == True
				):
				try:
					globals()[trendline_name[i]] = self.get(length=ln,timeframe = timeframe)
				except Exception as ex:
					globals()[trendline_name[i]] = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])

			else:
				globals()[trendline_name[i]] = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])
			i += 1

		if timeframe == '5M':
			return trendline_long_5M, trendline_mid_5M, trendline_short1_5M, trendline_short2_5M

		if timeframe == '1H':
			return trendline_long_1H, trendline_mid_1H, trendline_short1_1H, trendline_short2_1H

	def ploter(self,length):

		if self.cfg[__class__.__name__ + '_T_5M'] == True:
			self.cfg[__class__.__name__ + '_plot'] = True
			local_5M = self.get(timeframe='5M',length = length)

			line = pd.DataFrame(plt.gca().lines[0].get_xdata(),columns=['line1'])
			line['line1'] = np.nan
			line['line2'] = np.nan

			for elm in plt.gca().lines[0].get_xdata():
				line['line1'][elm] = plt.gca().lines[0].get_ydata()[elm]

			for elm in plt.gca().lines[2].get_xdata():
				line['line2'][elm] = plt.gca().lines[2].get_ydata()[elm]

			apd = mpf.make_addplot(line)


			length_data = self.elements[__class__.__name__ + '_length_' + length + '_5M']

			datachanger = DataChanger()
			dataset_ramp = datachanger.Spliter(
												data = self.elements['dataset_' + '5M'],
												length = length_data
												)

			dataset = dataset_ramp.copy(deep = True)
			dataset.index.name = 'Time'
			dataset.index = dataset_ramp.time
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

			point_1 = float(plt.gca().lines[3].get_ydata()[0])
			point_2 = float(plt.gca().lines[1].get_ydata()[0])

			
			plt.close('all')

			mpf.plot(
					dataset,
					type='candle',
					volume=False,
					style='yahoo',
					figscale=1,
					title='5M TrendLines',
					hlines=dict(hlines=[point_1,point_2],colors=['black','purple'],linestyle='-.'),
					#if config.savefig_5M savefig=dict(fname=config.path_5M,dpi=600,pad_inches=0.25) else None,
					marketcolor_overrides=mco,
					addplot=apd
					)


		if self.cfg[__class__.__name__ + '_T_1H'] == True:

			self.cfg[__class__.__name__ + '_plot'] = True
			local_1H = self.get(timeframe='1H',length = length)

			line = pd.DataFrame(plt.gca().lines[0].get_xdata(),columns=['line1'])
			line['line1'] = np.nan
			line['line2'] = np.nan

			for elm in plt.gca().lines[0].get_xdata():
				line['line1'][elm] = plt.gca().lines[0].get_ydata()[elm]

			for elm in plt.gca().lines[2].get_xdata():
				line['line2'][elm] = plt.gca().lines[2].get_ydata()[elm]

			apd = mpf.make_addplot(line)

			length_data = self.elements[__class__.__name__ + '_length_' + length + '_1H']

			datachanger = DataChanger()
			dataset_ramp = datachanger.Spliter(
												data = self.elements['dataset_' + '1H'],
												length = length_data
												)

			dataset = dataset_ramp.copy(deep = True)
			dataset.index.name = 'Time'
			dataset.index = dataset_ramp.time
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

			point_1 = float(plt.gca().lines[3].get_ydata()[0])
			point_2 = float(plt.gca().lines[1].get_ydata()[0])
			
			plt.close('all')

			mpf.plot(
					dataset,
					type='candle',
					volume=False,
					style='yahoo',
					figscale=1,
					title='1H TrendLines',
					hlines=dict(hlines=[point_1,point_2],colors=['black','purple'],linestyle='-.'),
					#if config.savefig_5M savefig=dict(fname=config.path_5M,dpi=600,pad_inches=0.25) else None,
					marketcolor_overrides=mco,
					addplot=apd
					)

		if (
			self.cfg[__class__.__name__ + '_T_1H'] == False and
			self.cfg[__class__.__name__ + '_T_5M'] == False
			): warnings.warn("No Permit To Plot %s, Please Check Flags in pr/Config.py".format(__class__.__name__))

	#/////////////////////////////////

