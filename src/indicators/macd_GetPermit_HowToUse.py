from Mt5_LoginGetData import LoginGetData as getdata
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd



loging = getdata()
# loging.account_name = 'mehrshadpc'
# loging.initilizer()
# loging.login()


parameters = Parameters()
config = Config()

# ind_params = indicator_parameters()
# ind_config = indicator_config()



parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')

parameters.elements['symbol'] = 'XAUUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

#print(parameters.elements['dataset_1H']['ETHUSD_i'])

macd = MACD(parameters = parameters, config = config)
macd_calc = macd.GetPermit(
						dataset_5M = parameters.elements['dataset_5M'],
						dataset_1H = parameters.elements['dataset_1H'], 
						symbol = 'XAUUSD_i',
						signaltype = 'sell',
						signalpriority = 'secondry',
						flag_savepic = False
						)