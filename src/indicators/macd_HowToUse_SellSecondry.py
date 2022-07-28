from Mt5_LoginGetData import LoginGetData as getdata
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd



loging = getdata()


parameters = Parameters()
config = Config()

# ind_params = indicator_parameters()
# ind_config = indicator_config()



parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 99800, number_1H = 8323)
parameters.elements['MACD_symbol'] = 'XAUUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

macd = MACD(parameters = parameters, config = config)
macd_calc = macd.Genetic(
						dataset_5M = parameters.elements['dataset_5M'], 
						dataset_1H = parameters.elements['dataset_1H'], 
						symbol = 'XAUUSD_i', 
						signaltype = 'sell', 
						signalpriority = 'secondry', 
						num_turn = 500
						)