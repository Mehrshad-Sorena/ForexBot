import pandas as pd
import pandas_ta as ind
from log_get_data import *
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import time
from F_I_RESIST_PROTECT import protect_resist
from sklearn.cluster import KMeans
import math
from scipy import stats
from fitter import Fitter, get_common_distributions, get_distributions
import fitter
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from scipy.optimize import fsolve
#For Genetic:
from random import seed
from random import randint
import csv
import os
from tqdm import tqdm
import logging
from datetime import datetime
#from logger import print
from timer import stTime
from sma import last_signal_sma
import sys
#from numba import jit, cuda, njit
import warnings
warnings.filterwarnings("ignore")


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ind.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ind.cci)

#***************** Functions List:

#golden_cross_zero()
#tester_golden_cross_zero()
#one_year_golden_cross_tester()
#genetic_algo_cci_golden_cross()
#read_ga_result()
#Find_Best_intervals()
#initilize_values_genetic()
#gen_creator()
#last_signal()

#**************************************** Logger *****************
"""
now = datetime.now()
log_path = 'log/cci/golden_cross_zero/-----.log',now.year, now.month, now.day, now.hour, now.minute, now.second)
log_level = 'info'
logger = logging.getLogger()

if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

if log_level == 'info':
    logger.setLevel(logging.INFO)
elif log_level == 'warning':
    logger.setLevel(logging.WARNING)
elif log_level == 'debug':
    logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
formatter = logging.Formatter('%(asctime)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def print(message):
    logger.info(message)
"""
#/////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************** Data Splitter

