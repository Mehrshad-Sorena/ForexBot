from Mt5_LoginGetData import LoginGetData as getdata
from indicator_Divergence import Divergence
from src.Indicators.MACD.Parameters import Parameters
from src.Indicators.MACD.Config import Config
from src.Indicators.MACD import MACD
import pandas as pd
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config
from indicator_Tester import Tester
import numpy as np
from random import randint
import random
from timer import stTime
from NoiseCanceller import NoiseCanceller
import ExtremePoints as extremepoints
import matplotlib.pyplot as plt
import sys
import os
import winsound
import threading
from multiprocessing import Process
import time
loging = getdata()


parameters = Parameters()
config = Config()

ind_params = indicator_parameters()
ind_config = indicator_config()



parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')
parameters.elements['MACD_symbol'] = 'XAUUSD_i'
parameters.elements['MACD_apply_to'] = 'close'

noise_canceller = NoiseCanceller()

# print('close ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['close'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'close')
# print('open ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['open'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'open')
# print('low ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['low'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'low')
# print('high ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['high'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'high')
# print('HL/2 ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['HL/2'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'HL/2')
# print('HLC/3 ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['HLC/3'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'HLC/3')
# print('OHLC/4 ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['OHLC/4'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'OHLC/4')
# print('HLCC/4 ...')
# parameters.elements['dataset_5M']['XAUUSD_i']['HLCC/4'] = noise_canceller.NoiseKalmanFilter(dataset = parameters.elements['dataset_5M']['XAUUSD_i'], applyto = 'HLCC/4')

