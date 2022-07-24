from multiprocessing.spawn import import_main_path
from ExtremePoints import ExtremePoints
from pr_IchimokouFlatLines import IchimokouFlatLines
from pr_TrendLines import TrendLines
from pr_Parameters import Parameters
from pr_Config import Config
import numpy as np
from timer import stTime
from pr_Runner import Runner
from Mt5_LoginGetData import LoginGetData as getdata
#import MetaTrader5 as mt5
import sys
import pandas as pd

	

# import itertools as itter

loging = getdata()
loging.account_name = 'mehrshadpc'
data_5M, data_1H = loging.readall(symbol = 'XAUUSD_i', number_5M = 99800, number_1H = 8323)
#print(data_1H['XAUUSD_i'])
#data_5M = loging.getone(timeframe = '5M', number = 500, symbol = 'XAUUSD_i')
# data_1H = loging.getone(timeframe = '1H', number = 500, symbol = 'XAUUSD_i')

parameters = Parameters()
parameters.elements['ExtremePoints_num_max_5M'] = 5
parameters.elements['ExtremePoints_num_min_5M'] = 5
parameters.elements['ExtremePoints_num_max_1H'] = 100
parameters.elements['ExtremePoints_num_min_1H'] = 100

parameters.elements['ExtremePoints_weight_5M'] = 200
parameters.elements['ExtremePoints_weight_1H'] = 200

config = Config()
config.cfg['ExtremePoints_T_5M'] = True
config.cfg['ExtremePoints_T_1H'] = True
config.cfg['ExtremePoints_status'] = True

#pr_Runner = Runner(parameters = parameters, config = config)
#pr_Runner.start()
"""
extreme_points = ExtremePoints(parameters = parameters, config = config)

extreme_points.get(timeframe = '5M')
#extreme_points.ploter()


parameters.elements['TrendLines_num_max_5M'] = 5
parameters.elements['TrendLines_num_min_5M'] = 5
parameters.elements['TrendLines_num_max_1H'] = 5
parameters.elements['TrendLines_num_min_1H'] = 5

parameters.elements['TrendLines_weight_5M'] = 200
parameters.elements['TrendLines_weight_1H'] = 200

config.cfg['TrendLines_T_5M'] = True
config.cfg['TrendLines_T_1H'] = True
config.cfg['TrendLines_status'] = True

trendline = TrendLines(parameters = parameters, config = config)

trendline.runner(timeframe='1H')
#trendline.ploter(length='mid')

flatlines = IchimokouFlatLines(parameters = parameters, config = config)

#flatlines.ploter()
"""

pr_Runner = Runner(parameters = parameters, config = config)

# print(pr_Runner.start(
# 				dataset_5M = data_5M['XAUUSD_i'], 
# 				dataset_1H = data_1H['XAUUSD_i'],
# 				loc_end_5M = 10
# 				))

print('start')

indexes = pd.DataFrame(range(2000,3000,100), index = range(2000,3000,100) , columns=['index'])

print(pr_Runner.run(
				dataset_5M = data_5M['XAUUSD_i'], 
				dataset_1H = data_1H['XAUUSD_i'],
				signals = indexes
				))
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(indexes)
print('finish')



@stTime
def run4(indexes):
	if __name__ == '__main__':
		pr = indexes.apply(
						lambda x: pd.Series(
												pr_Runner.start(
																dataset_5M = data_5M['XAUUSD_i'], 
																dataset_1H = data_1H['XAUUSD_i'],
																loc_end_5M = x['index']
																), 
																index = ['high_upper', 'high_mid', 'high_lower', 'power_high_upper', 
																		'power_high_mid', 'power_high_lower', 'low_upper', 'lowe_mid', 
																		'low_lower','power_low_upper', 'power_low_mid', 'power_low_lower']
												),
						axis = 1,
						result_type = 'expand'
						)
		indexes = indexes.join(pr)
		return indexes


# indexes = pd.DataFrame(range(2000,99700,100),columns=['index'])
# print('start')
# indexes = run4(indexes)
# print('finish')

# for elm in indexes['high_upper']:
# 	print(elm)

	

	#pr_Runner.startparallel(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=i)



#pr_Runner.ploter(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=400)
