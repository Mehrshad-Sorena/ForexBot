from pr_Parameters import Parameters
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from pr_Config import Config
from timer import stTime
import pandas_ta as ind
import pandas as pd
import numpy as np

#**************************************************** Ichimoko Lines *******************************************************
#This Function is Used for Finding Flat Lines in ichimoku:
class IchimokouFlatLines:

	parameters = Parameters()
	config = Config()

	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict(
							{

							__class__.__name__ + '_tenkan_5M': parameters.elements[__class__.__name__ + '_tenkan_5M'],
							__class__.__name__ + '_kijun_5M': parameters.elements[__class__.__name__ + '_kijun_5M'],
							__class__.__name__ + '_senkou_5M': parameters.elements[__class__.__name__ + '_senkou_5M'],

							__class__.__name__ + '_n_cluster_5M': parameters.elements[__class__.__name__ + '_n_cluster_5M'],

							__class__.__name__ + '_weight_5M': parameters.elements[__class__.__name__ + '_weight_5M'],

							__class__.__name__ + '_tenkan_1H': parameters.elements[__class__.__name__ + '_tenkan_1H'],
							__class__.__name__ + '_kijun_1H': parameters.elements[__class__.__name__ + '_kijun_1H'],
							__class__.__name__ + '_senkou_1H': parameters.elements[__class__.__name__ + '_senkou_1H'],

							__class__.__name__ + '_n_cluster_1H': parameters.elements[__class__.__name__ + '_n_cluster_1H'],

							__class__.__name__ + '_weight_1H': parameters.elements[__class__.__name__ + '_weight_1H'],


							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],
							}
							)

		self.cfg = dict(
						{
						__class__.__name__ + '_T_5M': config.cfg[__class__.__name__ + '_T_5M'],
						__class__.__name__ + '_T_1H': config.cfg[__class__.__name__ + '_T_1H'],
						__class__.__name__ + '_status': config.cfg[__class__.__name__ + '_status'],

						__class__.__name__ + '_plot': config.cfg[__class__.__name__ + '_plot'],
						}
						)

	#****************** Preparer
	def IchiPreparer(
					self,
					ichi
					):

		#Separate SPANA in one DataFrame:
		column = ichi[0].columns[0]
		SPANA = pd.DataFrame(
							ichi[0], 
							columns=[column]
							)

		#Separate SPANB in one DataFrame:
		column = ichi[0].columns[1]
		SPANB = pd.DataFrame(
							ichi[0], 
							columns=[column]
							)

		#Separate Tenkan in one DataFrame:
		column = ichi[0].columns[2]
		Tenkan = pd.DataFrame(
							ichi[0], 
							columns=[column]
							)

		#Separate Kihun in one DataFrame:
		column = ichi[0].columns[3]
		Kijun = pd.DataFrame(
							ichi[0], 
							columns=[column]
							)


		#Define empty DataFrames:

		Tenkan_train = pd.DataFrame({
									'flat': Tenkan.dropna().values.reshape(len(Tenkan.dropna())),
									'power': np.ones(len(Tenkan.dropna()))*1
									})
		
		Kijun_train = pd.DataFrame({
									'flat': Kijun.dropna().values.reshape(len(Kijun.dropna())),
									'power': np.ones(len(Kijun.dropna()))*1
									})

		SPANA_train = pd.DataFrame({
									'flat': SPANA.dropna().values.reshape(len(SPANA.dropna())),
									'power': np.ones(len(SPANA.dropna()))*2
									})

		SPANB_train = pd.DataFrame({
									'flat': SPANB.dropna().values.reshape(len(SPANB.dropna())),
									'power': np.ones(len(SPANB.dropna()))*2
									})

		#Define DataFrame for flating in Kijun, SPANA, SPANB:
		Three_train_1 = pd.DataFrame(
									np.concatenate(
													(
														Kijun_train['flat'].to_numpy(),
														SPANA_train['flat'].to_numpy(),
														SPANB_train['flat'].to_numpy()
													),
													axis = None
													),
									columns=['flat']
									)

		Three_train_1['power'] = np.ones(len(Three_train_1))*3


		#Define DataFrame for flating in tENKAN, SPANA, SPANB:
		Three_train_2 = pd.DataFrame(
									np.concatenate(
													(
														Tenkan_train['flat'].to_numpy(),
														SPANA_train['flat'].to_numpy(),
														SPANB_train['flat'].to_numpy()
													),
													axis = None
													),
									columns=['flat']
									)

		Three_train_2['power'] = np.ones(len(Three_train_2))*3


		#Define DataFrame for flating in Tenkan, Kijun, SPANA, SPANB:
		Four_train = pd.DataFrame(
								np.concatenate(
												(
													Tenkan_train['flat'].to_numpy(),
													Kijun_train['flat'].to_numpy(),
													SPANA_train['flat'].to_numpy(),
													SPANB_train['flat'].to_numpy()
												),
												axis = None
												),
								columns=['flat']
								)

		Four_train['power'] = np.ones(len(Four_train))*4

		return Tenkan_train, Kijun_train, SPANA_train, SPANB_train, Three_train_1, Three_train_2, Four_train
	#///////////////////////////////

	#************* ichi

	def Ichimokou(
				self,
				timeframe
				):
		#Calculate ichimoku:
		ichi = ind.ichimoku(
							high = self.elements['dataset_' + timeframe].high,
							low = self.elements['dataset_' + timeframe].low,
							close = self.elements['dataset_' + timeframe].close,
							tenkan = self.elements[__class__.__name__ + '_tenkan_' + timeframe],
							kijun = self.elements[__class__.__name__ + '_kijun_' + timeframe],
							senkou = self.elements[__class__.__name__ + '_senkou_' + timeframe]
							)
		return ichi

	#/////////////////////////////


	#*************** Optimizer:

	def optimizer(
					self,
					timeframe,
					flat_lines
					):

		#Define KMeans Algo Module From Scikit-learn library:
		kmeans = KMeans(
						n_clusters=self.elements[__class__.__name__ + '_n_cluster_' + timeframe],
						random_state=0,
						init='k-means++',
						n_init=2,
						max_iter=3
						)
		
		#Fitting KMeans for Flat Lines Of ichimokou For finding where ichimokou is Flated:
		kmeans = kmeans.fit(
							flat_lines['flats'].to_numpy().reshape(-1,1),
							sample_weight= flat_lines['power'].to_numpy()
							)

		#Value of where ichimoku flat lines:
		X_pred = kmeans.cluster_centers_
		#Vlaue of itterated lines and how much Power of flat lines:
		Power = np.bincount(kmeans.labels_)


		#Define a DataFrame For Flats Output With Power:
		flat_lines_pred = pd.DataFrame(
										X_pred, 
										columns=['extreme']
										)
		#weight Can Changed with TimeFrame, Example For 5M is 400, For 1H is 4800:
		flat_lines_pred['power'] = Power * self.elements[__class__.__name__ + '_weight_' + timeframe]

		return flat_lines_pred

	#///////////////////////////////

	#****************** Finder:
	def finder(
				self,
				timeframe
				):

		Tenkan_train, Kijun_train, SPANA_train, SPANB_train, Three_train_1, Three_train_2, Four_train = self.IchiPreparer(self.Ichimokou(timeframe = timeframe))
		#Concatenate All DataFrames:
		flat_lines = pd.DataFrame(
									np.concatenate(
													(
														Tenkan_train['flat'].to_numpy(), 
														Kijun_train['flat'].to_numpy(),
														SPANA_train['flat'].to_numpy(),
														SPANB_train['flat'].to_numpy(),
														Three_train_1['flat'].to_numpy(),
														Three_train_2['flat'].to_numpy(),
														Four_train['flat'].to_numpy()
														), 
													axis=None
													),
									columns=['flats']
									)

		#Defininge Power Column in final DataFrame:
		flat_lines['power'] = np.concatenate(
												(
													Tenkan_train['power'].to_numpy(),
													Kijun_train['power'].to_numpy(),
													SPANA_train['power'].to_numpy(),
													SPANB_train['power'].to_numpy(),
													Three_train_1['power'].to_numpy(),
													Three_train_2['power'].to_numpy(),
													Four_train['power'].to_numpy()
													), 
												axis=None
												)

		flat_lines_pred = self.optimizer(flat_lines = flat_lines, timeframe = timeframe)
		

		return flat_lines_pred
	#///////////////////////////////////


	#************ Get:
	
	def get(
			self,
			timeframe
			):
		#Finding Extremes From Time Frame
		flat_lines = pd.DataFrame(np.nan, index=[0], columns=['extreme','power'])
		
		if (
			self.cfg[__class__.__name__ + '_T_' + timeframe] == True and
			self.cfg[__class__.__name__ + '_status'] == True
			):
			flat_lines = self.finder(timeframe = timeframe)

		return flat_lines

	def ploter(self):

		if self.cfg[__class__.__name__ + '_plot'] == True:
			if self.cfg[__class__.__name__ + '_T_5M'] == True:
				ichi = self.Ichimokou(timeframe='5M')
				print(self.elements['dataset_5M'])
				points = self.get(timeframe='5M')

				for clm in ichi[0].columns:
					if 'ISA' in clm: color = '#008000'
					if 'ISB' in clm: color = '#FF0000'
					if 'ITS' in clm: color = '#8B0000'
					if 'IKS' in clm: color = '#0000FF'
					if 'ICS' in clm: color = '#7CFC00'
					data_plot = pd.DataFrame(
											ichi[0], 
											columns=[clm]
											)
					print(data_plot)
					plt.plot(data_plot.index, data_plot, color = color, label=clm)

				for point in points['extreme']:
					plt.axhline(y = point, c = 'black', linestyle = ':')

				plt.title(__class__.__name__ + '_5M')
				plt.xlabel('Time')
				plt.xlabel('Ichimokou')

				plt.show()

			if self.cfg[__class__.__name__ + '_T_1H'] == True:
				ichi = self.Ichimokou(timeframe='1H')
				points = self.get(timeframe='1H')

				for clm in ichi[0].columns:
					if 'ISA' in clm: color = '#008000'
					if 'ISB' in clm: color = '#FF0000'
					if 'ITS' in clm: color = '#8B0000'
					if 'IKS' in clm: color = '#0000FF'
					if 'ICS' in clm: color = '#7CFC00'
					data_plot = pd.DataFrame(
											ichi[0], 
											columns=[clm]
											)

					plt.plot(data_plot.index,data_plot, color = color, label=clm)

				for point in points['extreme']:
					plt.axhline(y = point, c = 'black', linestyle = ':')

				plt.title(__class__.__name__ + '_1H')
				plt.xlabel('Time')
				plt.xlabel('Ichimokou')

				plt.show()

