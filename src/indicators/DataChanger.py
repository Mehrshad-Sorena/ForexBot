import numpy as np
try:
	import cudf as pd
except:
	try:
		import modin.pandas as pd
	except:
		import pandas as pd

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

		data_splited = data.truncate(before=cut_first, after=int(len(data.low)-1), axis=None, copy=True).reset_index(drop=True)

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

		dataset_pr_5M = dataset_5M.truncate(before=cut_first, after=int(loc_end_5M-1), axis=None, copy=True).reset_index(drop=True)

		location_1H = -1
		list_time = np.where(
							(dataset_1H['time'].dt.year.to_numpy() == dataset_5M['time'][int(loc_end_5M-1)].year) &
							(dataset_1H['time'].dt.month.to_numpy() == dataset_5M['time'][int(loc_end_5M-1)].month) &
							(dataset_1H['time'].dt.day.to_numpy() == dataset_5M['time'][int(loc_end_5M-1)].day) &
							(dataset_1H['time'].dt.hour.to_numpy() == dataset_5M['time'][int(loc_end_5M-1)].hour)
							)[0]
		try:
			location_1H = list_time[0] + 1
		except:
			location_1H = 0

		if location_1H <= 1: return pd.DataFrame(), pd.DataFrame()

		cut_first_1H = 0
		if location_1H >= length_1H:
			cut_first_1H = location_1H - length_1H

		dataset_pr_1H = dataset_1H.truncate(before=cut_first_1H, after=int(location_1H-1), axis=None, copy=True).reset_index(drop=True)

		return dataset_pr_5M, dataset_pr_1H