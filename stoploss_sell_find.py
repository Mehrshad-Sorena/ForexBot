from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
#import matplotlib.pyplot as plt
import numpy as np
from log_get_data import *
import operator
import os
import csv

def stoploss_sell_find(data,diff,time_frame,sym_name):
	pre_min_find = {}
	min_find = {}

	i = 0

	while (len(data['low']) > 1):

		index, pre_min_find[i] = min(enumerate(data['low']), key=operator.itemgetter(1))

		data['low'][index] = 1000

		if (pre_min_find[i] == 1000): break

		#print('max = ',pre_max_find[i],index)

		if (((index - 7) > 0) & ((index + 7) < len(data['low']))):
			if (((data['low'][index - 1] != 1000)
				& (data['low'][index - 2] != 1000)
				& (data['low'][index - 3] != 1000)
				& (data['low'][index - 4] != 1000)
				& (data['low'][index - 5] != 1000)
				& (data['low'][index - 6] != 1000)
				& (data['low'][index - 7] != 1000)
				& (data['low'][index + 1] != 1000)
				& (data['low'][index + 2] != 1000)
				& (data['low'][index + 3] != 1000)
				& (data['low'][index + 4] != 1000)
				& (data['low'][index + 5] != 1000)
				& (data['low'][index + 6] != 1000)
				& (data['low'][index + 7] != 1000))):

				if ((pre_min_find[i] <= data['low'][index - 1])
					& (pre_min_find[i] <= data['low'][index - 2])
					& (pre_min_find[i] <= data['low'][index - 3])
					& (pre_min_find[i] < data['low'][index - 4])
					& (pre_min_find[i] < data['low'][index - 5])
					& (pre_min_find[i] < data['low'][index - 6])
					& (pre_min_find[i] < data['low'][index - 7])
					& (pre_min_find[i] <= data['low'][index + 1])
					& (pre_min_find[i] <= data['low'][index + 2])
					& (pre_min_find[i] <= data['low'][index + 3])
					& (pre_min_find[i] < data['low'][index + 4])
					& (pre_min_find[i] < data['low'][index + 5])
					& (pre_min_find[i] < data['low'][index + 6])
					& (pre_min_find[i] < data['low'][index + 7])):
				
					min_find[i] = pre_min_find[i]

				else:
					min_find[i] = 0
					continue

			else:
				min_find[i] = 0
				continue

		else:
			min_find[i] = 0
			continue

		

		j = 0

		while (j < (len(data['low'] - 1))):

			#print('j = ',j)

			
			#print('jj = ',j)

			#print('len = ',(len(data['high'] - 2)))
			if (((abs(data['low'][j] - min_find[i])/data['low'][j]) * 100) <= diff):
				
				#del(data['high'][j])
				data['low'][j] = 1000
				#print(j)


				#data['high'].drop([j])

				#data['high'].reset_index()

				#data['high'] = data['high'].reset_index(drop=True)

				#print('j = ',j)
				#print(data['high'])

				

				
				
				
			#print('len = ',len(data['high']))
			

			j += 1
			if (j >= (len(data['low'] - 1))): break



		i += 1

	#print(max_find.items())
	out_min_find = {}
	i = 0
	for x, y in min_find.items():
		if y != 0:
			out_min_find[i] = y
			i += 1

	try:

		if os.path.exists("Res_Sell_Protection_Buy/"+time_frame+'/'+sym_name+'.csv'):
			os.remove("Res_Sell_Protection_Buy/"+time_frame+'/'+sym_name+'.csv')

		i = 0

		fields=[]
		add_row = {}

		for out in out_min_find.values():

			add_row['Res_Sell_Protection_Buy' + str(i)] = out

			fields.append('Res_Sell_Protection_Buy' + str(i))

			i += 1


		with open("Res_Sell_Protection_Buy/"+time_frame+'/'+sym_name+'.csv', 'w', newline='') as myfile:
			writer=csv.DictWriter(myfile,fieldnames=fields)
			writer.writeheader()
			writer.writerow(add_row)
	except:
		print('some thing wrong')

	#with open("Res_Buy_Protection_Sell/"+time_frame+'/'+sym_name+'.csv', 'r', newline='') as myfile:
	#	for line in csv.DictReader(myfile):
	#		print('line = ',line)


	#print(x)



#data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,100)

#stoploss_sell_find(data['GBPUSD_i'],0.1,'1H','GBPUSD_i')
