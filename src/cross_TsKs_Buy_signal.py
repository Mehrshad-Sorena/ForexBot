def cross_TsKs_Buy_signal(tenkan,kijun,symbol):

	signal_buy = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
	}

	signal_sell = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
	}

	signal = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
	}

	i = len(tenkan)-1

	while ((tenkan[i] != True) & (kijun[i] != True)):
		if (((i+5) <= len(tenkan)-1) & ((i-5) >= 0)):
			if (((tenkan[i-2] <= kijun[i-2]) & (tenkan[i-1] <= kijun[i-1])) 
				& ((tenkan[i-5] < kijun[i-5]) & (tenkan[i-4] < kijun[i-4])) 
				& ((tenkan[i-3] <= kijun[i-3])) 
				& ((tenkan[i+2] >= kijun[i+2]) & (tenkan[i+1] >= kijun[i+1]) & (tenkan[i+5] > tenkan[i-5]))
				& ((tenkan[i+5] > kijun[i+5]) & (tenkan[i+4] > kijun[i+4]))
				& ((tenkan[i+3] >= kijun[i+3]))):
				signal = {
				'signal': 'buy',
				'index': i,
				'symbol': symbol
				}
				break

			if (((tenkan[i-2] >= kijun[i-2]) & (tenkan[i-1] >= kijun[i-1])) 
				& ((tenkan[i-5] > kijun[i-5]) & (tenkan[i-4] > kijun[i-4])) 
				& ((tenkan[i-3] >= kijun[i-3]))
				& ((tenkan[i+2] <= kijun[i+2]) & (tenkan[i+1] <= kijun[i+1]) & (tenkan[i+5] < tenkan[i-5]))
				& ((tenkan[i+5] < kijun[i+5]) & (tenkan[i+4] < kijun[i+4]))
				& ((tenkan[i+3] <= kijun[i+3]))):
				signal = {
				'signal': 'sell',
				'index': i,
				'symbol': symbol
				}
				break
		i -= 1
		if (i < 0):
			break

	return signal