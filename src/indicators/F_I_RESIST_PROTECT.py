import pandas as pd
import pandas_ta as ind
from log_get_data import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import math
from scipy import stats
from fitter import Fitter, get_common_distributions, get_distributions
import fitter
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
import time
from matplotlib.collections import LineCollection
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state

# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ta.ichimoku)

#***************** Function Names ***********
# Extreme_points(high,low,number_min,number_max)
# Extreme_points_ichimoko(high,low,close,tenkan=9,kijun=26,senkou=52,n_clusters=15,weight=1)
# extreme_points_ramp_lines(high,low,close,length='short',number_min=10,number_max=10,plot=False)
# Best_Extreme_Finder(exterm_point,high,low,n_clusters_low,n_clusters_high,alpha_low,alpha_high,timeout_break)
# protect_resist(T_5M,T_15M,T_1H,T_4H,T_1D,dataset_5M,dataset_15M,dataset_1H,dataset_4H,dataset_1D,plot=False)
#//////////////////////////////////////////////

#**************************************************** extreme High Or Low Lines *******************************************************

def Extreme_points(high,low,number_min,number_max):
	
	extremes = pd.DataFrame(low, columns=['low'])
	extremes['high'] = high

	#Finding Extreme Points
	extremes['min'] = extremes.iloc[argrelextrema(extremes.low.values, comparator = np.less,order=number_max)[0]]['low']
	extremes['max'] = extremes.iloc[argrelextrema(extremes.high.values, comparator = np.greater,order=number_max)[0]]['high']

	exterm_point = pd.DataFrame(np.concatenate((extremes['max'].dropna().to_numpy(), 
		extremes['min'].dropna().to_numpy()), axis=None),columns=['extremes'])

	return exterm_point
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ichimoko Lines *******************************************************

def Extreme_points_ichimoko(high,low,close,tenkan=9,kijun=26,senkou=52,n_clusters=15,weight=1):
	ichi = ind.ichimoku(high = high,low = low,close = close,tenkan = tenkan,kijun = kijun,senkou = senkou)

	column = ichi[0].columns[0]
	SPANA = pd.DataFrame(ichi[0], columns=[column])
	column = ichi[0].columns[1]
	SPANB = pd.DataFrame(ichi[0], columns=[column])
	column = ichi[0].columns[2]
	Tenkan = pd.DataFrame(ichi[0], columns=[column])
	column = ichi[0].columns[3]
	Kijun = pd.DataFrame(ichi[0], columns=[column])


	Tenkan_train = pd.DataFrame()
	Tenkan_train['extreme'] = Tenkan.dropna()
	Tenkan_train['power'] = np.ones(len(Tenkan_train))*1

	Kijun_train = pd.DataFrame()
	Kijun_train['extreme'] = Kijun.dropna()
	Kijun_train['power'] = np.ones(len(Kijun_train))*1

	SPANA_train = pd.DataFrame()
	SPANA_train['extreme'] = SPANA.dropna()
	SPANA_train['power'] = np.ones(len(SPANA_train))*2

	SPANB_train = pd.DataFrame()
	SPANB_train['extreme'] = SPANB.dropna()
	SPANB_train['power'] = np.ones(len(SPANB_train))*2

	Three_train_1 = pd.DataFrame(np.concatenate((Kijun_train['extreme'].to_numpy(),SPANA_train['extreme'].to_numpy(),SPANB_train['extreme'].to_numpy()),axis = None),columns=['extreme'])
	Three_train_1['power'] = np.ones(len(Three_train_1))*3

	Three_train_2 = pd.DataFrame(np.concatenate((Tenkan_train['extreme'].to_numpy(),SPANA_train['extreme'].to_numpy(),SPANB_train['extreme'].to_numpy()),axis = None),columns=['extreme'])
	Three_train_2['power'] = np.ones(len(Three_train_2))*3

	Four_train = pd.DataFrame(np.concatenate((Tenkan_train['extreme'].to_numpy(),Kijun_train['extreme'].to_numpy(),SPANA_train['extreme'].to_numpy(),SPANB_train['extreme'].to_numpy()),axis = None),columns=['extreme'])
	Four_train['power'] = np.ones(len(Four_train))*4


	exterm_point = pd.DataFrame(np.concatenate((Tenkan_train['extreme'].to_numpy(), 
				Kijun_train['extreme'].to_numpy(),SPANA_train['extreme'].to_numpy(),
				SPANB_train['extreme'].to_numpy(),Three_train_1['extreme'].to_numpy(),
				Three_train_2['extreme'].to_numpy(),Four_train['extreme'].to_numpy())
				, axis=None),columns=['extremes'])

	exterm_point['power'] = np.concatenate((Tenkan_train['power'].to_numpy(), 
				Kijun_train['power'].to_numpy(),SPANA_train['power'].to_numpy(),
				SPANB_train['power'].to_numpy(),Three_train_1['power'].to_numpy(),
				Three_train_2['power'].to_numpy(),Four_train['power'].to_numpy())
				, axis=None)

	kmeans = KMeans(n_clusters=n_clusters, random_state=0)
	#fitting
	kmeans = kmeans.fit(exterm_point['extremes'].to_numpy().reshape(-1,1), sample_weight= exterm_point['power'].to_numpy())

	X_pred = kmeans.cluster_centers_
	
	#Power = np.bincount(kmeans.fit_predict(close.to_numpy().reshape(-1,1)))
	Power = np.bincount(kmeans.labels_)


	exterm_point_pred = pd.DataFrame(X_pred, columns=['extreme'])
	exterm_point_pred['power'] = Power * weight
	return exterm_point_pred
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ramp Lines *******************************************************

