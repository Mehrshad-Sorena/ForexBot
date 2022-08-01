from Mt5_LoginGetData import LoginGetData as getdata
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd



loging = getdata()
loging.account_name = 'mehrshadpc'
loging.initilizer()
loging.login()


parameters = Parameters()
config = Config()

# ind_params = indicator_parameters()
# ind_config = indicator_config()



parameters.elements['dataset_5M'] = loging.getone(timeframe = '5M', number = 99800, symbol = 'ETHUSD_i')
parameters.elements['dataset_1H'] = loging.getone(timeframe = '1H', number = 8323, symbol = 'ETHUSD_i')

parameters.elements['symbol'] = 'ETHUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

macd = MACD(parameters = parameters, config = config)
macd_calc = macd.GetPermit(
						dataset_5M = parameters.elements['dataset_5M'], 
						dataset_1H = parameters.elements['dataset_1H'], 
						symbol = 'ETHUSD_i',
						signaltype = 'buy', 
						signalpriority = 'secondry',
						flag_savepic = True
						)