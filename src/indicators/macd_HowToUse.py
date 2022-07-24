from Mt5_LoginGetData import LoginGetData as getdata
from macd_Divergence import Divergence
from macd_Tester import Tester
from macd_Parameters import Parameters
from macd_Config import Config
import pandas as pd

loging = getdata()


parameters = Parameters()
config = Config()

parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 99800, number_1H = 8323)
parameters.elements['Divergence_symbol'] = 'XAUUSD_i'
parameters.elements['Divergence_apply_to'] = 'close'

macd = Divergence(parameters = parameters, config = config)
signal, signaltype = macd.divergence(sigtype = 'buy', sigpriority = 'primary')

macd_tester = Tester(parameters = parameters, config = config)

signal_out, score_out = macd_tester.Run_GL(signal = signal, sigtype = signaltype, flaglearn = True, flagtest = True)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(signal_out)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(score_out)