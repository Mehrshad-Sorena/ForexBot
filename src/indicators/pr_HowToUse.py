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

#for i in range(100,2000,100):
#pr_Runner.ploter(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=200)

# df = pd.DataFrame({
# 			    'year' : [2018, 2019, 2020, 2021,2018, 2019, 2020, 2021,2018, 2019, 2020, 2021],
# 			    'id'   : ['ABC','ABC','ABC','ABC','DEF','DEF','DEF','DEF','GHI','GHI','GHI','GHI'],
# 			    'A': np.random.choice(range(100),12),
# 			    'B': np.random.choice(range(100),12),
# 			    'C': np.random.choice(range(100),12),
# 			    'D': np.random.choice(range(100),12),
# 			    'E': np.random.choice(range(100),12),
# 			})

# df["Share"] = ( df.B + df.C ) / ( df.B + df.C + df.D )
# df["X"] = ( df.A + df.Share * df.E ).where( df.year >= 2020 )
# #print('first = ',df.year)
# def my_func( year,a,b,c,d,e ):
#     #This function can be longer and do more things
#     print(type(year))
#     if year < 2020:
#     	return np.nan
#     else:
#     	return a + ( ( (b + c) / (b + c + d) ) * e )
    #return np.nan if year < 2020 else a + ( ( (b + c) / (b + c + d) ) * e )
#my_func( x.name, x.A, x.B, x.C, x.D, x.E )

#df['X'] = df.apply( lambda x: my_func( x.year, x.A, x.B, x.C, x.D, x.E ), axis = 1 )

#print('sec = ',df)

@stTime
def run1():
	#itter.cycle(range(100,17999))
	pr = pd.DataFrame(np.nan, index = range(2000,99700,100), columns = ['high_upper', 'high_mid', 'high_lower', 'power_high_upper', 
															'power_high_mid', 'power_high_lower', 'low_upper', 'lowe_mid', 
															'low_lower','power_low_upper', 'power_low_mid', 'power_low_lower'])
	for i in range(2000,99700,100):
		pr_ = pr_Runner.start(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=i)

		pr['high_upper'][i] = pr_[0]
		pr['high_mid'][i] = pr_[1]
		pr['high_lower'][i] = pr_[2]

		pr['power_high_upper'][i] = pr_[3]
		pr['power_high_mid'][i] = pr_[4]
		pr['power_high_lower'][i] = pr_[5]

		pr['low_upper'][i] = pr_[6]
		pr['lowe_mid'][i] = pr_[7]
		pr['low_lower'][i] = pr_[8]

		pr['power_low_upper'][i] = pr_[9]
		pr['power_low_mid'][i] = pr_[10]
		pr['power_low_lower'][i] = pr_[11]



print('start')
run1()
print('finish')

# pr = pr_Runner.start(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=2000)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(pr)

# print(pr['high'])

@stTime
def run2(indexes):
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
print('start')
# indexes = pd.DataFrame(
# 						{
# 						'high_upper': [0],
# 						'high_mid': [0],
# 						'high_lower': [0],
# 						'power_high_upper': 0,
# 						'power_high_mid': 0,
# 						'power_high_lower': 0,
# 						'low_upper': [0],
# 						'lowe_mid': [0],
# 						'low_lower': [0],
# 						'power_low_upper': 0,
# 						'power_low_mid': 0,
# 						'power_low_lower': 0,
# 						'index': range(2000,3000,100),
# 						},
# 						index = range(2000,3000,100)
# 						)
indexes = pd.DataFrame(range(2000,99700,100), index = range(2000,99700,100) , columns=['index'])
indexes = run2(indexes)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(indexes)
print('finish')

#import swifter

@stTime
def run3(indexes):
	if __name__ == '__main__':
 		pr = indexes.swifter.progress_bar(False).apply(
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


# indexes = pd.DataFrame(range(2000,99700,100), index = range(2000,99700,100) , columns=['index'])
# indexes = run3(indexes)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(indexes)






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
