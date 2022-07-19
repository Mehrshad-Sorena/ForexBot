import pandas as pd
import numpy as np

class DataChanger:

	def Spliter(
				self,
				data,
				length
				):

		data_splited = pd.DataFrame()
		cut_first = 0

		if (
			int(len(data.low)-1) > length
			):

			cut_first = int(len(data.low)-1) - length

		data_splited['low'] = data.low[
										cut_first:int(len(data.low)-1)
										].reset_index(drop=True)

		data_splited['high'] = data.high[
										cut_first:int(len(data.high)-1)
										].reset_index(drop=True)

		data_splited['close'] = data.close[
											cut_first:int(len(data.close)-1)
											].reset_index(drop=True)

		data_splited['open'] = data.open[
										cut_first:int(len(data.open)-1)
										].reset_index(drop=True)

		data_splited['time'] = data['time'][
										cut_first:int(len(data['time'])-1)
										].reset_index(drop=True)

		data_splited['volume'] = data['volume'][
										cut_first:int(len(data['volume'])-1)
										].reset_index(drop=True)

		data_splited['OHLC/4'] = data['OHLC/4'][
										cut_first:int(len(data['OHLC/4'])-1)
										].reset_index(drop=True)

		data_splited['HLCC/4'] = data['HLCC/4'][
										cut_first:int(len(data['HLCC/4'])-1)
										].reset_index(drop=True)

		data_splited['HLC/3'] = data['HLC/3'][
										cut_first:int(len(data['HLC/3'])-1)
										].reset_index(drop=True)

		data_splited['HL/2'] = data['HL/2'][
										cut_first:int(len(data['HL/2'])-1)
										].reset_index(drop=True)

		return data_splited

	def SpliterSyncPR(
						self,
						dataset_5M,
						dataset_1H,
						loc_end_5M,
						length_5M,
						length_1H,
						):
		dataset_pr_5M = pd.DataFrame()
		dataset_pr_1H = pd.DataFrame()

		cut_first = 0
		if (loc_end_5M > length_5M):
			cut_first = int(loc_end_5M) - length_5M

		dataset_pr_5M['low'] = dataset_5M['low'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['high'] = dataset_5M['high'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['close'] = dataset_5M['close'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['open'] = dataset_5M['open'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['volume'] = dataset_5M['volume'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['OHLC/4'] = dataset_5M['OHLC/4'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['HLCC/4'] = dataset_5M['HLCC/4'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['HLC/3'] = dataset_5M['HLC/3'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['HL/2'] = dataset_5M['HL/2'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_5M['time'] = dataset_5M['time'][cut_first:int(loc_end_5M)].reset_index(drop=True)

		location_1H = -1
		list_time = np.where(
							(dataset_1H['time'].dt.year.to_numpy() == dataset_5M['time'][int(loc_end_5M)].year) &
							(dataset_1H['time'].dt.month.to_numpy() == dataset_5M['time'][int(loc_end_5M)].month) &
							(dataset_1H['time'].dt.day.to_numpy() == dataset_5M['time'][int(loc_end_5M)].day) &
							(dataset_1H['time'].dt.hour.to_numpy() == dataset_5M['time'][int(loc_end_5M)].hour)
							)[0]
		try:
			location_1H = list_time[0] + 1
		except:
			location_1H = 0

		cut_first_1H = 0
		if location_1H >= length_1H:
			cut_first_1H = location_1H - length_1H

		dataset_pr_1H['low'] = dataset_1H['low'][cut_first_1H:location_1H].reset_index(drop=True)
		dataset_pr_1H['high'] = dataset_1H['high'][cut_first_1H:location_1H].reset_index(drop=True)
		dataset_pr_1H['close'] = dataset_1H['close'][cut_first_1H:location_1H].reset_index(drop=True)
		dataset_pr_1H['open'] = dataset_1H['open'][cut_first_1H:location_1H].reset_index(drop=True)
		dataset_pr_1H['volume'] = dataset_1H['volume'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_1H['OHLC/4'] = dataset_1H['OHLC/4'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_1H['HLCC/4'] = dataset_1H['HLCC/4'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_1H['HLC/3'] = dataset_1H['HLC/3'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_1H['HL/2'] = dataset_1H['HL/2'][cut_first:int(loc_end_5M)].reset_index(drop=True)
		dataset_pr_1H['time'] = dataset_1H['time'][cut_first:int(loc_end_5M)].reset_index(drop=True)

		return dataset_pr_5M, dataset_pr_1H