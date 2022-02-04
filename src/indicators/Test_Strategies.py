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


symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,400)

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
	
    #plt.plot(*LineString(intersection).xy, 'o',c='g')
    cross = pd.DataFrame(*LineString(intersection).xy)
    cross_index = cross.index.to_numpy()
    cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
    cross['points'] = cross_index
    #print(cross.points)
    
elif intersection.geom_type == 'Point':
    #plt.plot(*intersection.xy, 'o',c='g')
    cross = pd.DataFrame(*intersection.xy)
    cross_index = cross.index.to_numpy()
    cross = pd.DataFrame(cross.values.astype(int),columns=['index'])
    cross['points'] = cross_index
    #print(cross.points)
    #print(*intersection.xy)

#plt.plot(y1.index, y1, c='#FF5733')
#plt.plot(y1.index, sma_low, c='b')
#plt.plot(y1.index, sma_high, c='r')
#plt.show()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************************************* Trending Protect Resist Finding ************************************************
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,50000)


x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']
time = symbol_data_5M['AUDCAD_i']['time']
#Finding Extreme Points
extremes = pd.DataFrame(y4, columns=['low'])
extremes['high'] = y3
extremes['min'] = extremes.iloc[argrelextrema(extremes.low.values, comparator = np.less,order=2000)[0]]['low']
extremes['max'] = extremes.iloc[argrelextrema(extremes.high.values, comparator = np.greater,order=5000)[0]]['high']
#Optimization Points With Scoring: Training Points 
exterm_point = pd.DataFrame(extremes['min'].dropna(inplace=False))

exterm_point_train, exterm_point_test, y_train, y_test = train_test_split(exterm_point.values, exterm_point.index, 
    test_size=0.1,shuffle=True)

kmeans = KMeans(n_clusters=4, random_state=0)
#Model Fitting
kmeans = kmeans.fit(exterm_point_train)
exterm_point_pred = kmeans.cluster_centers_
Y_pred = kmeans.labels_

#exterm_point_pred = exterm_point_pred[np.where(exterm_point_pred > np.mean(exterm_point_pred))]


counts = np.bincount(Y_pred)
mean_counts = np.mean(counts)
index = np.arange(0,len(exterm_point_pred),1)

k = 0
for elm in exterm_point_pred:
    index[k] = pd.DataFrame(abs(exterm_point - elm)).idxmin()
    k += 1
#print(index)


#******* DataSet *********************
n = len(exterm_point_pred)
x = index#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
rs = check_random_state(0)
y = exterm_point_pred.reshape(len(exterm_point_pred))

#////////////////

#***** Model Fitting *****************
ir = IsotonicRegression(out_of_bounds="clip")
y_ = ir.fit_transform(x, y)

lr = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr.fit(x[:, np.newaxis], y)  # x needs to be 2d for LinearRegression

#///////////////////////

#********* Plot Fitting ************
segments = [[[i, y[i]], [i, y_[i]]] for i in range(n)]
lc = LineCollection(segments, zorder=0)
lc.set_array(np.ones(len(y)))
lc.set_linewidths(np.full(n, 0.5))

fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))

ax0.plot(y3.index,y3,c='r')
ax0.plot(x, y, "C0.", markersize=12)
ax0.plot(x, y_, "C1.-", markersize=12)
x = y3.index
ax0.plot(x, (lr.predict(x[:, np.newaxis])), "C2-")

ax0.add_collection(lc)
ax0.legend(("Training data", "Isotonic fit", "Linear fit"), loc="lower right")
ax0.set_title("Isotonic regression fit on noisy data (n=%d)" % n)

x_test = y3.index
ax1.plot(x_test, ir.predict(x_test), "C1-")
ax1.plot(ir.X_thresholds_, ir.y_thresholds_, "C1.", markersize=12)
ax1.set_title("Prediction function (%d thresholds)" % len(ir.X_thresholds_))

plt.show()