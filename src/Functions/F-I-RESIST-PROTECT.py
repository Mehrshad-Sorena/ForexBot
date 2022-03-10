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

# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ta.ichimoku)

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
def Extreme_points_ichimoko(high,low,close,tenkan=9,kijun=26,senkou=52,n_clusters=15):
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
	Power = np.bincount(kmeans.fit_predict(close.to_numpy().reshape(-1,1)))

	Y_pred = kmeans.labels_

	exterm_point_pred = pd.DataFrame(X_pred, columns=['extremes'])
	exterm_point_pred['power'] = Power
	return exterm_point_pred
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ramp Lines *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** olgooie parcam *******************************************************

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
		kmeans_low = KMeans(n_clusters=n_clusters_low, random_state=0,init='k-means++',n_init=10,max_iter=100)
		kmeans_high = KMeans(n_clusters=n_clusters_high, random_state=0,init='k-means++',n_init=10,max_iter=100)
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

		if ((len(Y_low) != len(X_low)) | ((len(Y_high) != len(X_high)))):
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
	distributions_low = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
	distributions_high = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']

	#************************************ Finding Low ****************************

	while True:
		
		f_low = Fitter(data = data_X_low, xmin=np.min(data_X_low), xmax=np.max(data_X_low), bins = len(exterm_point_pred_final_low['X']), distributions = distributions_low, timeout=30, density=True)

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
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()
		
		elif dist_name_low == 'dweibull':
			Y = f_low.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_low, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()
		
		elif dist_name_low == 'rayleigh':
			Y = f_low.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()
		
		elif dist_name_low == 'expon':
			Y = f_low.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()
		
		elif dist_name_low == 'nakagami':
			Y = f_low.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_low, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_low, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()
		
		elif dist_name_low == 'norm':
			Y = f_low.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_low, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_low = Extereme[1]
			Lower_Line_low = Extereme[0]
			Mid_Line_low = np.array(dist_parameters['loc'])
			Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1,-1))].to_numpy()
			Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1,-1))].to_numpy()
			Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1,-1))].to_numpy()

		if (time.time() > timeout):
			if (distributions_low == None):
				return 'timeout.error'

		if ((Mid_Line_low <= Upper_Line_low)&(Mid_Line_low >= Lower_Line_low)): 
			break
		else:
			distributions_low.remove(dist_name_low)
			if (distributions_low == None):
				return 'timeout.error'

	#//////////////////////////////////////////////////////////////////////////////////////

	timeout = time.time() + timeout_break  # timeout_break Sec from now
	#************************************ Finding High *************************************
	while True:
		
		f_high = Fitter(data = data_X_high, xmin=np.min(data_X_high), xmax=np.max(data_X_high), bins = len(exterm_point_pred_final_high['X']), distributions = distributions_high, timeout=30, density=True)

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
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()
	
		elif dist_name_high == 'dweibull':
			Y = f_high.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_high, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()
		
		elif dist_name_high == 'rayleigh':
			Y = f_high.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()
		
		elif dist_name_high == 'expon':
			Y = f_high.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()
		
		elif dist_name_high == 'nakagami':
			Y = f_high.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_high, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_high, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()
		
		elif dist_name_high == 'norm':
			Y = f_high.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_high, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_high = Extereme[1]
			Lower_Line_high = Extereme[0]
			Mid_Line_high = np.array(dist_parameters['loc'])
			Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1,-1))].to_numpy()
			Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1,-1))].to_numpy()
			Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1,-1))].to_numpy()

		if (time.time() > timeout):
			if (distributions_high == None):
				return 'timeout.error'

		if ((Mid_Line_high <= Upper_Line_high)&(Mid_Line_high >= Lower_Line_high)): 
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






symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,200)
symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,6000)
symbol_data_1H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,2000)
symbol_data_4H,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,360)
symbol_data_1D,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_D1,0,60)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

print('data get')


#exterm_point_pred = Extreme_points_ichimoko(high=y3,low=y4,close=y1,tenkan=9,kijun=26,senkou=52,n_clusters=15)
#print(exterm_point_pred)
#i = 0
#for elm in exterm_point_pred['extremes']:
#	plt.axhline(y=elm, color='g', linestyle='-')
#plt.plot(Kijun.index, Kijun,'b',Tenkan.index,Tenkan,'r',SPANA.index,SPANA,'g',SPANB.index,SPANB,'g')
#plt.plot(y1.index,y1)
#plt.show()

