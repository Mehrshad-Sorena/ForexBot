from indicator_BestFinder import BestFinder
import ExtremePoints as extremepoints
from pr_Runner import Runner
from timer import stTime
import pandas as pd
import numpy as np


class Tester:

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

							#Best Finder Params:

							'BestFinder' + '_n_clusters': parameters.elements['BestFinder' + '_n_clusters'],
							'BestFinder_alpha': parameters.elements['BestFinder_alpha'],

							#/////////////////////

							#Tester:

							'Tester_money': parameters.elements['Tester_money'],
							'Tester_coef_money': parameters.elements['Tester_coef_money'],

							#/////////////////////////
							
							})
	#@stTime
	def RunGL(self, signal, sigtype, flaglearn, flagtest, pr_parameters, pr_config, indicator = '', flag_savepic = False):

		signal = self.ProfitFlagFinder(
										signal = signal, 
										sigtype = sigtype, 
										flaglearn = flaglearn, 
										flagtest = flagtest,
										pr_parameters = pr_parameters,
										pr_config = pr_config,
										indicator = indicator,
										flag_savepic = flag_savepic
										)

		scores = self.Scoring(signal = signal)

		return signal, scores

	
	def ProfitFlagFinder(self, signal, sigtype, flaglearn, flagtest, pr_parameters, pr_config, indicator = '', flag_savepic = False):

		#*************************************************************
		# Bayad Maghadir Baraye Params Va Config As func baraye PR dar GA , Learner daryaft beshan

		#/////////////////////////////////////////////////////////////

		pr_Runner = Runner(parameters = pr_parameters, config = pr_config)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig1 = ',signal)

		signals = pd.DataFrame(
								{
									'index': signal['index'].values, 
								},
								index = signal['index'].values
								)

		self.elements['symbol'] = signal['symbol'][signal.index[0]]

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig1 = ',signal)

		signals = pr_Runner.run(
								dataset_5M = self.elements['dataset_5M'][self.elements['symbol']], 
								dataset_1H = self.elements['dataset_1H'][self.elements['symbol']],
								signals_index = signals,
								sigtype = sigtype,
								flaglearn = flaglearn,
								flagtest = flagtest,
								indicator = indicator,
								signals = signal,
								flag_savepic = flag_savepic
								)

		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# 	print('sig2 = ',signal)

		signal = signal.drop(columns = ['index'], inplace = False)

		signal = signal.join(signals).dropna(inplace = False)

		return signal

	
	def Scoring(self, signal):
		
		scores_out = pd.DataFrame()

		scores_out['mean_tp_pr'] = [np.mean(signal['tp_pr'][signal['index'][signal['flag'] != 'no_flag']])]
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

		#Finding Best Values:

		scores_out = self.BestPreparer(signal = signal, scores_out = scores_out)

		#///////////////////////////

		if scores_out['num_trade_pr'][0] != 0:

			if scores_out['num_trade_pr'][0] >= 20:
				score_num_tp = ((scores_out['num_tp_pr'][0]-scores_out['num_st_pr'][0])/scores_out['num_trade_pr'][0]) * 100

			else:
				score_num_tp = ((scores_out['num_tp_pr'][0]-scores_out['num_st_pr'][0])/20) * 100
		else:
			score_num_tp = 1

		if score_num_tp <= 0: score_num_tp = 1


		if (scores_out['mean_tp_pr'][0]+scores_out['mean_st_pr'][0]) != 0:
			score_mean_tp = ((scores_out['mean_tp_pr'][0]-scores_out['mean_st_pr'][0])/(scores_out['mean_tp_pr'][0]+scores_out['mean_st_pr'][0])) * 100
		else:
			score_mean_tp = 1

		if score_mean_tp <= 0: score_mean_tp = 1


		if (scores_out['max_tp_pr'][0]+scores_out['max_st_pr'][0]) != 0:
			score_max_tp = ((scores_out['max_tp_pr'][0]-scores_out['max_st_pr'][0])/(scores_out['max_tp_pr'][0]+scores_out['max_st_pr'][0])) * 100
		else:
			score_max_tp = 1

		if score_max_tp <= 0: score_max_tp = 1


		if (scores_out['sum_tp_pr'][0]+scores_out['sum_st_pr'][0]) != 0:
			score_sum_tp = ((scores_out['sum_tp_pr'][0]-scores_out['sum_st_pr'][0])/(scores_out['sum_tp_pr'][0]+scores_out['sum_st_pr'][0])) * 100
		else:
			score_sum_tp = 1

		if score_sum_tp <= 0: score_sum_tp = 1


		# Calculate Score Of Money:

		ideal_money = self.IdealMoneyCalc(scores_out = scores_out)

		score_money = ((ideal_money - signal['money'][np.max(signal['money'].index)])/ideal_money) * 100
		score_money = 100 - score_money
		scores_out['money'] = [signal['money'][np.max(signal['money'].index)]]

		if score_money <= 0: score_money = 1

		#//////////////////////////////

		#DrawDown Calculation:

		draw_down = self.DrawDownCalc(signal = signal)

		score_drow_down = 100 - draw_down

		scores_out['draw_down'] = [draw_down]

		if score_drow_down <= 0: score_drow_down = 1

		#////////////////////////////////

		normalizer = 100 * 100 * 100 * 100 * 100 * 100

		scores_out['score'] = [((score_num_tp*score_sum_tp*score_mean_tp*score_max_tp*score_money*score_drow_down)/normalizer) * 100]
			

		if np.isnan(scores_out['score'][0]) : scores_out['score'][0] = 0

		scores_out['methode'] = ['pr']

		return scores_out

	def DrawDownCalc(self, signal):

		extremes_points = extremepoints.finder(
												high = signal['money'].reset_index()['money'],
												low = signal['money'].reset_index()['money'],
												number_min = 1,
												number_max = 1
												)

		max_money = pd.DataFrame(
									{
										'max': extremes_points['max'],
										'index': extremes_points['index_max'],
									}
									).dropna(inplace = False).sort_values(by = ['index'])

		max_money['index'] = max_money['index'].astype('int32').reset_index()['index']
		draw_down = list(range(0,len(max_money['index'])-1))

		for idx in max_money['index'].index:

			if idx + 1 >= len(max_money['index']): break

			min_money = signal['money'].reset_index()['money'][max_money['index'][idx]:max_money['index'][idx+1]].min()
			draw_down[idx] = ((max_money['max'][idx] - min_money)/max_money['max'][idx]) * 100

		if len(draw_down) > 1:
			draw_down = np.max(draw_down)
		elif len(draw_down) == 1:
			draw_down = draw_down[0]
		else:
			draw_down = 0

		return draw_down


	def IdealMoneyCalc(self, scores_out):

		my_money = self.elements['Tester_money']
		coef_money = self.elements['Tester_coef_money']

		for i in range(0,scores_out['num_tp_pr'][0]):

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			if lot > 2000: lot = 2000

			my_money = my_money + (lot * scores_out['mean_tp_pr'][0])

		ideal_money = my_money

		return ideal_money

	def BestPreparer(self, signal, scores_out):

		best_values = BestFinder(parameters = self)

		upper = 0
		mid = 1
		lower = 2

		value_front_intervals_pr = best_values.Finder(
														signals = signal,
														apply_to='indicator_front',
														)

		value_back_intervals_pr = best_values.Finder(
													signals=signal,
													apply_to='indicator_back',
													)


		diff_top_pr = best_values.Finder(
												signals=signal,
												apply_to='tp_pr',
												)

		diff_down_pr = best_values.Finder(
												signals=signal,
												apply_to='st_pr',
												)

		diff_extereme = best_values.Finder(
												signals=signal,
												apply_to='diff_extereme',
												)


		scores_out['max_st'] = [round(diff_down_pr['interval'][upper],2)]
		scores_out['max_st_power'] = diff_down_pr['power'][upper]

		scores_out['min_st'] = [round(diff_down_pr['interval'][lower],2)]
		scores_out['min_st_power'] = diff_down_pr['power'][lower]

		scores_out['max_tp'] = [round(diff_top_pr['interval'][upper],2)]
		scores_out['max_tp_power'] = diff_top_pr['power'][upper]

		scores_out['min_tp'] = [round(diff_top_pr['interval'][lower],2)]
		scores_out['min_tp_power'] = diff_top_pr['power'][lower]


		scores_out['value_front_intervals_pr_upper'] = [value_front_intervals_pr['interval'][upper]]
		scores_out['value_front_intervals_pr_upper_power'] = value_front_intervals_pr['power'][upper]

		scores_out['value_front_intervals_pr_lower'] = [value_front_intervals_pr['interval'][lower]]
		scores_out['value_front_intervals_pr_lower_power'] = value_front_intervals_pr['power'][lower]

		scores_out['value_back_intervals_pr_upper'] = [value_back_intervals_pr['interval'][upper]]
		scores_out['value_back_intervals_pr_upper_power'] = value_back_intervals_pr['power'][upper]

		scores_out['value_back_intervals_pr_lower'] = [value_back_intervals_pr['interval'][lower]]
		scores_out['value_back_intervals_pr_lower_power'] = value_back_intervals_pr['power'][lower]

		scores_out['diff_extereme'] = [round(diff_extereme['interval'][upper])]

		return scores_out
