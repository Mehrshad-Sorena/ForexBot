from zipline.api import attach_pipeline, pipeline_output, record
from zipline.pipeline import Pipeline, CustomFactor
from zipline.pipeline.factors import Returns, AverageDollarVolume
from zipline import run_algorithm
import pandas as pd

#from zipline.research import run_pipeline

#from zipline.pipeline.data.builtin import USEquityPricing
# from zipline.pipeline.data.morningstar import income_statement, operation_ratios, balance_sheet
# from quantopian.pipeline.data.psychsignal import stocktwits
# from quantopian.pipeline.factors import CustomFactor, SimpleMovingAverage, Returns
# from quantopian.pipeline.filters import QTradableStocksUS

MONTH, YEAR = 21, 252
N_LONGS = N_SHORTS = 25
VOL_SCREEN = 1000

class MeanReversion(CustomFactor):
	"""Compute ratio of latest monthly returnto 12m average,
	normalized by std dev of monthly returns"""
	inputs = [Returns(window_length=MONTH)]

	window_length = YEAR

	def compute(self, today, assets, out, monthly_returns):
		df = pd.DataFrame(monthly_returns)
		out[:] = df.iloc[-1].sub(df.mean()).div(df.std())
		
def compute_factors():
	"""Create factor pipeline incl. mean reversion,
	filtered by 30d Dollar Volume; capture factor ranks"""
	mean_reversion = MeanReversion()
	dollar_volume = AverageDollarVolume(window_length=30)
	returnPipeline(columns={'longs' : mean_reversion.bottom(N_LONGS),
	'shorts' : mean_reversion.top(N_SHORTS),
	'ranking': 
	mean_reversion.rank(ascending=False)},
	screen=dollar_volume.top(VOL_SCREEN))

def initialize(context):
	"""Setup: register pipeline, schedule rebalancing,
	andset trading params"""
	attach_pipeline(compute_factors(), 'factor_pipeline')

def before_trading_start(context, data):
	"""Run factor pipeline"""
	context.factor_data = pipeline_output('factor_pipeline')
	record(factor_data=context.factor_data.ranking)
	assets = context.factor_data.index
	record(prices=data.current(assets, 'price'))


start, end = pd.Timestamp('2015-01-01', tz='UTC'), pd.Timestamp('2018-01-01', tz='UTC')
capital_base = 1e7
performance = run_algorithm(
							start=start,
							end=end,
							initialize=initialize,
							before_trading_start=before_trading_start,
							capital_base=capital_base
							)
performance.to_pickle('single_factor.pickle')