import numpy as np
import pandas as pd
from pr_Parameters import Parameters

class Tester:

	parameters = Parameters()

	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict(
							{

							#Elemns For Tester:

							__class__.__name__ + '_coef_money': parameters.elements['Tester_coef_money'],
							__class__.__name__ + '_spred': parameters.elements['Tester_spred'],

							#////////////////////////////////

							#Elemns Gloal:

							'st_percent_min': parameters.elements['st_percent_min'],
							'st_percent_max': parameters.elements['st_percent_max'],

							'tp_percent_min': parameters.elements['tp_percent_min'],
							'tp_percent_max': parameters.elements['tp_percent_max'],

							#////////////////////////////////
							}
							)

		self.cfg = dict(
							{

							#Config For Tester:

							__class__.__name__ + '_flag_realtest': config.cfg['Tester_flag_realtest'],

							#/////////////////////////

							}
						)

		#*****************************

	def FlagFinderBuy(self, dataset_5M, extereme, flaglearn, loc_end_5M, money):
		
		spred = self.elements['Tester_spred']

		diff_pr_top = (((extereme['high_upper'][loc_end_5M]) - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
		diff_pr_down = ((dataset_5M['low'][loc_end_5M] - (extereme['low_lower'][loc_end_5M]))/dataset_5M['low'][loc_end_5M]) * 100

		st_percent_min = self.elements['st_percent_min']
		st_percent_max = self.elements['st_percent_max']

		tp_percent_min = self.elements['tp_percent_min']
		tp_percent_max = self.elements['tp_percent_max']

		if flaglearn == False:
			if diff_pr_down < st_percent_min:
				diff_pr_down = st_percent_min
				extereme['low_lower'][loc_end_5M] = dataset_5M['low'][loc_end_5M] * (1-(st_percent_min/100))

			if diff_pr_top < tp_percent_min:
				diff_pr_top = tp_percent_min
				extereme['high_upper'][loc_end_5M] = dataset_5M['high'][loc_end_5M] * (1+(tp_percent_min/100))

		if diff_pr_down > st_percent_max:
			diff_pr_down = st_percent_max
			extereme['low_lower'][loc_end_5M] = dataset_5M['low'][loc_end_5M] * (1-(st_percent_max/100))
		
		if diff_pr_top > tp_percent_max:
			diff_pr_top = tp_percent_max
			extereme['high_upper'][loc_end_5M] = dataset_5M['high'][loc_end_5M] * (1+(tp_percent_max/100))

		if (
			dataset_5M['high'][loc_end_5M] >= extereme['high_upper'][loc_end_5M] or
			dataset_5M['low'][loc_end_5M] <= extereme['low_lower'][loc_end_5M]
			):
			extereme = extereme.assign(
										flag =  'no_flag',
										tp_pr =  np.nan,
										st_pr =  np.nan,
										index_tp =  np.nan,
										index_st = np.nan,
										money = money,
										time = np.nan,
										)
			return extereme

		#*************** Finding Take Profit:

		if (len(np.where(((dataset_5M['high'][(loc_end_5M):-1].values) >= extereme['high_upper'][loc_end_5M]))[0]) > 1):
			index_tp =	loc_end_5M + min(
										np.where(
													(
														(dataset_5M['high'][(loc_end_5M):-1].values) >= extereme['high_upper'][loc_end_5M]
													)
												)[0] 
										)

		elif (len(np.where(((dataset_5M['high'][(loc_end_5M):-1].values) >= extereme['high_upper'][loc_end_5M]))[0]) == 1):
			index_tp =	loc_end_5M + np.where(
												(
													(dataset_5M['high'][(loc_end_5M):-1].values) >= extereme['high_upper'][loc_end_5M]
												)
											)[0][0] 

		else:
			index_tp = -1
			tp_pr = 0
		#///////////////////////////////

		#************ Finding Stop Loss:

		if (len(np.where(((dataset_5M['low'][(loc_end_5M):-1].values) <= extereme['low_lower'][loc_end_5M]))[0]) > 1):
			index_st =	loc_end_5M + min(
										np.where(
													(
														(dataset_5M['low'][(loc_end_5M):-1].values) <= extereme['low_lower'][loc_end_5M]
													)
												)[0]
										)

		elif (len(np.where(((dataset_5M['low'][(loc_end_5M):-1].values) <= extereme['low_lower'][loc_end_5M]))[0]) == 1):
			index_st =	loc_end_5M + np.where(
												(
													(dataset_5M['low'][(loc_end_5M):-1].values) <= extereme['low_lower'][loc_end_5M]
												)
											)[0][0]

		else:
			index_st = -1
			st_pr = 0

		if (
			index_tp < index_st and
			index_tp != -1
			):

			st_pr = ((dataset_5M['low'][loc_end_5M] - np.min(dataset_5M['low'][loc_end_5M:index_tp]))/dataset_5M['low'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['high'][index_tp] - dataset_5M['high'][loc_end_5M]*(1 + spred))/(dataset_5M['high'][loc_end_5M] * (1 + spred))) * 100

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money + (lot * tp_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'tp',
										tp_pr = tp_pr,
										st_pr = st_pr,
										index_tp = index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_tp != -1 and
			index_st == -1
			):
			st_pr = ((dataset_5M['low'][loc_end_5M] - np.min(dataset_5M['low'][loc_end_5M:index_tp]))/dataset_5M['low'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['high'][index_tp] - dataset_5M['high'][loc_end_5M]*(1 + spred))/(dataset_5M['high'][loc_end_5M] * (1 + spred))) * 100

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money + (lot * tp_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'tp',
										tp_pr = tp_pr,
										st_pr = st_pr,
										index_tp = index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_st < index_tp and
			index_st != -1
			):
			st_pr = ((dataset_5M['low'][loc_end_5M] - dataset_5M['low'][index_st])/dataset_5M['low'][loc_end_5M]) * 100
			tp_pr = ((np.max(dataset_5M['high'][loc_end_5M:index_st]) - dataset_5M['high'][loc_end_5M]*(1 + spred))/(dataset_5M['high'][loc_end_5M] * (1 + spred))) * 100

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money - (lot * st_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'st',
										tp_pr =  tp_pr,
										st_pr =  st_pr,
										index_tp =  index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_tp == -1 and
			index_st != -1
			):
			st_pr = ((dataset_5M['low'][loc_end_5M] - dataset_5M['low'][index_st])/dataset_5M['low'][loc_end_5M]) * 100
			tp_pr = ((np.max(dataset_5M['high'][loc_end_5M:index_st]) - dataset_5M['high'][loc_end_5M]*(1 + spred))/(dataset_5M['high'][loc_end_5M] * (1 + spred))) * 100
			
			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money - (lot * st_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'st',
										tp_pr =  tp_pr,
										st_pr =  st_pr,
										index_tp =  index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		if index_st == index_tp:

			if index_st != -1:
				st_pr = ((dataset_5M['low'][loc_end_5M] - dataset_5M['low'][index_st])/dataset_5M['low'][loc_end_5M]) * 100
				tp_pr = ((np.max(dataset_5M['high'][loc_end_5M:index_st]) - dataset_5M['high'][loc_end_5M]*(1 + spred))/(dataset_5M['high'][loc_end_5M] * (1 + spred))) * 100
				
				my_money = money
				coef_money = self.elements['Tester_coef_money']

				if my_money >=100:
					lot = int(my_money/100) * coef_money
				else:
					lot = coef_money

				my_money = my_money - (lot * st_pr)

				money = my_money

				extereme = extereme.assign(
											flag =  'st',
											tp_pr =  tp_pr,
											st_pr =  st_pr,
											index_tp =  index_tp,
											index_st = index_st,
											money = my_money,
											time = dataset_5M['time'][loc_end_5M],
											)
			else:
				extereme = extereme.assign(
											flag =  'no_flag',
											tp_pr =  np.nan,
											st_pr =  np.nan,
											index_tp =  np.nan,
											index_st = np.nan,
											money = money,
											time = np.nan,
											)

		return extereme

	#////////////////////////////


	#******************************

	def FlagFinderSell(self, dataset_5M, extereme, flaglearn, loc_end_5M, money):
		
		spred = self.elements['Tester_spred']

		diff_pr_top = (((extereme['high_upper'][loc_end_5M]) - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
		diff_pr_down = ((dataset_5M['low'][loc_end_5M] - (extereme['low_lower'][loc_end_5M]))/dataset_5M['low'][loc_end_5M]) * 100

		st_percent_min = self.elements['st_percent_min']
		st_percent_max = self.elements['st_percent_max']

		tp_percent_min = self.elements['tp_percent_min']
		tp_percent_max = self.elements['tp_percent_max']
			

		if flaglearn == False:
			if diff_pr_top < st_percent_min:
				diff_pr_top = st_percent_min
				extereme['high_upper'][loc_end_5M] = dataset_5M['high'][loc_end_5M] * (1+(st_percent_min/100))

			if diff_pr_down < tp_percent_min:
				diff_pr_down = tp_percent_min
				extereme['low_lower'][loc_end_5M] = dataset_5M['low'][loc_end_5M] * (1-(tp_percent_min/100))

		if diff_pr_top > st_percent_max:
			diff_pr_top = st_percent_max
			extereme['high_upper'][loc_end_5M] = dataset_5M['high'][loc_end_5M] * (1+(st_percent_max/100))
		
		if diff_pr_down > tp_percent_max:
			diff_pr_down = tp_percent_max
			extereme['low_lower'][loc_end_5M] = dataset_5M['low'][loc_end_5M] * (1-(tp_percent_max/100))


		if (
			dataset_5M['high'][loc_end_5M] >= extereme['high_upper'][loc_end_5M] or
			dataset_5M['low'][loc_end_5M] <= extereme['low_lower'][loc_end_5M]
			):
			extereme = extereme.assign(
										flag =  'no_flag',
										tp_pr =  np.nan,
										st_pr =  np.nan,
										index_tp =  np.nan,
										index_st = np.nan,
										money = money,
										time = np.nan,
										)
			return extereme

		#*************** Finding Take Profit:

		if (len(np.where(((dataset_5M['low'][(loc_end_5M):-1].values * (1 + spred)) <= extereme['low_lower'][loc_end_5M]))[0]) > 1):
			index_tp =	loc_end_5M + min(
										np.where(
													(
														(dataset_5M['low'][(loc_end_5M):-1].values) * (1 + spred) <= extereme['low_lower'][loc_end_5M]
													)
												)[0] 
										)

		elif (len(np.where(((dataset_5M['low'][(loc_end_5M):-1].values * (1 + spred)) <= extereme['low_lower'][loc_end_5M]))[0]) == 1):
			index_tp =	loc_end_5M + np.where(
												(
													(dataset_5M['low'][(loc_end_5M):-1].values * (1 + spred)) <= extereme['low_lower'][loc_end_5M]
												)
											)[0][0] 

		else:
			index_tp = -1
			tp_pr = 0
		#///////////////////////////////

		#************ Finding Stop Loss:

		if (len(np.where(((dataset_5M['high'][(loc_end_5M):-1].values * (1 + spred)) >= extereme['high_upper'][loc_end_5M]))[0]) > 1):
			index_st =	loc_end_5M + min(
										np.where(
													(
														(dataset_5M['high'][(loc_end_5M):-1].values * (1 + spred)) >= extereme['high_upper'][loc_end_5M]
													)
												)[0]
										)

		elif (len(np.where(((dataset_5M['high'][(loc_end_5M):-1].values * (1 + spred)) >= extereme['high_upper'][loc_end_5M]))[0]) == 1):
			index_st =	loc_end_5M + np.where(
												(
													(dataset_5M['high'][(loc_end_5M):-1].values * (1 + spred)) >= extereme['high_upper'][loc_end_5M]
												)
											)[0][0]

		else:
			index_st = -1
			st_pr = 0

		if (
			index_tp < index_st and
			index_tp != -1
			):

			st_pr = ((np.max(dataset_5M['high'][loc_end_5M:index_tp]) - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['low'][loc_end_5M] - dataset_5M['low'][index_tp] * (1 + spred))/(dataset_5M['low'][loc_end_5M])) * 100

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money + (lot * tp_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'tp',
										tp_pr = tp_pr,
										st_pr = st_pr,
										index_tp = index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_tp != -1 and
			index_st == -1
			):
			st_pr = ((np.max(dataset_5M['high'][loc_end_5M:index_tp]) - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['low'][loc_end_5M] - dataset_5M['low'][index_tp] * (1 + spred))/(dataset_5M['low'][loc_end_5M])) * 100

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money + (lot * tp_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'tp',
										tp_pr = tp_pr,
										st_pr = st_pr,
										index_tp = index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_st < index_tp and
			index_st != -1
			):
			st_pr = ((dataset_5M['high'][index_st] - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['low'][loc_end_5M] - np.min(dataset_5M['low'][loc_end_5M:index_st]) * (1 + spred))/(dataset_5M['low'][loc_end_5M])) * 100
			

			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money - (lot * st_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'st',
										tp_pr =  tp_pr,
										st_pr =  st_pr,
										index_tp =  index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		elif (
			index_tp == -1 and
			index_st != -1
			):
			st_pr = ((dataset_5M['high'][index_st] - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
			tp_pr = ((dataset_5M['low'][loc_end_5M] - np.min(dataset_5M['low'][loc_end_5M:index_st]) * (1 + spred))/(dataset_5M['low'][loc_end_5M])) * 100
			
			my_money = money
			coef_money = self.elements['Tester_coef_money']

			if my_money >=100:
				lot = int(my_money/100) * coef_money
			else:
				lot = coef_money

			my_money = my_money - (lot * st_pr)

			money = my_money

			extereme = extereme.assign(
										flag =  'st',
										tp_pr =  tp_pr,
										st_pr =  st_pr,
										index_tp =  index_tp,
										index_st = index_st,
										money = my_money,
										time = dataset_5M['time'][loc_end_5M],
										)

		if index_st == index_tp:

			if index_st != -1:
				st_pr = ((dataset_5M['high'][index_st] - dataset_5M['high'][loc_end_5M])/dataset_5M['high'][loc_end_5M]) * 100
				tp_pr = ((dataset_5M['low'][loc_end_5M] - np.min(dataset_5M['low'][loc_end_5M:index_st]) * (1 + spred))/(dataset_5M['low'][loc_end_5M])) * 100
				
				my_money = money
				coef_money = self.elements['Tester_coef_money']

				if my_money >=100:
					lot = int(my_money/100) * coef_money
				else:
					lot = coef_money

				my_money = my_money - (lot * st_pr)

				money = my_money

				extereme = extereme.assign(
											flag =  'st',
											tp_pr =  tp_pr,
											st_pr =  st_pr,
											index_tp =  index_tp,
											index_st = index_st,
											money = my_money,
											time = dataset_5M['time'][loc_end_5M],
											)
			else:
				extereme = extereme.assign(
											flag =  'no_flag',
											tp_pr =  np.nan,
											st_pr =  np.nan,
											index_tp =  np.nan,
											index_st = np.nan,
											money = money,
											time = np.nan,
											)

		return extereme


	#/////////////////////////////