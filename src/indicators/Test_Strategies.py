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

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,24000)


x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']
time = symbol_data_5M['AUDCAD_i']['time']
#Finding Extreme Points
extremes_1 = pd.DataFrame(y4[(int((len(y3)-1) * 0.98)):(len(y3)-1)], columns=['low'])
extremes_2 = pd.DataFrame(y4[(int((len(y3)-1) * 0.93)):(len(y3)-1)], columns=['low'])
extremes_3 = pd.DataFrame(y4[(int((len(y3)-1) * 0.75)):(len(y3)-1)], columns=['low'])
extremes_4 = pd.DataFrame(y4[(int((len(y3)-1) * 0.0)):(len(y3)-1)], columns=['low'])

extremes_1['high'] = y3[(int((len(y3)-1) * 0.98)):(len(y3)-1)]
extremes_2['high'] = y3[(int((len(y3)-1) * 0.93)):(len(y3)-1)]
extremes_3['high'] = y3[(int((len(y3)-1) * 0.75)):(len(y3)-1)]
extremes_4['high'] = y3[(int((len(y3)-1) * 0.0)):(len(y3)-1)]

exterm_point_train, exterm_point_test, y_train, y_test = train_test_split(y3.values, y3.index,test_size=0.9,shuffle=True)

extremes_1['min'] = extremes_1.iloc[argrelextrema(extremes_1.low.values, comparator = np.less,order=20)[0]]['low']
extremes_1['max'] = extremes_1.iloc[argrelextrema(extremes_1.high.values, comparator = np.greater,order=20)[0]]['high']

extremes_2['min'] = extremes_2.iloc[argrelextrema(extremes_2.low.values, comparator = np.less,order=100)[0]]['low']
extremes_2['max'] = extremes_2.iloc[argrelextrema(extremes_2.high.values, comparator = np.greater,order=100)[0]]['high']

extremes_3['min'] = extremes_3.iloc[argrelextrema(extremes_3.low.values, comparator = np.less,order=500)[0]]['low']
extremes_3['max'] = extremes_3.iloc[argrelextrema(extremes_3.high.values, comparator = np.greater,order=500)[0]]['high']

extremes_4['min'] = extremes_4.iloc[argrelextrema(extremes_4.low.values, comparator = np.less,order=2000)[0]]['low']
extremes_4['max'] = extremes_4.iloc[argrelextrema(extremes_4.high.values, comparator = np.greater,order=2000)[0]]['high']
#Optimization Points With Scoring: Training Points 
exterm_point_1 = pd.DataFrame(extremes_1['max'].dropna(inplace=False))
exterm_point_2 = pd.DataFrame(extremes_2['max'].dropna(inplace=False))
exterm_point_3 = pd.DataFrame(extremes_3['max'].dropna(inplace=False))
exterm_point_4 = pd.DataFrame(extremes_4['max'].dropna(inplace=False))

kmeans = KMeans(n_clusters=5,init='k-means++', n_init=2, max_iter=2)
#Model Fitting
kmeans = kmeans.fit(exterm_point_1.values)
exterm_point_pred_1 = kmeans.cluster_centers_
Y_pred_1 = kmeans.labels_
counts_1 = np.bincount(Y_pred_1)
mean_counts_1 = np.mean(counts_1)
index_1 = np.arange(0,len(exterm_point_pred_1),1)
k = 0
for elm in exterm_point_pred_1:
    index_1[k] = (pd.DataFrame(abs(exterm_point_1 - elm)).idxmin())
    k += 1

kmeans = KMeans(n_clusters=4,init='k-means++', n_init=2, max_iter=2)
kmeans = kmeans.fit(exterm_point_2.values)
exterm_point_pred_2 = kmeans.cluster_centers_
Y_pred_2 = kmeans.labels_
counts_2 = np.bincount(Y_pred_2)
mean_counts_2 = np.mean(counts_2)
index_2 = np.arange(0,len(exterm_point_pred_2),1)
k = 0
for elm in exterm_point_pred_2:
    index_2[k] = (pd.DataFrame(abs(exterm_point_2 - elm)).idxmin())
    k += 1

