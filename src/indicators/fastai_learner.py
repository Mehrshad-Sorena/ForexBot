from fastai.tabular.all import *

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

import pandas_ta as ind

procs = [FillMissing, Normalize, Categorify]

loging = getdata()


parameters = Parameters()
config = Config()

ind_params = indicator_parameters()
ind_config = indicator_config()



data_5M, data_1H = loging.readall(symbol = 'ETHUSD_i', number_5M = 99800, number_1H = 8323)

print('start')
macd_read_5M = ind.macd(data_5M['ETHUSD_i']['close'],fast = 12,slow = 26,signal = 9)
macd_read_1H = ind.macd(data_1H['ETHUSD_i']['close'],fast = 12,slow = 26,signal = 9)

signal_out = data_5M['ETHUSD_i'].copy(deep = True)
signal_out = signal_out.assign(
								macd = macd_read_5M['MACD_12_26_9'],
								macds = macd_read_5M['MACDs_12_26_9'],
								macdh = macd_read_5M['MACDh_12_26_9']
								)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(signal_out)


cat_vars = [ 
			#'flag', 'diff_extereme'
			]

cont_vars = [
			'open', 'close', 'low', 'high', 'HL/2', 'volume', 'HLC/3', 'HLCC/4', 'OHLC/4'
   			]

y_names = [
			'macd', 'macds', 'macdh'
			]

valid_idx = signal_out.index

bs = len(signal_out.index)

#dep_var = 'money'

signal_out_tabular = TabularPandas(
									signal_out, 
									procs, 
									cat_vars, 
									cont_vars, 
									#dep_var, 
									y_block=RegressionBlock(),
                   					inplace=True, 
                   					reduce_memory=True
                   					)

dls = TabularDataLoaders.from_df(
								signal_out,
								procs = procs, 
								cat_names = cat_vars, 
								cont_names = cont_vars, 
                                y_names = y_names, 
                                valid_idx = list(range(500,1000)), 
                                bs = 64
                                )

#dls.show_batch()
# learn = tabular_learner(dls)
# learn.lr_find()
# learn.export('myModel')

learn = load_learner('myModel')

loging.account_name = 'mehrshadpc'
loging.initilizer()
loging.login()

data = loging.getone(timeframe = '5M', number = 100, symbol = 'ETHUSD_i')

macd_read_5M = ind.macd(data['ETHUSD_i']['close'],fast = 12,slow = 26,signal = 9)

data = data['ETHUSD_i'].copy(deep = True)
data = data.assign(
								macd = macd_read_5M['MACD_12_26_9'],
								macds = macd_read_5M['MACDs_12_26_9'],
								macdh = macd_read_5M['MACDh_12_26_9']
								)

dl = learn.dls.test_dl(data)
raw_test_preds = learn.get_preds(dl=dl)
print(raw_test_preds)

learn.validate(dl=dl)

#learn.summary()



# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(score_out)