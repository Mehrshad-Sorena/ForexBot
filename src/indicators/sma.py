import pandas as pd
import pandas_ta as ind
from log_get_data import *
from sklearn.cluster import KMeans
import math
from scipy import stats
from fitter import Fitter, get_common_distributions, get_distributions
import fitter
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from scipy.optimize import fsolve
from shapely.geometry import LineString
import matplotlib.pyplot as plt


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ind.sma)

#**************************************************** Golden Cross *******************************************************
def Golden_Cross_SMA(dataset,Low_Period,High_Period,Low_ApplyTo,High_ApplyTo):

	x = np.arange(0,len(dataset[Low_ApplyTo]),1)

	SMA_Low = ind.sma(dataset[Low_ApplyTo], length = Low_Period)
	SMA_High = ind.sma(dataset[High_ApplyTo], length = High_Period)

	first_line = LineString(np.column_stack((x[(High_Period-1):], SMA_Low[(High_Period-1):])))
	second_line = LineString(np.column_stack((x[(High_Period-1):], SMA_High.dropna())))

	intersection = first_line.intersection(second_line)

	if intersection.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection).xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index
    
	elif intersection.geom_type == 'Point':
		cross = pd.DataFrame(*intersection.xy)
		cross_index = cross.index.to_numpy()
		cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross['index'] = cross.values.astype(int)
		cross['values'] = cross_index

	signal_buy = pd.DataFrame(np.zeros(len(cross)))
	signal_buy['signal'] = np.nan
	signal_buy['values'] = np.nan
	signal_buy['index'] = np.nan
	signal_buy['profit'] = np.nan

	signal_sell = pd.DataFrame(np.zeros(len(cross)))
	signal_sell['signal'] = np.nan
	signal_sell['values'] = np.nan
	signal_sell['index'] = np.nan
	signal_sell['profit'] = np.nan

	i = 0
	j = 0
	k = 0

	for elm in cross['index']:
		#print(elm)
		if ((SMA_Low[elm-1]<SMA_High[elm-1])&(SMA_Low[elm+1]>SMA_High[elm+1])):
			signal_buy['signal'][i] = 'buy'
			signal_buy['values'][i] = cross['values'][j]
			signal_buy['index'][i] = elm

			if ((j+1) < len(cross)):
				signal_buy['profit'][i] = (np.max(close[elm:cross['index'][j+1]] - close[elm])/close[elm]) * 100
			else:
				signal_buy['profit'][i] = (np.max(close[elm:-1] - close[elm])/close[elm]) * 100
			i += 1

		if ((SMA_Low[elm-1]>SMA_High[elm-1])&(SMA_Low[elm+1]<SMA_High[elm+1])):
			signal_sell['signal'][k] = 'sell'
			signal_sell['values'][k] = cross['values'][j]
			signal_sell['index'][k] = elm
			if ((j+1) < len(cross)):
				signal_sell['profit'][k] = (np.max(close[elm] - close[elm:cross['index'][j+1]])/np.min(close[elm:cross['index'][j+1]])) * 100
			else:
				signal_sell['profit'][k] = (np.max(close[elm] - close[elm:-1])/np.min(close[elm:-1])) * 100
			#print('elm_sell = ',elm)
			k += 1
		j += 1


	signal_buy = signal_buy.dropna(inplace = False)
	signal_sell = signal_sell.dropna(inplace = False)

	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_sell = signal_sell.sort_values(by = ['index'])

	return signal_buy,signal_sell

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Scalpe *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Find Best Intervals *******************************************************
def Find_Best_interval(dataset,period_low,period_high,Low_ApplyTo,High_ApplyTo,max_profit_buy,max_profit_sell,alpha_sell,alpha_buy):
	signal_buy,signal_sell = Golden_Cross_SMA(dataset=dataset,Low_Period=period_low,High_Period=period_high,Low_ApplyTo=Low_ApplyTo,High_ApplyTo=High_ApplyTo)

	signal_buy_good = signal_buy.drop(np.where(signal_buy['profit']<max_profit_buy)[0])
	signal_sell_good = signal_sell.drop(np.where(signal_sell['profit']<max_profit_sell)[0])

	SMA_Low = ind.sma(dataset[Low_ApplyTo], length = period_low)
	SMA_High = ind.sma(dataset[High_ApplyTo], length = period_high)

	ofset_buy = 1.000 + (max_profit_buy/100)
	ofset_sell = 1.000 - (max_profit_sell/100)

	#timeout = time.time() + 20  # timeout_break Sec from now
	while True:

		if (len(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))])-1) > (len(signal_buy_good['values'].to_numpy()) - 1):
			if (len(signal_buy_good['values'].to_numpy()) - 1) >= 10:
				n_clusters_buy = 10
			else:
				n_clusters_buy = len(signal_buy_good['values'].to_numpy()) - 1
		else:
			n_clusters_buy = len(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))])-1
		

		if (len(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))])-1) > (len(signal_sell_good['values'].to_numpy()) - 1):
			if (len(signal_sell_good['values'].to_numpy()) - 1) >= 10:
				n_clusters_sell = 10
			else:
				n_clusters_sell = len(signal_sell_good['values'].to_numpy()) - 1
		else:
			n_clusters_sell = len(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))])-1

		kmeans_sell = KMeans(n_clusters=n_clusters_sell, random_state=0,init='k-means++',n_init=10,max_iter=100)
		kmeans_buy = KMeans(n_clusters=n_clusters_buy, random_state=0,init='k-means++',n_init=10,max_iter=100)
		#Model Fitting
		kmeans_sell = kmeans_sell.fit(signal_sell_good['values'].to_numpy().reshape(-1,1), sample_weight= signal_sell_good['profit'].to_numpy())
		kmeans_buy = kmeans_buy.fit(signal_buy_good['values'].to_numpy().reshape(-1,1), sample_weight= signal_buy_good['profit'].to_numpy())
		
		Y_sell = kmeans_sell.cluster_centers_
		Y_buy = kmeans_buy.cluster_centers_

		#Power_low = kmeans_low.labels_
	
		Power_sell = kmeans_sell.fit_predict(signal_sell['values'].to_numpy()[np.where(signal_sell['values']>=(signal_sell['values'][len(signal_sell['values'])-1] * ofset_sell))].reshape(-1,1))
		#SMA_Low.dropna().to_numpy()[np.where(SMA_Low.dropna()>=(SMA_Low.dropna()[len(SMA_Low.dropna())-1] * ofset_sell))]
		Power_buy = kmeans_buy.fit_predict(signal_buy['values'].to_numpy()[np.where(signal_buy['values']<=(signal_buy['values'][len(signal_buy['values'])-1] * ofset_buy))].reshape(-1,1))
		#SMA_Low.dropna().to_numpy()[np.where(SMA_Low.dropna()<=(SMA_Low.dropna()[len(SMA_Low.dropna())-1] * ofset_buy))]
		#[np.where(y4>=y3[len(y3)-1])]

		
		X_sell = kmeans_sell.cluster_centers_
		X_buy = kmeans_buy.cluster_centers_

		Power_sell = np.bincount(Power_sell)
		Power_buy = np.bincount(Power_buy)

		if ((len(Y_sell) != len(X_sell)) | ((len(Y_buy) != len(X_buy)))):
			timeout = time.time() + timeout_break
			continue
		#if (time.time() > timeout):
			#return 'timeout.error'
		if ((len(Y_sell) == len(X_sell)) & ((len(Y_buy) == len(X_buy)))): break

	signal_sell_final = pd.DataFrame(X_sell, columns=['X'])
	signal_sell_final['Y'] = Y_sell
	signal_sell_final['power'] = Power_sell
	signal_sell_final = signal_sell_final.sort_values(by = ['X'])


	signal_buy_final = pd.DataFrame(X_buy, columns=['X'])
	signal_buy_final['Y'] = Y_buy
	signal_buy_final['power'] = Power_buy
	signal_buy_final = signal_buy_final.sort_values(by = ['X'])


	#Fitting Model Finding ****************************
	data_X_buy=np.zeros(np.sum(signal_buy_final['power']))
	data_X_sell=np.zeros(np.sum(signal_sell_final['power']))

	j = 0
	z = 0
	for elm in signal_sell_final['X']:
		k = 0
		while k < signal_sell_final['power'].to_numpy()[j]:
			data_X_sell[z] = elm
			k += 1
			z += 1
		j += 1

	j = 0
	z = 0
	for elm in signal_buy_final['X']:
		k = 0
		while k < signal_buy_final['power'].to_numpy()[j]:
			data_X_buy[z] = elm
			k += 1
			z += 1
		j += 1

	data_X_sell = np.sort(data_X_sell)
	data_X_buy = np.sort(data_X_buy)

	distributions_sell = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
	distributions_buy = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']

	#************************************ Finding Sell's ****************************

	while True:
		
		f_sell = Fitter(data = data_X_sell, xmin=np.min(data_X_sell), xmax=np.max(data_X_sell), bins = len(signal_sell_final['X']), distributions = distributions_sell, timeout=30, density=True)

		f_sell.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_sell = list(f_sell.get_best(method = 'sumsquare_error').items())
		dist_name_sell = items_sell[0][0]
		dist_parameters = items_sell[0][1]

		if dist_name_sell == 'foldnorm':
			Y = f_sell.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'dweibull':
			Y = f_sell.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_sell, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
		
		elif dist_name_sell == 'rayleigh':
			Y = f_sell.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'expon':
			Y = f_sell.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'nakagami':
			Y = f_sell.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_sell, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_sell, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
	
		elif dist_name_sell == 'norm':
			Y = f_sell.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_sell, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_sell = Extereme[1]
			Lower_Line_sell = Extereme[0]
			Mid_Line_sell = np.array(dist_parameters['loc'])
			Power_Upper_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Lower_Line_sell =(signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])
			Power_Mid_Line_sell = (signal_sell_final['power'][kmeans_sell.predict(Mid_Line_sell.reshape(1,-1))].to_numpy())/np.max(signal_sell_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_sell == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line_sell <= Upper_Line_sell)&(Mid_Line_sell >= Lower_Line_sell)): 
			break
		else:
			distributions_sell.remove(dist_name_sell)
			if (distributions_sell == None):
				#return 'timeout.error'
				pass

	#//////////////////////////////////////////////////////////////////////////////////////

	#timeout = time.time() + timeout_break  # timeout_break Sec from now
	#************************************ Finding High *************************************
	while True:
		
		f_buy = Fitter(data = data_X_buy, xmin=np.min(data_X_buy), xmax=np.max(data_X_buy), bins = len(signal_buy_final['X']), distributions = distributions_buy, timeout=30, density=True)

		f_buy.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items_buy = list(f_buy.get_best(method = 'sumsquare_error').items())
		dist_name_buy = items_buy[0][0]
		dist_parameters = items_buy[0][1]

		if dist_name_buy == 'foldnorm':
			Y = f_buy.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
	
		elif dist_name_buy == 'dweibull':
			Y = f_buy.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha_buy, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'rayleigh':
			Y = f_buy.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'expon':
			Y = f_buy.fitted_pdf['expon']
			Y = expon.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'nakagami':
			Y = f_buy.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X_buy, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha_buy, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
		
		elif dist_name_buy == 'norm':
			Y = f_buy.fitted_pdf['norm']
			Y = norm.pdf(x=data_X_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha_buy, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line_buy = Extereme[1]
			Lower_Line_buy = Extereme[0]
			Mid_Line_buy = np.array(dist_parameters['loc'])
			Power_Upper_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Upper_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Lower_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Lower_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])
			Power_Mid_Line_buy = (signal_buy_final['power'][kmeans_buy.predict(Mid_Line_buy.reshape(1,-1))].to_numpy())/np.max(signal_buy_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_buy == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line_buy <= Upper_Line_buy)&(Mid_Line_buy >= Lower_Line_buy)): 
			break
		else:
			distributions_buy.remove(dist_name_buy)
			if (distributions_buy == None):
				#return 'timeout.error'
				pass

	best_signals_interval = pd.DataFrame()
	best_signals_interval['buy'] = [Upper_Line_buy,Mid_Line_buy,Lower_Line_buy]
	best_signals_interval['power_buy'] = [Power_Upper_Line_buy,Power_Mid_Line_buy,Power_Lower_Line_buy]
	best_signals_interval['alpha_buy'] = [alpha_buy,alpha_buy,alpha_buy]

	best_signals_interval['sell'] = [Upper_Line_sell,Mid_Line_sell,Lower_Line_sell]
	best_signals_interval['power_sell'] = [Power_Upper_Line_sell,Power_Mid_Line_sell,Power_Lower_Line_sell]
	best_signals_interval['alpha_sell'] = [alpha_sell,alpha_sell,alpha_sell]

	return best_signals_interval,signal_buy,signal_sell

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#************************************************** Last Signals With Weight ******************************************************************************
def Signal(best_signals,buy_signal,sell_signal,len_price):
	#**** 
	#the inputs of Functions Must read From Data Base Number's

	signal = pd.DataFrame()
	#signal['signal'] = np.nan
	#signal['power'] = np.nan
	#signal['index'] = np.nan

	if (buy_signal['index'][len(buy_signal)-1] > sell_signal['index'][len(sell_signal)-1]):
		signal['signal'] = ['buy']
		signal['index'] = buy_signal['index'][len(buy_signal)-1]

		if ((buy_signal['values'][len(buy_signal)-1] <= best_signals['buy'][0]) & (buy_signal['values'][len(buy_signal)-1] >= best_signals['buy'][2])):
			signal['power'] = np.mean(best_signals['power_buy']) * (2/(len_price - buy_signal['index'][len(buy_signal)-1] + 1))
		else:
			signal['power'] = np.mean(best_signals['power_buy']) * (1 - best_signals['alpha_buy']) * (2/(len_price - buy_signal['index'][len(buy_signal)-1] + 1))
	else:
		signal['signal'] = ['sell']
		signal['index'] = sell_signal['index'][len(sell_signal)-1]

		if ((sell_signal['values'][len(sell_signal)-1] <= best_signals['sell'][0]) & (sell_signal['values'][len(sell_signal)-1] >= best_signals['sell'][2])):
			signal['power'] = np.mean(best_signals['power_sell']) * (2/(len_price - sell_signal['index'][len(sell_signal)-1] + 1))
		else:
			signal['power'] = np.mean(best_signals['power_sell']) * (1 - best_signals['alpha_sell']) * (2/(len_price - sell_signal['index'][len(sell_signal)-1] + 1))

		#Add Interval From Index Last to Signal For Power Decreasing
	return signal

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#************************************************** USE OF Funcyions ******************************************************************************

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)


