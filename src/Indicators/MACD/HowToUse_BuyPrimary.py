from Mt5_LoginGetData import LoginGetData as getdata
from .Parameters import Parameters
from .Config import Config
from .MACD import MACD
import pandas as pd
from indicator_Parameters import Parameters as IndicatorParameters
from indicator_Config import Config as IndicatorConfig
from indicator_Divergence import Divergence
import os
import numpy as np
import pandas as pd



loging = getdata()


parameters = Parameters()
config = Config()
# ind_params = IndicatorParameters()
# ind_config = IndicatorConfig()

# # ind_params = indicator_parameters()
# # ind_config = indicator_config()

# signalpriority = 'primary'
# signaltype = 'sell'
# symbol = 'XAUUSD_i'

# parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')
# parameters.elements['symbol'] = 'XAUUSD_i'
# parameters.elements['MACD_apply_to'] = 'close'

# path_elites_chrom = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_ChromosomeResults.csv'
# path_elites_learn = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_LearningResults.csv'
# # path_elites_super = config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'
# # path_elites_society = config.cfg['path_society'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'

# df = pd.read_csv(path_elites_chrom).drop(columns='Unnamed: 0')
# df_learn = pd.read_csv(path_elites_learn).drop(columns='Unnamed: 0')

# df = df.assign(
# 				corr = np.nan,
# 				corr_low = np.nan,
# 				corr_high = np.nan
# 				)

# # output = pd.DataFrame(np.ones(len(df_learn.index)))
# # output['corr_low'] = np.nan
# # output['corr_high'] = np.nan
# # output['corr'] = np.nan

# for elm in df_learn.index:
# 	parameters.elements['MACD' + '_apply_to'] = df['MACD' + '_apply_to'][elm]
# 	parameters.elements['MACD' + '_fast'] = df['MACD' + '_fast'][elm]
# 	parameters.elements['MACD' + '_slow'] = df['MACD' + '_slow'][elm]
# 	parameters.elements['MACD' + '_signal'] = df['MACD' + '_signal'][elm]

# 	ind_params.elements['Divergence' + '_diff_extereme'] = df['Divergence' + '_diff_extereme'][elm]
# 	ind_params.elements['Divergence' + '_num_exteremes_min'] = df['Divergence' + '_num_exteremes_min'][elm]
# 	ind_params.elements['Divergence' + '_num_exteremes_max'] = df['Divergence' + '_num_exteremes_max'][elm]
# 	dive_column = df['MACD_column_div'][elm]


# 	macd = MACD(parameters = parameters, config = config)
# 	macd_calc = macd.calculator_macd()


# 	macd = Divergence(parameters = ind_params, config = ind_config)
# 	signal, signaltype, indicator = macd.divergence(
# 													sigtype = signaltype,
# 													sigpriority = signalpriority,
# 													indicator = macd_calc,
# 													column_div = dive_column,
# 													ind_name = 'macd',
# 													dataset_5M = parameters.elements['dataset_5M'],
# 													dataset_1H = parameters.elements['dataset_1H'],
# 													symbol = 'XAUUSD_i',
# 													flaglearn = True,
# 													flagtest = True
# 													)
# 	if signal.empty == True: continue
# 	divergence_out = pd.DataFrame(np.ones(signal.index[-1]))
# 	divergence_out['macd'] = np.nan
# 	divergence_out['low'] = np.nan
# 	divergence_out['high'] = np.nan

# 	counter = 0
# 	for idx in signal.index:
# 		divergence_out['macd'][counter] = signal.indicator_front[idx]
# 		divergence_out['macd'][counter + 1] = signal.indicator_back[idx]

# 		divergence_out['low'][counter] = signal.low_front[idx]
# 		divergence_out['low'][counter + 1] = signal.low_back[idx]

# 		divergence_out['high'][counter] = signal.high_front[idx]
# 		divergence_out['high'][counter + 1] = signal.high_back[idx]

# 		counter += 2

# 	divergence_out = divergence_out.dropna()
# 	divergence_out = divergence_out.drop(columns = [0])

# 	number_divergence = len(divergence_out.index)/1000

# 	divergence_out = divergence_out.corr()

# 	df['corr'][elm] = -((divergence_out['macd'][2] * divergence_out['macd'][1] * number_divergence) ** (1/3))
# 	if (
# 		divergence_out['macd'][2] > 0 and
# 		divergence_out['macd'][1] > 0
# 		):
# 		df['corr'][elm] = -df['corr'][elm]

# 	print('turn =====> ', elm, ' Corr = ', df['corr'][elm])

