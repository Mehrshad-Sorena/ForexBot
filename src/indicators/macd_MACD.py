import pandas_ta as ind
import pandas as pd
import numpy as np
from macd_Chromosome import Chromosome
import os
from macd_Config import Config as MACDConfig
from macd_Parameters import Parameters as MACDParameters

from indicator_Parameters import Parameters as IndicatorParameters

from progress.bar import Bar
from random import randint
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config

from pr_Parameters import Parameters as PRParameters
from pr_Config import Config as PRConfig

from timer import stTime

from indicator_Divergence import Divergence
from indicator_Tester import Tester

from pr_Runner import Runner

#Functions Used:

#calculator_macd(self)

#/////////////////////////////////

class MACD:

	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({
							#*********************

							__class__.__name__ + '_fast': parameters.elements[__class__.__name__ + '_fast'],
							__class__.__name__ + '_slow': parameters.elements[__class__.__name__ + '_slow'],
							__class__.__name__ + '_signal': parameters.elements[__class__.__name__ + '_signal'],

							__class__.__name__ + '_apply_to': parameters.elements[__class__.__name__ + '_apply_to'],

							'symbol': parameters.elements['symbol'],

							#///////////////////////

							#Globals:

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],

							#/////////////////////////
							})

		self.cfg = dict({

						})


	def ParameterReader(self, symbol, signaltype, signalpriority):

		macd_config = MACDConfig()
		path_superhuman = macd_config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'

		macd_parameters = MACDParameters()

		pr_parameters = PRParameters()
		pr_config = PRConfig()

		ind_parameters = IndicatorParameters()


		if os.path.exists(path_superhuman + symbol + '.csv'):

			GL_Results = pd.read_csv(path_superhuman + symbol + '.csv')

			for elm in GL_Results.columns:

				for pr_param_elm in pr_parameters.elements.keys():
					if pr_param_elm == elm:

						if (
							elm == 'BestFinder_alpha_low' or
							elm == 'BestFinder_alpha_high' or
							elm == 'st_percent_min' or
							elm == 'st_percent_max' or
							elm == 'tp_percent_min' or
							elm == 'tp_percent_max'
							):
							pr_parameters.elements[pr_param_elm] = GL_Results[elm][0]
						else:
							pr_parameters.elements[pr_param_elm] = int(GL_Results[elm][0])

				for pr_conf_elm in pr_config.cfg.keys():
					if pr_conf_elm == elm:
						pr_config.cfg[pr_conf_elm] = GL_Results[elm][0]


				for ind_elm in ind_parameters.elements.keys():
					if ind_elm == elm:

						if elm == 'BestFinder_alpha':
							ind_parameters.elements[ind_elm] = GL_Results[elm][0]
						else:
							ind_parameters.elements[ind_elm] = int(GL_Results[elm][0])


				for macd_elm in macd_parameters.elements.keys():
					if macd_elm == elm:
						if elm == 'MACD_apply_to':
							macd_parameters.elements[macd_elm] = GL_Results[elm][0]
						else:
							macd_parameters.elements[macd_elm] = int(GL_Results[elm][0])

			return GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters, pr_config

		else:
			return pd.DataFrame(), '', '', '', '', ''



	@stTime
	def Simulator(self, dataset_5M, dataset_1H, symbol, signaltype, signalpriority, flag_savepic):


		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters, pr_config = self.ParameterReader(
										 																				symbol = symbol, 
										 																				signaltype = signaltype, 
										 																				signalpriority = signalpriority
										 																				)

		ind_parameters.elements['dataset_5M'] = dataset_5M
		ind_parameters.elements['dataset_1H'] = dataset_1H
		ind_config = indicator_config()
		macd_tester = Tester(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		cut_first = 0

		output = pd.DataFrame()

		for candle_counter in range(17999, len(dataset_5M[symbol]['close'])):

			if candle_counter >= 17999:
				cut_first = candle_counter - 17999

			self.elements['dataset_5M'] = {
											symbol:	dataset_5M[symbol].loc[cut_first:candle_counter,['close', 'open', 'high', 'low', 'HL/2', 'HLC/3', 'HLCC/4', 'OHLC/4', 'time']],
											}

			macd = Divergence(parameters = ind_parameters, config = ind_config)

			

			signal = pd.DataFrame()

			try:	

				macd_calc = self.calculator_macd()

				signal, _, indicator = macd.divergence(
												sigtype = signaltype,
												sigpriority = signalpriority,
												indicator = macd_calc,
												column_div = GL_Results['MACD_column_div'][0],
												ind_name = 'macd',
												dataset_5M = self.elements['dataset_5M'],
												dataset_1H = dataset_1H,
												symbol = symbol,
												flaglearn = GL_Results['islearned'][0],
												flagtest = True
												)
			except Exception as ex:
				#print(f"LastSignal {signaltype} {signalpriority}: {ex}")
				signal = pd.DataFrame()
			
			if signal.empty == False:
				lst_idx = signal['index'].iloc[-1]
			else:
				lst_idx = 0

			if np.max(self.elements['dataset_5M'][symbol]['close'].index) - 1 - lst_idx <= 6:

				sig = signal.loc[[lst_idx], 
										[
										'index', 
										'indicator_front', 
										'indicator_back', 
										'index_back', 
										'low_front', 
										'low_back', 
										'high_front', 
										'high_back',
										'time_low_front',
										'time_low_back',
										'time_high_front',
										'time_high_back',
										'div',
										'diff_extereme',
										'signal',
										'indicator_name',
										'column_div',
										'symbol'
										]]

				output = pd.concat([output , sig], ignore_index = True)
				print('lst_idx = ', lst_idx)

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print(output)

		signal_output = pd.DataFrame()
		learning_output = pd.DataFrame()

		try:
			signal_output, learning_output = macd_tester.RunGL(
															signal = output, 
															sigtype = signaltype, 
															flaglearn = GL_Results['islearned'][0], 
															flagtest = True,
															pr_parameters = pr_parameters,
															pr_config = pr_config,
															indicator = indicator,
															flag_savepic = flag_savepic
															)

		except Exception as ex:
			print('ERROR PR Last Signal: ',ex)
			signal_output = pd.DataFrame()
			learning_output = pd.DataFrame()

		return signal_output, learning_output


	@stTime
	def LastSignal(self,dataset_5M, dataset_1H, symbol):

		#BUY Primary:

		signaltype = 'buy'
		signalpriority = 'primary'

		macd_config = MACDConfig()
		path_superhuman = macd_config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'

		if not os.path.exists(path_superhuman + symbol + '.csv'): return 'no_trade', 0, 0

		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters_buy_primary, pr_config_buy_primary = self.ParameterReader(
												 																				symbol = symbol, 
												 																				signaltype = signaltype, 
												 																				signalpriority = signalpriority
												 																				)

		ind_config = indicator_config()
		macd = Divergence(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		macd_calc = self.calculator_macd()

		signal_buy_primary = pd.DataFrame()

		try:

			if GL_Results['permit'][0] == True:

				signal_buy_primary, _, _ = macd.divergence(
															sigtype = signaltype,
															sigpriority = signalpriority,
															indicator = macd_calc,
															column_div = GL_Results['MACD_column_div'][0],
															ind_name = 'macd',
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															flaglearn = GL_Results['islearned'][0],
															flagtest = True
															)
			else:
				lst_idx_buy_primary = 0

		except Exception as ex:
			print(f"LastSignal {signaltype} {signalpriority}: {ex}")
			signal_buy_primary = pd.DataFrame()

		if signal_buy_primary.empty == False:
			lst_idx_buy_primary = int(signal_buy_primary['index'].iloc[-1])

		else:
			lst_idx_buy_primary = 0

		#*****************************


		#BUY Secondry:

		signaltype = 'buy'
		signalpriority = 'secondry'

		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters_buy_secondry, pr_config_buy_secondry = self.ParameterReader(
													 																				symbol = symbol, 
													 																				signaltype = signaltype, 
													 																				signalpriority = signalpriority
													 																				)

		ind_config = indicator_config()
		macd = Divergence(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		macd_calc = self.calculator_macd()

		signal_buy_secondry = pd.DataFrame()

		try:

			if GL_Results['permit'][0] == True:
				
				signal_buy_secondry, _, _ = macd.divergence(
															sigtype = signaltype,
															sigpriority = signalpriority,
															indicator = macd_calc,
															column_div = GL_Results['MACD_column_div'][0],
															ind_name = 'macd',
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															flaglearn = GL_Results['islearned'][0],
															flagtest = True
															)
			else:
				signal_buy_secondry = 0

		except Exception as ex:
			print(f"LastSignal {signaltype} {signalpriority}: {ex}")
			signal_buy_secondry = pd.DataFrame()

		if signal_buy_secondry.empty == False:
			lst_idx_buy_secondry = int(signal_buy_secondry['index'].iloc[-1])

		else:
			signal_buy_secondry = 0

		#*****************************


		#SELL Primary:

		signaltype = 'sell'
		signalpriority = 'primary'

		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters_sell_primary, pr_config_sell_primary = self.ParameterReader(
													 																				symbol = symbol, 
													 																				signaltype = signaltype, 
													 																				signalpriority = signalpriority
													 																				)

		ind_config = indicator_config()
		macd = Divergence(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		macd_calc = self.calculator_macd()

		signal_sell_primary = pd.DataFrame()

		try:
			if GL_Results['permit'][0] == True:

				signal_sell_primary, _, _ = macd.divergence(
															sigtype = signaltype,
															sigpriority = signalpriority,
															indicator = macd_calc,
															column_div = GL_Results['MACD_column_div'][0],
															ind_name = 'macd',
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															flaglearn = GL_Results['islearned'][0],
															flagtest = True
															)
			else:
				lst_idx_sell_primary = 0

		except Exception as ex:
			print(f"LastSignal {signaltype} {signalpriority}: {ex}")
			signal_sell_primary = pd.DataFrame()

		if signal_sell_primary.empty == False:
			lst_idx_sell_primary = int(signal_sell_primary['index'].iloc[-1])

		else:
			lst_idx_sell_primary = 0

		#*****************************


		#SELL Secondry:

		signaltype = 'sell'
		signalpriority = 'secondry'

		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters_sell_secondry, pr_config_sell_secondry = self.ParameterReader(
													 																				symbol = symbol, 
													 																				signaltype = signaltype, 
													 																				signalpriority = signalpriority
													 																				)

		ind_config = indicator_config()
		macd = Divergence(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		macd_calc = self.calculator_macd()

		signal_sell_secondry = pd.DataFrame()

		try:
			if GL_Results['permit'][0] == True:

				signal_sell_secondry, _, _ = macd.divergence(
															sigtype = signaltype,
															sigpriority = signalpriority,
															indicator = macd_calc,
															column_div = GL_Results['MACD_column_div'][0],
															ind_name = 'macd',
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															flaglearn = GL_Results['islearned'][0],
															flagtest = True
															)
			else:
				lst_idx_sell_secondry = 0

		except Exception as ex:
			print(f"LastSignal {signaltype} {signalpriority}: {ex}")
			signal_sell_secondry = pd.DataFrame()


		if signal_sell_secondry.empty == False:
			lst_idx_sell_secondry = int(signal_sell_secondry['index'].iloc[-1])

		else:
			lst_idx_sell_secondry = 0

		#*****************************

		print('lst_idx_buy_primary = ', lst_idx_buy_primary)
		print('lst_idx_buy_secondry = ', lst_idx_buy_secondry)
		print('lst_idx_sell_primary = ', lst_idx_sell_primary)
		print('lst_idx_sell_secondry = ', lst_idx_sell_secondry)
		print('len data = ', len(dataset_5M[symbol]['close']) - 1)

		#***** Last Signal:

		if (
			lst_idx_buy_primary > lst_idx_sell_primary and
			lst_idx_buy_primary > lst_idx_sell_secondry and
			lst_idx_buy_primary >= lst_idx_buy_secondry and
			(len(dataset_5M[symbol]['close']) - 1 - lst_idx_buy_primary) <= 6
			):

			print('======> last signal buy primary ',symbol)
			print('dataset length: ',len(dataset_5M[symbol]['close']))
			print('last index: ',lst_idx_buy_primary)
			

			if lst_idx_buy_primary != 0:

				res_pro_buy_primary = pd.DataFrame()
				try:
					res_pro_buy_primary = self.ProfitFinder(
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															signal = signal_buy_primary, 
															sigtype = 'buy', 
															pr_parameters = pr_parameters_buy_primary, 
															pr_config = pr_config_buy_primary
															)
				except Exception as ex:
					print('ERROR PR Last Signal: ',ex)
					res_pro_buy_primary = pd.DataFrame()


				if (res_pro_buy_primary.empty == False):

					diff_pr_top_buy_primary = (((res_pro_buy_primary['high_upper'][int(lst_idx_buy_primary)]) - dataset_5M[symbol]['high'][int(lst_idx_buy_primary)])/dataset_5M[symbol]['high'][int(lst_idx_buy_primary)]) * 100
					diff_pr_down_buy_primary = ((dataset_5M[symbol]['low'][int(lst_idx_buy_primary)] - (res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)]))/dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]) * 100

					# if type(diff_pr_down_buy_primary) is np.ndarray:
					# 	res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]*(1-(diff_pr_down_buy_primary[0]/100))
					# else:
					# 	res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]*(1-(diff_pr_down_buy_primary/100))

					if diff_pr_top_buy_primary > pr_parameters_buy_primary.elements['tp_percent_max']:
						diff_pr_top_buy_primary = pr_parameters_buy_primary.elements['tp_percent_max']
						res_pro_buy_primary['high_upper'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['high'][int(lst_idx_buy_primary)]*(1+(diff_pr_top_buy_primary/100))

					if diff_pr_down_buy_primary > pr_parameters_buy_primary.elements['st_percent_max']:
						diff_pr_down_buy_primary = pr_parameters_buy_primary.elements['st_percent_max']
						res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]*(1-(diff_pr_down_buy_primary/100))


					resist_buy = (res_pro_buy_primary['high_upper'][int(lst_idx_buy_primary)])
					protect_buy = (res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)])

					signal = 'buy_primary'

				else:
					diff_pr_top_buy = 0
					diff_pr_down_buy = 0
					diff_pr_top_buy_power = 0
					diff_pr_down_buy_power = 0

					resist_buy = 0
					protect_buy = 0

					signal = 'no_trade'		

			print('================================')\

		elif (
			lst_idx_buy_secondry > lst_idx_sell_primary and
			lst_idx_buy_secondry > lst_idx_sell_secondry and
			lst_idx_buy_secondry > lst_idx_buy_primary and
			(len(dataset_5M[symbol]['close']) - 1 - lst_idx_buy_secondry) <= 6
			):

			print('======> last signal buy secondry ',symbol)
			print('dataset length: ',len(dataset_5M[symbol]['close']))
			print('last index: ',lst_idx_buy_secondry)
			


			if lst_idx_buy_secondry != 0:

				res_pro_buy_secondry = pd.DataFrame()
				try:
					res_pro_buy_secondry = self.ProfitFinder(
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															signal = signal_buy_secondry, 
															sigtype = 'buy', 
															pr_parameters = pr_parameters_buy_secondry, 
															pr_config = pr_config_buy_secondry
															)
				except Exception as ex:
					print('ERROR PR Last Signal: ',ex)
					res_pro_buy_secondry = pd.DataFrame()

				if (res_pro_buy_secondry.empty == False):

					diff_pr_top_buy_secondry = (((res_pro_buy_secondry['high_upper'][int(lst_idx_buy_secondry)]) - dataset_5M[symbol]['high'][int(lst_idx_buy_secondry)])/dataset_5M[symbol]['high'][int(lst_idx_buy_secondry)]) * 100
					diff_pr_down_buy_secondry = ((dataset_5M[symbol]['low'][int(lst_idx_buy_secondry)] - (res_pro_buy_secondry['low_lower'][int(lst_idx_buy_secondry)]))/dataset_5M[symbol]['low'][int(lst_idx_buy_secondry)]) * 100

					# if type(diff_pr_down_buy_primary) is np.ndarray:
					# 	res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]*(1-(diff_pr_down_buy_primary[0]/100))
					# else:
					# 	res_pro_buy_primary['low_lower'][int(lst_idx_buy_primary)] = dataset_5M[symbol]['low'][int(lst_idx_buy_primary)]*(1-(diff_pr_down_buy_primary/100))

					if diff_pr_top_buy_secondry > pr_parameters_buy_secondry.elements['tp_percent_max']:
						diff_pr_top_buy_secondry = pr_parameters_buy_secondry.elements['tp_percent_max']
						res_pro_buy_secondry['high_upper'][int(lst_idx_buy_secondry)] = dataset_5M[symbol]['high'][int(lst_idx_buy_secondry)]*(1+(diff_pr_top_buy_secondry/100))

					if diff_pr_down_buy_secondry > pr_parameters_buy_secondry.elements['st_percent_max']:
						diff_pr_down_buy_secondry = pr_parameters_buy_secondry.elements['st_percent_max']
						res_pro_buy_secondry['low_lower'][int(lst_idx_buy_secondry)] = dataset_5M[symbol]['low'][int(lst_idx_buy_secondry)]*(1-(diff_pr_down_buy_secondry/100))


					resist_buy = (res_pro_buy_secondry['high_upper'][int(lst_idx_buy_secondry)])
					protect_buy = (res_pro_buy_secondry['low_lower'][int(lst_idx_buy_secondry)])

					signal = 'buy_secondry'

				else:
					diff_pr_top_buy = 0
					diff_pr_down_buy = 0
					diff_pr_top_buy_power = 0
					diff_pr_down_buy_power = 0

					resist_buy = 0
					protect_buy = 0

					signal = 'no_trade'	

		elif (
			lst_idx_sell_primary > lst_idx_buy_primary and
			lst_idx_sell_primary >= lst_idx_sell_secondry and
			lst_idx_sell_primary > lst_idx_buy_secondry and
			(len(dataset_5M[symbol]['close']) - 1 - lst_idx_sell_primary) <= 6
			):

			print('======> last signal sell primary ',symbol)
			print('dataset length: ',len(dataset_5M[symbol]['close']))
			print('last index: ',lst_idx_sell_primary)
			

			if lst_idx_sell_primary != 0:

				res_pro_sell_primary = pd.DataFrame()
				try:
					res_pro_sell_primary = self.ProfitFinder(
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															signal = signal_sell_primary, 
															sigtype = 'sell', 
															pr_parameters = pr_parameters_sell_primary, 
															pr_config = pr_config_sell_primary
															)
				except Exception as ex:
					print('ERROR PR Last Signal: ',ex)
					res_pro_sell_primary = pd.DataFrame()


				if (res_pro_sell_primary.empty == False):

					diff_pr_top_sell_primary = (((res_pro_sell_primary['high_upper'][int(lst_idx_sell_primary)]) - dataset_5M[symbol]['high'][int(lst_idx_sell_primary)])/dataset_5M[symbol]['high'][int(lst_idx_sell_primary)]) * 100
					diff_pr_down_sell_primary = ((dataset_5M[symbol]['low'][int(lst_idx_sell_primary)] - (res_pro_sell_primary['low_lower'][int(lst_idx_sell_primary)]))/dataset_5M[symbol]['low'][int(lst_idx_sell_primary)]) * 100


					if diff_pr_top_sell_primary > pr_parameters_sell_primary.elements['st_percent_max']:
						diff_pr_top_sell_primary = pr_parameters_sell_primary.elements['st_percent_max']
						(res_pro_sell_primary['high_upper'][int(lst_idx_sell_primary)]) = dataset_5M[symbol]['high'][int(lst_idx_sell_primary)]*(1+(diff_pr_top_sell_primary/100))

					if diff_pr_down_sell_primary > pr_parameters_sell_primary.elements['tp_percent_max']:
						diff_pr_down_sell_primary = pr_parameters_sell_primary.elements['tp_percent_max']
						(res_pro_sell_primary['low_lower'][int(lst_idx_sell_primary)]) = dataset_5M[symbol]['low'][int(lst_idx_sell_primary)]*(1-(diff_pr_down_sell_primary/100))
						

					resist_sell = (res_pro_sell_primary['high_upper'][int(lst_idx_sell_primary)])
					protect_sell = (res_pro_sell_primary['low_lower'][int(lst_idx_sell_primary)])

					signal = 'sell_primary'

				else:
					diff_pr_top_sell_primary = 0
					diff_pr_down_sell_primary = 0

					resist_sell = 0
					protect_sell = 0

					signal = 'no_trade'

		
		elif (
			lst_idx_sell_secondry > lst_idx_buy_primary and
			lst_idx_sell_secondry > lst_idx_sell_primary and
			lst_idx_sell_secondry > lst_idx_buy_secondry and
			(len(dataset_5M[symbol]['close']) - 1 - lst_idx_sell_secondry) <= 6
			):

			print('======> last signal sell secondry ',symbol)
			print('dataset length: ',len(dataset_5M[symbol]['close']))
			print('last index: ',lst_idx_sell_secondry)

			if lst_idx_sell_secondry != 0:

				res_pro_sell_secondry = pd.DataFrame()
				try:
					res_pro_sell_secondry = self.ProfitFinder(
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															signal = signal_sell_secondry, 
															sigtype = 'sell', 
															pr_parameters = pr_parameters_sell_secondry, 
															pr_config = pr_config_sell_secondry
															)
				except Exception as ex:
					print('ERROR PR Last Signal: ',ex)
					res_pro_sell_secondry = pd.DataFrame()


				if (res_pro_sell_secondry.empty == False):

					diff_pr_top_sell_secondry = (((res_pro_sell_secondry['high_upper'][int(lst_idx_sell_secondry)]) - dataset_5M[symbol]['high'][int(lst_idx_sell_secondry)])/dataset_5M[symbol]['high'][int(lst_idx_sell_secondry)]) * 100
					diff_pr_down_sell_secondry = ((dataset_5M[symbol]['low'][int(lst_idx_sell_secondry)] - (res_pro_sell_secondry['low_lower'][int(lst_idx_sell_secondry)]))/dataset_5M[symbol]['low'][int(lst_idx_sell_secondry)]) * 100


					if diff_pr_top_sell_secondry > pr_parameters_sell_secondry.elements['st_percent_max']:
						diff_pr_top_sell_secondry = pr_parameters_sell_secondry.elements['st_percent_max']
						(res_pro_sell_secondry['high_upper'][int(lst_idx_sell_secondry)]) = dataset_5M[symbol]['high'][int(lst_idx_sell_secondry)]*(1+(diff_pr_top_sell_secondry/100))

					if diff_pr_down_sell_secondry > pr_parameters_sell_secondry.elements['tp_percent_max']:
						diff_pr_down_sell_secondry = pr_parameters_sell_secondry.elements['tp_percent_max']
						(res_pro_sell_secondry['low_lower'][int(lst_idx_sell_secondry)]) = dataset_5M[symbol]['low'][int(lst_idx_sell_secondry)]*(1-(diff_pr_down_sell_secondry/100))
						

					resist_sell = (res_pro_sell_secondry['high_upper'][int(lst_idx_sell_secondry)])
					protect_sell = (res_pro_sell_secondry['low_lower'][int(lst_idx_sell_secondry)])
					
					signal = 'sell_secondry'

				else:
					diff_pr_top_sell_secondry = 0
					diff_pr_down_sell_secondry = 0

					resist_sell = 0
					protect_sell = 0

					signal = 'no_trade'			

			print('================================')
		else:
			resist_sell = 0
			protect_sell = 0

			signal = 'no_trade'	

		if (
			signal == 'buy_primary' or
			signal == 'buy_secondry'
			):
			return signal, resist_buy, protect_buy
		elif (
			signal == 'sell_primary' or
			signal == 'sell_secondry'
			):
			return signal, protect_sell, resist_sell
		else:
			return signal, 0, 0


	#ProfitFinder For Last Signal:

	def ProfitFinder(self, dataset_5M,dataset_1H, symbol, signal, sigtype, pr_parameters, pr_config):

		#*************************************************************
		# Bayad Maghadir Baraye Params Va Config As func baraye PR dar GA , Learner daryaft beshan

		#/////////////////////////////////////////////////////////////

		pr_Runner = Runner(parameters = pr_parameters, config = pr_config)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig1 = ',signal['index'].iloc[-1])

		signals = pd.DataFrame(
								{
									'index': signal['index'].iloc[-1], 
								},
								index = [signal['index'].iloc[-1]]
								)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig1 = ',signals)

		signals = pr_Runner.run(
								dataset_5M = dataset_5M[symbol], 
								dataset_1H = dataset_1H[symbol],
								signals_index = signals,
								sigtype = sigtype,
								flaglearn = True,
								flagtest = False,
								indicator = 'macd',
								signals = signal,
								flag_savepic = False
								)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig2 = ',signal)

		signal = signal.drop(columns = ['index'], inplace = False)

		signal = signal.join(signals).dropna(inplace = False)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig2 = ',signal)

		return signal


	#/////////////////////////////





	def GetPermit(self,dataset_5M, dataset_1H, symbol, signaltype, signalpriority, flag_savepic):

		GL_Results, path_superhuman, macd_parameters, ind_parameters, pr_parameters, pr_config = self.ParameterReader(
									 																				symbol = symbol, 
									 																				signaltype = signaltype, 
									 																				signalpriority = signalpriority
									 																				)

		ind_config = indicator_config()
		macd = Divergence(parameters = ind_parameters, config = ind_config)

		ind_parameters.elements['dataset_5M'] = dataset_5M
		ind_parameters.elements['dataset_1H'] = dataset_1H
		macd_tester = Tester(parameters = ind_parameters, config = ind_config)

		self.elements = macd_parameters.elements
		self.elements['dataset_5M'] = dataset_5M
		self.elements['dataset_1H'] = dataset_1H
		self.elements['symbol'] = symbol

		macd_calc = self.calculator_macd()

		try:

			signal, signaltype, indicator = macd.divergence(
															sigtype = signaltype,
															sigpriority = signalpriority,
															indicator = macd_calc,
															column_div = GL_Results['MACD_column_div'][0],
															ind_name = 'macd',
															dataset_5M = dataset_5M,
															dataset_1H = dataset_1H,
															symbol = symbol,
															flaglearn = GL_Results['islearned'][0],
															flagtest = True
															)
			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print(signal)

			signal_output, learning_output = macd_tester.RunGL(
																signal = signal, 
																sigtype = signaltype, 
																flaglearn = GL_Results['islearned'][0], 
																flagtest = True,
																pr_parameters = pr_parameters,
																pr_config = pr_config,
																indicator = indicator,
																flag_savepic = flag_savepic
																)
		except Exception as ex:
			print('Permit Error: ', ex)

			signal_output = pd.DataFrame()
			learning_output = pd.DataFrame()

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('signals = ', signal_output)

		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print('learning = ', learning_output)

		if learning_output.empty == False:

			if learning_output['score'][0] >= GL_Results['score'][0] * 0.9:
				GL_Results['permit'] = [True]
				GL_Results['score'][0] = learning_output['score'][0]

			else:
				GL_Results['permit'] = [False]
				GL_Results['score'][0] = learning_output['score'][0]

		else:
			GL_Results['permit'] = [False]
			GL_Results['score'][0] = 0

		if os.path.exists(path_superhuman + symbol + '.csv'):
			os.remove(path_superhuman + symbol + '.csv')

		GL_Results.to_csv(path_superhuman + symbol + '.csv')


	def Genetic(self, dataset_5M, dataset_1H, symbol, signaltype, signalpriority, num_turn):

		if symbol == 'ETHUSD_i':
			self.elements['st_percent_up'] = 2000
			self.elements['st_percent_down'] = 1500
			self.elements['tp_percent_up'] = 2000
			self.elements['tp_percent_down'] = 1500
		else:
			self.elements['st_percent_up'] = 120
			self.elements['st_percent_down'] = 90
			self.elements['tp_percent_up'] = 120
			self.elements['tp_percent_down'] = 90

		chrom = Chromosome(parameters = self)
		macd_config = MACDConfig()
		path_elites_chromosome = macd_config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/' + symbol + '_ChromosomeResults.csv'
		
		while not chrom.Get(
							work = 'Optimize',
							signaltype = signaltype,
							signalpriority = signalpriority,
							symbol = symbol,
							number_chromos = 10,
							Chromosome = '',
							chrom_counter = 0,
							path_elites_chromosome = path_elites_chromosome,
							alpha = 0.2
							):
			pass

		chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'BigBang',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 10,
																							Chromosome = '',
																							chrom_counter = 0
																							)

		macd_config = MACDConfig()
		path_superhuman = macd_config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'
		path_elites = macd_config.cfg['path_elites'] + signalpriority + '/' + signaltype + '/'

		if os.path.exists(path_superhuman + symbol + '.csv'):
			max_score_gl = pd.read_csv(path_superhuman + symbol + '.csv')['score'][0]
		else:
			max_score_gl = 0.00001

		max_score_gl = 0.00001


		print('================================ START Genetic ',signaltype,' ===> ',symbol,' ',signalpriority)
		print('\n')

		learning_output_before = pd.DataFrame()

		if (
			os.path.exists(path_elites + symbol + '_LearningResults.csv') and
			os.path.exists(path_elites + symbol + '_ChromosomeResults.csv')
			):

			learning_result = pd.read_csv(path_elites + symbol + '_LearningResults.csv').drop(columns='Unnamed: 0')
			chromosome_output = pd.read_csv(path_elites + symbol + '_ChromosomeResults.csv').drop(columns='Unnamed: 0')

			if num_turn <= len(learning_result['score']):
				num_turn = (len(learning_result['score'])) + 2

				if len(chromosome_output) >= num_turn:
					num_turn = len(chromosome_output) + 2

			num_turn = 40

		else:
			learning_result = pd.DataFrame()
			chromosome_output = pd.DataFrame()

		

		chrom_counter = 0
		all_chorms = 0
		chorm_reset_counter = 0
		bad_score_counter = 0
		bad_score_counter_2 = 0
		score = max_score_gl
		score_for_reset = 0

		learning_interval_counter = 0
		learn_counter = 1

		bar = Bar(signaltype + ' ' + signalpriority, max = int(num_turn))

		for i in range(len(chromosome)):

			if (
				chromosome[chrom_counter]['score'] != 0 and
				chromosome[chrom_counter]['islearned'] == True and
				chromosome[chrom_counter]['isborn'] == False
				):
				chrom_counter += 1
				continue


		if chrom_counter >= len(chromosome):
			chrom_counter = 0
			print("Group Sex Start")
			chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																								work = 'group_sex',
																								signaltype = signaltype,
																								signalpriority = signalpriority,
																								symbol = symbol,
																								number_chromos = 0,
																								Chromosome = chromosome,
																								chrom_counter = chrom_counter
																								)
			print("Group Sex Finish")

		#print(chrom_counter)




		while chrom_counter < len(chromosome):

			if chromosome == 'End_of_Chromosomes':
				# print(chromosome)
				break

			# print()
			# print('================== Num Symbol ==>',symbol, ' ' , signaltype, ' ',signalpriority)
			# print()
			# print('================== Num =========> ', len(chromosome_output))
			# print('================== Num Chroms ======> ', chrom_counter)
			# print('================== All Chorms ======> ', all_chorms)
			# print('================== Flag Learn ======> ', chromosome[chrom_counter]['islearned'])
			# print('================== Chorm Reseter ===> ',chorm_reset_counter)
			# print('===== bad score counter ========> ',bad_score_counter)
			# print('===== bad score counter 2 ======> ',bad_score_counter_2)
			# print()
			bar.next()

			

			if (chorm_reset_counter >= 27):
				chorm_reset_counter = 0
				
				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'fucker_0',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 0,
																							Chromosome = chromosome,
																							chrom_counter = chrom_counter
																							)


				all_chorms += 1
				continue

			if all_chorms >= int(num_turn): break
			all_chorms += 1


			self.elements = macd_parameters.elements
			self.elements['dataset_5M'] = dataset_5M
			self.elements['dataset_1H'] = dataset_1H
			self.elements['symbol'] = symbol

			macd_calc = self.calculator_macd()

			ind_config = indicator_config()
			macd = Divergence(parameters = ind_parameters, config = ind_config)

			try:

				signal, signaltype, indicator = macd.divergence(
																sigtype = signaltype,
																sigpriority = signalpriority,
																indicator = macd_calc,
																column_div = chromosome[chrom_counter]['MACD_column_div'],
																ind_name = 'macd',
																dataset_5M = dataset_5M,
																dataset_1H = dataset_1H,
																symbol = symbol,
																flaglearn = chromosome[chrom_counter]['islearned'],
																flagtest = True
																)
				chromosome[chrom_counter]['isborn'] = False

			except Exception as ex:
				# print('Divergence Error: ',ex)
				signal = pd.DataFrame()
				signal_output = pd.DataFrame()
				learning_output_now = pd.DataFrame()
				learning_output_before = pd.DataFrame()

			#print('siiiiiiignaaaaaal ====> ', len(signal['index']))

			if signal.empty == True:
				chromosome[chrom_counter]['isborn'] = False
				chromosome[chrom_counter]['islearned'] = True
				chromosome[chrom_counter]['score'] = -1

				_, _, _, _, _ = chrom.Get(
											work = 'graveyard',
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											number_chromos = 0,
											Chromosome = chromosome,
											chrom_counter = chrom_counter
											)

				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'fucker_0',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 0,
																							Chromosome = chromosome,
																							chrom_counter = chrom_counter
																							)
				continue

			ind_parameters.elements['dataset_5M'] = dataset_5M
			ind_parameters.elements['dataset_1H'] = dataset_1H

			macd_tester = Tester(parameters = ind_parameters, config = ind_config)
			try:

				signal_output, learning_output_now = macd_tester.RunGL(
																	signal = signal, 
																	sigtype = signaltype, 
																	flaglearn = chromosome[chrom_counter]['islearned'], 
																	flagtest = True,
																	pr_parameters = pr_parameters,
																	pr_config = pr_config,
																	indicator = indicator,
																	flag_savepic = False
																	)

			except Exception as ex:
				# print('Learning Error: ',ex)
				# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				# 	print(signal)
				signal_output = pd.DataFrame()
				learning_output_now = pd.DataFrame()
				learning_output_before = pd.DataFrame()

			if (
				signal_output.empty == True or
				learning_output_now.empty == True
				):

				chromosome[chrom_counter]['isborn'] = False
				chromosome[chrom_counter]['islearned'] = True
				chromosome[chrom_counter]['score'] = -1

				_, _, _, _, _ = chrom.Get(
											work = 'graveyard',
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											number_chromos = 0,
											Chromosome = chromosome,
											chrom_counter = chrom_counter
											)

				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'fucker_0',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 0,
																							Chromosome = chromosome,
																							chrom_counter = chrom_counter
																							)
				continue

			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print(learning_output_now)

			# print()

			#print(' max score ========> ', max_score_gl)
			if (
				chromosome[chrom_counter]['islearned'] == False
				):

				bad_flag = True
				bad_score_counter += 1
				learning_output_before = learning_output_now

				if (
					learning_output_now['max_tp'][0] >= 0.1 and
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['max_tp'][0] > learning_output_now['min_st'][0] * 1.2
					):
					chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp'][0]
					flag_learn_tp_percent_max = True

					#********************************************************************************************************************************
				else:
					if (
						learning_output_now['score'][0] >= score_for_reset and
						learning_output_now['min_st'][0] != 0 and
						learning_output_now['max_st'][0] >= 0.1
						):
						chromosome[chrom_counter]['tp_percent_max'] = randint(int((learning_output_now['max_st'][0]/2)*100), int(learning_output_now['max_st'][0]*100)*2)/100

						while chromosome[chrom_counter]['tp_percent_max'] <= learning_output_now['min_st'][0]:
							chromosome[chrom_counter]['tp_percent_max'] = randint(int((learning_output_now['max_st'][0]/2)*100), int(learning_output_now['max_st'][0]*100)*2)/100

						flag_learn_tp_percent_max = True
					else:
						if (
							learning_output_now['max_tp'][0] == 0 and
							learning_output_now['min_tp'][0] == 0 and
							learning_output_now['max_st'][0] == 0 and
							learning_output_now['min_st'][0] == 0
							):
							chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp_pr'][0]

							flag_learn_tp_percent_max = True

						else:

							chromosome[chrom_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

							flag_learn_tp_percent_max = False


				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['min_tp'][0] != 0
					):

					chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['min_tp'][0]

					flag_learn_tp_percent_min = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['mean_tp_pr'][0]

						flag_learn_tp_percent_min = True
					else:

						chromosome[chrom_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

						flag_learn_tp_percent_min = False

				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['max_st'][0] >= 0.1
					):

					chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st'][0]

					flag_learn_st_percent_max = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st_pr'][0]

						flag_learn_st_percent_max = True

					else:

						chromosome[chrom_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100

						flag_learn_st_percent_max = False

				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['min_st'][0] != 0
					):
					chromosome[chrom_counter]['st_percent_min'] = learning_output_now['min_st'][0]
					flag_learn_st_percent_min = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['st_percent_min'] = learning_output_now['mean_st_pr'][0]
						flag_learn_st_percent_min = True

					else:

						chromosome[chrom_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
						flag_learn_st_percent_min = False

						while chromosome[chrom_counter]['tp_percent_max'] < chromosome[chrom_counter]['st_percent_min']:
							chromosome[chrom_counter]['st_percent_min'] = randint(int((chromosome[chrom_counter]['tp_percent_max']/2)*100), 100)/100

							while chromosome[chrom_counter]['tp_percent_max'] < chromosome[chrom_counter]['st_percent_min']:
								chromosome[chrom_counter]['st_percent_min'] = randint(int((chromosome[chrom_counter]['tp_percent_max']/2)*100), 1500)/100

				if learning_output_now['diff_extereme'][0] != 0:
					diff_extereme = learning_output_now['diff_extereme'][0]
				else:
					diff_extereme = randint(1,6)

				score_for_reset = learning_output_now['score'][0]
				chromosome[chrom_counter]['islearned'] = (flag_learn_tp_percent_max & flag_learn_tp_percent_min & flag_learn_st_percent_max & flag_learn_st_percent_min)


			elif (
				learning_output_now['score'][0] >= max_score_gl * 0.99 and
				chromosome[chrom_counter]['islearned'] == True
				):

				learning_output_before['num_st_pr'] = [learning_output_now['num_st_pr'][0]]
				learning_output_before['num_tp_pr'] = [learning_output_now['num_tp_pr'][0]]
				learning_output_before['num_trade_pr'] = [learning_output_now['num_trade_pr'][0]]

				learning_output_before['score'] = [learning_output_now['score'][0]]

				learning_output_before['max_tp_pr'] = [learning_output_now['max_tp_pr'][0]]
				learning_output_before['max_st_pr'] = [learning_output_now['max_st_pr'][0]]

				learning_output_before['mean_tp_pr'] = [learning_output_now['mean_tp_pr'][0]]
				learning_output_before['mean_st_pr'] = [learning_output_now['mean_st_pr'][0]]

				learning_output_before['sum_st_pr'] = [learning_output_now['sum_st_pr'][0]]
				learning_output_before['sum_tp_pr'] = [learning_output_now['sum_tp_pr'][0]]

				learning_output_before['money'] = [learning_output_now['money'][0]]
				learning_output_before['draw_down'] = [learning_output_now['draw_down'][0]]

				learning_result = learning_result.append(learning_output_before, ignore_index=True)

				score = (learning_output_now['score'][0])
				chromosome[chrom_counter]['score'] = learning_output_now['score'][0]

				chromosome_output = chromosome_output.append(chromosome[chrom_counter], ignore_index=True)

				#Saving Elites:

				if not os.path.exists(path_elites):
					os.makedirs(path_elites)

				if os.path.exists(path_elites + symbol + '_LearningResults.csv'):
					os.remove(path_elites + symbol + '_LearningResults.csv')

				if os.path.exists(path_elites + symbol + '_ChromosomeResults.csv'):
					os.remove(path_elites + symbol + '_ChromosomeResults.csv')

				chromosome_output.to_csv(path_elites + symbol + '_ChromosomeResults.csv')
				learning_result.to_csv(path_elites + symbol + '_LearningResults.csv')

				#//////////////////////


				_, _, _, _, _ = chrom.Get(
											work = 'graveyard',
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											number_chromos = 0,
											Chromosome = chromosome,
											chrom_counter = chrom_counter
											)

				chorm_reset_counter = 0
				bad_score_counter = 0
				score_for_reset = 0


				learning_output_before = pd.DataFrame()
				learning_output_now = pd.DataFrame()

				bad_flag = False

			elif (
				learning_output_now['score'][0] < max_score_gl * 0.99 and
				chromosome[chrom_counter]['islearned'] == True
				):

				chromosome[chrom_counter]['isborn'] = False
				chromosome[chrom_counter]['islearned'] = True
				chromosome[chrom_counter]['score'] = -1

				_, _, _, _, _ = chrom.Get(
											work = 'graveyard',
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											number_chromos = 0,
											Chromosome = chromosome,
											chrom_counter = chrom_counter
											)

				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'fucker_0',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 0,
																							Chromosome = chromosome,
																							chrom_counter = chrom_counter
																							)

				score_for_reset = 0
				bad_score_counter = 0
				bad_score_counter_2 = 0
				continue

			if (
				len(chromosome_output) >= int(num_turn)
				):
				break


			if bad_flag == True:

				if bad_score_counter < 4:

					chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																									work = 'fucker_1',
																									scoresdataframe = learning_output_now,
																									signaltype = signaltype,
																									signalpriority = signalpriority,
																									symbol = symbol,
																									number_chromos = 0,
																									Chromosome = chromosome,
																									chrom_counter = chrom_counter
																									)
					

				else:
					if (
						bad_score_counter_2 >= 3
						):
						
						chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																									work = 'fucker_2',
																									signaltype = signaltype,
																									signalpriority = signalpriority,
																									symbol = symbol,
																									number_chromos = 0,
																									Chromosome = chromosome,
																									chrom_counter = chrom_counter
																									)

						score_for_reset = 0
						bad_score_counter = 0
						bad_score_counter_2 = 0

					else:
						chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																										work = 'fucker_3',
																										signaltype = signaltype,
																										signalpriority = signalpriority,
																										symbol = symbol,
																										number_chromos = 0,
																										Chromosome = chromosome,
																										chrom_counter = chrom_counter
																										)
						score_for_reset = 0
						bad_score_counter_2 += 1
						bad_score_counter = 0

				continue

			chrom_counter += 1

			if (chrom_counter >= len(chromosome)):

				chrom_counter = 0

				print('Group Sex Start')

				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																									work = 'group_sex',
																									signaltype = signaltype,
																									signalpriority = signalpriority,
																									symbol = symbol,
																									number_chromos = 0,
																									Chromosome = chromosome,
																									chrom_counter = chrom_counter
																									)

				print('Group Sex Finish')
				continue

		#**************************** Best Find *********************************************************
		#************ Finded:
		if len(chromosome_output) > 0:

			if not os.path.exists(path_elites):
				os.makedirs(path_elites)

			if os.path.exists(path_elites + symbol + '_LearningResults.csv'):
				os.remove(path_elites + symbol + '_LearningResults.csv')

			if os.path.exists(path_elites + symbol + '_ChromosomeResults.csv'):
				os.remove(path_elites + symbol + '_ChromosomeResults.csv')

			chromosome_output.to_csv(path_elites + symbol + '_ChromosomeResults.csv')
			learning_result.to_csv(path_elites + symbol + '_LearningResults.csv')

			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print('=======> Chorme ===> ')
			# 	print()
			# 	print('........................................................')
			# 	print(chromosome_output)
			# 	print('........................................................')
			# 	print()

			best_chromosome = pd.DataFrame()
			max_score_output = np.max(learning_result['score'].dropna())
			best_score_index = np.where(learning_result['score'] == max_score_output)[0]
			best_dict = dict()
			for idx in best_score_index:
				for clm in learning_result.columns:
					best_dict.update(
						{
						clm: learning_result[clm][idx]
						})
				for clm in chromosome_output.columns:
					best_dict.update(
						{
						clm: chromosome_output[clm][idx]
						})

				best_chromosome = best_chromosome.append(best_dict, ignore_index=True)

				for clm in best_chromosome.columns:
					if clm == 'Unnamed: 0':
						best_chromosome = best_chromosome.drop(columns='Unnamed: 0')

			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print(best_chromosome)

			path_superhuman = macd_config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'
			if not os.path.exists(path_superhuman):
				os.makedirs(path_superhuman)

			if os.path.exists(path_superhuman + symbol + '.csv'):
				os.remove(path_superhuman + symbol + '.csv')

			best_chromosome.to_csv(path_superhuman + symbol + '.csv')
		#//////////////////////

	def calculator_macd(self):

		symbol = self.elements['symbol']
		apply_to = self.elements[__class__.__name__ + '_apply_to']
		macd_read = ind.macd(
							self.elements['dataset_5M'][symbol][apply_to],
							fast = self.elements[__class__.__name__ + '_fast'],
							slow = self.elements[__class__.__name__ + '_slow'],
							signal = self.elements[__class__.__name__ + '_signal']
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