from multiprocessing.spawn import import_main_path
from pr_ExtremePoints import ExtremePoints
from pr_IchimokouFlatLines import IchimokouFlatLines
from pr_TrendLines import TrendLines
from pr_Parameters import Parameters
from pr_Config import Config
import numpy as np
from timer import stTime
from pr_Runner import Runner
from log_get_data import *
import MetaTrader5 as mt5
import sys

data_5M,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,800)
data_1H,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,600)

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
print(pr_Runner.start(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=700))
#pr_Runner.ploter(dataset_5M = pd.DataFrame(data_5M['XAUUSD_i']), dataset_1H = pd.DataFrame(data_1H['XAUUSD_i']),loc_end_5M=700)