# 	df['corr_low'][elm] = divergence_out['macd'][1]
# 	df['corr_high'][elm] = divergence_out['macd'][2]

# #output = output.drop(columns = [0])
# #output = pd.concat([output, df], ignore_index=True)
# os.remove(path_elites_chrom)
# df.to_csv(path_elites_chrom)

# for elm in df['score'].index:
# 	if df['score'][elm] > 100:
# 		df['score'][elm] = 0.1

# 	if (
# 		df_learn['num_trade_pr'][elm] < 100 and
# 		df['score'][elm] >= 10
# 		):
# 		df['score'][elm] = df['score'][elm] / 5

# 	if df_learn['sum_tp_pr'][elm] < 0:
# 		df['score'][elm] = 0

# os.remove(path_elites_chrom)
# df.to_csv(path_elites_chrom)

# df = pd.read_csv(path_elites_learn).drop(columns='Unnamed: 0')

# for elm in df['score'].index:
# 	if df['score'][elm] > 100:
# 		df['score'][elm] = 0.1

# 	if (
# 		df['num_trade_pr'][elm] < 100 and
# 		df['score'][elm] >= 10
# 		):
# 		df['score'][elm] = df['score'][elm] / 5

# 	df['num_trade_pr'][elm] = df['num_tp_pr'][elm] + df['num_st_pr'][elm]

# 	if df['sum_tp_pr'][elm] < 0:
# 		df['score'][elm] = 0

# os.remove(path_elites_learn)
# df.to_csv(path_elites_learn)

# df = pd.read_csv(path_elites_super).drop(columns='Unnamed: 0')

# for elm in df['score'].index:
# 	if df['score'][elm] > 100:
# 		df['score'][elm] = 0.1

# 	if (
# 		df['num_trade_pr'][elm] < 100 and
# 		df['score'][elm] >= 10
# 		):
# 		df['score'][elm] = df['score'][elm] / 5

# 	if df_learn['sum_tp_pr'][elm] < 0:
# 		df['score'][elm] = 0

# os.remove(path_elites_super)
# df.to_csv(path_elites_super)

# df = pd.read_csv(path_elites_society).drop(columns='Unnamed: 0')

# for elm in df['score'].index:
# 	if df['score'][elm] > 100:
# 		df['score'][elm] = 0.1

# os.remove(path_elites_society)
# df.to_csv(path_elites_society)

# signalpriority = 'secondry'
# signaltype = 'sell'
# symbol = 'ETHUSD_i'

# path_elites_chrom = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_ChromosomeResults.csv'
# path_elites_learn = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_LearningResults.csv'
# path_elites_super = config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'
# path_elites_society = config.cfg['path_society'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'
# path_graveyard = config.cfg['path_graveyard'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'

# df = pd.read_csv(path_graveyard).drop(columns='Unnamed: 0')

# df = df.drop(columns = 'n_clusters_best_low')
# df = df.drop(columns = 'n_clusters_best_high')

# os.remove(path_graveyard)
# df.to_csv(path_graveyard)


# df = pd.read_csv(path_elites_learn).drop(columns='Unnamed: 0')

# df = df.drop(columns = 'n_clusters_best_low')
# df = df.drop(columns = 'n_clusters_best_high')

# os.remove(path_elites_learn)
# df.to_csv(path_elites_learn)


# df = pd.read_csv(path_elites_super).drop(columns='Unnamed: 0')

# df = df.drop(columns = 'n_clusters_best_low')
# df = df.drop(columns = 'n_clusters_best_high')

# os.remove(path_elites_super)
# df.to_csv(path_elites_super)


# df = pd.read_csv(path_elites_society).drop(columns='Unnamed: 0')

# df = df.drop(columns = 'n_clusters_best_low')
# df = df.drop(columns = 'n_clusters_best_high')

# os.remove(path_elites_society)
# df.to_csv(path_elites_society)




parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')
parameters.elements['symbol'] = 'XAUUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

macd = MACD(parameters = parameters, config = config)
macd_calc = macd.Genetic(
						dataset_5M = parameters.elements['dataset_5M'], 
						dataset_1H = parameters.elements['dataset_1H'], 
						symbol = 'XAUUSD_i',
						signaltype = 'buy', 
						signalpriority = 'primary', 
						num_turn = 40
						)

macd_calc = macd.GetPermit(
						dataset_5M = parameters.elements['dataset_5M'],
						dataset_1H = parameters.elements['dataset_1H'], 
						symbol = 'XAUUSD_i',
						signaltype = 'buy',
						signalpriority = 'primary',
						flag_savepic = False
						)