from multiprocessing.spawn import import_main_path
from pr_ExtremePoints import ExtremePoints
from pr_Parameters import Parameters
from pr_Config import Config
from log_get_data import *
import MetaTrader5 as mt5
import sys

data_5M,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)
data_1H,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,500)

parameters = Parameters()
parameters.elements['dataset_5M'] = pd.DataFrame(data_5M['XAUUSD_i'])
parameters.elements['dataset_1H'] = pd.DataFrame(data_1H['XAUUSD_i'])
parameters.elements['ExtremePoints_num_max_5M'] = 50
parameters.elements['ExtremePoints_num_min_5M'] = 50
parameters.elements['ExtremePoints_num_max_1H'] = 10
parameters.elements['ExtremePoints_num_min_1H'] = 10

parameters.elements['ExtremePoints_weight_5M'] = 200
parameters.elements['ExtremePoints_weight_1H'] = 200

config = Config()
config.cfg['ExtremePoints_T_5M'] = True
config.cfg['ExtremePoints_T_1H'] = False
config.cfg['ExtremePoints_status'] = True

extreme_points = ExtremePoints(parameters = parameters, config = config)


extreme_points.get(timeframe = '5M')
extreme_points.ploter()




