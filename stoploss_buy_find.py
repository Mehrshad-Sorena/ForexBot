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

def stoploss_buy_find(data,diff,time_frame,sym_name):
	pre_max_find = {}
	max_find = {}

	i = 0

	while (len(data['high']) > 1):

		index, pre_max_find[i] = max(enumerate(data['high']), key=operator.itemgetter(1))

		data['high'][index] = -10

		if (pre_max_find[i] == -10): break

		#print('max = ',pre_max_find[i],index)

		if (((index - 7) > 0) & ((index + 7) < len(data['high']))):
			if (((data['high'][index - 1] != -10)
				& (data['high'][index - 2] != -10)
				& (data['high'][index - 3] != -10)
				& (data['high'][index - 4] != -10)
				& (data['high'][index - 5] != -10)
				& (data['high'][index - 6] != -10)
				& (data['high'][index - 7] != -10)
				& (data['high'][index + 1] != -10)
				& (data['high'][index + 2] != -10)
				& (data['high'][index + 3] != -10)
				& (data['high'][index + 4] != -10)
				& (data['high'][index + 5] != -10)
				& (data['high'][index + 6] != -10)
				& (data['high'][index + 7] != -10))):

				if ((pre_max_find[i] >= data['high'][index - 1])
					& (pre_max_find[i] >= data['high'][index - 2])
					& (pre_max_find[i] >= data['high'][index - 3])
					& (pre_max_find[i] > data['high'][index - 4])
					& (pre_max_find[i] > data['high'][index - 5])
					& (pre_max_find[i] > data['high'][index - 6])
					& (pre_max_find[i] > data['high'][index - 7])
					& (pre_max_find[i] >= data['high'][index + 1])
					& (pre_max_find[i] >= data['high'][index + 2])
					& (pre_max_find[i] >= data['high'][index + 3])
					& (pre_max_find[i] > data['high'][index + 4])
					& (pre_max_find[i] > data['high'][index + 5])
					& (pre_max_find[i] > data['high'][index + 6])
					& (pre_max_find[i] > data['high'][index + 7])):
				
					max_find[i] = pre_max_find[i]

				else:
					max_find[i] = 0
					continue

			else:
				max_find[i] = 0
				continue

		else:
			max_find[i] = 0
			continue

		

		j = 0

		while (j < (len(data['high'] - 1))):

			#print('j = ',j)

			
			#print('jj = ',j)

			#print('len = ',(len(data['high'] - 2)))
			if (((abs(data['high'][j] - max_find[i])/data['high'][j]) * 100) <= diff):
				
				#del(data['high'][j])
				data['high'][j] = -10
				#print(j)


				#data['high'].drop([j])

				#data['high'].reset_index()

				#data['high'] = data['high'].reset_index(drop=True)

				#print('j = ',j)
				#print(data['high'])

				

				
				
				
			#print('len = ',len(data['high']))
			

			j += 1
			if (j >= (len(data['high'] - 1))): break



		i += 1

	#print(max_find.items())
	out_max_find = {}
	i = 0
	for x, y in max_find.items():
		if y != 0:
			out_max_find[i] = y
			i += 1

	try:

		if os.path.exists("Res_Buy_Protection_Sell/"+time_frame+'/'+sym_name+'.csv'):
			os.remove("Res_Buy_Protection_Sell/"+time_frame+'/'+sym_name+'.csv')

		i = 0

		fields=[]
		add_row = {}

		for out in out_max_find.values():

			add_row['Res_Buy_Protection_Sell' + str(i)] = out

			fields.append('Res_Buy_Protection_Sell' + str(i))

			i += 1


		with open("Res_Buy_Protection_Sell/"+time_frame+'/'+sym_name+'.csv', 'w', newline='') as myfile:
			writer=csv.DictWriter(myfile,fieldnames=fields)
			writer.writeheader()
			writer.writerow(add_row)
	except:
		print('some thing wrong')
				


	#print(x)



#data,my_money,symbols = log_get_data(mt5.TIMEFRAME_H1,100)

#stoploss_buy_find(data['GBPUSD_i'],0.1,'1H','GBPUSD_i')
