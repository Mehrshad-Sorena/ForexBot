import math
import pandas as pd

def cross_macd(macd,macds,macdh,symbol,diff_minus,diff_plus):
	signal_buy = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
		'diff_plus': 0,
		'diff_minus': 0
	}

	signal_sell = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
		'diff_plus': 0,
		'diff_minus': 0
	}

	signal = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol,
		'diff_plus': 0,
		'diff_minus': 0
	}

	i = len(macd)-1

	mean_macd = abs(pd.DataFrame.mean(macds))
	#diff_plus = diff_plus + mean_macd
	#diff_minus = diff_minus - mean_macd
	while ((macd[i] != True) & (macds[i] != True) & (macdh[i] != True)):

		if (((i+3) <= len(macd)-1) & ((i-3) >= 0)):

			if True:#(((macd[i+2] > macds[i+2]) & (macd[i-2] < macds[i-2])) | ((macd[i+2] < macds[i+2]) & (macd[i-2] > macds[i-2]))):

				if (((macd[i+3] < macds[i+3]) & (macd[i-3] > macds[i-3]))
					& ((macd[i+3] < macds[i+3]) & (macd[i-3] > macds[i-3]))
					& ((macd[i+3] < macds[i+3]) & (macd[i-3] > macds[i-3]))
					& ((macd[i+2] <= macds[i+2]) & (macd[i-2] >= macds[i-2]))
					& ((macd[i+1] <= macds[i+1]) & (macd[i-1] >= macds[i-1]))):
					
					if ((macd[i] >= diff_minus) & (macds[i] >= diff_minus)):#(((macd[i] > (mean_macd)) & (macds[i] > (mean_macd)))
						if (macd[i]) >= 0:
							diff_minus_out = 0
							diff_plus_out = min(macd[i] , macds[i])
						if (macd[i]) <= 0:
							diff_minus_out = min(macd[i] , macds[i])
							diff_plus_out = 0
						signal = {
						"index": i,
						'signal': "sell",
						'symbol': symbol,
						'diff_plus': diff_plus_out,
						'diff_minus': diff_minus_out
						}
						break
					if ((macd[i] < diff_minus) | (macds[i] < diff_minus)):
						if (macd[i]) >= 0:
							diff_minus_out = 0
							diff_plus_out = min(macd[i] , macds[i])
						if (macd[i]) <= 0:
							diff_minus_out = min(macd[i] , macds[i])
							diff_plus_out = 0
						signal = {
						"index": i,
						'signal': "faild_sell",
						'symbol': symbol,
						'diff_plus': diff_plus_out,
						'diff_minus': diff_minus_out
						}
						break
				if (((macd[i+3] > macds[i+3]) & (macd[i-3] < macds[i-3]))
					& ((macd[i+3] > macds[i+3]) & (macd[i-3] < macds[i-3]))
					& ((macd[i+3] > macds[i+3]) & (macd[i-3] < macds[i-3]))
					& ((macd[i+2] >= macds[i+2]) & (macd[i-2] <= macds[i-2]))
					& ((macd[i+1] >= macds[i+1]) & (macd[i-1] <= macds[i-1]))):
					
					if ((macd[i] <= diff_plus) & (macds[i] <= diff_plus)):#(((macd[i] < ((-1) * mean_macd)) & (macds[i] < ((-1) * mean_macd)))
						#| (((macd[i] > (mean_macd)) & (macds[i] > (mean_macd))))):
						if (macd[i]) >= 0:
							diff_minus_out = 0
							diff_plus_out = min(macd[i] , macds[i])
						if (macd[i]) <= 0:
							diff_minus_out = min(macd[i] , macds[i])
							diff_plus_out = 0
						signal = {
						"index": i,
						'signal': "buy",
						'symbol': symbol,
						'diff_plus': diff_plus_out,
						'diff_minus': diff_minus_out
						}
						break
					if ((macd[i] > diff_plus) | (macds[i] > diff_plus)):
						if (macd[i]) >= 0:
							diff_minus_out = 0
							diff_plus_out = min(macd[i] , macds[i])
						if (macd[i]) <= 0:
							diff_minus_out = min(macd[i] , macds[i])
							diff_plus_out = 0
						signal = {
						"index": i,
						'signal': "faild_buy",
						'symbol': symbol,
						'diff_plus': diff_plus_out,
						'diff_minus': diff_minus_out
						}
						break
		if ((i-3) < 0):
			break

		i -= 1

	return signal
