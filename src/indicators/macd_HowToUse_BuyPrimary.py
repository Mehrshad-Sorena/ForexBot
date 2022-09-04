from Mt5_LoginGetData import LoginGetData as getdata
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd
import os



loging = getdata()


parameters = Parameters()
config = Config()

# # ind_params = indicator_parameters()
# # ind_config = indicator_config()

# signalpriority = 'primary'
# signaltype = 'buy'
# symbol = 'ETHUSD_i'

# path_elites_chrom = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_ChromosomeResults.csv'
# path_elites_learn = config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_LearningResults.csv'
# path_elites_super = config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'
# path_elites_society = config.cfg['path_society'] + signalpriority + '/' + signaltype + '/' + symbol + '.csv'

# df = pd.read_csv(path_elites_chrom).drop(columns='Unnamed: 0')
# df_learn = pd.read_csv(path_elites_learn).drop(columns='Unnamed: 0')

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