kmeans = KMeans(n_clusters=4,init='k-means++', n_init=2, max_iter=2)
kmeans = kmeans.fit(exterm_point_3.values)
exterm_point_pred_3 = kmeans.cluster_centers_
Y_pred_3 = kmeans.labels_
counts_3 = np.bincount(Y_pred_3)
mean_counts_3 = np.mean(counts_3)
index_3 = np.arange(0,len(exterm_point_pred_3),1)
k = 0
for elm in exterm_point_pred_3:
    index_3[k] = (pd.DataFrame(abs(exterm_point_3 - elm)).idxmin())
    k += 1

kmeans = KMeans(n_clusters=3,init='k-means++', n_init=2, max_iter=2)
kmeans = kmeans.fit(exterm_point_4.values)
exterm_point_pred_4 = kmeans.cluster_centers_
Y_pred_4 = kmeans.labels_
counts_4 = np.bincount(Y_pred_4)
mean_counts_4 = np.mean(counts_4)
index_4 = np.arange(0,len(exterm_point_pred_4),1)
k = 0
for elm in exterm_point_pred_4:
    index_4[k] = (pd.DataFrame(abs(exterm_point_4 - elm)).idxmin())
    k += 1

#******* DataSet *********************
n_1 = len(exterm_point_pred_1)
x_1 = index_1#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
y_1 = exterm_point_pred_1.reshape(len(exterm_point_pred_1))

n_2 = len(exterm_point_pred_2)
x_2 = index_2#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
y_2 = exterm_point_pred_2.reshape(len(exterm_point_pred_2))

n_3 = len(exterm_point_pred_3)
x_3 = index_3#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
y_3 = exterm_point_pred_3.reshape(len(exterm_point_pred_3))

n_4 = len(exterm_point_pred_4)
x_4 = index_4#extremes['max'].dropna(inplace=False).index#np.arange(0,len(extremes['max'].dropna(inplace=False)),1)
y_4 = exterm_point_pred_4.reshape(len(exterm_point_pred_4))

#////////////////

#***** Model Fitting *****************
ir_1 = IsotonicRegression(out_of_bounds="clip")
y__1 = ir_1.fit_transform(x_1, y_1)

lr_1 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_1.fit(x_1[:, np.newaxis], y_1)  # x needs to be 2d for LinearRegression

ir_2 = IsotonicRegression(out_of_bounds="clip")
y__2 = ir_1.fit_transform(x_2, y_2)

lr_2 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_2.fit(x_2[:, np.newaxis], y_2)  # x needs to be 2d for LinearRegression

ir_3 = IsotonicRegression(out_of_bounds="clip")
y__3 = ir_3.fit_transform(x_3, y_3)

lr_3 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_3.fit(x_3[:, np.newaxis], y_3)  # x needs to be 2d for LinearRegression

ir_4 = IsotonicRegression(out_of_bounds="clip")
y__4 = ir_4.fit_transform(x_4, y_4)

lr_4 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_4.fit(x_4[:, np.newaxis], y_4)  # x needs to be 2d for LinearRegression

#///////////////////////



#********* Plot Fitting ************
segments = [[[i, y_4[i]], [i, y__4[i]]] for i in range(n_4)]
#lc = LineCollection(segments, zorder=0)
#lc.set_array(np.ones(len(y_4)))
#lc.set_linewidths(np.full(n_4, 0.5))

#fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))

#ax0.plot(y1.index,y1,c='g')
#ax0.plot(x_1, y_1, "C0.", markersize=12)
#ax0.plot(x_1, y__1, "C0.-", markersize=12)
x_1 = index_1
#ax0.plot(x_1, lr_1.predict(x_1[:, np.newaxis]), "C0-",c='r')

#ax0.plot(x_2, y_2, "C1.", markersize=2)
#ax0.plot(x_2, y__2, "C1.-", markersize=2)
x_2 = index_2
#ax0.plot(x_2, lr_2.predict(x_2[:, np.newaxis]), "C1-",c='b')

