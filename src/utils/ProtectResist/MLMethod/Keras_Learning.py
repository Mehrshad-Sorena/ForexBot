from Mt5_LoginGetData import LoginGetData as getdata
from FeatureEngineering import FeatureEngineering
from NoiseCanceller import NoiseCanceller
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
from random import randint


# Returns: A tf.data.Dataset instance. 
# If targets was passed, the dataset yields tuple (batch_of_sequences, batch_of_targets). 
# If not, the dataset yields only batch_of_sequences.

# tf.keras.utils.timeseries_dataset_from_array(
# 											    data,  # Numpy array or eager tensor containing consecutive data points (timesteps)
# 											    targets,  # Targets corresponding to timesteps in data. targets[i]
# 											    sequence_length,  # Length of the output sequences
# 											    sequence_stride=1,  # Period between successive output sequences.
# 											    sampling_rate=1,  # Period between successive individual timesteps within sequences.
# 											    batch_size=128,  # Number of timeseries samples in each batch
# 											    shuffle=False,
# 											    seed=None,  # Optional int; random seed for shuffling.
# 											    start_index=None,
# 											    end_index=None,
# 											)


titles = [
		    'close_5m', 'HL2_5m', 'HLC3_5m', 'HLCC4_5m', 'OHLC4_5m', 'volume_5m',
			#'close_1h', 'open_1h', 'low_1h', 'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h', 'volume_1h',
			'rsi_5m', #'rsi_1h',
			'bband_lower_5m', 'bband_mid_5m', 'bband_upper_5m', 'bband_bandwidth_5m', 'bband_percent_5m',
			#'bband_lower_1h', 'bband_mid_1h', 'bband_upper_1h', 'bband_bandwidth_1h', 'bband_percent_1h',
			'sma_5m_14', 'sma_5m_25', 'sma_5m_50', 'sma_5m_100', 'sma_5m_150', 'sma_5m_200', 'sma_5m_250',
			#'sma_1h_14', 'sma_1h_25', 'sma_1h_50', 'sma_1h_100', 'sma_1h_150', 'sma_1h_200', 'sma_1h_250',
			'ema_5m_14', 'ema_5m_25', 'ema_5m_50', 'ema_5m_100', 'ema_5m_150', 'ema_5m_200', 'ema_5m_250',
			#'ema_1h_14', 'ema_1h_25', 'ema_1h_50', 'ema_1h_100', 'ema_1h_150', 'ema_1h_200', 'ema_1h_250',
			'spana_5m', 'spanb_5m', 'tenkan_5m', 'kijun_5m', 'chikou_5m', 
			#'spana_1h', 'spanb_1h', 'tenkan_1h', 'kijun_1h', 'chikou_1h',
			'macd_5m', 'macds_5m', 'macdh_5m',
			#'macd_1h', 'macds_1h', 'macdh_1h',
			'stoch_k_5m', 'stoch_d_5m',
			#'stoch_k_1h', 'stoch_d_1h',
			'cci_5m', #'cci_1h',
		]

feature_keys = [
				'close_5m', 'HL2_5m', 'HLC3_5m', 'HLCC4_5m', 'OHLC4_5m', 'volume_5m',
				#'close_1h', 'open_1h', 'low_1h', 'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h', 'volume_1h',
				'rsi_5m', #'rsi_1h',
				'bband_lower_5m', 'bband_mid_5m', 'bband_upper_5m', 'bband_bandwidth_5m', 'bband_percent_5m',
				#'bband_lower_1h', 'bband_mid_1h', 'bband_upper_1h', 'bband_bandwidth_1h', 'bband_percent_1h',
				'sma_5m_14', 'sma_5m_25', 'sma_5m_50', 'sma_5m_100', 'sma_5m_150', 'sma_5m_200', 'sma_5m_250',
				#'sma_1h_14', 'sma_1h_25', 'sma_1h_50', 'sma_1h_100', 'sma_1h_150', 'sma_1h_200', 'sma_1h_250',
				'ema_5m_14', 'ema_5m_25', 'ema_5m_50', 'ema_5m_100', 'ema_5m_150', 'ema_5m_200', 'ema_5m_250',
				#'ema_1h_14', 'ema_1h_25', 'ema_1h_50', 'ema_1h_100', 'ema_1h_150', 'ema_1h_200', 'ema_1h_250',
				'spana_5m', 'spanb_5m', 'tenkan_5m', 'kijun_5m', 'chikou_5m', 
				#'spana_1h', 'spanb_1h', 'tenkan_1h', 'kijun_1h', 'chikou_1h',
				'macd_5m', 'macds_5m', 'macdh_5m',
				#'macd_1h', 'macds_1h', 'macdh_1h',
				'stoch_k_5m', 'stoch_d_5m',
				#'stoch_k_1h', 'stoch_d_1h',
				'cci_5m', #'cci_1h',
				]

