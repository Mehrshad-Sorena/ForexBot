import pandas as pd
import seaborn as sns
from pathlib import Path
import requests
from io import BytesIO
from zipfile import ZipFile, BadZipFile
import pandas_datareader.data as web
# from talib import RSI, BBANDS, MACD, CCI, EMA, SMA, STOCH
import pandas_ta as ind
import numpy as np
import matplotlib.pyplot as plt


class FeatureEngineering:

	def __init__(self):
		
		self.lags = [1, 2, 3, 6, 9, 12, 24, 48]
		self.timelags = [1, 2, 3, 6, 9, 12, 24, 48]
		self.momentums = [1, 2, 3, 6, 9, 12, 24, 48]

		#SMA Parameters:
		self.config_sma_5m = [True, True, True, True, True, True, True]
		self.sma_5m_length = [  14,   25,   50,  100,  150,  200,  250]

		self.config_sma_1h = [True, True, True, True, True, True, True]
		self.sma_1h_length = [  14,   25,   50,  100,  150,  200,  250]
		#/////////////////////////////////////


		#EMA Parameters:
		self.config_ema_5m = [True, True, True, True, True, True, True]
		self.ema_5m_length = [  14,   25,   50,  100,  150,  200,  250]

		self.config_ema_1h = [True, True, True, True, True, True, True]
		self.ema_1h_length = [  14,   25,   50,  100,  150,  200,  250]
		#/////////////////////////////////////


		#RSI Parameters:
		self.config_rsi_5m = True
		self.rsi_5m_length = 14

		self.config_rsi_1h = True
		self.rsi_1h_length = 14
		#//////////////////////////////////////

		#BBAND Parameters:
		self.config_bband_5m = True
		self.bband_5m_length = 5 
		self.bband_5m_std = 2 
		self.bband_5m_ddof = 0 
		self.bband_5m_mamod = 'sma'

		self.config_bband_1h = True
		self.bband_1h_length = 5 
		self.bband_1h_std = 2 
		self.bband_1h_ddof = 0 
		self.bband_1h_mamod = 'sma'
		#/////////////////////////////////////

		#IchiMokou Parameters:
		self.config_ichi_5m = True
		self.ichi_5m_tenkan = 9
		self.ichi_5m_kijun = 26
		self.ichi_5m_senkou = 52

		self.config_ichi_1h = True
		self.ichi_1h_tenkan = 9
		self.ichi_1h_kijun = 26
		self.ichi_1h_senkou = 52
		#/////////////////////////////////////

		#MACD Parametere:
		self.config_macd_5m = True
		self.macd_5m_applyto = 'close_5m'
		self.macd_5m_fast = 12
		self.macd_5m_slow = 26
		self.macd_5m_signal = 9

		self.config_macd_1h = True
		self.macd_1h_applyto = 'close_1h'
		self.macd_1h_fast = 12
		self.macd_1h_slow = 26
		self.macd_1h_signal = 9
		#//////////////////////////////

		#StochAstic Parameters:
		self.config_stoch_5m = True
		self.stoch_5m_k = 14
		self.stoch_5m_d = 3
		self.stoch_5m_smooth_k = 3
		self.stoch_5m_mamod = 'sma'

		self.config_stoch_1h = True
		self.stoch_1h_k = 14
		self.stoch_1h_d = 3
		self.stoch_1h_smooth_k = 3
		self.stoch_1h_mamod = 'sma'
		#//////////////////////////////

		#CCI Parameters:
		self.config_cci_5m = True
		self.length_cci_5m = 14

		self.config_cci_1h = True
		self.length_cci_1h = 14
		#/////////////////////////////

		#Candle Patterns Parameters:
		self.config_pattern_5m = True

		self.config_pattern_1h = True
		#/////////////////////////////


	def DatasetCreation(self, dataset_5M, dataset_1H):

		dataset_5m = dataset_5M.copy(deep = True)
		dataset_5m.index = dataset_5m['time']

		dataset = pd.DataFrame()
		dataset = dataset.assign(
								close_5m = dataset_5m['close'],
								open_5m = dataset_5m['open'],
								low_5m = dataset_5m['low'],
								high_5m = dataset_5m['high'],
								HL2_5m = dataset_5m['HL/2'],
								HLC3_5m = dataset_5m['HLC/3'],
								HLCC4_5m = dataset_5m['HLCC/4'],
								OHLC4_5m = dataset_5m['OHLC/4'],
								volume_5m = dataset_5m['volume'],
								time_5m = dataset_5m['time'],
								)

		dataset.index = dataset['time_5m']

		dataset_1h = dataset_1H.copy(deep = True)
		dataset_1h.index = dataset_1h['time']

		dataset = dataset.assign(
								close_1h = dataset_1h['close'],
								open_1h = dataset_1h['open'],
								low_1h = dataset_1h['low'],
								high_1h = dataset_1h['high'],
								HL2_1h = dataset_1h['HL/2'],
								HLC3_1h = dataset_1h['HLC/3'],
								HLCC4_1h = dataset_1h['HLCC/4'],
								OHLC4_1h = dataset_1h['OHLC/4'],
								volume_1h = dataset_1h['volume'],
								time_1h = dataset_1h['time'],
								)

		dataset.index = range(0 , len(dataset['close_5m']))

		return dataset


	def FourierCreation():
		pass


	def LagCreation(self, dataset):

		dataset_lag = dataset.copy(deep = True)
		dataset_lag.index = dataset_lag['time_5m']
		dataset_lag = dataset_lag.drop(columns = ['time_5m', 'time_1h'])

		dataset_Hourly = dataset_lag.resample('15T').last()

		print(dataset_Hourly)

		outlier_cutoff = 0.01
		LagedData = pd.DataFrame()

		for lag in self.lags:
			LagedData[f'return_{lag}h'] = (dataset_Hourly
														.pct_change(lag)
														.stack()
														.pipe(lambda x:
																		x.clip(
																				lower=x.quantile(outlier_cutoff),
																				upper=x.quantile(1-outlier_cutoff)
																				)
															)
														.add(1)
														.pow(1/lag)
														.sub(1)
											)

		LagedData['real'] = (dataset_Hourly.stack())

		LagedData = LagedData.swaplevel().dropna()

		return LagedData


	def MemontumCreation(self, dataset):

		for lag in self.momentums:
			dataset[f'momentum_{lag}'] = dataset[f'return_{lag}h'].sub(dataset.return_1h)
		dataset[f'momentum_3_12'] = dataset[f'return_12h'].sub(dataset.return_3h)

		return dataset

	def LagShiftedCreation(self, dataset):

		for t in self.timelags:
			dataset[f'target_-{t}h'] = (dataset[f'return_{t}h'].shift(t))

		for t in self.lags:
			dataset[f'target_{t}h'] = (dataset[f'return_{t}h'].shift(-t))
		
		return dataset


	def TimeCreation(self, dataset):

		times = dataset.index.get_level_values('time_5m')
		dataset['hour'] = times.hour
		dataset['minute'] = times.minute

		return dataset

	def MainDataAdd(self, dataset, data):

		data['real'] = np.nan
		for clm in dataset.columns:
			data['real'] = dataset[clm].copy(deep = True)

		return data


	#Indicators Creation:

	def AlphaFactorRSI(self, dataset):

		if self.config_rsi_5m == True:

			rsi_5m = ind.rsi(dataset['close_5m'], length = self.rsi_5m_length)

			dataset = dataset.assign(rsi_5m = rsi_5m)


		if self.config_rsi_1h == True:

			rsi_1h = ind.rsi(dataset['close_1h'].dropna(), length = self.rsi_1h_length)

			dataset = dataset.assign(rsi_1h = rsi_1h)

		return dataset


	def AlphaFactorBBAND(self, dataset):

		if self.config_bband_5m == True:
			bband_ind_5m = ind.bbands(
									dataset['close_5m'], 
									length = self.bband_5m_length, #5, 
									std = self.bband_5m_std, #2, 
									ddof = self.bband_5m_ddof, #0, 
									mamod = self.bband_5m_mamod #'sma'
									)

			bband_lower_5m = bband_ind_5m[bband_ind_5m.columns[0]]
			bband_mid_5m = bband_ind_5m[bband_ind_5m.columns[1]]
			bband_upper_5m = bband_ind_5m[bband_ind_5m.columns[2]]
			bband_bandwidth_5m = bband_ind_5m[bband_ind_5m.columns[3]]
			bband_percent_5m = bband_ind_5m[bband_ind_5m.columns[4]]

			dataset = dataset.assign(
									bband_lower_5m = bband_lower_5m,
									bband_mid_5m = bband_mid_5m,
									bband_upper_5m = bband_upper_5m,
									bband_bandwidth_5m = bband_bandwidth_5m,
									bband_percent_5m = bband_percent_5m,
									)


		if self.config_bband_1h == True:
			bband_ind_1h = ind.bbands(
									dataset['close_1h'].dropna(), 
									length = self.bband_1h_length, #5, 
									std = self.bband_1h_std, #2, 
									ddof = self.bband_1h_ddof, #0, 
									mamod = self.bband_1h_mamod #'sma'
									)

			bband_lower_1h = bband_ind_1h[bband_ind_1h.columns[0]]
			bband_mid_1h = bband_ind_1h[bband_ind_1h.columns[1]]
			bband_upper_1h = bband_ind_1h[bband_ind_1h.columns[2]]
			bband_bandwidth_1h = bband_ind_1h[bband_ind_1h.columns[3]]
			bband_percent_1h = bband_ind_1h[bband_ind_1h.columns[4]]

			dataset = dataset.assign(
									bband_lower_1h = bband_lower_1h,
									bband_mid_1h = bband_mid_1h,
									bband_upper_1h = bband_upper_1h,
									bband_bandwidth_1h = bband_bandwidth_1h,
									bband_percent_1h = bband_percent_1h,
									)

		return dataset

	def AlphaFactorSMA(self, dataset):

		counter = 0
		for elm in self.config_sma_5m:

			if elm == True:
				sma_ind_5m = ind.sma(dataset['close_5m'], length = self.sma_5m_length[counter])

				dataset[f'sma_5m_{self.sma_5m_length[counter]}'] = sma_ind_5m

			counter += 1

		counter = 0
		for elm in self.config_sma_1h:

			if elm == True:
				sma_ind_1h = ind.sma(dataset['close_1h'].dropna(), length = self.sma_1h_length[counter])

				dataset[f'sma_1h_{self.sma_1h_length[counter]}'] = sma_ind_1h

			counter += 1
		
		return dataset

	def AlphaFactorEMA(self, dataset):

		counter = 0
		for elm in self.config_ema_5m:

			if elm == True:

				ema_ind_5m = ind.ema(dataset['close_5m'], length = self.ema_5m_length[counter])

				dataset[f'ema_5m_{self.ema_5m_length[counter]}'] = ema_ind_5m

			counter += 1


		counter = 0
		for elm in self.config_ema_1h:

			if elm == True:

				ema_ind_1h = ind.ema(dataset['close_1h'].dropna(), length = self.ema_1h_length[counter])

				dataset[f'ema_1h_{self.ema_1h_length[counter]}'] = ema_ind_1h

			counter += 1

		return dataset

	def AlphaFactorIchimokou(self, dataset):

		if self.config_ichi_5m == True:

			ichi_ind_5m, _ = ind.ichimoku(
										high = dataset['high_5m'],
										low = dataset['low_5m'],
										close = dataset['close_5m'],
										tenkan = self.ichi_5m_tenkan,
										kijun = self.ichi_5m_kijun,
										senkou = self.ichi_5m_senkou
										)

			spana_5m = ichi_ind_5m[ichi_ind_5m.columns[0]]
			spanb_5m = ichi_ind_5m[ichi_ind_5m.columns[1]]
			tenkan_5m = ichi_ind_5m[ichi_ind_5m.columns[2]]
			kijun_5m = ichi_ind_5m[ichi_ind_5m.columns[3]]
			chikou_5m = ichi_ind_5m[ichi_ind_5m.columns[4]]

			dataset = dataset.assign(
									spana_5m = spana_5m,
									spanb_5m = spanb_5m,
									tenkan_5m = tenkan_5m,
									kijun_5m = kijun_5m,
									chikou_5m = chikou_5m,
									)

		if self.config_ichi_1h == True:

			ichi_ind_1h, _ = ind.ichimoku(
										high = dataset['high_1h'].dropna(),
										low = dataset['low_1h'].dropna(),
										close = dataset['close_1h'].dropna(),
										tenkan = self.ichi_1h_tenkan,
										kijun = self.ichi_1h_kijun,
										senkou = self.ichi_1h_senkou
										)

			spana_1h = ichi_ind_1h[ichi_ind_1h.columns[0]]
			spanb_1h = ichi_ind_1h[ichi_ind_1h.columns[1]]
			tenkan_1h = ichi_ind_1h[ichi_ind_1h.columns[2]]
			kijun_1h = ichi_ind_1h[ichi_ind_1h.columns[3]]
			chikou_1h = ichi_ind_1h[ichi_ind_1h.columns[4]]

			dataset = dataset.assign(
									spana_1h = spana_1h,
									spanb_1h = spanb_1h,
									tenkan_1h = tenkan_1h,
									kijun_1h = kijun_1h,
									chikou_1h = chikou_1h,
									)
		

		return dataset

	def AlphaFactorMACD(self, dataset):

		if self.config_macd_5m == True:

			macd_ind_5m = ind.macd(
									dataset[self.macd_5m_applyto], 
									fast = self.macd_5m_fast, 
									slow = self.macd_5m_slow, 
									signal = self.macd_5m_signal
									)

			macd_5m = macd_ind_5m[macd_ind_5m.columns[0]]
			macds_5m = macd_ind_5m[macd_ind_5m.columns[1]]
			macdh_5m = macd_ind_5m[macd_ind_5m.columns[2]]

			dataset = dataset.assign(
									macd_5m = macd_5m,
									macds_5m = macds_5m,
									macdh_5m = macdh_5m,
									)

		if self.config_macd_1h == True:
			macd_ind_1h = ind.macd(
									dataset[self.macd_1h_applyto].dropna(), 
									fast = self.macd_1h_fast, 
									slow = self.macd_1h_slow, 
									signal = self.macd_1h_signal
									)

			macd_1h = macd_ind_1h[macd_ind_1h.columns[0]]
			macds_1h = macd_ind_1h[macd_ind_1h.columns[1]]
			macdh_1h = macd_ind_1h[macd_ind_1h.columns[2]]

			dataset = dataset.assign(
									macd_1h = macd_1h,
									macds_1h = macds_1h,
									macdh_1h = macdh_1h,
									)

		return dataset


	def AlphaFactorStochAstic(self, dataset):

		if self.config_stoch_5m == True:

			stoch_ind_5m = ind.stoch(
									high = dataset['high_5m'],
									low = dataset['low_5m'],
									close = dataset['close_5m'],
									k = self.stoch_5m_k, #14
									d = self.stoch_5m_d, #3
									smooth_k = self.stoch_5m_smooth_k, #3
									mamod = self.stoch_5m_mamod #'sma'
								)

			stoch_k_5m = stoch_ind_5m[stoch_ind_5m.columns[0]]
			stoch_d_5m = stoch_ind_5m[stoch_ind_5m.columns[1]]

			dataset = dataset.assign(	
									stoch_k_5m = stoch_k_5m,
									stoch_d_5m = stoch_d_5m,
									)

		if self.config_stoch_1h == True:

			stoch_ind_1h = ind.stoch(
									high = dataset['high_1h'].dropna(),
									low = dataset['low_1h'].dropna(),
									close = dataset['close_1h'].dropna(),
									k = self.stoch_1h_k,
									d = self.stoch_1h_d,
									smooth_k = self.stoch_1h_smooth_k,
									mamod = self.stoch_1h_mamod
								)

			stoch_k_1h = stoch_ind_1h[stoch_ind_1h.columns[0]]
			stoch_d_1h = stoch_ind_1h[stoch_ind_1h.columns[1]]

			dataset = dataset.assign(	
									stoch_k_1h = stoch_k_1h,
									stoch_d_1h = stoch_d_1h,
									)

		return dataset


	def AlphaFactorCCI(self, dataset):

		if self.config_cci_5m == True:

			cci_ind_5m = ind.cci(
								high = dataset['high_5m'],
								low = dataset['low_5m'],
								close = dataset['close_5m'],
								length = self.length_cci_5m
								)

			dataset = dataset.assign(
									cci_5m = cci_ind_5m,
									)

		if self.config_cci_1h == True:

			cci_ind_1h = ind.cci(
								high = dataset['high_1h'].dropna(),
								low = dataset['low_1h'].dropna(),
								close = dataset['close_1h'].dropna(),
								length = self.length_cci_1h
								)

			dataset = dataset.assign(
									cci_1h = cci_ind_1h,
									)
		return dataset

	#//////////////////////////////////////////////

	#Candle Patterns:

	def AlphaCandlePatterns(self, dataset):

		if self.config_pattern_5m == True:

			cdl_patterns_5m = ind.cdl_pattern(
											open_ = dataset['open_5m'],
											high = dataset['high_5m'],
											low = dataset['low_5m'],
											close = dataset['close_5m'],
											name = 'all'
											)

			counter = 0
			for pattern in cdl_patterns_5m.columns:

				dataset[f'pattern_5m_{counter}'] = cdl_patterns_5m[pattern]

				counter += 1

		if self.config_pattern_1h == True:

			cdl_patterns_1h = ind.cdl_pattern(
											open_ = dataset['open_1h'].dropna(),
											high = dataset['high_1h'].dropna(),
											low = dataset['low_1h'].dropna(),
											close = dataset['close_1h'].dropna(),
											name = 'all'
											)

			


			counter = 0
			for pattern in cdl_patterns_1h.columns:

				dataset[f'pattern_1h_{counter}'] = cdl_patterns_1h[pattern]

				counter += 1

		return dataset

	#//////////////////////////////////////////////





#with pd.option_context('display.max_rows', None, 'display.max_columns', None):

