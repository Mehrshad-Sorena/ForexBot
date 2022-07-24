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
		

		return scores


	def Run_GL(self, signal, sigtype, flaglearn, flagtest):

		signal = self.ProfitFlagFinder(self, signal = signal, sigtype = sigtype, flaglearn = flaglearn, flagtest = flagtest)

		scores = self.Scoring(signal = signal)
