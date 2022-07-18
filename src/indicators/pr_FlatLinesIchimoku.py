from sklearn.cluster import KMeans
import pandas_ta as ind
import pandas as pd
import numpy as np

#**************************************************** Ichimoko Lines *******************************************************
#This Function is Used for Finding Flat Lines in ichimoku:
def flat_lines_ichimoko(
							high,
							low,
							close,
							tenkan=9,
							kijun=26,
							senkou=52,
							n_clusters=15,
							weight=1
							):
	
	#Calculate ichimoku:
	ichi = ind.ichimoku(
						high = high,
						low = low,
						close = close,
						tenkan = tenkan,
						kijun = kijun,
						senkou = senkou
						)

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
	Tenkan_train = pd.DataFrame()
	Tenkan_train['flat'] = Tenkan.dropna()
	Tenkan_train['power'] = np.ones(len(Tenkan_train))*1

	Kijun_train = pd.DataFrame()
	Kijun_train['flat'] = Kijun.dropna()
	Kijun_train['power'] = np.ones(len(Kijun_train))*1

	SPANA_train = pd.DataFrame()
	SPANA_train['flat'] = SPANA.dropna()
	SPANA_train['power'] = np.ones(len(SPANA_train))*2

	SPANB_train = pd.DataFrame()
	SPANB_train['flat'] = SPANB.dropna()
	SPANB_train['power'] = np.ones(len(SPANB_train))*2

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
								columns=['flats']
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
								columns=['flats']
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
							columns=['flats']
							)

	Four_train['power'] = np.ones(len(Four_train))*4


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

	flat_lines_pred = ichi_flat_optimizer(n_clusters=n_clusters,flat_lines=flat_lines,weight=weight)
	

	return flat_lines_pred
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ichi_flat_optimizer(
						n_clusters,
						flat_lines,
						weight
						):

						#Define KMeans Algo Module From Scikit-learn library:
						kmeans = KMeans(
										n_clusters=n_clusters,
										random_state=0
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
						flat_lines_pred['power'] = Power * weight

						return flat_lines_pred