colors = [
		    "blue",
		    "orange",
		    "green",
		    "red",
		    "purple",
		    "brown",
		    "pink",
		    "gray",
		    "olive",
		    "cyan",
		]

date_time_key = "time_5m"


def show_raw_visualization(data):
    time_data = data[date_time_key]

    fig, axes = plt.subplots(nrows=int(len(feature_keys)/2)+1, ncols=2, figsize=(15, 20), dpi=80, facecolor="w", edgecolor="k")

    for i in range(len(feature_keys)):
        key = feature_keys[i]
        c = colors[i % (len(colors))]
        t_data = data[key]
        t_data.index = time_data
        t_data.head()
        ax = t_data.plot(
			            ax=axes[i // 2, i % 2],
			            color=c,
			            title="{} - {}".format(titles[i], key),
			            rot=25,
        				)
        ax.legend([titles[i]])
    plt.tight_layout()
    plt.show()

def show_heatmap(data):
    plt.matshow(data.corr())
    plt.xticks(range(data.shape[1]), data.columns, fontsize=14, rotation=90)
    plt.gca().xaxis.tick_bottom()
    plt.yticks(range(data.shape[1]), data.columns, fontsize=14)

    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title("Feature Correlation Heatmap", fontsize=14)
    plt.show()


loging = getdata()
dataset_5M, dataset_1H = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')

FE = FeatureEngineering()
print('dataset geted')
dataset = FE.DatasetCreation(dataset_5M = dataset_5M['XAUUSD_i'], dataset_1H = dataset_1H['XAUUSD_i'])


FE.ichi_5m_tenkan = 9
FE.ichi_5m_kijun = 26
FE.ichi_5m_senkou = 52

FE.macd_5m_fast = 4
FE.macd_5m_slow = 9
FE.macd_5m_signal = 50

FE.rsi_5m_length = 26

dataset = FE.AlphaFactorIchimokou(dataset = dataset)
dataset = FE.AlphaFactorRSI(dataset = dataset)

dataset = FE.AlphaFactorSMA(dataset = dataset)

dataset = FE.AlphaFactorMACD(dataset = dataset)

dataset = dataset.drop(columns = ['macd_1h', 'macds_1h', 'macdh_1h'])

dataset = dataset.drop(columns = ['sma_1h_14', 'sma_1h_25', 'sma_1h_50', 'sma_1h_100', 'sma_1h_150', 'sma_1h_200', 'sma_1h_250'])

dataset = dataset.drop(columns = ['tenkan_1h', 'kijun_1h', 'chikou_1h', 'spana_1h', 
									'spanb_1h', 'close_1h', 'open_1h', 'low_1h', 
									'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h', 'volume_1h',
									'rsi_1h', ])

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(dataset.corr())

import sys

sys.exit()
# dataset = FE.AlphaCandlePatterns(dataset = dataset)
#dataset = FE.AlphaFactorRSI(dataset = dataset)



from scipy.optimize import minimize
import scipy.stats

FE.sma_5m_length = range(2 , 1000, 10)
FE.config_sma_5m = np.ones(len(FE.sma_5m_length))
FE.config_sma_1H = np.ones(len(FE.sma_5m_length)) * False
print(FE.config_sma_1H)

dataset = FE.AlphaFactorSMA(dataset = dataset)

dataset = dataset.drop(columns = ['sma_1h_14', 'sma_1h_25', 'sma_1h_50', 'sma_1h_100', 'sma_1h_150', 'sma_1h_200', 'sma_1h_250'])

for i in range(2 , 1000, 10):

	print('i = ', i)
	print(scipy.stats.pearsonr(dataset['close_5m'][dataset[f'sma_5m_{i}'].dropna().index[0]-1:-1], dataset[f'sma_5m_{i}'].dropna()))    # Pearson's r

	print(scipy.stats.spearmanr(dataset['close_5m'][dataset[f'sma_5m_{i}'].dropna().index[0]-1:-1], dataset[f'sma_5m_{i}'].dropna()))   # Spearman's rho

	print(scipy.stats.kendalltau(dataset['close_5m'][dataset[f'sma_5m_{i}'].dropna().index[0]-1:-1], dataset[f'sma_5m_{i}'].dropna()))

	print()

print(dataset.corr())


FE.rsi_5m_length = 200

dataset = FE.AlphaFactorRSI(dataset = dataset)

print('pers = ',
		dataset.corr().drop(
									index = [
											'volume_5m', 'close_1h', 'open_1h', 'low_1h', 
											'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h',
											'volume_1h', 'rsi_5m', 'rsi_1h'
											]
									)
	)

print('spearman = ',
		dataset.corr(method='spearman').drop(
									index = [
											'volume_5m', 'close_1h', 'open_1h', 'low_1h', 
											'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h',
											'volume_1h', 'rsi_5m', 'rsi_1h'
											]
									)
	)

print('kendall = ',
		dataset.corr(method='kendall').drop(
									index = [
											'volume_5m', 'close_1h', 'open_1h', 'low_1h', 
											'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h',
											'volume_1h', 'rsi_5m', 'rsi_1h'
											]
									)
		)

# cost function
def cost_fun(x0, dataset):
	FE.rsi_5m_length = int(randint(2 , 4500))
	#FE.rsi_1h_length = int(x0[1])

	#print('rsi coef = ', FE.rsi_5m_length)

	dataset = FE.AlphaFactorRSI(dataset = dataset)
	#print('corr = ',dataset.corr())
	return -abs(dataset.corr().drop(
									index = [
											'volume_5m', 'close_1h', 'open_1h', 'low_1h', 
											'high_1h', 'HL2_1h', 'HLC3_1h', 'HLCC4_1h', 'OHLC4_1h',
											'volume_1h', 'rsi_5m', 'rsi_1h'
											]
									)['rsi_5m'].min())

# run minimizer
# res = minimize(
# 				cost_fun, 
# 				x0 = np.ones(1), 
# 				args = (dataset), 
# 				method = 'Nelder-Mead',
# 				options={"maxiter": 10000, "disp": True}
# 				)

dataset = FE.AlphaFactorRSI(dataset = dataset)
print(dataset.corr())
print('max corr = ',dataset.corr().mean())
print('rsi 5m length = ', FE.rsi_5m_length)
# results
print('res = ',res)


dataset = FE.AlphaFactorBBAND(dataset = dataset)
dataset = FE.AlphaFactorSMA(dataset = dataset)
dataset = FE.AlphaFactorEMA(dataset = dataset)
dataset = FE.AlphaFactorIchimokou(dataset = dataset)
dataset = FE.AlphaFactorMACD(dataset = dataset)
dataset = FE.AlphaFactorStochAstic(dataset = dataset)
dataset = FE.AlphaFactorCCI(dataset = dataset)



data = FE.LagCreation(dataset = dataset)
data = FE.MemontumCreation(dataset = data)
data = FE.LagShiftedCreation(dataset = data)
data = FE.TimeCreation(dataset = data)
# data = FE.MainDataAdd(dataset = dataset, data = data)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):

# from statsmodels.graphics.tsaplots import plot_acf
# plot_acf(data, lags=50)
# plt.show()


# print(data.loc['close_5m'])
print(data.info())
print(data)
show_heatmap(data = data)

split_fraction = 0.715
train_split = int(split_fraction * int(data.shape[0]))
step = 6

past = 720
future = 72
learning_rate = 0.001
batch_size = 256
epochs = 10


def normalize(data, train_split):
    data_mean = data[:train_split].mean(axis=0)
    data_std = data[:train_split].std(axis=0)
    return (data - data_mean) / data_std

# show_raw_visualization(data = dataset)
# show_heatmap(data = dataset)