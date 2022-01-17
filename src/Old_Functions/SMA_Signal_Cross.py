import math
import pandas as pd

def cross_SMA(SMA_low,SMA_high,symbol):
	signal_buy = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}

	signal_sell = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}

	signal = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}

	i = len(SMA_low)-1


	while ((SMA_low[i] != True) & (SMA_high[i] != True)):
		if (((i+2) <= len(SMA_low)-1) & ((i-2) >= 0)):
			if ((SMA_low[i+2] < SMA_high[i+2]) & (SMA_low[i-2] > SMA_high[i-2])):
				signal = {
					"index": i,
					'signal': "sell",
					'symbol': symbol
					}
				break
			if ((SMA_low[i+2] > SMA_high[i+2]) & (SMA_low[i-2] < SMA_high[i-2])):
				signal = {
					"index": i,
					'signal': "buy",
					'symbol': symbol
					}
				break

		if ((i-2) < 0):
			break

		i -= 1

	return signal