def extreme_points_ramp_lines(high,low,close,length='short',number_min=10,number_max=10,plot=False):
	
	#length:
	#short
	#mid
	#long

	#Finding Extreme Points
	extremes = pd.DataFrame(low, columns=['low'])
	extremes['high'] = high

	extremes['min'] = extremes.iloc[argrelextrema(extremes.low.values, comparator = np.less,order=number_min)[0]]['low']
	extremes['max'] = extremes.iloc[argrelextrema(extremes.high.values, comparator = np.greater,order=number_max)[0]]['high']

	#Optimization Points With Scoring: Training Points 
	exterm_point_high = pd.DataFrame(extremes['max'].dropna(inplace=False))
	exterm_point_low = pd.DataFrame(extremes['min'].dropna(inplace=False))
	#Model Fitting High
	exterm_point_pred_high = exterm_point_high.to_numpy()
	#Model Fitting Low
	exterm_point_pred_low = exterm_point_low.to_numpy()

	index_high = exterm_point_high.index
	index_low = exterm_point_low.index
	#******* DataSet High *********************
	n_high = len(exterm_point_pred_high)
	x_high = index_high#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
	y_high = exterm_point_pred_high.reshape(len(exterm_point_pred_high))

	#******* DataSet Low *********************
	n_low = len(exterm_point_pred_low)
	x_low = index_low#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
	y_low = exterm_point_pred_low.reshape(len(exterm_point_pred_low))

	#////////////////

	#***** Model Fitting High *****************
	lr_high = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
	lr_high.fit(x_high.to_numpy().reshape(-1,1), y_high) # x needs to be 2d for LinearRegression

	#***** Model Fitting Low *****************
	lr_low = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
	lr_low.fit(x_low.to_numpy().reshape(-1,1), y_low)  # x needs to be 2d for LinearRegression
	#///////////////////////

	#********* Plot Fitting High ************
	if (plot == True):
		fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))

	if (plot == True):
		ax0.plot(high.index,high,c='g')
	#ax0.plot(x, y, "C0.", markersize=12)
	#ax0.plot(x_high, y_high, "C0.-", markersize=12)
	x_high = close.index

	#ax0.plot(x_high, lr_high.predict(y3[:, np.newaxis]), "C0-",c='r')
	if (plot == True):
		ax0.plot(x_high, lr_high.predict(x_high.to_numpy().reshape(-1,1)), "C0-",c='r')
	
	x1_high = high[x_high]
	y_high = lr_high.predict(x_high.to_numpy().reshape(-1,1))
	f_high = interp1d(x1_high, y_high)
	#print(f_high(y3[len(y1)-1]))

	if (plot == True):
		ax0.axhline(y= f_high(high[high.index[0] + len(high)-1]), color = 'r', linestyle = '-')

	#********* Plot Fitting Low ************
	#ax0.plot(x_low, y_low, "C0.-", markersize=12)
	x_low = close.index
	y_low = lr_low.predict(x_low.to_numpy().reshape(-1,1))
	if (plot == True):
		ax0.plot(x_low, y_low, "C1-",c='b')
	#print('y_low1 = ',lr_low.predict(x_low[:, np.newaxis]))
	x1_low = low
	#print('y_low2 = ',y_low)
	f_low = interp1d(x1_low, y_low)
	#print(f_low(y4[len(y1)-1]))

	if (plot == True):
		ax0.axhline(y= f_low(low[low.index[0] + len(low)-1]), color = 'b', linestyle = '--')
		plt.show()

	#finding Trend and Powers
	if (f_low(low[low.index[0] + len(low)-1]) > f_low(low[np.min(low.index)])):
		ramp_low = 'pos'
	elif (f_low(low[low.index[0] + len(low)-1]) < f_low(low[np.min(low.index)])):
		ramp_low = 'neg'
	else:
		ramp_low = 'none'

	if (f_high(high[high.index[0] + len(high)-1]) > f_high(high[np.min(high.index)])):
		ramp_high = 'pos'
	elif (f_high(high[high.index[0] + len(high)-1]) < f_high(high[np.min(high.index)])):
		ramp_high = 'neg'
	else:
		ramp_high = 'none'

	trend_lines = pd.DataFrame(np.zeros(1))
	trend_lines['trend'] = np.nan
	trend_lines['power'] = np.nan
	trend_lines['min'] = np.nan
	trend_lines['max'] = np.nan

	if (length == 'short'):
		power_trends = 100
	if (length == 'mid'):
		power_trends = 200
	if (length == 'long'):
		power_trends = 400	

	if (ramp_high == 'pos') & (ramp_low == 'pos'):
		trend_lines['trend'] = 'buy'
		trend_lines['power'] = power_trends
		trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
		trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	if (ramp_high == 'neg') & (ramp_low == 'neg'):
		trend_lines['trend'] = 'sell'
		trend_lines['power'] = power_trends
		trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
		trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	if (ramp_high == 'neg') & ((ramp_low == 'pos')|(ramp_low == 'none') ):
		if (f_high(high[np.min(high.index)]) > f_low(low[np.min(low.index)])):
			trend_lines['trend'] = 'parcham'
			trend_lines['power'] = power_trends
			trend_lines['min'] = f_low(low[low.index[0] + len(low)-1])
			trend_lines['max'] = f_high(high[high.index[0] + len(high)-1])

	return trend_lines

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Best Extreme Finder ***************************************************


