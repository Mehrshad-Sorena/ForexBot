from macd_Parameters import Parameters
from macd_Config import Config
import pandas_ta as ind
import pandas as pd
import ExtremePoints as extremepoints
from pr_Parameters import Parameters as ex_params
from pr_Config import Config as ex_config
import numpy as np
from timer import stTime


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
							__class__.__name__ + '_symbol': parameters.elements[__class__.__name__ + '_symbol'],
							__class__.__name__ + '_out_before_buy': parameters.elements[__class__.__name__ + '_out_before_buy'],
							__class__.__name__ + '_out_before_sell': parameters.elements[__class__.__name__ + '_out_before_sell'],
							__class__.__name__ + '_macd_fast': parameters.elements[__class__.__name__ + '_macd_fast'],
							__class__.__name__ + '_macd_slow': parameters.elements[__class__.__name__ + '_macd_slow'],
							__class__.__name__ + '_macd_signal': parameters.elements[__class__.__name__ + '_macd_signal'],
							__class__.__name__ + '_st_percent_buy_max': parameters.elements[__class__.__name__ + '_st_percent_buy_max'],
							__class__.__name__ + '_st_percent_buy_min': parameters.elements[__class__.__name__ + '_st_percent_buy_min'],
							__class__.__name__ + '_st_percent_sell_max': parameters.elements[__class__.__name__ + '_st_percent_sell_max'],
							__class__.__name__ + '_st_percent_sell_min': parameters.elements[__class__.__name__ + '_st_percent_sell_min'],
							__class__.__name__ + '_tp_percent_buy_max': parameters.elements[__class__.__name__ + '_tp_percent_buy_max'],
							__class__.__name__ + '_tp_percent_buy_min': parameters.elements[__class__.__name__ + '_tp_percent_buy_min'],
							__class__.__name__ + '_tp_percent_sell_max': parameters.elements[__class__.__name__ + '_tp_percent_sell_max'],
							__class__.__name__ + '_tp_percent_sell_min': parameters.elements[__class__.__name__ + '_tp_percent_sell_min'],
							__class__.__name__ + '_alpha': parameters.elements[__class__.__name__ + '_alpha'],
							__class__.__name__ + '_num_exteremes_min': parameters.elements[__class__.__name__ + '_num_exteremes_min'],
							__class__.__name__ + '_num_exteremes_max': parameters.elements[__class__.__name__ + '_num_exteremes_max'],
							__class__.__name__ + '_diff_extereme': parameters.elements[__class__.__name__ + '_diff_extereme'],

							#////////////////////////


							#************* Global:

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],

							#/////////////////////
							})

		self.cfg = dict({
						__class__.__name__ + '_mode': config.cfg[__class__.__name__ + '_mode'],
						__class__.__name__ + '_plot': config.cfg[__class__.__name__ + '_plot'],
						__class__.__name__ + '_buy_doing': config.cfg[__class__.__name__ + '_buy_doing'],
						__class__.__name__ + '_sell_doing': config.cfg[__class__.__name__ + '_sell_doing'],
						__class__.__name__ + '_primary_doing': config.cfg[__class__.__name__ + '_primary_doing'],
						__class__.__name__ + '_secondry_doing': config.cfg[__class__.__name__ + '_secondry_doing'],
						__class__.__name__ + '_name_stp_pr': config.cfg[__class__.__name__ + '_name_stp_pr'],
						__class__.__name__ + '_name_stp_minmax': config.cfg[__class__.__name__ + '_name_stp_minmax'],
						__class__.__name__ + '_real_test': config.cfg[__class__.__name__ + '_real_test'],
						__class__.__name__ + '_flag_learning': config.cfg[__class__.__name__ + '_flag_learning'],
						__class__.__name__ + '_pic_save': config.cfg[__class__.__name__ + '_pic_save']
						})


	#Finding Divergences:
	def divergence(self):

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

		self.type_signal(extremes = extreme_min, signal = 'buy', type = 'primary')
		

		


	def calculator_macd(self):

		symbol = self.elements[__class__.__name__ + '_symbol']
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

		extreme_max = extreme_max.assign(
										max_1 = extreme_max.shift(periods = 1, fill_value = -np.inf)['max'],
										max_2 = extreme_max.shift(periods = 2, fill_value = -np.inf)['max'],
										max_3 = extreme_max.shift(periods = 3, fill_value = -np.inf)['max'],
										max_4 = extreme_max.shift(periods = 4, fill_value = -np.inf)['max'],
										max_5 = extreme_max.shift(periods = 5, fill_value = -np.inf)['max'],
										max_6 = extreme_max.shift(periods = 6, fill_value = -np.inf)['max'],
										)

		return extreme_max, extreme_min

	@stTime
	def type_signal(self, extremes, signal, type):

		if self.cfg[__class__.__name__ + '_' + signal + '_doing']: #Example buy_doing True

			
			#print(extremes)

			macd_div_1 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_1'], True)).where(extremes['min'] > extremes['min_1'], False),
										'index': extremes['index'],
										}
									)
			
			macd_div_2 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_2'], True)).where(extremes['min'] > extremes['min_2'], False),
										'index': extremes['index'],
										}
									)
			macd_div_3 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_3'], True)).where(extremes['min'] > extremes['min_3'], False),
										'index': extremes['index'],
										}
									)
			macd_div_4 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_4'], True)).where(extremes['min'] > extremes['min_4'], False),
										'index': extremes['index'],
										}
									)
			macd_div_5 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_5'], True)).where(extremes['min'] > extremes['min_5'], False),
										'index': extremes['index'],
										}
									)
			macd_div_6 = pd.DataFrame(
										{
										'div': ((extremes['min'].copy(deep = True)).mask(extremes['min'] > extremes['min_6'], True)).where(extremes['min'] > extremes['min_6'], False),
										'index': extremes['index'],
										}
									)

			dataset_5M_div = self.dataset_preparer(index = macd_div_1)
			macd_div_1 = macd_div_1[macd_div_1['div'] == True].reset_index(inplace = False, drop = True)
			print(macd_div_1)
			print(dataset_5M_div)
			data_div_1 = ((dataset_5M_div['low_front'].copy(deep = True)).mask(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], True)).where(dataset_5M_div['low_front'] < dataset_5M_div['low_back'], False)
			print(data_div_1[data_div_1 == True])
			# data_div_2 = ((dataset_5M_div['low'].copy(deep = True)).mask(dataset_5M_div['low'] < dataset_5M_div['low_2'], True)).where(dataset_5M_div['low'] < dataset_5M_div['low_2'], False)
			# data_div_3 = ((dataset_5M_div['low'].copy(deep = True)).mask(dataset_5M_div['low'] < dataset_5M_div['low_3'], True)).where(dataset_5M_div['low'] < dataset_5M_div['low_3'], False)
			# data_div_4 = ((dataset_5M_div['low'].copy(deep = True)).mask(dataset_5M_div['low'] < dataset_5M_div['low_4'], True)).where(dataset_5M_div['low'] < dataset_5M_div['low_4'], False)
			# data_div_5 = ((dataset_5M_div['low'].copy(deep = True)).mask(dataset_5M_div['low'] < dataset_5M_div['low_5'], True)).where(dataset_5M_div['low'] < dataset_5M_div['low_5'], False)
			# data_div_6 = ((dataset_5M_div['low'].copy(deep = True)).mask(dataset_5M_div['low'] < dataset_5M_div['low_6'], True)).where(dataset_5M_div['low'] < dataset_5M_div['low_6'], False)

			# # print(macd_div_1)
			# # print(data_div_1)
			# # print(macd_div_1 * data_div_1)
			# extremes.assign(
			# 				div_1 = extremes[extremes['min'] > extremes['min_1']]
			# 				)

			# print(pd.where(
			# 					(extremes['min'] > extremes['min_1']),True,False
			# 					))

	#@stTime
	def dataset_preparer(self, index):

		symbol = self.elements[__class__.__name__ + '_symbol']
		dataset_5M_ = self.elements['dataset_5M'][symbol].loc[:, ['high', 'low']].copy(deep = True)

		div_index_list_front = list((index['index'].where(index['div'] == True)).dropna(inplace = False).index)
		div_index_list_back = list((index['index'].where(index['div'] == True)).dropna(inplace = False).index - 1)

		dataset_5M_div = pd.DataFrame(
									{
										'low_front': dataset_5M_['low'][index['index'][div_index_list_front]].values,
										'low_back': dataset_5M_['low'][index['index'][div_index_list_back]].values,
										'high_front': dataset_5M_['low'][index['index'][div_index_list_front]].values,
										'high_back': dataset_5M_['low'][index['index'][div_index_list_back]].values,
									}
									)

		return dataset_5M_div



from Mt5_LoginGetData import LoginGetData as getdata

loging = getdata()


parameters = Parameters()
config = Config()

parameters.elements['dataset_5M'], parameters.elements['dataset_1H'] = loging.readall(symbol = 'XAUUSD_i', number_5M = 99800, number_1H = 500)
parameters.elements['Divergence_symbol'] = 'XAUUSD_i'
parameters.elements['Divergence_apply_to'] = 'close'

macd = Divergence(parameters = parameters, config = config)
print(macd.divergence())