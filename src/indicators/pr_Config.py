class Config:

	def __init__(cls):
		
		cls.cfg = dict(
						{
						#Config For ExtremePoints:
						'ExtremePoints_status': True,
						'ExtremePoints_T_5M': False,
						'ExtremePoints_T_1H': False,
						#///////////////////////////


						#Config For TrendLines:
						'TrendLines_status': True,

						'TrendLines_T_5M': True,

						'TrendLines_long_T_5M': True,
						'TrendLines_mid_T_5M': True,
						'TrendLines_short1_T_5M': True,
						'TrendLines_short2_T_5M': True,

						'TrendLines_T_1H': True,

						'TrendLines_long_T_1H': True,
						'TrendLines_mid_T_1H': True,
						'TrendLines_short1_T_1H': True,
						'TrendLines_short2_T_1H': True,

						'TrendLines_plot': False,
						#///////////////////////////

						#Config For IchimokouFlatLines:

						'IchimokouFlatLines' + '_T_5M': True,
						'IchimokouFlatLines' + '_T_1H': True,
						'IchimokouFlatLines' + '_status': True,

						'IchimokouFlatLines_plot': True,

						#//////////////////////////


						#Config For
						'plot': True,
						}
						)