def Best_Extreme_Finder(exterm_point,high,low,n_clusters_low,n_clusters_high,alpha_low,alpha_high,timeout_break):

	#************************ Help ***********************************************************
	#exterm_point: All Extreme Points From Protection Resistion Functions
	#n_clusters: Number Of Mean Centers Of Extreme Points, **** Must Be Optimazing and save in Database ****
	#high: the High Level Of Candles from that Time Frame You want
	#low: the Low Level Of Candles from that Time Frame You want
	#alpha: the Accuracy of Finding Best Protection Or Resistation, **** Must Be Optimazing and save in Database ****
	#timeout_break: Maximum Time Out For Running this Optimizer
	#/////////////////////////////////////////////////////////////////////////////////////////

	timeout = time.time() + timeout_break  # timeout_break Sec from now
	while True:
		if (len(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1)) > (n_clusters_low * 4)):
			n_clusters_low = n_clusters_low
		else:
			n_clusters_low = int(len(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1))/4) + 1

		if (len(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1)) > (n_clusters_high * 4)):
			n_clusters_high = n_clusters_high
		else:
			n_clusters_high = int(len(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1))/4) + 1

		kmeans_low = KMeans(n_clusters=n_clusters_low, random_state=0,init='k-means++',n_init=2,max_iter=3)
		kmeans_high = KMeans(n_clusters=n_clusters_high, random_state=0,init='k-means++',n_init=2,max_iter=3)
		#Model Fitting
		kmeans_low = kmeans_low.fit(exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']<=high[len(high)-1])].reshape(-1,1), sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']<=high[len(high)-1])])
		kmeans_high = kmeans_high.fit(exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']>=low[len(low)-1])].reshape(-1,1), sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']>=low[len(low)-1])])
		
		Y_low = kmeans_low.cluster_centers_
		Y_high = kmeans_high.cluster_centers_

		#Power_low = kmeans_low.labels_
	
		Power_low = kmeans_low.fit_predict(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1))
		Power_high = kmeans_high.fit_predict(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1))

		
		X_low = kmeans_low.cluster_centers_
		X_high = kmeans_high.cluster_centers_

		Power_low = np.bincount(Power_low)
		Power_high = np.bincount(Power_high)

		if ((len(Y_low) != len(X_low)) | (len(Power_low) != len(Y_low)) | (len(Power_low) != len(X_low)) |
		 ((len(Y_high) != len(X_high)) | (len(Power_high) != len(Y_high)) | (len(Power_high) != len(X_high)) )):
			timeout = time.time() + timeout_break
			continue
		#if (time.time() > timeout):
			#return 'timeout.error'
		if ((len(Y_low) == len(X_low)) & ((len(Y_high) == len(X_high)))): break

	exterm_point_pred_final_low = pd.DataFrame(X_low, columns=['X'])
	exterm_point_pred_final_low['Y'] = Y_low
	exterm_point_pred_final_low['power'] = Power_low
	exterm_point_pred_final_low = exterm_point_pred_final_low.sort_values(by = ['X'])


	exterm_point_pred_final_high = pd.DataFrame(X_high, columns=['X'])
	exterm_point_pred_final_high['Y'] = Y_high
	exterm_point_pred_final_high['power'] = Power_high
	exterm_point_pred_final_high = exterm_point_pred_final_high.sort_values(by = ['X'])


	#Fitting Model Finding ****************************
	data_X_high=np.zeros(np.sum(exterm_point_pred_final_high['power']))
	data_X_low=np.zeros(np.sum(exterm_point_pred_final_low['power']))

	j = 0
	z = 0
	for elm in exterm_point_pred_final_low['X']:
		k = 0
		while k < exterm_point_pred_final_low['power'].to_numpy()[j]:
			data_X_low[z] = elm
			k += 1
			z += 1
		j += 1

	j = 0
	z = 0
	for elm in exterm_point_pred_final_high['X']:
		k = 0
		while k < exterm_point_pred_final_high['power'].to_numpy()[j]:
			data_X_high[z] = elm
			k += 1
			z += 1
		j += 1
	#data = np.sort(data)
	data_X_low = np.sort(data_X_low)
	data_X_high = np.sort(data_X_high)

	timeout = time.time() + timeout_break  # timeout_break Sec from now
	#'rayleigh','nakagami','expon','foldnorm','dweibull',
	distributions_low = ['expon','norm']
	distributions_high = ['expon','norm']
	#************************************ Finding Low ****************************

	while True:
		f_low = Fitter(data = data_X_low, xmin=np.min(data_X_low), xmax=np.max(data_X_low), bins = len(exterm_point_pred_final_low['X']), distributions = distributions_low, timeout=0.05, density=True)

		f_low.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_low = list(f_low.get_best(method = 'sumsquare_error').items())
		dist_name_low = items_low[0][0]
		dist_parameters = items_low[0][1]

		if dist_name_low == 'foldnorm':
			Y = f_low.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
		
		elif dist_name_low == 'dweibull':
			Y = f_low.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
		
		elif dist_name_low == 'rayleigh':
			Y = f_low.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
		
		elif dist_name_low == 'expon':
			Y = f_low.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
		
		elif dist_name_low == 'nakagami':
			Y = f_low.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_low, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_low, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
		
		elif dist_name_low == 'norm':
			Y = f_low.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_low['power'])

		if (time.time() > timeout):
			if (distributions_low == None):
				return 'timeout.error'

		if ((Mid_Line_low <= Upper_Line_low)&(Mid_Line_low >= Lower_Line_low)&(Upper_Line_low>Lower_Line_low)): 
			break
		else:
			distributions_low.remove(dist_name_low)
			if (distributions_low == None):
				return 'timeout.error'

	#//////////////////////////////////////////////////////////////////////////////////////

	timeout = time.time() + timeout_break  # timeout_break Sec from now
	#************************************ Finding High *************************************
	while True:
		f_high = Fitter(data = data_X_high, xmin=np.min(data_X_high), xmax=np.max(data_X_high), bins = len(exterm_point_pred_final_high['X']), distributions = distributions_high, timeout=0.05, density=True)

		f_high.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_high = list(f_high.get_best(method = 'sumsquare_error').items())
		dist_name_high = items_high[0][0]
		dist_parameters = items_high[0][1]

		if dist_name_high == 'foldnorm':
			Y = f_high.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
	
		elif dist_name_high == 'dweibull':
			Y = f_high.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
		
		elif dist_name_high == 'rayleigh':
			Y = f_high.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
		
		elif dist_name_high == 'expon':
			Y = f_high.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
		
		elif dist_name_high == 'nakagami':
			Y = f_high.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_high, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_high, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
		
		elif dist_name_high == 'norm':
			Y = f_high.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()/np.max(exterm_point_pred_final_high['power'])

		if (time.time() > timeout):
			if (distributions_high == None):
				return 'timeout.error'

		if ((Mid_Line_high <= Upper_Line_high)&(Mid_Line_high >= Lower_Line_high)&(Upper_Line_high>Lower_Line_high)): 
			break
		else:
			distributions_high.remove(dist_name_high)
			if (distributions_high == None):
				return 'timeout.error'

	best_extremes = pd.DataFrame()
	best_extremes['high'] = [Upper_Line_high,Mid_Line_high,Lower_Line_high]
	best_extremes['power_high'] = [Power_Upper_Line_high,Power_Mid_Line_high,Power_Lower_Line_high]
	best_extremes['low'] = [Upper_Line_low,Mid_Line_low,Lower_Line_low]
	best_extremes['power_low'] = [Power_Upper_Line_low,Power_Mid_Line_low,Power_Lower_Line_low]

	return best_extremes
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#***************************** Protect Resist Finder **************************************************************