#@stTime
def macd_optimizer(turn, main_turn, sigtype, sigpriority):
	print('Start ...')
	parameters.elements['dataset_5M']['XAUUSD_i']['index'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
	parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('time').resample('15T').last().dropna()
	parameters.elements['dataset_5M']['XAUUSD_i']['time'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
	parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('index')

	path = 'optimize/macd' + '_' + sigtype + '_' + sigpriority + '.csv'

	if os.path.exists(path):
		output_read = pd.read_csv(path).drop(columns = ['Unnamed: 0'])
	else:
		output_read = pd.DataFrame()
		output_read['MACD_apply_to'] = np.nan
		output_read['MACD_fast'] = np.nan
		output_read['MACD_slow'] = np.nan
		output_read['MACD_signal'] = np.nan
		output_read['MACD_column_div'] = np.nan
		output_read['corr_low'] = np.nan
		output_read['corr_high'] = np.nan
		output_read['diff_divergence'] = np.nan
		output_read['num_extreme_min'] = np.nan
		output_read['num_extreme_max'] = np.nan
		output_read['score'] = np.nan
	
	output = pd.DataFrame(np.ones(turn))
	output['MACD_apply_to'] = np.nan
	output['MACD_fast'] = np.nan
	output['MACD_slow'] = np.nan
	output['MACD_signal'] = np.nan
	output['MACD_column_div'] = np.nan
	output['corr_low'] = np.nan
	output['corr_high'] = np.nan
	output['diff_divergence'] = np.nan
	output['num_extreme_min'] = np.nan
	output['num_extreme_max'] = np.nan
	output['score'] = np.nan

	for i in range(turn):
		parameters.elements['MACD' + '_apply_to'] = random.choice([
																	'open',
																	'close',
																	'low',
																	'high',
																	'HL/2',
																	'HLC/3',
																	'HLCC/4',
																	'OHLC/4'
																	])
		parameters.elements['MACD' + '_fast'] = randint(2, 300)
		parameters.elements['MACD' + '_slow'] = randint(2 , 700)
		parameters.elements['MACD' + '_signal'] = randint(2 , 50)

		ind_params.elements['Divergence' + '_diff_extereme'] = randint(1 , 6)
		ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(2 , 500)
		ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(2 , 500)

		dive_column = random.choice(['macd', 'macds', 'macdh'])

		while parameters.elements['MACD' + '_fast'] >= parameters.elements['MACD' + '_slow'] + 10:
			parameters.elements['MACD' + '_fast'] = randint(2, 300)
			parameters.elements['MACD' + '_slow'] = randint(2 , 700)

		repeat_counter = 0
		if output.dropna().empty == False:

			repeat_checker_now = np.where(
										(parameters.elements['MACD' + '_fast'] == output['MACD_fast'].values) &
										(parameters.elements['MACD' + '_slow'] == output['MACD_slow'].values) &
										(parameters.elements['MACD' + '_signal'] == output['MACD_signal'].values) &
										(ind_params.elements['Divergence' + '_diff_extereme'] == output['diff_divergence'].values) &
										(ind_params.elements['Divergence' + '_num_exteremes_min'] == output['num_extreme_min'].values) &
										(parameters.elements['MACD' + '_apply_to'] == output['MACD_apply_to'].values) &
										(dive_column == output['MACD_column_div'].values)
									)[0]

			repeat_checker_before = np.where(
										(parameters.elements['MACD' + '_fast'] == output_read['MACD_fast'].values) &
										(parameters.elements['MACD' + '_slow'] == output_read['MACD_slow'].values) &
										(parameters.elements['MACD' + '_signal'] == output_read['MACD_signal'].values) &
										(ind_params.elements['Divergence' + '_diff_extereme'] == output_read['diff_divergence'].values) &
										(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_read['num_extreme_min'].values) &
										(parameters.elements['MACD' + '_apply_to'] == output_read['MACD_apply_to'].values) &
										(dive_column == output_read['MACD_column_div'].values)
									)[0]

			while (
					len(repeat_checker_now) > 0 or
					len(repeat_checker_before) >0
					):
				parameters.elements['MACD' + '_apply_to'] = random.choice([
																			'open',
																			'close',
																			'low',
																			'high',
																			'HL/2',
																			'HLC/3',
																			'HLCC/4',
																			'OHLC/4'
																			])
				parameters.elements['MACD' + '_fast'] = randint(2, 300)
				parameters.elements['MACD' + '_slow'] = randint(2 , 700)
				parameters.elements['MACD' + '_signal'] = randint(2 , 50)

				ind_params.elements['Divergence' + '_diff_extereme'] = randint(1 , 6)
				ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(2 , 250)
				ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(2 , 250)

				dive_column = random.choice(['macd', 'macds', 'macdh'])

				while parameters.elements['MACD' + '_fast'] >= parameters.elements['MACD' + '_slow'] + 10:
					parameters.elements['MACD' + '_fast'] = randint(2, 300)
					parameters.elements['MACD' + '_slow'] = randint(2 , 700)

				repeat_checker_now = np.where(
										(parameters.elements['MACD' + '_fast'] == output['MACD_fast'].values) &
										(parameters.elements['MACD' + '_slow'] == output['MACD_slow'].values) &
										(parameters.elements['MACD' + '_signal'] == output['MACD_signal'].values) &
										(ind_params.elements['Divergence' + '_diff_extereme'] == output['diff_divergence'].values) &
										(ind_params.elements['Divergence' + '_num_exteremes_min'] == output['num_extreme_min'].values) &
										(parameters.elements['MACD' + '_apply_to'] == output['MACD_apply_to'].values) &
										(dive_column == output['MACD_column_div'].values)
									)[0]

				repeat_checker_before = np.where(
											(parameters.elements['MACD' + '_fast'] == output_read['MACD_fast'].values) &
											(parameters.elements['MACD' + '_slow'] == output_read['MACD_slow'].values) &
											(parameters.elements['MACD' + '_signal'] == output_read['MACD_signal'].values) &
											(ind_params.elements['Divergence' + '_diff_extereme'] == output_read['diff_divergence'].values) &
											(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_read['num_extreme_min'].values) &
											(parameters.elements['MACD' + '_apply_to'] == output_read['MACD_apply_to'].values) &
											(dive_column == output_read['MACD_column_div'].values)
										)[0]

				if repeat_counter >= len(output_read['MACD_fast'].dropna().index): break
				repeat_counter += 1
			

		output['MACD_apply_to'][i] = parameters.elements['MACD' + '_apply_to']
		output['MACD_fast'][i] = parameters.elements['MACD' + '_fast']
		output['MACD_slow'][i] = parameters.elements['MACD' + '_slow']
		output['MACD_signal'][i] = parameters.elements['MACD' + '_signal']
		output['MACD_column_div'][i] = dive_column


		macd = MACD(parameters = parameters, config = config)
		macd_calc = macd.calculator_macd()


		macd = Divergence(parameters = ind_params, config = ind_config)
		signal, signaltype, indicator = macd.divergence(
														sigtype = sigtype,
														sigpriority = sigpriority,
														indicator = macd_calc,
														column_div = dive_column,
														ind_name = 'macd',
														dataset_5M = parameters.elements['dataset_5M'],
														dataset_1H = parameters.elements['dataset_1H'],
														symbol = 'XAUUSD_i',
														flaglearn = False,
														flagtest = True
														)
		if signal.empty == True: continue
		divergence_out = pd.DataFrame(np.ones(signal.index[-1]))
		divergence_out['macd'] = np.nan
		divergence_out['low'] = np.nan
		divergence_out['high'] = np.nan

		counter = 0
		for elm in signal.index:
			divergence_out['macd'][counter] = signal.indicator_front[elm]
			divergence_out['macd'][counter + 1] = signal.indicator_back[elm]

			divergence_out['low'][counter] = signal.low_front[elm]
			divergence_out['low'][counter + 1] = signal.low_back[elm]

			divergence_out['high'][counter] = signal.high_front[elm]
			divergence_out['high'][counter + 1] = signal.high_back[elm]

			counter += 2

		divergence_out = divergence_out.dropna()
		divergence_out = divergence_out.drop(columns = [0])

		number_divergence = len(divergence_out.index)/1000

		divergence_out = divergence_out.corr()

		output['score'][i] = -((divergence_out['macd'][2] * divergence_out['macd'][1] * number_divergence) ** (1/3))

		if (
			divergence_out['macd'][2] > 0 and
			divergence_out['macd'][1] > 0
			):
			output['score'][i] = -output['score'][i]

		output['corr_low'][i] = divergence_out['macd'][1]
		output['corr_high'][i] = divergence_out['macd'][2]
		output['diff_divergence'][i] = ind_params.elements['Divergence' + '_diff_extereme']
		output['num_extreme_min'][i] = ind_params.elements['Divergence' + '_num_exteremes_min']
		output['num_extreme_max'][i] = ind_params.elements['Divergence' + '_num_exteremes_max']
		#print(output.head(i))
		print('turn = ', main_turn * i, ', score = ', output_read['score'].min(), ' ', sigtype, ' ', sigpriority)

	if os.path.exists(path):
		os.remove(path)

	output = output.drop(columns = [0])
	output = pd.concat([output, output_read], ignore_index=True)

	output.dropna().sort_values(by = ['score'], ascending = False).to_csv(path)

	return output.dropna().sort_values(by = ['score'], ascending = False)

@stTime
def task_optimizer(main_turn):

	try:
	    job_thread_buy_primary = threading.Thread(
				    								target = macd_optimizer, 
				    								args = [
				    										100, 
				    										main_turn,
				    										'buy',
				    										'primary'
				    										]
				    							)
	except Exception as ex:
		print(ex)

    # job_thread_buy_primary = Process(
	   #  								target = macd_optimizer, 
	   #  								args = [
	   #  										100, 
	   #  										main_turn,
	   #  										'buy',
	   #  										'primary'
	   #  										]
	   #  							)

	try:
	    job_thread_buy_secondry = threading.Thread(
					    								target = macd_optimizer, 
					    								args = [
					    										100, 
					    										main_turn,
					    										'buy',
					    										'secondry'
					    										]
					    							)

	except Exception as ex:
		print(ex)

    # job_thread_buy_secondry = Process(
	   #  								target = macd_optimizer, 
	   #  								args = [
	   #  										100, 
	   #  										main_turn,
	   #  										'buy',
	   #  										'secondry'
	   #  										]
	   #  							)

	try:
	    job_thread_sell_primary = threading.Thread(
					    								target = macd_optimizer, 
					    								args = [
					    										100, 
					    										main_turn,
					    										'sell',
					    										'primary'
					    										]
					    							)
	except Exception as ex:
		print(ex)

    # job_thread_sell_primary = Process(
	   #  								target = macd_optimizer, 
	   #  								args = [
	   #  										100, 
	   #  										main_turn,
	   #  										'sell',
	   #  										'primary'
	   #  										]
	   #  							)

	try:
	    job_thread_sell_secondry = threading.Thread(
					    								target = macd_optimizer, 
					    								args = [
					    										100, 
					    										main_turn,
					    										'sell',
					    										'secondry'
					    										]
					    							)
	except Exception as ex:
		print(ex)

	job_thread_buy_primary.start()
	time.sleep(10)
	job_thread_buy_secondry.start()
	time.sleep(10)
	job_thread_sell_primary.start()
	time.sleep(10)
	job_thread_sell_secondry.start()

	job_thread_buy_primary.join()
	job_thread_buy_secondry.join()
	job_thread_sell_primary.join()
	job_thread_sell_secondry.join()
    

#*************************************************************
# for i in range(1, 10000):
# 		# macd_optimizer_output = macd_optimizer(100, main_turn = i, sigtype = 'buy', sigpriority = 'secondry')

# 	task_optimizer(main_turn = i)

# 	frequency = 1000  # Set Frequency To 2500 Hertz
# 	duration = 100  # Set Duration To 1000 ms == 1 second
# 	winsound.Beep(frequency, duration)
#/////////////////////////////////////////////////////////////

# macd_optimizer_output = macd_optimizer_output.dropna()
# macd_optimizer_output = macd_optimizer_output.sort_values(by = ['score'], ascending = False)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(macd_optimizer_output.iloc[len(macd_optimizer_output) - 5 :])


# frequency = 5000  # Set Frequency To 2500 Hertz
# duration = 100  # Set Duration To 1000 ms == 1 second

# for i in range(0, 20):
# 	winsound.Beep(frequency, duration) 

# sys.exit()

def plot_periodogram(ts, detrend='linear', ax=None):
    from scipy.signal import periodogram
    fs = pd.Timedelta("1Y") / pd.Timedelta("1H")
    print(pd.Timedelta("5T"))
    print(pd.Timedelta("1Y"))
    print(fs)
    freqencies, spectrum = periodogram(
								        ts,
								        fs=fs,
								        detrend=detrend,
								        window="boxcar",
								        scaling='spectrum',
								    )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    print(freqencies)
    spectrum_counter = 0
    for elm in spectrum:
    	if elm == np.max(spectrum):
    		freq = freqencies[spectrum_counter]
    	spectrum_counter += 1
    print('freq = ', freq)

    period_time = (freq * pd.Timedelta("1H"))/pd.Timedelta("1Y")
    
    print('period time = ', period_time)

    ax.set_xscale("log")
    ax.set_xticks([1, 100, 1000, 10000, 100000])
    # ax.set_xticklabels(
				#         [
				#             "Annual (1)",
				#             "Semiannual (2)",
				#             "Quarterly (4)",
				#             "Bimonthly (6)",
				#             "Monthly (12)",
				#             "Biweekly (26)",
				#             "Weekly (52)",
				#             "Semiweekly (104)",
				#         ],
				#         rotation=30,
				#     )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    return ax

# Fourier Transfer Fuction: ********************************************************

# from scipy import signal
# func = signal.TransferFunction(parameters.elements['dataset_5M']['XAUUSD_i'].index.minute, parameters.elements['dataset_5M']['XAUUSD_i']['low'].values)
# print('poles = ', func.poles)

# for elm in func.poles:
# 	print('pole = ',abs(elm))

# sys.exit()
# ////////////////////////////////////////////////////////////////////////////////////

#Decompose: *********************************************************************
# from statsmodels.tsa.seasonal import seasonal_decompose
# analysis = parameters.elements['dataset_5M']['XAUUSD_i'].copy(deep = True)
# print(analysis['low'])

# # for i in range(400, 2000, 50):
# decompose_result_mult = seasonal_decompose(analysis['close'], model="multiplicative", period = 1000)

# trend = decompose_result_mult.trend
# seasonal = decompose_result_mult.seasonal
# residual = decompose_result_mult.resid

# print(seasonal)

# decompose_result_mult.plot();
# plt.show()
# sys.exit()

#////////////////////////////////////////////////////////////////////////////////////

# N = range(0 , len(parameters.elements['dataset_5M']['XAUUSD_i'].index))
# plt.plot(N, parameters.elements['dataset_5M']['XAUUSD_i'].low, c = 'r')

#Fourier Tarnsform: ****************************************************************

# from scipy.fft import fft, fftfreq

# # days within a week# Number of sample points
# N = len(parameters.elements['dataset_5M']['XAUUSD_i'].index)
# # sample spacing
# T = N * 288

# print(N)
# print(T)

# yf = fft(parameters.elements['dataset_5M']['XAUUSD_i']['low'].values)
# xf = fftfreq(N, T)

# for elm in yf:
# 	print(abs(elm))
# print(yf)
# print('xf = ',xf*T)
# import matplotlib.pyplot as plt
# plt.plot(xf, 2.0/N * np.abs(yf))
# plt.grid()
# plt.show()
#////////////////////////////////////////////////////////////////////////////////////

#Periodogram:********************************************************************************
# parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('time').resample('5T').last().dropna()
# print(parameters.elements['dataset_5M']['XAUUSD_i'])
# macd = MACD(parameters = parameters, config = config)
# macd_calc = macd.calculator_macd()
# macd_calc = macd_calc.assign(time = parameters.elements['dataset_5M']['XAUUSD_i']['time'])
# macd_calc = macd_calc.set_index('time').resample('5T').last().dropna()
plot_periodogram(parameters.elements['dataset_1H']['XAUUSD_i'].close)#parameters.elements['dataset_5M']['XAUUSD_i'].close)
plt.show()
sys.exit()
#////////////////////////////////////////////////////////////////////////////////////

#Plot Periodogram: ************************************************************************
# from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

# fourier = CalendarFourier(freq="5T", order=10)  # 10 sin/cos pairs for "A"nnual seasonality
# print(fourier)

# dp = DeterministicProcess(
# 						    index=signal_out.index,
# 						    constant=True,               # dummy feature for bias (y-intercept)
# 						    order=1,                     # trend (order 1 means linear)
# 						    seasonal=True,               # weekly seasonality (indicators)
# 						    additional_terms=[fourier],  # annual seasonality (fourier)
# 						    drop=True,                   # drop terms to avoid collinearity
# 						)

# X = dp.in_sample()  # create features for dates in tunnel.index

#////////////////////////////////////////////////////////////////////////////////////


def extereme_optimizer(turn):

	parameters.elements['dataset_5M']['XAUUSD_i']['index'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
	parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('time').resample('15T').last().dropna()
	parameters.elements['dataset_5M']['XAUUSD_i']['time'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
	parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('index')

	output_min = pd.DataFrame(np.ones(turn))
	output_max = pd.DataFrame(np.ones(turn))
	output_min['num_extreme_min'] = np.nan
	output_max['num_extreme_max'] = np.nan
	output_min['score_min'] = np.nan
	output_max['score_max'] = np.nan
	output_min['number_min_finded'] = np.nan
	output_max['number_max_finded'] = np.nan

	for turn_counter in range(turn):
		#print('turn = ', turn_counter)

		ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(1 , 500)
		ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(1 , 500)

		if output_min.empty == False or output_max.empty == False:

			min_counter = 0
			min_repeat = np.where(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_min['num_extreme_min'].values)[0]
			while len(min_repeat) > 0:
				ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(1 , 500)
				min_repeat = np.where(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_min['num_extreme_min'].values)[0]
				
				if min_counter >= 500:
					min_counter = 500
					min_repeat = []

				min_counter += 1

			max_counter = 0
			max_repeat = np.where(ind_params.elements['Divergence' + '_num_exteremes_max'] == output_max['num_extreme_max'].values)[0]
			while len(max_repeat) > 0:
				ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(1 , 500)
				max_repeat = np.where(ind_params.elements['Divergence' + '_num_exteremes_max'] == output_max['num_extreme_max'].values)[0]

				if max_counter >= 500:
					max_counter = 500
					max_repeat = []
				max_counter += 1
			
			if min_counter + max_counter >= 1000:
				break

		extremes_points = extremepoints.finder(
												high = parameters.elements['dataset_5M']['XAUUSD_i']['high'],
												low = parameters.elements['dataset_5M']['XAUUSD_i']['low'],
												number_min = ind_params.elements['Divergence' + '_num_exteremes_min'],
												number_max = ind_params.elements['Divergence' + '_num_exteremes_max']
												)

		extreme_min = pd.DataFrame(
									{
										'min': extremes_points['min'],
										'index': extremes_points['index_min'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		extreme_min['index'] = extreme_min['index'].astype('int32')
		extreme_min.index = extreme_min['index']
		parameters.elements['dataset_5M']['XAUUSD_i']['min'] = np.nan
		parameters.elements['dataset_5M']['XAUUSD_i']['min'] = extreme_min['min']

		extreme_max = pd.DataFrame(
									{
										'max': extremes_points['max'],
										'index': extremes_points['index_max'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		extreme_max['index'] = extreme_max['index'].astype('int32')
		extreme_max.index = extreme_max['index']
		parameters.elements['dataset_5M']['XAUUSD_i']['max'] = np.nan
		parameters.elements['dataset_5M']['XAUUSD_i']['max'] = extreme_max['max']

	
		# plt.plot(parameters.elements['dataset_5M']['XAUUSD_i'].index, parameters.elements['dataset_5M']['XAUUSD_i']['low'])
	

		pct_change_low = (parameters.elements['dataset_5M']['XAUUSD_i']['low'].pct_change(ind_params.elements['Divergence' + '_num_exteremes_min'])[extreme_min.index] * 100) / ind_params.elements['Divergence' + '_num_exteremes_min']
		pct_change_low_inverse = (parameters.elements['dataset_5M']['XAUUSD_i']['low'].pct_change(-ind_params.elements['Divergence' + '_num_exteremes_min'])[extreme_min.index] * 100) / ind_params.elements['Divergence' + '_num_exteremes_min']
		
		pct_change_high = (parameters.elements['dataset_5M']['XAUUSD_i']['high'].pct_change(ind_params.elements['Divergence' + '_num_exteremes_max'])[extreme_max.index] * 100) / ind_params.elements['Divergence' + '_num_exteremes_max']
		pct_change_high_inverse = (parameters.elements['dataset_5M']['XAUUSD_i']['high'].pct_change(-ind_params.elements['Divergence' + '_num_exteremes_max'])[extreme_max.index] * 100) / ind_params.elements['Divergence' + '_num_exteremes_max']
		
		# print(ind_params.elements['Divergence' + '_num_exteremes_min'])
		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print(pct_change_low_inverse, pct_change_low)

		# for elm in pct_change_high.values:
		# 	if elm == 0:
		# 		print('Zeroooooooooooo')
		# print('mean = ', pct_change_low.mean())
		# print('min = ', pct_change_low.min())
		
		# for elm in pct_change_low.index:
		# 	# print(elm)
		# 	if pct_change_low[elm] < pct_change_low.mean():
		# 		plt.axhline(extreme_min['min'][elm], c = 'r')

		output_min['num_extreme_min'][turn_counter] = ind_params.elements['Divergence' + '_num_exteremes_min']
		output_max['num_extreme_max'][turn_counter] = ind_params.elements['Divergence' + '_num_exteremes_max']

		output_min['number_min_finded'][turn_counter] = len(extreme_min.index)
		output_max['number_max_finded'][turn_counter] = len(extreme_max.index)

		output_min['score_min'][turn_counter] = (pct_change_low.dropna().mean() * pct_change_low_inverse.dropna().mean()) ** (1/2)
		output_max['score_max'][turn_counter] = (pct_change_high.dropna().mean() * pct_change_high_inverse.dropna().mean()) ** (1/2)

		# print((pct_change_high.dropna().mean() / pct_change_high.dropna().var()) ** (1/2))
		print('turn = ', turn_counter, ' score_min = ', output_min['score_min'].max(), ' score_max = ', output_max['score_max'].max())

	return output_min.drop(columns = 0), output_max.drop(columns = 0)

	# plt.show()
	# sys.exit()

# out_extreme_optimizer_min, out_extreme_optimizer_max = extereme_optimizer(turn = 10000)

# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# # 	print('min = ',out_extreme_optimizer)

# print()
# print('min =========================> ')
# min_output = out_extreme_optimizer_min.dropna().sort_values(by = ['score_min'], ascending = True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(min_output[len(min_output) - 5:])

# print()
# print('max =========================> ')
# max_output = out_extreme_optimizer_max.dropna().sort_values(by = ['score_max'], ascending = True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# 	print(max_output[len(max_output) - 5:])

# sys.exit()

print('Start ...')

parameters.elements['MACD' + '_apply_to'] = 'OHLC/4'
parameters.elements['MACD' + '_fast'] = 129
parameters.elements['MACD' + '_slow'] = 502
parameters.elements['MACD' + '_signal'] = 23

ind_params.elements['Divergence' + '_diff_extereme'] = 6
ind_params.elements['Divergence' + '_num_exteremes_min'] = 2#10
ind_params.elements['Divergence' + '_num_exteremes_max'] = 43#245

dive_column = 'macdh'

plt.plot(parameters.elements['dataset_5M']['XAUUSD_i'].close, c = 'r')

dataset_5M_ = parameters.elements['dataset_5M']['XAUUSD_i'].copy(deep = True)

parameters.elements['dataset_5M']['XAUUSD_i']['index'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('time').resample('15T').last().dropna()
parameters.elements['dataset_5M']['XAUUSD_i']['time'] = parameters.elements['dataset_5M']['XAUUSD_i'].index
parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].set_index('index')
# parameters.elements['dataset_5M']['XAUUSD_i'] = parameters.elements['dataset_5M']['XAUUSD_i'].drop(columns = ['XAUUSD_i']).reset_index(inplace = False)
#parameters.elements['dataset_5M']['XAUUSD_i'].index.name = 'DatetimeIndex'

from pr_Parameters import Parameters as pr_Parameters
from pr_Config import Config as pr_Config

flaglearn = False

pr_parameters = pr_Parameters()
pr_config = pr_Config()

# Buy Primary:
# pr_parameters.elements['st_percent_min'] = 0.05
# pr_parameters.elements['st_percent_max'] = 0.07

# pr_parameters.elements['tp_percent_min'] = 0.12
# pr_parameters.elements['tp_percent_max'] = 0.14
#/////////////////////

# Sell Primary:
pr_parameters.elements['st_percent_min'] = 1
pr_parameters.elements['st_percent_max'] = 1

pr_parameters.elements['tp_percent_min'] = 1
pr_parameters.elements['tp_percent_max'] = 1
#////////////////////

plt.plot(parameters.elements['dataset_5M']['XAUUSD_i'].close)


macd = MACD(parameters = parameters, config = config)
macd_calc = macd.calculator_macd()

# plt.plot(macd_calc['macd'])
# plt.show()

# parameters.elements['dataset_5M']['XAUUSD_i'] = dataset_5M_.copy(deep = True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
print(parameters.elements['dataset_5M']['XAUUSD_i'])

macd = Divergence(parameters = ind_params, config = ind_config)
signal, signaltype, indicator = macd.divergence(
												sigtype = 'sell',
												sigpriority = 'primary',
												indicator = macd_calc,
												column_div = dive_column,
												ind_name = 'macd',
												dataset_5M = parameters.elements['dataset_5M'],
												dataset_1H = parameters.elements['dataset_1H'],
												symbol = 'XAUUSD_i',
												flaglearn = flaglearn,
												flagtest = True
												)


#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
plt.plot(signal['index_back'].values, signal['low_back'].values, marker="o", markersize=5, markeredgecolor="g", markerfacecolor="green")
plt.plot(signal['index'].values, signal['low_front'].values, marker="o", markersize=5, markeredgecolor="g", markerfacecolor="green")
# plt.show()
# print(signal.columns)

ind_params.elements['dataset_5M'] = {}
ind_params.elements['dataset_5M']['XAUUSD_i'] = dataset_5M_
ind_params.elements['dataset_1H'] = parameters.elements['dataset_1H']

# print(ind_params.elements['dataset_5M'])

macd_tester = Tester(parameters = ind_params, config = ind_config)

signal_out, score_out = macd_tester.RunGL(
											signal = signal, 
											sigtype = signaltype, 
											flaglearn = flaglearn, 
											flagtest = True,
											pr_parameters = pr_parameters,
											pr_config = pr_Config(),
											indicator = indicator,
											flag_savepic = False
											)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(signal_out)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(score_out)

frequency = 2000  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

plt.show()

