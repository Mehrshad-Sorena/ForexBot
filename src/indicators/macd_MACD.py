import pandas_ta as ind
import pandas as pd
import numpy as np
from macd_Chromosome import Chromosome
import os
from macd_Config import Config as MACDConfig
from progress.bar import Bar
from random import randint
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config

from pr_Parameters import Parameters as pr_Parameters
from pr_Config import Config as pr_Config

from indicator_Divergence import Divergence
from indicator_Tester import Tester

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


	def Genetic(self, dataset_5M, dataset_1H, symbol, signaltype, signalpriority, num_turn):

		if symbol == 'ETHUSD_i':
			self.elements['st_percent_up'] = 1500
			self.elements['st_percent_down'] = 100
			self.elements['tp_percent_up'] = 1500
			self.elements['tp_percent_down'] = 100

		chrom = Chromosome(parameters = self)
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
			max_score_gl = 0

		max_score_gl = 0


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
				num_turn = num_turn * (len(learning_result['score']))

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

		bar = Bar(signaltype + signalpriority, max = int(num_turn))

		while chrom_counter < len(chromosome):

			chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																							work = 'graveyard',
																							signaltype = signaltype,
																							signalpriority = signalpriority,
																							symbol = symbol,
																							number_chromos = 0,
																							Chromosome = chromosome,
																							chrom_counter = chrom_counter
																							)

			if chromosome[chrom_counter]['score'] != 0:
				chrom_counter += 1
				continue

			if chromosome == 'End_of_Chromosomes':
				# print(chromosome)
				break

			# print()
			# print('================== Num Symbol ==>',symbol, ' ' , signaltype, ' ',signalpriority)
			# print()
			# print('================== Num =========> ',len(chromosome_output))
			# print('================== Num Chroms ======> ',chrom_counter)
			# print('================== All Chorms ======> ',all_chorms)
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

			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print(signal)

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

			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			# 	print(learning_output_now)

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

			#print(' max score ========> ', max_score_gl)
			if ( learning_output_now['score'][0] >= max_score_gl * 0.99 ):

				max_st_last_buy = chromosome[chrom_counter]['st_percent_max']
				min_st_last_buy = chromosome[chrom_counter]['st_percent_min']
				max_tp_last_buy = chromosome[chrom_counter]['tp_percent_max']
				min_tp_last_buy = chromosome[chrom_counter]['tp_percent_min']

				if learning_output_now['max_tp'][0] >= 0.1:
					chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp'][0]
				else:
					chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp_pr'][0]

				if learning_output_now['min_tp'][0] != 0:
					chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['min_tp'][0]
				else:
					chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['mean_tp_pr'][0]


				if learning_output_now['max_st'][0] >= 0.1:
					chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st'][0]

				else:
					chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st_pr'][0]

				if learning_output_now['min_st'][0] != 0:
					chromosome[chrom_counter]['st_percent_min'] = learning_output_now['min_st'][0]

				else:
					chromosome[chrom_counter]['st_percent_min'] = learning_output_now['mean_st_pr'][0]

				if chromosome[chrom_counter]['islearned'] == True:

					# print(chromosome)

					# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
					# 	print(learning_output_now)

					learning_output_now['max_tp'][0] = max_tp_last_buy
					learning_output_now['max_st'][0] = max_st_last_buy
					learning_output_now['min_st'][0] = min_st_last_buy
					learning_output_now['min_tp'][0] = min_tp_last_buy

					learning_output_before['num_st_pr'] = [learning_output_now['num_st_pr'][0]]
					learning_output_before['num_tp_pr'] = [learning_output_now['num_tp_pr'][0]]
					learning_output_before['score'] = [learning_output_now['score'][0]]
					learning_output_before['max_tp_pr'] = [learning_output_now['max_tp_pr'][0]]
					learning_output_before['mean_tp_pr'] = [learning_output_now['mean_tp_pr'][0]]
					learning_output_before['mean_st_pr'] = [learning_output_now['mean_st_pr'][0]]
					learning_output_before['sum_st_pr'] = [learning_output_now['sum_st_pr'][0]]
					learning_output_before['sum_tp_pr'] = [learning_output_now['sum_tp_pr'][0]]
					learning_output_before['money'] = [learning_output_now['money'][0]]

					learning_result = learning_result.append(learning_output_before, ignore_index=True)

					score = (learning_output_now['score'][0])
					chromosome[chrom_counter]['score'] = learning_output_now['score'][0]

					learning_output_before = learning_output_now

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


					chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																									work = 'graveyard',
																									signaltype = signaltype,
																									signalpriority = signalpriority,
																									symbol = symbol,
																									number_chromos = 0,
																									Chromosome = chromosome,
																									chrom_counter = chrom_counter
																									)
					chorm_reset_counter = 0

					bad_score_counter_buy = 0

					score_for_reset = 0


					if learning_output_now['diff_extereme'][0] != 0:
						diff_extereme = learning_output_now['diff_extereme'][0]
					else:
						diff_extereme = randint(1,6)

					chromosome[chrom_counter]['islearned'] = False

					chromosome[chrom_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
					chromosome[chrom_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
					chromosome[chrom_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100
					chromosome[chrom_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

					bad_flag = False
				else:
					bad_score_counter += 1
					bad_flag = True
					chromosome[chrom_counter]['islearned'] = True
					score_for_reset = learning_output_now['score'][0]

					chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st'][0]
					chromosome[chrom_counter]['st_percent_min'] = learning_output_now['min_st'][0]
					chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp'][0]
					chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['min_tp'][0]

					learning_output_before = learning_output_now

					if learning_output_now['diff_extereme'][0] != 0:
						diff_extereme = learning_output_now['diff_extereme'][0]
					else:
						diff_extereme = randint(1,6)

			else:
				bad_flag = True

				bad_score_counter += 1

				learning_output_before = learning_output_now

				if (
					learning_output_now['max_tp'][0] >= 0.1 and
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['max_tp'][0] > learning_output_now['min_st'][0] * 1.2
					):
					chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp'][0]
					chromosome[chrom_counter]['islearned'] = True

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

						chromosome[chrom_counter]['islearned'] = True
					else:
						if (
							learning_output_now['max_tp'][0] == 0 and
							learning_output_now['min_tp'][0] == 0 and
							learning_output_now['max_st'][0] == 0 and
							learning_output_now['min_st'][0] == 0
							):
							chromosome[chrom_counter]['tp_percent_max'] = learning_output_now['max_tp_pr'][0]

							chromosome[chrom_counter]['islearned'] = True

						else:

							chromosome[chrom_counter]['tp_percent_max'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

							chromosome[chrom_counter]['islearned'] = False


				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['min_tp'][0] != 0
					):

					chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['min_tp'][0]

					chromosome[chrom_counter]['islearned'] = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['tp_percent_min'] = learning_output_now['mean_tp_pr'][0]

						chromosome[chrom_counter]['islearned'] = True
					else:

						chromosome[chrom_counter]['tp_percent_min'] = randint(self.elements['tp_percent_down'], self.elements['tp_percent_up'])/100

						chromosome[chrom_counter]['islearned'] = False

				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['max_st'][0] >= 0.1
					):

					chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st'][0]

					chromosome[chrom_counter]['islearned'] = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['st_percent_max'] = learning_output_now['max_st_pr'][0]

						chromosome[chrom_counter]['islearned'] = True

					else:

						chromosome[chrom_counter]['st_percent_max'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100

						chromosome[chrom_counter]['islearned'] = False

				if (
					learning_output_now['score'][0] >= score_for_reset and
					learning_output_now['min_st'][0] != 0
					):
					chromosome[chrom_counter]['st_percent_min'] = learning_output_now['min_st'][0]
					chromosome[chrom_counter]['islearned'] = True

				else:
					if (
						learning_output_now['max_tp'][0] == 0 and
						learning_output_now['min_tp'][0] == 0 and
						learning_output_now['max_st'][0] == 0 and
						learning_output_now['min_st'][0] == 0
						):

						chromosome[chrom_counter]['st_percent_min'] = learning_output_now['mean_st_pr'][0]
						chromosome[chrom_counter]['islearned'] = True

					else:

						chromosome[chrom_counter]['st_percent_min'] = randint(self.elements['st_percent_down'], self.elements['st_percent_up'])/100
						chromosome[chrom_counter]['islearned'] = False

						while chromosome[chrom_counter]['tp_percent_max'] < chromosome[chrom_counter]['st_percent_min']:
							chromosome[chrom_counter]['st_percent_min'] = randint(int((chromosome[chrom_counter]['tp_percent_max']/2)*100), 100)/100

							while chromosome[chrom_counter]['tp_percent_max'] < chromosome[chrom_counter]['st_percent_min']:
								chromosome[chrom_counter]['st_percent_min'] = randint(int((chromosome[chrom_counter]['tp_percent_max']/2)*100), 1500)/100

				if learning_output_now['diff_extereme'][0] != 0:
					diff_extereme = learning_output_now['diff_extereme'][0]
				else:
					diff_extereme = randint(1,6)

				score_for_reset = learning_output_now['score'][0]

			if (
				len(chromosome_output) >= int(num_turn/20)
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

				chromosome, macd_parameters, ind_parameters, pr_parameters, pr_config = chrom.Get(
																									work = 'group_sex',
																									signaltype = signaltype,
																									signalpriority = signalpriority,
																									symbol = symbol,
																									number_chromos = 0,
																									Chromosome = chromosome,
																									chrom_counter = chrom_counter
																									)
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

			with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				print('=======> Chorme ===> ')
				print()
				print('........................................................')
				print(chromosome_output)
				print('........................................................')
				print()

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

			with pd.option_context('display.max_rows', None, 'display.max_columns', None):
				print(best_chromosome)

			path_superhuman = macd_config.cfg['path_superhuman'] + signalpriority + '/' + signaltype + '/'
			if not os.path.exists(path_superhuman):
				os.makedirs(path_superhuman)

			if os.path.exists(path_superhuman + symbol + '.csv'):
				os.remove(path_superhuman + symbol + '.csv')

			best_chromosome.to_csv(path_superhuman + symbol + '.csv')
		#//////////////////////

		# 	#*************************** Save to TXT File ***************************************************************
			
			# try:
				

			# 	with open(path_superhuman + symbol + '.csv', 'w', newline='') as myfile:
			# 		fields = best_chromosome.columns.to_list()
			# 		writer = csv.DictWriter(myfile, fieldnames=fields)
			# 		writer.writeheader()
		
			# 		for idx in range(len(best_chromosome)):
			# 			rows = dict()
			# 			for clm in best_chromosome.columns:
			# 				rows.update({clm: best_chromosome[clm][idx]})
			# 			writer.writerow(rows)
						
			# except Exception as ex:
			# 	print('Saving CSV Error: ', ex)

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