def protect_resist(T_5M,T_15M,T_1H,T_4H,T_1D,dataset_5M,dataset_15M,dataset_1H,dataset_4H,dataset_1D,plot=False):

	#Extreme Points Finder Function

	local_extreme_5M = pd.DataFrame()
	local_extreme_5M['extreme'] = np.nan
	local_extreme_5M['power'] = np.nan
	if (T_5M == True):
		local_extreme_5M['extreme'] = pd.DataFrame(Extreme_points(high=dataset_5M['high'],low=dataset_5M['low'],
			number_min=5,number_max=5))
		local_extreme_5M['power'] = np.ones(len(local_extreme_5M))*10

	local_extreme_15M = pd.DataFrame()
	local_extreme_15M['extreme'] = np.nan
	local_extreme_15M['power'] = np.nan
	if (T_15M == True):
		local_extreme_15M['extreme'] = pd.DataFrame(Extreme_points(high=dataset_15M['high'],low=dataset_15M['low'],
			number_min=5,number_max=5))
		local_extreme_15M['power'] = np.ones(len(local_extreme_15M))*3

	local_extreme_1H = pd.DataFrame()
	local_extreme_1H['extreme'] = np.nan
	local_extreme_1H['power'] = np.nan
	if (T_1H == True):
		local_extreme_1H['extreme'] = pd.DataFrame(Extreme_points(high=dataset_1H['high'],low=dataset_1H['low'],
			number_min=5,number_max=5))
		local_extreme_1H['power'] = np.ones(len(local_extreme_1H))*12

	local_extreme_4H = pd.DataFrame()
	local_extreme_4H['extreme'] = np.nan
	local_extreme_4H['power'] = np.nan
	if (T_4H == True):
		local_extreme_4H['extreme'] = pd.DataFrame(Extreme_points(high=dataset_4H['high'],low=dataset_4H['low'],
			number_min=2,number_max=2))
		local_extreme_4H['power'] = np.ones(len(local_extreme_4H))*48

	local_extreme_1D = pd.DataFrame()
	local_extreme_1D['extreme'] = np.nan
	local_extreme_1D['power'] = np.nan
	if (T_1D == True):
		local_extreme_1D['extreme'] = pd.DataFrame(Extreme_points(high=dataset_1D['high'],low=dataset_1D['low'],
			number_min=2,number_max=2))
		local_extreme_1D['power'] = np.ones(len(local_extreme_1D))*288

	#Trend Line Extreme Finder Function
	trend_local_extreme_5M_long = pd.DataFrame()
	trend_local_extreme_5M_long = np.nan
	if (T_5M == True):
		trend_local_extreme_5M_long = extreme_points_ramp_lines(high = dataset_5M['high'],low = dataset_5M['low'],close = dataset_5M['close'],length='long',number_min=2,number_max=2,plot=False)

	trend_local_extreme_5M_mid = pd.DataFrame()
	trend_local_extreme_5M_mid = np.nan
	if (T_5M == True):
		trend_local_extreme_5M_mid = extreme_points_ramp_lines(high = dataset_5M['high'][int((len(dataset_5M['high'])-1)/2):len(dataset_5M['high'])-1],low = dataset_5M['low'][int((len(dataset_5M['low'])-1)/2):len(dataset_5M['low'])-1],close = dataset_5M['close'][int((len(dataset_5M['high'])-1)/2):len(dataset_5M['high'])-1],length='long',number_min=2,number_max=2,plot=False)

	trend_local_extreme_5M_short_1 = pd.DataFrame()
	trend_local_extreme_5M_short_1 = np.nan
	if (T_5M == True):
		trend_local_extreme_5M_short_1 = extreme_points_ramp_lines(high = dataset_5M['high'][int((len(dataset_5M['high'])-1)/4):len(dataset_5M['high'])-1],low = dataset_5M['low'][int((len(dataset_5M['high'])-1)/4):len(dataset_5M['high'])-1],close = dataset_5M['close'][int((len(dataset_5M['high'])-1)/4):len(dataset_5M['high'])-1],length='long',number_min=2,number_max=2,plot=False)

	trend_local_extreme_5M_short_2 = pd.DataFrame()
	trend_local_extreme_5M_short_2 = np.nan
	if (T_5M == True):
		trend_local_extreme_5M_short_2 = extreme_points_ramp_lines(high = dataset_5M['high'][int((len(dataset_5M['high'])-1)/8):len(dataset_5M['high'])-1],low = dataset_5M['low'][int((len(dataset_5M['high'])-1)/8):len(dataset_5M['high'])-1],close = dataset_5M['close'][int((len(dataset_5M['high'])-1)/8):len(dataset_5M['high'])-1],length='long',number_min=2,number_max=2,plot=False)
	#ichi Extreme Finder Function

	ichi_local_extreme_5M = pd.DataFrame()
	ichi_local_extreme_5M['extreme'] = np.nan
	ichi_local_extreme_5M['power'] = np.nan
	if (T_5M == True):
		ichi_local_extreme_5M = Extreme_points_ichimoko(dataset_5M['high'],dataset_5M['low'],dataset_5M['close'],tenkan=9,kijun=26,senkou=52,n_clusters=4,weight=1)

	ichi_local_extreme_15M = pd.DataFrame()
	ichi_local_extreme_15M['extreme'] = np.nan
	ichi_local_extreme_15M['power'] = np.nan
	if (T_15M == True):
		ichi_local_extreme_15M = Extreme_points_ichimoko(dataset_15M['high'],dataset_15M['low'],dataset_15M['close'],tenkan=9,kijun=26,senkou=52,n_clusters=4,weight=2)

	ichi_local_extreme_1H = pd.DataFrame()
	ichi_local_extreme_1H['extreme'] = np.nan
	ichi_local_extreme_1H['power'] = np.nan
	if (T_1H == True):
		ichi_local_extreme_1H = Extreme_points_ichimoko(dataset_1H['high'],dataset_1H['low'],dataset_1H['close'],tenkan=9,kijun=26,senkou=52,n_clusters=4,weight=5)

	ichi_local_extreme_4H = pd.DataFrame()
	ichi_local_extreme_4H['extreme'] = np.nan
	ichi_local_extreme_4H['power'] = np.nan
	if (T_4H == True):
		ichi_local_extreme_4H = Extreme_points_ichimoko(dataset_4H['high'],dataset_4H['low'],dataset_4H['close'],tenkan=9,kijun=26,senkou=52,n_clusters=4,weight=20)

	ichi_local_extreme_1D = pd.DataFrame()
	ichi_local_extreme_1D['extreme'] = np.nan
	ichi_local_extreme_1D['power'] = np.nan
	if (T_1D == True):
		ichi_local_extreme_1D = Extreme_points_ichimoko(dataset_1D['high'],dataset_1D['low'],dataset_1D['close'],tenkan=9,kijun=26,senkou=52,n_clusters=2,weight=100)

	#concat Extremes

	exterm_point = pd.DataFrame(np.concatenate((local_extreme_5M['extreme'].to_numpy(), 
			local_extreme_15M['extreme'].to_numpy(),local_extreme_1H['extreme'].to_numpy(),
			local_extreme_4H['extreme'].to_numpy(),local_extreme_1D['extreme'].to_numpy(),
			trend_local_extreme_5M_long['min'].to_numpy(),trend_local_extreme_5M_long['max'].to_numpy(),
			trend_local_extreme_5M_mid['min'].to_numpy(),trend_local_extreme_5M_mid['max'].to_numpy(),
			trend_local_extreme_5M_short_1['min'].to_numpy(),trend_local_extreme_5M_short_1['max'].to_numpy(),
			trend_local_extreme_5M_short_2['min'].to_numpy(),trend_local_extreme_5M_short_2['max'].to_numpy(),
			ichi_local_extreme_5M['extreme'].to_numpy(),
			ichi_local_extreme_15M['extreme'].to_numpy(),
			ichi_local_extreme_1H['extreme'].to_numpy(),
			ichi_local_extreme_4H['extreme'].to_numpy(),
			ichi_local_extreme_1D['extreme'].to_numpy()) , axis=None),columns=['extremes'])

	exterm_point['power'] = np.concatenate((local_extreme_5M['power'].to_numpy(), 
			local_extreme_15M['power'].to_numpy(),local_extreme_1H['power'].to_numpy(),
			local_extreme_4H['power'].to_numpy(),local_extreme_1D['power'].to_numpy(),
			trend_local_extreme_5M_long['power'].to_numpy(),trend_local_extreme_5M_long['power'].to_numpy(),
			trend_local_extreme_5M_mid['power'].to_numpy(),trend_local_extreme_5M_mid['power'].to_numpy(),
			trend_local_extreme_5M_short_1['power'].to_numpy(),trend_local_extreme_5M_short_1['power'].to_numpy(),
			trend_local_extreme_5M_short_2['power'].to_numpy(),trend_local_extreme_5M_short_2['power'].to_numpy(),
			ichi_local_extreme_5M['power'].to_numpy(),
			ichi_local_extreme_15M['power'].to_numpy(),
			ichi_local_extreme_1H['power'].to_numpy(),
			ichi_local_extreme_4H['power'].to_numpy(),
			ichi_local_extreme_1D['power'].to_numpy()) , axis=None)

	exterm_point = exterm_point.dropna()

	extereme = pd.DataFrame()
	extereme = Best_Extreme_Finder(exterm_point=exterm_point,high=dataset_5M['high'],low=dataset_5M['low'],n_clusters_low=4,n_clusters_high=4,alpha_low=0.05,alpha_high=0.05,timeout_break=1)
	extereme['trend_long'] = [trend_local_extreme_5M_long['trend'],trend_local_extreme_5M_long['trend'],trend_local_extreme_5M_long['trend']]
	extereme['trend_mid'] = [trend_local_extreme_5M_mid['trend'],trend_local_extreme_5M_mid['trend'],trend_local_extreme_5M_mid['trend']]
	extereme['trend_short1'] = [trend_local_extreme_5M_short_1['trend'],trend_local_extreme_5M_short_1['trend'],trend_local_extreme_5M_short_1['trend']]
	extereme['trend_short2'] = [trend_local_extreme_5M_short_2['trend'],trend_local_extreme_5M_short_2['trend'],trend_local_extreme_5M_short_2['trend']]

	if (plot == True):
		fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))
		ax0.axhline(y = extereme['high'][0], color = 'r', linestyle = '-')
		ax0.axhline(y = extereme['high'][1], color = 'g', linestyle = '-')
		ax0.axhline(y = extereme['high'][2], color = 'r', linestyle = '-')

		ax0.axhline(y = extereme['low'][0], color = 'g', linestyle = '-')
		ax0.axhline(y = extereme['low'][1], color = 'b', linestyle = '-')
		ax0.axhline(y = extereme['low'][2], color = 'g', linestyle = '-')

		end = len(dataset_5M['close']) - 1

		ax0.axvline(x = end, color = 'r', linestyle = '-')
		ax1.axvline(x = end, color = 'r', linestyle = '-')

		ax0.plot(dataset_5M['close'].index[end-100:end],dataset_5M['close'][end-100:end],'b')
		ax1.plot(dataset_5M['close'].index[end-10:end+300],dataset_5M['close'][end-10:end+300],'b')
		plt.show()

	return extereme
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


