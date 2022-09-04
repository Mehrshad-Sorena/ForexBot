from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from fitter import Fitter, get_common_distributions, get_distributions
from sklearn.cluster import KMeans
from scipy import stats
import pandas as pd
import numpy as np
import fitter
import time
import math

#**************************************************** Best Extreme Finder ***************************************************
#This Function is Calculating With Distribution Functions:
#Goal: Calculate Two Best Points Of Tp And St
def best_extreme_finder(
						exterm_point,
						high,
						low,
						n_clusters_low,
						n_clusters_high,
						alpha_low,
						alpha_high,
						timeout_break
						):

	#************************ Help ***********************************************************
	#exterm_point: All Extreme Points From Protection Resistion Functions
	#n_clusters: Number Of Mean Centers Of Extreme Points, **** Must Be Optimazing and save in Database ****
	#high: the High Level Of Candles from that Time Frame You want
	#low: the Low Level Of Candles from that Time Frame You want
	#alpha: the Accuracy of Finding Best Protection Or Resistation, **** Must Be Optimazing and save in Database ****
	#timeout_break: Maximum Time Out For Running this Optimizer
	#/////////////////////////////////////////////////////////////////////////////////////////

	timeout = time.time() + timeout_break  # timeout_break Sec from now

	exterm_point_pred_final_high, exterm_point_pred_final_low, kmeans_high, kmeans_low = clustering_points(
																											low = low,
																											high = high,
																											n_clusters_low = n_clusters_low,
																											n_clusters_high = n_clusters_high,
																											exterm_point = exterm_point
																											)

	if (
		exterm_point_pred_final_low == '' or
		exterm_point_pred_final_high == ''
		):
		best_extremes = pd.DataFrame()
		best_extremes['high'] = [0, 0, 0]
		best_extremes['power_high'] = [0, 0, 0]
		best_extremes['low'] = [0, 0, 0]
		best_extremes['power_low'] = [0, 0, 0]
		return best_extremes

	data_X_high, data_X_low = data_distriute_get(
												exterm_point_pred_final_high = exterm_point_pred_final_high,
												exterm_point_pred_final_low = exterm_point_pred_final_low,
												)

	timeout = time.time() + timeout_break  # timeout_break Sec from now

	#************************************ Finding Low Distribution Functions ****************************

	dist_items, f_low = best_distribute_finder(
												data = data_X_low,
												exterm_point_pred_final = exterm_point_pred_final_low
												)

	if dist_items != '':
		Upper_Line_low, 
		Mid_Line_low, 
		Lower_Line_low, 
		Power_Upper_Line_low, 
		Power_Mid_Line_low, 
		Power_Lower_Line_low = best_values_get(
												dist_items = dist_items,
												f = f_low,
												data = data_X_low,
												exterm_point_pred_final = exterm_point_pred_final_low,
												alpha = alpha_low,
												kmeans_f = kmeans_low
												)
	#//////////////////////////////////////////////////////////////////////////////////////

	#************************************ Finding High *************************************

	dist_items, f_high = best_distribute_finder(
												data = data_X_high,
												exterm_point_pred_final = exterm_point_pred_final_high
												)

	if dist_items != '':
		Upper_Line_high, 
		Mid_Line_high, 
		Lower_Line_high, 
		Power_Upper_Line_high, 
		Power_Mid_Line_high, 
		Power_Lower_Line_high = best_values_get(
												dist_items = dist_items,
												f = f_high,
												data = data_X_high,
												exterm_point_pred_final = exterm_point_pred_final_high,
												alpha = alpha_high,
												kmeans_f = kmeans_high
												)

	#/////////////////////////////////////////////////////////////////////////////////////////////

	#Define DataFrame For OutPuts:
	#Out Best High Point And Best Low Points With Powers:
	best_extremes = pd.DataFrame()
	best_extremes['high'] = [
							Upper_Line_high,
							Mid_Line_high,
							Lower_Line_high
							]

	best_extremes['power_high'] = [
									Power_Upper_Line_high,
									Power_Mid_Line_high,
									Power_Lower_Line_high
									]

	best_extremes['low'] = [
							Upper_Line_low,
							Mid_Line_low,
							Lower_Line_low
							]

	best_extremes['power_low'] = [
									Power_Upper_Line_low,
									Power_Mid_Line_low,
									Power_Lower_Line_low
									]

	return best_extremes
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************

