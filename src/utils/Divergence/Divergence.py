import ExtremePoints as extremepoints
import matplotlib as matplotlib
import matplotlib.pyplot as plt
from timer import stTime
import mplfinance as mpf
import pandas as pd
import numpy as np
import os



#************ Functions:

#divergence()
#dataset_preparer()
#calculator_indicator()
#extreme_preparer()
#SignalFinder()
#buy_primaryFinder()
#buy_secondryFinder()
#sell_primaryFinder()
#sell_secondryFinder()
#PlotSaver()

#//////////////////////

class Divergence:

	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({
							
							#************** Divergence:
							
							__class__.__name__ + '_num_exteremes_min': parameters.elements[__class__.__name__ + '_num_exteremes_min'],
							__class__.__name__ + '_num_exteremes_max': parameters.elements[__class__.__name__ + '_num_exteremes_max'],
							__class__.__name__ + '_diff_extereme': parameters.elements[__class__.__name__ + '_diff_extereme'],

							#////////////////////////


							#************* Global:

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],
							'symbol': parameters.elements['symbol'],

							#/////////////////////
							})

		self.cfg = dict({
						__class__.__name__ + '_buy_doing': config.cfg[__class__.__name__ + '_buy_doing'],
						__class__.__name__ + '_sell_doing': config.cfg[__class__.__name__ + '_sell_doing'],
						__class__.__name__ + '_primary_doing': config.cfg[__class__.__name__ + '_primary_doing'],
						__class__.__name__ + '_secondry_doing': config.cfg[__class__.__name__ + '_secondry_doing'],
						})


	#Finding Divergences:
	#@stTime
	def divergence(self, sigtype, sigpriority, indicator, column_div, ind_name, dataset_5M, dataset_1H, symbol, flagtest, flaglearn):

		#*************** OutPuts:
		#Four Panda DataFrams: signal_buy_primary, signal_buy_secondry, signal_sell_primary, signal_sell_secondry
		#signal = buy_primary, buy_secondry, sell_primary, sell_secondry
		#value_front: the value of last index of Divergence
		#value_back: the value of before index of Divergence
		#index: the index of last index of Divergence
		#ramp_indicator
		#ramp_candle
		#coef_ramps
		#diff_ramps
		#beta
		#danger_line
		#diff_min_max_indicator
		#diff_min_max_candle
		#** Just in optimize mode:
		#tp_min_max_index
		#tp_min_max
		#st_min_max_index
		#st_min_max
		#flag_min_max: st or tp
		#tp_pr_index
		#tp_pr
		#st_pr_index
		#st_pr
		#flag_pr: st or tp
		#diff_pr_top
		#diff_pr_down
		#/////////////////////////////

		#***************************** Initialize Inputs ************************

		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol


		extreme_max, extreme_min = self.extreme_preparer(indicator = indicator, column_div = column_div, sigpriority = sigpriority)

		if sigtype == 'buy':

			signal = self.SignalFinder(extremes = extreme_min, sigtype = sigtype, sigpriority = sigpriority)

		if sigtype == 'sell':

			signal = self.SignalFinder(extremes = extreme_max, sigtype = sigtype, sigpriority = sigpriority)
		

		if (
			flagtest == False or
			flaglearn == True
			):

			signal = signal.drop(signal.index[signal['diff_extereme'] >= self.elements[__class__.__name__ + '_diff_extereme']])

		signal = signal.drop_duplicates(subset = ['index'], keep='last', inplace=False, ignore_index=False).sort_values(by = ['index'])
		signal = signal.set_index(signal['index'])
		signal = signal.assign(
								indicator_name = ind_name,
								column_div = column_div,
								symbol = symbol
								)

		return signal, sigtype, indicator


	def extreme_preparer(self, indicator, column_div, sigpriority):

		extremes_points = extremepoints.finder(
												high = indicator[column_div],
												low = indicator[column_div],
												number_min = self.elements[__class__.__name__ + '_num_exteremes_min'],
												number_max = self.elements[__class__.__name__ + '_num_exteremes_max']
												)

		extreme_min = pd.DataFrame(
									{
										'min': extremes_points['min'],
										'index': extremes_points['index_min'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		extreme_min['index'] = extreme_min['index'].astype('int32')

		if sigpriority == 'secondry':
			coef = -1
		else:
			coef = 1

		extreme_min = extreme_min.assign(
										min_1 = extreme_min.shift(periods = 1, fill_value = coef * np.inf)['min'],
										min_2 = extreme_min.shift(periods = 2, fill_value = coef * np.inf)['min'],
										min_3 = extreme_min.shift(periods = 3, fill_value = coef * np.inf)['min'],
										min_4 = extreme_min.shift(periods = 4, fill_value = coef * np.inf)['min'],
										min_5 = extreme_min.shift(periods = 5, fill_value = coef * np.inf)['min'],
										min_6 = extreme_min.shift(periods = 6, fill_value = coef * np.inf)['min'],

										index_min_1 = extreme_min.shift(periods = 1, fill_value = np.inf)['index'],
										index_min_2 = extreme_min.shift(periods = 2, fill_value = np.inf)['index'],
										index_min_3 = extreme_min.shift(periods = 3, fill_value = np.inf)['index'],
										index_min_4 = extreme_min.shift(periods = 4, fill_value = np.inf)['index'],
										index_min_5 = extreme_min.shift(periods = 5, fill_value = np.inf)['index'],
										index_min_6 = extreme_min.shift(periods = 6, fill_value = np.inf)['index'],
										)

		extreme_max = pd.DataFrame(
									{
										'max': extremes_points['max'],
										'index': extremes_points['index_max'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		extreme_max['index'] = extreme_max['index'].astype('int32')

		extreme_max = extreme_max.assign(
										max_1 = extreme_max.shift(periods = 1, fill_value = coef * -np.inf)['max'],
										max_2 = extreme_max.shift(periods = 2, fill_value = coef * -np.inf)['max'],
										max_3 = extreme_max.shift(periods = 3, fill_value = coef * -np.inf)['max'],
										max_4 = extreme_max.shift(periods = 4, fill_value = coef * -np.inf)['max'],
										max_5 = extreme_max.shift(periods = 5, fill_value = coef * -np.inf)['max'],
										max_6 = extreme_max.shift(periods = 6, fill_value = coef * -np.inf)['max'],

										index_max_1 = extreme_max.shift(periods = 1, fill_value = -np.inf)['index'],
										index_max_2 = extreme_max.shift(periods = 2, fill_value = -np.inf)['index'],
										index_max_3 = extreme_max.shift(periods = 3, fill_value = -np.inf)['index'],
										index_max_4 = extreme_max.shift(periods = 4, fill_value = -np.inf)['index'],
										index_max_5 = extreme_max.shift(periods = 5, fill_value = -np.inf)['index'],
										index_max_6 = extreme_max.shift(periods = 6, fill_value = -np.inf)['index'],
										)

		return extreme_max, extreme_min

	#@stTime
	def SignalFinder(self, extremes, sigtype, sigpriority):

		if (
			self.cfg[__class__.__name__ + '_' + 'buy' + '_doing'] and
			self.cfg[__class__.__name__ + '_primary_doing'] and
			sigtype == 'buy' and
			sigpriority == 'primary'
			): #Example buy_doing True

			signal = self.buy_primaryFinder(extremes =  extremes)

		elif (
			self.cfg[__class__.__name__ + '_' + 'buy' + '_doing'] and
			self.cfg[__class__.__name__ + '_secondry_doing'] and
			sigtype == 'buy' and
			sigpriority == 'secondry'
			): #Example buy_doing True

			signal = self.buy_secondryFinder(extremes =  extremes)

		elif (
			self.cfg[__class__.__name__ + '_' + 'sell' + '_doing'] and
			self.cfg[__class__.__name__ + '_primary_doing'] and
			sigtype == 'sell' and
			sigpriority == 'primary'
			): #Example buy_doing True

			signal = self.sell_primaryFinder(extremes =  extremes)

		elif (
			self.cfg[__class__.__name__ + '_' + 'sell' + '_doing'] and
			self.cfg[__class__.__name__ + '_secondry_doing'] and
			sigtype == 'sell' and
			sigpriority == 'secondry'
			): #Example buy_doing True

			signal = self.sell_secondryFinder(extremes =  extremes)

		return signal
			

	#@stTime
	def dataset_preparer(self, index):

		symbol = self.elements['symbol']
		dataset_5M_ = self.elements['dataset_5M'][symbol].loc[:, ['high', 'low', 'time']].copy(deep = True)

		index = index.replace([np.inf, -np.inf], np.nan)
		index = index.dropna(inplace = False).reset_index(drop=True)

		div_index_list_fron = list((index['index'].where(index['div'] == True)).dropna(inplace = False).index)
		div_index_list_front = div_index_list_fron#list(filter(lambda x: x != 0, div_index_list_fron))

		div_index_list_bac = list((index['index_back'].where(index['div'] == True)).dropna(inplace = False).index)
		div_index_list_back = list(filter(lambda x: x >= 0, div_index_list_bac))

		dataset_5M_div = pd.DataFrame(
									{
										'low_front': dataset_5M_['low'][index['index'][div_index_list_front]].values,
										'low_back': dataset_5M_['low'][index['index_back'][div_index_list_back]].values,

										'high_front': dataset_5M_['high'][index['index'][div_index_list_front]].values,
										'high_back': dataset_5M_['high'][index['index_back'][div_index_list_back]].values,

										'time_low_front':  dataset_5M_['time'][index['index'][div_index_list_front]].values,
										'time_low_back': dataset_5M_['time'][index['index_back'][div_index_list_back]].values,

										'time_high_front': dataset_5M_['time'][index['index'][div_index_list_front]].values,
										'time_high_back': dataset_5M_['time'][index['index_back'][div_index_list_back]].values,
									}
									)

		return dataset_5M_div


	def buy_primaryFinder(self, extremes):

		indicator_div_1 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_1'], True)).where(extremes['min'] > extremes['min_1'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_1'],
									'index_back': extremes['index_min_1'],
									}
								)
		indicator_div_2 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_2'], True)).where(extremes['min'] > extremes['min_2'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_2'],
									'index_back': extremes['index_min_2'],
									}
								)
		indicator_div_3 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_3'], True)).where(extremes['min'] > extremes['min_3'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_3'],
									'index_back': extremes['index_min_3'],
									}
								)
		indicator_div_4 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_4'], True)).where(extremes['min'] > extremes['min_4'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_4'],
									'index_back': extremes['index_min_4'],
									}
								)
		indicator_div_5 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_5'], True)).where(extremes['min'] > extremes['min_5'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_5'],
									'index_back': extremes['index_min_5'],
									}
								)
		indicator_div_6 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_6'], True)).where(extremes['min'] > extremes['min_6'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_6'],
									'index_back': extremes['index_min_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = indicator_div_1)
		indicator_div_1 = indicator_div_1[indicator_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = indicator_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'buy_primary'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_2)
		indicator_div_2 = indicator_div_2[indicator_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_3)
		indicator_div_3 = indicator_div_3[indicator_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_4)
		indicator_div_4 = indicator_div_4[indicator_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_5)
		indicator_div_5 = indicator_div_5[indicator_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_6)
		indicator_div_6 = indicator_div_6[indicator_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def buy_secondryFinder(self, extremes):

		indicator_div_1 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_1'], True)).where(extremes['min'] < extremes['min_1'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_1'],
									'index_back': extremes['index_min_1'],
									}
								)
			
		indicator_div_2 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_2'], True)).where(extremes['min'] < extremes['min_2'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_2'],
									'index_back': extremes['index_min_2'],
									}
								)
		indicator_div_3 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_3'], True)).where(extremes['min'] < extremes['min_3'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_3'],
									'index_back': extremes['index_min_3'],
									}
								)
		indicator_div_4 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_4'], True)).where(extremes['min'] < extremes['min_4'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_4'],
									'index_back': extremes['index_min_4'],
									}
								)
		indicator_div_5 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_5'], True)).where(extremes['min'] < extremes['min_5'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_5'],
									'index_back': extremes['index_min_5'],
									}
								)
		indicator_div_6 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_6'], True)).where(extremes['min'] < extremes['min_6'], False),
									'index': extremes['index'],
									'indicator_front': extremes['min'],
									'indicator_back': extremes['min_6'],
									'index_back': extremes['index_min_6'],
									}
								)
		
		dataset_5M_div = self.dataset_preparer(index = indicator_div_1)
		indicator_div_1 = indicator_div_1[indicator_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = indicator_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'buy_secondry'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_2)
		indicator_div_2 = indicator_div_2[indicator_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_3)
		indicator_div_3 = indicator_div_3[indicator_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_4)
		indicator_div_4 = indicator_div_4[indicator_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_5)
		indicator_div_5 = indicator_div_5[indicator_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_6)
		indicator_div_6 = indicator_div_6[indicator_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(indicator_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def sell_primaryFinder(self, extremes):

		indicator_div_1 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_1'], True)).where(extremes['max'] < extremes['max_1'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_1'],
									'index_back': extremes['index_max_1'],
									}
								)
			
		indicator_div_2 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_2'], True)).where(extremes['max'] < extremes['max_2'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_2'],
									'index_back': extremes['index_max_2'],
									}
								)
		indicator_div_3 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_3'], True)).where(extremes['max'] < extremes['max_3'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_3'],
									'index_back': extremes['index_max_3'],
									}
								)
		indicator_div_4 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_4'], True)).where(extremes['max'] < extremes['max_4'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_4'],
									'index_back': extremes['index_max_4'],
									}
								)
		indicator_div_5 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_5'], True)).where(extremes['max'] < extremes['max_5'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_5'],
									'index_back': extremes['index_max_5'],
									}
								)
		indicator_div_6 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_6'], True)).where(extremes['max'] < extremes['max_6'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_6'],
									'index_back': extremes['index_max_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = indicator_div_1)
		indicator_div_1 = indicator_div_1[indicator_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = indicator_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'sell_primary'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_2)
		indicator_div_2 = indicator_div_2[indicator_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_3)
		indicator_div_3 = indicator_div_3[indicator_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_4)
		indicator_div_4 = indicator_div_4[indicator_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_5)
		indicator_div_5 = indicator_div_5[indicator_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_6)
		indicator_div_6 = indicator_div_6[indicator_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def sell_secondryFinder(self, extremes):

		indicator_div_1 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_1'], True)).where(extremes['max'] > extremes['max_1'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_1'],
									'index_back': extremes['index_max_1'],
									}
								)
			
		indicator_div_2 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_2'], True)).where(extremes['max'] > extremes['max_2'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_2'],
									'index_back': extremes['index_max_2'],
									}
								)
		indicator_div_3 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_3'], True)).where(extremes['max'] > extremes['max_3'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_3'],
									'index_back': extremes['index_max_3'],
									}
								)
		indicator_div_4 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_4'], True)).where(extremes['max'] > extremes['max_4'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_4'],
									'index_back': extremes['index_max_4'],
									}
								)
		indicator_div_5 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_5'], True)).where(extremes['max'] > extremes['max_5'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_5'],
									'index_back': extremes['index_max_5'],
									}
								)
		indicator_div_6 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_6'], True)).where(extremes['max'] > extremes['max_6'], False),
									'index': extremes['index'],
									'indicator_front': extremes['max'],
									'indicator_back': extremes['max_6'],
									'index_back': extremes['index_max_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = indicator_div_1)
		indicator_div_1 = indicator_div_1[indicator_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = indicator_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'sell_secondry'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_2)
		indicator_div_2 = indicator_div_2[indicator_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = indicator_div_3)
		indicator_div_3 = indicator_div_3[indicator_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_4)
		indicator_div_4 = indicator_div_4[indicator_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_5)
		indicator_div_5 = indicator_div_5[indicator_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = indicator_div_6)
		indicator_div_6 = indicator_div_6[indicator_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(indicator_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences

	def PlotSaver(
					self,
					signals,
					extreme,
					loc_end_5M,
					indicator,
					dataset_5M,
					res_pro_high,
					res_pro_low,
					flag_savepic
					):

		if flag_savepic == False: return

		if extreme['flag'][loc_end_5M] == 'no_flag': return
		#Example: macd/candle/sell_secondry/symbol/tp/
		path_candle = (
						'pics/' + 
						signals['indicator_name'][signals['index'].max()] +  '/' + 
						signals['signal'][signals['index'].max()] + '/' + 
						signals['symbol'][signals['index'].max()] + '/' +
						extreme['flag'][loc_end_5M] + '/'
						'/candle' + '/'
						)

		path_indicator = (
						'pics/' +
						signals['indicator_name'][signals['index'].max()] +  '/' + 
						signals['signal'][signals['index'].max()] + '/' + 
						signals['symbol'][signals['index'].max()] + '/' +
						extreme['flag'][loc_end_5M] + '/' +
						signals['indicator_name'][signals['index'].max()] + '/'
						)

		if not os.path.exists(path_candle):
			os.makedirs(path_candle)
			path_candle = path_candle + str(loc_end_5M)
		else:
			path_candle = path_candle + str(loc_end_5M)

		if not os.path.exists(path_indicator):
			os.makedirs(path_indicator)
			path_indicator = path_indicator + str(loc_end_5M)
		else:
			path_indicator = path_indicator + str(loc_end_5M)

		fig = plt.figure()
		plt.figure().clear()
		plt.close('all')
		plt.cla()
		plt.clf()

		index_end = int(loc_end_5M)
		index_start = int(signals['index_back'][loc_end_5M]) - 20

		if extreme['flag'][loc_end_5M] == 'tp':
			index_pos = extreme['index_tp'][loc_end_5M]

		elif extreme['flag'][loc_end_5M] == 'st':
			index_pos = extreme['index_st'][loc_end_5M]

		index_pos = int(index_pos + 20)

		if index_pos > len(dataset_5M): index_pos = len(dataset_5M) - 1

		plt.plot([signals['index_back'][loc_end_5M], signals['index'][loc_end_5M]], [signals['indicator_back'][loc_end_5M], signals['indicator_front'][loc_end_5M]], 'o',c='purple')

		plt.plot(range(int(signals['index_back'][loc_end_5M]) - 20, index_pos), indicator[signals['column_div'][loc_end_5M]][range(int(signals['index_back'][loc_end_5M]) - 20, index_pos)],c='b')
		plt.plot(range(int(signals['index_back'][loc_end_5M]) - 20, index_pos), indicator[signals['column_div'][loc_end_5M]][range(int(signals['index_back'][loc_end_5M]) - 20,index_pos)],c='yellow')
		plt.bar(range(int(signals['index_back'][loc_end_5M]) - 20, index_pos), indicator[signals['column_div'][loc_end_5M]][range(int(signals['index_back'][loc_end_5M]) - 20,index_pos)],align='center',color='orange')

		plt.plot([signals['index_back'][loc_end_5M], signals['index'][loc_end_5M]], [signals['indicator_back'][loc_end_5M], signals['indicator_front'][loc_end_5M]], c='r',linestyle="-")
		plt.grid(linestyle = '--', linewidth = 0.5)

		plt.savefig(path_indicator, dpi=600, bbox_inches='tight')

		plt.figure().clear()
		plt.close('all')
		plt.cla()
		plt.clf()
										
		#ax1.plot(dataset[symbol]['close'].index,dataset[symbol]['close'],c='b')

		dataset_plot_candle = pd.DataFrame()
		dataset_plot_candle['low'] = dataset_5M['low'][range(index_start,index_pos)].reset_index(drop=True)
		dataset_plot_candle['high'] = dataset_5M['high'][range(index_start,index_pos)].reset_index(drop=True)
		dataset_plot_candle['close'] = dataset_5M['close'][range(index_start,index_pos)].reset_index(drop=True)
		dataset_plot_candle['open'] = dataset_5M['open'][range(index_start,index_pos)].reset_index(drop=True)
		dataset_plot_candle['time'] = dataset_5M['time'][range(index_start,index_pos)].reset_index(drop=True)
		dataset_plot_candle['volume'] = dataset_5M['volume'][range(index_start,index_pos)].reset_index(drop=True)

		daily = pd.DataFrame(dataset_plot_candle)
		daily.index.name = 'Time'
		daily.index = dataset_plot_candle['time']
		daily.head(3)
		daily.tail(3)

		mc = mpf.make_marketcolors(
									base_mpf_style='yahoo',
									up='green',
									down='red',
									#vcedge = {'up': 'green', 'down': 'red'}, 
									vcdopcod = True,
									alpha = 0.0001
									)
		mco = [mc]*len(daily)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print(signals)

		if 'buy' in signals['signal'][loc_end_5M]:
			two_points = [
						(signals['time_low_back'][loc_end_5M], signals['low_back'][loc_end_5M]),
						(signals['time_low_front'][loc_end_5M], signals['low_front'][loc_end_5M])
						]
		elif 'sell' in signals['signal'][loc_end_5M]:
			two_points = [
						(signals['time_high_back'][loc_end_5M], signals['high_back'][loc_end_5M]),
						(signals['time_high_front'][loc_end_5M], signals['high_front'][loc_end_5M])
						]

		mpf.plot(
				daily,
				type='candle',
				volume=True,
				style='yahoo',
				figscale=1,
				hlines=dict(hlines=[res_pro_low,res_pro_high],colors=['black','purple'],linestyle='-.'),
				savefig=dict(fname=path_candle,dpi=600,pad_inches=0.25),
				marketcolor_overrides=mco,
				alines=dict(alines=two_points,colors=['orange'],linestyle='-.'),
				)

		mpf.figure().clear()
		matplotlib.use("Agg")