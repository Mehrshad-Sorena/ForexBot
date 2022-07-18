from multiprocessing.spawn import import_main_path
from pr_ExtremePoints import ExtremePoints
from pr_TrendLines import TrendLines
from pr_Parameters import Parameters
from pr_Config import Config
import numpy as np
from timer import stTime
#from pr_Runner import Runner
from log_get_data import *
import MetaTrader5 as mt5
import sys

data_5M,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)
data_1H,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,500)

parameters = Parameters()
parameters.elements['dataset_5M'] = pd.DataFrame(data_5M['XAUUSD_i'])
parameters.elements['dataset_1H'] = pd.DataFrame(data_1H['XAUUSD_i'])
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

find = TrendLines(parameters = parameters, config = config)

find.get(
		length='long',
		timeframe='5M'
		)
#find.ploter(length='mid')




