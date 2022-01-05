def find_flat(data,name_ichi,symbol):
	flat_finded = {}
	j = 0
	count = 0
	not_equal = 1
	i = 0
	#print("Flat Check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	while j<len(data)-1:
		#print(count)
		if data[j] == data[j+1]:
			count += 1
			not_equal = 0
		else:
			not_equal = 1

		if ((count>=3) & (not_equal==1)):
			#print(count)
			flat = 1
			#print("number of frist flat: ",j)
			#print("kiju= ",data[j])
			flat_finded[i] = {
			i: i,
			'symbol': symbol,
			"ichi_name": name_ichi,
			'number': j,
			'value': data[j],
			'power':count 
			}
			i += 1
			count = 0

		j += 1
	return flat_finded