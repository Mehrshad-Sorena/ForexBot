from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from scipy.signal import argrelextrema
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas_ta as ind
import pandas as pd
import numpy as np

#**************************************************** Ramp Lines *******************************************************
#This Function Used For Finding Trending Lines and Protect Resist of Trending Lines:
def extreme_points_ramp_lines(
							high,
							low,
							close,
							length='short',
							number_min=10,
							number_max=10,
							plot=False
							):
	
	#length: How Many Candles We Want To See For Finding Trending Lines?'short', 'mid', 'long'

	#Finding Extreme Points
	dataset = pd.DataFrame(
							low, columns=['low']
							)
	dataset['high'] = high

	exterm_point_high, exterm_point_low = extreme_points_finder(
																dataset=dataset
																)

	#Model Fitting High
	exterm_point_pred_high = exterm_point_high.to_numpy()
	#Model Fitting Low
	exterm_point_pred_low = exterm_point_low.to_numpy()


	f_high, f_low = trend_lines_optimizer(
										low = low,
										high = high,
										exterm_point_high = exterm_point_high,
										exterm_point_low = exterm_point_low,
										exterm_point_pred_high = exterm_point_pred_high,
										exterm_point_pred_low = exterm_point_pred_low,
										plot = False
											)

	trend_lines = trend_checker(
								f_low = f_low,
								f_high = f_high,
								low = low,
								high = high
								)

	return trend_lines

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************************

def extreme_points_finder(
							dataset
							):
	


	#Finding Min And Max Of Top Down From Candles:
	dataset['min'] = dataset.iloc[
									argrelextrema(
												dataset.low.values,
												comparator = np.less,
												order=number_min
												)[0]
									]['low']

	dataset['max'] = dataset.iloc[
									argrelextrema(
												dataset.high.values,
												comparator = np.greater,
												order=number_max
												)[0]
									]['high']


	#Optimization Points With Scoring: Training Points 
	#Define Two DataFrame For Max And Min:
	exterm_point_high = pd.DataFrame(
									dataset['max'].dropna(inplace=False)
									)

	exterm_point_low = pd.DataFrame(
									dataset['min'].dropna(inplace=False)
									)
	return exterm_point_high, exterm_point_low

#//////////////////////////////////

#*********************************

def trend_lines_optimizer(
						low,
						high,
						exterm_point_high,
						exterm_point_low,
						exterm_point_pred_high,
						exterm_point_pred_low,
						plot = False			
						):

	index_high = exterm_point_high.index
	index_low = exterm_point_low.index
	#******* DataSet High *********************
	n_high = len(exterm_point_pred_high)
	x_high = index_high
	y_high = exterm_point_pred_high.reshape(len(exterm_point_pred_high))

	#******* DataSet Low *********************
	n_low = len(exterm_point_pred_low)
	x_low = index_low
	y_low = exterm_point_pred_low.reshape(len(exterm_point_pred_low))

	#////////////////

	#***** Model Fitting High *****************
	lr_high = LinearRegression(
								fit_intercept=True, 
								copy_X=True, 
								n_jobs=-1, 
								positive=False
								)

	lr_high.fit(
				x_high.to_numpy().reshape(-1,1), 
				y_high
				) # x needs to be 2d for LinearRegression

	#***** Model Fitting Low *****************
	lr_low = LinearRegression(
								fit_intercept=True, 
								copy_X=True, 
								n_jobs=-1, 
								positive=False
								)

	lr_low.fit(
				x_low.to_numpy().reshape(-1,1), 
				y_low
				)  # x needs to be 2d for LinearRegression
	#///////////////////////

	#********* Plot Fitting High ************
	if (plot == True):
		fig, (ax0, ax1) = plt.subplots(
										ncols=2, 
										figsize=(12, 6)
										)

		ax0.plot(
				high.index,
				high,c='g'
				)


	x_high = close.index

	if (plot == True):
		ax0.plot(
				x_high, 
				lr_high.predict(x_high.to_numpy().reshape(-1,1)), 
				"C0-",
				c='r'
				)
	

	#Finding interpolation Points For X_High and High Points:
	x1_high = high[x_high]
	y_high = lr_high.predict(x_high.to_numpy().reshape(-1,1))
	f_high = interp1d(x1_high, y_high)


	if (plot == True):
		ax0.axhline(
					y= f_high(high[high.index[0] + len(high)-1]), 
					color = 'r', 
					linestyle = '-'
					)

	#********* Plot Fitting Low ************
	x_low = close.index
	y_low = lr_low.predict(x_low.to_numpy().reshape(-1,1))

	if (plot == True):
		ax0.plot(
				x_low, 
				y_low, 
				"C1-",
				c='b'
				)
	
	#Finding Interpoition Points For X_low And Low Points:
	x1_low = low
	f_low = interp1d(x1_low, y_low)

	return f_high, f_low
#////////////////////////////////

#*******************************

def trend_checker(
					f_low,
					f_high,
					low,
					high
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

	#Define Weights For short, mid, Long Trends:
	if (length == 'short'):
		power_trends = 100
	if (length == 'mid'):
		power_trends = 200
	if (length == 'long'):
		power_trends = 400	


	#Finding Increasing Or Decreasing Trends:
	#Buy: Increasing
	#Sell: Decreasing
	if (
		(ramp_high == 'pos') & 
		(ramp_low == 'pos')
		):

		trend_lines['trend'] = 'buy'
		trend_lines['power'] = power_trends

		#Value Of Protect Or Resist Finding With Interpolated Functions:
		trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
		trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	if (
		(ramp_high == 'neg') & 
		(ramp_low == 'neg')
		):

		trend_lines['trend'] = 'sell'
		trend_lines['power'] = power_trends

		#Value Of Protect Or Resist Finding With Interpolated Functions:
		trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
		trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	if (
		(ramp_high == 'neg') & 
			(
			(ramp_low == 'pos')|
			(ramp_low == 'none') 
			)
		):

		if (
			f_high(high[np.min(high.index)]) > f_low(low[np.min(low.index)])
			):

			trend_lines['trend'] = 'parcham'
			trend_lines['power'] = power_trends

			#Value Of Protect Or Resist Finding With Interpolated Functions:
			trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
			trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	return trend_lines

#//////////////////////////////