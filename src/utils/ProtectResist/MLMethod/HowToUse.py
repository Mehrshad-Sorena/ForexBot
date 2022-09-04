from Mt5_LoginGetData import LoginGetData as getdata
from FeatureEngineering import FeatureEngineering
from NoiseCanceller import NoiseCanceller
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
loging = getdata()

dataset_5M, dataset_1H = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 500)

FE = FeatureEngineering()
print('dataset geted')
dataset = FE.DatasetCreation(dataset_5M = dataset_5M['XAUUSD_i'], dataset_1H = dataset_1H['XAUUSD_i'])
dataset = FE.AlphaCandlePatterns(dataset = dataset)
dataset = FE.AlphaFactorRSI(dataset = dataset)
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

numeric_feature_names = [
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
normalized_data = dataset[numeric_feature_names][500:len(dataset['close_5m']) - 2000]

print(normalized_data)

tf.convert_to_tensor(normalized_data)


normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(normalized_data)

normalized_data = normalizer(normalized_data)
print("var: %.4f" % np.var(normalized_data))
print("mean: %.4f" % np.mean(normalized_data))
print(normalized_data[:,0])

def get_basic_model():

	model = tf.keras.Sequential([
								normalizer,
								tf.keras.layers.Dense(1000, activation='relu'),
								tf.keras.layers.Dense(1000, activation='relu'),
								tf.keras.layers.Dense(1)
								])

	model.compile(
					optimizer='adam',
					loss=tf.keras.losses.BinaryCrossentropy(from_logits = True),
					metrics=['accuracy']
				)

	return model

SHUFFLE_BUFFER = 500
BATCH_SIZE = 400

target = normalized_data[:,0]
print(target)
print(normalized_data[:, 1:-1])

model = get_basic_model()
model.fit(normalized_data, target, epochs = 15, batch_size = BATCH_SIZE)

x_test = dataset['close_5m']
y = dataset['time_5m']
y_pred = model.predict(x_test)
print(y_pred)

plt.figure(figsize=(18, 6))
plt.plot(y , x_test)
plt.plot(y_pred)
plt.legend(["actual", "forecast"])

plt.show()

# naive_mse, model_mse = (
#     np.square(x_test[:, -1, :, 0] - y[:, 0, :]).mean(),
#     np.square(y_pred[:, 0, :] - y[:, 0, :]).mean(),
# )
# print(f"naive MAE: {naive_mse}, model MAE: {model_mse}")



noise_canceller = NoiseCanceller()

print(noise_canceller.NoiseKalmanFilter(dataset = dataset, applyto = 'close_5m'))
plt.plot(dataset_5M['XAUUSD_i']['close'].index[50:-1], dataset_5M['XAUUSD_i']['close'][50:-1], c = 'r')
plt.show()

#print(noise_canceller.NoiseWavelet(dataset = dataset, applyto = 'sma_5m_200'))