from Mt5_LoginGetData import LoginGetData as getdata
from indicator_Divergence import Divergence
from indicator_Tester import Tester
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config

from pr_Parameters import Parameters as pr_Parameters
from pr_Config import Config as pr_Config

loging = getdata()


parameters = Parameters()
config = Config()

ind_params = indicator_parameters()
ind_config = indicator_config()



parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 4000, number_1H = 8323)
parameters.elements['MACD_symbol'] = 'XAUUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

macd = MACD(parameters = parameters, config = config)
macd_calc = macd.calculator_macd()


macd = Divergence(parameters = ind_params, config = ind_config)
signal, signaltype, indicator = macd.divergence(
												sigtype = 'buy',
												sigpriority = 'secondry',
												indicator = macd_calc,
												column_div = 'macds',
												ind_name = 'macd',
												dataset_5M = parameters.elements['dataset_5M'],
												dataset_1H = parameters.elements['dataset_1H'],
												symbol = 'XAUUSD_i',
												flaglearn = True,
												flagtest = True
												)

ind_params.elements['dataset_5M'] = parameters.elements['dataset_5M'] 
ind_params.elements['dataset_1H'] = parameters.elements['dataset_1H']

macd_tester = Tester(parameters = ind_params, config = ind_config)

signal_out, score_out = macd_tester.RunGL(
											signal = signal, 
											sigtype = signaltype, 
											flaglearn = True, 
											flagtest = True,
											pr_parameters = pr_Parameters(),
											pr_config = pr_Config(),
											indicator = indicator,
											flag_savepic = False
											)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(signal_out)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(score_out)