import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from log_get_data import *
import tarfile

symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,600)

daily = pd.DataFrame(symbol_data_5M['XAUUSD_i'])
daily.index.name = 'Time'
daily.index = symbol_data_5M['XAUUSD_i']['time']
daily.head(3)
daily.tail(3)
#plt.style.use('ggplot')

mc = mpf.make_marketcolors(
							base_mpf_style='yahoo',
							up='green',
							down='red',
							#vcedge = {'up': 'green', 'down': 'red'}, 
							vcdopcod = True,
							alpha = 0.0001
							)
mco = [mc]*len(daily)


two_points = [
				(symbol_data_5M['XAUUSD_i']['time'][0],symbol_data_5M['XAUUSD_i']['high'][0]),
				(symbol_data_5M['XAUUSD_i']['time'][100],symbol_data_5M['XAUUSD_i']['high'][100])
			]
mpf.plot(
		daily,
		type='candle',
		volume=True,
		style='yahoo',
		figscale=1,
		savefig=dict(fname='pic/tsave100.jpg',dpi=600,pad_inches=0.25),
		marketcolor_overrides=mco,
		alines=two_points
		)#.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()