#***************************** How To Use Functions **********************************************


#symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,2000)
#symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,700)
#symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,10)
#symbol_data_4H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,10)
#symbol_data_1D,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,10)

#x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
#y1 = symbol_data_5M['AUDCAD_i']['close']
#y2 = symbol_data_5M['AUDCAD_i']['open']
#y3 = symbol_data_5M['AUDCAD_i']['high']
#y4 = symbol_data_5M['AUDCAD_i']['low']

#print('data get')


#exterm_point_pred = Extreme_points_ichimoko(high=y3,low=y4,close=y1,tenkan=9,kijun=26,senkou=52,n_clusters=15)
#print(exterm_point_pred)
#i = 0
#for elm in exterm_point_pred['extremes']:
#	plt.axhline(y=elm, color='g', linestyle='-')
#plt.plot(Kijun.index, Kijun,'b',Tenkan.index,Tenkan,'r',SPANA.index,SPANA,'g',SPANB.index,SPANB,'g')
#plt.plot(y1.index,y1)
#plt.show()

#time_last = time.time()
#res_pro = protect_resist(T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,dataset_5M=symbol_data_5M['AUDCAD_i'],dataset_15M=symbol_data_15M['AUDCAD_i'],dataset_1H=symbol_data_1H['AUDCAD_i'],dataset_4H=symbol_data_4H['AUDCAD_i'],dataset_1D=symbol_data_1D['AUDCAD_i'],plot=False)
#print('time left = ',time.time()-time_last)
#print(res_pro['power_high'])
#print('************************ Finish ***************************************')

#//////////////////////////////////////////////////////////////////////////////////

