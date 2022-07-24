from macd_Parameters import Parameters
from macd_Config import Config
import pandas_ta as ind
import pandas as pd
import ExtremePoints as extremepoints
import numpy as np
from timer import stTime

#************ Functions:

#divergence()
#dataset_preparer()
#calculator_macd()
#extreme_preparer()
#SignalFinder()
#buy_primaryFinder()
#buy_secondryFinder()
#sell_primaryFinder()
#sell_secondryFinder()

#//////////////////////

class Divergence:

	parameters = Parameters()
	config = Config()
	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({
							
							#************** Divergence:

							__class__.__name__ + '_apply_to': parameters.elements[__class__.__name__ + '_apply_to'],
							
							__class__.__name__ + '_macd_fast': parameters.elements[__class__.__name__ + '_macd_fast'],
							__class__.__name__ + '_macd_slow': parameters.elements[__class__.__name__ + '_macd_slow'],
							__class__.__name__ + '_macd_signal': parameters.elements[__class__.__name__ + '_macd_signal'],
							__class__.__name__ + '_num_exteremes_min': parameters.elements[__class__.__name__ + '_num_exteremes_min'],
							__class__.__name__ + '_num_exteremes_max': parameters.elements[__class__.__name__ + '_num_exteremes_max'],
							#__class__.__name__ + '_diff_extereme': parameters.elements[__class__.__name__ + '_diff_extereme'],

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
	@stTime
	def divergence(self, sigtype, sigpriority):

		#*************** OutPuts:
		#Four Panda DataFrams: signal_buy_primary, signal_buy_secondry, signal_sell_primary, signal_sell_secondry
		#signal = buy_primary, buy_secondry, sell_primary, sell_secondry
		#value_front: the value of last index of Divergence
		#value_back: the value of before index of Divergence
		#index: the index of last index of Divergence
		#ramp_macd
		#ramp_candle
		#coef_ramps
		#diff_ramps
		#beta
		#danger_line
		#diff_min_max_macd
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

		macd = self.calculator_macd()

		extreme_max, extreme_min = self.extreme_preparer(macd = macd)

		if sigtype == 'buy':

			signal = self.SignalFinder(extremes = extreme_min, sigtype = sigtype, sigpriority = sigpriority)

		if sigtype == 'sell':

			signal = self.SignalFinder(extremes = extreme_max, sigtype = sigtype, sigpriority = sigpriority)
		
		
		signal = signal.drop_duplicates(subset = ['index'], keep='last', inplace=False, ignore_index=False).sort_values(by = ['index'])
		signal = signal.set_index(signal['index'])

		return signal, sigtype

	def calculator_macd(self):

		symbol = self.elements['symbol']
		apply_to = self.elements[__class__.__name__ + '_apply_to']
		macd_read = ind.macd(
							self.elements['dataset_5M'][symbol][apply_to],
							fast = self.elements[__class__.__name__ + '_macd_fast'],
							slow = self.elements[__class__.__name__ + '_macd_slow'],
							signal = self.elements[__class__.__name__ + '_macd_signal']
							)

		column_macds = macd_read.columns[2]
		column_macd = macd_read.columns[0]
		column_macdh = macd_read.columns[1]

		macd = pd.DataFrame(
							{
								'macds': macd_read[column_macds],
								'macd': macd_read[column_macd],
								'macdh': macd_read[column_macdh],
							}
							).dropna(inplace = False)
		
		return macd

	def extreme_preparer(self,macd):

		extremes_points = extremepoints.finder(
												high = macd.macds,
												low = macd.macds,
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

		extreme_min = extreme_min.assign(
										min_1 = extreme_min.shift(periods = 1, fill_value = np.inf)['min'],
										min_2 = extreme_min.shift(periods = 2, fill_value = np.inf)['min'],
										min_3 = extreme_min.shift(periods = 3, fill_value = np.inf)['min'],
										min_4 = extreme_min.shift(periods = 4, fill_value = np.inf)['min'],
										min_5 = extreme_min.shift(periods = 5, fill_value = np.inf)['min'],
										min_6 = extreme_min.shift(periods = 6, fill_value = np.inf)['min'],
										)

		extreme_max = pd.DataFrame(
									{
										'max': extremes_points['max'],
										'index': extremes_points['index_max'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		extreme_max['index'] = extreme_max['index'].astype('int32')

		extreme_max = extreme_max.assign(
										max_1 = extreme_max.shift(periods = 1, fill_value = -np.inf)['max'],
										max_2 = extreme_max.shift(periods = 2, fill_value = -np.inf)['max'],
										max_3 = extreme_max.shift(periods = 3, fill_value = -np.inf)['max'],
										max_4 = extreme_max.shift(periods = 4, fill_value = -np.inf)['max'],
										max_5 = extreme_max.shift(periods = 5, fill_value = -np.inf)['max'],
										max_6 = extreme_max.shift(periods = 6, fill_value = -np.inf)['max'],
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
		dataset_5M_ = self.elements['dataset_5M'][symbol].loc[:, ['high', 'low']].copy(deep = True)


		div_index_list_fron = list((index['index'].where(index['div'] == True)).dropna(inplace = False).index)
		div_index_list_front = list(filter(lambda x: x != 0, div_index_list_fron))

		div_index_list_bac = list((index['index'].where(index['div'] == True)).dropna(inplace = False).index - 1)
		div_index_list_back = list(filter(lambda x: x >= 0, div_index_list_bac))
		

		dataset_5M_div = pd.DataFrame(
									{
										'low_front': dataset_5M_['low'][index['index'][div_index_list_front]].values,
										'low_back': dataset_5M_['low'][index['index'][div_index_list_back]].values,
										'high_front': dataset_5M_['low'][index['index'][div_index_list_front]].values,
										'high_back': dataset_5M_['low'][index['index'][div_index_list_back]].values,
									}
									)

		return dataset_5M_div


	def buy_primaryFinder(self, extremes):

		macd_div_1 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_1'], True)).where(extremes['min'] > extremes['min_1'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_1'],
									}
								)
		macd_div_2 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_2'], True)).where(extremes['min'] > extremes['min_2'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_2'],
									}
								)
		macd_div_3 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_3'], True)).where(extremes['min'] > extremes['min_3'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_3'],
									}
								)
		macd_div_4 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_4'], True)).where(extremes['min'] > extremes['min_4'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_4'],
									}
								)
		macd_div_5 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_5'], True)).where(extremes['min'] > extremes['min_5'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_5'],
									}
								)
		macd_div_6 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_6'], True)).where(extremes['min'] > extremes['min_6'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = macd_div_1)
		macd_div_1 = macd_div_1[macd_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = macd_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'buy_primary'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_2)
		macd_div_2 = macd_div_2[macd_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_3)
		macd_div_3 = macd_div_3[macd_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_4)
		macd_div_4 = macd_div_4[macd_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_5)
		macd_div_5 = macd_div_5[macd_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_6)
		macd_div_6 = macd_div_6[macd_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'buy_primary'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def buy_secondryFinder(self, extremes):

		macd_div_1 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_1'], True)).where(extremes['min'] < extremes['min_1'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_1'],
									}
								)
			
		macd_div_2 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_2'], True)).where(extremes['min'] < extremes['min_2'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_2'],
									}
								)
		macd_div_3 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_3'], True)).where(extremes['min'] < extremes['min_3'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_3'],
									}
								)
		macd_div_4 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_4'], True)).where(extremes['min'] < extremes['min_4'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_4'],
									}
								)
		macd_div_5 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_5'], True)).where(extremes['min'] < extremes['min_5'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_5'],
									}
								)
		macd_div_6 = pd.DataFrame(
									{
									'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] < extremes['min_6'], True)).where(extremes['min'] < extremes['min_6'], False),
									'index': extremes['index'],
									'macd_front': extremes['min'],
									'macd_back': extremes['min_6'],
									}
								)
		
		dataset_5M_div = self.dataset_preparer(index = macd_div_1)
		macd_div_1 = macd_div_1[macd_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = macd_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'buy_secondry'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_2)
		macd_div_2 = macd_div_2[macd_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_3)
		macd_div_3 = macd_div_3[macd_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_4)
		macd_div_4 = macd_div_4[macd_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_5)
		macd_div_5 = macd_div_5[macd_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_6)
		macd_div_6 = macd_div_6[macd_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] > dataset_5M_div['low_back'], False)

		divergences = divergences.append(macd_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'buy_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def sell_primaryFinder(self, extremes):

		macd_div_1 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_1'], True)).where(extremes['max'] < extremes['max_1'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_1'],
									}
								)
			
		macd_div_2 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_2'], True)).where(extremes['max'] < extremes['max_2'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_2'],
									}
								)
		macd_div_3 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_3'], True)).where(extremes['max'] < extremes['max_3'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_3'],
									}
								)
		macd_div_4 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_4'], True)).where(extremes['max'] < extremes['max_4'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_4'],
									}
								)
		macd_div_5 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_5'], True)).where(extremes['max'] < extremes['max_5'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_5'],
									}
								)
		macd_div_6 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] < extremes['max_6'], True)).where(extremes['max'] < extremes['max_6'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = macd_div_1)
		macd_div_1 = macd_div_1[macd_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = macd_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'sell_primary'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_2)
		macd_div_2 = macd_div_2[macd_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_3)
		macd_div_3 = macd_div_3[macd_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_4)
		macd_div_4 = macd_div_4[macd_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_5)
		macd_div_5 = macd_div_5[macd_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_6)
		macd_div_6 = macd_div_6[macd_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] > dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'sell_primary'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences


	def sell_secondryFinder(self, extremes):

		macd_div_1 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_1'], True)).where(extremes['max'] > extremes['max_1'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_1'],
									}
								)
			
		macd_div_2 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_2'], True)).where(extremes['max'] > extremes['max_2'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_2'],
									}
								)
		macd_div_3 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_3'], True)).where(extremes['max'] > extremes['max_3'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_3'],
									}
								)
		macd_div_4 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_4'], True)).where(extremes['max'] > extremes['max_4'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_4'],
									}
								)
		macd_div_5 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_5'], True)).where(extremes['max'] > extremes['max_5'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_5'],
									}
								)
		macd_div_6 = pd.DataFrame(
									{
									'div': ((extremes['max'].copy(deep = True)).mask(extremes['max'] > extremes['max_6'], True)).where(extremes['max'] > extremes['max_6'], False),
									'index': extremes['index'],
									'macd_front': extremes['max'],
									'macd_back': extremes['max_6'],
									}
								)

		dataset_5M_div = self.dataset_preparer(index = macd_div_1)
		macd_div_1 = macd_div_1[macd_div_1['div'] == True].reset_index(inplace = False, drop = True)
		data_div_1 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = macd_div_1.drop(columns = ['div']).join(dataset_5M_div).assign(
																					div = data_div_1[data_div_1 == True], 
																					diff_extereme = 1, 
																					signal = 'sell_secondry'
																					).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_2)
		macd_div_2 = macd_div_2[macd_div_2['div'] == True].reset_index(inplace = False, drop = True)
		data_div_2 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_2[data_div_2 == True], 
																									diff_extereme = 2, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)


		dataset_5M_div = self.dataset_preparer(index = macd_div_3)
		macd_div_3 = macd_div_3[macd_div_3['div'] == True].reset_index(inplace = False, drop = True)
		data_div_3 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_3.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_3[data_div_3 == True], 
																									diff_extereme = 3, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_4)
		macd_div_4 = macd_div_4[macd_div_4['div'] == True].reset_index(inplace = False, drop = True)
		data_div_4 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_4.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_4[data_div_4 == True], 
																									diff_extereme = 4, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_5)
		macd_div_5 = macd_div_5[macd_div_5['div'] == True].reset_index(inplace = False, drop = True)
		data_div_5 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_2.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_5[data_div_5 == True], 
																									diff_extereme = 5, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)
		

		dataset_5M_div = self.dataset_preparer(index = macd_div_6)
		macd_div_6 = macd_div_6[macd_div_6['div'] == True].reset_index(inplace = False, drop = True)
		data_div_6 = ((dataset_5M_div['high_front'].copy(deep = True)).mask(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], True)).where(dataset_5M_div['high_front'] < dataset_5M_div['high_back'], False)

		divergences = divergences.append(macd_div_6.drop(columns = ['div']).join(dataset_5M_div).assign(
																									div = data_div_6[data_div_6 == True], 
																									diff_extereme = 6, 
																									signal = 'sell_secondry'
																									)).dropna().reset_index(inplace = False, drop = True)

		return divergences