import pandas as pd
import pandas_ta as ind
from log_get_data import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
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
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,500)

x = np.arange(0,len(symbol_data_5M['AUDCAD_i']['close']),1)
y1 = symbol_data_5M['AUDCAD_i']['close']
y2 = symbol_data_5M['AUDCAD_i']['open']
y3 = symbol_data_5M['AUDCAD_i']['high']
y4 = symbol_data_5M['AUDCAD_i']['low']

ichi = ind.ichimoku(high = y3,low = y4,close = y1,tenkan = 9,kijun = 26,senkou = 52)

column = ichi[0].columns[0]
SPANA = pd.DataFrame(ichi[0], columns=[column])
SPANA_copy = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[1]
SPANB = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[2]
Tenkan = pd.DataFrame(ichi[0], columns=[column])
column = ichi[0].columns[3]
Kijun = pd.DataFrame(ichi[0], columns=[column])

#SPANA_Duplicates = SPANA[SPANA.isin(SPANA[SPANA.duplicated(keep=False)])]
SPANA_Duplicates = pd.DataFrame(SPANA[SPANA.duplicated(keep=False)])
print(SPANA_Duplicates)
#SPANA_Duplicates = pd.DataFrame(SPANA.drop_duplicates(keep=False))
#print(SPANA_Duplicates)
#SPANA_Duplicates = SPANA_Duplicates.assign(e=pd.DataFrame(SPANA[SPANA.duplicated(keep=False)].value_counts()))
count = SPANA_Duplicates.value_counts()
print(count)
#print(pd.DataFrame(count).index)
#print(len(count))

i = np.arange(0,len(count),1)

plt.scatter(SPANA_Duplicates.index, SPANA_Duplicates, c='r')
plt.plot(SPANA.index, SPANA, c='#FF5733')
#plt.plot(SPANB.index, SPANB, c='g')
#plt.plot(Tenkan.index, Tenkan, c='r')
#plt.plot(Kijun.index, Kijun, c='b')
#plt.show()
