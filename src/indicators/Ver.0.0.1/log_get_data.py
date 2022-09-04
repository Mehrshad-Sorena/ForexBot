from datetime import datetime
try:
	from MetaTrader5 import *
	import MetaTrader5 as mt5
except Exception as ex:
	print('login get data : ',ex)

import pandas as pd
import numpy as np

syms = np.array(
	[
		'WSt30_m_i','SPX500_m_i','NQ100_m_i','GER40_m_i',
		'GER40_i','WTI_i','BRN_i','STOXX50_i','NQ100_i',
		'EURDKK_i','DAX30_i','XRPUSD_i','XBNUSD_i',
		'LTCUSD_i','ETHUSD_i','BTCUSD_i','XAUUSD_i'
	]
	)

def log_get_data(frame,number):
	#if not mt5.initialize(login=2671410, server="MofidSecurities-Server",password="gfx7zzqe"):
	#	print("initialize() failed, error code =",mt5.last_error())
	#	quit()
#ind.indicators()

# display data on the MetaTrader 5 package
	#print("MetaTrader5 package author: ",mt5.__author__)
	#print("MetaTrader5 package version: ",mt5.__version__)
 
# establish MetaTrader 5 connection to a specified trading account

	

#if not mt5.initialize(login=50746123, server="Alpari-MT5-Demo",password="yufcye2k"):
#    print("initialize() failed, error code =",mt5.last_error())
#    quit()

	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()

#demo:
#50819811
#ni1vhvve

#real:
#17070454
#0J4BA1BI6

#demo:
#50823100
#cws5bwbe

#demo:
#50825064
#v2hmkibt

#demo:
#50825103
#8tfarxvn

#demo:
#50825951
#3zsvqxje
	authorized=mt5.login(51149098, password="zyowt2zj")
	if True:#authorized:
		account_info=mt5.account_info()
		if account_info!=None:
			account_info_dict = mt5.account_info()._asdict()


        	# display trading account data 'as is'
        #print(account_info)
        # display trading account data in the form of a dictionary
        #print("Show account_info()._asdict():")
        	#print("  {}={}".format("balance", account_info_dict["balance"]))
        	#print()
 
        # convert the dictionary into DataFrame and print
        #symbol_data['EURUSD']=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
        #print("account_info() as dataframe:")
        #print(symbol_data['EURUSD'])


	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
 

# display data on connection status, server name and trading account
#print('info = \n',mt5.terminal_info(),'\n')
# display data on MetaTrader 5 version
#print('version = \n',mt5.version(),'\n')

	symbols=mt5.symbols_get()
	#print('Symbols: ', len(symbols))
	count=0
# display the first five ones
#for s in symbols:
#    count+=1
#    print("{}. {}".format(count,s.name))
#    if count==len(symbols): break
#print()

#d = pd.DataFrame()
	symbol_data = {}

	try:
		for i in symbols:
			try:
				rates = mt5.copy_rates_from_pos(i.name, frame, 0, number)
			# display each element of obtained data in a new line
			#print("Display obtained data 'as is'",i.name)
			# create DataFrame out of the obtained data
				rates_frame = pd.DataFrame(rates)
			# convert time in seconds into the datetime format
				rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
				symbol_data[i.name] = {
				i.name: i.name,
				'open': rates_frame['open'],
				'close': rates_frame['close'],
				'low': rates_frame['low'],
				'high': rates_frame['high'],
				'HL/2': ((rates_frame['high']+rates_frame['low'])/2),
				'HLC/3': ((rates_frame['high']+rates_frame['low']+rates_frame['close'])/3),
				'HLCC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['close'])/4),
				'OHLC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['open'])/4),
				'volume': rates_frame['tick_volume'],
				'time': rates_frame['time']
				}
			except:
				print("some thing wrong log get data_1!!!",i.name)
	except:
		print("some thing wrong log get data_2!!!",i.name)

	mt5.shutdown()

	return symbol_data,account_info_dict["balance"],symbols

def get_symbols(frame):

	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()

	#initialize(
		#"C:/Program Files/Alpari MT5/terminal64.exe",
		#login=51014899,
		#password="q5r5S4z6j",
		#server="Alpari-MT5-Demo",
		#timeout=200000,          
		#portable=False            
		#)

	#print(mt5.version())
	#authorized=mt5.login(17221085)
	#if authorized:
	#	print("connected to account #{}".format(17221085))
	#else:
	#	print("failed to connect at account #{}, error code: {}".format(17221085, mt5.last_error()))
	
	authorized=mt5.login(51149098, password="zyowt2zj")
	#print('0:',authorized)
	if True:#authorized:
		account_info=mt5.account_info()
		#print('1:',account_info)
		if account_info!=None:
			
			account_info_dict = mt5.account_info()._asdict()
			#print('2:',account_info_dict)
	else:
		print("failed to connect to trade account 51014854 with password=rmqmyjj8, error code =",mt5.last_error())

	symbols=mt5.symbols_get()

	mt5.shutdown()

	return symbols,account_info_dict["balance"]

