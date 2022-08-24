from macd_Config import Config as MACDConfig
from indicator_Parameters import Parameters as IndicatorParameters
from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from fitter import Fitter, get_common_distributions, get_distributions
from sklearn.cluster import KMeans
from pr_Parameters import Parameters as PRParameters
from pr_Config import Config as PRConfig
from macd_Parameters import Parameters as MACDParameters
from macd_ParameterLimits import ParameterLimits as Limits
from random import randint
import random
import pandas as pd
import os
import sys
import numpy as np
from timer import stTime
import warnings
warnings.filterwarnings("ignore")

limits = Limits()


apply_to_list = [
					'open',
					'close',
					'low',
					'high',
					'HL/2',
					'HLC/3',
					'HLCC/4',
					'OHLC/4'
					]

Chromosome_Accepted_List = [
							'MACD_apply_to',
							'MACD_fast',
							'MACD_slow',
							'MACD_signal',
							'MACD_column_div',
							'Divergence_num_exteremes_min',
							'Divergence_num_exteremes_max',
							'Divergence_diff_extereme',
							'BestFinder_n_clusters',
							'BestFinder_alpha',
							'Runner_methode1__lenght_data_5M',
							'Runner_methode1__lenght_data_1H',
							'ExtremePoints_num_max_5M',
							'ExtremePoints_num_min_5M',
							'ExtremePoints_weight_5M',
							'ExtremePoints_num_max_1H',
							'ExtremePoints_num_min_1H',
							'ExtremePoints_weight_1H',
							'TrendLines_num_max_5M',
							'TrendLines_num_min_5M',
							'TrendLines_weight_5M',
							'TrendLines_num_max_1H',
							'TrendLines_num_min_1H',
							'TrendLines_weight_1H',
							'TrendLines_length_long_5M',
							'TrendLines_length_mid_5M',
							'TrendLines_length_short1_5M',
							'TrendLines_length_short2_5M',
							'TrendLines_length_long_1H',
							'TrendLines_length_mid_1H',
							'TrendLines_length_short1_1H',
							'TrendLines_length_short2_1H',
							'TrendLines_power_long_5M',
							'TrendLines_power_mid_5M',
							'TrendLines_power_short1_5M',
							'TrendLines_power_short2_5M',
							'TrendLines_power_long_1H',
							'TrendLines_power_mid_1H',
							'TrendLines_power_short1_1H',
							'TrendLines_power_short2_1H',
							'IchimokouFlatLines_tenkan_5M',
							'IchimokouFlatLines_kijun_5M',
							'IchimokouFlatLines_senkou_5M',
							'IchimokouFlatLines_n_cluster_5M',
							'IchimokouFlatLines_weight_5M',
							'IchimokouFlatLines_tenkan_1H',
							'IchimokouFlatLines_kijun_1H',
							'IchimokouFlatLines_senkou_1H',
							'IchimokouFlatLines_n_cluster_1H',
							'IchimokouFlatLines_weight_1H',
							'BestFinder_n_cluster_low',
							'BestFinder_n_cluster_high',
							'BestFinder_alpha_low',
							'BestFinder_alpha_high',
							'st_percent_min',
							'st_percent_max',
							'tp_percent_min',
							'tp_percent_max',
							'ExtremePoints_status',
							'ExtremePoints_T_5M',
							'ExtremePoints_T_1H',
							'TrendLines_status',
							'TrendLines_T_5M',
							'TrendLines_long_T_5M',
							'TrendLines_mid_T_5M',
							'TrendLines_short1_T_5M',
							'TrendLines_short2_T_5M',
							'TrendLines_T_1H',
							'TrendLines_long_T_1H',
							'TrendLines_mid_T_1H',
							'TrendLines_short1_T_1H',
							'TrendLines_short2_T_1H',
							'IchimokouFlatLines_T_5M',
							'IchimokouFlatLines_T_1H',
							'IchimokouFlatLines_status',
							'score',
							'islearned',
							'isborn',
							]

#Functions:

#MACDChromosomeInitializer()
#DivergenceChromosomeInitializer()
#ProtectResistChromosomeInitializer()

#//////////////////////

