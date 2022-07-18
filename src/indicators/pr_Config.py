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
						'TrendLines_T_1H': True,
						'TrendLines_plot': False,
						#///////////////////////////


						#Config For
						'plot': False,
						}
						)