y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']
time = symbol_data_5M['AUDCAD_i']['time']

best_signals,buy_signal,sell_signal = Find_Best_interval(dataset = symbol_data_5M['AUDCAD_i'],period_low=2,period_high=5,Low_ApplyTo='close',High_ApplyTo='close',max_profit_buy=0.06,max_profit_sell=0.06,alpha_sell=0.1,alpha_buy=0.1)

signal = Signal(best_signals=best_signals ,buy_signal = buy_signal ,sell_signal = sell_signal,len_price=len(y1)-1)

print(signal)

plt.axvline(x = signal['index'][0], color = 'r', linestyle = '-')

plt.axhline(y = best_signals['buy'][0], color = 'r', linestyle = '-')
plt.axhline(y = best_signals['buy'][1], color = 'g', linestyle = '-')
plt.axhline(y = best_signals['buy'][2], color = 'r', linestyle = '-')

plt.axhline(y = best_signals['sell'][0], color = 'b', linestyle = '-')
plt.axhline(y = best_signals['sell'][1], color = 'g', linestyle = '-')
plt.axhline(y = best_signals['sell'][2], color = 'b', linestyle = '-')

print(np.mean(best_signals['power_buy']))
print('buy')
print(best_signals['buy'][0])
print(best_signals['buy'][1])
print(best_signals['buy'][2])

print('sell')
print(best_signals['sell'][0])
print(best_signals['sell'][1])
print(best_signals['sell'][2])

#plt.plot(signal_buy['index'], signal_buy['values'],'o', c='#FF5733')
#plt.plot(signal_sell['index'], signal_sell['values'],'o', c='g')
plt.plot(y1.index[0:-1], y1[0:-1], c='r')
#plt.plot(y1.index, sma_high, c='r')
plt.show()