class Chromosome:

	def __init__(self, parameters):

		self.elements = dict({

							#ST TP Limits:

							'st_percent_up': parameters.elements['st_percent_up'],
							'st_percent_down': parameters.elements['st_percent_down'],
							'tp_percent_up': parameters.elements['tp_percent_up'],
							'tp_percent_down': parameters.elements['tp_percent_down'],

							#////////////////////

							})


	def Get(
			self,
			work,
			signaltype,
			signalpriority,
			symbol,
			number_chromos,
			Chromosome,
			chrom_counter,
			scoresdataframe = '',
			path_elites_chromosome = '',
			alpha = 0.4
			):

		macd_parameters = MACDParameters()

		pr_parameters = PRParameters()
		pr_config = PRConfig()

		ind_parameters = IndicatorParameters()

		#Select Which Work is Be Done:

		if work == 'Optimize':
			self.ParameterOptimizer(
									path_elites_chromosome = path_elites_chromosome,
									alpha = alpha
									)

			return True

		if work == 'BigBang':

			Chromosome = self.Initializer(
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol,
										number_chromos = number_chromos
										)

		Chromosome = self.Deleter(Chromosome = Chromosome)

		if work == 'graveyard':

			Chromosome = self.GraveyardCheker(
												Chromosome = Chromosome,
												chrom_counter = chrom_counter,
												signaltype = signaltype,
												signalpriority = signalpriority,
												symbol = symbol
												)

		elif work == 'fucker_0': 

			Chromosome[chrom_counter] = self.Creator(
													chrom_counter = chrom_counter,
													signaltype = signaltype,
													signalpriority = signalpriority,
													symbol = symbol,
													)
			Chromosome = self.GraveyardCheker(
												Chromosome = Chromosome,
												chrom_counter = chrom_counter,
												signaltype = signaltype,
												signalpriority = signalpriority,
												symbol = symbol
												)

		elif work == 'fucker_1':

			Chromosome = self.fucker_1(
										scoresdataframe = scoresdataframe,
										Chromosome = Chromosome,
										chrom_counter = chrom_counter,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol
										)


		elif work == 'fucker_2':

			Chromosome = self.fucker_2(
										Chromosome = Chromosome,
										chrom_counter = chrom_counter,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol
										)

		elif work == 'fucker_3':	

			Chromosome = self.fucker_3(
									Chromosome = Chromosome,
									chrom_counter = chrom_counter,
									signaltype = signaltype,
									signalpriority = signalpriority,
									symbol = symbol
									)

		elif work == 'sttp_minmax': pass

		elif work == 'group_sex':

			Chromosome = self.GroupSex(
										Chromosome = Chromosome,
										chrom_counter = chrom_counter,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol
										)

		#/////////////////////////////////////////////////////////


		self.SocietyRefresher(
								Chromosome = Chromosome,
								signaltype = signaltype,
								signalpriority = signalpriority,
								symbol = symbol
								)

		#Chromosome And Parameters Reader:

		for elm in Chromosome[chrom_counter].keys():

			for pr_param_elm in pr_parameters.elements.keys():
				if pr_param_elm == elm:
					pr_parameters.elements[pr_param_elm] = Chromosome[chrom_counter][elm]

			for pr_conf_elm in pr_config.cfg.keys():
				if pr_conf_elm == elm:
					pr_config.cfg[pr_conf_elm] = Chromosome[chrom_counter][elm]

			for ind_elm in ind_parameters.elements.keys():
				if ind_elm == elm:
					ind_parameters.elements[ind_elm] = Chromosome[chrom_counter][elm]

			for macd_elm in macd_parameters.elements.keys():
				if macd_elm == elm:
					macd_parameters.elements[macd_elm] = Chromosome[chrom_counter][elm]
		#//////////////////////////////////////

		return Chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config


	def Initializer(
					self,
					signaltype,
					signalpriority,
					symbol,
					number_chromos = 5
					):
		#************************** initialize Values ******************************************************
		macdconfig = MACDConfig()
		path_society = macdconfig.cfg['path_society'] + signalpriority + '/' + signaltype + '/'
		path_superhuman = macdconfig.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'

		Chromosome_vares = dict()

		Chor_DataFrame = pd.DataFrame()

		if os.path.exists(path_society + symbol + '.csv'):

			Chromosome_vares = pd.read_csv(path_society + symbol + '.csv').drop(columns='Unnamed: 0').to_dict('index')

			Chromosome_vares = self.Deleter(Chromosome = Chromosome_vares)

			if os.path.exists(path_superhuman + symbol + '.csv'):

				check = 0
				for key in Chromosome_vares.keys():
					check = np.where(pd.read_csv(path_superhuman + symbol + '.csv').drop(columns=['Unnamed: 0','permit']).to_dict('index')[0] == Chromosome_vares[key])
					if len(check) > 0:
						check = 1

				if check == 0:
					Chromosome_vares.update({len(Chromosome_vares): pd.read_csv(path_superhuman + symbol + '.csv').drop(columns='Unnamed: 0').to_dict('index')[0]})

					Chromosome_vares = self.Deleter(Chromosome = Chromosome_vares)
		else:

			i = 0
			
			while i < number_chromos:

				Chromosome_vares[i] = dict({})

				macd_parameters = self.MACDChromosomeInitializer()

				Chromosome_vares[i].update(macd_parameters.elements)

				del Chromosome_vares[i]['symbol']
				del Chromosome_vares[i]['st_percent_up']
				del Chromosome_vares[i]['st_percent_down']
				del Chromosome_vares[i]['tp_percent_up']
				del Chromosome_vares[i]['tp_percent_down']


				div_parameters = self.DivergenceChromosomeInitializer()

				Chromosome_vares[i].update(div_parameters.elements)

				del Chromosome_vares[i]['symbol']

				
				pr_parameters, pr_config = self.ProtectResistChromosomeInitializer()

				Chromosome_vares[i].update(pr_parameters.elements)
				Chromosome_vares[i].update(pr_config.cfg)

				del Chromosome_vares[i]['dataset_5M']
				del Chromosome_vares[i]['dataset_1H']
				del Chromosome_vares[i]['plot']
				del Chromosome_vares[i]['Tester_plot_save']
				del Chromosome_vares[i]['Tester_flag_realtest']
				del Chromosome_vares[i]['IchimokouFlatLines_plot']
				del Chromosome_vares[i]['Tester_money']
				del Chromosome_vares[i]['Tester_coef_money']
				del Chromosome_vares[i]['Tester_spred']
				del Chromosome_vares[i]['Tester_index_tp']
				del Chromosome_vares[i]['Tester_index_st']
				del Chromosome_vares[i]['TrendLines_plot']

				Chromosome_vares[i].update(
											{
												'score': 0,
												'islearned': False,
												'isborn': True,
											}
											)

				Chor_DataFrame_While = pd.DataFrame(Chromosome_vares[i], index = [i])

				Chor_DataFrame = pd.concat([Chor_DataFrame , Chor_DataFrame_While], ignore_index = True)
				
				i += 1

			if not os.path.exists(path_society):
				os.makedirs(path_society)
			
			Chor_DataFrame.to_csv(path_society + symbol + '.csv')
		#***********************************************************************************
		return Chromosome_vares


	def Creator(
				self,
				chrom_counter,
				signaltype,
				signalpriority,
				symbol,
				):

		macdconfig = MACDConfig()
		path_society = macdconfig.cfg['path_society'] + signalpriority + '/' + signaltype + '/'

		Chromosome_vares = dict()

		Chor_DataFrame = pd.DataFrame()

		Chromosome_vares[chrom_counter] = dict({})

		macd_parameters = self.MACDChromosomeInitializer()

		Chromosome_vares[chrom_counter].update(macd_parameters.elements)

		del Chromosome_vares[chrom_counter]['symbol']
		del Chromosome_vares[chrom_counter]['st_percent_up']
		del Chromosome_vares[chrom_counter]['st_percent_down']
		del Chromosome_vares[chrom_counter]['tp_percent_up']
		del Chromosome_vares[chrom_counter]['tp_percent_down']


		div_parameters = self.DivergenceChromosomeInitializer()

		Chromosome_vares[chrom_counter].update(div_parameters.elements)

		del Chromosome_vares[chrom_counter]['symbol']

		
		pr_parameters, pr_config = self.ProtectResistChromosomeInitializer()

		Chromosome_vares[chrom_counter].update(pr_parameters.elements)
		Chromosome_vares[chrom_counter].update(pr_config.cfg)

		del Chromosome_vares[chrom_counter]['dataset_5M']
		del Chromosome_vares[chrom_counter]['dataset_1H']
		del Chromosome_vares[chrom_counter]['plot']
		del Chromosome_vares[chrom_counter]['Tester_plot_save']
		del Chromosome_vares[chrom_counter]['Tester_flag_realtest']
		del Chromosome_vares[chrom_counter]['IchimokouFlatLines_plot']
		del Chromosome_vares[chrom_counter]['Tester_money']
		del Chromosome_vares[chrom_counter]['Tester_coef_money']
		del Chromosome_vares[chrom_counter]['Tester_spred']
		del Chromosome_vares[chrom_counter]['Tester_index_tp']
		del Chromosome_vares[chrom_counter]['Tester_index_st']
		del Chromosome_vares[chrom_counter]['TrendLines_plot']

		Chromosome_vares[chrom_counter].update(
												{
													'score': 0,
													'islearned': False,
													'isborn': True,
												}
												)
		return Chromosome_vares[chrom_counter]

	#@stTime
	def GraveyardCheker(
						self,
						Chromosome,
						chrom_counter,
						signaltype,
						signalpriority,
						symbol,
						number_dead_chromos = 0
						):

		macd_config = MACDConfig()
		path_graveyard = macd_config.cfg['path_graveyard'] + signalpriority + '/' + signaltype + '/'

		if (
			Chromosome[chrom_counter]['isborn'] == False and
			Chromosome[chrom_counter]['islearned'] == True and
			Chromosome[chrom_counter]['score'] != 0
			):

			if os.path.exists(path_graveyard + symbol + '.csv'):

				GL_result = pd.read_csv(path_graveyard + symbol + '.csv').drop(columns = 'Unnamed: 0')
				GL_result_First = pd.DataFrame(Chromosome[chrom_counter], index = [len(GL_result[GL_result.columns[0]])])
				GL_result = pd.concat([GL_result , GL_result_First], ignore_index=True)

				os.remove(path_graveyard + symbol + '.csv')

			else:

				GL_result = pd.DataFrame(Chromosome[chrom_counter], index = [0])
	 
			for clm in GL_result.columns:
				if clm == 'Unnamed: 0':
					GL_result = GL_result.drop(columns = 'Unnamed: 0')

			if not os.path.exists(path_graveyard):
				os.makedirs(path_graveyard)
				
			GL_result.to_csv(path_graveyard + symbol + '.csv')

			return Chromosome

		if os.path.exists(path_graveyard + symbol + '.csv'):

			GL_result = pd.read_csv(path_graveyard + symbol + '.csv').drop(columns = 'Unnamed: 0')

			GL_result_checking = GL_result.copy(deep = True).drop(
																	columns = [
																				'isborn', 'islearned', 'score', 
																				'st_percent_min', 'st_percent_max', 
																				'tp_percent_min', 'tp_percent_max'
																				]
																	)

			dead_counter = 0

			chor = dict(Chromosome[chrom_counter])
			del chor['isborn']
			del chor['islearned']
			del chor['score']
			del chor['st_percent_min']
			del chor['st_percent_max']
			del chor['tp_percent_min']
			del chor['tp_percent_max']


			check = np.where(GL_result_checking == chor)[0]
			check_numbers = np.bincount(check)

			if len(np.where(check_numbers == len(GL_result_checking.columns))[0]) >= 1:
				in_graveyard = True
			else:
				in_graveyard = False
			
			if in_graveyard == True:

				Chromosome[chrom_counter] = self.Creator(
														chrom_counter = chrom_counter,
														signaltype = signaltype,
														signalpriority = signalpriority,
														symbol = symbol,
														)

				chor = dict(Chromosome[chrom_counter])
				del chor['isborn']
				del chor['islearned']
				del chor['score']
				del chor['st_percent_min']
				del chor['st_percent_max']
				del chor['tp_percent_min']
				del chor['tp_percent_max']

				check = np.where(GL_result_checking == chor)[0]
				check_numbers = np.bincount(check)

				if len(np.where(check_numbers == len(GL_result_checking.columns))[0]) >= 1:
					number_dead_chromos += 1

					#if number_dead_chromos >= len(GL_result[GL_result.columns[0]]): return 'End_of_Chromosomes'

					self.GraveyardCheker(
										Chromosome = Chromosome[chrom_counter],
										chrom_counter = chrom_counter,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol,
										number_dead_chromos = number_dead_chromos
										)
				else:
					self.SocietyRefresher(
										Chromosome = Chromosome,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol
										)
					return Chromosome
			else:
				return Chromosome
		elif not os.path.exists(path_graveyard + symbol + '.csv'):
			return Chromosome



	def ProtectResistChromosomeInitializer(self):

		pr_config = PRConfig()
		pr_parameters = PRParameters()


		#Parameters:
		#Elemns For Runner Module:

		pr_parameters.elements['Runner' + '_methode1_' + '_lenght_data_5M'] = randint(limits.elements['Runner_methode1__lenght_data_5M_lower'], limits.elements['Runner_methode1__lenght_data_5M_upper'])
		pr_parameters.elements['Runner' + '_methode1_' + '_lenght_data_1H'] = randint(limits.elements['Runner_methode1__lenght_data_1H_lower'], limits.elements['Runner_methode1__lenght_data_1H_upper'])

		#//////////////////////////////


		#Elemns For ExtremePoints Module:

		pr_parameters.elements['ExtremePoints_num_max_5M'] = randint(limits.elements['ExtremePoints_num_max_5M_lower'], limits.elements['ExtremePoints_num_max_5M_upper'])
		pr_parameters.elements['ExtremePoints_num_min_5M'] = randint(limits.elements['ExtremePoints_num_min_5M_lower'], limits.elements['ExtremePoints_num_min_5M_upper'])
		pr_parameters.elements['ExtremePoints_weight_5M'] = randint(limits.elements['ExtremePoints_weight_5M_lower'], limits.elements['ExtremePoints_weight_5M_upper'])

		pr_parameters.elements['ExtremePoints_num_max_1H'] = randint(limits.elements['ExtremePoints_num_max_1H_lower'], limits.elements['ExtremePoints_num_max_1H_upper'])
		pr_parameters.elements['ExtremePoints_num_min_1H'] = randint(limits.elements['ExtremePoints_num_min_1H_lower'], limits.elements['ExtremePoints_num_min_1H_upper'])
		pr_parameters.elements['ExtremePoints_weight_1H'] = randint(limits.elements['ExtremePoints_weight_1H_lower'], limits.elements['ExtremePoints_weight_1H_upper'])

		#/////////////////////////////////


		#Elemns For TrendingLines Module:

		pr_parameters.elements['TrendLines_num_max_5M'] = randint(limits.elements['TrendLines_num_max_5M_lower'], limits.elements['TrendLines_num_max_5M_upper'])
		pr_parameters.elements['TrendLines_num_min_5M'] = randint(limits.elements['TrendLines_num_min_5M_lower'], limits.elements['TrendLines_num_min_5M_upper'])
		pr_parameters.elements['TrendLines_weight_5M'] = randint(limits.elements['TrendLines_weight_5M_lower'], limits.elements['TrendLines_weight_5M_upper'])

		pr_parameters.elements['TrendLines_num_max_1H'] = randint(limits.elements['TrendLines_num_max_1H_lower'], limits.elements['TrendLines_num_max_1H_upper'])
		pr_parameters.elements['TrendLines_num_min_1H'] = randint(limits.elements['TrendLines_num_min_1H_lower'], limits.elements['TrendLines_num_min_1H_upper'])
		pr_parameters.elements['TrendLines_weight_1H'] = randint(limits.elements['TrendLines_weight_1H_lower'], limits.elements['TrendLines_weight_1H_upper'])

		pr_parameters.elements['TrendLines' + '_length_long_5M'] = randint(limits.elements['TrendLines_length_long_5M_lower'], limits.elements['TrendLines_length_long_5M_upper'])
		pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(limits.elements['TrendLines_length_mid_5M_lower'], limits.elements['TrendLines_length_mid_5M_upper'])
		pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])
		pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(limits.elements['TrendLines_length_short2_5M_lower'], limits.elements['TrendLines_length_short2_5M_upper'])

		while pr_parameters.elements['TrendLines' + '_length_mid_5M'] >= pr_parameters.elements['TrendLines' + '_length_long_5M']:
			pr_parameters.elements['TrendLines' + '_length_long_5M'] = randint(limits.elements['TrendLines_length_long_5M_lower'], limits.elements['TrendLines_length_long_5M_upper'])
			pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(limits.elements['TrendLines_length_mid_5M_lower'], limits.elements['TrendLines_length_mid_5M_upper'])

			while pr_parameters.elements['TrendLines' + '_length_short1_5M'] >= pr_parameters.elements['TrendLines' + '_length_mid_5M']:
				pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(limits.elements['TrendLines_length_mid_5M_lower'], limits.elements['TrendLines_length_mid_5M_upper'])
				pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])

				while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
					pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])
					pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(limits.elements['TrendLines_length_short2_5M_lower'], limits.elements['TrendLines_length_short2_5M_upper'])

		while pr_parameters.elements['TrendLines' + '_length_short1_5M'] >= pr_parameters.elements['TrendLines' + '_length_mid_5M']:
			pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(limits.elements['TrendLines_length_long_5M_lower'], limits.elements['TrendLines_length_long_5M_upper'])
			pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])

			while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
				pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])
				pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(limits.elements['TrendLines_length_short2_5M_lower'], limits.elements['TrendLines_length_short2_5M_upper'])

		while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
			pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(limits.elements['TrendLines_length_short1_5M_lower'], limits.elements['TrendLines_length_short1_5M_upper'])
			pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(limits.elements['TrendLines_length_short2_5M_lower'], limits.elements['TrendLines_length_short2_5M_upper'])


		pr_parameters.elements['TrendLines' + '_length_long_1H'] = randint(limits.elements['TrendLines_length_long_1H_lower'], limits.elements['TrendLines_length_long_1H_upper'])
		pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(limits.elements['TrendLines_length_mid_1H_lower'], limits.elements['TrendLines_length_mid_1H_upper'])
		pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])
		pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(limits.elements['TrendLines_length_short2_1H_lower'], limits.elements['TrendLines_length_short2_1H_upper'])

		while pr_parameters.elements['TrendLines' + '_length_mid_1H'] >= pr_parameters.elements['TrendLines' + '_length_long_1H']:
			pr_parameters.elements['TrendLines' + '_length_long_1H'] = randint(limits.elements['TrendLines_length_long_1H_lower'], limits.elements['TrendLines_length_long_1H_upper'])
			pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(limits.elements['TrendLines_length_mid_1H_lower'], limits.elements['TrendLines_length_mid_1H_upper'])

			while pr_parameters.elements['TrendLines' + '_length_short1_1H'] >= pr_parameters.elements['TrendLines' + '_length_mid_1H']:
				pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(limits.elements['TrendLines_length_mid_1H_lower'], limits.elements['TrendLines_length_mid_1H_upper'])
				pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])

				while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
					pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])
					pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(limits.elements['TrendLines_length_short2_1H_lower'], limits.elements['TrendLines_length_short2_1H_upper'])

		while pr_parameters.elements['TrendLines' + '_length_short1_1H'] >= pr_parameters.elements['TrendLines' + '_length_mid_1H']:
			pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(limits.elements['TrendLines_length_mid_1H_lower'], limits.elements['TrendLines_length_mid_1H_upper'])
			pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])

			while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
				pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])
				pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(limits.elements['TrendLines_length_short2_1H_lower'], limits.elements['TrendLines_length_short2_1H_upper'])

		while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
			pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(limits.elements['TrendLines_length_short1_1H_lower'], limits.elements['TrendLines_length_short1_1H_upper'])
			pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(limits.elements['TrendLines_length_short2_1H_lower'], limits.elements['TrendLines_length_short2_1H_upper'])

		pr_parameters.elements['TrendLines' + '_power_long_5M'] = randint(limits.elements['TrendLines_power_long_5M_lower'], limits.elements['TrendLines_power_long_5M_upper'])
		pr_parameters.elements['TrendLines' + '_power_mid_5M'] = randint(limits.elements['TrendLines_power_mid_5M_lower'], limits.elements['TrendLines_power_mid_5M_upper'])
		pr_parameters.elements['TrendLines' + '_power_short1_5M'] = randint(limits.elements['TrendLines_power_short1_5M_lower'], limits.elements['TrendLines_power_short1_5M_upper'])
		pr_parameters.elements['TrendLines' + '_power_short2_5M'] = randint(limits.elements['TrendLines_power_short2_5M_lower'], limits.elements['TrendLines_power_short2_5M_upper'])

		pr_parameters.elements['TrendLines' + '_power_long_1H'] = randint(limits.elements['TrendLines_power_long_1H_lower'], limits.elements['TrendLines_power_long_1H_upper'])
		pr_parameters.elements['TrendLines' + '_power_mid_1H'] = randint(limits.elements['TrendLines_power_mid_1H_lower'], limits.elements['TrendLines_power_mid_1H_upper'])
		pr_parameters.elements['TrendLines' + '_power_short1_1H'] = randint(limits.elements['TrendLines_power_short1_1H_lower'], limits.elements['TrendLines_power_short1_1H_upper'])
		pr_parameters.elements['TrendLines' + '_power_short2_1H'] = randint(limits.elements['TrendLines_power_short2_1H_lower'], limits.elements['TrendLines_power_short2_1H_upper'])

		#/////////////////////////////////


		#Elemns For FlatLinesIchimoku Module:

		pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] = randint(limits.elements['IchimokouFlatLines_tenkan_5M_lower'], limits.elements['IchimokouFlatLines_tenkan_5M_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M'] = randint(limits.elements['IchimokouFlatLines_kijun_5M_lower'], limits.elements['IchimokouFlatLines_kijun_5M_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_senkou_5M'] = randint(limits.elements['IchimokouFlatLines_senkou_5M_lower'], limits.elements['IchimokouFlatLines_senkou_5M_upper'])

		while pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] >= pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M']:
			pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] = randint(limits.elements['IchimokouFlatLines_tenkan_5M_lower'], limits.elements['IchimokouFlatLines_tenkan_5M_upper'])
			pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M'] = randint(limits.elements['IchimokouFlatLines_kijun_5M_lower'], limits.elements['IchimokouFlatLines_kijun_5M_upper'])

		pr_parameters.elements['IchimokouFlatLines' + '_n_cluster_5M'] = randint(limits.elements['IchimokouFlatLines' + '_n_cluster_5M_lower'], limits.elements['IchimokouFlatLines' + '_n_cluster_5M_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_weight_5M'] = randint(limits.elements['IchimokouFlatLines' + '_weight_5M_lower'], limits.elements['IchimokouFlatLines' + '_weight_5M_upper'])


		pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] = randint(limits.elements['IchimokouFlatLines_tenkan_1H_lower'], limits.elements['IchimokouFlatLines_tenkan_1H_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H'] = randint(limits.elements['IchimokouFlatLines_kijun_1H_lower'], limits.elements['IchimokouFlatLines_kijun_1H_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_senkou_1H'] = randint(limits.elements['IchimokouFlatLines_senkou_1H_lower'], limits.elements['IchimokouFlatLines_senkou_1H_upper'])

		while pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] >= pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H']:
			pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] = randint(limits.elements['IchimokouFlatLines_tenkan_1H_lower'], limits.elements['IchimokouFlatLines_tenkan_1H_upper'])
			pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H'] = randint(limits.elements['IchimokouFlatLines_kijun_1H_lower'], limits.elements['IchimokouFlatLines_kijun_1H_upper'])


		pr_parameters.elements['IchimokouFlatLines' + '_n_cluster_1H'] = randint(limits.elements['IchimokouFlatLines_n_cluster_1H_lower'], limits.elements['IchimokouFlatLines_n_cluster_1H_upper'])
		pr_parameters.elements['IchimokouFlatLines' + '_weight_1H'] = randint(limits.elements['IchimokouFlatLines_weight_1H_lower'], limits.elements['IchimokouFlatLines_weight_1H_upper'])

		#/////////////////////////////////


		#Elemns For BestFinder Module:

		pr_parameters.elements['BestFinder' + '_n_cluster_low'] = randint(limits.elements['BestFinder_n_cluster_low_lower'], limits.elements['BestFinder_n_cluster_low_upper'])
		pr_parameters.elements['BestFinder' + '_n_cluster_high'] = randint(limits.elements['BestFinder_n_cluster_high_lower'], limits.elements['BestFinder_n_cluster_high_upper'])

		pr_parameters.elements['BestFinder' + '_alpha_low'] = randint(limits.elements['BestFinder_alpha_low_lower'], limits.elements['BestFinder_alpha_low_upper'])/100
		pr_parameters.elements['BestFinder' + '_alpha_high'] = randint(limits.elements['BestFinder_alpha_high_lower'], limits.elements['BestFinder_alpha_high_upper'])/100

		#/////////////////////////////////


		#Elemns For Tester:

		pr_parameters.elements['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		pr_parameters.elements['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		pr_parameters.elements['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100
		pr_parameters.elements['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100		

		#//////////////////

		#**********************************************
		#Config For ExtremePoints:

		pr_config.cfg['ExtremePoints_status'] = random.choice([True, False])
		pr_config.cfg['ExtremePoints_T_5M'] = random.choice([True, False])
		pr_config.cfg['ExtremePoints_T_1H'] = random.choice([True, False])
		
		#///////////////////////////


		#Config For TrendLines:

		pr_config.cfg['TrendLines_status'] = random.choice([True, False])

		pr_config.cfg['TrendLines_T_5M'] = random.choice([True, False])
		pr_config.cfg['TrendLines_long_T_5M'] = random.choice([True, False])
		pr_config.cfg['TrendLines_mid_T_5M'] = random.choice([True, False])
		pr_config.cfg['TrendLines_short1_T_5M'] = random.choice([True, False])
		pr_config.cfg['TrendLines_short2_T_5M'] = random.choice([True, False])

		pr_config.cfg['TrendLines_T_1H'] = random.choice([True, False])
		pr_config.cfg['TrendLines_long_T_1H'] = random.choice([True, False])
		pr_config.cfg['TrendLines_mid_T_1H'] = random.choice([True, False])
		pr_config.cfg['TrendLines_short1_T_1H'] = random.choice([True, False])
		pr_config.cfg['TrendLines_short2_T_1H'] = random.choice([True, False])

		#///////////////////////////

		
		#Config For IchimokouFlatLines:
		pr_config.cfg['IchimokouFlatLines' + '_status'] = random.choice([True, False])
		pr_config.cfg['IchimokouFlatLines' + '_T_5M'] = random.choice([True, False])
		pr_config.cfg['IchimokouFlatLines' + '_T_1H'] = random.choice([True, False])

		#//////////////////////////

		return pr_parameters, pr_config




	def DivergenceChromosomeInitializer(self):

		ind_parameters = IndicatorParameters()

		#*********** Divergence:

		ind_parameters.elements['Divergence' + '_num_exteremes_min'] = randint(limits.elements['Divergence_num_exteremes_min_lower'], limits.elements['Divergence_num_exteremes_min_upper'])
		ind_parameters.elements['Divergence' + '_num_exteremes_max'] = randint(limits.elements['Divergence_num_exteremes_max_lower'], limits.elements['Divergence_num_exteremes_max_upper'])

		ind_parameters.elements['Divergence' + '_diff_extereme'] = 6

		#///////////////////////

		#BestFinder:

		ind_parameters.elements['BestFinder' + '_n_clusters'] = randint(limits.elements['BestFinder_n_clusters_lower'], limits.elements['BestFinder_n_clusters_upper'])
		ind_parameters.elements['BestFinder' + '_alpha'] = randint(limits.elements['BestFinder_alpha_lower'], limits.elements['BestFinder_alpha_upper'])/100

		#//////////////////////

		return ind_parameters


	def MACDChromosomeInitializer(self):
		
		macd_parameters = MACDParameters()

		macd_parameters.elements['MACD' + '_apply_to'] = random.choice(apply_to_list)

		macd_parameters.elements['MACD' + '_fast'] = randint(limits.elements['MACD' + '_fast_lower'], limits.elements['MACD' + '_fast_upper'])
		macd_parameters.elements['MACD' + '_slow'] = randint(limits.elements['MACD' + '_slow_lower'], limits.elements['MACD' + '_slow_upper'])

		while macd_parameters.elements['MACD' + '_fast'] >= macd_parameters.elements['MACD' + '_slow']:
			macd_parameters.elements['MACD' + '_fast'] = randint(limits.elements['MACD' + '_fast_lower'], limits.elements['MACD' + '_fast_upper'])
			macd_parameters.elements['MACD' + '_slow'] = randint(limits.elements['MACD' + '_slow_lower'], limits.elements['MACD' + '_slow_upper'])


		macd_parameters.elements['MACD' + '_signal'] = randint(limits.elements['MACD' + '_signal_lower'], limits.elements['MACD' + '_signal_upper'])

		macd_parameters.elements['MACD' + '_column_div'] = random.choice(['macd', 'macds', 'macdh'])

		return macd_parameters


	#@stTime
	def SocietyRefresher(
						self,
						Chromosome,
						signaltype,
						signalpriority,
						symbol
						):
		
		macdconfig = MACDConfig()
		path_society = macdconfig.cfg['path_society'] + signalpriority + '/' + signaltype + '/'

		if os.path.exists(path_society + symbol + '.csv'):
			os.remove(path_society + symbol + '.csv')

			Chor_DataFrame = pd.DataFrame()

			for key in Chromosome.keys():

				Chor_DataFrame_While = pd.DataFrame(Chromosome[key], index = [key])

				Chor_DataFrame = pd.concat([Chor_DataFrame , Chor_DataFrame_While], ignore_index = True)

			Chor_DataFrame.to_csv(path_society + symbol + '.csv')

	#@stTime
	def fucker_1(
				self,
				scoresdataframe,
				Chromosome,
				chrom_counter,
				signaltype,
				signalpriority,
				symbol
				):

		Chromosome[chrom_counter]['MACD_apply_to'] = random.choice(apply_to_list)
		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(limits.elements['BestFinder_alpha_lower'], limits.elements['BestFinder_alpha_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(limits.elements['BestFinder_alpha_low_lower'], limits.elements['BestFinder_alpha_low_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(limits.elements['BestFinder_alpha_high_lower'], limits.elements['BestFinder_alpha_high_upper'])/100

		if scoresdataframe['diff_extereme'][0] != 0:
			Chromosome[chrom_counter]['Divergence_diff_extereme'] = scoresdataframe['diff_extereme'][0]
		else:
			Chromosome[chrom_counter]['Divergence_diff_extereme'] = randint(1,6)


		Chromosome[chrom_counter]['score'] = 0
		Chromosome[chrom_counter]['islearned'] = True
		Chromosome[chrom_counter]['isborn'] = True

		Chromosome = self.GraveyardCheker(
											Chromosome = Chromosome,
											chrom_counter = chrom_counter,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol
											)

		return Chromosome

	def fucker_2(
				self,
				Chromosome,
				chrom_counter,
				signaltype,
				signalpriority,
				symbol
				):

		Chromosome[chrom_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		Chromosome[chrom_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		Chromosome[chrom_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100
		Chromosome[chrom_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

		fast_period = randint(limits.elements['MACD_fast_lower'], limits.elements['MACD_fast_upper'])
		while Chromosome[chrom_counter]['MACD_slow'] < fast_period:
			fast_period = randint(limits.elements['MACD_fast_lower'], limits.elements['MACD_fast_upper'])
			
		
		Chromosome[chrom_counter]['MACD_apply_to'] = random.choice(apply_to_list)
		Chromosome[chrom_counter]['MACD_fast'] = fast_period
		Chromosome[chrom_counter]['MACD_signal'] = randint(limits.elements['MACD_signal_lower'], limits.elements['MACD_signal_upper'])
		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(limits.elements['BestFinder_alpha_lower'], limits.elements['BestFinder_alpha_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(limits.elements['BestFinder_alpha_low_lower'], limits.elements['BestFinder_alpha_low_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(limits.elements['BestFinder_alpha_high_lower'], limits.elements['BestFinder_alpha_high_upper'])/100
		Chromosome[chrom_counter]['Divergence_diff_extereme'] = 6
		Chromosome[chrom_counter]['Divergence_num_exteremes_max'] = randint(limits.elements['Divergence_num_exteremes_max_lower'], limits.elements['Divergence_num_exteremes_max_upper'])
		Chromosome[chrom_counter]['Divergence_num_exteremes_min'] = randint(limits.elements['Divergence_num_exteremes_min_lower'], limits.elements['Divergence_num_exteremes_min_upper'])

		Chromosome[chrom_counter]['score'] = 0
		Chromosome[chrom_counter]['islearned'] = False
		Chromosome[chrom_counter]['isborn'] = True

		Chromosome = self.GraveyardCheker(
											Chromosome = Chromosome,
											chrom_counter = chrom_counter,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol
											)

		return Chromosome

	def fucker_3(
				self,
				Chromosome,
				chrom_counter,
				signaltype,
				signalpriority,
				symbol
				):


		Chromosome[chrom_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		Chromosome[chrom_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
		Chromosome[chrom_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100
		Chromosome[chrom_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

		Chromosome[chrom_counter]['MACD_signal'] = randint(limits.elements['MACD_signal_lower'], limits.elements['MACD_signal_upper'])
		Chromosome[chrom_counter]['MACD_apply_to'] = random.choice(apply_to_list)

		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(limits.elements['BestFinder_alpha_lower'], limits.elements['BestFinder_alpha_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(limits.elements['BestFinder_alpha_low_lower'], limits.elements['BestFinder_alpha_low_upper'])/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(limits.elements['BestFinder_alpha_high_lower'], limits.elements['BestFinder_alpha_high_upper'])/100

		Chromosome[chrom_counter]['Divergence_num_exteremes_max'] = randint(limits.elements['Divergence_num_exteremes_max_lower'], limits.elements['Divergence_num_exteremes_max_upper'])
		Chromosome[chrom_counter]['Divergence_num_exteremes_min'] = randint(limits.elements['Divergence_num_exteremes_min_lower'], limits.elements['Divergence_num_exteremes_min_upper'])

		Chromosome[chrom_counter]['Divergence_diff_extereme'] = 6

		Chromosome[chrom_counter]['score'] = 0
		Chromosome[chrom_counter]['islearned'] = False
		Chromosome[chrom_counter]['isborn'] = True

		Chromosome = self.GraveyardCheker(
											Chromosome = Chromosome,
											chrom_counter = chrom_counter,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol
											)

		return Chromosome

	def takeSecond(self, elem):
		return elem[1]

	@stTime
	def GroupSex(
				self,
				Chromosome,
				chrom_counter,
				signaltype,
				signalpriority,
				symbol
				):
		
		scr = []
		for k,v in zip(Chromosome.keys(), Chromosome.values()):
			scr.append([k, v.get('score')])

		scr_idx = sorted(scr, key = self.takeSecond, reverse=True)[:int(len(Chromosome)/2)]

		chor = dict()
		for key in Chromosome.keys():

			chor[key] = dict(Chromosome[key])
			del chor[key]['isborn']
			del chor[key]['islearned']
			del chor[key]['score']
			del chor[key]['st_percent_min']
			del chor[key]['st_percent_max']
			del chor[key]['tp_percent_min']
			del chor[key]['tp_percent_max']

		baby = {}

		chrom_creator_counter = 0
		baby_counter = 0

		baby_counter_create = 0

		while (baby_counter_create < (len(chor) * 2)):

			baby[baby_counter_create] = dict({})

			baby_counter_create += 1


		while chrom_creator_counter < len(chor):

			#********************************************* Baby ***********************************************************
			
			Chromosome_selector_1 = np.random.choice(len(scr_idx), size=1)[0]
			Chromosome_selector_2 = np.random.choice(len(scr_idx), size=1)[0]

			res_1 = list(chor[Chromosome_selector_1].keys())
			res_2 = list(chor[Chromosome_selector_2].keys())

			Chromosome_Cutter = randint(0, len(chor[0].keys()))#****************************** -1

			change_chrom_counter = 0

			while change_chrom_counter < Chromosome_Cutter:

				baby[baby_counter].update({res_1[change_chrom_counter]: chor[Chromosome_selector_1][res_1[change_chrom_counter]]})
				baby[baby_counter + 1].update({res_2[change_chrom_counter]: chor[Chromosome_selector_2][res_2[change_chrom_counter]]})

				change_chrom_counter += 1

			change_chrom_counter = Chromosome_Cutter

			while change_chrom_counter < len(chor[0].keys()) - 1:

				baby[baby_counter].update({res_2[change_chrom_counter]: chor[Chromosome_selector_2][res_2[change_chrom_counter]]})
				baby[baby_counter + 1].update({res_1[change_chrom_counter]: chor[Chromosome_selector_1][res_1[change_chrom_counter]]})
				change_chrom_counter += 1

			baby_counter = baby_counter + 2

						#********************************************///////***************************************************************************
			chrom_creator_counter += 1

		i = 0
		limit_counter = len(chor) * 2 
		while i < (limit_counter):
			chor[i] = dict({})
			i += 1

		re_counter = 0
		while (re_counter < limit_counter):

			for key in baby[re_counter].keys():
				chor[re_counter][key] = baby[re_counter][key]

			chor[re_counter] = self.LimitChecker(Chromosome = chor[re_counter])

			chor[re_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
			chor[re_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
			chor[re_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100
			chor[re_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

			chor[re_counter]['score'] = 0
			chor[re_counter]['isborn'] = True
			chor[re_counter]['islearned'] = False
			
			re_counter += 1

		for key in chor.keys():
			i = 0
			while i < len(Chromosome):
				if key == i:
					i += 1
					continue

				check = np.where(chor[key] == chor[i])

				if len(check) > 0:
					chor[key] = self.Creator(
											chrom_counter = key,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											)

				i += 1
			chor = self.GraveyardCheker(	
										Chromosome = chor,
										chrom_counter = key,
										signaltype = signaltype,
										signalpriority = signalpriority,
										symbol = symbol
										)

		return chor

	def LimitChecker(self, Chromosome):

		while Chromosome['MACD' + '_fast'] >= Chromosome['MACD' + '_slow']:
			Chromosome['MACD' + '_fast'] = randint(4, 800)
			Chromosome['MACD' + '_slow'] = randint(4, 1500)

		while Chromosome['TrendLines' + '_length_mid_5M'] >= Chromosome['TrendLines' + '_length_long_5M']:
			Chromosome['TrendLines' + '_length_long_5M'] = randint(10, 1000)
			Chromosome['TrendLines' + '_length_mid_5M'] = randint(10, 1000)

			while Chromosome['TrendLines' + '_length_short1_5M'] >= Chromosome['TrendLines' + '_length_mid_5M']:
				Chromosome['TrendLines' + '_length_mid_5M'] = randint(10, 1000)
				Chromosome['TrendLines' + '_length_short1_5M'] = randint(5, 500)

				while Chromosome['TrendLines' + '_length_short2_5M'] >= Chromosome['TrendLines' + '_length_short1_5M']:
					Chromosome['TrendLines' + '_length_short1_5M'] = randint(5, 500)
					Chromosome['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while Chromosome['TrendLines' + '_length_short1_5M'] >= Chromosome['TrendLines' + '_length_mid_5M']:
			Chromosome['TrendLines' + '_length_mid_5M'] = randint(10, 1000)
			Chromosome['TrendLines' + '_length_short1_5M'] = randint(5, 500)

			while Chromosome['TrendLines' + '_length_short2_5M'] >= Chromosome['TrendLines' + '_length_short1_5M']:
				Chromosome['TrendLines' + '_length_short1_5M'] = randint(5, 500)
				Chromosome['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while Chromosome['TrendLines' + '_length_short2_5M'] >= Chromosome['TrendLines' + '_length_short1_5M']:
			Chromosome['TrendLines' + '_length_short1_5M'] = randint(5, 500)
			Chromosome['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while Chromosome['TrendLines' + '_length_mid_1H'] >= Chromosome['TrendLines' + '_length_long_1H']:
			Chromosome['TrendLines' + '_length_long_1H'] = randint(10, 1000)
			Chromosome['TrendLines' + '_length_mid_1H'] = randint(10, 1000)

			while Chromosome['TrendLines' + '_length_short1_1H'] >= Chromosome['TrendLines' + '_length_mid_1H']:
				Chromosome['TrendLines' + '_length_mid_1H'] = randint(10, 1000)
				Chromosome['TrendLines' + '_length_short1_1H'] = randint(5, 500)

				while Chromosome['TrendLines' + '_length_short2_1H'] >= Chromosome['TrendLines' + '_length_short1_1H']:
					Chromosome['TrendLines' + '_length_short1_1H'] = randint(5, 500)
					Chromosome['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		while Chromosome['TrendLines' + '_length_short1_1H'] >= Chromosome['TrendLines' + '_length_mid_1H']:
			Chromosome['TrendLines' + '_length_mid_1H'] = randint(10, 1000)
			Chromosome['TrendLines' + '_length_short1_1H'] = randint(5, 500)

			while Chromosome['TrendLines' + '_length_short2_1H'] >= Chromosome['TrendLines' + '_length_short1_1H']:
				Chromosome['TrendLines' + '_length_short1_1H'] = randint(5, 500)
				Chromosome['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		while Chromosome['TrendLines' + '_length_short2_1H'] >= Chromosome['TrendLines' + '_length_short1_1H']:
			Chromosome['TrendLines' + '_length_short1_1H'] = randint(5, 500)
			Chromosome['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		#/////////////////////////////////


		#Elemns For FlatLinesIchimoku Module:

		while Chromosome['IchimokouFlatLines' + '_tenkan_5M'] >= Chromosome['IchimokouFlatLines' + '_kijun_5M']:
			Chromosome['IchimokouFlatLines' + '_tenkan_5M'] = randint(2, 500)
			Chromosome['IchimokouFlatLines' + '_kijun_5M'] = randint(2, 1400)


		while Chromosome['IchimokouFlatLines' + '_tenkan_1H'] >= Chromosome['IchimokouFlatLines' + '_kijun_1H']:
			Chromosome['IchimokouFlatLines' + '_tenkan_1H'] = randint(2, 500)
			Chromosome['IchimokouFlatLines' + '_kijun_1H'] = randint(2, 1400)

		return Chromosome

	def Deleter(self, Chromosome):

		chor = dict()
		for key in Chromosome.keys():
			chor[key] = dict(Chromosome[key])

		for key in Chromosome.keys():
			for elm in Chromosome[key].keys():

				if not elm in Chromosome_Accepted_List:

					del chor[key][elm]

		return chor


	def ParameterOptimizer(self, path_elites_chromosome, alpha):

		macd_config = MACDConfig()

		if os.path.exists(path_elites_chromosome):

			chromosome = pd.read_csv(path_elites_chromosome).drop(columns='Unnamed: 0')

		upper = 0
		lower = 2

		MACD_fast = self.Finder(chromosome = chromosome, apply_to = 'MACD_fast', alpha = alpha)
		limits.elements['MACD_fast_upper'] = round(MACD_fast['interval'][upper])
		limits.elements['MACD_fast_lower'] = int(MACD_fast['interval'][lower])

		MACD_slow = self.Finder(chromosome = chromosome, apply_to = 'MACD_slow', alpha = alpha)
		limits.elements['MACD_slow_upper'] = round(MACD_slow['interval'][upper])
		limits.elements['MACD_slow_lower'] = int(MACD_slow['interval'][lower])

		MACD_signal = self.Finder(chromosome = chromosome, apply_to = 'MACD_signal', alpha = alpha)
		limits.elements['MACD_signal_upper'] = round(MACD_signal['interval'][upper])
		limits.elements['MACD_signal_lower'] = int(MACD_signal['interval'][lower])

		Divergence_num_exteremes_min = self.Finder(chromosome = chromosome, apply_to = 'Divergence_num_exteremes_min', alpha = alpha)
		limits.elements['Divergence_num_exteremes_min_upper'] = round(Divergence_num_exteremes_min['interval'][upper])
		limits.elements['Divergence_num_exteremes_min_lower'] = int(Divergence_num_exteremes_min['interval'][lower])

		Divergence_num_exteremes_max = self.Finder(chromosome = chromosome, apply_to = 'Divergence_num_exteremes_max', alpha = alpha)
		limits.elements['Divergence_num_exteremes_max_upper'] = round(Divergence_num_exteremes_max['interval'][upper])
		limits.elements['Divergence_num_exteremes_max_lower'] = int(Divergence_num_exteremes_max['interval'][lower])

		BestFinder_n_clusters = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_n_clusters', alpha = alpha)
		limits.elements['BestFinder_n_clusters_upper'] = round(BestFinder_n_clusters['interval'][upper])
		limits.elements['BestFinder_n_clusters_lower'] = int(BestFinder_n_clusters['interval'][lower])

		BestFinder_alpha = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_alpha', alpha = 0.9)
		limits.elements['BestFinder_alpha_upper'] = int(round(BestFinder_alpha['interval'][upper], 3) * 100)
		limits.elements['BestFinder_alpha_lower'] = int(round(BestFinder_alpha['interval'][lower], 3) * 100)

		Runner_methode1__lenght_data_5M = self.Finder(chromosome = chromosome, apply_to = 'Runner_methode1__lenght_data_5M', alpha = alpha)
		limits.elements['Runner_methode1__lenght_data_5M_upper'] = round(Runner_methode1__lenght_data_5M['interval'][upper])
		limits.elements['Runner_methode1__lenght_data_5M_lower'] = int(Runner_methode1__lenght_data_5M['interval'][lower])

		Runner_methode1__lenght_data_1H = self.Finder(chromosome = chromosome, apply_to = 'Runner_methode1__lenght_data_1H', alpha = alpha)
		limits.elements['Runner_methode1__lenght_data_1H_upper'] = round(Runner_methode1__lenght_data_1H['interval'][upper])
		limits.elements['Runner_methode1__lenght_data_1H_lower'] = int(Runner_methode1__lenght_data_1H['interval'][lower])

		ExtremePoints_num_max_5M = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_num_max_5M', alpha = alpha)
		limits.elements['ExtremePoints_num_max_5M_upper'] = round(ExtremePoints_num_max_5M['interval'][upper])
		limits.elements['ExtremePoints_num_max_5M_lower'] = int(ExtremePoints_num_max_5M['interval'][lower])

		ExtremePoints_num_min_5M = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_num_min_5M', alpha = alpha)
		limits.elements['ExtremePoints_num_min_5M_upper'] = round(ExtremePoints_num_min_5M['interval'][upper])
		limits.elements['ExtremePoints_num_min_5M_lower'] = int(ExtremePoints_num_min_5M['interval'][lower])

		ExtremePoints_weight_5M = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_weight_5M', alpha = alpha)
		limits.elements['ExtremePoints_weight_5M_upper'] = round(ExtremePoints_weight_5M['interval'][upper])
		limits.elements['ExtremePoints_weight_5M_lower'] = int(ExtremePoints_weight_5M['interval'][lower])

		ExtremePoints_num_max_1H = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_num_max_1H', alpha = alpha)
		limits.elements['ExtremePoints_num_max_1H_upper'] = round(ExtremePoints_num_max_1H['interval'][upper])
		limits.elements['ExtremePoints_num_max_1H_lower'] = int(ExtremePoints_num_max_1H['interval'][lower])

		ExtremePoints_num_min_1H = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_num_min_1H', alpha = alpha)
		limits.elements['ExtremePoints_num_min_1H_upper'] = round(ExtremePoints_num_min_1H['interval'][upper])
		limits.elements['ExtremePoints_num_min_1H_lower'] = int(ExtremePoints_num_min_1H['interval'][lower])

		ExtremePoints_weight_1H = self.Finder(chromosome = chromosome, apply_to = 'ExtremePoints_weight_1H', alpha = alpha)
		limits.elements['ExtremePoints_weight_1H_upper'] = round(ExtremePoints_weight_1H['interval'][upper])
		limits.elements['ExtremePoints_weight_1H_lower'] = int(ExtremePoints_weight_1H['interval'][lower])

		TrendLines_num_max_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_num_max_5M', alpha = alpha)
		limits.elements['TrendLines_num_max_5M_upper'] = round(TrendLines_num_max_5M['interval'][upper])
		limits.elements['TrendLines_num_max_5M_lower'] = int(TrendLines_num_max_5M['interval'][lower])

		TrendLines_num_max_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_num_max_5M', alpha = alpha)
		limits.elements['TrendLines_num_max_5M_upper'] = round(TrendLines_num_max_5M['interval'][upper])
		limits.elements['TrendLines_num_max_5M_lower'] = int(TrendLines_num_max_5M['interval'][lower])

		TrendLines_num_min_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_num_min_5M', alpha = alpha)
		limits.elements['TrendLines_num_min_5M_upper'] = round(TrendLines_num_min_5M['interval'][upper])
		limits.elements['TrendLines_num_min_5M_lower'] = int(TrendLines_num_min_5M['interval'][lower])

		TrendLines_weight_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_weight_5M', alpha = alpha)
		limits.elements['TrendLines_weight_5M_upper'] = round(TrendLines_weight_5M['interval'][upper])
		limits.elements['TrendLines_weight_5M_lower'] = int(TrendLines_weight_5M['interval'][lower])

		TrendLines_num_max_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_num_max_1H', alpha = alpha)
		limits.elements['TrendLines_num_max_1H_upper'] = round(TrendLines_num_max_1H['interval'][upper])
		limits.elements['TrendLines_num_max_1H_lower'] = int(TrendLines_num_max_1H['interval'][lower])

		TrendLines_num_min_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_num_min_1H', alpha = alpha)
		limits.elements['TrendLines_num_min_1H_upper'] = round(TrendLines_num_min_1H['interval'][upper])
		limits.elements['TrendLines_num_min_1H_lower'] = int(TrendLines_num_min_1H['interval'][lower])

		TrendLines_weight_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_weight_1H', alpha = alpha)
		limits.elements['TrendLines_weight_1H_upper'] = round(TrendLines_weight_1H['interval'][upper])
		limits.elements['TrendLines_weight_1H_lower'] = int(TrendLines_weight_1H['interval'][lower])

		TrendLines_length_long_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_long_5M', alpha = alpha)
		limits.elements['TrendLines_length_long_5M_upper'] = round(TrendLines_length_long_5M['interval'][upper])
		limits.elements['TrendLines_length_long_5M_lower'] = int(TrendLines_length_long_5M['interval'][lower])

		TrendLines_length_mid_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_mid_5M', alpha = alpha)
		limits.elements['TrendLines_length_mid_5M_upper'] = round(TrendLines_length_mid_5M['interval'][upper])
		limits.elements['TrendLines_length_mid_5M_lower'] = int(TrendLines_length_mid_5M['interval'][lower])

		TrendLines_length_short1_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_short1_5M', alpha = alpha)
		limits.elements['TrendLines_length_short1_5M_upper'] = round(TrendLines_length_short1_5M['interval'][upper])
		limits.elements['TrendLines_length_short1_5M_lower'] = int(TrendLines_length_short1_5M['interval'][lower])

		TrendLines_length_short2_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_short2_5M', alpha = alpha)
		limits.elements['TrendLines_length_short2_5M_upper'] = round(TrendLines_length_short2_5M['interval'][upper])
		limits.elements['TrendLines_length_short2_5M_lower'] = int(TrendLines_length_short2_5M['interval'][lower])

		TrendLines_length_long_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_long_1H', alpha = alpha)
		limits.elements['TrendLines_length_long_1H_upper'] = round(TrendLines_length_long_1H['interval'][upper])
		limits.elements['TrendLines_length_long_1H_lower'] = int(TrendLines_length_long_1H['interval'][lower])

		TrendLines_length_mid_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_mid_1H', alpha = alpha)
		limits.elements['TrendLines_length_mid_1H_upper'] = round(TrendLines_length_mid_1H['interval'][upper])
		limits.elements['TrendLines_length_mid_1H_lower'] = int(TrendLines_length_mid_1H['interval'][lower])

		TrendLines_length_short1_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_short1_1H', alpha = alpha)
		limits.elements['TrendLines_length_short1_1H_upper'] = round(TrendLines_length_short1_1H['interval'][upper])
		limits.elements['TrendLines_length_short1_1H_lower'] = int(TrendLines_length_short1_1H['interval'][lower])

		TrendLines_length_short2_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_length_short2_1H', alpha = alpha)
		limits.elements['TrendLines_length_short2_1H_upper'] = round(TrendLines_length_short2_1H['interval'][upper])
		limits.elements['TrendLines_length_short2_1H_lower'] = int(TrendLines_length_short2_1H['interval'][lower])

		TrendLines_power_long_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_long_5M', alpha = alpha)
		limits.elements['TrendLines_power_long_5M_upper'] = round(TrendLines_power_long_5M['interval'][upper])
		limits.elements['TrendLines_power_long_5M_lower'] = int(TrendLines_power_long_5M['interval'][lower])

		TrendLines_power_mid_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_mid_5M', alpha = alpha)
		limits.elements['TrendLines_power_mid_5M_upper'] = round(TrendLines_power_mid_5M['interval'][upper])
		limits.elements['TrendLines_power_mid_5M_lower'] = int(TrendLines_power_mid_5M['interval'][lower])

		TrendLines_power_short1 = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_short1_5M', alpha = alpha)
		limits.elements['TrendLines_power_short1_5M_upper'] = round(TrendLines_power_short1['interval'][upper])
		limits.elements['TrendLines_power_short1_5M_lower'] = int(TrendLines_power_short1['interval'][lower])

		TrendLines_power_short2_5M = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_short2_5M', alpha = alpha)
		limits.elements['TrendLines_power_short2_5M_upper'] = round(TrendLines_power_short2_5M['interval'][upper])
		limits.elements['TrendLines_power_short2_5M_lower'] = int(TrendLines_power_short2_5M['interval'][lower])

		TrendLines_power_long_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_long_1H', alpha = alpha)
		limits.elements['TrendLines_power_long_1H_upper'] = round(TrendLines_power_long_1H['interval'][upper])
		limits.elements['TrendLines_power_long_1H_lower'] = int(TrendLines_power_long_1H['interval'][lower])

		TrendLines_power_mid_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_mid_1H', alpha = alpha)
		limits.elements['TrendLines_power_mid_1H_upper'] = round(TrendLines_power_mid_1H['interval'][upper])
		limits.elements['TrendLines_power_mid_1H_lower'] = int(TrendLines_power_mid_1H['interval'][lower])

		TrendLines_power_short1_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_short1_1H', alpha = alpha)
		limits.elements['TrendLines_power_short1_1H_upper'] = round(TrendLines_power_short1_1H['interval'][upper])
		limits.elements['TrendLines_power_short1_1H_lower'] = int(TrendLines_power_short1_1H['interval'][lower])

		TrendLines_power_short2_1H = self.Finder(chromosome = chromosome, apply_to = 'TrendLines_power_short2_1H', alpha = alpha)
		limits.elements['TrendLines_power_short2_1H_upper'] = round(TrendLines_power_short2_1H['interval'][upper])
		limits.elements['TrendLines_power_short2_1H_lower'] = int(TrendLines_power_short2_1H['interval'][lower])

		IchimokouFlatLines_tenkan_5M = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_tenkan_5M', alpha = alpha)
		limits.elements['IchimokouFlatLines_tenkan_5M_upper'] = round(IchimokouFlatLines_tenkan_5M['interval'][upper])
		limits.elements['IchimokouFlatLines_tenkan_5M_lower'] = int(IchimokouFlatLines_tenkan_5M['interval'][lower])

		IchimokouFlatLines_kijun_5M = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_kijun_5M', alpha = alpha)
		limits.elements['IchimokouFlatLines_kijun_5M_upper'] = round(IchimokouFlatLines_kijun_5M['interval'][upper])
		limits.elements['IchimokouFlatLines_kijun_5M_lower'] = int(IchimokouFlatLines_kijun_5M['interval'][lower])

		IchimokouFlatLines_senkou_5M = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_senkou_5M', alpha = alpha)
		limits.elements['IchimokouFlatLines_senkou_5M_upper'] = round(IchimokouFlatLines_senkou_5M['interval'][upper])
		limits.elements['IchimokouFlatLines_senkou_5M_lower'] = int(IchimokouFlatLines_senkou_5M['interval'][lower])

		IchimokouFlatLines_n_cluster_5M = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_n_cluster_5M', alpha = alpha)
		limits.elements['IchimokouFlatLines_n_cluster_5M_upper'] = round(IchimokouFlatLines_n_cluster_5M['interval'][upper])
		limits.elements['IchimokouFlatLines_n_cluster_5M_lower'] = int(IchimokouFlatLines_n_cluster_5M['interval'][lower])

		IchimokouFlatLines_weight_5M = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_weight_5M', alpha = alpha)
		limits.elements['IchimokouFlatLines_weight_5M_upper'] = round(IchimokouFlatLines_weight_5M['interval'][upper])
		limits.elements['IchimokouFlatLines_weight_5M_lower'] = int(IchimokouFlatLines_weight_5M['interval'][lower])

		IchimokouFlatLines_tenkan_1H = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_tenkan_1H', alpha = alpha)
		limits.elements['IchimokouFlatLines_tenkan_1H_upper'] = round(IchimokouFlatLines_tenkan_1H['interval'][upper])
		limits.elements['IchimokouFlatLines_tenkan_1H_lower'] = int(IchimokouFlatLines_tenkan_1H['interval'][lower])

		IchimokouFlatLines_kijun_1H = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_kijun_1H', alpha = alpha)
		limits.elements['IchimokouFlatLines_kijun_1H_upper'] = round(IchimokouFlatLines_kijun_1H['interval'][upper])
		limits.elements['IchimokouFlatLines_kijun_1H_lower'] = int(IchimokouFlatLines_kijun_1H['interval'][lower])

		IchimokouFlatLines_senkou_1H = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_senkou_1H', alpha = alpha)
		limits.elements['IchimokouFlatLines_senkou_1H_upper'] = round(IchimokouFlatLines_senkou_1H['interval'][upper])
		limits.elements['IchimokouFlatLines_senkou_1H_lower'] = int(IchimokouFlatLines_senkou_1H['interval'][lower])

		IchimokouFlatLines_n_cluster_1H = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_n_cluster_1H', alpha = alpha)
		limits.elements['IchimokouFlatLines_n_cluster_1H_upper'] = round(IchimokouFlatLines_n_cluster_1H['interval'][upper])
		limits.elements['IchimokouFlatLines_n_cluster_1H_lower'] = int(IchimokouFlatLines_n_cluster_1H['interval'][lower])

		IchimokouFlatLines_weight_1H = self.Finder(chromosome = chromosome, apply_to = 'IchimokouFlatLines_weight_1H', alpha = alpha)
		limits.elements['IchimokouFlatLines_weight_1H_upper'] = round(IchimokouFlatLines_weight_1H['interval'][upper])
		limits.elements['IchimokouFlatLines_weight_1H_lower'] = int(IchimokouFlatLines_weight_1H['interval'][lower])

		BestFinder_n_cluster_low = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_n_cluster_low', alpha = alpha)
		limits.elements['BestFinder_n_cluster_low_upper'] = round(BestFinder_n_cluster_low['interval'][upper])
		limits.elements['BestFinder_n_cluster_low_lower'] = int(BestFinder_n_cluster_low['interval'][lower])

		BestFinder_n_cluster_high = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_n_cluster_high', alpha = alpha)
		limits.elements['BestFinder_n_cluster_high_upper'] = round(BestFinder_n_cluster_high['interval'][upper])
		limits.elements['BestFinder_n_cluster_high_lower'] = int(BestFinder_n_cluster_high['interval'][lower])

		BestFinder_alpha_low = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_alpha_low', alpha = alpha)
		limits.elements['BestFinder_alpha_low_upper'] = int(round(BestFinder_alpha_low['interval'][upper], 3) * 100)
		limits.elements['BestFinder_alpha_low_lower'] = int(round(BestFinder_alpha_low['interval'][lower], 3) * 100)

		BestFinder_alpha_high = self.Finder(chromosome = chromosome, apply_to = 'BestFinder_alpha_high', alpha = alpha)
		limits.elements['BestFinder_alpha_high_upper'] = int(round(BestFinder_alpha_high['interval'][upper], 3) * 100)
		limits.elements['BestFinder_alpha_high_lower'] = int(round(BestFinder_alpha_high['interval'][lower], 3) * 100)


	def Finder(self, chromosome, apply_to, alpha):

		signal_good = chromosome.copy(deep = True)

		if (signal_good.empty == True): 
			best_signals_interval = pd.DataFrame(
											{
											'interval': [0,0,0],
											'power': [0,0,0],
											'alpha': [alpha,alpha,alpha],
											}
											)
			return best_signals_interval

		#signal_good = signal_good.replace([np.inf, -np.inf], np.nan, inplace=False)
		#signal_good = signal_good.drop(columns = ['index'])
		#signal_good = signal_good.sort_values()
		signal_good = signal_good.reset_index(drop = True)

		try:

			signal_final, kmeans = self.Clustere(signal_good = signal_good, apply_to = apply_to)

		except Exception as ex:
			#print('Kmeans Error  = ',ex)
			best_signals_interval = pd.DataFrame(
											{
											'interval': [0,0,0],
											'power': [0,0,0],
											'alpha': [alpha,alpha,alpha],
											}
											)
			return best_signals_interval





		#Fitting Model Finding ****************************
		data_X = self.DataPreparer(signal_pred_final = signal_final)

		#************************************ Finding Sell's ****************************

		dist_item, f = self.DistributePreparer(
												data = data_X,
												signal_pred_final = signal_final,
												distributions = ['expon', 'norm']
												)

		if dist_item != '':
			Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line = self.ValuesPreparer(
																														dist_items = dist_item,
																														f = f,
																														data = data_X,
																														signal_pred_final = signal_final,
																														alpha = alpha,
																														kmeans_f = kmeans,
																														distributions = ['expon', 'norm']
																														)
		best_signals_interval = pd.DataFrame(
										{
										'interval': [Upper_Line,Mid_Line,Lower_Line],
										'power': [Power_Upper_Line,Power_Mid_Line,Power_Lower_Line],
										'alpha': [alpha,alpha,alpha],
										}
										)

		return best_signals_interval

		#//////////////////////////////////////////////////////////////////////////////////////

	def Clustere(self, signal_good, apply_to):

		kmeans = KMeans(
						#n_clusters = 5, 
						random_state=0,
						init='k-means++',
						n_init=5,
						max_iter=5,

						)
		signal_good_kmeans = signal_good[apply_to]
		signal_good_kmeans = signal_good_kmeans.dropna()
		#Model Fitting
		kmeans = kmeans.fit(signal_good_kmeans.to_numpy().reshape(-1,1), sample_weight = signal_good['score'].dropna().to_numpy())

		Y = kmeans.cluster_centers_
		Power = kmeans.labels_
		Power = np.bincount(Power)

		signal_final = pd.DataFrame(Y, columns=['Y'])
		signal_final['power'] = Power
		signal_final = signal_final.sort_values(by = ['Y'])

		return signal_final, kmeans

	def DataPreparer(
					self,
					signal_pred_final
					):

		#Fitting Model Finding ****************************
		#Make To DataFrame With Extreme Points And Num Of Itteration For Distribution Functions:
		data_X = np.zeros(np.sum(signal_pred_final['power']))

		j = 0
		z = 0
		for elm in signal_pred_final['Y']:
			k = 0
			while k < signal_pred_final['power'].to_numpy()[j]:
				data_X[z] = elm
				k += 1
				z += 1
			j += 1

		data_X = np.sort(data_X)

		return data_X

	def DistributePreparer(
							self,
							data,
							signal_pred_final,
							distributions
							):
		#'rayleigh','nakagami','expon','foldnorm','dweibull',

		#Define Name Of Distributions that We Want To Use:
		#distributions = 

		#************************************ Finding Low Distribution Functions ****************************

		try:
			#Fitter Finding Best Function That Can Distribute Or Low Extremes:
			f = Fitter(
						data = data,
						xmin = np.min(data),
						xmax = np.max(data),
						bins = len(signal_pred_final['Y'])-1,
						distributions = distributions,
						timeout = 1,
						density = True
						)

			f.fit(
				amp = 1, 
				progress = False, 
				n_jobs = -1
				)

			#Getting the Name of Best Destributer Functions and that Parameters:
			dist_items = list(f.get_best(method = 'sumsquare_error').items())

		except Exception as ex:
			print('DistP Error = ',ex)
			dist_items = ''

		return dist_items, f


	def ValuesPreparer(
						self,
						dist_items,
						f,
						data,
						signal_pred_final,
						alpha,
						kmeans_f,
						distributions
						):


		#************************************ Finding Low Distribution Functions ****************************

		try:
			#Getting the Name of Best Destributer Functions and that Parameters:
			dist_name = dist_items[0][0]
			dist_parameters = dist_items[0][1]
			#Finding Best Points Of Low Extremes With Best Distributed Function and That Parameters:
			if dist_name == 'expon':


				Y = f.fitted_pdf['expon']
				#Using Probability Distribution Function From Scipy Library:
				Y = expon.pdf(
								x=data, 
								loc=dist_parameters['loc'], 
								scale=dist_parameters['scale']
								)
				#Finding Best Interval Low Points:
				Extereme = expon.interval(
										alpha=alpha, 
										loc=dist_parameters['loc'], 
										scale=dist_parameters['scale']
										)

				Upper_Line = Extereme[1]
				Lower_Line = Extereme[0]
				Mid_Line = np.array(dist_parameters['loc'])

				Power_Upper_Line = signal_pred_final['power'][
																		kmeans_f.predict(Upper_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])

				Power_Lower_Line = signal_pred_final['power'][
																		kmeans_f.predict(Lower_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])
				Power_Mid_Line = signal_pred_final['power'][
																		kmeans_f.predict(Mid_Line.reshape(1,-1))
																		].to_numpy()/np.max(signal_pred_final['power'])
			
			elif dist_name == 'norm':

				Y = f.fitted_pdf['norm']

				Y = norm.pdf(
							x=data, 
							loc=dist_parameters['loc'], 
							scale=dist_parameters['scale']
							)

				Extereme = norm.interval(
										alpha=alpha, 
										loc=dist_parameters['loc'], 
										scale=dist_parameters['scale']
										)

				Upper_Line = Extereme[1]
				Lower_Line = Extereme[0]
				Mid_Line = np.array(dist_parameters['loc'])
				Power_Upper_Line = signal_pred_final['power'][
																	kmeans_f.predict(Upper_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
				Power_Lower_Line = signal_pred_final['power'][
																	kmeans_f.predict(Lower_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
				Power_Mid_Line = signal_pred_final['power'][
																	kmeans_f.predict(Mid_Line.reshape(1,-1))
																	].to_numpy()/np.max(signal_pred_final['power'])
			if (
				Mid_Line >= Upper_Line or
				Mid_Line <= Lower_Line
				):
				if len(distributions) > 0:

					distributions.remove(dist_name)

					dist_item, f = self.DistributePreparer(
																data = data,
																signal_pred_final = signal_pred_final,
																distributions = distributions
																)
					Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line = self.ValuesPreparer(
																																dist_items = dist_item,
																																f = f,
																																data = data,
																																signal_pred_final = signal_pred_final,
																																alpha = alpha,
																																kmeans_f = kmeans_f,
																																distributions = distributions
																																)
				else:
					Upper_Line = 0
					Lower_Line = 0
					Mid_Line = 0
					Power_Upper_Line = 0
					Power_Lower_Line = 0
					Power_Mid_Line = 0
			
		except Exception as ex:
			print(ex)
			Upper_Line = 0
			Lower_Line = 0
			Mid_Line = 0
			Power_Upper_Line = 0
			Power_Lower_Line = 0
			Power_Mid_Line = 0

		return Upper_Line, Mid_Line, Lower_Line, Power_Upper_Line, Power_Mid_Line, Power_Lower_Line



# parameters = MACDParameters()
# chorom = Chromosome(parameters)


# chorom.ParameterOptimizer(
# 						path_elites_chromosome = 'GeneticLearning_DB/elites/' + 'primary' + '/' + 'buy' + '/' + 'ETHUSD_i' + '_ChromosomeResults.csv',
# 						alpha = 0.4
# 						)

# chromosomes = chorom.Initializer(
# 								signaltype = 'buy',
# 								signalpriority = 'primary',
# 								symbol = 'XAUUSD_i',
# 								number_chromos = 5
# 								)



# chorom.SocietyRefresher(
# 						Chromosome = chromosomes,
# 						signaltype = 'buy',
# 						signalpriority = 'primary',
# 						symbol = 'XAUUSD_i'
# 						)
# # print(chromosomes[1])
# # print()

# chromosomes = chorom.GraveyardCheker(
# 									Chromosome = chromosomes,
# 									chrom_counter = 3,
# 									signaltype = 'buy',
# 									signalpriority = 'primary',
# 									symbol = 'XAUUSD_i'
# 									)

# chromosomes, macd_parameters, ind_parameters, pr_parameters, pr_config = chorom.Get(
# 																					work = 'BigBang',
# 																					signaltype = 'buy',
# 																					signalpriority = 'primary',
# 																					symbol = 'XAUUSD_i',
# 																					number_chromos = 10,
# 																					Chromosome = chromosomes,
# 																					chrom_counter = 0
# 																					)

