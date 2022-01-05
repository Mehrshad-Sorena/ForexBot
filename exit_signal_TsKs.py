def exit_signal_TsKs(tenkan,kijun,symbol):
	i = 1
	count = 0
	signal_data = {}
	while i<len(tenkan):
		if ((i+2) == len(tenkan)):
			break
		if ((tenkan[i-1] > tenkan[i]) & (tenkan[i] > tenkan[i+1]) & (tenkan[i+1] > tenkan[i+2]) 
			& (kijun[i-1] == kijun[i]) & (kijun[i] == kijun[i+1]) & (kijun[i+1] == kijun[i+2])
			& (tenkan[i] > kijun[i])):
			signal_data[count] = {
			'signal': 'exit buy',
			'number': i+1,
			'symbol': symbol
			}
			count += 1
			#print("tenkan = ",tenkan[i])
			#print("kijun = ",kijun[i])

		if ((tenkan[i-1] < tenkan[i]) & (tenkan[i] < tenkan[i+1]) & (tenkan[i+1] < tenkan[i+2])
			& (kijun[i-1] == kijun[i]) & (kijun[i] == kijun[i+1]) & (kijun[i+1] == kijun[i+2])
			& (tenkan[i] < kijun[i])):
			signal_data[count] = {
			'signal': 'exit sell',
			'number': i+1,
			'symbol': symbol
			}
			count += 1
		i += 1
	if (signal_data == {}):
		return 0
	else:
		return signal_data