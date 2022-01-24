import pandas as pd
import pandas_ta as ind
from log_get_data import *

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
help(ind.sma)

#**************************************************** Golden Cross *******************************************************
def Golden_Cross_SMA(dataset,Low_Period,High_Period,Low_ApplyTo,High_ApplyTo):
	SMA_Low = ind.sma(dataset[Low_ApplyTo], lenghth = Low_Period)
	SMA_High = ind.sma(dataset[High_ApplyTo], lenghth = High_Period)

	Signal_SMA = {
		"index": 0,
		'signal': "no_trade",
		'score': 0
	}

	data_length = len(dataset[Low_ApplyTo]) - 1

	if ((SMA_Low[data_length] > SMA_High[data_length]) & (SMA_Low[data_length-2] < SMA_High[data_length-2])):
		Signal_SMA = {
		"index": data_length,
		'signal': "buy",
		'score': 0
		}
	elif ((SMA_Low[data_length] > SMA_High[data_length]) & (SMA_Low[data_length-2] < SMA_High[data_length-2])):
		Signal_SMA = {
		"index": data_length,
		'signal': "sell",
		'score': 0
		}
	else:
		Signal_SMA = {
		"index": data_length,
		'signal': "no_trade",
		'score': 0
		}
	return Signal_SMA
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Scalpe *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#************************************************** USE OF Funcyions ******************************************************************************
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,500)

print(Golden_Cross_SMA(dataset = symbol_data_5M['AUDCAD_i'], Low_Period = 100, High_Period = 200, Low_ApplyTo = 'close', High_ApplyTo = 'high'))