def log_get_data_one_by_one(frame,number,sym_name):

	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()

	authorized=mt5.login(51149098, password="zyowt2zj")
	if True:#authorized:
		account_info=mt5.account_info()
		if account_info!=None:
			account_info_dict = mt5.account_info()._asdict()
	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())

	symbols=mt5.symbols_get()
	count=0
	symbol_data = {}

	try:
		if True:
			try:
				rates = mt5.copy_rates_from_pos(sym_name, frame, 0, number)
			# display each element of obtained data in a new line
			#print("Display obtained data 'as is'",i.name)
			# create DataFrame out of the obtained data
				rates_frame = pd.DataFrame(rates)
			# convert time in seconds into the datetime format
				rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
				symbol_data[sym_name] = {
				sym_name: sym_name,
				'open': rates_frame['open'],
				'close': rates_frame['close'],
				'low': rates_frame['low'],
				'high': rates_frame['high'],
				'HL/2': ((rates_frame['high']+rates_frame['low'])/2),
				'HLC/3': ((rates_frame['high']+rates_frame['low']+rates_frame['close'])/3),
				'HLCC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['close'])/4),
				'OHLC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['open'])/4),
				'volume': rates_frame['tick_volume'],
				'time': rates_frame['time']
				}
			except:
				print("some thing wrong log get data!!!")
	except:
		print("some thing wrong log get data!!!")

	mt5.shutdown()

	return symbol_data,account_info_dict["balance"]

def log_get_data_Genetic(frame,number_start,number_end):
	#if not mt5.initialize(login=2671410, server="MofidSecurities-Server",password="gfx7zzqe"):
	#	print("initialize() failed, error code =",mt5.last_error())
	#	quit()
#ind.indicators()

# display data on the MetaTrader 5 package
	#print("MetaTrader5 package author: ",mt5.__author__)
	#print("MetaTrader5 package version: ",mt5.__version__)
 
# establish MetaTrader 5 connection to a specified trading account

	

#if not mt5.initialize(login=50746123, server="Alpari-MT5-Demo",password="yufcye2k"):
#    print("initialize() failed, error code =",mt5.last_error())
#    quit()

	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()

#demo:
#50819811
#ni1vhvve

#real:
#17070454
#0J4BA1BI6

#demo:
#50823100
#cws5bwbe

#demo:
#50825064
#v2hmkibt

#demo:
#50825103
#8tfarxvn

#demo:
#50825951
#3zsvqxje
	authorized=mt5.login(51149098, password="zyowt2zj")
	if True:#authorized:
		account_info=mt5.account_info()
		if account_info!=None:
			account_info_dict = mt5.account_info()._asdict()


        	# display trading account data 'as is'
        #print(account_info)
        # display trading account data in the form of a dictionary
        #print("Show account_info()._asdict():")
        	#print("  {}={}".format("balance", account_info_dict["balance"]))
        	#print()
 
        # convert the dictionary into DataFrame and print
        #symbol_data['EURUSD']=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
        #print("account_info() as dataframe:")
        #print(symbol_data['EURUSD'])


	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
 

# display data on connection status, server name and trading account
#print('info = \n',mt5.terminal_info(),'\n')
# display data on MetaTrader 5 version
#print('version = \n',mt5.version(),'\n')

	symbols=mt5.symbols_get()
	#print('Symbols: ', len(symbols))
	count=0
# display the first five ones
#for s in symbols:
#    count+=1
#    print("{}. {}".format(count,s.name))
#    if count==len(symbols): break
#print()

#d = pd.DataFrame()
	symbol_data = {}

	try:
		for i in symbols:
			try:
				rates = mt5.copy_rates_from_pos(i.name, frame, number_start, number_end)
			# display each element of obtained data in a new line
			#print("Display obtained data 'as is'",i.name)
			# create DataFrame out of the obtained data
				rates_frame = pd.DataFrame(rates)
			# convert time in seconds into the datetime format
				rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
				symbol_data[i.name] = {
				i.name: i.name,
				'open': rates_frame['open'],
				'close': rates_frame['close'],
				'low': rates_frame['low'],
				'high': rates_frame['high'],
				'HL/2': ((rates_frame['high']+rates_frame['low'])/2),
				'HLC/3': ((rates_frame['high']+rates_frame['low']+rates_frame['close'])/3),
				'HLCC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['close'])/4),
				'OHLC/4': ((rates_frame['high']+rates_frame['low']+rates_frame['close']+rates_frame['open'])/4),
				'volume': rates_frame['tick_volume'],
				'time': rates_frame['time']
				}
			except:
				print("some thing wrong log get data genetic!!!")
	except:
		print("some thing wrong log get data genetic!!!")

	mt5.shutdown()

	return symbol_data,account_info_dict["balance"],symbols