#ax0.plot(x_3, y_3, "C2.", markersize=12)
#ax0.plot(x_3, y__3, "C2.-", markersize=12)
x_3 = index_3
#ax0.plot(x_3, (lr_3.predict(x_3[:, np.newaxis])), "C2-",c='g')

#ax0.plot(x_4, y_4, "C3.", markersize=12)
#ax0.plot(x_4, y__4, "C3.-", markersize=12)
x_4 = index_4
#ax0.plot(x_4, (lr_4.predict(x_4[:, np.newaxis])), "C3-")

#***** Model Fitting Total *****************

y_tot = np.concatenate((lr_1.predict(x_1[:, np.newaxis]), lr_2.predict(x_2[:, np.newaxis]),
    lr_3.predict(x_3[:, np.newaxis]),lr_4.predict(x_4[:, np.newaxis])),axis=None)
x_tot = np.concatenate((index_1,index_2,index_3,index_4),axis=None)

ir_tot = IsotonicRegression(out_of_bounds="clip")
y__tot = ir_tot.fit_transform(x_tot, y_tot)

lr_tot = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
lr_tot.fit(x_tot[:, np.newaxis], y_tot)  # x needs to be 2d for LinearRegression

#ax0.plot(x_tot, y_tot, "C4.", markersize=1)
#ax0.plot(x_tot, y__tot, "C4.-", markersize=1)
x_tot = x_tot
#ax0.plot(x_tot, (lr_tot.predict(x_tot[:, np.newaxis])), "C4-")

#///////////////////////
#ax0.add_collection(lc)
#ax0.legend(("Training data", "Isotonic fit", "Linear fit"), loc="lower right")
#ax0.set_title("Isotonic regression fit on noisy data (n=%d)" % n_4)

x_test = x_tot
#ax1.plot(x_test, ir_tot.predict(x_test), "C7-")
#ax1.plot(ir_tot.X_thresholds_, ir_tot.y_thresholds_, "C1.", markersize=12)
#ax1.set_title("Prediction function (%d thresholds)" % len(ir_tot.X_thresholds_))

plt.show()

#*********************************** Test Function in my Mind *********************
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,4000)


x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']
time = symbol_data_5M['AUDCAD_i']['time']

#print(np.max(y1))
alfa = 0.9
exp_closes = np.mean(y1)
j = 0
#for i in y1:
exp_closes = (1/(1 + np.exp(-1 * alfa * y1)))
    #j += 1
#print(j)
exp_closes = (exp_closes/np.max(exp_closes))
exp_closes = (exp_closes) * y1
#print(type(exp_closes))

sum_exp = np.zeros(len(y1))
#sum_exp[0] = exp_closes[0]
#print(sum_exp[0])
sigma = 0
j = 0
for i in exp_closes:
    sigma = (sigma + i) * i
    sum_exp[j] = sigma
    j += 1
#print(np.max(y1))
sum_exp = (sum_exp/np.max(sum_exp)) + np.max(y1)
sum_exp = (sum_exp/np.max(sum_exp)) * y1
#print(sum_exp)
#plt.plot(y1.index, y1, c='b')
#plt.plot(y1.index, exp_closes, c='r')
#plt.plot(np.arange(0,len(y1),1), sum_exp, c='g')
#plt.show()

from scipy import stats
from scipy.stats import norm

print(stats.norm.__doc__)
print('bounds of distribution lower: %s, upper: %s' % norm.support())
pdf = (norm.pdf(y1)) * y1
sum_exp = np.zeros(len(y1))
sigma = 0
j = 0
for i in pdf:
    sigma = (sigma + i)
    sum_exp[j] = sigma
    j += 1
sum_exp=sum_exp

#fig ,ax = plt.subplots(1, 1)
#ax.hist(pdf, density=True, histtype='stepfilled', alpha=0.2)
#ax.legend(loc='best', frameon=False)
plt.plot(sum_exp,y1, c='g')
plt.show()

from scipy.interpolate import interp1d
x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
print(f)
f2 = interp1d(x, y, kind='cubic')
print(f2)
xnew = np.linspace(0, 10, num=41, endpoint=True)
print(f(xnew))
import matplotlib.pyplot as plt
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()