def clustering_points(
						low,
						high,
						n_clusters_low,
						n_clusters_high,
						exterm_point
						):

	#Some times Number Of Clusters not Equal To Number Of Powers, That Need Run And Run To Finding Correct Clusters:
	try:
		#Maybe Num of Clusters is Greater than Number Of Extremes:
		if (
			len(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1)) > 25
			):

			n_clusters_low = 5

		else:
			n_clusters_low = int(len(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1))/4)


		if (
			len(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1)) > 25
			):

			n_clusters_high = 5

		else:
			n_clusters_high = int(len(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1))/4)



		#Defining Kmeans Algo For Points that Lower Of Latest Low Price Candle:
		kmeans_low = KMeans(
							n_clusters=n_clusters_low, 
							random_state=0,
							init='k-means++',
							n_init=2,
							max_iter=3
							)

		#Defining Kmeans Algo For Points that Higher Of Latest High Price Candle:
		kmeans_high = KMeans(
							n_clusters=n_clusters_high, 
							random_state=0,
							init='k-means++',
							n_init=2,
							max_iter=3
							)

		#Model Fitting KMeans To Low Extreme Points:
		kmeans_low = kmeans_low.fit(
									exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']<=high[len(high)-1])].reshape(-1,1), 
									sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']<=high[len(high)-1])]
									)

		##Model Fitting KMeans To High Extreme Points:
		kmeans_high = kmeans_high.fit(
									exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']>=low[len(low)-1])].reshape(-1,1), 
									sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']>=low[len(low)-1])]
									)
		
		#kmeans_low = kmeans_low.fit(exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']<=low[len(low)-1])].reshape(-1,1), sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']<=low[len(low)-1])])
		#kmeans_high = kmeans_high.fit(exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes']>=high[len(high)-1])].reshape(-1,1), sample_weight= exterm_point['power'].to_numpy()[np.where(exterm_point['extremes']>=high[len(high)-1])])


		Y_low = kmeans_low.cluster_centers_
		Y_high = kmeans_high.cluster_centers_
	
		Power_low = kmeans_low.fit_predict(low.to_numpy()[np.where(low<=high[len(high)-1])].reshape(-1,1))
		Power_high = kmeans_high.fit_predict(high.to_numpy()[np.where(high>=low[len(low)-1])].reshape(-1,1))

		X_low = kmeans_low.cluster_centers_
		X_high = kmeans_high.cluster_centers_

		#Power_low = kmeans_low.labels_
		#Power_high = kmeans_high.labels_
		

		Power_low = np.bincount(Power_low)
		Power_high = np.bincount(Power_high)

		#Define DataFrame For All Of Extreme Clusters With Num Of Itteration Of Each:
		#For Low Points:
		exterm_point_pred_final_low = pd.DataFrame(X_low, columns=['X'])
		exterm_point_pred_final_low['Y'] = Y_low
		exterm_point_pred_final_low['power'] = Power_low
		exterm_point_pred_final_low = exterm_point_pred_final_low.sort_values(by = ['X'])


		#Define DataFrame For All Of Extreme Clusters With Num Of Itteration Of Each:
		#For High Points:
		exterm_point_pred_final_high = pd.DataFrame(X_high, columns=['X'])
		exterm_point_pred_final_high['Y'] = Y_high
		exterm_point_pred_final_high['power'] = Power_high
		exterm_point_pred_final_high = exterm_point_pred_final_high.sort_values(by = ['X'])

	except Exception as ex:
		exterm_point_pred_final_low = ''
		exterm_point_pred_final_high = ''


	return exterm_point_pred_final_high, exterm_point_pred_final_low, kmeans_high, kmeans_low

#/////////////////////

#********************

