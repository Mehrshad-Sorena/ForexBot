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
from progress.bar import Bar


# Create a DataFrame so 'ta' can be used.
#df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ind.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
#help(ind.cci)

#**************************************************** High Low Toucehd *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Ramp Lines Toucehd *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#**************************************************** Divergence *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Golden Cross Zero *******************************************************
def golden_cross_zero(dataset,dataset_15M,symbol,Low_Period=25,High_Period=50,distance_lines=2,mode='online',name_stp_minmax=True,name_stp_pr=False,plot=False):
	x = np.arange(0,len(dataset[symbol]['HLC/3']),1)

	CCI_Low = ind.cci(high=dataset[symbol]['high'], low=dataset[symbol]['low'], close=dataset[symbol]['close'], length = Low_Period)
	CCI_High = ind.cci(high=dataset[symbol]['high'], low=dataset[symbol]['low'], close=dataset[symbol]['close'], length = High_Period)

	zero_line = pd.DataFrame(np.zeros(len(x)))

	#****************** Finding Low Period Cross With Zero Line ************************
	first_line = LineString(np.column_stack((x[(High_Period-1):], CCI_Low[(High_Period-1):])))
	second_line = LineString(np.column_stack((x[(High_Period-1):], zero_line[(High_Period-1):])))

	intersection_low = first_line.intersection(second_line)

	if intersection_low.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection_low).xy)
		cross_index = cross.index.to_numpy()
		cross_low = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_low['index'] = cross.values.astype(int)
		cross_low['values'] = cross_index

		if (plot == True):
			plt.plot(cross_low['index'],cross_low['values'], 'o',c='g')
    
	elif intersection_low.geom_type == 'Point':
		cross = pd.DataFrame(*intersection_low.xy)
		cross_index = cross.index.to_numpy()
		cross_low = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_low['index'] = cross.values.astype(int)
		cross_low['values'] = cross_index

		if (plot == True):
			plt.plot(cross_low['index'],cross_low['values'], 'o',c='g')

	#///////////////////////////////////////////////////////////////////////////////////

	#****************** Finding High Period Cross With Zero Line ************************
	first_line = LineString(np.column_stack((x[(High_Period-1):], CCI_High.dropna())))
	second_line = LineString(np.column_stack((x[(High_Period-1):], zero_line[(High_Period-1):])))

	intersection_high = first_line.intersection(second_line)

	if intersection_high.geom_type == 'MultiPoint':
		cross = pd.DataFrame(*LineString(intersection_high).xy)
		cross_index = cross.index.to_numpy()
		cross_high = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_high['index'] = cross.values.astype(int)
		cross_high['values'] = cross_index

		if (plot == True):
			plt.plot(cross_high['index'],cross_high['values'], 'o',c='g')
    
	elif intersection_high.geom_type == 'Point':
		cross = pd.DataFrame(*intersection_high.xy)
		cross_index = cross.index.to_numpy()
		cross_high = pd.DataFrame(cross.values.astype(int),columns=['index'])
		cross_high['index'] = cross.values.astype(int)
		cross_high['values'] = cross_index

		if (plot == True):
			plt.plot(cross_high['index'],cross_high['values'], 'o',c='g')

	#///////////////////////////////////////////////////////////////////////////////////

	#print('high = ',cross_high)
	#print('low = ',cross_low)

	i = 0
	finding_points = pd.DataFrame(np.zeros(len(CCI_Low)))
	finding_points['index'] = np.nan

	for elm in cross_high.index:
		points = cross_low['index'][np.where(abs(cross_low['index'] - cross_high['index'][elm]) <= distance_lines)[0]]
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

		signal_sell = pd.DataFrame(np.zeros(len(finding_points)))
		signal_sell['signal'] = np.nan
		signal_sell['index'] = np.nan
		signal_sell['ramp_low'] = np.nan
		signal_sell['ramp_high'] = np.nan
		signal_sell['diff_min_max_cci'] = np.nan
		signal_sell['diff_min_max_candle'] = np.nan
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

	buy_counter = 0
	sell_counter = 0

	for elm in finding_points.index:

		if (plot == True):
			plt.axvline(x=finding_points['index'][elm],c='r')

		if (elm-2 < 0): continue
		#******************** Buy Signal Finding *********************************
		if ((CCI_Low[finding_points['index'][elm]] > CCI_Low[finding_points['index'][elm]-1]) &
			(CCI_High[finding_points['index'][elm]] > CCI_High[finding_points['index'][elm]-1])):
			signal_buy['signal'][buy_counter] = 'buy'
			signal_buy['index'][buy_counter] = finding_points['index'][elm]
			signal_buy['ramp_low'][buy_counter] = CCI_Low[finding_points['index'][elm]] - CCI_Low[finding_points['index'][elm]-1]
			signal_buy['ramp_high'][buy_counter] = CCI_High[finding_points['index'][elm]] - CCI_High[finding_points['index'][elm]-1]
			signal_buy['diff_min_max_cci'][buy_counter] = np.max(CCI_High[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
			signal_buy['diff_min_max_candle'][buy_counter] = np.max(dataset[symbol]['high'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])


			#Calculate porfits
			#must read protect and resist from protect resist function
			if (mode == 'optimize'):

				if (name_stp_minmax == True):
					#Calculate With Min Max Diff From MACD:
					if ((len(np.where(dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values >= signal_buy['diff_min_max_candle'][buy_counter])[0]) - 1) > 1):
						signal_buy['tp_min_max_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where(dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values >= signal_buy['diff_min_max_candle'][buy_counter])[0])
						signal_buy['tp_min_max'][buy_counter] = ((dataset[symbol]['high'][signal_buy['tp_min_max_index'][buy_counter]] - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
					else:
						signal_buy['tp_min_max_index'][buy_counter] = -1
						signal_buy['tp_min_max'][buy_counter] = 0

					if ((len(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (dataset[symbol]['low'][int(finding_points['index'][elm])] * 0.9994)))[0])-1) > 1):
						signal_buy['st_min_max_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (dataset[symbol]['low'][int(finding_points['index'][elm])] * 0.9994)))[0])
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
					#///////////////////////////////////////////////////
				if (name_stp_pr == True):
					#Calculate ST and TP With Protect Resist Function
					dataset_pr_5M = pd.DataFrame()
					dataset_pr_15M = pd.DataFrame()
					cut_first = 0
					if (int(finding_points['index'][elm]) > 2000):
						cut_first = int(finding_points['index'][elm]) - 2000
					dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

					dataset_pr_15M['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)

					res_pro = pd.DataFrame()
					
					try:
						res_pro = protect_resist(T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,dataset_5M=dataset_pr_5M,dataset_15M=dataset_pr_15M,dataset_1H=dataset_pr_15M,dataset_4H=dataset_pr_5M,dataset_1D=dataset_pr_5M,plot=False)
					except:
						res_pro['high'] = 'nan'
						res_pro['low'] = 'nan'

					if (res_pro.empty == False):
						signal_buy['diff_pr_top'][buy_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
						signal_buy['diff_pr_down'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - (res_pro['low'][2] * 0.9994))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

						if ((len(np.where(((dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values) >= (res_pro['high'][0] * 0.9994)))[0]) - 1) > 1):
							signal_buy['tp_pr_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where(((dataset[symbol]['high'][int(finding_points['index'][elm]):-1].values) >= (res_pro['high'][0] * 0.9994)))[0])
							signal_buy['tp_pr'][buy_counter] = ((dataset[symbol]['high'][signal_buy['tp_pr_index'][buy_counter]] - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
						else:
							signal_buy['tp_pr_index'][buy_counter] = -1
							signal_buy['tp_pr'][buy_counter] = 0

						if ((len(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])-1) > 1):
							signal_buy['st_pr_index'][buy_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['low'][int(finding_points['index'][elm]):-1]).values) <= (res_pro['low'][2] * 0.9994)))[0])
							signal_buy['st_pr'][buy_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][signal_buy['st_pr_index'][buy_counter]])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
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
					#///////////////////////////////////////////////////

			buy_counter += 1
		#///////////////////////////////////////////////////////////////////////

		#************************ Sell Signal Finding *****************************
		if ((CCI_Low[finding_points['index'][elm]] < CCI_Low[finding_points['index'][elm]-1]) &
			(CCI_High[finding_points['index'][elm]] < CCI_High[finding_points['index'][elm]-1])):
			signal_sell['signal'][sell_counter] = 'sell'
			signal_sell['index'][sell_counter] = finding_points['index'][elm]
			signal_sell['ramp_low'][sell_counter] = CCI_Low[finding_points['index'][elm]] - CCI_Low[finding_points['index'][elm]-1]
			signal_sell['ramp_high'][sell_counter] = CCI_High[finding_points['index'][elm]] - CCI_High[finding_points['index'][elm]-1]
			signal_sell['diff_min_max_cci'][sell_counter] = np.max(CCI_High[int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])
			signal_sell['diff_min_max_candle'][sell_counter] = np.max(dataset[symbol]['high'][int(finding_points['index'][elm-2]):int(finding_points['index'][elm])])

			#Calculate porfits
			#must read protect and resist from protect resist function
			if (mode == 'optimize'):

				if (name_stp_minmax == True):
					#Calculate With Min Max Diff From MACD:

					if ((len(np.where((((((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][int(finding_points['index'][elm]):-1])/dataset[symbol]['low'][int(finding_points['index'][elm])]).values) * 100) >= (signal_sell['diff_min_max_candle'][sell_counter])))[0]) - 1) > 1):
						signal_sell['tp_min_max_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][int(finding_points['index'][elm]):-1])/dataset[symbol]['low'][int(finding_points['index'][elm])]).values) * 100) >= (signal_sell['diff_min_max_candle'][sell_counter])))[0])
						signal_sell['tp_min_max'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][signal_sell['tp_min_max_index'][sell_counter]])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
					else:
						signal_sell['tp_min_max_index'][sell_counter] = -1
						signal_sell['tp_min_max'][sell_counter] = 0

					if ((len(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (dataset[symbol]['high'][int(finding_points['index'][elm])] * 1.0006)))[0])-1) > 1):
						signal_sell['st_min_max_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (dataset[symbol]['high'][int(finding_points['index'][elm])] * 1.0006)))[0])
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
					#///////////////////////////////////////////////////
				if (name_stp_pr == True):
					#Calculate ST and TP With Protect Resist Function
					dataset_pr_5M = pd.DataFrame()
					dataset_pr_15M = pd.DataFrame()
					cut_first = 0
					if (int(finding_points['index'][elm]) > 2000):
						cut_first = int(finding_points['index'][elm]) - 2000
					dataset_pr_5M['low'] = dataset[symbol]['low'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['high'] = dataset[symbol]['high'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['close'] = dataset[symbol]['close'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)
					dataset_pr_5M['open'] = dataset[symbol]['open'][cut_first:int(finding_points['index'][elm])].reset_index(drop=True)

					dataset_pr_15M['low'] = dataset_15M[symbol]['low'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['high'] = dataset_15M[symbol]['high'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['close'] = dataset_15M[symbol]['close'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)
					dataset_pr_15M['open'] = dataset_15M[symbol]['open'][int(cut_first/3):int(int(finding_points['index'][elm])/3)].reset_index(drop=True)

					res_pro = pd.DataFrame()
					
					try:
						res_pro = protect_resist(T_5M=True,T_15M=True,T_1H=False,T_4H=False,T_1D=False,dataset_5M=dataset_pr_5M,dataset_15M=dataset_pr_15M,dataset_1H=dataset_pr_15M,dataset_4H=dataset_pr_5M,dataset_1D=dataset_pr_5M,plot=False)
					except:
						res_pro['high'] = 'nan'
						res_pro['low'] = 'nan'

					if (res_pro.empty == False):
						signal_sell['diff_pr_top'][sell_counter] = (((res_pro['high'][0] * 1.0006) - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
						signal_sell['diff_pr_down'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - (res_pro['low'][2] * 1.0006))/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100

						if ((len(np.where(((dataset[symbol]['low'][int(finding_points['index'][elm]):-1].values) <= (res_pro['low'][2] * 1.0006)))[0]) - 1) > 1):
							signal_sell['tp_pr_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where(((dataset[symbol]['low'][int(finding_points['index'][elm]):-1].values) <= (res_pro['low'][2] * 1.0006)))[0])
							signal_sell['tp_pr'][sell_counter] = ((dataset[symbol]['low'][int(finding_points['index'][elm])] - dataset[symbol]['low'][signal_sell['tp_pr_index'][sell_counter]])/dataset[symbol]['low'][int(finding_points['index'][elm])]) * 100
						else:
							signal_sell['tp_pr_index'][sell_counter] = -1
							signal_sell['tp_pr'][sell_counter] = 0

						if ((len(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])-1) > 1):
							signal_sell['st_pr_index'][sell_counter] = int(finding_points['index'][elm]) + np.min(np.where((((dataset[symbol]['high'][int(finding_points['index'][elm]):-1]).values) >= (res_pro['high'][0] * 1.0006)))[0])
							signal_sell['st_pr'][sell_counter] = ((dataset[symbol]['high'][signal_sell['st_pr_index'][sell_counter]] - dataset[symbol]['high'][int(finding_points['index'][elm])])/dataset[symbol]['high'][int(finding_points['index'][elm])]) * 100
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
					#///////////////////////////////////////////////////

			sell_counter += 1

		#////////////////////////////////////////////////////////////////////////////
	
	signal_buy = signal_buy.drop(columns=0)
	signal_buy = signal_buy.dropna()
	signal_buy = signal_buy.sort_values(by = ['index'])
	signal_buy = signal_buy.reset_index(drop=True)

	signal_sell = signal_sell.drop(columns=0)
	signal_sell = signal_sell.dropna()
	signal_sell = signal_sell.sort_values(by = ['index'])
	signal_sell = signal_sell.reset_index(drop=True)


	if (plot == True):
		plt.plot(CCI_Low.index, CCI_Low,c='b')
		plt.plot(CCI_High.index, CCI_High,c='r')
		plt.show()

	return signal_buy, signal_sell
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Find Best Intervals *******************************************************
def Find_Best_intervals(signals,apply_to, min_tp=0.1, max_st=0.1, name_stp='flag_min_max', alpha=0.1):

	if (name_stp == 'flag_min_max'):
		signal_good = signals.drop(np.where((signals[name_stp]=='st')|
			(signals['st_min_max']>max_st)|
			(signals['tp_min_max']<min_tp))[0])

	if (name_stp == 'flag_pr'):
		signal_good = signals.drop(np.where((signals[name_stp]=='st')|
			(signals['st_pr']>max_st)|
			(signals['tp_pr']<min_tp))[0])
			#(signals['diff_pr_down']>max_st)

	signal_good = signal_good.sort_values(by = ['index'])
	signal_good = signal_good.reset_index(drop=True)

	#timeout = time.time() + 20  # timeout_break Sec from now
	while True:

		if (len(signal_good[apply_to].to_numpy()) - 1) >= 10:
			n_clusters = 5
		else:
			n_clusters = len(signal_good[apply_to].to_numpy()) - 1

		kmeans = KMeans(n_clusters=n_clusters, random_state=0,init='k-means++',n_init=5,max_iter=5)
		#Model Fitting
		kmeans = kmeans.fit(signal_good[apply_to].to_numpy().reshape(-1,1))

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		if ((len(Y) != len(Power))):
			timeout = time.time() + timeout_break
			continue
		if ((len(Y) == len(Power))): break

	signal_final = pd.DataFrame(Y, columns=['Y'])
	signal_final['power'] = Power
	signal_final = signal_final.sort_values(by = ['Y'])

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

	distributions = ['foldnorm','dweibull','rayleigh','expon','nakagami','norm']

	#************************************ Finding Sell's ****************************

	while True:
		
		f = Fitter(data = data_X, xmin=np.min(data_X), xmax=np.max(data_X), bins = len(signal_final['Y']), distributions = distributions, timeout=30, density=True)

		f.fit(amp=1, progress=False, n_jobs=-1)

		#distributions=['foldnorm','dweibull','rayleigh','expon','nakagami','norm']
		#f.summary(Nbest=5, lw=2, plot=True, method='sumsquare_error', clf=True)
		#print(f.get_best(method = 'sumsquare_error').items())

		items = list(f.get_best(method = 'sumsquare_error').items())
		dist_name = items[0][0]
		dist_parameters = items[0][1]

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
def tester_golden_cross_zero():

	return 0
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#**************************************************** Create First Cromosomes *******************************************************
def initilize_values():
	#************************** initialize Values ******************************************************
	Chromosome = {}
	range(1)
	value = randint(50, 100)

	Chromosome[0] = {
	'high_period': 50,
	'low_period': 25,
	'distance_lines': 2,
	'min_tp': 0.1,
	'max_st': 0.2,
	'alfa': 0.5
	}

	Chromosome[1] = {
	'high_period': 100,
	'low_period': 50,
	'distance_lines': 4,
	'min_tp': 0.2,
	'max_st': 0.1,
	'alfa': 0.2
	}
	i = 2
	while i < 20:
		Chromosome[i] = {
			'high_period': randint(60, 120),
			'low_period': randint(1, 60),
			'distance_lines': randint(0, 10),
			'min_tp': randint(0, 6)/10,
			'max_st': randint(0, 4)/10,
			'alfa': randint(1, 100)/100
		}
		res = list(Chromosome[i].keys()) 
		#print(res[1])
		#print(Chromosome[i][res[1]])
		i += 1
	#***********************************************************************************
	return Chromosome
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#*************************** How To Use Funcs *****************************************
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,99000)
symbol_data_15M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,33000)
print('data get')

print(initilize_values())

for symbolic in sym:
	#if (True): break
	print()
	print('**************************  ',symbolic.name,'  ***********************************************')
	if (symbolic.name == 'RUBRUR'): continue
	time_before = time.time()
	buy,sell = golden_cross_zero(dataset=symbol_data_5M,dataset_15M=symbol_data_15M,symbol=symbolic.name,Low_Period=25,High_Period=50,
		distance_lines=3,mode='optimize',name_stp_minmax=True,name_stp_pr=True,plot=False)
	print('time = ',time.time()-time_before)
	

	print('*************** Profits Min Max:')

	ramp_high_intervals_minmax = Find_Best_intervals(signals=buy,apply_to='ramp_high',
	 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

	ramp_low_intervals_minmax = Find_Best_intervals(signals=buy,apply_to='ramp_low',
	 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

	diff_min_max_cci_intervals_minmax = Find_Best_intervals(signals=buy,apply_to='diff_min_max_cci',
	 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

	diff_min_max_candle_intervals_minmax = Find_Best_intervals(signals=buy,apply_to='diff_min_max_candle',
	 min_tp=0.1, max_st=0.2, name_stp='flag_min_max',alpha=0.5)

	print('ramp_high_intervals_minmax = ',ramp_high_intervals_minmax)
	print('ramp_low_intervals_minmax = ',ramp_low_intervals_minmax)
	print('diff_min_max_cci_intervals_minmax = ',diff_min_max_cci_intervals_minmax)
	print('diff_min_max_candle_intervals_minmax = ',diff_min_max_candle_intervals_minmax)

	upper = 0
	mid = 1
	lower = 2

	list_index_ok = np.where(((buy['ramp_high'].to_numpy()>=ramp_high_intervals_minmax['interval'][lower]))&
		((buy['ramp_low'].to_numpy()>=ramp_low_intervals_minmax['interval'][lower]))&
		((buy['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_minmax['interval'][upper]))&
		((buy['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_minmax['interval'][upper]))
		)[0]



	print('mean tp min_max = ',np.mean(buy['tp_min_max'][list_index_ok]))
	print('mean st min_max = ',np.mean(buy['st_min_max'][list_index_ok]))

	print('max tp min_max = ',np.max(buy['tp_min_max'][list_index_ok]))
	print('max st min_max = ',np.max(buy['st_min_max'][list_index_ok]))

	print('tp min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'tp'))
	print('st min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'st'))


	print('sum st min_max = ',np.sum(buy['st_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'st')[0]].to_numpy()))
	print('sum tp min_max = ',np.sum(buy['tp_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'tp')[0]].to_numpy()))

	print('/////////////////////////////////////////////////////')



	ramp_low_intervals_pr = Find_Best_intervals(signals=buy,apply_to='ramp_low',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	ramp_high_intervals_pr = Find_Best_intervals(signals=buy,apply_to='ramp_high',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	diff_min_max_cci_intervals_pr = Find_Best_intervals(signals=buy,apply_to='diff_min_max_cci',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	diff_min_max_candle_intervals_pr = Find_Best_intervals(signals=buy,apply_to='diff_min_max_candle',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	diff_top_intervals_pr = Find_Best_intervals(signals=buy,apply_to='diff_pr_top',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	diff_down_intervals_pr = Find_Best_intervals(signals=buy,apply_to='diff_pr_down',
	 min_tp=0.1, max_st=0.2, name_stp='flag_pr',alpha=0.5)

	print('ramp_low_intervals_pr = ',ramp_low_intervals_pr)
	print('ramp_high_intervals_pr = ',ramp_high_intervals_pr)

	print('diff_min_max_cci_intervals_pr = ',diff_min_max_cci_intervals_pr)
	print('diff_min_max_candle_intervals_pr = ',diff_min_max_candle_intervals_pr)

	print('diff_top_intervals_pr = ',diff_top_intervals_pr)
	print('diff_down_intervals_pr = ',diff_down_intervals_pr)


	list_index_ok = np.where(((buy['ramp_low'].to_numpy()>=ramp_low_intervals_pr['interval'][lower]))&
		((buy['ramp_high'].to_numpy()>=ramp_high_intervals_pr['interval'][lower]))&
		((buy['diff_pr_top'].to_numpy()<=diff_top_intervals_pr['interval'][upper]))&
		((buy['diff_pr_down'].to_numpy()<=diff_down_intervals_pr['interval'][upper]))&
		((buy['diff_min_max_cci'].to_numpy()<=diff_min_max_cci_intervals_pr['interval'][upper]))&
		((buy['diff_min_max_candle'].to_numpy()<=diff_min_max_candle_intervals_pr['interval'][upper]))
		)[0]


	print('***************** Double Check')
	print('mean tp pr = ',np.mean(buy['tp_pr'][list_index_ok]))
	print('mean st pr = ',np.mean(buy['st_pr'][list_index_ok]))

	print('max tp pr = ',np.max(buy['tp_pr'][list_index_ok]))
	print('max st pr = ',np.max(buy['st_pr'][list_index_ok]))

	print('tp pr = ',np.bincount(buy['flag_pr'][list_index_ok] == 'tp'))
	print('st pr = ',np.bincount(buy['flag_pr'][list_index_ok] == 'st'))


	print('sum st pr = ',np.sum(buy['st_pr'][np.where(buy['flag_pr'][list_index_ok] == 'st')[0]].to_numpy()))
	print('sum tp pr = ',np.sum(buy['tp_pr'][np.where(buy['flag_pr'][list_index_ok] == 'tp')[0]].to_numpy()))

	print('mean tp min_max = ',np.mean(buy['tp_min_max'][list_index_ok]))
	print('mean st min_max = ',np.mean(buy['st_min_max'][list_index_ok]))

	print('max tp min_max = ',np.max(buy['tp_min_max'][list_index_ok]))
	print('max st min_max = ',np.max(buy['st_min_max'][list_index_ok]))

	print('tp min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'tp'))
	print('st min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'st'))


	print('sum st min_max = ',np.sum(buy['st_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'st')[0]].to_numpy()))
	print('sum tp min_max = ',np.sum(buy['tp_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'tp')[0]].to_numpy()))

	print('/////////////////////////////////////////////////////')


	print('********************* fixed Parameters:')

	list_index_ok = np.where(((buy['ramp_low'].to_numpy()>=21.072226))&
		((buy['ramp_high'].to_numpy()>=15.477149))&
		((buy['diff_pr_top'].to_numpy()<=0.662101))&
		((buy['diff_pr_down'].to_numpy()<=0.875824))&
		((buy['diff_min_max_cci'].to_numpy()<=181.974826))&
		((buy['diff_min_max_candle'].to_numpy()<=0.930234))
		)[0]


	print('***************** Double Check')
	print('mean tp pr = ',np.mean(buy['tp_pr'][list_index_ok]))
	print('mean st pr = ',np.mean(buy['st_pr'][list_index_ok]))

	print('max tp pr = ',np.max(buy['tp_pr'][list_index_ok]))
	print('max st pr = ',np.max(buy['st_pr'][list_index_ok]))

	print('tp pr = ',np.bincount(buy['flag_pr'][list_index_ok] == 'tp'))
	print('st pr = ',np.bincount(buy['flag_pr'][list_index_ok] == 'st'))


	print('sum st pr = ',np.sum(buy['st_pr'][np.where(buy['flag_pr'][list_index_ok] == 'st')[0]].to_numpy()))
	print('sum tp pr = ',np.sum(buy['tp_pr'][np.where(buy['flag_pr'][list_index_ok] == 'tp')[0]].to_numpy()))

	print('mean tp min_max = ',np.mean(buy['tp_min_max'][list_index_ok]))
	print('mean st min_max = ',np.mean(buy['st_min_max'][list_index_ok]))

	print('max tp min_max = ',np.max(buy['tp_min_max'][list_index_ok]))
	print('max st min_max = ',np.max(buy['st_min_max'][list_index_ok]))

	print('tp min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'tp'))
	print('st min_max = ',np.bincount(buy['flag_min_max'][list_index_ok] == 'st'))


	print('sum st min_max = ',np.sum(buy['st_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'st')[0]].to_numpy()))
	print('sum tp min_max = ',np.sum(buy['tp_min_max'][np.where(buy['flag_min_max'][list_index_ok] == 'tp')[0]].to_numpy()))

	print('/////////////////////////////////////////////////////')