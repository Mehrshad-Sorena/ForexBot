from multiprocessing.spawn import import_main_path
from ExtremePoints import ExtremePoints
from Parameters import Parameters
#from .MetaTrader.MetaTrader5.log_get_data import *
import MetaTrader5 as mt5
import sys

data_5M,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)
data_1H,money,_  = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,500)

parameters = Parameters()
parameters.dataset_5M = pd.DataFrame(data_5M['XAUUSD_i'])
parameters.dataset_1H = pd.DataFrame(data_1H['XAUUSD_i'])
parameters.number_max_5M = 50
parameters.number_min_5M = 50
parameters.number_max_1H = 10
parameters.number_min_1H = 10

parameters.weight_extreme_5M = 200
parameters.weight_extreme_1H = 200

extreme_points = ExtremePoints(parameters = parameters)
extreme_points.get(timeframe = '5M')
extreme_points.ploter()