def data_distriute_get(
						exterm_point_pred_final_high,
						exterm_point_pred_final_low
						):

	#Fitting Model Finding ****************************
	#Make To DataFrame With Extreme Points And Num Of Itteration For Distribution Functions:
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

	return data_X_high, data_X_low


#///////////////////

#*********************

def best_distribute_finder(
							data,
							exterm_point_pred_final
							):
	#'rayleigh','nakagami','expon','foldnorm','dweibull',

	#Define Name Of Distributions that We Want To Use:
	distributions = ['expon','norm']


	#************************************ Finding Low Distribution Functions ****************************

	try:
		#Fitter Finding Best Function That Can Distribute Or Low Extremes:
		f = Fitter(
					data = data,
					xmin=np.min(data),
					xmax=np.max(data),
					bins = len(exterm_point_pred_final['X'])-1,
					distributions = distributions,
					timeout=0.1,
					density=True
					)

		f.fit(
			amp=1, 
			progress=False, 
			n_jobs=-1
			)

		#Getting the Name of Best Destributer Functions and that Parameters:
		dist_items = list(f_low.get_best(method = 'sumsquare_error').items())

	except Exception as ex:
		dist_items = ''

	return dist_items, f

#/////////////////////

#*********************

def best_values_get(
					dist_items,
					f,
					data,
					exterm_point_pred_final,
					alpha,
					kmeans_f
					):


	#************************************ Finding Low Distribution Functions ****************************

	try:
		#Getting the Name of Best Destributer Functions and that Parameters:
		dist_name = dist_items[0][0]
		dist_parameters = dist_items[0][1]

		#Finding Best Points Of Low Extremes With Best Distributed Function and That Parameters:
		if (
			dist_name == 'expon'
			):

			Y = f.fitted_pdf['expon']
			#Using Probability Distribution Function From Scipy Library:
			Y = expon.pdf(
							x=data, 
							loc=dist_parameters['loc'], 
							scale=dist_parameters['scale']
							)
			#Finding Best Interval Low Points:
			Extereme = expon.interval(
									alpha=alpha, 
									loc=dist_parameters['loc'], 
									scale=dist_parameters['scale']
									)

			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])

			Power_Upper_Line = exterm_point_pred_final['power'][
																	kmeans_f.predict(Upper_Line.reshape(1,-1))
																	].to_numpy()/np.max(exterm_point_pred_final['power'])

			Power_Lower_Line = exterm_point_pred_final['power'][
																	kmeans_f.predict(Lower_Line.reshape(1,-1))
																	].to_numpy()/np.max(exterm_point_pred_final['power'])
			Power_Mid_Line = exterm_point_pred_final['power'][
																	kmeans_f.predict(Mid_Line_low.reshape(1,-1))
																	].to_numpy()/np.max(exterm_point_pred_final['power'])
		
		elif dist_name == 'norm':

			Y = f.fitted_pdf['norm']

			Y = norm.pdf(
						x=data, 
						loc=dist_parameters['loc'], 
						scale=dist_parameters['scale']
						)

			Extereme = norm.interval(
									alpha=alpha, 
									loc=dist_parameters['loc'], 
									scale=dist_parameters['scale']
									)

			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = exterm_point_pred_final['power'][
																kmeans_f.predict(Upper_Line.reshape(1,-1))
																].to_numpy()/np.max(exterm_point_pred_final['power'])
			Power_Lower_Line = exterm_point_pred_final['power'][
																kmeans_f.predict(Lower_Line.reshape(1,-1))
																].to_numpy()/np.max(exterm_point_pred_final['power'])
			Power_Mid_Line = exterm_point_pred_final['power'][
																kmeans_f.predict(Mid_Line.reshape(1,-1))
																].to_numpy()/np.max(exterm_point_pred_final['power'])


		"""
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
		
		"""
	except Exception as ex:
		Upper_Line = 0
		Lower_Line = 0
		Mid_Line = 0
		Power_Upper_Line = 0
		Power_Lower_Line = 0
		Power_Mid_Line = 0

	return Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line
		

#////////////////////