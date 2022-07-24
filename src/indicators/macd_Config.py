

class Config:

	def __init__(cls):
		
		cls.cfg = dict({

						#************** Divergence:

						'Divergence' + '_mode': 'online',
						'Divergence' + '_plot': False,
						'Divergence' + '_buy_doing': True,
						'Divergence' + '_sell_doing': True,
						'Divergence' + '_primary_doing': True,
						'Divergence' + '_secondry_doing': True,
						'Divergence' + '_name_stp_pr': True,
						'Divergence' + '_real_test': False,
						'Divergence' + '_flag_learning': False,
						'Divergence' + '_pic_save': False,

						#/////////////////////////////

						})
