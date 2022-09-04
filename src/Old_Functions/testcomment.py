from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
#import matplotlib.pyplot as plt
import numpy as np
from find_flat import *
from three_flat_find import *
from cross_TsKs_Buy_signal import *
from exit_signal_TsKs import *
from chiko_signal import *
from log_get_data import *
import math
from divergence import *
from cross_macd import *
import schedule
import time
import os
from datetime import date
import datetime
import pytz
import threading
import concurrent.futures
import logging
import csv
from Genetic_MACD_buysell_algo_onebyone import *
from multiprocessing import Process
import threading
from Accounts import *
from UTC_Time import *
from SMA_Signal_Cross import *

symbol_data_5M,my_money,symbols = log_get_data(mt5.TIMEFRAME_M5,10)

for sym in symbols:
	positions = mt5.positions_get(symbol=sym.name)
	#print(positions)
	if positions == None:
		print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
	elif len(positions)>0:
		for position in positions:
			#print(position)
			type_position = position[5]
			vol_position = position[9]
			comment_position = position[17]
			tp_position = position[12]
			sl_position = position[11]
			price_open_position = position[10]
			ticket_position = position[0]
			price_current_position = position[13]
			ID_position = position[18]

			profit_position = position[15]
			magic_position = position[6]

			symbol_position = position[16]
			print(symbol_position,comment_position,type_position,tp_position,sl_position,price_open_position,ticket_position,price_current_position,ID_position)
			if ((sym.name == symbol_position) & (type_position == 1) & (comment_position == '5M30M gen SMI')):
				print('same sell')
				break

			#vol_traded += vol_position