def chiko_signal(chikospan,tenkan,kijun,symbol):
	i = 0
	count = 0
	signal_data = {}
	flag_find = 0
	while i<len(tenkan):
		if ((i+1) >= len(tenkan)):
			break
		if (i-1 < 0):
			i += 1
			continue
		if ((chikospan[i-1] > tenkan[i-1])
			& (chikospan[i-1] > kijun[i-1])
			& (chikospan[i+1] < tenkan[i+1])
			& (chikospan[i+1] < kijun[i+1])):
			signal_data[count] = {
			'signal': 'sell',
			'number': i+1,
			'symbol': symbol
			}
			flag_find = 1
			count += 1
		else:
			flag_find = 0
			#print("tenkan = ",tenkan[i])
			#print("kijun = ",kijun[i])

		if ((chikospan[i-1] < tenkan[i-1])
			& (chikospan[i-1] < kijun[i-1])
			& (chikospan[i+1] > tenkan[i+1])
			& (chikospan[i+1] > kijun[i+1])):
			signal_data[count] = {
			'signal': 'buy',
			'number': i+1,
			'symbol': symbol
			}
			flag_find = 1
			count += 1
		else:
			flag_find = 0


		if (flag_find == 0):
			j = 1
			while j<3:
				if ((i+j+1) >= len(tenkan)):
					break
				if (i-j < 0):
					break
				if ((chikospan[i-j] > tenkan[i-j])
					& (chikospan[i-j] > kijun[i-j])
					& (chikospan[i+j] < tenkan[i+j])
					& (chikospan[i+j] < kijun[i+j])):
					signal_data[count] = {
					'signal': 'sell',
					'number': i+j,
					'symbol': symbol
					}
					count += 1
					flag_find = 1
					break
			#print("tenkan = ",tenkan[i])
			#print("kijun = ",kijun[i])

				if ((chikospan[i-j] < tenkan[i-j])
					& (chikospan[i-j] < kijun[i-j])
					& (chikospan[i+j] > tenkan[i+j])
					& (chikospan[i+j] > kijun[i+j])):
					signal_data[count] = {
					'signal': 'buy',
					'number': i+j,
					'symbol': symbol
					}
					count += 1
					flag_find = 1
					break
				j += 1
		i += 1
	if (signal_data == {}):
		return 0
	else:
		return signal_data