#********************************************** Finding Res_Pro With Trend Lines **************************

from matplotlib.collections import LineCollection

from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state

#Finding Extreme Points
extremes = pd.DataFrame(y4, columns=['low'])
extremes['high'] = y3

extremes['min'] = extremes.iloc[argrelextrema(extremes.low.values, comparator = np.less,order=10)[0]]['low']
extremes['max'] = extremes.iloc[argrelextrema(extremes.high.values, comparator = np.greater,order=10)[0]]['high']

#Optimization Points With Scoring: Training Points 
exterm_point_high = pd.DataFrame(extremes['max'].dropna(inplace=False))
exterm_point_low = pd.DataFrame(extremes['min'].dropna(inplace=False))

kmeans_high = KMeans(n_clusters=1,init='k-means++', n_init=2, max_iter=2)
#Model Fitting High
kmeans_high = kmeans_high.fit(exterm_point_high.values)
Power_high = kmeans_high.fit_predict(y3.to_numpy().reshape(-1,1))
exterm_point_pred_high = exterm_point_high.to_numpy()#kmeans_high.cluster_centers_
Y_pred_high = kmeans_high.labels_
counts_high = np.bincount(Y_pred_high)
mean_counts_high = np.mean(counts_high)
index_high = np.arange(0,len(exterm_point_pred_high),1)

#Model Fitting Low
kmeans_low = KMeans(n_clusters=1,init='k-means++', n_init=2, max_iter=2)
kmeans_low = kmeans_low.fit(exterm_point_low.values)
Power_low = kmeans_low.fit_predict(y4.to_numpy().reshape(-1,1))
exterm_point_pred_low = exterm_point_low.to_numpy()#kmeans_low.cluster_centers_
Y_pred_low = kmeans_low.labels_
counts_low = np.bincount(Y_pred_low)
mean_counts_low = np.mean(counts_low)
index_low = np.arange(0,len(exterm_point_pred_low),1)

k = 0
for elm in exterm_point_pred_high:
    index_high[k] = (pd.DataFrame(abs(exterm_point_high - elm)).idxmin())
    k += 1
index_high = exterm_point_high.index
k = 0
for elm in exterm_point_pred_low:
    index_low[k] = (pd.DataFrame(abs(exterm_point_low - elm)).idxmin())
    k += 1
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
lr_high.fit(x_high[:, np.newaxis], y_high) # x needs to be 2d for LinearRegression

#***** Model Fitting Low *****************
lr_low = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_low.fit(x_low[:, np.newaxis], y_low)  # x needs to be 2d for LinearRegression
#///////////////////////

#********* Plot Fitting High ************
fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))

ax0.plot(y3.index,y3,c='g')
#ax0.plot(x, y, "C0.", markersize=12)
#ax0.plot(x_high, y_high, "C0.-", markersize=12)
x_high = y1.index

#ax0.plot(x_high, lr_high.predict(y3[:, np.newaxis]), "C0-",c='r')
ax0.plot(x_high, lr_high.predict(x_high[:, np.newaxis]), "C0-",c='r')
from scipy.interpolate import interp1d
x1_high = y3[x_high]
y_high = lr_high.predict(x_high[:, np.newaxis])
f_high = interp1d(x1_high, y_high)
print(f_high(y3[len(y1)-1]))

ax0.axhline(y= f_high(y3[len(y3)-1]), color = 'r', linestyle = '-')

#********* Plot Fitting Low ************
#ax0.plot(x_low, y_low, "C0.-", markersize=12)
x_low = y1.index
y_low = lr_low.predict(x_low[:, np.newaxis])
ax0.plot(x_low, y_low, "C1-",c='b')
print('y_low1 = ',lr_low.predict(x_low[:, np.newaxis]))
x1_low = y4

print('y_low2 = ',y_low)
f_low = interp1d(x1_low, y_low)
print(f_low(y4[len(y1)-1]))

