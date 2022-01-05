from find_flat import *
def three_flat_find(SPANA,SPANB,kiju,tenku,symbol):
	three_flat_finded = {}
	find_spanA = find_flat(SPANA,"SPANA",symbol)
	find_spanB = find_flat(SPANB,"SPANB",symbol)
	find_kiju = find_flat(kiju,"kiju",symbol)
	find_tenku = find_flat(tenku,"tenku",symbol)

	i = 0
	count = 0
	while i<len(find_spanA):
		j = 0
		while j<len(find_tenku):
			k = 0
			while k<len(find_kiju):
				if ((find_spanA[i]['value']==find_kiju[k]['value'])&(find_spanA[i]['value']==find_tenku[j]['value'])):
					three_flat_finded[count] = find_spanA[i]['value']
					count += 1
				k += 1
			j += 1
		i += 1 

	i = 0
	while i<len(find_spanB):
		j = 0
		while j<len(find_tenku):
			k = 0
			while k<len(find_kiju):
				if ((find_spanB[i]['value']==find_kiju[k]['value'])&(find_spanB[i]['value']==find_tenku[j]['value'])):
					three_flat_finded[count] = find_spanB[i]['value']
					count += 1
				k += 1
			j += 1
		i += 1
	return three_flat_finded