from Mt5_LoginGetData import LoginGetData as getdata
from .Parameters import Parameters
from .Config import Config
from .MACD import MACD
import pandas as pd
import os


loging = getdata()


parameters = Parameters()
config = Config()

parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'ETHUSD_i', number_5M = 'all', number_1H = 'all')
parameters.elements['symbol'] = 'ETHUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

macd = MACD(parameters = parameters, config = config)

print('**************** Start ********************')
macd_signal, scores = macd.Simulator(
							dataset_5M = parameters.elements['dataset_5M'], 
							dataset_1H = parameters.elements['dataset_1H'], 
							symbol = 'ETHUSD_i',
							signaltype = 'sell',
							signalpriority = 'secondry',
							flag_savepic = False
							)

print('************** Finish *********************')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(macd_signal)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(scores)
