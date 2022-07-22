from macd_Parameters import Parameters
from macd_Config import Config

class MACD:

	parameters = Parameters()
	config = Config()
	def __init__(
				self,
				parameters,
				config
				):

		self.elements = dict({

							})

		self.cfg = dict({

						})





parameters = Parameters()
config = Config()

macd = MACD(parameters = parameters, config = config)
macd.divergence()