def dataset_spliter(
					symbol,
					dataset_5M,
					dataset_1H,
					spliter_5M_end,
					spliter_5M_first
					):
	symbol_data_5M = pd.DataFrame()
	symbol_data_1H = pd.DataFrame()

	symbol_data_5M = {
						symbol: dataset_5M[symbol].copy()
						}

	symbol_data_5M[symbol]['low'] = dataset_5M[symbol]['low'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['high'] = dataset_5M[symbol]['high'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['close'] = dataset_5M[symbol]['close'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['open'] = dataset_5M[symbol]['open'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HL/2'] = dataset_5M[symbol]['HL/2'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HLC/3'] = dataset_5M[symbol]['HLC/3'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['HLCC/4'] = dataset_5M[symbol]['HLCC/4'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['OHLC/4'] = dataset_5M[symbol]['OHLC/4'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['volume'] = dataset_5M[symbol]['volume'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)
	symbol_data_5M[symbol]['time'] = dataset_5M[symbol]['time'][spliter_5M_first:spliter_5M_end].reset_index(drop=True)

	loc_1H = 0
	location_1H = -1
	for ti in dataset_1H[symbol]['time']:
		#print('1H===> ',ti.year)
		if (
			ti.year == symbol_data_5M[symbol]['time'].iloc[-1].year and
			ti.month == symbol_data_5M[symbol]['time'].iloc[-1].month and
			ti.day == symbol_data_5M[symbol]['time'].iloc[-1].day and
			ti.hour == symbol_data_5M[symbol]['time'].iloc[-1].hour
			):
			location_1H = loc_1H

		loc_1H += 1

	symbol_data_1H = {
						symbol: dataset_1H[symbol].copy()
						}

	symbol_data_1H[symbol]['low'] = dataset_1H[symbol]['low'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['high'] = dataset_1H[symbol]['high'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['close'] = dataset_1H[symbol]['close'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['open'] = dataset_1H[symbol]['open'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HL/2'] = dataset_1H[symbol]['HL/2'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HLC/3'] = dataset_1H[symbol]['HLC/3'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['HLCC/4'] = dataset_1H[symbol]['HLCC/4'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['OHLC/4'] = dataset_1H[symbol]['OHLC/4'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['volume'] = dataset_1H[symbol]['volume'][0:location_1H].reset_index(drop=True)
	symbol_data_1H[symbol]['time'] = dataset_1H[symbol]['time'][0:location_1H].reset_index(drop=True)

	return symbol_data_5M, symbol_data_1H

#/////////////////////////////////////////
#**************************************************** High Low Toucehd *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ramp Lines Toucehd *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Divergence *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Golden Cross Zero *******************************************************
@stTime
def golden_cross_zero(
						dataset,
						dataset_15M,
						dataset_1H,
						dataset_4H,
						symbol,
						Low_Period=25,
						High_Period=50,
						distance_lines=2,
						cross_line=0,
						mode='online',
						name_stp_minmax=True,
						name_stp_pr=False,
						plot=False,
						pbar_flag=False,
						buy_flag=True,
						sell_flag=True,
						st_percent_minmax_buy = 0.1,
						st_percent_minmax_sell = 0.1,
						tp_percent_minmax_sell_min = 0.04,
						tp_percent_minmax_sell_max = 0.5,
						tp_percent_minmax_buy_min = 0.04,
						tp_percent_minmax_buy_max = 0.5
						):

	x = np.arange(0,len(dataset[symbol]['HLC/3']),1)

	High_Period = int(High_Period)
	Low_Period = int(Low_Period)

	CCI_Low = ind.cci(high=dataset[symbol]['high'], low=dataset[symbol]['low'], close=dataset[symbol]['close'], length = Low_Period)
	CCI_High = ind.cci(high=dataset[symbol]['high'], low=dataset[symbol]['low'], close=dataset[symbol]['close'], length = High_Period)

	zero_line = pd.DataFrame(np.zeros(len(x)) + cross_line)

	#****************** Finding Low Period Cross With Zero Line ************************
	first_line = LineString(np.column_stack((x[(High_Period-1):], CCI_Low[(High_Period-1):])))
	second_line = LineString(np.column_stack((x[(High_Period-1):], zero_line[(High_Period-1):])))

	intersection_low = first_line.intersection(second_line)

	cross_find_flag_low = False

	if intersection_low.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection_low).xy)
		cross_index = cross.index.to_numpy()
		cross_low = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_low['index'] = cross.values.astype(int)
		cross_low['values'] = cross_index

		cross_find_flag_low = True

		if (plot == True):
			plt.plot(cross_low['index'],cross_low['values'], 'o',c='g')
    
	elif intersection_low.geom_type == 'Point':
		cross = pd.DataFrame(*intersection_low.xy)
		cross_index = cross.index.to_numpy()
		cross_low = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_low['index'] = cross.values.astype(int)
		cross_low['values'] = cross_index

		cross_find_flag_low = True

		if (plot == True):
			plt.plot(cross_low['index'],cross_low['values'], 'o',c='g')

	#///////////////////////////////////////////////////////////////////////////////////

	#****************** Finding High Period Cross With Zero Line ************************
	first_line = LineString(np.column_stack((x[(High_Period-1):], CCI_High.dropna())))
	second_line = LineString(np.column_stack((x[(High_Period-1):], zero_line[(High_Period-1):])))

	intersection_high = first_line.intersection(second_line)

	cross_find_flag_high = False

	if intersection_high.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection_high).xy)
		cross_index = cross.index.to_numpy()
		cross_high = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_high['index'] = cross.values.astype(int)
		cross_high['values'] = cross_index

		cross_find_flag_high = True

		if (plot == True):
			plt.plot(cross_high['index'],cross_high['values'], 'o',c='b')
    
	elif intersection_high.geom_type == 'Point':
		cross = pd.DataFrame(*intersection_high.xy)
		cross_index = cross.index.to_numpy()
		cross_high = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_high['index'] = cross.values.astype(int)
		cross_high['values'] = cross_index

		cross_find_flag_high = True

		if (plot == True):
			plt.plot(cross_high['index'],cross_high['values'], 'o',c='b')

	#///////////////////////////////////////////////////////////////////////////////////

	#print('high = ',cross_high)
	#print('low = ',cross_low)

	if (
		not cross_find_flag_low or
		not cross_find_flag_high
		):
		signal_buy = pd.DataFrame()
		signal_buy['signal'] = 'no_flag'
		signal_buy['index'] = -1
		signal_buy['ramp_low'] = -1
		signal_buy['ramp_high'] = -1
		signal_buy['diff_min_max_cci'] = -1
		signal_buy['diff_min_max_candle'] = -1
		signal_buy['value_max_cci'] = -1
		signal_buy['value_min_cci'] = -1
		signal_buy['value_min_max_candle'] = -1

		signal_sell = pd.DataFrame()
		signal_sell['signal'] = 'no_flag'
		signal_sell['index'] = -1
		signal_sell['ramp_low'] = -1
		signal_sell['ramp_high'] = -1
		signal_sell['diff_min_max_cci'] = -1
		signal_sell['diff_min_max_candle'] = -1
		signal_sell['value_max_cci'] = -1
		signal_sell['value_min_cci'] = -1
		signal_sell['value_min_max_candle'] = -1

		return signal_buy, signal_sell

	i = 0
	finding_points = pd.DataFrame(np.zeros(len(CCI_Low)))
	finding_points['index'] = np.nan

	for elm in cross_high.index:
		points = cross_low['index'][np.where(((cross_high['index'][elm] - cross_low['index']) <= distance_lines) &
		 ((cross_high['index'][elm] - cross_low['index']) >= 0))[0]]
		for mle in points:
			finding_points['index'][i] = mle
			i += 1

	finding_points = finding_points.dropna(inplace = False)
	finding_points = finding_points.drop(columns = 0)
	finding_points = finding_points.sort_values(by = ['index'])
	finding_points = finding_points.drop_duplicates(keep = 'last', inplace = False)
	finding_points = finding_points.reset_index(drop=True)

	if ((mode == 'optimize') | (mode == 'online')):
		signal_buy = pd.DataFrame(np.zeros(len(finding_points)))
		signal_buy['signal'] = np.nan
		signal_buy['index'] = np.nan
		signal_buy['ramp_low'] = np.nan
		signal_buy['ramp_high'] = np.nan
		signal_buy['diff_min_max_cci'] = np.nan
		signal_buy['diff_min_max_candle'] = np.nan
		signal_buy['value_max_cci'] = np.nan
		signal_buy['value_min_cci'] = np.nan
		signal_buy['value_min_max_candle'] = np.nan
		signal_buy['st_point'] = np.nan
		signal_buy['st_percent'] = np.nan
		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_buy['tp_min_max_index'] = np.nan
				signal_buy['tp_min_max'] = np.nan
				signal_buy['st_min_max_index'] = np.nan
				signal_buy['st_min_max'] = np.nan
				signal_buy['flag_min_max'] = np.nan
			if (name_stp_pr == True):
				signal_buy['tp_pr_index'] = np.nan
				signal_buy['tp_pr'] = np.nan
				signal_buy['st_pr_index'] = np.nan
				signal_buy['st_pr'] = np.nan
				signal_buy['flag_pr'] = np.nan
				signal_buy['diff_pr_top'] = np.nan
				signal_buy['diff_pr_down'] = np.nan
				#signal_buy['trend_long'] = np.nan
				#signal_buy['trend_mid'] = np.nan
				#signal_buy['trend_short1'] = np.nan
				#signal_buy['trend_short2'] = np.nan
				signal_buy['tp_line'] = np.nan
				signal_buy['st_line'] = np.nan
				signal_buy['power_pr_high'] = np.nan
				signal_buy['power_pr_low'] = np.nan
				#signal_buy['time'] = np.nan

		signal_sell = pd.DataFrame(np.zeros(len(finding_points)))
		signal_sell['signal'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['ramp_low'] = np.nan
		signal_sell['ramp_high'] = np.nan
		signal_sell['diff_min_max_cci'] = np.nan
		signal_sell['diff_min_max_candle'] = np.nan
		signal_sell['value_max_cci'] = np.nan
		signal_sell['value_min_cci'] = np.nan
		signal_sell['value_min_max_candle'] = np.nan
		signal_sell['st_point'] = np.nan
		signal_sell['st_percent'] = np.nan

		if (mode == 'optimize'):
			if (name_stp_minmax == True):
				signal_sell['tp_min_max_index'] = np.nan
				signal_sell['tp_min_max'] = np.nan
				signal_sell['st_min_max_index'] = np.nan
				signal_sell['st_min_max'] = np.nan
				signal_sell['flag_min_max'] = np.nan

			if (name_stp_pr == True):
				signal_sell['tp_pr_index'] = np.nan
				signal_sell['tp_pr'] = np.nan
				signal_sell['st_pr_index'] = np.nan
				signal_sell['st_pr'] = np.nan
				signal_sell['flag_pr'] = np.nan
				signal_sell['diff_pr_top'] = np.nan
				signal_sell['diff_pr_down'] = np.nan
				#signal_sell['trend_long'] = np.nan
				#signal_sell['trend_mid'] = np.nan
				#signal_sell['trend_short1'] = np.nan
				#signal_sell['trend_short2'] = np.nan
				signal_sell['power_pr_high'] = np.nan
				signal_sell['power_pr_low'] = np.nan

	buy_counter = 0
	sell_counter = 0

	if pbar_flag == True:
		pbar = tqdm(total=len(finding_points['index']))
		print(len(finding_points['index']))

	#for elm in finding_points['index']:
		#print('time = ',dataset[symbol]['time'][elm]))

	#for elm in finding_points.index:
		#print('time = > ',finding_points['index'][elm]))
	print('finding signals = ',len(finding_points['index']))
	mehrshad = 0
	for elm in finding_points.index:

		if pbar_flag == True:
			pbar.update(elm)

		if (plot == True):
			plt.axvline(x=finding_points['index'][elm],c='r')
			print(finding_points['index'][elm])

		if (elm-2 < 0): continue

		#******************** Buy Signal Finding *********************************
		if buy_flag:
			if ((CCI_Low[finding_points['index'][elm]] > CCI_Low[finding_points['index'][elm]-1]) &
				(CCI_High[finding_points['index'][elm]] > CCI_High[finding_points['index'][elm]-1])):

				signal_buy['signal'][buy_counter] = 'buy'
				signal_buy['index'][buy_counter] = finding_points['index'][elm]
				signal_buy['ramp_low'][buy_counter] = (CCI_Low[int(finding_points['index'][elm])] - np.min(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))/(int(finding_points['index'][elm]) - np.argmin(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))#CCI_Low[finding_points['index'][elm]-1]
				signal_buy['ramp_high'][buy_counter] = (CCI_High[int(finding_points['index'][elm])] - np.min(CCI_High[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))/(int(finding_points['index'][elm]) - np.argmin(CCI_High[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))#CCI_High[finding_points['index'][elm]-1]
				signal_buy['diff_min_max_cci'][buy_counter] = ((np.max(CCI_Low[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])]) - CCI_Low[int(finding_points['index'][elm])])/abs(CCI_Low[int(finding_points['index'][elm])]))*100
				signal_buy['diff_min_max_candle'][buy_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])])*100

				signal_buy['value_min_cci'][buy_counter] = np.min(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])])
				signal_buy['value_max_cci'][buy_counter] = np.max(CCI_Low[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])

				signal_buy['value_min_max_candle'][buy_counter] = np.max(dataset[symbol]['high'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
				signal_buy['st_point'][buy_counter] = np.min(dataset[symbol]['low'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
				signal_buy['st_percent'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - signal_buy['st_point'][buy_counter])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

				if signal_buy['st_percent'][buy_counter] <= st_percent_minmax_buy:
					signal_buy['st_percent'][buy_counter] = st_percent_minmax_buy
					signal_buy['st_point'][buy_counter] = dataset[symbol]['low'][int(finding_points['index'][elm])] * (1-(st_percent_minmax_buy/100))
				
				if signal_buy['diff_min_max_candle'][buy_counter] <= tp_percent_minmax_buy_min:
					signal_buy['diff_min_max_candle'][buy_counter] = tp_percent_minmax_buy_min
					signal_buy['value_min_max_candle'][buy_counter] = signal_buy['value_min_max_candle'][buy_counter]*(1+(tp_percent_minmax_buy_min/100))

				if signal_buy['diff_min_max_candle'][buy_counter] > tp_percent_minmax_buy_max:
					signal_buy['diff_min_max_candle'][buy_counter] = tp_percent_minmax_buy_max
					signal_buy['value_min_max_candle'][buy_counter] = signal_buy['value_min_max_candle'][buy_counter]*(1-((signal_buy['diff_min_max_candle'][buy_counter] - tp_percent_minmax_buy_max)/100))
				
				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:
						dataset_5M_minmax = pd.DataFrame()
						dataset_15M_minmax = pd.DataFrame()

						cut_first = 0
						if (int(finding_points['index'][elm]) > 300):
							cut_first = int(finding_points['index'][elm]) - 300

						dataset_5M_minmax['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HL/2'] = dataset[symbol]['HL/2'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HLC/3'] = dataset[symbol]['HLC/3'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HLCC/4'] = dataset[symbol]['HLCC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['OHLC/4'] = dataset[symbol]['OHLC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

						dataset_15M_minmax['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HL/2'] = dataset_15M[symbol]['HL/2'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HLC/3'] = dataset_15M[symbol]['HLC/3'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HLCC/4'] = dataset_15M[symbol]['HLCC/4'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['OHLC/4'] = dataset_15M[symbol]['OHLC/4'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)

						try:
							trend_sma_5M = last_signal_sma(dataset_5M_minmax, symbol, time_frame = '5M')['signal'][0]
							trend_sma_15M = last_signal_sma(dataset_15M_minmax, symbol, time_frame = '15M')['signal'][0]
						except Exception as ex:
							print('sma trend buy: ',ex)
							trend_sma_5M = 'no_flag'
							trend_sma_15M = 'no_flag'

						if (
							signal_buy['value_min_max_candle'][buy_counter] > dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004 and
							signal_buy['diff_min_max_candle'][buy_counter] >= (signal_buy['st_percent'][buy_counter] + 0.0) and
							dataset[symbol]['low'][int(finding_points['index'][elm])] > signal_buy['st_point'][buy_counter] and
							trend_sma_5M == 'buy' and
							True#trend_sma_15M == 'buy'
							):
							if ((len(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]-dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004)/dataset[symbol]['high'][int(finding_points['index'][elm])]).values*100) >= (signal_buy['diff_min_max_candle'][buy_counter]+0.04))[0]) - 1) > 1):
								signal_buy['tp_min_max_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]-dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004)/dataset[symbol]['high'][int(finding_points['index'][elm])]).values*100) >= (signal_buy['diff_min_max_candle'][buy_counter]+0.04))[0])
								signal_buy['tp_min_max'][buy_counter] = ((dataset[symbol]['high'][signal_buy['tp_min_max_index'][buy_counter]] - dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004)/(dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004)) * 100
							else:
								signal_buy['tp_min_max_index'][buy_counter] = -1
								signal_buy['tp_min_max'][buy_counter] = 0

							if ((len(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (signal_buy['st_point'][buy_counter] * 0.9994)))[0])-1) > 1):
								signal_buy['st_min_max_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (signal_buy['st_point'][buy_counter] * 0.9994)))[0])
								signal_buy['st_min_max'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][signal_buy['st_min_max_index'][buy_counter]])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
							else:
								signal_buy['st_min_max_index'][buy_counter] = -1
								signal_buy['st_min_max'][buy_counter] = 0

							if (signal_buy['st_min_max_index'][buy_counter] < signal_buy['tp_min_max_index'][buy_counter])&(signal_buy['st_min_max_index'][buy_counter] != -1):
								signal_buy['flag_min_max'][buy_counter] = 'st'
								signal_buy['tp_min_max'][buy_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_buy['st_min_max_index'][buy_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							else:
						
								if (signal_buy['tp_min_max_index'][buy_counter] != -1):
									signal_buy['flag_min_max'][buy_counter] = 'tp'
									signal_buy['st_min_max'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_buy['tp_min_max_index'][buy_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

								if (signal_buy['tp_min_max_index'][buy_counter] == -1) & (signal_buy['st_min_max_index'][buy_counter] != -1):
									signal_buy['flag_min_max'][buy_counter] = 'st'
									signal_buy['tp_min_max'][buy_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_buy['st_min_max_index'][buy_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
						else:
							signal_buy['flag_min_max'][buy_counter] = 'no_flag'
							signal_buy['tp_min_max'][buy_counter] = 0
							signal_buy['st_min_max'][buy_counter] = 0
							signal_buy['tp_min_max_index'][buy_counter] = -1
							signal_buy['st_min_max_index'][buy_counter] = -1

						if np.isnan(signal_buy['tp_min_max'][buy_counter]): 
							signal_buy['tp_min_max'][buy_counter] = 0
							signal_buy['flag_min_max'][buy_counter] = 'no_flag'
						if np.isnan(signal_buy['st_min_max'][buy_counter]): signal_buy['st_min_max'][buy_counter] = 0
						if np.isnan(signal_buy['tp_min_max_index'][buy_counter]): signal_buy['tp_min_max_index'][buy_counter] = -1
						if np.isnan(signal_buy['st_min_max_index'][buy_counter]): signal_buy['st_min_max_index'][buy_counter] = -1
						#///////////////////////////////////////////////////
					if (name_stp_pr == True):

						if (int(finding_points['index'][elm]) < 1000): continue

						#Calculate ST and TP With Protect Resist Function
						dataset_pr_5M = pd.DataFrame()
						dataset_pr_1H = pd.DataFrame()

						cut_first = 0
						if (int(finding_points['index'][elm]) > 1000):
							cut_first = int(finding_points['index'][elm]) - 1000

						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

						loc_1H = 0
						location_1H = -1
						for ti in dataset_1H[symbol]['time']:
							#print('1H===> ',ti.year)
							if (
								ti.year == dataset[symbol]['time'][int(finding_points['index'][elm])].year and
								ti.month == dataset[symbol]['time'][int(finding_points['index'][elm])].month and
								ti.day == dataset[symbol]['time'][int(finding_points['index'][elm])].day and
								ti.hour == dataset[symbol]['time'][int(finding_points['index'][elm])].hour
								):
								location_1H = loc_1H

							loc_1H += 1

						if location_1H < 500: continue
						
						#print('location_1H buy =====> ',location_1H)
						#print('5M buy =====> ',dataset[symbol]['time'][int(finding_points['index'][elm])])
						#print('1H buy =====> ',dataset_1H[symbol]['time'][location_1H])

						

						cut_first_1H = 0
						if location_1H >= 500:
							cut_first_1H = location_1H - 500

						dataset_pr_1H['low'] = dataset_1H[symbol]['low'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['high'] = dataset_1H[symbol]['high'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['close'] = dataset_1H[symbol]['close'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['open'] = dataset_1H[symbol]['open'][cut_first_1H:location_1H].reset_index(drop=True)


						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(
													T_5M=True,
													T_15M=False,
													T_1H=True,
													T_4H=False,
													T_1D=False,
													dataset_5M=dataset_pr_5M,
													dataset_15M=dataset_pr_1H,
													dataset_1H=dataset_pr_1H,
													dataset_4H=dataset_pr_1H,
													dataset_1D=dataset_pr_1H,
													plot=False
													)
						except Exception as ex:
							#print('pr buy: ',ex)
							res_pro['high'] = 'nan'
							res_pro['low'] = 'nan'

						if (res_pro.empty == False):

							signal_buy['diff_pr_top'][buy_counter] = (((res_pro['high'][0]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							signal_buy['diff_pr_down'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - (res_pro['low'][2]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

							signal_buy['power_pr_high'][buy_counter] = res_pro['power_high'][0]
							signal_buy['power_pr_low'][buy_counter] = res_pro['power_low'][2]
							
							
							if signal_buy['diff_pr_top'][buy_counter] > tp_percent_minmax_buy_max:
								signal_buy['diff_pr_top'][buy_counter] = tp_percent_minmax_buy_max
								res_pro['high'][0] = dataset[symbol]['high'][int(finding_points['index'][elm])]*(1+(tp_percent_minmax_buy_max/100))
							
							#if signal_buy['diff_pr_down'][buy_counter] >= st_percent_minmax_buy:
								#signal_buy['diff_pr_down'][buy_counter] = st_percent_minmax_buy
								#res_pro['low'][2] = dataset[symbol]['low'][int(finding_points['index'][elm])] * (1-(st_percent_minmax_buy/100))
							

							"""
							signal_buy['trend_long'][buy_counter] = res_pro['trend_long'][0].values[0]
							signal_buy['trend_mid'][buy_counter] = res_pro['trend_mid'][0].values[0]
							signal_buy['trend_short1'][buy_counter] = res_pro['trend_short1'][0].values[0]
							signal_buy['trend_short2'][buy_counter] = res_pro['trend_short2'][0].values[0]

							if signal_buy['trend_long'][buy_counter] is np.nan: signal_buy['trend_long'][buy_counter] = 'parcham'
							if signal_buy['trend_mid'][buy_counter] is np.nan: signal_buy['trend_mid'][buy_counter] = 'parcham'
							if signal_buy['trend_short1'][buy_counter] is np.nan: signal_buy['trend_short1'][buy_counter] = 'parcham'
							if signal_buy['trend_short2'][buy_counter] is np.nan: signal_buy['trend_short2'][buy_counter] = 'parcham'
							"""
							signal_buy['tp_line'][buy_counter] = res_pro['high'][0]
							signal_buy['st_line'][buy_counter] = res_pro['low'][2]


							dataset_5M_minmax = pd.DataFrame()

							cut_first = 0
							if (int(finding_points['index'][elm]) > 500):
								cut_first = int(finding_points['index'][elm]) - 500

							dataset_5M_minmax['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HL/2'] = dataset[symbol]['HL/2'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HLC/3'] = dataset[symbol]['HLC/3'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HLCC/4'] = dataset[symbol]['HLCC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['OHLC/4'] = dataset[symbol]['OHLC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

							try:
								trend_sma_5M = last_signal_sma(dataset_5M_minmax, symbol, time_frame = '5M')['signal'][0]
							except Exception as ex:
								print('sma trend buy: ',ex)
								trend_sma_5M = 'no_flag'


							#print('dataset[symbol][high] = ',dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004)
							#print('res_pro[high] = ',res_pro['high'][0])
							#print(dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004 < (res_pro['high'][0]))

							#print('dataset[symbol][low] = ',dataset[symbol]['low'][int(finding_points['index'][elm])])
							#print('res_pro[low] = ',res_pro['low'][2])
							#print(dataset[symbol]['low'][int(finding_points['index'][elm])] >= (res_pro['low'][2]))

							#print('signal_buy[diff_pr_top] = ',signal_buy['diff_pr_top'][buy_counter])
							#print('signal_buy[diff_pr_down] = ',signal_buy['diff_pr_down'][buy_counter])
							#print(signal_buy['diff_pr_top'][buy_counter] >= signal_buy['diff_pr_down'][buy_counter])

							#print('st_percent_minmax_buy = ',st_percent_minmax_buy)
							#print(signal_buy['diff_pr_down'][buy_counter] <= st_percent_minmax_buy)

							#print('trend_sma_5M = ',trend_sma_5M)

							
							if (
								dataset[symbol]['high'][int(finding_points['index'][elm])]*1.0004 < (res_pro['high'][0]) and
								dataset[symbol]['low'][int(finding_points['index'][elm])] >= (res_pro['low'][2]) and
								signal_buy['diff_pr_top'][buy_counter] >= signal_buy['diff_pr_down'][buy_counter] and
								signal_buy['diff_pr_down'][buy_counter] <= st_percent_minmax_buy and
								trend_sma_5M == 'buy'
								):
								mehrshad += 1
								if signal_buy['diff_pr_down'][buy_counter] <= st_percent_minmax_buy:#signal_buy['diff_pr_top'][buy_counter]:
									signal_buy['diff_pr_down'][buy_counter] = st_percent_minmax_buy
									res_pro['low'][2] = dataset[symbol]['low'][int(finding_points['index'][elm])] * (1-(st_percent_minmax_buy/100))
								
								if signal_buy['diff_pr_top'][buy_counter] > tp_percent_minmax_buy_max:
									signal_buy['diff_pr_top'][buy_counter] = tp_percent_minmax_buy_max
									res_pro['high'][0] = dataset[symbol]['high'][int(finding_points['index'][elm])]*(1+(tp_percent_minmax_buy_max/100))

								#signal_buy['time'][buy_counter] = dataset[symbol]['time'][int(finding_points['index'][elm])]

								if ((len(np.where(((dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values*0.9996) >= (res_pro['high'][0])))[0]) - 1) > 1):
									signal_buy['tp_pr_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where(((dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values*0.9996) >= (res_pro['high'][0])))[0])
									signal_buy['tp_pr'][buy_counter] = ((dataset[symbol]['high'][signal_buy['tp_pr_index'][buy_counter]]*0.9996 - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
								else:
									signal_buy['tp_pr_index'][buy_counter] = -1
									signal_buy['tp_pr'][buy_counter] = 0

								if ((len(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (res_pro['low'][2])))[0])-1) > 1):
									signal_buy['st_pr_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (res_pro['low'][2])))[0])
									signal_buy['st_pr'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - res_pro['low'][2])/res_pro['low'][2]) * 100
								else:
									signal_buy['st_pr_index'][buy_counter] = -1
									signal_buy['st_pr'][buy_counter] = 0

								if ((signal_buy['st_pr_index'][buy_counter] < signal_buy['tp_pr_index'][buy_counter]) & (signal_buy['st_pr_index'][buy_counter] != -1)):
									signal_buy['flag_pr'][buy_counter] = 'st'
									signal_buy['tp_pr'][buy_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_buy['st_pr_index'][buy_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
								else:
									if (signal_buy['tp_pr_index'][buy_counter] != -1):
										signal_buy['flag_pr'][buy_counter] = 'tp'
										signal_buy['st_pr'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_buy['tp_pr_index'][buy_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

									if (signal_buy['tp_pr_index'][buy_counter] == -1) & (signal_buy['st_pr_index'][buy_counter] != -1):
										signal_buy['flag_pr'][buy_counter] = 'st'
										signal_buy['tp_pr'][buy_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_buy['st_pr_index'][buy_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							else:
								signal_buy['tp_pr_index'][buy_counter] = -1
								signal_buy['tp_pr'][buy_counter] = 0
								signal_buy['st_pr_index'][buy_counter] = -1
								signal_buy['st_pr'][buy_counter] = 0
								signal_buy['flag_pr'][buy_counter] = 'no_flag'
						else:
							signal_buy['tp_pr_index'][buy_counter] = -1
							signal_buy['tp_pr'][buy_counter] = 0
							signal_buy['st_pr_index'][buy_counter] = -1
							signal_buy['st_pr'][buy_counter] = 0
							signal_buy['flag_pr'][buy_counter] = 'no_flag'

						if np.isnan(signal_buy['tp_pr'][buy_counter]): 
							signal_buy['tp_pr'][buy_counter] = 0
							signal_buy['flag_pr'][buy_counter] = 'no_my_flag'
						if np.isnan(signal_buy['st_pr'][buy_counter]): signal_buy['st_pr'][buy_counter] = 0
						if np.isnan(signal_buy['tp_pr_index'][buy_counter]): signal_buy['tp_pr_index'][buy_counter] = -1
						if np.isnan(signal_buy['st_pr_index'][buy_counter]): signal_buy['st_pr_index'][buy_counter] = -1
						#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
							#print(signal_buy)
						#///////////////////////////////////////////////////

				buy_counter += 1
		#///////////////////////////////////////////////////////////////////////

		#************************ Sell Signal Finding *****************************
		if sell_flag:
			if ((CCI_Low[finding_points['index'][elm]] < CCI_Low[finding_points['index'][elm]-1]) &
				(CCI_High[finding_points['index'][elm]] < CCI_High[finding_points['index'][elm]-1])):

				signal_sell['signal'][sell_counter] = 'sell'
				signal_sell['index'][sell_counter] = finding_points['index'][elm]
				signal_sell['ramp_low'][sell_counter] = (CCI_Low[int(finding_points['index'][elm])] - np.max(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))/(int(finding_points['index'][elm]) - np.argmax(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))#CCI_Low[finding_points['index'][elm]-1]
				signal_sell['ramp_high'][sell_counter] = (CCI_High[int(finding_points['index'][elm])] - np.max(CCI_High[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))/(int(finding_points['index'][elm]) - np.argmax(CCI_High[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])]))#CCI_High[finding_points['index'][elm]-1]
				signal_sell['diff_min_max_cci'][sell_counter] = ((CCI_Low[int(finding_points['index'][elm])] - np.min(CCI_Low[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])]))/abs(CCI_Low[int(finding_points['index'][elm])])) * 100
				signal_sell['diff_min_max_candle'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100


				signal_sell['value_min_cci'][sell_counter] = np.min(CCI_Low[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
				signal_sell['value_max_cci'][sell_counter] = np.max(CCI_Low[int(finding_points['index'][elm-1]):int(finding_points['index'][elm])])

				signal_sell['value_min_max_candle'][sell_counter] = np.min(dataset[symbol]['low'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])

				signal_sell['st_point'][sell_counter] = np.max(dataset[symbol]['high'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
				signal_sell['st_percent'][sell_counter] = ((signal_sell['st_point'][sell_counter] - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100

				if signal_sell['st_percent'][sell_counter] <= st_percent_minmax_sell:
					signal_sell['st_percent'][sell_counter] = st_percent_minmax_sell
					signal_sell['st_point'][sell_counter] = dataset[symbol]['high'][int(finding_points['index'][elm])] * (1-(st_percent_minmax_sell/100))
				
				if signal_sell['diff_min_max_candle'][sell_counter] <= tp_percent_minmax_sell_min:
					signal_sell['diff_min_max_candle'][sell_counter] = tp_percent_minmax_sell_min
					signal_sell['value_min_max_candle'][sell_counter] = signal_sell['value_min_max_candle'][sell_counter] * (1-(tp_percent_minmax_sell_min/100))

				if signal_sell['diff_min_max_candle'][sell_counter] > tp_percent_minmax_sell_max:
					signal_sell['diff_min_max_candle'][sell_counter] = tp_percent_minmax_sell_max
					signal_sell['value_min_max_candle'][sell_counter] = signal_sell['value_min_max_candle'][sell_counter] * (1+((signal_sell['diff_min_max_candle'][sell_counter] - tp_percent_minmax_sell_max)/100))
				
				#Calculate porfits
				#must read protect and resist from protect resist function
				if (mode == 'optimize'):

					if (name_stp_minmax == True):
						#Calculate With Min Max Diff From MACD:
						dataset_5M_minmax = pd.DataFrame()
						dataset_15M_minmax = pd.DataFrame()

						cut_first = 0
						if (int(finding_points['index'][elm]) > 300):
							cut_first = int(finding_points['index'][elm]) - 300

						dataset_5M_minmax['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HL/2'] = dataset[symbol]['HL/2'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HLC/3'] = dataset[symbol]['HLC/3'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['HLCC/4'] = dataset[symbol]['HLCC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_5M_minmax['OHLC/4'] = dataset[symbol]['OHLC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

						dataset_15M_minmax['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HL/2'] = dataset_15M[symbol]['HL/2'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HLC/3'] = dataset_15M[symbol]['HLC/3'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['HLCC/4'] = dataset_15M[symbol]['HLCC/4'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)
						dataset_15M_minmax['OHLC/4'] = dataset_15M[symbol]['OHLC/4'][int(cut_first/3):int(finding_points['index'][elm]/3)].reset_index(drop=True)

						try:
							trend_sma_5M = last_signal_sma(dataset_5M_minmax, symbol, time_frame = '5M')['signal'][0]
							trend_sma_15M = last_signal_sma(dataset_15M_minmax, symbol, time_frame = '15M')['signal'][0]
						except Exception as ex:
							print('sma trend buy: ',ex)
							trend_sma_5M = 'no_flag'
							trend_sma_15M = 'no_flag'

						if (
							signal_sell['value_min_max_candle'][sell_counter] < dataset[symbol]['low'][int(finding_points['index'][elm])]*0.9996 and
							signal_sell['diff_min_max_candle'][sell_counter] >= signal_sell['st_percent'][sell_counter] and
							dataset[symbol]['high'][int(finding_points['index'][elm])] < signal_sell['st_point'][sell_counter] and
							trend_sma_5M == 'sell' and
							True#trend_sma_15M == 'sell'
							):
							if ((len(np.where((((((dataset[symbol]['low'][int(finding_points['index'][elm])]*0.9996 - dataset[symbol]['low'][int(finding_points['index'][elm]):-1])/dataset[symbol]['low'][int(finding_points['index'][elm])]).values) * 100) >= (signal_sell['diff_min_max_candle'][sell_counter]+0.04)))[0]) - 1) > 1):
								signal_sell['tp_min_max_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((((dataset[symbol]['low'][int(finding_points['index'][elm])]*0.9996 - dataset[symbol]['low'][int(finding_points['index'][elm]):-1])/dataset[symbol]['low'][int(finding_points['index'][elm])]).values) * 100) >= (signal_sell['diff_min_max_candle'][sell_counter]+0.04)))[0])
								signal_sell['tp_min_max'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])]*0.9996 - dataset[symbol]['low'][signal_sell['tp_min_max_index'][sell_counter]])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
							else:
								signal_sell['tp_min_max_index'][sell_counter] = -1
								signal_sell['tp_min_max'][sell_counter] = 0

							if ((len(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (signal_sell['st_point'][sell_counter] * 1.0006)))[0])-1) > 1):
								signal_sell['st_min_max_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (signal_sell['st_point'][sell_counter] * 1.0006)))[0])
								signal_sell['st_min_max'][sell_counter] = ((dataset[symbol]['high'][signal_sell['st_min_max_index'][sell_counter]] - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							else:
								signal_sell['st_min_max_index'][sell_counter] = -1
								signal_sell['st_min_max'][sell_counter] = 0

							if ((signal_sell['st_min_max_index'][sell_counter] < signal_sell['tp_min_max_index'][sell_counter]) & (signal_sell['st_min_max_index'][sell_counter] != -1)):
								signal_sell['flag_min_max'][sell_counter] = 'st'
								signal_sell['tp_min_max'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_sell['st_min_max_index'][sell_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
							else:
						
								if (signal_sell['tp_min_max_index'][sell_counter] != -1):
									signal_sell['flag_min_max'][sell_counter] = 'tp'
									signal_sell['st_min_max'][sell_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_sell['tp_min_max_index'][sell_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100

								if (signal_sell['tp_min_max_index'][sell_counter] == -1) & (signal_sell['st_min_max_index'][sell_counter] != -1):
									signal_sell['flag_min_max'][sell_counter] = 'st'
									signal_sell['tp_min_max'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_sell['st_min_max_index'][sell_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
						else:
							signal_sell['flag_min_max'][sell_counter] = 'no_flag'
							signal_sell['tp_min_max'][sell_counter] = 0
							signal_sell['st_min_max'][sell_counter] = 0
							signal_sell['tp_min_max_index'][sell_counter] = -1
							signal_sell['st_min_max_index'][sell_counter] = -1

						if np.isnan(signal_sell['tp_min_max'][sell_counter]): 
							signal_sell['tp_min_max'][sell_counter] = 0
							signal_sell['flag_min_max'][sell_counter] = 'no_flag'
						if np.isnan(signal_sell['st_min_max'][sell_counter]): signal_sell['st_min_max'][sell_counter] = 0
						if np.isnan(signal_sell['tp_min_max_index'][sell_counter]): signal_sell['tp_min_max_index'][sell_counter] = -1
						if np.isnan(signal_sell['st_min_max_index'][sell_counter]): signal_sell['st_min_max_index'][sell_counter] = -1
						#///////////////////////////////////////////////////
					if (name_stp_pr == True):
						#Calculate ST and TP With Protect Resist Function
						if (int(finding_points['index'][elm]) < 1000): continue

						dataset_pr_5M = pd.DataFrame()
						dataset_pr_1H = pd.DataFrame()

						cut_first = 0
						if (int(finding_points['index'][elm]) > 1000):
							cut_first = int(finding_points['index'][elm]) - 1000

						dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
						dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

						loc_1H = 0
						location_1H = -1
						for ti in dataset_1H[symbol]['time']:
							#print('1H===> ',ti.year)
							if (
								ti.year == dataset[symbol]['time'][int(finding_points['index'][elm])].year and
								ti.month == dataset[symbol]['time'][int(finding_points['index'][elm])].month and
								ti.day == dataset[symbol]['time'][int(finding_points['index'][elm])].day and
								ti.hour == dataset[symbol]['time'][int(finding_points['index'][elm])].hour
								):
								location_1H = loc_1H

							loc_1H += 1

						if location_1H < 500: continue

						cut_first_1H = 0
						if location_1H >= 500:
							cut_first_1H = location_1H - 500

						dataset_pr_1H['low'] = dataset_1H[symbol]['low'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['high'] = dataset_1H[symbol]['high'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['close'] = dataset_1H[symbol]['close'][cut_first_1H:location_1H].reset_index(drop=True)
						dataset_pr_1H['open'] = dataset_1H[symbol]['open'][cut_first_1H:location_1H].reset_index(drop=True)

						#print('location_1H sell =====> ',location_1H)
						#print('5M sell =====> ',dataset[symbol]['time'][int(finding_points['index'][elm])])
						#print('1H sell =====> ',dataset_1H[symbol]['time'][location_1H])


						res_pro = pd.DataFrame()
					
						try:
							res_pro = protect_resist(
													T_5M=True,
													T_15M=False,
													T_1H=True,
													T_4H=False,
													T_1D=False,
													dataset_5M=dataset_pr_5M,
													dataset_15M=dataset_pr_1H,
													dataset_1H=dataset_pr_1H,
													dataset_4H=dataset_pr_1H,
													dataset_1D=dataset_pr_1H,
													plot=False
													)

						except Exception as ex:
							#print('pr sell: ',ex)
							res_pro['high'] = 'nan'
							res_pro['low'] = 'nan'

						if (res_pro.empty == False):

							signal_sell['diff_pr_top'][sell_counter] = (((res_pro['high'][2]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							signal_sell['diff_pr_down'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - (res_pro['low'][0]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

							signal_sell['power_pr_high'][sell_counter] = res_pro['power_high'][2]
							signal_sell['power_pr_low'][sell_counter] = res_pro['power_low'][0]


							if signal_sell['diff_pr_down'][sell_counter] > tp_percent_minmax_sell_max:
								signal_sell['diff_pr_down'][sell_counter] = tp_percent_minmax_sell_max
								res_pro['low'][0] = dataset[symbol]['low'][int(finding_points['index'][elm])] * (1-(tp_percent_minmax_sell_max/100))
							
							
							#if signal_sell['diff_pr_top'][sell_counter] >= st_percent_minmax_sell:
								#signal_sell['diff_pr_top'][sell_counter] = st_percent_minmax_sell
								#res_pro['high'][2] = dataset[symbol]['high'][int(finding_points['index'][elm])] * (1+(st_percent_minmax_sell/100))

							"""
							signal_sell['trend_long'][sell_counter] = res_pro['trend_long'][0].values[0]
							signal_sell['trend_mid'][sell_counter] = res_pro['trend_mid'][0].values[0]
							signal_sell['trend_short1'][sell_counter] = res_pro['trend_short1'][0].values[0]
							signal_sell['trend_short2'][sell_counter] = res_pro['trend_short2'][0].values[0]

							if signal_sell['trend_long'][sell_counter] is np.nan: signal_sell['trend_long'][sell_counter] = 'parcham'
							if signal_sell['trend_mid'][sell_counter] is np.nan: signal_sell['trend_mid'][sell_counter] = 'parcham'
							if signal_sell['trend_short1'][sell_counter] is np.nan: signal_sell['trend_short1'][sell_counter] = 'parcham'
							if signal_sell['trend_short2'][sell_counter] is np.nan: signal_sell['trend_short2'][sell_counter] = 'parcham'
	
							"""

							dataset_5M_minmax = pd.DataFrame()

							cut_first = 0
							if (int(finding_points['index'][elm]) > 500):
								cut_first = int(finding_points['index'][elm]) - 500

							dataset_5M_minmax['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HL/2'] = dataset[symbol]['HL/2'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HLC/3'] = dataset[symbol]['HLC/3'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['HLCC/4'] = dataset[symbol]['HLCC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
							dataset_5M_minmax['OHLC/4'] = dataset[symbol]['OHLC/4'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

							try:
								trend_sma_5M = last_signal_sma(dataset_5M_minmax, symbol, time_frame = '5M')['signal'][0]
							except Exception as ex:
								print('sma trend buy: ',ex)
								trend_sma_5M = 'no_flag'

							#print('dataset[symbol][low] = ',dataset[symbol]['low'][int(finding_points['index'][elm])] * 0.9996)
							#print('res_pro[low] = ',res_pro['low'][0])
							#print(dataset[symbol]['low'][int(finding_points['index'][elm])] * 0.9996 > (res_pro['low'][0]))

							#print('dataset[symbol][high] = ',dataset[symbol]['high'][int(finding_points['index'][elm])])
							#print('res_pro[high] = ',res_pro['high'][2])
							#print(dataset[symbol]['high'][int(finding_points['index'][elm])] < (res_pro['high'][2]))

							#print('signal_sell[diff_pr_top] = ',signal_sell['diff_pr_top'][sell_counter])
							#print('signal_sell[diff_pr_down] = ',signal_sell['diff_pr_down'][sell_counter])
							#print(signal_sell['diff_pr_top'][sell_counter] <= signal_sell['diff_pr_down'][sell_counter])

							#print('st_percent_minmax_sell = ',st_percent_minmax_sell)
							#print(signal_sell['diff_pr_top'][sell_counter] <= st_percent_minmax_sell)

							#print('trend_sma_5M = ',trend_sma_5M)

							if (
								dataset[symbol]['low'][int(finding_points['index'][elm])] * 0.9996 > (res_pro['low'][0]) and
								dataset[symbol]['high'][int(finding_points['index'][elm])] < (res_pro['high'][2]) and
								signal_sell['diff_pr_down'][sell_counter] >= signal_sell['diff_pr_top'][sell_counter] and
								signal_sell['diff_pr_top'][sell_counter] <= st_percent_minmax_sell and
								trend_sma_5M == 'sell'
								):

								if signal_sell['diff_pr_top'][sell_counter] <= signal_sell['diff_pr_down'][sell_counter]:
									signal_sell['diff_pr_top'][sell_counter] = st_percent_minmax_sell
									res_pro['high'][2] = dataset[symbol]['high'][int(finding_points['index'][elm])] * (1+(st_percent_minmax_sell/100))


								if ((len(np.where(((dataset[symbol]['low'][int(finding_points['index'][elm]):-1].values*1.0004) <= (res_pro['low'][0])))[0]) - 1) > 1):
									signal_sell['tp_pr_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where(((dataset[symbol]['low'][int(finding_points['index'][elm]):-1].values*1.0004) <= (res_pro['low'][0])))[0])
									signal_sell['tp_pr'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][signal_sell['tp_pr_index'][sell_counter]]*1.0004)/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
								else:
									signal_sell['tp_pr_index'][sell_counter] = -1
									signal_sell['tp_pr'][sell_counter] = 0

								if ((len(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) * 1.0004 >= (res_pro['high'][2])))[0])-1) > 1):
									signal_sell['st_pr_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values)*1.0004 >= (res_pro['high'][2])))[0])
									signal_sell['st_pr'][sell_counter] = ((res_pro['high'][2] - dataset[symbol]['high'][int(finding_points['index'][elm])])/res_pro['high'][2]) * 100
								else:
									signal_sell['st_pr_index'][sell_counter] = -1
									signal_sell['st_pr'][sell_counter] = 0

								if (signal_sell['st_pr_index'][sell_counter] < signal_sell['tp_pr_index'][sell_counter])&(signal_sell['st_pr_index'][sell_counter] != -1):
									signal_sell['flag_pr'][sell_counter] = 'st'
									signal_sell['tp_pr'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_sell['st_pr_index'][sell_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
								else:
							
									if (signal_sell['tp_pr_index'][sell_counter] != -1):
										signal_sell['flag_pr'][sell_counter] = 'tp'
										signal_sell['st_pr'][sell_counter] = ((np.max(dataset[symbol]['high'][int(finding_points['index'][elm]):int(signal_sell['tp_pr_index'][sell_counter])]) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
							
									if (signal_sell['tp_pr_index'][sell_counter] == -1) & (signal_sell['st_pr_index'][sell_counter] != -1):
										signal_sell['flag_pr'][sell_counter] = 'st'
										signal_sell['tp_pr'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - np.min(dataset[symbol]['low'][int(finding_points['index'][elm]):int(signal_sell['st_pr_index'][sell_counter])]))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
							else:
								signal_sell['tp_pr_index'][sell_counter] = -1
								signal_sell['tp_pr'][sell_counter] = 0
								signal_sell['st_pr_index'][sell_counter] = -1
								signal_sell['st_pr'][sell_counter] = 0
								signal_sell['flag_pr'][sell_counter] = 'no_flag'
						else:
							signal_sell['tp_pr_index'][sell_counter] = -1
							signal_sell['tp_pr'][sell_counter] = 0
							signal_sell['st_pr_index'][sell_counter] = -1
							signal_sell['st_pr'][sell_counter] = 0
							signal_sell['flag_pr'][sell_counter] = 'no_flag'

						if np.isnan(signal_sell['tp_pr'][sell_counter]): 
							signal_sell['tp_pr'][sell_counter] = 0
							signal_sell['flag_pr'][sell_counter] = 'no_flag'
						if np.isnan(signal_sell['st_pr'][sell_counter]): signal_sell['st_pr'][sell_counter] = 0
						if np.isnan(signal_sell['tp_pr_index'][sell_counter]): signal_sell['tp_pr_index'][sell_counter] = -1
						if np.isnan(signal_sell['st_pr_index'][sell_counter]): signal_sell['st_pr_index'][sell_counter] = -1
						#///////////////////////////////////////////////////
					#print('tp = ',signal_sell['tp_pr'][sell_counter])
					#print('tp index = ',signal_sell['tp_pr_index'][sell_counter])
					#print('st = ',signal_sell['st_pr'][sell_counter])
					#print('st index = ',signal_sell['st_pr_index'][sell_counter])
					#print('flag_pr = ',signal_sell['flag_pr'][sell_counter])

				sell_counter += 1

		#////////////////////////////////////////////////////////////////////////////
	
	#print('last index sell = ',signal_sell)
	print('mehrshad = ',mehrshad)
	signal_buy = signal_buy.drop(columns=0)
	signal_buy = signal_buy.dropna()
	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_buy = signal_buy.reset_index(drop=True)

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		#print('last index buy = ',signal_buy)

	#for elm in signal_buy['index']:
		#print('time = > ',elm))

	#for elm in signal_buy['index']:
		#print('time ====> ',dataset[symbol]['time'][elm]))

	signal_sell = signal_sell.drop(columns=0)
	signal_sell = signal_sell.dropna()
	signal_sell = signal_sell.sort_values(by = ['index'])
	signal_sell = signal_sell.reset_index(drop=True)

	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		#print('last index sell = ',signal_sell)

	#print('last index = ',signal_buy)


	if (plot == True):
		plt.plot(CCI_Low.index, CCI_Low,c='b')
		plt.plot(CCI_High.index, CCI_High,c='r')
		plt.show()

	return signal_buy, signal_sell
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Find Best Intervals *******************************************************
#@stTime
def Find_Best_intervals(signals,apply_to, min_tp=0.1, max_st=0.1, name_stp='flag_min_max', alpha=0.1):

	if (name_stp == 'flag_min_max'):
		signal_good = signals.drop(
									np.where(
											(signals[name_stp]=='st')|
											(signals['st_min_max']>max_st)|
											(signals['tp_min_max']<min_tp)
											)[0])

		if (signal_good.empty == True): 
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval

	if (name_stp == 'flag_pr'):
		signal_good = signals.drop(
								np.where(
										(signals[name_stp]=='st')|
										(signals[name_stp]=='no_flag')
										#(signals['st_pr']>max_st)|
										#(signals['tp_pr']<min_tp)
										)[0])

			#(signals['diff_pr_down']>max_st)
		
		if (signal_good.empty == True): 
			print('no good signal 1')
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval

	signal_good = signal_good.sort_values(by = ['index'])
	signal_good = signal_good.reset_index(drop=True)

	#timeout = time.time() + 20  # timeout_break Sec from now
	try:
		if (len(signal_good[apply_to].to_numpy()) - 1) >= 25:
			n_clusters = 5
		else:
			n_clusters = int(len(signal_good[apply_to].to_numpy())/4)
			if (n_clusters <= 0):
				best_signals_interval = pd.DataFrame()
				best_signals_interval['interval'] = [0,0,0]
				best_signals_interval['power'] = [0,0,0]
				best_signals_interval['alpha'] = [alpha,alpha,alpha]
				best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
				return best_signals_interval
		
		kmeans = KMeans(n_clusters=n_clusters, random_state=0,init='k-means++',n_init=5,max_iter=5)
		#Model Fitting
		kmeans = kmeans.fit(signal_good[apply_to].to_numpy().reshape(-1,1))

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		#if ((len(Y) != len(Power))):
			#timeout = time.time() + timeout_break
			#continue
		#if ((len(Y) == len(Power))): break

		signal_final = pd.DataFrame(Y, columns=['Y'])
		signal_final['power'] = Power
		signal_final = signal_final.sort_values(by = ['Y'])

	except Exception as ex:
		print('no good signal 1')
		best_signals_interval = pd.DataFrame()
		best_signals_interval['interval'] = [0,0,0]
		best_signals_interval['power'] = [0,0,0]
		best_signals_interval['alpha'] = [alpha,alpha,alpha]
		best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
		return best_signals_interval

	

	#Fitting Model Finding ****************************
	data_X = np.zeros(np.sum(signal_final['power']))

	j = 0
	z = 0
	for elm in signal_final['Y']:
		k = 0
		while k < signal_final['power'].to_numpy()[j]:
			data_X[z] = elm
			k += 1
			z += 1
		j += 1

	data_X = np.sort(data_X)

	distributions = ['foldnorm','dweibull','expon','nakagami','norm']

	#************************************ Finding Sell's ****************************

	while True:
		
		try:
			f = Fitter(
					data = data_X,
					xmin=np.min(data_X),
					xmax=np.max(data_X), 
					bins = len(signal_final['Y'])-1, 
					distributions = distributions, 
					timeout=1, 
					density=True
					)
	
			f.fit(amp=1, progress=False, n_jobs=-1)
	
			#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
			#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
			#print(f.get_best(method = 'sumsquare_error').items())
	
			items = list(f.get_best(method = 'sumsquare_error').items())
			dist_name = items[0][0]
			dist_parameters = items[0][1]
		except Exception as ex:
			print('Find Best ERROR = ',ex)
			best_signals_interval = pd.DataFrame()
			best_signals_interval['interval'] = [0,0,0]
			best_signals_interval['power'] = [0,0,0]
			best_signals_interval['alpha'] = [alpha,alpha,alpha]
			best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]
			return best_signals_interval

		if dist_name == 'foldnorm':
			Y = f.fitted_pdf['foldnorm']
			Y = foldnorm.pdf(x=data_X, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = foldnorm.interval(alpha=alpha, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'dweibull':
			Y = f.fitted_pdf['dweibull']
			Y = dweibull.pdf(x=data_X, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = dweibull.interval(alpha=alpha, c=dist_parameters['c'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
		
		elif dist_name == 'rayleigh':
			Y = f.fitted_pdf['rayleigh']
			Y = rayleigh.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = rayleigh.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'expon':
			Y = f.fitted_pdf['expon']
			Y = expon.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = expon.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'nakagami':
			Y = f.fitted_pdf['nakagami']
			Y = nakagami.pdf(x=data_X, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = nakagami.interval(alpha=alpha, nu=dist_parameters['nu'], loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
	
		elif dist_name == 'norm':
			Y = f.fitted_pdf['norm']
			Y = norm.pdf(x=data_X, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Extereme = norm.interval(alpha=alpha, loc=dist_parameters['loc'], scale=dist_parameters['scale'])
			Upper_Line = Extereme[1]
			Lower_Line = Extereme[0]
			Mid_Line = np.array(dist_parameters['loc'])
			Power_Upper_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Lower_Line =(signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])
			Power_Mid_Line = (signal_final['power'][kmeans.predict(Mid_Line.reshape(1,-1))].to_numpy())/np.max(signal_final['power'])

		#if (time.time() > timeout):
		#	if (distributions_sell == None):
				#return 'timeout.error'
		#		pass

		if ((Mid_Line <= Upper_Line)&(Mid_Line >= Lower_Line)&(Upper_Line>Lower_Line)): 
			break
		else:
			distributions.remove(dist_name)
			if (distributions == None):
				#return 'timeout.error'
				pass

	#//////////////////////////////////////////////////////////////////////////////////////

	best_signals_interval = pd.DataFrame()
	best_signals_interval['interval'] = [Upper_Line,Mid_Line,Lower_Line]
	best_signals_interval['power'] = [Power_Upper_Line,Power_Mid_Line,Power_Lower_Line]
	best_signals_interval['alpha'] = [alpha,alpha,alpha]
	best_signals_interval[name_stp] = [name_stp,name_stp,name_stp]

	return best_signals_interval

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Tester Golden Cross Zero *******************************************************
#@stTime
def tester_golden_cross_zero(
							signal_buy,
							signal_sell,
							min_tp,
							max_st,
							alpha,
							name_stp_minmax,
							name_stp_pr,
							flag_trade
							):

	upper = 0
	mid = 1
	lower = 2

	#print('flag =====> ',flag_trade)

	#*********** Methode 1 Profits With MinMax Buy:
	if flag_trade == 'buy':
		
		output_buy = pd.DataFrame()

		if name_stp_minmax == True:

			#ramp_high_intervals_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='ramp_high',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#ramp_low_intervals_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='ramp_low',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_cci_intervals_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_cci',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_candle_intervals_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_candle',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#value_min_cci_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='value_min_cci',
				#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			#value_max_cci_minmax_buy = Find_Best_intervals(signals=signal_buy,apply_to='value_max_cci',
				#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			#power_high_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='power_pr_high',
			 	#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=0.04)

			#power_low_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='power_pr_low',
			 	#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=0.04)

			#print('==== value min 1 ==> ',value_min_cci_minmax_buy)
			#print('==== value max 1 ==> ',value_max_cci_minmax_buy)

			list_index_ok = np.where(
							#((signal_buy['ramp_high'].to_numpy()>=ramp_high_intervals_minmax_buy['interval'][lower]))&
							#((signal_buy['ramp_low'].to_numpy()>=ramp_low_intervals_minmax_buy['interval'][lower]))&
							#((signal_buy['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_minmax_buy['interval'][upper]))&
							#((signal_buy['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax_buy['interval'][upper]))&
							#(signal_buy['value_min_cci'].to_numpy()<=value_min_cci_minmax_buy['interval'][upper]) &
							#(signal_buy['power_pr_high'].to_numpy()<=power_high_pr_buy['interval'][lower]) &
							#(signal_buy['power_pr_low'].to_numpy()<=power_low_pr_buy['interval'][lower])
							#(signal_buy['value_max_cci'].to_numpy()>=value_max_cci_minmax_buy['interval'][lower])
							True)[0]

			#list_index_ok = range(0,len(signal_buy))

		
			output_buy['mean_tp_min_max'] = [np.mean(signal_buy['tp_min_max'][list_index_ok])]
			output_buy['mean_st_min_max'] = [np.mean(signal_buy['st_min_max'][list_index_ok])]
			output_buy['max_tp_min_max'] = [np.max(signal_buy['tp_min_max'][list_index_ok])]
			output_buy['max_st_min_max'] = [np.max(signal_buy['st_min_max'][list_index_ok])]
	
			try:
				output_buy['sum_st_min_max'] = [np.sum(signal_buy['st_min_max'][list_index_ok[np.where(signal_buy['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_buy['sum_tp_min_max'] = [np.sum(signal_buy['tp_min_max'][list_index_ok[np.where(signal_buy['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
			except Exception as ex:
				print('tester minmax buy: ',ex)
				output_buy['sum_st_min_max'] = 0
				output_buy['sum_tp_min_max'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_buy['flag_min_max'][list_index_ok]:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_buy['num_tp_min_max'] = [tp_counter]
			output_buy['num_st_min_max'] = [st_counter]
			output_buy['num_trade_min_max'] = [st_counter + tp_counter]
	#output_buy['ramp_low_upper_min_max'] = [ramp_low_intervals_minmax_buy['interval'][upper]]
	#output_buy['ramp_low_lower_min_max'] = [ramp_low_intervals_minmax_buy['interval'][lower]]
	#output_buy['ramp_high_upper_min_max'] = [ramp_high_intervals_minmax_buy['interval'][upper]]
	#output_buy['ramp_high_lower_min_max'] = [ramp_high_intervals_minmax_buy['interval'][lower]]
	#output_buy['diff_min_max_cci_upper_min_max'] = [diff_min_max_cci_intervals_minmax_buy['interval'][upper]]
	#output_buy['diff_min_max_cci_lower_min_max'] = [diff_min_max_cci_intervals_minmax_buy['interval'][lower]]
	#output_buy['diff_min_max_candle_upper_min_max'] = [diff_min_max_candle_intervals_minmax_buy['interval'][upper]]
	#output_buy['diff_min_max_candle_lower_min_max'] = [diff_min_max_candle_intervals_minmax_buy['interval'][lower]]
			#output_buy['value_max_lower_cci_min_max'] = [value_max_cci_minmax_buy['interval'][lower]]
			#output_buy['value_min_upper_cci_min_max'] = [value_min_cci_minmax_buy['interval'][upper]]

			#print('==== value min 2 ==> ',output_buy['value_min_upper_cci_min_max'])
			#print('==== value max 2 ==> ',output_buy['value_max_lower_cci_min_max'])

			if output_buy['num_trade_min_max'][0] != 0:
				if output_buy['num_st_min_max'][0] != 0:
					score_num_tp = (tp_counter-output_buy['num_st_min_max'][0])

					if (tp_counter-output_buy['num_st_min_max'][0]) == 0:
						score_num_tp = 8

					if (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_buy['max_st_min_max'][0] != 0:
				score_max_tp = (output_buy['max_tp_min_max'][0]-output_buy['max_st_min_max'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_buy['max_tp_min_max'][0]
				if (output_buy['max_tp_min_max'][0] != 0):
					score_max_tp = output_buy['max_tp_min_max'][0] * 10

			if (output_buy['mean_st_min_max'][0] != 0):
				score_mean_tp = (output_buy['mean_tp_min_max'][0]-output_buy['mean_st_min_max'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_buy['mean_tp_min_max'][0]
				if (output_buy['mean_tp_min_max'][0] != 0):
					score_mean_tp = output_buy['mean_tp_min_max'][0] * 10

			if (output_buy['sum_st_min_max'][0] != 0):
				score_sum_tp = (output_buy['sum_tp_min_max'][0]-output_buy['sum_st_min_max'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 1
			else:
				score_sum_tp = output_buy['sum_tp_min_max'][0]
				if (output_buy['sum_tp_min_max'][0] != 0):
					score_sum_tp = output_buy['sum_tp_min_max'][0] * 10

			output_buy['score_min_max'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]
			output_buy['score_pr'] = [0]
		else:
			output_buy['score_min_max'] = [0]
			output_buy['score_pr'] = [0]

		#///////////////////////////////////////////////

	#*********** Methode 1 Profits With MinMax Sell:
	if flag_trade == 'sell':

		output_sell = pd.DataFrame()

		if name_stp_minmax == True:

			#ramp_high_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_high',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#ramp_low_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_low',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_cci_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_cci',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#diff_min_max_candle_intervals_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_candle',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#value_min_cci_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_min_cci',
			 #min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			#value_max_cci_minmax_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_max_cci',
			 #min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=0.04)

			list_index_ok = np.where(
				#((signal_sell['ramp_high'].to_numpy()<=ramp_high_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['ramp_low'].to_numpy()<=ramp_low_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax_sell['interval'][upper]))&
				#((signal_sell['value_min_cci'].to_numpy()<=value_min_cci_minmax_sell['interval'][upper])) &
				#((signal_sell['value_max_cci'].to_numpy()>=value_max_cci_minmax_sell['interval'][lower]))
				True)[0]

			#list_index_ok = range(0,len(signal_sell))
		
			output_sell['mean_tp_min_max'] = [np.mean(signal_sell['tp_min_max'][list_index_ok])]
			output_sell['mean_st_min_max'] = [np.mean(signal_sell['st_min_max'][list_index_ok])]
			output_sell['max_tp_min_max'] = [np.max(signal_sell['tp_min_max'][list_index_ok])]
			output_sell['max_st_min_max'] = [np.max(signal_sell['st_min_max'][list_index_ok])]
			try:
				output_sell['sum_st_min_max'] = [np.sum(signal_sell['st_min_max'][list_index_ok[np.where(signal_sell['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_sell['sum_tp_min_max'] = [np.sum(signal_sell['tp_min_max'][list_index_ok[np.where(signal_sell['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
			except Exception as ex:
				print('tester minmax sell: ',ex)
				output_sell['sum_st_min_max'] = 0
				output_sell['sum_tp_min_max'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_sell['flag_min_max'][list_index_ok]:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_sell['num_tp_min_max'] = [tp_counter]
			output_sell['num_st_min_max'] = [st_counter]
			output_sell['num_trade_min_max'] = [st_counter + tp_counter]
	#output_sell['ramp_low_upper_min_max'] = [ramp_low_intervals_minmax_sell['interval'][upper]]
	#output_sell['ramp_low_lower_min_max'] = [ramp_low_intervals_minmax_sell['interval'][lower]]
	#output_sell['ramp_high_upper_min_max'] = [ramp_high_intervals_minmax_sell['interval'][upper]]
	#output_sell['ramp_high_lower_min_max'] = [ramp_high_intervals_minmax_sell['interval'][lower]]
	#output_sell['diff_min_max_cci_upper_min_max'] = [diff_min_max_cci_intervals_minmax_sell['interval'][upper]]
	#output_sell['diff_min_max_cci_lower_min_max'] = [diff_min_max_cci_intervals_minmax_sell['interval'][lower]]
	#output_sell['diff_min_max_candle_upper_min_max'] = [diff_min_max_candle_intervals_minmax_sell['interval'][upper]]
	#output_sell['diff_min_max_candle_lower_min_max'] = [diff_min_max_candle_intervals_minmax_sell['interval'][lower]]
			#output_sell['value_max_lower_cci_min_max'] = [value_max_cci_minmax_sell['interval'][lower]]
			#output_sell['value_min_upper_cci_min_max'] = [value_min_cci_minmax_sell['interval'][upper]]

			if output_sell['num_trade_min_max'][0] != 0:

				if output_sell['num_st_min_max'][0] != 0:
					score_num_tp = (tp_counter-output_sell['num_st_min_max'][0])

					if (tp_counter-output_sell['num_st_min_max'][0]) == 0:
						score_num_tp = 8

					if (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_sell['max_st_min_max'][0] != 0:
				score_max_tp = (output_sell['max_tp_min_max'][0]-output_sell['max_st_min_max'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_sell['max_tp_min_max'][0]
				if (output_sell['max_tp_min_max'][0] != 0):
					score_max_tp = output_sell['max_tp_min_max'][0] * 10

			if (output_sell['mean_st_min_max'][0] != 0):
				score_mean_tp = (output_sell['mean_tp_min_max'][0]-output_sell['mean_st_min_max'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_sell['mean_tp_min_max'][0]
				if (output_sell['mean_tp_min_max'][0] != 0):
					score_mean_tp = output_sell['mean_tp_min_max'][0] * 10

			if (output_sell['sum_st_min_max'][0] != 0):
				score_sum_tp = (output_sell['sum_tp_min_max'][0]-output_sell['sum_st_min_max'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 1
			else:
				score_sum_tp = output_sell['sum_tp_min_max'][0]
				if (output_sell['sum_tp_min_max'][0] != 0):
					score_sum_tp = output_sell['sum_tp_min_max'][0] * 10

			output_sell['score_min_max'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]
			output_sell['score_pr'] = [0]
		else:
			output_sell['score_min_max'] = [0]
			output_sell['score_pr'] = [0]

		#///////////////////////////////////////////////
	
	#*********** Methode 2 Profits With PR Buy:
	if flag_trade == 'buy':
		if name_stp_pr == True:
			#ramp_low_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='ramp_low',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#ramp_high_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='ramp_high',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_min_max_cci_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_cci',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_min_max_candle_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_min_max_candle',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_top_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_pr_top',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_down_intervals_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='diff_pr_down',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			value_min_cci_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='value_min_cci',
			 min_tp=0.0, max_st=0, name_stp='flag_pr',alpha=0.05)

			#value_max_cci_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='value_max_cci',
			# min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			diff_top_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='tp_pr',
			 	min_tp=0.0, max_st=0, name_stp='flag_pr',alpha=0.05)

			diff_down_pr_buy = Find_Best_intervals(signals=signal_buy,apply_to='st_pr',
			 	min_tp=0.0, max_st=0, name_stp='flag_pr',alpha=0.05)

			list_index_ok = np.where(
				#((signal_buy['ramp_low'].to_numpy()>=ramp_low_intervals_pr_buy['interval'][lower]))&
				#((signal_buy['ramp_high'].to_numpy()>=ramp_high_intervals_pr_buy['interval'][lower]))&
				#(signal_buy['diff_pr_top'].to_numpy()<=diff_top_intervals_pr_buy['interval'][upper])&
				#((signal_buy['trend_long'].to_numpy()!='sell')&
				#((signal_buy['trend_mid'].to_numpy()!='sell')&
				#(signal_buy['trend_short1'].to_numpy()=='buy')&
				#(signal_buy['trend_short2'].to_numpy()=='buy')))
				#((signal_buy['diff_pr_down'].to_numpy()<=diff_down_intervals_pr_buy['interval'][upper]))&
				#((signal_buy['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_pr_buy['interval'][upper]))&
				#((signal_buy['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_pr_buy['interval'][upper]))&
				#((signal_buy['value_min_cci'].to_numpy()<=value_min_cci_pr_buy['interval'][upper]))
				#((signal_buy['value_max_cci'].to_numpy()>=value_max_cci_pr_buy['interval'][lower]))
				True)[0]

			output_buy['mean_tp_pr'] = [np.mean(signal_buy['tp_pr'])]
			output_buy['mean_st_pr'] = [np.mean(signal_buy['st_pr'])]
			output_buy['max_tp_pr'] = [np.max(signal_buy['tp_pr'])]
			output_buy['max_st_pr'] = [np.max(signal_buy['st_pr'])]
			try:
				output_buy['sum_st_pr'] = [np.sum(signal_buy['st_pr'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy())]
				output_buy['sum_tp_pr'] = [np.sum(signal_buy['tp_pr'][np.where(signal_buy['flag_pr'] == 'tp')[0]].to_numpy())]
			except Exception as ex:
				print('error tester pr buy: ',ex)
				output_buy['sum_st_pr'] = 0
				output_buy['sum_tp_pr'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_buy['flag_pr']:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_buy['num_tp_pr'] = [tp_counter]
			output_buy['num_st_pr'] = [st_counter]
			output_buy['num_trade_pr'] = [st_counter + tp_counter]

			output_buy['max_st'] = [diff_down_pr_buy['interval'][upper]]
			output_buy['max_tp'] = [diff_top_pr_buy['interval'][upper]]

	#output_buy['ramp_low_upper_pr'] = [ramp_low_intervals_pr_buy['interval'][upper]]
	#output_buy['ramp_low_lower_pr'] = [ramp_low_intervals_pr_buy['interval'][lower]]
	#output_buy['ramp_high_upper_pr'] = [ramp_high_intervals_pr_buy['interval'][upper]]
	#output_buy['ramp_high_lower_pr'] = [ramp_high_intervals_pr_buy['interval'][lower]]
	#output_buy['diff_min_max_cci_upper_pr'] = [diff_min_max_cci_intervals_pr_buy['interval'][upper]]
	#output_buy['diff_min_max_cci_lower_pr'] = [diff_min_max_cci_intervals_pr_buy['interval'][lower]]
	#output_buy['diff_min_max_candle_upper_pr'] = [diff_min_max_candle_intervals_pr_buy['interval'][upper]]
	#output_buy['diff_min_max_candle_lower_pr'] = [diff_min_max_candle_intervals_pr_buy['interval'][lower]]
			#output_buy['diff_top_upper_pr'] = [diff_top_intervals_pr_buy['interval'][upper]]
			#output_buy['diff_top_lower_pr'] = [diff_top_intervals_pr_buy['interval'][lower]]
	#output_buy['diff_down_upper_pr'] = [diff_down_intervals_pr_buy['interval'][upper]]
	#output_buy['diff_down_lower_pr'] = [diff_down_intervals_pr_buy['interval'][lower]]
	#output_buy['value_max_lower_cci_pr'] = [value_max_cci_pr_buy['interval'][lower]]
			output_buy['value_min_upper_cci_pr'] = [value_min_cci_pr_buy['interval'][upper]]

			if output_buy['num_trade_pr'][0] != 0:

				if output_buy['num_st_pr'][0] != 0:
					score_num_tp = (tp_counter-output_buy['num_st_pr'][0])

					if (tp_counter-output_buy['num_st_pr'][0]) == 0:
						score_num_tp = 8

					elif (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_buy['max_st_pr'][0] != 0:
				score_max_tp = (output_buy['max_tp_pr'][0]-output_buy['max_st_pr'][0])

				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_buy['max_tp_pr'][0]
				if (output_buy['max_tp_pr'][0] != 0):
					score_max_tp = output_buy['max_tp_pr'][0] * 10

			if (output_buy['mean_st_pr'][0] != 0):
				score_mean_tp = (output_buy['mean_tp_pr'][0]-output_buy['mean_st_pr'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_buy['mean_tp_pr'][0]
				if (output_buy['mean_tp_pr'][0] != 0):
					score_mean_tp = output_buy['mean_tp_pr'][0] * 10

			if (output_buy['sum_st_pr'][0] != 0):
				score_sum_tp = (output_buy['sum_tp_pr'][0]-output_buy['sum_st_pr'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 0.1
			else:
				score_sum_tp = output_buy['sum_tp_pr'][0]
				if (output_buy['sum_tp_pr'][0] != 0):
					score_sum_tp = output_buy['sum_tp_pr'][0] * 10

			output_buy['score_pr'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

			if name_stp_minmax != True:
				output_buy['score_min_max'] = [0]
	
		else:
			output_buy['score_pr'] = [0]

			if name_stp_minmax != True:
				output_buy['score_min_max'] = [0]

		if np.isnan(output_buy['score_pr'][0]) : output_buy['score_pr'][0] = 0
		if np.isnan(output_buy['score_min_max'][0]) : output_buy['score_min_max'][0] = 0

		if (output_buy['score_pr'][0] > output_buy['score_min_max'][0]):
			output_buy['methode'] = ['pr']

		if (output_buy['score_min_max'][0] >= output_buy['score_pr'][0]):
			output_buy['methode'] = ['min_max']

		if (output_buy['score_pr'][0] == 0) and (output_buy['score_min_max'][0] == 0):
			output_buy['methode'] = ['no_trade']

	#///////////////////////////////////////////////
	
	#*********** Methode 2 Profits With PR Sell:
	if flag_trade == 'sell':
		if name_stp_pr == True:
			#ramp_low_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_low',
			 #min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#ramp_high_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='ramp_high',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_min_max_cci_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_cci',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_min_max_candle_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_min_max_candle',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_top_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_pr_top',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#diff_down_intervals_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='diff_pr_down',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=alpha)

			#value_min_cci_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_min_cci',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_min_max',alpha=alpha)

			#value_max_cci_pr_sell = Find_Best_intervals(signals=signal_sell,apply_to='value_max_cci',
	 		#min_tp=min_tp, max_st=max_st, name_stp='flag_pr',alpha=0.1)

			list_index_ok = np.where(
				#((signal_sell['ramp_low'].to_numpy()<=ramp_low_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['ramp_high'].to_numpy()<=ramp_high_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['diff_pr_top'].to_numpy()<=diff_top_intervals_pr_sell['interval'][upper]))&
				#(signal_sell['diff_pr_down'].to_numpy()<=diff_down_intervals_pr_sell['interval'][upper])&
				#((signal_sell['trend_long'].to_numpy()!='buy')&
				#((signal_sell['trend_mid'].to_numpy()!='buy')&
				#(signal_sell['trend_short1'].to_numpy()=='sell')&
				#(signal_sell['trend_short2'].to_numpy()=='sell')))
				#((signal_sell['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_pr_sell['interval'][upper]))&
				#((signal_sell['value_min_cci'].to_numpy()<=value_min_cci_pr_sell['interval'][upper]))&
				#((signal_sell['value_max_cci'].to_numpy()>=value_max_cci_pr_sell['interval'][lower]))
				True)[0]

			output_sell['mean_tp_pr'] = [np.mean(signal_sell['tp_pr'])]
			output_sell['mean_st_pr'] = [np.mean(signal_sell['st_pr'])]
			output_sell['max_tp_pr'] = [np.max(signal_sell['tp_pr'])]
			output_sell['max_st_pr'] = [np.max(signal_sell['st_pr'])]
			try:
				output_sell['sum_st_pr'] = [np.sum(signal_sell['st_pr'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy())]
				output_sell['sum_tp_pr'] = [np.sum(signal_sell['tp_pr'][np.where(signal_sell['flag_pr'] == 'tp')[0]].to_numpy())]
			except Exception as ex:
				print('error tester pr sell: ',ex)
				output_sell['sum_st_pr'] = 0
				output_sell['sum_tp_pr'] = 0

			tp_counter = 0
			st_counter = 0
			for elm in signal_sell['flag_pr']:
				if (elm == 'tp'):
					tp_counter += 1
				if (elm == 'st'):
					st_counter += 1
			output_sell['num_tp_pr'] = [tp_counter]
			output_sell['num_st_pr'] = [st_counter]
			output_sell['num_trade_pr'] = [st_counter + tp_counter]
	#output_sell['ramp_low_upper_pr'] = [ramp_low_intervals_pr_sell['interval'][upper]]
	#output_sell['ramp_low_lower_pr'] = [ramp_low_intervals_pr_sell['interval'][lower]]
	#output_sell['ramp_high_upper_pr'] = [ramp_high_intervals_pr_sell['interval'][upper]]
	#output_sell['ramp_high_lower_pr'] = [ramp_high_intervals_pr_sell['interval'][lower]]
	#output_sell['diff_min_max_cci_upper_pr'] = [diff_min_max_cci_intervals_pr_sell['interval'][upper]]
	#output_sell['diff_min_max_cci_lower_pr'] = [diff_min_max_cci_intervals_pr_sell['interval'][lower]]
	#output_sell['diff_min_max_candle_upper_pr'] = [diff_min_max_candle_intervals_pr_sell['interval'][upper]]
	#output_sell['diff_min_max_candle_lower_pr'] = [diff_min_max_candle_intervals_pr_sell['interval'][lower]]
	#output_sell['diff_top_upper_pr'] = [diff_top_intervals_pr_sell['interval'][upper]]
	#output_sell['diff_top_lower_pr'] = [diff_top_intervals_pr_sell['interval'][lower]]
			#output_sell['diff_down_upper_pr'] = [diff_down_intervals_pr_sell['interval'][upper]]
			#output_sell['diff_down_lower_pr'] = [diff_down_intervals_pr_sell['interval'][lower]]
			#output_sell['value_max_lower_cci_pr'] = [value_max_cci_pr_sell['interval'][lower]]
	#output_sell['value_min_upper_cci_pr'] = [value_min_cci_pr_sell['interval'][upper]]

			if output_sell['num_trade_pr'][0] != 0:

				if output_sell['num_st_pr'][0] != 0:
					score_num_tp = (tp_counter-output_sell['num_st_pr'][0])

					if (tp_counter-output_sell['num_st_pr'][0]):
						score_num_tp = 8

					elif (score_num_tp > 0):
						score_num_tp = score_num_tp * 9
					else:
						score_num_tp = 1
				else:
					if tp_counter != 0:
						score_num_tp = tp_counter * 10
					else:
						score_num_tp = 1
			else:
				score_num_tp = 1

			if output_sell['max_st_pr'][0] != 0:
				score_max_tp = (output_sell['max_tp_pr'][0]-output_sell['max_st_pr'][0])
				if (score_max_tp > 0):
					score_max_tp = score_max_tp * 9
				else:
					score_max_tp = 1
			else:
				score_max_tp = output_sell['max_tp_pr'][0]
				if (output_sell['max_tp_pr'][0] != 0):
					score_max_tp = output_sell['max_tp_pr'][0] * 10

			if (output_sell['mean_st_pr'][0] != 0):
				score_mean_tp = (output_sell['mean_tp_pr'][0]-output_sell['mean_st_pr'][0])

				if (score_mean_tp > 0):
					score_mean_tp = score_mean_tp * 9
				else:
					score_mean_tp = 1
			else:
				score_mean_tp = output_sell['mean_tp_pr'][0]
				if (output_sell['mean_tp_pr'][0] != 0):
					score_mean_tp = output_sell['mean_tp_pr'][0] * 10

			if (output_sell['sum_st_pr'][0] != 0):
				score_sum_tp = (output_sell['sum_tp_pr'][0]-output_sell['sum_st_pr'][0])

				if (score_sum_tp > 0):
					score_sum_tp = score_sum_tp * 9
				else:
					score_sum_tp = 0.1
			else:
				score_sum_tp = output_sell['sum_tp_pr'][0]
				if (output_sell['sum_tp_pr'][0] != 0):
					score_sum_tp = output_sell['sum_tp_pr'][0] * 10

			output_sell['score_pr'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

			if name_stp_minmax != True:
				output_sell['score_min_max'] = [0]

		else:
			output_sell['score_pr'] = [0]

			if name_stp_minmax != True:
				output_sell['score_min_max'] = [0]

		if np.isnan(output_sell['score_pr'][0]) : output_sell['score_pr'][0] = 0
		if np.isnan(output_sell['score_min_max'][0]) : output_sell['score_min_max'][0] = 0

		if (output_sell['score_pr'][0] > output_sell['score_min_max'][0]):
			output_sell['methode'] = ['pr']

		if (output_sell['score_min_max'][0] >= output_sell['score_pr'][0]):
			output_sell['methode'] = ['min_max']

		if (output_sell['score_pr'][0] == 0) and (output_sell['score_min_max'][0] == 0):
			output_sell['methode'] = ['no_trade']

	#///////////////////////////////////////////////

	if flag_trade == 'buy':
		output_sell = pd.DataFrame()

	if flag_trade == 'sell':
		output_buy = pd.DataFrame()

	return output_buy,output_sell
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Create First Cromosomes *******************************************************
#@stTime
def initilize_values_genetic(
							high_period_upper,
							high_period_lower,
							low_period_upper,
							low_period_lower
							):
	#************************** initialize Values ******************************************************
	Chromosome = {}

	Chromosome[0] = {
	'high_period': high_period_upper,
	'low_period': low_period_upper,
	'distance_lines': 2,
	'cross_line': 70,
	#'max_st': 0.4,
	#'max_tp': 0.6,
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}

	Chromosome[1] = {
	'high_period': high_period_lower,
	'low_period': low_period_lower,
	'distance_lines': 4,
	'cross_line': 100,
	#'max_st': 0.5,
	#'max_tp': 0.5,
	'signal': None,
	'score_buy': 0,
	'score_sell': 0
	}
	i = 2
	while i < 5:
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		
		#while max_tp < max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		Chromosome[i] = {
			'high_period': randint(high_period_lower, high_period_upper),
			'low_period': randint(low_period_lower, low_period_upper),
			'distance_lines': randint(0, 6),
			'cross_line': randint(0, 150),
			#'max_st': max_st,
			#'max_tp': max_tp,
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
			}

		if (Chromosome[i]['high_period'] <= Chromosome[i]['low_period'] + 10): continue
		res = list(Chromosome[i].keys()) 
		#print(res[1])
		#print(Chromosome[i][res[1]])
		i += 1
	#***********************************************************************************
	return Chromosome
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#************************************************ Gen Creator ****************************************************************
def takeSecond(elem):
    return elem[1]

#@stTime
def gen_creator(
				Chromosome,
				high_period_upper,
				high_period_lower,
				low_period_upper,
				low_period_lower
				):

	Chromosome_Cutter = randint(0, 3)

	Chromosome_selector = randint(0, 4)

	baby = {}

	#print('Generate Baby')
	chrom_creator_counter = 0
	baby_counter = 0

	baby_counter_create = 0

	while (baby_counter_create < (len(Chromosome) * 2)):
		
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		#while max_tp <= max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		baby[baby_counter_create] = {
			'high_period': randint(high_period_lower, high_period_upper),
			'low_period': randint(low_period_lower, low_period_upper),
			'distance_lines': randint(0, 6),
			'cross_line': randint(0, 150),
			#'max_st': max_st,
			#'max_tp': max_tp,
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
			}

		baby_counter_create += 1

	scr = []
	for k,v in zip(Chromosome.keys(), Chromosome.values()):
		scr.append([k, (v.get('score_buy') + v.get('score_sell'))/2])

	scr_idx = sorted(scr, key=takeSecond, reverse=True)[:int(len(Chromosome)/2)]

	while chrom_creator_counter < len(Chromosome):

		#********************************************* Baby ***********************************************************
		
		
		Chromosome_selector_1 = np.random.choice(len(scr_idx), size=1)[0]
		Chromosome_selector_2 = np.random.choice(len(scr_idx), size=1)[0]

		res_1 = list(Chromosome[Chromosome_selector_1].keys())
		res_2 = list(Chromosome[Chromosome_selector_2].keys())

		Chromosome_Cutter = randint(0, 3)
		change_chrom_counter = 0

		while change_chrom_counter < Chromosome_Cutter:
						#print(change_chrom_counter)
			baby[baby_counter].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})

			change_chrom_counter += 1

		change_chrom_counter = Chromosome_Cutter

		while change_chrom_counter < 4:
			baby[baby_counter].update({res_2[change_chrom_counter]: Chromosome[Chromosome_selector_2][res_2[change_chrom_counter]]})
			baby[baby_counter + 1].update({res_1[change_chrom_counter]: Chromosome[Chromosome_selector_1][res_1[change_chrom_counter]]})
			change_chrom_counter += 1

		baby_counter = baby_counter + 2

					#********************************************///////***************************************************************************
		chrom_creator_counter += 1

	i = 0
	limit_counter = len(Chromosome) * 2 
	while i < (limit_counter):
		#max_tp = randint(10, 80)/100
		#max_st = randint(10, 70)/100
		#while max_tp <= max_st:
			#max_tp = randint(10, 80)/100
			#max_st = randint(10, 70)/100

		Chromosome[i] = {
			'high_period': randint(high_period_lower, high_period_upper),
			'low_period': randint(low_period_lower, low_period_upper),
			'distance_lines': randint(0, 6),
			'cross_line': randint(0, 150),
			#'max_st': max_st,
			#'max_tp': max_tp,
			'signal': None,
			'score_buy': 0,
			'score_sell': 0
			}

		if (Chromosome[i]['high_period'] <= Chromosome[i]['low_period'] + 10): continue
		i += 1

	re_counter = 0
	while (re_counter < limit_counter):
		Chromosome[re_counter]['high_period'] = baby[re_counter]['high_period']
		Chromosome[re_counter]['low_period'] = baby[re_counter]['low_period']
		Chromosome[re_counter]['distance_lines'] = baby[re_counter]['distance_lines']
		Chromosome[re_counter]['cross_line'] = baby[re_counter]['cross_line']
		#Chromosome[re_counter]['max_st'] = baby[re_counter]['max_st']
		#Chromosome[re_counter]['max_tp'] = baby[re_counter]['max_tp']
		Chromosome[re_counter]['signal'] = baby[re_counter]['signal']
		Chromosome[re_counter]['score_buy'] = baby[re_counter]['score_buy']
		Chromosome[re_counter]['score_sell'] = baby[re_counter]['score_sell']

		if (Chromosome[re_counter]['high_period'] <= Chromosome[re_counter]['low_period']):
			high_period = randint(high_period_lower, high_period_upper) 
			low_period = randint(low_period_lower, low_period_upper)
			while high_period <= low_period + 10:
				high_period = randint(high_period_lower, high_period_upper) 
				low_period = randint(low_period_lower, low_period_upper)

			Chromosome[re_counter] = {
						'high_period': high_period,
						'low_period': low_period,
						'distance_lines': randint(0, 6),
						'cross_line': randint(0, 150),
						#'max_st': max_st,
						#'max_tp': max_tp,
						'signal': None,
						'score_buy': 0,
						'score_sell': 0
						}
		re_counter += 1

	for key in Chromosome.keys():
		i = 0
		while i < len(Chromosome):
			if key == i:
				i += 1
				continue
			if (
				Chromosome[key]['high_period'] == Chromosome[i]['high_period'] and
				Chromosome[key]['low_period'] == Chromosome[i]['low_period'] and
				Chromosome[key]['distance_lines'] == Chromosome[i]['distance_lines'] and
				Chromosome[key]['cross_line'] == Chromosome[i]['cross_line']
				#Chromosome[key]['max_st'] == Chromosome[i]['max_st'] and
				#Chromosome[key]['max_tp'] == Chromosome[i]['max_tp']
				):

				#max_tp = randint(10, 80)/100
				#max_st = randint(10, 70)/100
		
				#while max_tp < max_st:
					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100

				high_period = randint(high_period_lower, high_period_upper) 
				low_period = randint(low_period_lower, low_period_upper)
				while high_period <= low_period + 10:
					high_period = randint(high_period_lower, high_period_upper) 
					low_period = randint(low_period_lower, low_period_upper)

				Chromosome[i] = {
							'high_period': high_period,
							'low_period': low_period,
							'distance_lines': randint(0, 6),
							'cross_line': randint(0, 150),
							#'max_st': max_st,
							#'max_tp': max_tp,
							'signal': None,
							'score_buy': 0,
							'score_sell': 0
							}
			i += 1
		#print(Chromosome_5M[6])

	return Chromosome

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#***************************************** Genetic Algorithm **************************************************************

#@stTime
#@cuda.jit()
def genetic_algo_cci_golden_cross(
								symbol_data_5M,
								symbol_data_15M,
								dataset_1H,
								dataset_4H,
								symbol,
								num_turn,
								max_score_ga_buy,
								max_score_ga_sell,
								flag_trade
								):

	#*************************** Algorithm *************************************************//

	high_period_upper = 800
	high_period_lower = 500

	low_period_upper = 750
	low_period_lower = 450

	Chromosome = initilize_values_genetic(
										high_period_upper=high_period_upper,
										high_period_lower=high_period_lower,
										low_period_upper=low_period_upper,
										low_period_lower=low_period_lower
										)

	if os.path.exists("Genetic_cci_output_buy/"+symbol+'.csv'):
		with open("Genetic_cci_output_buy/"+symbol+'.csv', 'r', newline='') as myfile:
			for line in csv.DictReader(myfile):
				chrom_get = line

				Chromosome[0]['high_period'] = float(chrom_get['high_period'])
				Chromosome[0]['low_period'] = float(chrom_get['low_period'])

				if flag_trade == 'buy':
					high_period_upper = Chromosome[0]['high_period'] + 100
					high_period_lower = Chromosome[0]['high_period'] - 100

					low_period_upper = Chromosome[0]['low_period'] + 100
					low_period_lower = Chromosome[0]['low_period'] - 100

	Chromosome = initilize_values_genetic(
										high_period_upper=high_period_upper,
										high_period_lower=high_period_lower,
										low_period_upper=low_period_upper,
										low_period_lower=low_period_lower
										)

	print('================================ START Genetic BUY ==> ',symbol)
	print('\n')

	now = datetime.now()

	if flag_trade == 'buy':
		buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
		if os.path.exists(buy_path):
			ga_result_buy, _ = read_ga_result(symbol=symbol)
			max_st_buy = ga_result_buy['max_st_pr'][0]
			max_tp_buy = ga_result_buy['max_tp_pr'][0]
		else:
			max_st_buy = randint(50, 80)/100
			max_tp_buy = randint(50, 80)/100

	#print('===============> ',symbol)

	if os.path.exists("Genetic_cci_output_buy/"+symbol+'.csv'):
		with open("Genetic_cci_output_buy/"+symbol+'.csv', 'r', newline='') as myfile:
			for line in csv.DictReader(myfile):
				chrom_get = line

				Chromosome[0]['high_period'] = float(chrom_get['high_period'])
				Chromosome[0]['low_period'] = float(chrom_get['low_period'])
				Chromosome[0]['distance_lines'] = float(chrom_get['distance_lines'])
				Chromosome[0]['cross_line'] = float(chrom_get['cross_line'])
				#Chromosome[0]['max_st'] = float(chrom_get['max_st'])
				#Chromosome[0]['max_tp'] = float(chrom_get['max_tp'])
				Chromosome[0]['signal'] = chrom_get['signal']
				Chromosome[0]['score_buy'] = float(chrom_get['score_buy'])
				Chromosome[0]['score_sell'] = float(chrom_get['score_sell'])

				if flag_trade == 'buy':
					high_period_upper = Chromosome[0]['high_period'] + 100
					high_period_lower = Chromosome[0]['high_period'] - 100

					low_period_upper = Chromosome[0]['low_period'] + 100
					low_period_lower = Chromosome[0]['low_period'] - 100

				if flag_trade == 'buy':
					ga_result_buy, _ = read_ga_result(symbol=symbol)

					if ga_result_buy['methode'][0] == 'min_max':
						max_score_ga_buy = float(chrom_get['score_min_max'])

					if ga_result_buy['methode'][0] == 'pr':
						max_score_ga_buy = float(chrom_get['score_pr'])
				print(Chromosome[0])

	if os.path.exists("Genetic_cci_output_sell/"+symbol+'.csv'):
		with open("Genetic_cci_output_sell/"+symbol+'.csv', 'r', newline='') as myfile:
			for line in csv.DictReader(myfile):
				chrom_get = line
				Chromosome[1]['high_period'] = float(chrom_get['high_period'])
				Chromosome[1]['low_period'] = float(chrom_get['low_period'])
				Chromosome[1]['distance_lines'] = float(chrom_get['distance_lines'])
				Chromosome[1]['cross_line'] = float(chrom_get['cross_line'])
				#Chromosome[1]['max_st'] = float(chrom_get['max_st'])
				#Chromosome[1]['max_tp'] = float(chrom_get['max_tp'])
				Chromosome[1]['signal'] = chrom_get['signal']
				Chromosome[1]['score_buy'] = float(chrom_get['score_buy'])
				Chromosome[1]['score_sell'] = float(chrom_get['score_sell'])

				if flag_trade == 'sell':
					_, ga_result_sell = read_ga_result(symbol=symbol)

					if ga_result_sell['methode'][0] == 'min_max':
						max_score_ga_sell = float(chrom_get['score_min_max'])

					if ga_result_sell['methode'][0] == 'pr':
						max_score_ga_sell = float(chrom_get['score_pr'])
				print(Chromosome[1])

				

	result_buy = pd.DataFrame()
	chromosome_buy = pd.DataFrame()

	result_sell = pd.DataFrame()
	chromosome_sell = pd.DataFrame()

	chrom_counter = 0
	all_chorms = 0
	chorm_reset_counter = 0

	learning_interval_counter = 0
	learn_counter = 1
	cross_line_upper_out_tester = 150

	with tqdm(total=num_turn) as pbar:
		while chrom_counter < len(Chromosome):

			#print('==== flag trade===> ', flag_trade)
			print()

			if flag_trade == 'buy':
				print()
				print('================== Num BUY Symbol ==>',symbol)
				print()
				print('================== Num BUY =========> ',len(chromosome_buy))

			if flag_trade == 'sell':
				print()
				print('================== Num SELL Symbol =>',symbol)
				print()
				print('================== Num SELL ========> ',len(chromosome_sell))

			print('================== Num Chroms ======> ',chrom_counter)
			print('================== All Chorms ======> ',all_chorms)
			print('================== Chorm Reseter ===> ',chorm_reset_counter)
			print('================== AI Turn =========> ',learn_counter-1)

			print()
			pbar_numbers = int((len(chromosome_buy) + len(chromosome_sell))/2)
			pbar.update(pbar_numbers)

			print()
			

			if (chorm_reset_counter >= 40):
				chorm_reset_counter = 0
				Chromosome.pop(chrom_counter)
				high_period = randint(high_period_lower, high_period_upper) 
				low_period = randint(low_period_lower, low_period_upper)
				while high_period <= low_period + 10:
					high_period = randint(high_period_lower, high_period_upper) 
					low_period = randint(low_period_lower, low_period_upper)

				#max_tp = randint(10, 80)/100
				#max_st = randint(10, 70)/100
				#while max_tp <= max_st:
					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100

				if flag_trade == 'buy':
					cross_line_upper_out_tester = abs(int(np.min(ind.cci(
																		high=symbol_data_5M[symbol]['high'],
																		low=symbol_data_5M[symbol]['low'],
																		close=symbol_data_5M[symbol]['close'],
																		length = low_period
																		))/2))

				Chromosome[chrom_counter] = {
					'high_period': high_period,
					'low_period': low_period,
					'distance_lines': randint(0, 10),
					'cross_line': randint(0, cross_line_upper_out_tester),
					#'max_st': max_st,
					#'max_tp': max_tp,
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				#all_chorms += 1
				#continue

			if False:#learning_interval_counter >= 100:

				learning_interval_counter = 0

				if learn_counter >= 5: break

				low_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))
				high_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))

				while (high_distance < low_distance) or (high_distance - low_distance != 10000):

					low_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))
					high_distance = randint((learn_counter*16800), ((learn_counter*16800) + 16800))

				print('==== High Distance =============> ',high_distance)
				print('==== Low Distance ==============> ',low_distance)

				print('==== Symbol ====================> ',symbol)

				print('==== AI Turn ===================> ',learn_counter)
				print('==== Length Dataset ============> ',high_distance - low_distance)

				dataset_5M, symbol_data_15M, dataset_1H, symbol_data_4H, _ = read_dataset_csv(
																									sym=symbol,
																									num_5M=99000,
																									num_15M=1,
																									num_1H=8250,
																									num_4H=1
																									)
				symbol_data_5M,symbol_data_1H = dataset_spliter(
															symbol=symbol,
															dataset_5M=dataset_5M,
															dataset_1H=dataset_1H,
															spliter_5M_end=high_distance,
															spliter_5M_first=low_distance
															)
				learn_counter += 1

			chorm_reset_counter += 1
			all_chorms += 1

			try:
				if flag_trade == 'buy':
					buy_data, _ = golden_cross_zero(
													dataset=symbol_data_5M,
													dataset_15M=symbol_data_15M,
													dataset_1H=dataset_1H,
													dataset_4H=dataset_4H,
													symbol=symbol,
													Low_Period=Chromosome[chrom_counter]['low_period'],
													High_Period=Chromosome[chrom_counter]['high_period'],
													distance_lines=Chromosome[chrom_counter]['distance_lines'],
													cross_line=-Chromosome[chrom_counter]['cross_line'],
													mode='optimize',
													name_stp_minmax=False,
													name_stp_pr=True,
													plot=False,
													pbar_flag=False,
													buy_flag=True,
													sell_flag=False,
													st_percent_minmax_buy=max_st_buy,#Chromosome[chrom_counter]['max_st'],
													st_percent_minmax_sell=1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_sell_min = 1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_sell_max = 1,#Chromosome[chrom_counter]['max_tp'],
													tp_percent_minmax_buy_min = 1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_buy_max = max_tp_buy#Chromosome[chrom_counter]['max_tp']
													)
					#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						#print('=======> buy_data = ',buy_data))

				if flag_trade == 'sell':
					_, sell_data = golden_cross_zero(
													dataset=symbol_data_5M,
													dataset_15M=symbol_data_15M,
													dataset_1H=dataset_1H,
													dataset_4H=dataset_4H,
													symbol=symbol,
													Low_Period=Chromosome[chrom_counter]['low_period'],
													High_Period=Chromosome[chrom_counter]['high_period'],
													distance_lines=Chromosome[chrom_counter]['distance_lines'],
													cross_line=Chromosome[chrom_counter]['cross_line'],
													mode='optimize',
													name_stp_minmax=False,
													name_stp_pr=True,
													plot=False,
													pbar_flag=False,
													buy_flag=False,
													sell_flag=True,
													st_percent_minmax_buy=1,#Chromosome[chrom_counter]['max_st'],
													st_percent_minmax_sell=1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_sell_min = 1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_sell_max = 1,#Chromosome[chrom_counter]['max_tp'],
													tp_percent_minmax_buy_min = 1,#Chromosome[chrom_counter]['max_st'],
													tp_percent_minmax_buy_max = 1#Chromosome[chrom_counter]['max_tp']
													)
					#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						#print('=======> sell_data = ',sell_data))

	
				flag_golden_cross = False

				if flag_trade == 'buy' and buy_data.empty==True:
					flag_golden_cross = True

				if flag_trade == 'sell' and sell_data.empty==True:
					flag_golden_cross = True

			except Exception as ex:
				print('getting error GA Golden Cross: ', ex)
				flag_golden_cross = True

			with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				print('======== Chorme ================> ')
				print()
				print('........................................................')
				print(Chromosome[chrom_counter])
				print('........................................................')
				print()

			if flag_golden_cross:
				max_st_buy = randint(10, 80)/100
				max_tp_buy = randint(10, 80)/100
				#Chromosome.pop(chrom_counter)
				high_period = randint(300, 800)
				low_period = randint(250, 750)
				while high_period <= low_period + 10:
					high_period = randint(300, 800)
					low_period = randint(250, 750)

				if flag_trade == 'buy':
					cross_line_upper_out_tester = abs(int(np.min(ind.cci(
																		high=symbol_data_5M[symbol]['high'],
																		low=symbol_data_5M[symbol]['low'],
																		close=symbol_data_5M[symbol]['close'],
																		length = low_period
																		))/2))

				#max_tp = randint(10, 80)/100
				#max_st = randint(10, 70)/100
				#while max_tp <= max_st:
					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100

				Chromosome[chrom_counter] = {
					'high_period': Chromosome[chrom_counter]['high_period'],#high_period,
					'low_period': Chromosome[chrom_counter]['low_period'],#low_period,
					'distance_lines': randint(0, 6),
					'cross_line': randint(0, cross_line_upper_out_tester),
					#'max_st': max_st,
					#'max_tp': max_tp,
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				continue

			try:
				if flag_trade == 'buy':
					output_buy, _ = tester_golden_cross_zero(
															signal_buy=buy_data,
															signal_sell=buy_data,
															min_tp=0.0,
															max_st=10,#Chromosome[chrom_counter]['max_st'],
															alpha=0.1,#Chromosome[chrom_counter]['max_tp'],
															name_stp_minmax=False,
															name_stp_pr=True,
															flag_trade=flag_trade
															)
					with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						print('======== Output Buy =======> ')
						print()
						print('........................................................')
						print(output_buy)
						print('........................................................')
						print()

				if flag_trade == 'sell':
					_, output_sell = tester_golden_cross_zero(
															signal_buy=sell_data,
															signal_sell=sell_data,
															min_tp=0.0,
															max_st=10,#Chromosome[chrom_counter]['max_st'],
															alpha=0.1,#Chromosome[chrom_counter]['max_tp'],
															name_stp_minmax=False,
															name_stp_pr=True,
															flag_trade=flag_trade
															)
					with pd.option_context('display.max_rows', None, 'display.max_columns', None):
						print('======== Output SELL ======> ')
						print()
						print('........................................................')
						print(output_sell)
						print('........................................................')
						print()

				flag_tester = False
			except Exception as ex:
				print('GA tester: ',ex)
				flag_tester = True

			if flag_tester:
				max_st_buy = randint(10, 80)/100
				max_tp_buy = randint(10, 80)/100
				#Chromosome.pop(chrom_counter)
				high_period = randint(5, 170)
				low_period = randint(5, 150)
				while high_period <= low_period + 10:
					high_period = randint(5, 170)
					low_period = randint(5, 150)

				if flag_trade == 'buy':
					cross_line_upper_out_tester = abs(int(np.min(ind.cci(
																		high=symbol_data_5M[symbol]['high'],
																		low=symbol_data_5M[symbol]['low'],
																		close=symbol_data_5M[symbol]['close'],
																		length = low_period
																		))/2))

				#max_tp = randint(10, 80)/100
				#max_st = randint(10, 70)/100
				#while max_tp <= max_st:
					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100

				Chromosome[chrom_counter] = {
					'high_period': Chromosome[chrom_counter]['high_period'],#high_period,
					'low_period': Chromosome[chrom_counter]['low_period'],#low_period,
					'distance_lines': randint(0, 6),
					'cross_line': randint(0, cross_line_upper_out_tester),
					#'max_st': max_st,
					#'max_tp': max_tp,
					'signal': None,
					'score_buy': 0,
					'score_sell': 0
					}
				continue

			if flag_trade == 'buy':
				if not np.isnan(output_buy['score_pr'][0]) or not np.isnan(output_buy['score_min_max'][0]):
					if (
						(
							output_buy['score_pr'][0] >= max_score_ga_buy * 0.99 and
							np.isnan(output_buy['score_pr'][0]) == False
						) or						(
							output_buy['score_min_max'][0] >= max_score_ga_buy * 0.99 and
							np.isnan(output_buy['score_min_max'][0]) == False
						)
						):
						
						Chromosome[chrom_counter]['signal'] = ('buy' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
						result_buy = result_buy.append(output_buy, ignore_index=True)
						score = (output_buy['score_pr'][0]+output_buy['score_min_max'][0])/2
						Chromosome[chrom_counter].update({'score_buy': score })
						chromosome_buy = chromosome_buy.append(Chromosome[chrom_counter], ignore_index=True)
						chorm_reset_counter = 0

						if output_buy['max_st_pr'][0] != 0:
							max_st_buy = output_buy['max_st_pr'][0]
						else:
							max_st_buy = randint(10, 80)/100

						if output_buy['max_tp_pr'][0] != 0:
							max_tp_buy = output_buy['max_tp_pr'][0]
						else:
							max_tp_buy = randint(10, 80)/100

						if output_buy['value_min_upper_cci_pr'][0] != 0:
							cross_line_upper_out_tester = abs(int(output_buy['value_min_upper_cci_pr'][0]))
						else:
							if flag_trade == 'buy':
								cross_line_upper_out_tester = abs(int(np.min(ind.cci(
																					high=symbol_data_5M[symbol]['high'],
																					low=symbol_data_5M[symbol]['low'],
																					close=symbol_data_5M[symbol]['close'],
																					length = Chromosome[chrom_counter]['low_period']
																					))/2))
								print('cross_line_upper_out_tester1 = ',cross_line_upper_out_tester)
						#max_score_ga_buy = np.max(chromosome_buy['score_pr'],1)
						#print('MMMMMMMMMaxxxxxxx ==========> ',max_score_ga_buy)

						bad_buy = False
					else:
						bad_buy = True

						if output_buy['max_st_pr'][0] != 0:
							max_st_buy = output_buy['max_st_pr'][0]
						else:
							max_st_buy = randint(10, 80)/100

						if output_buy['max_tp_pr'][0] != 0:
							max_tp_buy = output_buy['max_tp_pr'][0]
						else:
							max_tp_buy = randint(10, 80)/100

						if output_buy['value_min_upper_cci_pr'][0] != 0:
							cross_line_upper_out_tester = abs(int(output_buy['value_min_upper_cci_pr'][0]))
						else:
							cross_line_upper_out_tester = abs(int(np.min(ind.cci(
																				high=symbol_data_5M[symbol]['high'],
																				low=symbol_data_5M[symbol]['low'],
																				close=symbol_data_5M[symbol]['close'],
																				length = Chromosome[chrom_counter]['low_period']
																				))/2))
							print('cross_line_upper_out_tester2 = ',cross_line_upper_out_tester)

			print('== Max Score Buy Must Be ====> ',max_score_ga_buy)

			if flag_trade == 'sell':
				if not np.isnan(output_sell['score_pr'][0]) or not np.isnan(output_sell['score_min_max'][0]):
					if (
						(
							output_sell['score_pr'][0] >= max_score_ga_sell * 0.99 and
							np.isnan(output_sell['score_pr'][0]) == False
						) or
						(
							output_sell['score_min_max'][0] >= max_score_ga_sell * 0.99 and
							np.isnan(output_sell['score_min_max'][0]) == False
						)
						):
						
						Chromosome[chrom_counter]['signal'] = ('sell' if Chromosome[chrom_counter].get('signal') else 'buy,sell')
						result_sell = result_sell.append(output_sell, ignore_index=True)
						score = (output_sell['score_pr'][0]+output_sell['score_min_max'][0])/2
						Chromosome[chrom_counter].update({'score_sell': score })
						chromosome_sell = chromosome_sell.append(Chromosome[chrom_counter], ignore_index=True)
						chorm_reset_counter = 0
						#max_score_ga_sell = np.max(chromosome_sell['score_pr'],1)

						bad_sell = False
					else:
						bad_sell = True

			print('== Max Score Sell Must Be =====> ',max_score_ga_sell)

			if flag_trade == 'buy':
				if (
					len(chromosome_buy) >= int(num_turn/20)
					):
					break

			if flag_trade == 'sell':
				if (
					len(chromosome_sell) >= int(num_turn/20)
					):
					break

			#if (
				#len(chromosome_buy) >= int(num_turn/12) or
				#len(chromosome_sell) >= int(num_turn/12)
				#):
				#if (len(chromosome_buy) >= int(num_turn/12)) and (len(chromosome_sell) >= 4): break
				#if (len(chromosome_sell) >= int(num_turn/12)) and (len(chromosome_buy) >= 4): break

			if flag_trade == 'buy':
				if bad_buy == True:

					#Chromosome.pop(chrom_counter)
					high_period = randint(5, 170)
					low_period = randint(5, 150)
					while high_period <= low_period + 10:
						high_period = randint(5, 170)
						low_period = randint(5, 150)

					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100
					#while max_tp <= max_st:
						#max_tp = randint(10, 80)/100
						#max_st = randint(10, 70)/100

					Chromosome[chrom_counter] = {
						'high_period': Chromosome[chrom_counter]['high_period'],#high_period,
						'low_period': Chromosome[chrom_counter]['low_period'],#low_period,
						'distance_lines': randint(0, 6),
						'cross_line': randint(0, cross_line_upper_out_tester),
						#'max_st': max_st,
						#'max_tp': max_tp,
						'signal': None,
						'score_buy': 0,
						'score_sell': 0
						}
					continue

			if flag_trade == 'sell':
				if bad_sell == True:

					#Chromosome.pop(chrom_counter)
					high_period = randint(5, 170)
					low_period = randint(5, 150)
					while high_period <= low_period + 10:
						high_period = randint(5, 170)
						low_period = randint(5, 150)

					#max_tp = randint(10, 80)/100
					#max_st = randint(10, 70)/100
					#while max_tp <= max_st:
						#max_tp = randint(10, 80)/100
						#max_st = randint(10, 70)/100

					Chromosome[chrom_counter] = {
						'high_period': Chromosome[chrom_counter]['high_period'],#high_period,
						'low_period': Chromosome[chrom_counter]['low_period'],#low_period,
						'distance_lines': randint(0, 6),
						'cross_line': randint(0, cross_line_upper_out_tester),
						#'max_st': max_st,
						#'max_tp': max_tp,
						'signal': None,
						'score_buy': 0,
						'score_sell': 0
						}
					continue

			if Chromosome[chrom_counter]['signal'] is None: continue

			chrom_counter += 1
			learning_interval_counter += 1
			if (chrom_counter >= ((len(Chromosome)))):
				chrom_counter = 0
				Chromosome = gen_creator(
										Chromosome=Chromosome,
										high_period_upper=high_period_upper,
										high_period_lower=high_period_lower,
										low_period_upper=low_period_upper,
										low_period_lower=low_period_lower
										)
				continue

			
	
	#**************************** Best Find *********************************************************

	#************ Buy Find:
	if flag_trade == 'buy':

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print('=======> Chorme ===> ')
			print()
			print('........................................................')
			print(chromosome_buy)
			print('........................................................')
			print()

		best_buy = pd.DataFrame()
		max_score_buy_pr = np.max(result_buy['score_pr'].dropna())
		max_score_buy_min_max = np.max(result_buy['score_min_max'].dropna())
		max_score_buy = max(max_score_buy_pr,max_score_buy_min_max)
		best_buy_score_index = np.where((result_buy['score_pr']==max_score_buy) | (result_buy['score_min_max'] == max_score_buy))[0]
		best_dict = dict()
		for idx in best_buy_score_index:
			for clm in result_buy.columns:
				best_dict.update(
					{
					clm: result_buy[clm][idx]
					})
			for clm in chromosome_buy.columns:
				best_dict.update(
					{
					clm: chromosome_buy[clm][idx]
					})

			best_buy = best_buy.append(best_dict, ignore_index=True)
	#//////////////////////
	#********** Sell Find:
	if flag_trade == 'sell':

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print('=======> Chorme ===> ')
			print()
			print('........................................................')
			print(chromosome_sell)
			print('........................................................')
			print()

		best_sell = pd.DataFrame()
		max_score_sell_pr = np.max(result_sell['score_pr'].dropna())
		max_score_sell_min_max = np.max(result_sell['score_min_max'].dropna())
		max_score_sell = max(max_score_sell_pr,max_score_sell_min_max)
		best_sell_score_index = np.where((result_sell['score_pr']==max_score_sell) | (result_sell['score_min_max'] == max_score_sell))[0]
		best_dict = dict()
		for idx in best_sell_score_index:
			for clm in result_sell.columns:
				best_dict.update(
					{
					clm: result_sell[clm][idx]
					})
			for clm in chromosome_sell.columns:
				best_dict.update(
					{
					clm: chromosome_sell[clm][idx]
					})

			best_sell = best_sell.append(best_dict, ignore_index=True)
	#//////////////////////

	#********************************///////////////****************************************************************

	#*************************** Save to TXT File ***************************************************************

	if flag_trade == 'buy':
		try:
			if os.path.exists("Genetic_cci_output_buy/"+symbol+'.csv'):
				os.remove("Genetic_cci_output_buy/"+symbol+'.csv')

			with open("Genetic_cci_output_buy/"+symbol+'.csv', 'w', newline='') as myfile:
				fields = best_buy.columns.to_list()
				writer = csv.DictWriter(myfile, fieldnames=fields)
				writer.writeheader()
	
				for idx in range(len(best_buy)):
					rows = dict()
					for clm in best_buy.columns:
						rows.update({clm: best_buy[clm][idx]})
					writer.writerow(rows)
					
		except Exception as ex:
			print('some thing wrong: ', ex)

	if flag_trade == 'sell':
		try:
			if os.path.exists("Genetic_cci_output_sell/"+symbol+'.csv'):
				os.remove("Genetic_cci_output_sell/"+symbol+'.csv')

			with open("Genetic_cci_output_sell/"+symbol+'.csv', 'w', newline='') as myfile:
				fields = best_sell.columns.to_list()
				writer = csv.DictWriter(myfile, fieldnames=fields)
				writer.writeheader()
	
				for idx in range(len(best_sell)):
					rows = dict()
					for clm in best_sell.columns:
						rows.update({clm: best_sell[clm][idx]})
					writer.writerow(rows)
					
		except Exception as ex:
			print('some thing wrong: ', ex)

	print('/////////////////////// Finish Genetic BUY ',symbol,'///////////////////////////////////')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#********************** read GA result ****************************************************************************

@stTime
def read_ga_result(symbol):
	buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
	sell_path = "Genetic_cci_output_sell/" + symbol + '.csv'
	if os.path.exists(buy_path):
		ga_result_buy = pd.read_csv(buy_path)
	else:
		ga_result_buy = pd.DataFrame()

	if os.path.exists(sell_path):
		ga_result_sell = pd.read_csv(sell_path)
	else:
		ga_result_sell = pd.DataFrame()

	return ga_result_buy, ga_result_sell
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#************************************ one year golden cross tester ***********************************************

#@stTime
def one_year_golden_cross_tester(
								dataset,
								dataset_15M,
								symbol_data_1H,
								symbol_data_4H,
								symbol,
								flag_trade,
								alfa = 0.1,
								max_st = 1,
								max_tp = 1,
								permit_flag=False
								):

	upper = 0
	mid = 1
	lower = 2

	print('=================> ',symbol)

	buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
	sell_path = "Genetic_cci_output_sell/" + symbol + '.csv'

	if os.path.exists(buy_path):
		ga_result_buy, ga_result_sell = read_ga_result(symbol=symbol)
	else:
		return 0
	#********************************************** Buy Test:

	if flag_trade == 'buy':
		if ga_result_buy['methode'][0] != 'no_trade':
			if ga_result_buy['methode'][0] == 'pr':
				name_stp_pr = True
				name_stp_minmax = False
			elif ga_result_buy['methode'][0] == 'min_max':
				name_stp_pr = False
				name_stp_minmax = True

			print('******************* BUY *************************')
			buy_data,_ = golden_cross_zero(
										dataset=dataset,
										dataset_15M=dataset_15M,
										dataset_1H=symbol_data_1H,
										dataset_4H=symbol_data_4H,
										symbol=symbol,
										Low_Period=ga_result_buy['low_period'][0],
										High_Period=ga_result_buy['high_period'][0],
										distance_lines=ga_result_buy['distance_lines'][0],
										cross_line=-ga_result_buy['cross_line'][0],
										mode='optimize',
										name_stp_minmax=name_stp_minmax,
										name_stp_pr=name_stp_pr,
										plot=False,
										pbar_flag=False,
										buy_flag=True,
										sell_flag=False,
										st_percent_minmax_buy= max_st,
										st_percent_minmax_sell=0,
										tp_percent_minmax_sell_min = 0,
										tp_percent_minmax_sell_max = 0,
										tp_percent_minmax_buy_min = 0,
										tp_percent_minmax_buy_max = max_tp
										)

		#*********************** Min Max Methode:

			if ga_result_buy['methode'][0] == 'min_max':
				#list_index_ok = range(0,len(buy_data))
				list_index_ok = np.where(
					#((buy_data['ramp_high'].to_numpy()>=ga_result_buy['ramp_high_lower_min_max'][0]))&
					#((buy_data['ramp_low'].to_numpy()>=ga_result_buy['ramp_low_lower_min_max'][0]))&
					#((buy_data['diff_min_max_cci'].to_numpy()<ga_result_buy['diff_min_max_cci_upper_min_max'][0]))&
					#((buy_data['diff_min_max_candle'].to_numpy()<=ga_result_buy['diff_min_max_candle_upper_min_max'][0]))&
					#((buy_data['value_max_cci'].to_numpy()>=ga_result_buy['value_max_lower_cci_min_max'][0]))
					((buy_data['value_min_cci'].to_numpy()<=ga_result_buy['value_min_upper_cci_min_max'][0]))
					)[0]

				output_buy = pd.DataFrame()
				output_buy['mean_tp_min_max'] = [np.mean(buy_data['tp_min_max'][list_index_ok])]
				output_buy['mean_st_min_max'] = [np.mean(buy_data['st_min_max'][list_index_ok])]
				output_buy['max_tp_min_max'] = [np.max(buy_data['tp_min_max'][list_index_ok])]
				output_buy['max_st_min_max'] = [np.max(buy_data['st_min_max'][list_index_ok])]

				try:
					output_buy['sum_st_min_max'] = [np.sum(buy_data['st_min_max'][list_index_ok[np.where(buy_data['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
					output_buy['sum_tp_min_max'] = [np.sum(buy_data['tp_min_max'][list_index_ok[np.where(buy_data['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
				except Exception as ex:
					print('tester minmax buy: ',ex)
					output_buy['sum_st_min_max'] = 0
					output_buy['sum_tp_min_max'] = 0

				tp_counter = 0
				st_counter = 0
				for elm in buy_data['flag_min_max'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_buy['num_tp_min_max'] = [tp_counter]
				output_buy['num_st_min_max'] = [st_counter]
				output_buy['num_trade_min_max'] = [st_counter + tp_counter]

				if output_buy['num_trade_min_max'][0] != 0:

					if output_buy['num_st_min_max'][0] != 0:
						score_num_tp = (tp_counter-output_buy['num_st_min_max'][0])

						if (tp_counter-output_buy['num_st_min_max'][0]) == 0:
							score_num_tp = 8

						if (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_buy['max_st_min_max'][0] != 0:

					score_max_tp = (output_buy['max_tp_min_max'][0]-output_buy['max_st_min_max'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1
				else:
					score_max_tp = output_buy['max_tp_min_max'][0]
					if (output_buy['max_tp_min_max'][0] != 0):
						score_max_tp = output_buy['max_tp_min_max'][0] * 10


				if (output_buy['mean_st_min_max'][0] != 0):

					score_mean_tp = (output_buy['mean_tp_min_max'][0]-output_buy['mean_st_min_max'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_buy['mean_tp_min_max'][0]
					if (output_buy['mean_tp_min_max'][0] != 0):
						score_mean_tp = output_buy['mean_tp_min_max'][0] * 10


				if (output_buy['sum_st_min_max'][0] != 0):

					score_sum_tp = (output_buy['sum_tp_min_max'][0]-output_buy['sum_st_min_max'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 0.1

				else:
					score_sum_tp = output_buy['sum_tp_min_max'][0]
					if (output_buy['sum_tp_min_max'][0] != 0):
						score_sum_tp = output_buy['sum_tp_min_max'][0] * 10

				output_buy['score_min_max'] = [(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_buy['score_min_max'][0]) : output_buy['score_min_max'][0] = 0

				print('=========> one year Buy: ',symbol)

				print('mean_tp_min_max= ',output_buy['mean_tp_min_max'][0])
				print('mean_st_min_max= ',output_buy['mean_st_min_max'][0])
				print('max_tp_min_max= ',output_buy['max_tp_min_max'][0])
				print('max_st_min_max= ',output_buy['max_st_min_max'][0])
				print('sum_st_min_max= ',output_buy['sum_st_min_max'][0])
				print('sum_tp_min_max= ',output_buy['sum_tp_min_max'][0])
				print('num_tp_min_max= ',output_buy['num_tp_min_max'][0])
				print('num_st_min_max= ',output_buy['num_st_min_max'][0])
				print('num_trade_min_max= ',output_buy['num_trade_min_max'][0])
				print('score_min_max= ',output_buy['score_min_max'][0])
				print('score_min_max ga= ',ga_result_buy['score_min_max'][0])

			#for idx in buy_data['tp_min_max'][np.where(buy_data['flag_min_max'] == 'tp')[0]]:
				#print('time tp = ',dataset[symbol]['time'][idx]))

			#for idx in buy_data['tp_min_max'][np.where(buy_data['flag_min_max'] == 'st')[0]]:
				#print('time st = ',dataset[symbol]['time'][idx]))


				if output_buy['score_min_max'][0] >= ga_result_buy['score_min_max'][0]:
					ga_result_buy['permit'] = True
					ga_result_buy.to_csv(buy_path)
				else:
					ga_result_buy['permit'] = False
					ga_result_buy.to_csv(buy_path)

		#////////////////////////////////////////////////////////////////

		#*********************** PR Methode:
			if ga_result_buy['methode'][0] == 'pr':

				value_min_cci_pr_buy = Find_Best_intervals(signals=buy_data,apply_to='value_min_cci',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				power_high_pr_buy = Find_Best_intervals(signals=buy_data,apply_to='power_pr_high',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				power_low_pr_buy = Find_Best_intervals(signals=buy_data,apply_to='power_pr_low',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				diff_top_pr_buy = Find_Best_intervals(signals=buy_data,apply_to='tp_pr',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				diff_down_pr_buy = Find_Best_intervals(signals=buy_data,apply_to='st_pr',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				print('value_min_cci_pr_buy = ',value_min_cci_pr_buy)
				print('power_high_pr_buy = ',power_high_pr_buy)
				print('power_low_pr_buy = ',power_low_pr_buy)
				print('diff_top_pr = ',diff_top_pr_buy)
				print('diff_down_pr = ',diff_down_pr_buy)

				list_index_ok = np.where(
					#((buy_data['ramp_low'].to_numpy()>=ga_result_buy['ramp_low_lower_pr'][0]))&
					#((buy_data['ramp_high'].to_numpy()>=ga_result_buy['ramp_high_lower_pr'][0]))&
					#((buy_data['diff_pr_top'].to_numpy()<=ga_result_buy['diff_top_upper_pr'][0]))
					#((buy_data['trend_long'].to_numpy()!='sell')&
					#((buy_data['trend_mid'].to_numpy()!='sell')&
					#(buy_data['trend_short1'].to_numpy()=='buy')&
					#(buy_data['trend_short2'].to_numpy()=='buy')))
					#((buy_data['diff_pr_down'].to_numpy()<=ga_result_buy['diff_down_upper_pr'][0]))&
					#(buy_data['diff_pr_top'].to_numpy() <= diff_top_pr['interval'][upper]) &
					#(buy_data['diff_pr_down'].to_numpy() >= diff_down_pr['interval'][lower]) &
					((buy_data['value_min_cci'].to_numpy()<=0))#value_min_cci_pr_buy['interval'][upper]))  #value_min_cci_pr_buy['interval'][upper]))
					#((buy_data['power_pr_high'].to_numpy()>=power_high_pr_buy['interval'][lower])) &
					#((buy_data['power_pr_low'].to_numpy()>=power_low_pr_buy['interval'][lower]))
					#((buy_data['value_max_cci'].to_numpy()>=ga_result_buy['value_max_lower_cci_pr'][0]))
					)[0]
				#print('list_index_ok = ',list_index_ok)
				#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
					#print('======== Output Buy =======> ')
					#print()
					#print('........................................................')
					#print(buy_data)
					#print('........................................................')
					#print()

				output_buy = pd.DataFrame()
				output_buy['mean_tp_pr'] = [np.mean(buy_data['tp_pr'][list_index_ok])]
				output_buy['mean_st_pr'] = [np.mean(buy_data['st_pr'][list_index_ok])]
				output_buy['max_tp_pr'] = [np.max(buy_data['tp_pr'][list_index_ok])]
				output_buy['max_st_pr'] = [np.max(buy_data['st_pr'][list_index_ok])]
				output_buy['sum_st_pr'] = [np.sum(buy_data['st_pr'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_buy['sum_tp_pr'] = [np.sum(buy_data['tp_pr'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'tp')[0]]].to_numpy())]
				output_buy['value_min_upper_cci_pr'] = [value_min_cci_pr_buy['interval'][upper]]
				output_buy['power_pr_high'] = [power_high_pr_buy['interval'][lower]]
				output_buy['power_pr_low'] = [power_low_pr_buy['interval'][lower]]
				output_buy['max_st'] = [diff_down_pr_buy['interval'][upper]]
				output_buy['max_tp'] = [diff_top_pr_buy['interval'][upper]]

				tp_counter = 0
				st_counter = 0
				for elm in buy_data['flag_pr'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_buy['num_tp_pr'] = [tp_counter]
				output_buy['num_st_pr'] = [st_counter]
				output_buy['num_trade_pr'] = [st_counter + tp_counter]
			

				if output_buy['num_trade_pr'][0] != 0:

					if output_buy['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_buy['num_st_pr'][0])

						if (tp_counter-output_buy['num_st_pr'][0]) == 0:
							score_num_tp = 8

						elif (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_buy['max_st_pr'][0] != 0:

					score_max_tp = (output_buy['max_tp_pr'][0]-output_buy['max_st_pr'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_buy['max_tp_pr'][0]
					if (output_buy['max_tp_pr'][0] != 0):
						score_max_tp = output_buy['max_tp_pr'][0] * 10

				if (output_buy['mean_st_pr'][0] != 0):

					score_mean_tp = (output_buy['mean_tp_pr'][0]-output_buy['mean_st_pr'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_buy['mean_tp_pr'][0]
					if (output_buy['mean_tp_pr'][0] != 0):
						score_mean_tp = output_buy['mean_tp_pr'][0] * 10

				if (output_buy['sum_st_pr'][0] != 0):

					score_sum_tp = (output_buy['sum_tp_pr'][0]-output_buy['sum_st_pr'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 0.1

				else:
					score_sum_tp = output_buy['sum_tp_pr'][0]
					if (output_buy['sum_tp_pr'][0] != 0):
						score_sum_tp = output_buy['sum_tp_pr'][0] * 10

				output_buy['score_pr'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_buy['score_pr'][0]) : output_buy['score_pr'][0] = 0

				print('=========> one year Buy: ',symbol)

				print('mean_tp_pr= ',output_buy['mean_tp_pr'][0])
				print('mean_st_pr= ',output_buy['mean_st_pr'][0])
				print('max_tp_pr= ',output_buy['max_tp_pr'][0])
				print('max_st_pr= ',output_buy['max_st_pr'][0])
				print('sum_st_pr= ',output_buy['sum_st_pr'][0])
				print('sum_tp_pr= ',output_buy['sum_tp_pr'][0])
				print('num_tp_pr= ',output_buy['num_tp_pr'][0])
				print('num_st_pr= ',output_buy['num_st_pr'][0])
				print('num_trade_pr= ',output_buy['num_trade_pr'][0])
				print('score_pr= ',output_buy['score_pr'][0])
				print('score_pr ga= ',ga_result_buy['score_pr'][0])
				print('value_min_cci_pr_buy = ',value_min_cci_pr_buy['interval'][upper])

				for idx in buy_data['index'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'tp')[0]]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in buy_data['index'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'st')[0]]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if permit_flag == True:
					if output_buy['score_pr'][0] >= ga_result_buy['score_pr'][0]*0.99: 
						ga_result_buy['permit'] = True
						#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

						if os.path.exists(buy_path):
							os.remove(buy_path)

						ga_result_buy.to_csv(buy_path)
					else:
						ga_result_buy['permit'] = False
						#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

						if os.path.exists(buy_path):
							os.remove(buy_path)

						ga_result_buy.to_csv(buy_path)

	#///////////////////////////////////////////////////////////////////////////////////////////////

	#********************************************** Sell Test:
	if flag_trade == 'sell':
		if ga_result_sell['methode'][0] != 'no_trade':
			if ga_result_sell['methode'][0] == 'pr':
				name_stp_pr = True
				name_stp_minmax = False
			elif ga_result_sell['methode'][0] == 'min_max':
				name_stp_pr = False
				name_stp_minmax = True

			print('******************* SELL *************************')

			_,sell_data = golden_cross_zero(
										dataset=dataset,
										dataset_15M=dataset_15M,
										dataset_1H=symbol_data_1H,
										dataset_4H=symbol_data_4H,
										symbol=symbol,
										Low_Period=ga_result_sell['low_period'][0],
										High_Period=ga_result_sell['high_period'][0],
										distance_lines=ga_result_sell['distance_lines'][0],
										cross_line=ga_result_sell['cross_line'][0],
										mode='optimize',
										name_stp_minmax=name_stp_minmax,
										name_stp_pr=name_stp_pr,
										plot=False,
										pbar_flag=False,
										sell_flag=True,
										buy_flag=False,
										st_percent_minmax_buy= 0,
										st_percent_minmax_sell= max_st,
										tp_percent_minmax_sell_min = 0,
										tp_percent_minmax_sell_max = max_tp,
										tp_percent_minmax_buy_min = 0,
										tp_percent_minmax_buy_max = 0
										)

			#*********************** Min Max Methode:
			if ga_result_sell['methode'][0] == 'min_max':
				#list_index_ok = range(0,len(sell_data))

				power_high_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='power_pr_high',
			 		min_tp=0.0, max_st=ga_result_sell['max_st'][0], name_stp='flag_pr',alpha=0.1)

				power_low_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='power_pr_low',
			 		min_tp=0.0, max_st=ga_result_sell['max_st'][0], name_stp='flag_pr',alpha=0.1)

				list_index_ok = np.where(
					#((sell_data['ramp_high'].to_numpy()<=ga_result_sell['ramp_high_upper_min_max'][0]))&
					#((sell_data['ramp_low'].to_numpy()<=ga_result_sell['ramp_low_upper_min_max'][0]))&
					#((sell_data['diff_min_max_cci'].to_numpy()<=ga_result_sell['diff_min_max_cci_upper_min_max'][0]))&
					#((sell_data['diff_min_max_candle'].to_numpy()<=ga_result_sell['diff_min_max_candle_upper_min_max'][0]))&
					#((sell_data['value_min_cci'].to_numpy()<=ga_result_sell['value_min_upper_cci_min_max'][0]))&
					((sell_data['value_max_cci'].to_numpy()>=ga_result_sell['value_max_lower_cci_min_max'][0])) &
					((sell_data['power_pr_high'].to_numpy()>=power_high_pr_sell['interval'][lower])) &
					((sell_data['power_pr_low'].to_numpy()>=power_low_pr_sell['interval'][lower]))
					)[0]

				output_sell = pd.DataFrame()
				output_sell['mean_tp_min_max'] = [np.mean(sell_data['tp_min_max'][list_index_ok])]
				output_sell['mean_st_min_max'] = [np.mean(sell_data['st_min_max'][list_index_ok])]
				output_sell['max_tp_min_max'] = [np.max(sell_data['tp_min_max'][list_index_ok])]
				output_sell['max_st_min_max'] = [np.max(sell_data['st_min_max'][list_index_ok])]

				try:
					output_sell['sum_st_min_max'] = [np.sum(sell_data['st_min_max'][list_index_ok[np.where(sell_data['flag_min_max'][list_index_ok] == 'st')[0]]].to_numpy())]
					output_sell['sum_tp_min_max'] = [np.sum(sell_data['tp_min_max'][list_index_ok[np.where(sell_data['flag_min_max'][list_index_ok] == 'tp')[0]]].to_numpy())]
				except Exception as ex:
					print('tester minmax sell: ',ex)
					output_sell['sum_st_min_max'] = 0
					output_sell['sum_tp_min_max'] = 0


				tp_counter = 0
				st_counter = 0
				for elm in sell_data['flag_min_max'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_sell['num_tp_min_max'] = [tp_counter]
				output_sell['num_st_min_max'] = [st_counter]
				output_sell['num_trade_min_max'] = [st_counter + tp_counter]

				if output_sell['num_trade_min_max'][0] != 0:

					if output_sell['num_st_min_max'][0] != 0:
						score_num_tp = (tp_counter-output_sell['num_st_min_max'][0])

						if (tp_counter-output_sell['num_st_min_max'][0]) == 0:
							score_num_tp = 8

						if (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_sell['max_st_min_max'][0] != 0:

					score_max_tp = (output_sell['max_tp_min_max'][0]-output_sell['max_st_min_max'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_sell['max_tp_min_max'][0]
					if (output_sell['max_tp_min_max'][0] != 0):
						score_max_tp = output_sell['max_tp_min_max'][0] * 10

				if (output_sell['mean_st_min_max'][0] != 0):

					score_mean_tp = (output_sell['mean_tp_min_max'][0]-output_sell['mean_st_min_max'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_sell['mean_tp_min_max'][0]
					if (output_sell['mean_tp_min_max'][0] != 0):
						score_mean_tp = output_sell['mean_tp_min_max'][0] * 10

				if (output_sell['sum_st_min_max'][0] != 0):

					score_sum_tp = (output_sell['sum_tp_min_max'][0]-output_sell['sum_st_min_max'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 0.1

				else:
					score_sum_tp = output_sell['sum_tp_min_max'][0]
					if (output_sell['sum_tp_min_max'][0] != 0):
						score_sum_tp = output_sell['sum_tp_min_max'][0] * 10

				output_sell['score_min_max'] = [(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_sell['score_min_max'][0]) : output_sell['score_min_max'][0] = 0

				print('=========> one year Sell: ',symbol)

				print('mean_tp_min_max= ',output_sell['mean_tp_min_max'][0])
				print('mean_st_min_max= ',output_sell['mean_st_min_max'][0])
				print('max_tp_min_max= ',output_sell['max_tp_min_max'][0])
				print('max_st_min_max= ',output_sell['max_st_min_max'][0])
				print('sum_st_min_max= ',output_sell['sum_st_min_max'][0])
				print('sum_tp_min_max= ',output_sell['sum_tp_min_max'][0])
				print('num_tp_min_max= ',output_sell['num_tp_min_max'][0])
				print('num_st_min_max= ',output_sell['num_st_min_max'][0])
				print('num_trade_min_max= ',output_sell['num_trade_min_max'][0])
				print('score_min_max= ',output_sell['score_min_max'][0])
				print('score_min_max ga= ',ga_result_sell['score_min_max'][0])

			#for idx in sell_data['index'][np.where(sell_data['flag_min_max'] == 'tp')[0]]:
				#print('time tp = ',dataset[symbol]['time'][idx]))

			#for idx in sell_data['index'][np.where(sell_data['flag_min_max'] == 'st')[0]]:
				#print('time st = ',dataset[symbol]['time'][idx]))

				if output_sell['score_min_max'][0] >= ga_result_sell['score_min_max'][0]: 
					ga_result_sell['permit'] = True
					ga_result_sell.to_csv(sell_path)
				else:
					ga_result_sell['permit'] = False
					ga_result_sell.to_csv(sell_path)

		#/////////////////////////////////////////

		#*********************** PR Methode:
			if ga_result_sell['methode'][0] == 'pr':

				value_max_cci_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='value_max_cci',
	 				min_tp=0.04, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				power_high_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='power_pr_high',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				power_low_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='power_pr_low',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				diff_top_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='diff_pr_top',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				diff_down_pr_sell = Find_Best_intervals(signals=sell_data,apply_to='diff_pr_down',
			 		min_tp=0.0, max_st=max_st, name_stp='flag_pr',alpha=alfa)

				list_index_ok = np.where(
					#((sell_data['ramp_low'].to_numpy()<=ga_result_sell['ramp_low_upper_pr'][0]))&
					#((sell_data['ramp_high'].to_numpy()<=ga_result_sell['ramp_high_upper_pr'][0]))&
					#((sell_data['diff_pr_top'].to_numpy()<=ga_result_sell['diff_top_upper_pr'][0]))&
					#((sell_data['diff_pr_down'].to_numpy()<=ga_result_sell['diff_down_upper_pr'][0]))
					#((sell_data['trend_long'].to_numpy()!='buy')&
					#((sell_data['trend_mid'].to_numpy()!='buy')&
					#(sell_data['trend_short1'].to_numpy()=='sell')&
					#(sell_data['trend_short2'].to_numpy()=='sell')))
					#((sell_data['diff_min_max_cci'].to_numpy()<=ga_result_sell['diff_min_max_cci_upper_pr'][0]))&
					#((sell_data['diff_min_max_candle'].to_numpy()<=ga_result_sell['diff_min_max_candle_upper_pr'][0]))&
					#((sell_data['value_min_cci'].to_numpy()<=ga_result_sell['value_min_upper_cci_pr'][0]))&
					((sell_data['value_max_cci'].to_numpy()>=value_max_cci_pr_sell['interval'][lower])) &#value_max_cci_pr_sell['interval'][lower]))
					((sell_data['power_pr_high'].to_numpy()>=power_high_pr_sell['interval'][lower])) &
					((sell_data['power_pr_low'].to_numpy()>=power_low_pr_sell['interval'][lower]))
					)[0]

				output_sell = pd.DataFrame()
				output_sell['mean_tp_pr'] = [np.mean(sell_data['tp_pr'][list_index_ok])]
				output_sell['mean_st_pr'] = [np.mean(sell_data['st_pr'][list_index_ok])]
				output_sell['max_tp_pr'] = [np.max(sell_data['tp_pr'][list_index_ok])]
				output_sell['max_st_pr'] = [np.max(sell_data['st_pr'][list_index_ok])]
				output_sell['sum_st_pr'] = [np.sum(sell_data['st_pr'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_sell['sum_tp_pr'] = [np.sum(sell_data['tp_pr'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'tp')[0]]].to_numpy())]
				output_sell['value_min_upper_cci_pr'] = [value_max_cci_pr_sell['interval'][lower]]
				output_sell['power_pr_high'] = [power_high_pr_sell['interval'][lower]]
				output_sell['power_pr_low'] = [power_low_pr_sell['interval'][lower]]
				output_sell['max_st'] = [diff_top_pr_sell['interval'][upper]]
				output_sell['max_tp'] = [diff_down_pr_sell['interval'][upper]]

				tp_counter = 0
				st_counter = 0
				for elm in sell_data['flag_pr'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_sell['num_tp_pr'] = [tp_counter]
				output_sell['num_st_pr'] = [st_counter]
				output_sell['num_trade_pr'] = [st_counter + tp_counter]

				if output_sell['num_trade_pr'][0] != 0:

					if output_sell['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_sell['num_st_pr'][0])

						if (tp_counter-output_sell['num_st_pr'][0]) == 0:
							score_num_tp = 8

						elif (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_sell['max_st_pr'][0] != 0:

					score_max_tp = (output_sell['max_tp_pr'][0]-output_sell['max_st_pr'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_sell['max_tp_pr'][0]
					if (output_sell['max_tp_pr'][0] != 0):
						score_max_tp = output_sell['max_tp_pr'][0] * 10

				if (output_sell['mean_st_pr'][0] != 0):

					score_mean_tp = (output_sell['mean_tp_pr'][0]-output_sell['mean_st_pr'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_sell['mean_tp_pr'][0]
					if (output_sell['mean_tp_pr'][0] != 0):
						score_mean_tp = output_sell['mean_tp_pr'][0] * 10

				if (output_sell['sum_st_pr'][0] != 0):

					score_sum_tp = (output_sell['sum_tp_pr'][0]-output_sell['sum_st_pr'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 0.1

				else:
					score_sum_tp = output_sell['sum_tp_pr'][0]
					if (output_sell['sum_tp_pr'][0] != 0):
						score_sum_tp = output_sell['sum_tp_pr'][0] * 10

				output_sell['score_pr'] = [(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_sell['score_pr'][0]) : output_sell['score_pr'][0] = 0

				print('=========> one year Sell: ',symbol)

				print('mean_tp_pr= ',output_sell['mean_tp_pr'][0])
				print('mean_st_pr= ',output_sell['mean_st_pr'][0])
				print('max_tp_pr= ',output_sell['max_tp_pr'][0])
				print('max_st_pr= ',output_sell['max_st_pr'][0])
				print('sum_st_pr= ',output_sell['sum_st_pr'][0])
				print('sum_tp_pr= ',output_sell['sum_tp_pr'][0])
				print('num_tp_pr= ',output_sell['num_tp_pr'][0])
				print('num_st_pr= ',output_sell['num_st_pr'][0])
				print('num_trade_pr= ',output_sell['num_trade_pr'][0])
				print('score_pr= ',output_sell['score_pr'][0])
				print('score_pr ga= ',ga_result_sell['score_pr'][0])
				print('value_max_cci_pr_sell = ',value_max_cci_pr_sell['interval'][lower])

				for idx in sell_data['index'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'tp')[0]]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in sell_data['index'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'st')[0]]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if permit_flag == True:
					if output_sell['score_pr'][0] >= ga_result_sell['score_pr'][0]*0.99:
						ga_result_sell['permit'] = True
						#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]

						if os.path.exists(sell_path):
							os.remove(sell_path)

						ga_result_sell.to_csv(sell_path)
					else:
						ga_result_sell['permit'] = False
						#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]
					
						if os.path.exists(sell_path):
							os.remove(sell_path)

						ga_result_sell.to_csv(sell_path)
		#////////////////////////////////////////
	print('//////////////////////////////////////////')

	if flag_trade == 'buy':
		output_sell = pd.DataFrame()

	if flag_trade == 'sell':
		output_buy = pd.DataFrame()

	return output_buy, output_sell

#///////////////////////////////////////////////////////////////////////////////////////////////////////

#*********************** Tester For Permit ***********************************


def golden_cross_tester_for_permit(
									dataset,
									dataset_15M,
									symbol_data_1H,
									symbol_data_4H,
									symbol,
									flag_trade,
									):

	upper = 0
	mid = 1
	lower = 2

	print('=================> ',symbol)

	buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
	sell_path = "Genetic_cci_output_sell/" + symbol + '.csv'

	if os.path.exists(buy_path):
		ga_result_buy, ga_result_sell = read_ga_result(symbol=symbol)
	else:
		return 0
	#********************************************** Buy Test:

	if ga_result_buy['methode'][0] != 'no_trade':
		if ga_result_buy['methode'][0] == 'pr':
			name_stp_pr = True
			name_stp_minmax = False
		elif ga_result_buy['methode'][0] == 'min_max':
			name_stp_pr = False
			name_stp_minmax = True

		if flag_trade == 'buy':
			print('******************* BUY *************************')
			buy_data,_ = golden_cross_zero(
										dataset=dataset,
										dataset_15M=dataset_15M,
										dataset_1H=symbol_data_1H,
										dataset_4H=symbol_data_4H,
										symbol=symbol,
										Low_Period=ga_result_buy['low_period'][0],
										High_Period=ga_result_buy['high_period'][0],
										distance_lines=ga_result_buy['distance_lines'][0],
										cross_line=-ga_result_buy['cross_line'][0],
										mode='optimize',
										name_stp_minmax=name_stp_minmax,
										name_stp_pr=name_stp_pr,
										plot=False,
										pbar_flag=True,
										buy_flag=True,
										sell_flag=False,
										st_percent_minmax_buy= ga_result_buy['max_st'][0],
										st_percent_minmax_sell=0,
										tp_percent_minmax_sell_min = 0,
										tp_percent_minmax_sell_max = 0,
										tp_percent_minmax_buy_min = 0,
										tp_percent_minmax_buy_max = ga_result_buy['max_tp'][0]
										)

			#*********************** PR Methode BUY:
			if ga_result_buy['methode'][0] == 'pr':

				output_sell = pd.DataFrame()

				list_index_ok = np.where(
					(buy_data['value_min_cci'].to_numpy()<=ga_result_buy['value_min_upper_cci_pr'][0]) &
					(buy_data['power_pr_high'].to_numpy()>=ga_result_buy['power_pr_high'][0]) &
					(buy_data['power_pr_low'].to_numpy()>=ga_result_buy['power_pr_low'][0])
					)[0]

				output_buy = pd.DataFrame()
				output_buy['mean_tp_pr'] = [np.mean(buy_data['tp_pr'][list_index_ok])]
				output_buy['mean_st_pr'] = [np.mean(buy_data['st_pr'][list_index_ok])]
				output_buy['max_tp_pr'] = [np.max(buy_data['tp_pr'][list_index_ok])]
				output_buy['max_st_pr'] = [np.max(buy_data['st_pr'][list_index_ok])]
				output_buy['sum_st_pr'] = [np.sum(buy_data['st_pr'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_buy['sum_tp_pr'] = [np.sum(buy_data['tp_pr'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'tp')[0]]].to_numpy())]

				tp_counter = 0
				st_counter = 0
				for elm in buy_data['flag_pr'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_buy['num_tp_pr'] = [tp_counter]
				output_buy['num_st_pr'] = [st_counter]
				output_buy['num_trade_pr'] = [st_counter + tp_counter]
			

				if output_buy['num_trade_pr'][0] != 0:

					if output_buy['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_buy['num_st_pr'][0])

						if (tp_counter-output_buy['num_st_pr'][0]) == 0:
							score_num_tp = 8

						elif (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_buy['max_st_pr'][0] != 0:

					score_max_tp = (output_buy['max_tp_pr'][0]-output_buy['max_st_pr'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_buy['max_tp_pr'][0]
					if (output_buy['max_tp_pr'][0] != 0):
						score_max_tp = output_buy['max_tp_pr'][0] * 10

				if (output_buy['mean_st_pr'][0] != 0):

					score_mean_tp = (output_buy['mean_tp_pr'][0]-output_buy['mean_st_pr'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_buy['mean_tp_pr'][0]
					if (output_buy['mean_tp_pr'][0] != 0):
						score_mean_tp = output_buy['mean_tp_pr'][0] * 10

				if (output_buy['sum_st_pr'][0] != 0):

					score_sum_tp = (output_buy['sum_tp_pr'][0]-output_buy['sum_st_pr'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 1

				else:
					score_sum_tp = output_buy['sum_tp_pr'][0]
					if (output_buy['sum_tp_pr'][0] != 0):
						score_sum_tp = output_buy['sum_tp_pr'][0] * 10

				output_buy['score_pr'] = [(score_num_tp*score_sum_tp)]#[(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_buy['score_pr'][0]) : output_buy['score_pr'][0] = 0

				print('=========> one year Buy: ',symbol)

				print('mean_tp_pr= ',output_buy['mean_tp_pr'][0])
				print('mean_st_pr= ',output_buy['mean_st_pr'][0])
				print('max_tp_pr= ',output_buy['max_tp_pr'][0])
				print('max_st_pr= ',output_buy['max_st_pr'][0])
				print('sum_st_pr= ',output_buy['sum_st_pr'][0])
				print('sum_tp_pr= ',output_buy['sum_tp_pr'][0])
				print('num_tp_pr= ',output_buy['num_tp_pr'][0])
				print('num_st_pr= ',output_buy['num_st_pr'][0])
				print('num_trade_pr= ',output_buy['num_trade_pr'][0])
				print('score_pr= ',output_buy['score_pr'][0])
				print('score_pr ga= ',ga_result_buy['score_pr'][0])

				for idx in buy_data['index'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'tp')[0]]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in buy_data['index'][list_index_ok[np.where(buy_data['flag_pr'][list_index_ok] == 'st')[0]]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if output_buy['score_pr'][0] >= ga_result_buy['score_pr'][0]*0.99: 
					ga_result_buy['permit'] = True
					#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

					if os.path.exists(buy_path):
						os.remove(buy_path)

					ga_result_buy.to_csv(buy_path)
				else:
					ga_result_buy['permit'] = False
					#ga_result_buy['max_st'][0] = value_min_cci_pr_buy['interval'][upper]

					if os.path.exists(buy_path):
						os.remove(buy_path)

					ga_result_buy.to_csv(buy_path)

	#///////////////////////////////////////////////////////////////////////////////////////////////

	#********************************************** Sell Test:
	if ga_result_sell['methode'][0] != 'no_trade':
		if ga_result_sell['methode'][0] == 'pr':
			name_stp_pr = True
			name_stp_minmax = False
		elif ga_result_sell['methode'][0] == 'min_max':
			name_stp_pr = False
			name_stp_minmax = True

		if flag_trade == 'sell':

			print('******************* SELL *************************')

			_,sell_data = golden_cross_zero(
										dataset=dataset,
										dataset_15M=dataset_15M,
										dataset_1H=symbol_data_1H,
										dataset_4H=symbol_data_4H,
										symbol=symbol,
										Low_Period=ga_result_sell['low_period'][0],
										High_Period=ga_result_sell['high_period'][0],
										distance_lines=ga_result_sell['distance_lines'][0],
										cross_line=ga_result_sell['cross_line'][0],
										mode='optimize',
										name_stp_minmax=name_stp_minmax,
										name_stp_pr=name_stp_pr,
										plot=False,
										pbar_flag=True,
										sell_flag=True,
										buy_flag=False,
										st_percent_minmax_buy= 0,
										st_percent_minmax_sell= ga_result_sell['max_st'][0],
										tp_percent_minmax_sell_min = 0,
										tp_percent_minmax_sell_max = ga_result_sell['max_tp'][0],
										tp_percent_minmax_buy_min = 0,
										tp_percent_minmax_buy_max = 0
										)

		#*********************** PR Methode:
			if ga_result_sell['methode'][0] == 'pr':

				output_sell = pd.DataFrame()

				list_index_ok = np.where(
					(sell_data['value_max_cci'].to_numpy()>=ga_result_sell['value_max_lower_cci_pr'][0]) &
					(sell_data['power_pr_high'].to_numpy()>=ga_result_sell['power_pr_high'][0]) &
					(sell_data['power_pr_low'].to_numpy()>=ga_result_sell['power_pr_low'][0])
					)[0]

				output_sell = pd.DataFrame()
				output_sell['mean_tp_pr'] = [np.mean(sell_data['tp_pr'][list_index_ok])]
				output_sell['mean_st_pr'] = [np.mean(sell_data['st_pr'][list_index_ok])]
				output_sell['max_tp_pr'] = [np.max(sell_data['tp_pr'][list_index_ok])]
				output_sell['max_st_pr'] = [np.max(sell_data['st_pr'][list_index_ok])]
				output_sell['sum_st_pr'] = [np.sum(sell_data['st_pr'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'st')[0]]].to_numpy())]
				output_sell['sum_tp_pr'] = [np.sum(sell_data['tp_pr'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'tp')[0]]].to_numpy())]

				tp_counter = 0
				st_counter = 0
				for elm in sell_data['flag_pr'][list_index_ok]:
					if (elm == 'tp'):
						tp_counter += 1
					if (elm == 'st'):
						st_counter += 1
				output_sell['num_tp_pr'] = [tp_counter]
				output_sell['num_st_pr'] = [st_counter]
				output_sell['num_trade_pr'] = [st_counter + tp_counter]

				if output_sell['num_trade_pr'][0] != 0:

					if output_sell['num_st_pr'][0] != 0:
						score_num_tp = (tp_counter-output_sell['num_st_pr'][0])

						if (tp_counter-output_sell['num_st_pr'][0]) == 0:
							score_num_tp = 8

						elif (score_num_tp > 0):
							score_num_tp = score_num_tp * 9
						else:
							score_num_tp = 1
					else:
						if tp_counter != 0:
							score_num_tp = tp_counter * 10
						else:
							score_num_tp = 1
				else:
					score_num_tp = 1

				if output_sell['max_st_pr'][0] != 0:

					score_max_tp = (output_sell['max_tp_pr'][0]-output_sell['max_st_pr'][0])

					if score_max_tp > 0:
						score_max_tp = score_max_tp * 9
					else:
						score_max_tp = 1

				else:
					score_max_tp = output_sell['max_tp_pr'][0]
					if (output_sell['max_tp_pr'][0] != 0):
						score_max_tp = output_sell['max_tp_pr'][0] * 10

				if (output_sell['mean_st_pr'][0] != 0):

					score_mean_tp = (output_sell['mean_tp_pr'][0]-output_sell['mean_st_pr'][0])

					if score_mean_tp > 0:
						score_mean_tp = score_mean_tp * 9
					else:
						score_mean_tp = 1

				else:
					score_mean_tp = output_sell['mean_tp_pr'][0]
					if (output_sell['mean_tp_pr'][0] != 0):
						score_mean_tp = output_sell['mean_tp_pr'][0] * 10

				if (output_sell['sum_st_pr'][0] != 0):

					score_sum_tp = (output_sell['sum_tp_pr'][0]-output_sell['sum_st_pr'][0])

					if score_sum_tp > 0:
						score_sum_tp = score_sum_tp * 9
					else:
						score_sum_tp = 1

				else:
					score_sum_tp = output_sell['sum_tp_pr'][0]
					if (output_sell['sum_tp_pr'][0] != 0):
						score_sum_tp = output_sell['sum_tp_pr'][0] * 10

				output_sell['score_pr'] = [(score_num_tp*score_max_tp*score_mean_tp*score_sum_tp)]

				if np.isnan(output_sell['score_pr'][0]) : output_sell['score_pr'][0] = 0

				print('=========> one year Sell: ',symbol)

				print('mean_tp_pr= ',output_sell['mean_tp_pr'][0])
				print('mean_st_pr= ',output_sell['mean_st_pr'][0])
				print('max_tp_pr= ',output_sell['max_tp_pr'][0])
				print('max_st_pr= ',output_sell['max_st_pr'][0])
				print('sum_st_pr= ',output_sell['sum_st_pr'][0])
				print('sum_tp_pr= ',output_sell['sum_tp_pr'][0])
				print('num_tp_pr= ',output_sell['num_tp_pr'][0])
				print('num_st_pr= ',output_sell['num_st_pr'][0])
				print('num_trade_pr= ',output_sell['num_trade_pr'][0])
				print('score_pr= ',output_sell['score_pr'][0])
				print('score_pr ga= ',ga_result_sell['score_pr'][0])

				for idx in sell_data['index'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'tp')[0]]]:
					print('time tp = ',dataset[symbol]['time'][idx])

				for idx in sell_data['index'][list_index_ok[np.where(sell_data['flag_pr'][list_index_ok] == 'st')[0]]]:
					print('time st = ',dataset[symbol]['time'][idx])

				if output_sell['score_pr'][0] >= ga_result_sell['score_pr'][0]*0.99:
					ga_result_sell['permit'] = True
					#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]

					if os.path.exists(sell_path):
						os.remove(sell_path)

					ga_result_sell.to_csv(sell_path)
				else:
					ga_result_sell['permit'] = False
					#ga_result_sell['max_st'][0] = value_max_cci_pr_sell['interval'][lower]
					
					if os.path.exists(sell_path):
						os.remove(sell_path)

					ga_result_sell.to_csv(sell_path)
		#////////////////////////////////////////
	print('//////////////////////////////////////////')

	if flag_trade == 'buy':
		output_sell = pd.DataFrame()

	if flag_trade == 'sell':
		output_buy = pd.DataFrame()

	return output_buy, output_sell

#///////////////////////////////////////////////////////////////////////////////////////////////////////

#******************************** Last Signal Out ******************************************************

#@stTime
def last_signal(dataset,dataset_15M,dataset_1H, dataset_4H,dataset_1D,symbol):
	""" Last signal out """
	buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
	sell_path = "Genetic_cci_output_sell/" + symbol + '.csv'
	resist = protect = 0


	if os.path.exists(buy_path):
		ga_result_buy = pd.read_csv(buy_path)
		ga_result_sell = pd.read_csv(sell_path)
	else:
		signal = 'no_trade'
		return signal, resist, protect

	#**************** Buy Check:
	if ga_result_buy['permit'][0]:
		
		cross_cut_len = 200
		cut_first = 0
		if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
			cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

		dataset_5M_cross = {
							symbol: dataset[symbol].copy()
							}

		dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3'])-1)].reset_index(drop=True)

		buy_data, _ = golden_cross_zero(
									dataset=dataset_5M_cross,
									dataset_15M=dataset_5M_cross,
									dataset_1H=dataset_1H,
									dataset_4H=dataset_4H,
									symbol=symbol,
									Low_Period=ga_result_buy['low_period'][0],
									High_Period=ga_result_buy['high_period'][0],
									distance_lines=ga_result_buy['distance_lines'][0],
									cross_line=-ga_result_buy['cross_line'][0],
									mode='online',
									name_stp_minmax=False,
									name_stp_pr=False,
									plot=False,
									pbar_flag=True,
									buy_flag=True,
									sell_flag=False,
									st_percent_minmax_buy= ga_result_buy['max_st'][0],
									st_percent_minmax_sell=0,
									tp_percent_minmax_sell_min = 0,
									tp_percent_minmax_sell_max = 0,
									tp_percent_minmax_buy_min = ga_result_buy['max_st'][0],
									tp_percent_minmax_buy_max = ga_result_buy['max_tp'][0]
									)
		if (buy_data.empty == False):
			lst_idx_buy = buy_data['index'].iloc[-1] + cut_first + 1
		else:
			lst_idx_buy = 0
	else:
		lst_idx_buy = 0
	#**************** Sell Check:
	if ga_result_sell['permit'][0]:

		cross_cut_len = 200
		cut_first = 0
		if (int(len(dataset[symbol]['low'])-1) > cross_cut_len):
			cut_first = int(len(dataset[symbol]['low'])-1) - cross_cut_len

		dataset_5M_cross = {
							symbol: dataset[symbol].copy()
							}

		dataset_5M_cross[symbol]['low'] = dataset_5M_cross[symbol]['low'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['low'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['high'] = dataset_5M_cross[symbol]['high'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['high'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['close'] = dataset_5M_cross[symbol]['close'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['close'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['open'] = dataset_5M_cross[symbol]['open'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['open'])-1)].reset_index(drop=True)
		dataset_5M_cross[symbol]['HLC/3'] = dataset_5M_cross[symbol]['HLC/3'].iloc[cut_first:int(len(dataset_5M_cross[symbol]['HLC/3'])-1)].reset_index(drop=True)

		_, sell_data = golden_cross_zero(
										dataset=dataset_5M_cross,
										dataset_15M=dataset_5M_cross,
										dataset_1H=dataset_1H,
										dataset_4H=dataset_4H,
										symbol=symbol,
										Low_Period=ga_result_sell['low_period'][0],
										High_Period=ga_result_sell['high_period'][0],
										distance_lines=ga_result_sell['distance_lines'][0],
										cross_line=ga_result_sell['cross_line'][0],
										mode='online',
										name_stp_minmax=False,
										name_stp_pr=False,
										plot=False,
										pbar_flag=False,
										sell_flag=True,
										buy_flag=False,
										st_percent_minmax_buy= 0,
										st_percent_minmax_sell=ga_result_sell['max_st'][0],
										tp_percent_minmax_sell_min = ga_result_sell['max_st'][0],
										tp_percent_minmax_sell_max = ga_result_sell['max_tp'][0],
										tp_percent_minmax_buy_min = 0,
										tp_percent_minmax_buy_max = 0
										)

		if (sell_data.empty == False):
			lst_idx_sell = sell_data['index'].iloc[-1] + cut_first + 1
		else:
			lst_idx_sell = 0
	else:
		lst_idx_sell = 0

	#***************** Calculate PR:
	

	#***** Last Signal:

	if lst_idx_buy > lst_idx_sell and (len(dataset[symbol]['close']) - 1 - lst_idx_buy) <= (ga_result_buy['distance_lines'][0] + 1):

		print('======> last signal buy ',symbol)
		print('dataset length: ',len(dataset[symbol]['close']))
		print('ga result buy: ',ga_result_buy['distance_lines'][0])
		print('ga result buy methode: ',ga_result_buy['methode'][0])
		print('last index: ',lst_idx_buy)
		

		if ga_result_buy['methode'][0] == 'pr':

			if ga_result_buy['methode'][0] == 'pr' and lst_idx_buy != 0:

				res_pro = pd.DataFrame()
				try:
					res_pro = protect_resist(
						T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,
						dataset_5M=dataset[symbol],
						dataset_15M=dataset_15M[symbol],
						dataset_1H=dataset_1H[symbol],
						dataset_4H=dataset_4H[symbol],
						dataset_1D=dataset_1D[symbol],
						plot=False
						)
				except:
					res_pro['high'] = 'nan'
					res_pro['low'] = 'nan'
					res_pro['power_high'] = 0
					res_pro['power_low'] = 0

				if (res_pro.empty == False):
					diff_pr_top_buy = (((res_pro['high'][0] * 0.9995) - dataset[symbol]['high'][lst_idx_buy])/dataset[symbol]['high'][lst_idx_buy]) * 100
					diff_pr_down_buy = ((dataset[symbol]['low'][lst_idx_buy] - (res_pro['low'][2] * 0.9995))/dataset[symbol]['low'][lst_idx_buy]) * 100
					diff_pr_top_buy_power = np.mean(res_pro['power_high'])
					diff_pr_down_buy_power = np.mean(res_pro['power_low'])

					trend_long_buy = res_pro['trend_long'][0].values[0]
					trend_mid_buy = res_pro['trend_mid'][0].values[0]
					trend_short_1_buy = res_pro['trend_short1'][0].values[0]
					trend_short_2_buy = res_pro['trend_short2'][0].values[0]

					if trend_long_buy is np.nan: trend_long_buy = 'parcham'
					if trend_mid_buy is np.nan: trend_mid_buy = 'parcham'
					if trend_short_1_buy is np.nan: trend_short_1_buy = 'parcham'
					if trend_short_2_buy is np.nan: trend_short_2_buy = 'parcham'

					resist_buy = (res_pro['high'][0] * 0.9995)
					protect_buy = (res_pro['low'][2] * 0.9995)

				else:
					diff_pr_top_buy = 0
					diff_pr_down_buy = 0
					diff_pr_top_buy_power = 0
					diff_pr_down_buy_power = 0

					resist_buy = 0
					protect_buy = 0

					trend_long_buy = 'no_flag'
					trend_mid_buy = 'no_flag'
					trend_short_1_buy = 'no_flag'
					trend_short_2_buy = 'no_flag'

			print('trend_long_buy: ',trend_long_buy)
			print('trend_mid_buy: ',trend_mid_buy)
			print('trend_short_1_buy: ',trend_short_1_buy)
			print('trend_short_2_buy: ',trend_short_2_buy)

			if (
				#buy_data['ramp_low'].iloc[-1]>=ga_result_buy['ramp_low_lower_pr'][0] and
				#buy_data['ramp_high'].iloc[-1]>=ga_result_buy['ramp_high_lower_pr'][0] and
				#diff_pr_top_buy <= ga_result_buy['diff_top_upper_pr'][0] and
				dataset[symbol]['high'].iloc[-1] < resist_buy and
				dataset[symbol]['low'].iloc[-1] > protect_buy and
				diff_pr_top_buy >= diff_pr_down_buy and
				diff_pr_down_buy <= 0.4 and
				((trend_long_buy != 'sell') and
				((trend_mid_buy != 'sell') and
				(trend_short_1_buy == 'buy') and
				(trend_short_2_buy == 'buy'))) 
				#diff_pr_down_buy<=ga_result_buy['diff_down_upper_pr'][0] and
				#buy_data['diff_min_max_cci'].iloc[-1]<=ga_result_buy['diff_min_max_cci_upper_pr'][0] and
				#buy_data['diff_min_max_candle'].iloc[-1]<=ga_result_buy['diff_min_max_candle_upper_pr'][0]
				):
				
				signal = 'buy'

			else:
				signal = 'no_trade'
				
		if ga_result_buy['methode'][0] == 'min_max':

			trend_sma_buy_5M = last_signal_sma(dataset[symbol], symbol)['signal'][0]
			trend_sma_buy_15M = last_signal_sma(dataset_15M[symbol], symbol)['signal'][0]

			print('trend_sma_buy: ',trend_sma_buy_5M)

			if (
				trend_sma_buy_5M == 'buy' and
				trend_sma_buy_15M == 'buy' and
				buy_data['value_min_max_candle'].iloc[-1] > dataset[symbol]['high'].iloc[-1]*1.0004 and
				buy_data['diff_min_max_candle'].iloc[-1]>= (buy_data['st_percent'].iloc[-1] + 0.04) and
				dataset[symbol]['low'].iloc[-1] > buy_data['st_point'].iloc[-1] and
				buy_data['value_min_cci'].iloc[-1] <= ga_result_buy['value_min_upper_cci_min_max'][0] and
				buy_data['value_max_cci'].iloc[-1] >= ga_result_buy['value_max_lower_cci_min_max'][0]
				#buy_data['ramp_high'].iloc[-1]>=ga_result_buy['ramp_high_lower_min_max'][0] and
				#buy_data['ramp_low'].iloc[-1]>=ga_result_buy['ramp_low_lower_min_max'][0] and
				#buy_data['diff_min_max_cci'].iloc[-1]<ga_result_buy['diff_min_max_cci_upper_min_max'][0] and
				#buy_data['diff_min_max_candle'].iloc[-1]<=ga_result_buy['diff_min_max_candle_upper_min_max'][0]
				):

				signal = 'buy'

				resist_buy = (1 + (buy_data['diff_min_max_candle'].iloc[-1]/100)) * dataset[symbol]['close'].iloc[-1]
				protect_buy = (buy_data['st_point'].iloc[-1] * 0.9994)



			else:
				signal = 'no_trade'
		print('================================')

	elif lst_idx_buy < lst_idx_sell and (len(dataset[symbol]['close']) - 1 - lst_idx_sell) <= (ga_result_sell['distance_lines'][0] + 1):

		print('======> last signal sell ',symbol)
		print('dataset length: ',len(dataset[symbol]['close']))
		print('ga result sell: ',ga_result_sell['distance_lines'][0])
		print('ga result sell methode: ',ga_result_sell['methode'][0])
		print('last index: ',lst_idx_sell)
		

		if ga_result_sell['methode'][0] == 'pr':

			if ga_result_sell['methode'][0] == 'pr' and lst_idx_sell != 0:

				res_pro = pd.DataFrame()
				try:
					res_pro = protect_resist(
						T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,
						dataset_5M=dataset[symbol],
						dataset_15M=dataset_15M[symbol],
						dataset_1H=dataset_1H[symbol],
						dataset_4H=dataset_4H[symbol],
						dataset_1D=dataset_1D[symbol],
						plot=False
						)
				except:
					res_pro['high'] = 'nan'
					res_pro['low'] = 'nan'
					res_pro['power_high'] = 0
					res_pro['power_low'] = 0

				if (res_pro.empty == False):
					diff_pr_top_sell = (((res_pro['high'][0] * 1.0005) - dataset[symbol]['high'][lst_idx_sell])/dataset[symbol]['high'][lst_idx_sell]) * 100
					diff_pr_down_sell = ((dataset[symbol]['low'][lst_idx_sell] - (res_pro['low'][0] * 1.0005))/dataset[symbol]['low'][lst_idx_sell]) * 100
					diff_pr_top_sell_power = np.mean(res_pro['power_high'])
					diff_pr_down_sell_power = np.mean(res_pro['power_low'])

					trend_long_sell = res_pro['trend_long'][0].values[0]
					trend_mid_sell = res_pro['trend_mid'][0].values[0]
					trend_short_1_sell = res_pro['trend_short1'][0].values[0]
					trend_short_2_sell = res_pro['trend_short2'][0].values[0]

					if trend_long_sell is np.nan: trend_long_sell = 'parcham'
					if trend_mid_sell is np.nan: trend_mid_sell = 'parcham'
					if trend_short_1_sell is np.nan: trend_short_1_sell = 'parcham'
					if trend_short_2_sell is np.nan: trend_short_2_sell = 'parcham'


					resist_sell = (res_pro['high'][0] * 1.0005)
					protect_sell = (res_pro['low'][2] * 1.0005)
				else:
					diff_pr_top_sell = 0
					diff_pr_down_sell = 0
					diff_pr_top_sell_power = 0
					diff_pr_down_sell_power = 0

					trend_long_sell = 'no_flag'
					trend_mid_sell = 'no_flag'
					trend_short_1_sell = 'no_flag'
					trend_short_2_sell = 'no_flag'

					resist_sell = 0
					protect_sell = 0

			print('trend_long_sell: ',trend_long_sell)
			print('trend_mid_sell: ',trend_mid_sell)
			print('trend_short_1_sell: ',trend_short_1_sell)
			print('trend_short_2_sell: ',trend_short_2_sell)
			if (
				#sell_data['ramp_low'].iloc[-1]<=ga_result_sell['ramp_low_upper_pr'][0] and
				#sell_data['ramp_high'].iloc[-1]<=ga_result_sell['ramp_high_upper_pr'][0] and
				#diff_pr_top_sell<=ga_result_sell['diff_top_upper_pr'][0] and
				#diff_pr_down_sell <= ga_result_sell['diff_down_upper_pr'][0] and
				dataset[symbol]['high'].iloc[-1] < resist_sell and
				dataset[symbol]['low'].iloc[-1] > protect_sell and
				diff_pr_down_sell >= diff_pr_top_sell and
				diff_pr_top_sell <= 0.4 and
				((trend_long_sell != 'buy') and
				((trend_mid_sell != 'buy') and
				(trend_short_1_sell == 'sell') and
				(trend_short_2_sell == 'sell')))  
				#sell_data['diff_min_max_cci'].iloc[-1]<=ga_result_sell['diff_min_max_cci_upper_pr'][0] and
				#sell_data['diff_min_max_candle'].iloc[-1]<=ga_result_sell['diff_min_max_candle_upper_pr'][0]
				):

				signal = 'sell'

			else:
				signal = 'no_trade'
				

		if ga_result_sell['methode'][0] == 'min_max':

			trend_sma_sell_5M = last_signal_sma(dataset[symbol],symbol)['signal'][0]
			trend_sma_sell_15M = last_signal_sma(dataset_15M[symbol], symbol)['signal'][0]

			print('trend_sma_sell_5M: ',trend_sma_sell_5M)

			if (
				trend_sma_sell_5M == 'sell' and
				trend_sma_sell_15M == 'sell' and
				sell_data['value_min_max_candle'].iloc[-1] < dataset[symbol]['low'].iloc[-1]*0.9994 and
				sell_data['diff_min_max_candle'].iloc[-1] >= sell_data['st_percent'].iloc[-1] and
				dataset[symbol]['high'].iloc[-1] < sell_data['st_point'].iloc[-1] and
				sell_data['value_min_cci'].iloc[-1] <= ga_result_sell['value_min_upper_cci_min_max'][0] and
				sell_data['value_max_cci'].iloc[-1] >= ga_result_sell['value_max_lower_cci_min_max'][0]
				#sell_data['ramp_high'].iloc[-1]<=ga_result_sell['ramp_high_upper_min_max'][0] and
				#sell_data['ramp_low'].iloc[-1]<=ga_result_sell['ramp_low_upper_min_max'][0] and
				#sell_data['diff_min_max_cci'].iloc[-1]<=ga_result_sell['diff_min_max_cci_upper_min_max'][0] and
				#sell_data['diff_min_max_candle'].iloc[-1]<=ga_result_sell['diff_min_max_candle_upper_min_max'][0]
				):

				signal = 'sell'
				resist_sell = (sell_data['st_point'].iloc[-1] * 1.0006)
				protect_sell = (1 - (sell_data['diff_min_max_candle'].iloc[-1]/100)) * dataset[symbol]['close'].iloc[-1]

			else:
				signal = 'no_trade'

		print('================================')
	else:
		signal = 'no_trade'

	if signal == 'buy':
		return signal, resist_buy, protect_buy
	elif signal == 'sell':
		return signal, protect_sell, resist_sell
	else:
		return signal, 0, 0

#//////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************** CPU And Memory Limit Usage *********************************************



#/////////////////////////////////////////////////////////////////////////////////////////////////////

#*************************** How To Use Funcs *****************************************
"""
symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																							sym='GBPUSD_i',
																							num_5M=10,
																							num_15M=10,
																							num_1H=1,
																							num_4H=4
																							)

print('data get')

#last_signal(
	#dataset=symbol_data_5M,
	#dataset_15M=symbol_data_5M,
	#dataset_1H=symbol_data_5M,
	#dataset_4H=symbol_data_5M,
	#dataset_1D=symbol_data_5M,
	#symbol='AUDCAD_i'
	#)

symbol_black_list = np.array(
	[
		'WSt30_m_i','SPX500_m_i','NQ100_m_i','GER40_m_i',
		'GER40_i','USDRUR','USDRUR_i','USDRUB','USDRUB_i',
		'USDHKD','WTI_i','BRN_i','STOXX50_i','NQ100_i',
		'NG_i','HSI50_i','CAC40_i','ASX200_i','SPX500_i',
		'NIKK225_i','IBEX35_i','FTSE100_i','RUBRUR',
		'EURDKK_i','DAX30_i','XRPUSD_i','XBNUSD_i',
		'LTCUSD_i','ETHUSD_i','BTCUSD_i','_DXY','_DJI',
		'EURTRY_i','USDTRY_i','USDDKK_i','EURRUB_i'
	])

for sym in symbol:
	if np.where(sym.name == symbol_black_list)[0].size != 0: continue
	#if os.path.exists("Genetic_cci_output_buy/"+sym.name+'.csv'): continue
	#if os.path.exists("Genetic_cci_output_sell/"+sym.name+'.csv'): continue

	if not (
		sym.name == 'AUDCAD_i' or
		sym.name == 'AUDCHF_i' or
		sym.name == 'AUDUSD_i' or
		sym.name == 'CADJPY_i' or
		sym.name == 'EURAUD_i' or
		sym.name == 'EURCAD_i' or
		sym.name == 'EURCHF_i' or
		sym.name == 'EURGBP_i' or
		sym.name == 'EURUSD_i' or
		sym.name == 'EURJPY_i' or
		sym.name == 'GBPAUD_i' or
		sym.name == 'GBPCAD_i' or
		sym.name == 'GBPJPY_i' or
		sym.name == 'GBPUSD_i' or
		sym.name == 'USDJPY_i' or
		sym.name == 'USDCAD_i' or
		sym.name == 'XAUUSD_i'
		): continue

	if sym.name == 'GBPUSD_i': continue
	if sym.name == 'EURUSD_i': continue
	break

	symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																							sym=sym.name,
																							num_5M=10,
																							num_15M=10,
																							num_1H=1,
																							num_4H=4
																							)

	try:
		#genetic_buy_algo(
				#symbol_data_5M=symbol_data_5M,
				#symbol_data_15M=symbol_data_15M,
				#dataset_1H=symbol_data_1H,
				#dataset_4H=symbol_data_4H,
				#symbol=sym.name,
				#num_turn=200,
				#max_score_ga_buy=2,
				#max_score_ga_sell=2
				#)
		pass
	except Exception as ex:
		print('getting error: ', ex)

#symbol_data_5M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,6000)
#symbol_data_15M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,2000)
#symbol_data_1H,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,500)
#symbol_data_4H,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,400)
print('gotwarara 2')

for sym in symbol:
	if np.where(sym.name == symbol_black_list)[0].size != 0: continue
	
	if not (
		sym.name == 'AUDCAD_i' or
		sym.name == 'AUDCHF_i' or
		sym.name == 'AUDUSD_i' or
		sym.name == 'CADJPY_i' or
		sym.name == 'EURAUD_i' or
		sym.name == 'EURCAD_i' or
		sym.name == 'EURCHF_i' or
		sym.name == 'EURGBP_i' or
		sym.name == 'EURUSD_i' or
		sym.name == 'EURJPY_i' or
		sym.name == 'GBPAUD_i' or
		sym.name == 'GBPCAD_i' or
		sym.name == 'GBPJPY_i' or
		sym.name == 'GBPUSD_i' or
		sym.name == 'USDJPY_i' or
		sym.name == 'USDCAD_i' or
		sym.name == 'XAUUSD_i'
		): continue

	#if sym.name == 'AUDCAD_i': continue
	#if sym.name == 'AUDCHF_i': continue
	#if sym.name == 'AUDJPY_i': continue
	#if sym.name == 'AUDNZD_i': continue
	#if sym.name == 'AUDUSD_i': continue
	#if sym.name == 'CADCHF_i': continue
	#if sym.name == 'CADJPY_i': continue
	#if sym.name == 'CHFJPY_i': continue
	#if sym.name == 'EURAUD_i': continue
	#if sym.name == 'EURCAD_i': continue
	#if sym.name == 'EURCHF_i': continue
	break
	symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																							sym=sym.name,
																							num_5M=10,
																							num_15M=10,
																							num_1H=1,
																							num_4H=1
																							)

	
	print('****************************** ',sym.name,' ******************************')
	#one_year_golden_cross_tester(
								#dataset=symbol_data_5M,
								#dataset_15M=symbol_data_15M,
								#symbol_data_1H=symbol_data_1H,
								#symbol_data_4H=symbol_data_4H,
								#symbol=sym.name
								#)
#print(last_signal(dataset=symbol_data_5M,dataset_15M=symbol_data_15M,symbol='AUDCAD_i'))

syms = 'EURUSD_i'

symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbol = read_dataset_csv(
																							sym=syms,
																							num_5M=3000,
																							num_15M=1000,
																							num_1H=8000,
																							num_4H=1
																							)

#mem_data = pd.DataFrame()
#mem_data = mem_data.append(symbol_data_5M,ignore_index=True)
#print(mem_data)
#print(mem_data.info(memory_usage='deep'))

upper = 0
mid = 1
lower = 2



buy_path = "Genetic_cci_output_buy/" + syms + '.csv'
sell_path = "Genetic_cci_output_sell/" + syms + '.csv'

if os.path.exists(buy_path):
	ga_result_buy, ga_result_sell = read_ga_result(symbol=syms)
else:
	pass

signal_buy,_ = golden_cross_zero(
								dataset=symbol_data_5M,
								dataset_15M=symbol_data_15M,
								dataset_1H=symbol_data_1H,
								dataset_4H=symbol_data_1H,
								symbol=syms,
								Low_Period=50,
								High_Period=ga_result_buy['high_period'][0],
								distance_lines=ga_result_buy['distance_lines'][0],
								cross_line=-ga_result_buy['cross_line'][0],
								mode='optimize',
								name_stp_minmax=False,
								name_stp_pr=True,
								plot=False,
								pbar_flag=True,
								buy_flag=True,
								sell_flag=False,
								st_percent_minmax_buy= ga_result_buy['max_st'][0],
								st_percent_minmax_sell=0,
								tp_percent_minmax_sell_min = 0,
								tp_percent_minmax_sell_max = 0,
								tp_percent_minmax_buy_min = ga_result_buy['max_st'][0],
								tp_percent_minmax_buy_max = ga_result_buy['max_tp'][0]
								)

_,signal_sell = golden_cross_zero(
								dataset=symbol_data_5M,
								dataset_15M=symbol_data_15M,
								dataset_1H=symbol_data_1H,
								dataset_4H=symbol_data_4H,
								symbol=syms,
								Low_Period=50,
								High_Period=ga_result_sell['high_period'][0],
								distance_lines=ga_result_sell['distance_lines'][0],
								cross_line=ga_result_sell['cross_line'][0],
								mode='optimize',
								name_stp_minmax=False,
								name_stp_pr=True,
								plot=False,
								pbar_flag=True,
								sell_flag=True,
								buy_flag=False,
								st_percent_minmax_buy= 0,
								st_percent_minmax_sell=ga_result_sell['max_st'][0],
								tp_percent_minmax_sell_min = ga_result_sell['max_st'][0],
								tp_percent_minmax_sell_max = ga_result_sell['max_tp'][0],
								tp_percent_minmax_buy_min = 0,
								tp_percent_minmax_buy_max = 0
								)

print('buy =====> ',signal_buy)
print('sell =====> ',signal_sell)

#print('===========> without filters MinMax Buy: ')
#print('mean tp = ',np.mean(signal_buy['tp_min_max']))
#print('mean st = ',np.mean(signal_buy['st_min_max']))
#print('max tp = ',np.max(signal_buy['tp_min_max']))
#print('max st = ',np.max(signal_buy['st_min_max']))
#print('sum st = ',np.sum(signal_buy['st_min_max'][np.where(signal_buy['flag_min_max'] == 'st')[0]].to_numpy()))
#print('sum tp = ',np.sum(signal_buy['tp_min_max'][np.where(signal_buy['flag_min_max'] == 'tp')[0]].to_numpy()))

#tp_counter = 0
#st_counter = 0
#for elm in signal_buy['flag_min_max']:
	#if (elm == 'tp'):
		#tp_counter += 1
	#if (elm == 'st'):
		#st_counter += 1

#print('tp = ',tp_counter)
#print('st = ',st_counter)
#print('full = ',st_counter + tp_counter)

#print('===========> without filters MinMax Sell: ')
#print('mean tp = ',np.mean(signal_sell['tp_min_max']))
#print('mean st = ',np.mean(signal_sell['st_min_max']))
#print('max tp = ',np.max(signal_sell['tp_min_max']))
#print('max st = ',np.max(signal_sell['st_min_max']))
#print('sum st = ',np.sum(signal_sell['st_min_max'][np.where(signal_sell['flag_min_max'] == 'st')[0]].to_numpy()))
#print('sum tp = ',np.sum(signal_sell['tp_min_max'][np.where(signal_sell['flag_min_max'] == 'tp')[0]].to_numpy()))

#tp_counter = 0
#st_counter = 0
#for elm in signal_sell['flag_min_max']:
	#if (elm == 'tp'):
		#tp_counter += 1
	#if (elm == 'st'):
		#st_counter += 1

#print('tp = ',tp_counter)
#print('st = ',st_counter)
#print('full = ',st_counter + tp_counter)

print('============> PR Buy: ')

print('mean tp = ',np.mean(signal_buy['tp_pr']))
print('mean st = ',np.mean(signal_buy['st_pr']))
print('max tp = ',np.max(signal_buy['tp_pr']))
print('max st = ',np.max(signal_buy['st_pr']))
print('sum st = ',np.sum(signal_buy['st_pr'][np.where(signal_buy['flag_pr'] == 'st')[0]].to_numpy()))
print('sum tp = ',np.sum(signal_buy['tp_pr'][np.where(signal_buy['flag_pr'] == 'tp')[0]].to_numpy()))
	
tp_counter = 0
st_counter = 0
for elm in signal_buy['flag_pr']:
	if (elm == 'tp'):
		tp_counter += 1
	if (elm == 'st'):
		st_counter += 1
print('tp = ',tp_counter)
print('st = ',st_counter)
print('full = ',st_counter + tp_counter)

print('============> PR Sell: ')

print('mean tp = ',np.mean(signal_sell['tp_pr']))
print('mean st = ',np.mean(signal_sell['st_pr']))
print('max tp = ',np.max(signal_sell['tp_pr']))
print('max st = ',np.max(signal_sell['st_pr']))
print('sum st = ',np.sum(signal_sell['st_pr'][np.where(signal_sell['flag_pr'] == 'st')[0]].to_numpy()))
print('sum tp = ',np.sum(signal_sell['tp_pr'][np.where(signal_sell['flag_pr'] == 'tp')[0]].to_numpy()))
	
tp_counter = 0
st_counter = 0
for elm in signal_sell['flag_pr']:
	if (elm == 'tp'):
		tp_counter += 1
	if (elm == 'st'):
		st_counter += 1
print('tp = ',tp_counter)
print('st = ',st_counter)
print('full = ',st_counter + tp_counter)


for elm in signal_buy['index'][list_index_ok[0] + np.where(signal_buy['flag_pr'][list_index_ok] == 'tp')[0]]:
	
	plt.axvline(x = elm, color='g', linestyle='-')
	plt.axhline(y = signal_buy['tp_line'][list_index_ok[0] + np.where(signal_buy['index'][list_index_ok] == elm )[0]].values, color='g', linestyle='-')
	plt.axhline(y = signal_buy['st_line'][list_index_ok[0] + np.where(signal_buy['index'][list_index_ok] == elm )[0]].values, color='r', linestyle='-')
	elm = int(elm)
	plt.plot(range(elm-50,elm+150),symbol_data_5M[syms]['close'][elm-50:elm+150],c='b')
	plt.show()

for elm in signal_buy['index'][list_index_ok[0] + np.where(signal_buy['flag_pr'][list_index_ok] == 'st')[0]]:
	plt.axvline(x = elm, color='r', linestyle='-')
	plt.axhline(y = signal_buy['tp_line'][list_index_ok[0] + np.where(signal_buy['index'][list_index_ok] == elm )[0]].values, color='g', linestyle='-')
	plt.axhline(y = signal_buy['st_line'][list_index_ok[0] + np.where(signal_buy['index'][list_index_ok] == elm )[0]].values, color='r', linestyle='-')
	elm = int(elm)
	plt.plot(range(elm-50,elm+150),symbol_data_5M[syms]['close'][elm-50:elm+150],c='b')
	plt.show()
	
"""
