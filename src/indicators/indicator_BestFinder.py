from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from fitter import Fitter, get_common_distributions, get_distributions
from sklearn.cluster import KMeans
import warnings as warnings
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

class BestFinder:

	def __init__(
				self,
				parameters
				):

		self.elements = dict({
							
							#************** Divergence:

							__class__.__name__ + '_n_clusters': parameters.elements[__class__.__name__ + '_n_clusters'],
							__class__.__name__ + '_alpha': parameters.elements[__class__.__name__ + '_alpha'],

							#////////////////////////

							})

	def Finder(self, signals, apply_to):

		alpha = self.elements[__class__.__name__ + '_alpha']
		if (
			apply_to == 'tp_pr' or
			apply_to == 'st_pr' 
			):
			signal_good = signals
		else:
			signal_good = signals.drop(signals['index'][signals['flag'] == 'st'])

		if (signal_good.empty == True): 
			best_signals_interval = pd.DataFrame(
											{
											'interval': [0,0,0],
											'power': [0,0,0],
											'alpha': [alpha,alpha,alpha],
											}
											)
			return best_signals_interval

		signal_good = signal_good.replace([np.inf, -np.inf], np.nan, inplace=False)
		signal_good = signal_good.drop(columns = ['index'])
		signal_good = signal_good.sort_values(by = ['index'])
		signal_good = signal_good.reset_index(drop=True)

		try:

			signal_final, kmeans = self.Clustere(signal_good = signal_good, apply_to = apply_to)

		except Exception as ex:
			#print('Kmeans Error  = ',ex)
			best_signals_interval = pd.DataFrame(
											{
											'interval': [0,0,0],
											'power': [0,0,0],
											'alpha': [alpha,alpha,alpha],
											}
											)
			return best_signals_interval





		#Fitting Model Finding ****************************
		data_X = self.DataPreparer(signal_pred_final = signal_final)

		#************************************ Finding Sell's ****************************

		dist_item, f = self.DistributePreparer(
												data = data_X,
												signal_pred_final = signal_final,
												distributions = ['expon', 'norm']
												)

		if dist_item != '':
			Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line = self.ValuesPreparer(
																														dist_items = dist_item,
																														f = f,
																														data = data_X,
																														signal_pred_final = signal_final,
																														alpha = self.elements[__class__.__name__ + '_alpha'],
																														kmeans_f = kmeans,
																														distributions = ['expon', 'norm']
																														)
		alpha = self.elements[__class__.__name__ + '_alpha']
		best_signals_interval = pd.DataFrame(
										{
										'interval': [Upper_Line,Mid_Line,Lower_Line],
										'power': [Power_Upper_Line,Power_Mid_Line,Power_Lower_Line],
										'alpha': [alpha,alpha,alpha],
										}
										)

		return best_signals_interval

		#//////////////////////////////////////////////////////////////////////////////////////

	def Clustere(self, signal_good, apply_to):

		kmeans = KMeans(
						n_clusters = self.elements[__class__.__name__ + '_n_clusters'], 
						random_state=0,
						init='k-means++',
						n_init=5,
						max_iter=5
						)
		signal_good_kmeans = signal_good[apply_to]
		signal_good_kmeans = signal_good_kmeans.dropna()
		#Model Fitting
		kmeans = kmeans.fit(signal_good_kmeans.to_numpy().reshape(-1,1))

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		signal_final = pd.DataFrame(Y, columns=['Y'])
		signal_final['power'] = Power
		signal_final = signal_final.sort_values(by = ['Y'])

		return signal_final, kmeans

	def DataPreparer(
					self,
					signal_pred_final
					):

		#Fitting Model Finding ****************************
		#Make To DataFrame With Extreme Points And Num Of Itteration For Distribution Functions:
		data_X = np.zeros(np.sum(signal_pred_final['power']))

		j = 0
		z = 0
		for elm in signal_pred_final['Y']:
			k = 0
			while k < signal_pred_final['power'].to_numpy()[j]:
				data_X[z] = elm
				k += 1
				z += 1
			j += 1

		data_X = np.sort(data_X)

		return data_X

	def DistributePreparer(
							self,
							data,
							signal_pred_final,
							distributions
							):
		#'rayleigh','nakagami','expon','foldnorm','dweibull',

		#Define Name Of Distributions that We Want To Use:
		#distributions = 

		#************************************ Finding Low Distribution Functions ****************************

		try:
			#Fitter Finding Best Function That Can Distribute Or Low Extremes:
			f = Fitter(
						data = data,
						xmin = np.min(data),
						xmax = np.max(data),
						bins = len(signal_pred_final['Y'])-1,
						distributions = distributions,
						timeout = 1,
						density = True
						)

			f.fit(
				amp = 1, 
				progress = False, 
				n_jobs = -1
				)

			#Getting the Name of Best Destributer Functions and that Parameters:
			dist_items = list(f.get_best(method = 'sumsquare_error').items())

		except Exception as ex:
			#print('DistP Error = ',ex)
			dist_items = ''

		return dist_items, f


	def ValuesPreparer(
						self,
						dist_items,
						f,
						data,
						signal_pred_final,
						alpha,
						kmeans_f,
						distributions
						):


		#************************************ Finding Low Distribution Functions ****************************

		try:
			#Getting the Name of Best Destributer Functions and that Parameters:
			dist_name = dist_items[0][0]
			dist_parameters = dist_items[0][1]
			#Finding Best Points Of Low Extremes With Best Distributed Function and That Parameters:
			if dist_name == 'expon':


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

				Power_Upper_Line = signal_pred_final['power'][
																		kmeans_f.predict(Upper_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])

				Power_Lower_Line = signal_pred_final['power'][
																		kmeans_f.predict(Lower_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])
				Power_Mid_Line = signal_pred_final['power'][
																		kmeans_f.predict(Mid_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])
			
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
				Power_Upper_Line = signal_pred_final['power'][
																	kmeans_f.predict(Upper_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
				Power_Lower_Line = signal_pred_final['power'][
																	kmeans_f.predict(Lower_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
				Power_Mid_Line = signal_pred_final['power'][
																	kmeans_f.predict(Mid_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
			if (
				Mid_Line >= Upper_Line or
				Mid_Line <= Lower_Line
				):
				if len(distributions) > 0:

					distributions.remove(dist_name)

					dist_item, f = self.DistributePreparer(
																data = data,
																signal_pred_final = signal_pred_final,
																distributions = distributions
																)
					Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line = self.ValuesPreparer(
																																dist_items = dist_item,
																																f = f,
																																data = data,
																																signal_pred_final = signal_pred_final,
																																alpha = self.elements[__class__.__name__ + '_alpha'],
																																kmeans_f = kmeans_f,
																																distributions = distributions
																																)
				else:
					Upper_Line = 0
					Lower_Line = 0
					Mid_Line = 0
					Power_Upper_Line = 0
					Power_Lower_Line = 0
					Power_Mid_Line = 0
			
		except Exception as ex:
			#print(ex)
			Upper_Line = 0
			Lower_Line = 0
			Mid_Line = 0
			Power_Upper_Line = 0
			Power_Lower_Line = 0
			Power_Mid_Line = 0

		return Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line