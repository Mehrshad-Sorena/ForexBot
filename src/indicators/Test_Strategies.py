import pandas as pd
import pandas_ta as ind
from log_get_data import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.cluster.vq import kmeans2

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ind.sma)
#help(ind.ichimoku)
#************************************************************************ Find Extremes ********************************************************************
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,500)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

macd = ind.macd(y1,fast = 12,slow = 26,signal = 9)

#plt.subplot(2, 1, 1)
#plt.plot(x,y1,color = 'r')
#plt.plot(x,y2,color = 'g')
#plt.plot(x,y3,color = 'b')
#plt.plot(x,y4,color = '#02d3e2')

#plt.subplot(2, 1, 2)
#plt.plot(x,macd[macd.columns[0]], color = 'b')
#plt.plot(x,macd[macd.columns[2]], color = 'r')
#plt.hist(macd[macd.columns[1]], color = 'g')

#plt.show()



#np.random.seed(0)
#rs = np.random.randn(200)
#xs = [0]
#for r in rs:
#   xs.append(xs[-1] * 0.9 + r)

column = macd.columns[0]

df = pd.DataFrame(macd, columns=[column])

n = 5  # number of points to be checked before and after

# Find local peaks

df['min'] = df.iloc[argrelextrema(df.MACD_12_26_9.values, comparator = np.less,
                    order=n)[0]][column]
df['max'] = df.iloc[argrelextrema(df.MACD_12_26_9.values, comparator = np.greater,
                    order=n)[0]][column]

# Plot results

#plt.scatter(df.index, df['min'], c='r')
#plt.scatter(df.index, df['max'], c='g')
#plt.plot(df.index, df['MACD_12_26_9'], c='b')

i = 0
data_extreme = np.zeros((len(symbol_data_5M['AUDCAD_i']['close'])))
for extreme in df['min']:
	if (extreme >= 0) | (extreme <= 0):
		data_extreme[i] = extreme
	i += 1
#print(data_extreme)
i = np.arange(0,i,1)

#plt.plot(i, data_extreme , c='r')
#plt.show()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#*********************************************************************** FlaT Finding ***********************************************************
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,160)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

ichi = ind.ichimoku(high = y3,low = y4,close = y1,tenkan = 9,kijun = 26,senkou = 52)

column = ichi[0].columns[0]
SPANA = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[1]
SPANB = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[2]
Tenkan = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[3]
Kijun = pd.DataFrame(ichi[0], columns=[column])

#SPANA_Duplicates = pd.DataFrame(SPANA[SPANA.duplicated(keep=False)])
#print(SPANA_Duplicates)

#count = SPANA.iloc[SPANA_Duplicates['ISA_9'].value_counts()]['ISA_9']
#print(count)

centroid, label = kmeans2(Kijun.dropna(), iter=10, k=10, minit='random')
#print(centroid,label)
counts = np.bincount(label)
#print(counts)
#for elm in centroid:
#	plt.axhline(y=elm, color='r', linestyle='-')
#plt.plot(Kijun.index, Kijun, c='#FF5733')
#plt.plot(SPANB.index, SPANB, c='g')
#plt.plot(Tenkan.index, Tenkan, c='r')
#plt.plot(Kijun.index, Kijun, c='b')
#plt.show()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************************************* Flat With Scikit Learn Methodes ************************************************
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score


symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,100)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

ichi = ind.ichimoku(high = y3,low = y4,close = y1,tenkan = 9,kijun = 26,senkou = 52)

column = ichi[0].columns[0]
SPANA = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[1]
SPANB = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[2]
Tenkan = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[3]
Kijun = pd.DataFrame(ichi[0], columns=[column])


X_train, X_test, y_train, y_test = train_test_split(Kijun.dropna(), Kijun.dropna().index, test_size=0.1,shuffle=True)
kmeans = KMeans(n_clusters=15, random_state=0)
#fitting
kmeans = kmeans.fit(X_train)
X_pred = kmeans.cluster_centers_
Y_pred = kmeans.labels_

#print(kmeans.score(X_test))
#print(y_test)
#print(Y_pred)

counts = np.bincount(Y_pred)
#print(counts)
mean_counts = np.mean(counts)
#print(counts)
i = 0
for elm in X_pred:
	if counts[i] >= (mean_counts/2):
		#plt.axhline(y=elm, color='g', linestyle='-')
		pass
	i += 1
#plt.plot(Kijun.index, Kijun, c='#FF5733')
#plt.plot(y1.index, y1, c='b')
#plt.show()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************************************* Cross Finding ************************************************
from scipy.optimize import fsolve
from shapely.geometry import LineString


symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,5000)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']
time = symbol_data_5M['AUDCAD_i']['time']

sma_low = ind.sma(y1 , length = 150)
sma_high = ind.sma(y1 , length = 200)

first_line = LineString(np.column_stack((x[199:], sma_low[199:])))
second_line = LineString(np.column_stack((x[199:], sma_high.dropna())))

intersection = first_line.intersection(second_line)

#intersected_df = pd.merge(sma_low[199:], sma_high.dropna(), how='inner')
#print(sma_low[199:])
#print(sma_high.dropna())
if intersection.geom_type == 'MultiPoint':
	
    plt.plot(*LineString(intersection).xy, 'o',c='g')
    cross = pd.DataFrame(*LineString(intersection).xy)
    cross_index = cross.index.to_numpy()
    cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
    cross['points'] = cross_index
    print(cross.points)
    
elif intersection.geom_type == 'Point':
    plt.plot(*intersection.xy, 'o',c='g')
    cross = pd.DataFrame(*intersection.xy)
    cross_index = cross.index.to_numpy()
    cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
    cross['points'] = cross_index
    print(cross.points)
    print(*intersection.xy)

plt.plot(y1.index, y1, c='#FF5733')
plt.plot(y1.index, sma_low, c='b')
plt.plot(y1.index, sma_high, c='r')
plt.show()