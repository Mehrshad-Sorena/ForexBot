import math

def divergence(data_ma,macd,window,symbol):
	
	last_window = len(macd)-1;
	first_window = last_window - window
	signal_buy = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}


	Diff_min_max = 30 #1~100

	min_macd = {}

	ma = data_ma[:]

	ma_not_nan = ma.dropna() # delete nan values
	#print(ma)
	sum_ma = sum(ma_not_nan)
	#print("sum = ",sum_ma)
	mean_ma = sum_ma/(len(ma_not_nan))
	#print("mean = ",mean_ma)
	ma_normalize = ma[:] - mean_ma
	#print(ma_normalize)

	#del macd[998]
	data_for_Divergence_macd = macd[:]
	data_for_Divergence_ma = ma_normalize[:]


	#min macd find
	minmacd1 = 0
	minma1 = 0

	flag = 0
	i = 0
	while ((minmacd1 >= 0) | (minma1 >= 0)):
		minmacd1 = min(data_for_Divergence_macd[first_window-i:last_window-i])

		minma1 = min(data_for_Divergence_ma[first_window-i:last_window-i])

		if ((math.isnan(minmacd1) != True) & (math.isnan(minma1) != True)):

			index_minmacd1 = data_for_Divergence_macd.tolist().index(minmacd1)

			index_minma1 = data_for_Divergence_ma.tolist().index(minma1)
		else:
			flag = 1
			break;

		i += window


	while flag == 0:
		del data_for_Divergence_macd[index_minmacd1]
		del data_for_Divergence_ma[index_minma1]

		minmacd2 = min(data_for_Divergence_macd[first_window-i:last_window-i])
		minma2 = min(data_for_Divergence_ma[first_window-i:last_window-i])

		data_for_Divergence_macd = macd[:]
		data_for_Divergence_ma = ma_normalize[:]

		if ((math.isnan(minmacd2) != True) & (math.isnan(minma2) != True)):
			index_minmacd2 = data_for_Divergence_macd.tolist().index(minmacd2)
			index_minma2 = data_for_Divergence_ma.tolist().index(minma2)
		else:
			print('nan value')
			break
	
		E1 = 0
		E2 = 0
		E3 = 0
		E4 = 'nan'
		E5 = 'nan'

		if ((index_minmacd2 - i < 0) | (index_minma2 - i < 0)):
			print("high index")
			break

		if ((index_minmacd1>index_minmacd2) & (minmacd1 < 0) & (minmacd2 < 0) & (math.isnan(data_for_Divergence_macd[index_minmacd2-i]) != True)):
			E2 = max(data_for_Divergence_macd[index_minmacd2-i:index_minmacd1-i])
			E1 = minmacd1
			E3 = minmacd2

			if ((index_minma1>index_minma2) & (minma1 < 0) & (minma2 < 0) & (math.isnan(data_for_Divergence_ma[index_minma2-i]) != True)):
				E4 = minma1
				E5 = minma2

				index_minma4 = index_minma1
				index_minma5 = index_minma2

			if ((index_minma1<index_minma2) & (minma1 < 0) & (minma2 < 0) & (math.isnan(data_for_Divergence_ma[index_minma2-i]) != True)):
				E4 = minma2
				E5 = minma1

				index_minma4 = index_minma2
				index_minma5 = index_minma1


			if ((E2>E1) & (E2>E3) & (Diff_min_max<(abs(abs(E2/E1)-1)*100))):
				flag = 1
				if ((E4 != 'nan') & (E5 != 'nan')):
					if (((E1<=E3) & (E4>E5)) | ((E1>E3) & (E4<E5)) & (index_minmacd1 == index_minma4) & (index_minmacd2 == index_minma5)):
						signal_buy = {
						"index": index_minma4,
						'signal': "buy",
						'symbol': symbol
						}
		if ((index_minmacd1<index_minmacd2) & (minmacd1 < 0) & (minmacd2 < 0) & (math.isnan(data_for_Divergence_macd[index_minmacd2-i]) != True)):
			E2 = max(data_for_Divergence_macd[index_minmacd1-i:index_minmacd2-i])
			E1 = minmacd2
			E3 = minmacd1

			if ((index_minma1>index_minma2) & (minma1 < 0) & (minma2 < 0) & (math.isnan(data_for_Divergence_ma[index_minma2-i]) != True)):
				E4 = minma1
				E5 = minma2

				index_minma4 = index_minma1
				index_minma5 = index_minma2

			if ((index_minma1<index_minma2) & (minma1 < 0) & (minma2 < 0) & (math.isnan(data_for_Divergence_ma[index_minma2-i]) != True)):
				E4 = minma2
				E5 = minma1

				index_minma4 = index_minma2
				index_minma5 = index_minma1

			if ((E2>E1) & (E2>E3) & (Diff_min_max<(abs(abs(E2/E1)-1)*100))):
				flag = 1
				if ((E4 != 'nan') & (E5 != 'nan')):
					if (((E1<=E3) & (E4>E5)) | ((E1>E3) & (E4<E5)) & (index_minmacd2 == index_minma4) & (index_minmacd1 == index_minma5)):
						signal_buy = {
						"index": index_minma4,
						'signal': "buy",
						'symbol': symbol
						}
		i += window

	#max macd
	#del macd[998]
	signal_sell = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}

	ma = data_ma[:]

	ma_not_nan = ma.dropna() # delete nan values
	#print(ma)
	sum_ma = sum(ma_not_nan)
	#print("sum = ",sum_ma)
	mean_ma = sum_ma/(len(ma_not_nan))
	#print("mean = ",mean_ma)
	ma_normalize = ma[:] - mean_ma
	#print(ma_normalize)

	#del macd[998]
	data_for_Divergence_macd = macd[:]
	data_for_Divergence_ma = ma_normalize[:]


	maxmacd1 = 0
	maxma1 = 0
	i = 0
	flag = 0

	while ((maxmacd1 <= 0) | (maxma1 <= 0)):
		maxmacd1 = max(data_for_Divergence_macd[first_window-i:last_window-i])

		maxma1 = max(data_for_Divergence_ma[first_window-i:last_window-i])

		if ((math.isnan(maxmacd1) != True) & (math.isnan(maxma1) != True)):

			index_maxmacd1 = data_for_Divergence_macd.tolist().index(maxmacd1)

			index_maxma1 = data_for_Divergence_ma.tolist().index(maxma1)
		else:
			flag = 1
			break

		i += window

	
	while flag == 0:
		del data_for_Divergence_macd[index_maxmacd1]
		del data_for_Divergence_ma[index_maxma1]

		maxmacd2 = max(data_for_Divergence_macd[first_window-i:last_window-i])
		maxma2 = max(data_for_Divergence_ma[first_window-i:last_window-i])

		data_for_Divergence_macd = macd[:]
		data_for_Divergence_ma = ma_normalize[:]

		if ((math.isnan(maxmacd2) != True) & (math.isnan(maxma2) != True)):
			index_maxmacd2 = data_for_Divergence_macd.tolist().index(maxmacd2)
			index_maxma2 = data_for_Divergence_ma.tolist().index(maxma2)
		else:
			break

		E1 = 0
		E2 = 0
		E3 = 0
		E4 = 'nan'
		E5 = 'nan'

		if ((index_maxmacd2 - i < 0) | (index_maxma2 - i < 0)):
			break
		if ((index_maxmacd1>index_maxmacd2) & (maxmacd1 > 0) & (maxmacd2 > 0) & (math.isnan(data_for_Divergence_macd[index_maxmacd2-i]) != True)):
			E2 = min(data_for_Divergence_macd[index_maxmacd2-i:index_maxmacd1-i])
			E1 = maxmacd1
			E3 = maxmacd2

			if ((index_maxma1>index_maxma2) & (maxma1 > 0) & (maxma2 > 0) & (math.isnan(data_for_Divergence_ma[index_maxma2-i]) != True)):
				E4 = maxma1
				E5 = maxma2

				index_maxma4 = index_maxma1
				index_maxma5 = index_maxma2

			if ((index_maxma1<index_maxma2) & (maxma1 > 0) & (maxma2 > 0) & (math.isnan(data_for_Divergence_ma[index_maxma2-i]) != True)):
				E4 = maxma2
				E5 = maxma1

				index_maxma4 = index_maxma2
				index_maxma5 = index_maxma1


			if ((E2<E1) & (E2<E3) & (Diff_min_max<(abs(abs(E1/E2)-1)*100))):
				flag = 1

				if ((E4 != 'nan') & (E5 != 'nan')):
					if (((E1>=E3) & (E4<E5)) | ((E1<E3) & (E4>E5)) & (index_maxmacd1 == index_maxma4) & (index_maxmacd2 == index_maxma5)):
						signal_sell = {
						"index": index_maxma4,
						'signal': "sell",
						'symbol': symbol
						}
		if ((index_maxmacd1<index_maxmacd2) & (maxmacd1 > 0) & (maxmacd2 > 0) & (math.isnan(data_for_Divergence_macd[index_maxmacd2-i]) != True)):
			E2 = min(data_for_Divergence_macd[index_maxmacd1-i:index_maxmacd2-i])
			E1 = maxmacd2
			E3 = maxmacd1

			if ((index_maxma1>index_maxma2) & (maxma1 > 0) & (maxma2 > 0) & (math.isnan(data_for_Divergence_ma[index_maxma2-i]) != True)):
				E4 = maxma1
				E5 = maxma2

				index_maxma4 = index_maxma1
				index_maxma5 = index_maxma2

			if ((index_maxma1<index_maxma2) & (maxma1 > 0) & (maxma2 > 0) & (math.isnan(data_for_Divergence_ma[index_maxma2-i]) != True)):
				E4 = maxma2
				E5 = maxma1

				index_maxma4 = index_maxma2
				index_maxma5 = index_maxma1

			if ((E2<E1) & (E2<E3) & (Diff_min_max<(abs(abs(E1/E2)-1)*100))):
				flag = 1

				if ((E4 != 'nan') & (E5 != 'nan')):
					if (((E1>=E3) & (E4<E5)) | ((E1<E3) & (E4>E5)) & (index_maxmacd1 == index_maxma4) & (index_maxmacd2 == index_maxma5)):
						signal_sell = {
						"index": index_maxma4,
						'signal': "sell",
						'symbol': symbol
					}
		i += window

	signal = {
		"index": 0,
		'signal': "nan",
		'symbol': symbol
	}

	if (signal_buy['index'] > signal_sell['index']):
		signal = signal_buy
	else:
		signal = signal_sell

	return signal