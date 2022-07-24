from macd_Parameters import Parameters
from macd_Config import Config
from pr_Runner import Runner
from pr_Parameters import Parameters as pr_parameters
from pr_Config import Config as pr_config
import pandas as pd
import numpy as np
from timer import stTime
import time

class Tester:

	parameters = Parameters()
	config = Config()
	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({

							#************* Global:

							'dataset_5M': parameters.elements['dataset_5M'],
							'dataset_1H': parameters.elements['dataset_1H'],
							'symbol': parameters.elements['symbol'],

							#/////////////////////
							})

	@stTime
	def ProfitFlagFinder(self, signal, sigtype, flaglearn, flagtest):

		pr_parameters_ = pr_parameters()
		pr_config_ = pr_config()

		#*************************************************************
		# Bayad Maghadir Baraye Params Va Config As func baraye PR dar GA , Learner daryaft beshan

		#/////////////////////////////////////////////////////////////

		pr_Runner = Runner(parameters = pr_parameters_, config = pr_config_)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig1 = ',signal)

		signals = pd.DataFrame(
								{
									'index': signal['index'].values, 
								},
								index = signal['index'].values
								)

		signals = pr_Runner.run(
								dataset_5M = self.elements['dataset_5M'][self.elements['symbol']], 
								dataset_1H = self.elements['dataset_1H'][self.elements['symbol']],
								signals = signals,
								sigtype = sigtype,
								flaglearn = flaglearn,
								flagtest = flagtest
								)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig2 = ',signal)

		signal = signal.drop(columns = ['index'], inplace = False)

		signal = signal.join(signals).dropna(inplace = False)

		return signal

	
	def Scoring(self, signal):
		
		scores_out = pd.DataFrame()

		scores_out['mean_tp_pr'] = [np.mean(signal['tp_pr'][signal['index'][signal['flag'] != 'no_flag']])]
		print(scores_out)
		scores_out['mean_st_pr'] = [np.mean(signal['st_pr'][signal['index'][signal['flag'] != 'no_flag']])]
		scores_out['max_tp_pr'] = [np.max(signal['tp_pr'])]
		scores_out['max_st_pr'] = [np.max(signal['st_pr'])]

		try:
			scores_out['sum_st_pr'] = [np.sum(signal['st_pr'][signal['index'][signal['flag'] == 'st']].to_numpy())]
			scores_out['sum_tp_pr'] = [np.sum(signal['tp_pr'][signal['index'][signal['flag'] == 'tp']].to_numpy())]
		except Exception as ex:
			#print('error tester pr: ',ex)
			scores_out['sum_st_pr'] = 0
			scores_out['sum_tp_pr'] = 0

		tp_counter = 0
		st_counter = 0
		for elm in signal['flag']:
			if (elm == 'tp'):
				tp_counter += 1
			if (elm == 'st'):
				st_counter += 1

		scores_out['num_tp_pr'] = [tp_counter]
		scores_out['num_st_pr'] = [st_counter]
		scores_out['num_trade_pr'] = [st_counter + tp_counter]

		#******************** Tabe best Finder Bayad Seda Beshe Va Parametr hash ham az Func GA , Learn Gerefte Beshan

		# scores_out['max_st'] = [round(diff_down_pr['interval'][upper],2)]
		# scores_out['max_st_power'] = diff_down_pr['power'][upper]

		# scores_out['min_st'] = [round(diff_down_pr['interval'][lower],2)]
		# scores_out['min_st_power'] = diff_down_pr['power'][lower]

		# scores_out['max_tp'] = [round(diff_top_pr['interval'][upper],2)]
		# scores_out['max_tp_power'] = diff_top_pr['power'][upper]

		# scores_out['min_tp'] = [round(diff_top_pr['interval'][lower],2)]
		# scores_out['min_tp_power'] = diff_top_pr['power'][lower]


		# scores_out['value_front_intervals_pr_upper'] = [value_front_intervals_pr['interval'][upper]]
		# scores_out['value_front_intervals_pr_upper_power'] = value_front_intervals_pr['power'][upper]

		# scores_out['value_front_intervals_pr_lower'] = [value_front_intervals_pr['interval'][lower]]
		# scores_out['value_front_intervals_pr_lower_power'] = value_front_intervals_pr['power'][lower]

		# scores_out['value_back_intervals_pr_upper'] = [value_back_intervals_pr['interval'][upper]]
		# scores_out['value_back_intervals_pr_upper_power'] = value_back_intervals_pr['power'][upper]

		# scores_out['value_back_intervals_pr_lower'] = [value_back_intervals_pr['interval'][lower]]
		# scores_out['value_back_intervals_pr_lower_power'] = value_back_intervals_pr['power'][lower]

		# scores_out['diff_extereme_pr'] = [round(diff_extereme_pr['interval'][upper])]

		if scores_out['num_trade_pr'][0] != 0:

			if scores_out['num_st_pr'][0] != 0:
				score_num_tp = (tp_counter-scores_out['num_st_pr'][0])

				if (tp_counter-scores_out['num_st_pr'][0] == 0):
					score_num_tp = 15

				elif (score_num_tp > 0):
					score_num_tp = 20
				else:
					score_num_tp = 0.04

			else:
				if tp_counter != 0:
					score_num_tp = 25
				else:
					score_num_tp = 1
		else:
			score_num_tp = 1

		if scores_out['max_st_pr'][0] != 0:
			score_max_tp = (scores_out['max_tp_pr'][0]-scores_out['max_st_pr'][0])

			if (score_max_tp > 0):
				score_max_tp = score_max_tp * 9
			else:
				score_max_tp = 1

		else:
			score_max_tp = scores_out['max_tp_pr'][0]
			if (scores_out['max_tp_pr'][0] != 0):
				score_max_tp = scores_out['max_tp_pr'][0] * 10


		if (scores_out['mean_st_pr'][0] != 0):
			score_mean_tp = (scores_out['mean_tp_pr'][0]-scores_out['mean_st_pr'][0])

			if (score_mean_tp > 0):
				score_mean_tp = 2#score_mean_tp * 100
			elif (score_mean_tp == 0):
				score_mean_tp = 1.5
			else:
				score_mean_tp = 1

		else:
			score_mean_tp = scores_out['mean_tp_pr'][0]
			if (scores_out['mean_tp_pr'][0] != 0):
				score_mean_tp = 2.5#scores_out['mean_tp_pr'][0] * 200


		if (scores_out['sum_st_pr'][0] != 0):
			score_sum_tp = (scores_out['sum_tp_pr'][0]-scores_out['sum_st_pr'][0])

			if (score_sum_tp > 0):
				score_sum_tp = score_sum_tp * 9
			else:
				score_sum_tp = 0.1

		else:
			score_sum_tp = scores_out['sum_tp_pr'][0]
			if (scores_out['sum_tp_pr'][0] != 0):
				score_sum_tp = scores_out['sum_tp_pr'][0] * 10

		score_sum_tp = (score_sum_tp/scores_out['num_trade_pr'][0])*100

		score_money = (round(((np.mean(signal['money']) - signal['money'][np.min(signal['money'].index)])/signal['money'][np.min(signal['money'].index)]),2) * 100) / scores_out['num_trade_pr'][0]

		scores_out['money'] = [score_money * scores_out['num_trade_pr'][0]]

		if score_money <= 0 : score_money = 1

		scores_out['score_pr'] = [(score_num_tp*score_sum_tp*score_mean_tp*score_money)]
			

		if np.isnan(scores_out['score_pr'][0]) : scores_out['score_pr'][0] = 0

		scores_out['methode'] = ['pr']

		return scores_out


	def Run_GL(self, signal, sigtype, flaglearn, flagtest):

		signal = self.ProfitFlagFinder(signal = signal, sigtype = sigtype, flaglearn = flaglearn, flagtest = flagtest)

		scores = self.Scoring(signal = signal)

		return signal, scores
