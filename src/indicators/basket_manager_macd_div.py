from log_get_data import *
import MetaTrader5 as mt5
import pandas as pd
import os

levrage_now = 100
risk_lot_now = 0.02

#******************************** Find Max Score ********************************************

def find_max_score():
	_, _, symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5, 0, 1)

	score_list = []
	for sym in symbols:
		
		buy_path_primary = 'GA/MACD/primary/buy/'+sym.name+'.csv'
		buy_path_secondry = 'GA/MACD/secondry/buy/'+sym.name+'.csv'

		sell_path_primary = 'GA/MACD/primary/sell/'+sym.name+'.csv'
		sell_path_secondry = 'GA/MACD/secondry/sell/'+sym.name+'.csv'

		if os.path.exists(buy_path_primary):
			buy_data_primary = pd.read_csv(buy_path_primary)
			score_list.append(buy_data_primary['score_pr'][0])

		if os.path.exists(buy_path_secondry):
			buy_data_secondry = pd.read_csv(buy_path_secondry)
			score_list.append(buy_data_secondry['score_pr'][0])

		if os.path.exists(sell_path_primary):
			sell_data_primary = pd.read_csv(sell_path_primary)
			score_list.append(sell_data_primary['score_pr'][0])

		if os.path.exists(sell_path_secondry):
			sell_data_secondry = pd.read_csv(sell_path_secondry)
			score_list.append(sell_data_secondry['score_pr'][0])

	#print('score_list = ',score_list)

	return max(score_list)
#///////////////////////////////////////////////////////////////////////////////////////////////////

#************************** Lot Checker **************************************************************

def lot_checker(my_money,symbol,signal,risk_lot=0.02,levrage=100):

	buy_path_primary = 'GA/MACD/primary/buy/'+symbol+'.csv'
	buy_path_secondry = 'GA/MACD/secondry/buy/'+symbol+'.csv'

	sell_path_primary = 'GA/MACD/primary/sell/'+symbol+'.csv'
	sell_path_secondry = 'GA/MACD/secondry/sell/'+symbol+'.csv'

	lot = 0

	if signal == 'buy_primary':
		if os.path.exists(buy_path_primary):
			ga_buy_primary = pd.read_csv(buy_path_primary)

			""" Calculate Lots """
			if ga_buy_primary['permit'][0] == True:
				if ga_buy_primary['methode'][0] == 'pr':
					print(ga_buy_primary['score_pr'][0])
					print('max = ',find_max_score())
					lot = (((ga_buy_primary['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_buy_primary['methode'][0] == 'min_max':
					lot = (((ga_buy_primary['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	if signal == 'buy_secondry':
		if os.path.exists(buy_path_secondry):
			ga_buy_secondry = pd.read_csv(buy_path_secondry)

			""" Calculate Lots """
			if ga_buy_secondry['permit'][0] == True:
				if ga_buy_secondry['methode'][0] == 'pr':
					lot = (((ga_buy_secondry['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_buy_secondry['methode'][0] == 'min_max':
					lot = (((ga_buy_secondry['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	if signal == 'sell_primary':
		if os.path.exists(sell_path_primary):
			ga_sell_primary = pd.read_csv(sell_path_primary)

			""" Calculate Lots """
			if ga_sell_primary['permit'][0] == True:
				if ga_sell_primary['methode'][0] == 'pr':
					lot = (((ga_sell_primary['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_sell_primary['methode'][0] == 'min_max':
					lot = (((ga_sell_primary['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	if signal == 'sell_secondry':
		if os.path.exists(sell_path_secondry):
			ga_sell_secondry = pd.read_csv(sell_path_secondry)

			""" Calculate Lots """
			if ga_sell_secondry['permit'][0] == True:
				if ga_sell_secondry['methode'][0] == 'pr':
					lot = (((ga_sell_secondry['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_sell_secondry['methode'][0] == 'min_max':
					lot = (((ga_sell_secondry['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	if 0 < lot < 0.01: lot = 0.01

	lot = float("{:.2f}".format((lot)))

	if lot > 0.09: lot = 0.09

	vol_traded_max = (my_money/levrage) * risk_lot

	if (lot >= vol_traded_max):
		lot = vol_traded_max

	lot = float("{:.2f}".format((lot)))

	return lot,vol_traded_max
#//////////////////////////////////////////////////////////////////////////////////////////

#*************************************** Position Checker **********************************
def position_checker(signal,symbol):
	if (
		signal == 'buy_primary' or
		signal == 'buy_secondry'
		):
		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()
		positions = mt5.positions_get(symbol=symbol)
		if positions == None:
			#print("No positions on ",symbol,", error code={}".format(mt5.last_error()))
			pass
		elif len(positions)>0:
			for position in positions:
				type_position = position[5]
				vol_position = position[9]
					
			print("Total positions on ",symbol,' = ',len(positions))
			if (type_position == 0):
				
				# *** Same Buy ***
				return False
			else:
				return 'buy'
		else:
			return 'buy'

	if (
		signal == 'sell_primary' or
		signal == 'sell_secondry'
		):
		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()
		positions = mt5.positions_get(symbol=symbol)
		if positions == None:
			print("No positions on ",symbol,", error code={}".format(mt5.last_error()))
		elif len(positions)>0:
			for position in positions:
				type_position = position[5]
				vol_position = position[9]
					
			print("Total positions on ",symbol,' = ',len(positions))
			if (type_position == 1):
				
				# *** Same Sell ***
				return False
			else:
				return 'sell'

		else:
			return 'sell'

#///////////////////////////////////////////////////////////////////////////////////////////////////

#********************************* Basket Manager *****************************************************

def basket_manager_macd_div(symbols,symbol,my_money,signal):

	vol_traded = 0

	for sym in symbols:
		if not mt5.initialize():
			print("initialize() failed, error code =",mt5.last_error())
			quit()
		positions = mt5.positions_get(symbol=sym.name)
		#print(positions)
		if positions == None:
			print("No positions on ",sym.name,", error code={}".format(mt5.last_error()))
		elif len(positions)>0:
			for position in positions:
				type_position = position[5]
				vol_position = position[9]

				vol_traded += vol_position

	lot,vol_traded_max = lot_checker(my_money=my_money,symbol=symbol,signal=signal,risk_lot=risk_lot_now,levrage=levrage_now)
	symbol_position = position_checker(signal=signal,symbol=symbol)

	#print(lot)
	#print(vol_traded_max)
	#print(symbol_position)
	if ((vol_traded + lot) > vol_traded_max):
		# *** No Money ***
		return False
	else:
		if symbol_position:
			return lot
		else:
			return False
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////

#********************* How to Use ****************************************************************************
#symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,5)

#print(basket_manager(symbols=symbols,symbol='AUDCAD_i',my_money=my_money,signal='sell'))
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////