def write_dataset_csv():
	symbol_data_5M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,99888)
	symbol_data_15M,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_M15,0,33296)
	symbol_data_1H,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,8324)
	symbol_data_4H,money,symbol = log_get_data_Genetic(mt5.TIMEFRAME_H4,0,2081)
	print('data get')

	for sym in symbol:
		dataset_path = 'dataset/5M/' + sym.name + '.csv'
		data_5M = pd.DataFrame(symbol_data_5M[sym.name])
		data_5M.to_csv(dataset_path)

	for sym in symbol:
		dataset_path = 'dataset/15M/' + sym.name + '.csv'
		data_15M = pd.DataFrame(symbol_data_15M[sym.name])
		data_15M.to_csv(dataset_path)

	for sym in symbol:
		dataset_path = 'dataset/1H/' + sym.name + '.csv'
		data_1H = pd.DataFrame(symbol_data_1H[sym.name])
		data_1H.to_csv(dataset_path)

	for sym in symbol:
		dataset_path = 'dataset/4H/' + sym.name + '.csv'
		data_4H = pd.DataFrame(symbol_data_4H[sym.name])
		data_4H.to_csv(dataset_path)

def read_dataset_csv(sym,num_5M,num_15M,num_1H,num_4H):

	dataset_path_5M = 'dataset/5M/' + sym + '.csv'
	dataset_path_15M = 'dataset/15M/' + sym + '.csv'
	dataset_path_1H = 'dataset/1H/' + sym + '.csv'
	dataset_path_4H = 'dataset/4H/' + sym + '.csv'

	try:
		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()

		authorized=mt5.login(51149098, password="zyowt2zj")
		if True:#authorized:
			account_info=mt5.account_info()
			if account_info!=None:
				account_info_dict = mt5.account_info()._asdict()
		else:
			print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
	except Exception as ex:
		print('read csv: ',ex)

	#symbols=mt5.symbols_get()
	symbols = syms
	count=0
	symbol_data_5M = {}
	symbol_data_15M = {}
	symbol_data_1H = {}
	symbol_data_4H = {}

	if True:
		for i in symbols:

			if i != sym: continue

			if True:
				rates_frame = pd.read_csv(dataset_path_5M)
				symbol_data_5M[i] = {
								i: i,
								'open': rates_frame['open'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True),
								'close': rates_frame['close'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True),
								'low': rates_frame['low'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True),
								'high': rates_frame['high'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True),
								'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True))/2),
								'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True))/3),
								'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True))/4),
								'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True))/4),
								'volume': rates_frame['volume'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True),
								'time': rates_frame['time'][(len(rates_frame['open'])-num_5M-1):-1].reset_index(drop=True)
								}

				rates_frame = pd.read_csv(dataset_path_15M)
				symbol_data_15M[i] = {
								i: i,
								'open': rates_frame['open'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True),
								'close': rates_frame['close'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True),
								'low': rates_frame['low'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True),
								'high': rates_frame['high'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True),
								'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True))/2),
								'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True))/3),
								'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True))/4),
								'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True))/4),
								'volume': rates_frame['volume'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True),
								'time': rates_frame['time'][(len(rates_frame['open'])-num_15M-1):-1].reset_index(drop=True)
								}

				rates_frame = pd.read_csv(dataset_path_1H)
				symbol_data_1H[i] = {
								i: i,
								'open': rates_frame['open'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True),
								'close': rates_frame['close'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True),
								'low': rates_frame['low'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True),
								'high': rates_frame['high'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True),
								'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True))/2),
								'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True))/3),
								'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True))/4),
								'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True))/4),
								'volume': rates_frame['volume'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True),
								'time': rates_frame['time'][(len(rates_frame['open'])-num_1H-1):-1].reset_index(drop=True)
								}


				rates_frame = pd.read_csv(dataset_path_4H)
				symbol_data_4H[i] = {
								i: i,
								'open': rates_frame['open'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True),
								'close': rates_frame['close'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True),
								'low': rates_frame['low'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True),
								'high': rates_frame['high'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True),
								'HL/2': ((rates_frame['high'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True))/2),
								'HLC/3': ((rates_frame['high'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True))/3),
								'HLCC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True))/4),
								'OHLC/4': ((rates_frame['high'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['low'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['close'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)+rates_frame['open'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True))/4),
								'volume': rates_frame['volume'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True),
								'time': rates_frame['time'][(len(rates_frame['open'])-num_4H-1):-1].reset_index(drop=True)
								}


			else:
				print("some thing wrong log get data_1!!!",i)
	else:
		print("some thing wrong log get data_2!!!",i)

	try:
		mt5.shutdown()
	except:
		pass

	time_counter = 0
	for ti in symbol_data_1H[sym]['time']:
		symbol_data_1H[sym]['time'][time_counter] = datetime.strptime(symbol_data_1H[sym]['time'][time_counter], "%Y-%m-%d %H:%M:%S")
		time_counter += 1

	time_counter = 0
	for ti in symbol_data_5M[sym]['time']:
		symbol_data_5M[sym]['time'][time_counter] = datetime.strptime(symbol_data_5M[sym]['time'][time_counter], "%Y-%m-%d %H:%M:%S")
		time_counter += 1

	return symbol_data_5M, symbol_data_15M, symbol_data_1H, symbol_data_4H, symbols
#print(log_get_data(mt5.TIMEFRAME_M5,1000))
#get_symbols(mt5.TIMEFRAME_M1)