ax0.axhline(y= f_low(y4[len(y4)-1]), color = 'b', linestyle = '--')

plt.show()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////




#***************************** Test Functions **********************************************

i = len(y3)-1
while False:#i <= len(y3)-1:
	end = i
	i += 100

	local_extreme_5M = pd.DataFrame()
	local_extreme_5M['extreme'] = pd.DataFrame(Extreme_points(high=symbol_data_5M['AUDCAD_i']['high'][0:end],low=symbol_data_5M['AUDCAD_i']['low'][0:end],
		number_min=5,number_max=5))
	local_extreme_5M['power'] = np.ones(len(local_extreme_5M))*1

	local_extreme_15M = pd.DataFrame()
	local_extreme_15M['extreme'] = pd.DataFrame(Extreme_points(high=symbol_data_15M['AUDCAD_i']['high'],low=symbol_data_15M['AUDCAD_i']['low'],
		number_min=5,number_max=5))
	local_extreme_15M['power'] = np.ones(len(local_extreme_15M))*3

	local_extreme_1H = pd.DataFrame()
	local_extreme_1H['extreme'] = pd.DataFrame(Extreme_points(high=symbol_data_1H['AUDCAD_i']['high'],low=symbol_data_1H['AUDCAD_i']['low'],
		number_min=5,number_max=5))
	local_extreme_1H['power'] = np.ones(len(local_extreme_1H))*12

	local_extreme_4H = pd.DataFrame()
	local_extreme_4H['extreme'] = pd.DataFrame(Extreme_points(high=symbol_data_4H['AUDCAD_i']['high'],low=symbol_data_4H['AUDCAD_i']['low'],
		number_min=2,number_max=2))
	local_extreme_4H['power'] = np.ones(len(local_extreme_4H))*48

	local_extreme_1D = pd.DataFrame()
	local_extreme_1D['extreme'] = pd.DataFrame(Extreme_points(high=symbol_data_1D['AUDCAD_i']['high'],low=symbol_data_1D['AUDCAD_i']['low'],
		number_min=2,number_max=2))
	local_extreme_1D['power'] = np.ones(len(local_extreme_1D))*288



	exterm_point = pd.DataFrame(np.concatenate((local_extreme_5M['extreme'].to_numpy(), 
			local_extreme_15M['extreme'].to_numpy(),local_extreme_1H['extreme'].to_numpy(),
			local_extreme_4H['extreme'].to_numpy(),local_extreme_1D['extreme'].to_numpy(),
			exterm_point_pred['extremes'].to_numpy())
			, axis=None),columns=['extremes'])

	exterm_point['power'] = np.concatenate((local_extreme_5M['power'].to_numpy(), 
			local_extreme_15M['power'].to_numpy(),local_extreme_1H['power'].to_numpy(),
			local_extreme_4H['power'].to_numpy(),local_extreme_1D['power'].to_numpy(),
			exterm_point_pred['power'].to_numpy())
			, axis=None)



	extereme = Best_Extreme_Finder(exterm_point=exterm_point,high=y3[0:end],low=y4[0:end],n_clusters_low=5,n_clusters_high=5,alpha_low=0.1,alpha_high=0.05,timeout_break=1)

	fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))
	ax0.axhline(y = extereme['high'][0], color = 'r', linestyle = '-')
	ax0.axhline(y = extereme['high'][1], color = 'g', linestyle = '-')
	ax0.axhline(y = extereme['high'][2], color = 'r', linestyle = '-')

	ax0.axhline(y = extereme['low'][0], color = 'g', linestyle = '-')
	ax0.axhline(y = extereme['low'][1], color = 'b', linestyle = '-')
	ax0.axhline(y = extereme['low'][2], color = 'g', linestyle = '-')

	ax0.axvline(x = end, color = 'r', linestyle = '-')
	ax1.axvline(x = end, color = 'r', linestyle = '-')

	ax0.plot(y3.index[end-100:end],y3[end-100:end],'b')
	ax1.plot(y3.index[end-10:end+300],y3[end-10:end+300],'b')
	plt.show()
#f.hist()
print('************************ Finish ***************************************')

#//////////////////////////////////////////////////////////////////////////////////

