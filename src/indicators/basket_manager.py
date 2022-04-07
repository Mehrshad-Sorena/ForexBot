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
		
		buy_path = "Genetic_cci_output_buy/" + sym.name + '.csv'
		sell_path = "Genetic_cci_output_sell/" + sym.name + '.csv'

		if os.path.exists(buy_path):
			buy_data = pd.read_csv(buy_path)
			sell_data = pd.read_csv(sell_path)

			score_list.append(buy_data['score_pr'][0])
			score_list.append(buy_data['score_min_max'][0])
			score_list.append(sell_data['score_pr'][0])
			score_list.append(sell_data['score_min_max'][0])

			return max(score_list)
#///////////////////////////////////////////////////////////////////////////////////////////////////

#************************** Lot Checker **************************************************************

def lot_checker(my_money,symbol,signal,risk_lot=0.02,levrage=100):
	buy_path = "Genetic_cci_output_buy/" + symbol + '.csv'
	sell_path = "Genetic_cci_output_sell/" + symbol + '.csv'

	lot = 0

	if signal == 'buy':
		if os.path.exists(buy_path):
			ga_buy = pd.read_csv(buy_path)

			""" Calculate Lots """
			if ga_buy['permit'][0] == True:
				if ga_buy['methode'][0] == 'pr':
					lot = (((ga_buy['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_buy['methode'][0] == 'min_max':
					lot = (((ga_buy['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	if signal == 'sell':
		if os.path.exists(sell_path):
			ga_sell = pd.read_csv(sell_path)

			""" Calculate Lots """
			if ga_sell['permit'][0] == True:
				if ga_sell['methode'][0] == 'pr':
					lot = (((ga_sell['score_pr'][0]/find_max_score())*my_money)/levrage)*risk_lot

				elif ga_sell['methode'][0] == 'min_max':
					lot = (((ga_sell['score_min_max'][0]/find_max_score())*my_money)/levrage)*risk_lot
			else:
				lot = 0

	lot = float("{:.2f}".format((lot)))

	vol_traded_max = (my_money/levrage) * risk_lot

	if (lot >= vol_traded_max):
		lot = vol_traded_max

	return lot,vol_traded_max
#//////////////////////////////////////////////////////////////////////////////////////////

#*************************************** Position Checker **********************************
def position_checker(signal,symbol):
	if signal == 'buy':
		positions = mt5.positions_get(symbol=symbol)
		if positions == None:
			print("No positions on ",symbol,", error code={}".format(mt5.last_error()))
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

	if signal == 'sell':
		
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

def basket_manager(symbols,symbol,my_money,signal):

	vol_traded = 0

	for sym in symbols:
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
