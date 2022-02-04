import pandas as pd
import pandas_ta as ind
from log_get_data import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

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
def Extreme_points(high,low,number_min,number_max,number_centers,Size_of_test=0.1):
	
	extremes = pd.DataFrame(low, columns=['low'])
	extremes['high'] = high

	#Finding Extreme Points
	extremes['min'] = extremes.iloc[argrelextrema(extremes.low.values, comparator = np.less,order=number_max)[0]]['low']
	extremes['max'] = extremes.iloc[argrelextrema(extremes.high.values, comparator = np.greater,order=number_max)[0]]['high']

	#Optimization Points With Scoring: Training Points 
	exterm_point = pd.DataFrame(np.concatenate((extremes['max'].dropna().to_numpy(), 
		extremes['min'].dropna().to_numpy()), axis=None),columns=['extremes'])

	exterm_point_train, exterm_point_test, y_train, y_test = train_test_split(exterm_point.values, exterm_point.index, 
		test_size=Size_of_test,shuffle=True)

	kmeans = KMeans(n_clusters=number_centers, random_state=0)
	#Model Fitting
	kmeans = kmeans.fit(exterm_point_train)
	exterm_point_pred = kmeans.cluster_centers_
	Y_pred = kmeans.labels_

	counts = np.bincount(Y_pred)
	mean_counts = np.mean(counts)

	return exterm_point_pred
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ichimoko Lines *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ramp Lines *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** olgooie parcam *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,50000)
symbol_data_1D,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,2500)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

local_extreme = pd.DataFrame(Extreme_points(high=symbol_data_1D['AUDCAD_i']['high'],low=symbol_data_1D['AUDCAD_i']['low'],
	number_min=2,number_max=2,number_centers=10,Size_of_test=0.2))
for point in local_extreme.values:
	plt.axhline(y=point, color='r', linestyle='-')

plt.plot(y3.index, y3, c='b')
plt.plot(y4.index, y4, c='#FF5733')
plt.show()