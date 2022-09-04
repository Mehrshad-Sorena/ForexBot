import winsound
import threading
from ConfigOptimizers import Config as ConfigOptimizers
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config
from src.Indicators.MACD import MACD
from indicator_Divergence import Divergence
from src.Indicators.MACD.Parameters import Parameters
from src.Indicators.MACD.Config import Config
import time


class Optimizers():

	def __init__(self):

		self.symbol = 'XAUUSD_i'
		self.sigpriority = 'primary'
		self.sigtype = 'buy'
		self.main_turn = 10
		self.turn = 100
		self.dataset = pd.DataFrame()
		self.timeframe = '5M'


	def FreqFinder(ts, detrend='linear'):
	    from scipy.signal import periodogram

	    if self.timeframe == '5M':
	    	min_time = '5T'

	    elif self.timeframe == '1H':
	    	min_time = '1H'

	    fs = pd.Timedelta("1Y") / pd.Timedelta(min_time)

	    freqencies, spectrum = periodogram(
									        ts,
									        fs=fs,
									        detrend=detrend,
									        window="boxcar",
									        scaling='spectrum',
									    )
	    spectrum_counter = 0
	    for elm in spectrum:
	    	if elm == np.max(spectrum):
	    		freq = freqencies[spectrum_counter]
	    	spectrum_counter += 1

	    period_time = (freq * pd.Timedelta(min_time))/pd.Timedelta("1Y")

	    return round(freq)


	def MacdOptimizer():

		print('Start ...')

		configoptimizers = ConfigOptimizers()
		macd_parameters = Parameters()
		macd_config = Config()

		ind_params = indicator_parameters()
		ind_config = indicator_config()

		self.dataset = self.dataset.assign(index = self.dataset.index)

		freq = self.FreqFinder(self.dataset.close)

		if self.timeframe == '5M':
			freq_time = str(5 * freq) + 'T'
		elif self.timeframe == '1H':
			freq_time = str(freq) + 'H'

		self.dataset = self.dataset.set_index('time').resample(freq_time).last().dropna()
		self.dataset = self.dataset.assign(time = self.dataset.index)
		self.dataset = self.dataset.set_index('index')

		path = configoptimizers.cfg['path_macd'] + '/' + self.sigtype + '/' + self.sigpriority+ '/' + self.timeframe + '/'

		if not os.path.exists(path):
			os.makedirs(path)

		path = configoptimizers.cfg['path_macd'] + '/' + self.sigtype + '/' + self.sigpriority+ '/' + self.timeframe + '/' + self.symbol + '.csv'

		if os.path.exists(path):
			output_read = pd.read_csv(path).drop(columns = ['Unnamed: 0'])
		else:
			output_read = pd.DataFrame()
			output_read['MACD_apply_to'] = np.nan
			output_read['MACD_fast'] = np.nan
			output_read['MACD_slow'] = np.nan
			output_read['MACD_signal'] = np.nan
			output_read['MACD_column_div'] = np.nan
			output_read['corr_low'] = np.nan
			output_read['corr_high'] = np.nan
			output_read['diff_divergence'] = np.nan
			output_read['num_extreme_min'] = np.nan
			output_read['num_extreme_max'] = np.nan
			output_read['score'] = np.nan
		
		output = pd.DataFrame(np.ones(self.turn))
		output['MACD_apply_to'] = np.nan
		output['MACD_fast'] = np.nan
		output['MACD_slow'] = np.nan
		output['MACD_signal'] = np.nan
		output['MACD_column_div'] = np.nan
		output['corr_low'] = np.nan
		output['corr_high'] = np.nan
		output['diff_divergence'] = np.nan
		output['num_extreme_min'] = np.nan
		output['num_extreme_max'] = np.nan
		output['score'] = np.nan

		for i in range(self.turn):
			macd_parameters.elements['MACD' + '_apply_to'] = random.choice([
																		'open',
																		'close',
																		'low',
																		'high',
																		'HL/2',
																		'HLC/3',
																		'HLCC/4',
																		'OHLC/4'
																		])
			macd_parameters.elements['MACD' + '_fast'] = randint(2, 300)
			macd_parameters.elements['MACD' + '_slow'] = randint(2 , 700)
			macd_parameters.elements['MACD' + '_signal'] = randint(2 , 50)

			ind_params.elements['Divergence' + '_diff_extereme'] = randint(1 , 6)
			ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(2 , 500)
			ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(2 , 500)

			dive_column = random.choice(['macd', 'macds', 'macdh'])

			while macd_parameters.elements['MACD' + '_fast'] >= macd_parameters.elements['MACD' + '_slow'] + 10:
				macd_parameters.elements['MACD' + '_fast'] = randint(2, 300)
				macd_parameters.elements['MACD' + '_slow'] = randint(2 , 700)

			repeat_counter = 0
			if output.dropna().empty == False:

				repeat_checker_now = np.where(
											(macd_parameters.elements['MACD' + '_fast'] == output['MACD_fast'].values) &
											(macd_parameters.elements['MACD' + '_slow'] == output['MACD_slow'].values) &
											(macd_parameters.elements['MACD' + '_signal'] == output['MACD_signal'].values) &
											(ind_params.elements['Divergence' + '_diff_extereme'] == output['diff_divergence'].values) &
											(ind_params.elements['Divergence' + '_num_exteremes_min'] == output['num_extreme_min'].values) &
											(macd_parameters.elements['MACD' + '_apply_to'] == output['MACD_apply_to'].values) &
											(dive_column == output['MACD_column_div'].values)
										)[0]

				repeat_checker_before = np.where(
											(macd_parameters.elements['MACD' + '_fast'] == output_read['MACD_fast'].values) &
											(macd_parameters.elements['MACD' + '_slow'] == output_read['MACD_slow'].values) &
											(macd_parameters.elements['MACD' + '_signal'] == output_read['MACD_signal'].values) &
											(ind_params.elements['Divergence' + '_diff_extereme'] == output_read['diff_divergence'].values) &
											(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_read['num_extreme_min'].values) &
											(macd_parameters.elements['MACD' + '_apply_to'] == output_read['MACD_apply_to'].values) &
											(dive_column == output_read['MACD_column_div'].values)
										)[0]

				while (
						len(repeat_checker_now) > 0 or
						len(repeat_checker_before) >0
						):
					macd_parameters.elements['MACD' + '_apply_to'] = random.choice([
																				'open',
																				'close',
																				'low',
																				'high',
																				'HL/2',
																				'HLC/3',
																				'HLCC/4',
																				'OHLC/4'
																				])
					macd_parameters.elements['MACD' + '_fast'] = randint(2, 300)
					macd_parameters.elements['MACD' + '_slow'] = randint(2 , 700)
					macd_parameters.elements['MACD' + '_signal'] = randint(2 , 50)

					ind_params.elements['Divergence' + '_diff_extereme'] = randint(1 , 6)
					ind_params.elements['Divergence' + '_num_exteremes_min'] = randint(2 , 250)
					ind_params.elements['Divergence' + '_num_exteremes_max'] = randint(2 , 250)

					dive_column = random.choice(['macd', 'macds', 'macdh'])

					while macd_parameters.elements['MACD' + '_fast'] >= macd_parameters.elements['MACD' + '_slow'] + 10:
						macd_parameters.elements['MACD' + '_fast'] = randint(2, 300)
						macd_parameters.elements['MACD' + '_slow'] = randint(2 , 700)

					repeat_checker_now = np.where(
											(macd_parameters.elements['MACD' + '_fast'] == output['MACD_fast'].values) &
											(macd_parameters.elements['MACD' + '_slow'] == output['MACD_slow'].values) &
											(macd_parameters.elements['MACD' + '_signal'] == output['MACD_signal'].values) &
											(ind_params.elements['Divergence' + '_diff_extereme'] == output['diff_divergence'].values) &
											(ind_params.elements['Divergence' + '_num_exteremes_min'] == output['num_extreme_min'].values) &
											(macd_parameters.elements['MACD' + '_apply_to'] == output['MACD_apply_to'].values) &
											(dive_column == output['MACD_column_div'].values)
										)[0]

					repeat_checker_before = np.where(
												(macd_parameters.elements['MACD' + '_fast'] == output_read['MACD_fast'].values) &
												(macd_parameters.elements['MACD' + '_slow'] == output_read['MACD_slow'].values) &
												(macd_parameters.elements['MACD' + '_signal'] == output_read['MACD_signal'].values) &
												(ind_params.elements['Divergence' + '_diff_extereme'] == output_read['diff_divergence'].values) &
												(ind_params.elements['Divergence' + '_num_exteremes_min'] == output_read['num_extreme_min'].values) &
												(macd_parameters.elements['MACD' + '_apply_to'] == output_read['MACD_apply_to'].values) &
												(dive_column == output_read['MACD_column_div'].values)
											)[0]

					if repeat_counter >= len(output_read['MACD_fast'].dropna().index): break
					repeat_counter += 1
				

			output['MACD_apply_to'][i] = macd_parameters.elements['MACD' + '_apply_to']
			output['MACD_fast'][i] = macd_parameters.elements['MACD' + '_fast']
			output['MACD_slow'][i] = macd_parameters.elements['MACD' + '_slow']
			output['MACD_signal'][i] = macd_parameters.elements['MACD' + '_signal']
			output['MACD_column_div'][i] = dive_column


			macd = MACD(parameters = macd_parameters, config = config)
			macd_calc = macd.calculator_macd()


			macd = Divergence(parameters = ind_params, config = ind_config)
			signal, signaltype, indicator = macd.divergence(
															sigtype = sigtype,
															sigpriority = sigpriority,
															indicator = macd_calc,
															column_div = dive_column,
															ind_name = 'macd',
															dataset_5M = macd_parameters.elements['dataset_' + self.timeframe],
															dataset_1H = macd_parameters.elements['dataset_' + self.timeframe],
															symbol = symbol,
															flaglearn = False,
															flagtest = True
															)
			if signal.empty == True: continue
			divergence_out = pd.DataFrame(np.ones(signal.index[-1]))
			divergence_out['macd'] = np.nan
			divergence_out['low'] = np.nan
			divergence_out['high'] = np.nan

			counter = 0
			for elm in signal.index:
				divergence_out['macd'][counter] = signal.indicator_front[elm]
				divergence_out['macd'][counter + 1] = signal.indicator_back[elm]

				divergence_out['low'][counter] = signal.low_front[elm]
				divergence_out['low'][counter + 1] = signal.low_back[elm]

				divergence_out['high'][counter] = signal.high_front[elm]
				divergence_out['high'][counter + 1] = signal.high_back[elm]

				counter += 2

			divergence_out = divergence_out.dropna()
			divergence_out = divergence_out.drop(columns = [0])

			number_divergence = len(divergence_out.index)/1000

			divergence_out = divergence_out.corr()

			output['score'][i] = -((divergence_out['macd'][2] * divergence_out['macd'][1] * number_divergence) ** (1/3))

			if (
				divergence_out['macd'][2] > 0 and
				divergence_out['macd'][1] > 0
				):
				output['score'][i] = -output['score'][i]

			output['corr_low'][i] = divergence_out['macd'][1]
			output['corr_high'][i] = divergence_out['macd'][2]
			output['diff_divergence'][i] = ind_params.elements['Divergence' + '_diff_extereme']
			output['num_extreme_min'][i] = ind_params.elements['Divergence' + '_num_exteremes_min']
			output['num_extreme_max'][i] = ind_params.elements['Divergence' + '_num_exteremes_max']
			#print(output.head(i))
			print('turn = ', self.main_turn * i, ', score = ', output_read['score'].min(), ' ', self.sigtype, ' ', self.sigpriority)

		if os.path.exists(path):
			os.remove(path)

		output = output.drop(columns = [0])
		output = pd.concat([output, output_read], ignore_index=True)

		output.dropna().sort_values(by = ['score'], ascending = False).to_csv(path)

		return output.dropna().sort_values(by = ['score'], ascending = False)