from macd_Config import Config as MACDConfig
from indicator_Parameters import Parameters as IndicatorParameters
from pr_Parameters import Parameters as PRParameters
from pr_Config import Config as PRConfig
from macd_Parameters import Parameters as MACDParameters
from random import randint
import random
import pandas as pd
import os
import sys
import numpy as np


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
							'n_clusters_best_low',
							'n_clusters_best_high',
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

	def Get(
			self,
			work,
			signaltype,
			signalpriority,
			symbol,
			number_chromos,
			Chromosome,
			chrom_counter,
			scoresdataframe = ''
			):

		macd_parameters = MACDParameters()

		pr_parameters = PRParameters()
		pr_config = PRConfig()

		ind_parameters = IndicatorParameters()

		#Select Which Work is Be Done:

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
					check = np.where(pd.read_csv(path_superhuman + symbol + '.csv').drop(columns='Unnamed: 0').to_dict('index')[0] == Chromosome_vares[key])
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

		pr_parameters.elements['Runner' + '_methode1_' + '_lenght_data_5M'] = randint(20, 3000)
		pr_parameters.elements['Runner' + '_methode1_' + '_lenght_data_1H'] = randint(20, 1000)

		#//////////////////////////////


		#Elemns For ExtremePoints Module:

		pr_parameters.elements['ExtremePoints_num_max_5M'] = randint(2, 250)
		pr_parameters.elements['ExtremePoints_num_min_5M'] = randint(2, 250)
		pr_parameters.elements['ExtremePoints_weight_5M'] = randint(2, 1000)

		pr_parameters.elements['ExtremePoints_num_max_1H'] = randint(2, 250)
		pr_parameters.elements['ExtremePoints_num_min_1H'] = randint(2, 250)
		pr_parameters.elements['ExtremePoints_weight_1H'] = randint(2, 1000)

		#/////////////////////////////////


		#Elemns For TrendingLines Module:

		pr_parameters.elements['TrendLines_num_max_5M'] = randint(2, 250)
		pr_parameters.elements['TrendLines_num_min_5M'] = randint(2, 250)
		pr_parameters.elements['TrendLines_weight_5M'] = randint(2, 1000)

		pr_parameters.elements['TrendLines_num_max_1H'] = randint(2, 250)
		pr_parameters.elements['TrendLines_num_min_1H'] = randint(2, 250)
		pr_parameters.elements['TrendLines_weight_1H'] = randint(2, 1000)

		pr_parameters.elements['TrendLines' + '_length_long_5M'] = randint(10, 1000)
		pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(10, 1000)
		pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)
		pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while pr_parameters.elements['TrendLines' + '_length_mid_5M'] >= pr_parameters.elements['TrendLines' + '_length_long_5M']:
			pr_parameters.elements['TrendLines' + '_length_long_5M'] = randint(10, 1000)
			pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(10, 1000)

			while pr_parameters.elements['TrendLines' + '_length_short1_5M'] >= pr_parameters.elements['TrendLines' + '_length_mid_5M']:
				pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(10, 1000)
				pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)

				while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
					pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)
					pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while pr_parameters.elements['TrendLines' + '_length_short1_5M'] >= pr_parameters.elements['TrendLines' + '_length_mid_5M']:
			pr_parameters.elements['TrendLines' + '_length_mid_5M'] = randint(10, 1000)
			pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)

			while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
				pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)
				pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(5, 500)

		while pr_parameters.elements['TrendLines' + '_length_short2_5M'] >= pr_parameters.elements['TrendLines' + '_length_short1_5M']:
			pr_parameters.elements['TrendLines' + '_length_short1_5M'] = randint(5, 500)
			pr_parameters.elements['TrendLines' + '_length_short2_5M'] = randint(5, 500)


		pr_parameters.elements['TrendLines' + '_length_long_1H'] = randint(2, 250)
		pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(2, 250)
		pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(2, 250)
		pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(2, 250)

		while pr_parameters.elements['TrendLines' + '_length_mid_1H'] >= pr_parameters.elements['TrendLines' + '_length_long_1H']:
			pr_parameters.elements['TrendLines' + '_length_long_1H'] = randint(10, 1000)
			pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(10, 1000)

			while pr_parameters.elements['TrendLines' + '_length_short1_1H'] >= pr_parameters.elements['TrendLines' + '_length_mid_1H']:
				pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(10, 1000)
				pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(5, 500)

				while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
					pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(5, 500)
					pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		while pr_parameters.elements['TrendLines' + '_length_short1_1H'] >= pr_parameters.elements['TrendLines' + '_length_mid_1H']:
			pr_parameters.elements['TrendLines' + '_length_mid_1H'] = randint(10, 1000)
			pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(5, 500)

			while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
				pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(5, 500)
				pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		while pr_parameters.elements['TrendLines' + '_length_short2_1H'] >= pr_parameters.elements['TrendLines' + '_length_short1_1H']:
			pr_parameters.elements['TrendLines' + '_length_short1_1H'] = randint(5, 500)
			pr_parameters.elements['TrendLines' + '_length_short2_1H'] = randint(5, 500)

		pr_parameters.elements['TrendLines' + '_power_long_5M'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_mid_5M'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_short1_5M'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_short2_5M'] = randint(2, 1000)

		pr_parameters.elements['TrendLines' + '_power_long_1H'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_mid_1H'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_short1_1H'] = randint(2, 1000)
		pr_parameters.elements['TrendLines' + '_power_short2_1H'] = randint(2, 1000)

		#/////////////////////////////////


		#Elemns For FlatLinesIchimoku Module:

		pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] = randint(2, 500)
		pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M'] = randint(2, 1400)
		pr_parameters.elements['IchimokouFlatLines' + '_senkou_5M'] = randint(2, 2500)

		while pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] >= pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M']:
			pr_parameters.elements['IchimokouFlatLines' + '_tenkan_5M'] = randint(2, 500)
			pr_parameters.elements['IchimokouFlatLines' + '_kijun_5M'] = randint(2, 1400)

		pr_parameters.elements['IchimokouFlatLines' + '_n_cluster_5M'] = randint(1, 50)
		pr_parameters.elements['IchimokouFlatLines' + '_weight_5M'] = randint(2, 1000)


		pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] = randint(2, 50)
		pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H'] = randint(2, 110)
		pr_parameters.elements['IchimokouFlatLines' + '_senkou_1H'] = randint(2, 210)

		while pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] >= pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H']:
			pr_parameters.elements['IchimokouFlatLines' + '_tenkan_1H'] = randint(2, 500)
			pr_parameters.elements['IchimokouFlatLines' + '_kijun_1H'] = randint(2, 1400)


		pr_parameters.elements['IchimokouFlatLines' + '_n_cluster_1H'] = randint(1, 50)
		pr_parameters.elements['IchimokouFlatLines' + '_weight_1H'] = randint(2, 1000)

		#/////////////////////////////////


		#Elemns For BestFinder Module:

		pr_parameters.elements['BestFinder' + '_n_cluster_low'] = randint(1, 50)
		pr_parameters.elements['BestFinder' + '_n_cluster_high'] = randint(1, 50)

		pr_parameters.elements['BestFinder' + '_alpha_low'] = randint(1, 99)/100
		pr_parameters.elements['BestFinder' + '_alpha_high'] = randint(1, 99)/100

		pr_parameters.elements['n_clusters_best_low'] = randint(1, 50)
		pr_parameters.elements['n_clusters_best_high'] = randint(1, 50)

		#/////////////////////////////////


		#Elemns For Tester:

		pr_parameters.elements['st_percent_min'] = randint(80, 99)/100
		pr_parameters.elements['st_percent_max'] = randint(80, 99)/100
		pr_parameters.elements['tp_percent_min'] = randint(80, 99)/100
		pr_parameters.elements['tp_percent_max'] = randint(80, 99)/100			

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

		ind_parameters.elements['Divergence' + '_num_exteremes_min'] = randint(2, 250)
		ind_parameters.elements['Divergence' + '_num_exteremes_max'] = randint(2, 250)

		ind_parameters.elements['Divergence' + '_diff_extereme'] = 6

		#///////////////////////

		#BestFinder:

		ind_parameters.elements['BestFinder' + '_n_clusters'] = randint(1, 50)
		ind_parameters.elements['BestFinder' + '_alpha'] = randint(1, 99)/100

		#//////////////////////

		return ind_parameters


	def MACDChromosomeInitializer(self):
		
		macd_parameters = MACDParameters()

		macd_parameters.elements['MACD' + '_apply_to'] = random.choice(apply_to_list)

		macd_parameters.elements['MACD' + '_fast'] = randint(4, 800)
		macd_parameters.elements['MACD' + '_slow'] = randint(4, 1500)

		while macd_parameters.elements['MACD' + '_fast'] >= macd_parameters.elements['MACD' + '_slow']:
			macd_parameters.elements['MACD' + '_fast'] = randint(4, 800)
			macd_parameters.elements['MACD' + '_slow'] = randint(4, 1500)


		macd_parameters.elements['MACD' + '_signal'] = randint(4, 50)

		macd_parameters.elements['MACD' + '_column_div'] = random.choice(['macd', 'macds', 'macdh'])

		return macd_parameters

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
		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(1, 99)/100

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

		Chromosome[chrom_counter]['st_percent_min'] = randint(80, 100)/100
		Chromosome[chrom_counter]['st_percent_max'] = randint(80, 100)/100
		Chromosome[chrom_counter]['tp_percent_min'] = randint(80, 100)/100
		Chromosome[chrom_counter]['tp_percent_max'] = randint(80, 100)/100

		fast_period = randint(int(12/4), 800)
		while Chromosome[chrom_counter]['MACD_slow'] < fast_period:
			fast_period = randint(4, 800)
			
		
		Chromosome[chrom_counter]['MACD_apply_to'] = random.choice(apply_to_list)
		Chromosome[chrom_counter]['MACD_fast'] = fast_period
		Chromosome[chrom_counter]['MACD_signal'] = randint(4, 50)
		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(1, 99)/100
		Chromosome[chrom_counter]['Divergence_diff_extereme'] = 6
		Chromosome[chrom_counter]['Divergence_num_exteremes_max'] = randint(2, 250)
		Chromosome[chrom_counter]['Divergence_num_exteremes_min'] = randint(2, 250)

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


		Chromosome[chrom_counter]['st_percent_min'] = randint(80, 100)/100
		Chromosome[chrom_counter]['st_percent_max'] = randint(80, 100)/100
		Chromosome[chrom_counter]['tp_percent_min'] = randint(80, 100)/100
		Chromosome[chrom_counter]['tp_percent_max'] = randint(80, 100)/100

		Chromosome[chrom_counter]['MACD_signal'] = randint(4, 50)
		Chromosome[chrom_counter]['MACD_apply_to'] = random.choice(apply_to_list)

		Chromosome[chrom_counter]['BestFinder_alpha'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_low'] = randint(1, 99)/100
		Chromosome[chrom_counter]['BestFinder_alpha_high'] = randint(1, 99)/100

		Chromosome[chrom_counter]['Divergence_num_exteremes_max'] = randint(2, 250)
		Chromosome[chrom_counter]['Divergence_num_exteremes_min'] = randint(2, 250)

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

			Chromosome_Cutter = randint(0, len(chor[0].keys()) - 1)

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

			
			chor[re_counter]['st_percent_min'] = randint(80, 100)/100
			chor[re_counter]['st_percent_max'] = randint(80, 100)/100
			chor[re_counter]['tp_percent_min'] = randint(80, 100)/100
			chor[re_counter]['tp_percent_max'] = randint(80, 100)/100

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
					chor[i] = self.Creator(
											chrom_counter = i,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol,
											)

				chor = self.GraveyardCheker(	
											Chromosome = chor,
											chrom_counter = i,
											signaltype = signaltype,
											signalpriority = signalpriority,
											symbol = symbol
											)

				i += 1

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


chorom = Chromosome()

chromosomes = chorom.Initializer(
								signaltype = 'buy',
								signalpriority = 'primary',
								symbol = 'XAUUSD_i',
								number_chromos = 5
								)



chorom.SocietyRefresher(
						Chromosome = chromosomes,
						signaltype = 'buy',
						signalpriority = 'primary',
						symbol = 'XAUUSD_i'
						)
# print(chromosomes[1])
# print()

chromosomes = chorom.GraveyardCheker(
									Chromosome = chromosomes,
									chrom_counter = 3,
									signaltype = 'buy',
									signalpriority = 'primary',
									symbol = 'XAUUSD_i'
									)

chromosomes, macd_parameters, ind_parameters, pr_parameters, pr_config = chorom.Get(
																					work = 'BigBang',
																					signaltype = 'buy',
																					signalpriority = 'primary',
																					symbol = 'XAUUSD_i',
																					number_chromos = 10,
																					Chromosome = chromosomes,
																					chrom_counter = 0
																					)

