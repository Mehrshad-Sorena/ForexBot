from log_get_data import *
import MetaTrader5 as mt5
#from logger import logs

def carrier_buy(symbol,lot,st,tp,comment,magic):

	point = mt5.symbol_info(symbol).point
	price_ask = mt5.symbol_info_tick(symbol).ask
	price = mt5.symbol_info_tick(symbol).ask
	price_bid = mt5.symbol_info_tick(symbol).bid
	spred = ((abs(price_ask-price_bid)/price_ask) * 100)
	deviation = 5

	print('==== BUY =======> ',symbol)
	print('spred: ',spred)

	if (spred > 0.045): 
		print('spred return: ',spred)
		return

	tp = tp - abs(price_ask-price_bid)
	#st = st - abs(price_ask-price_bid)

	if (tp <= (price)): 
		print('tp return: ',price)
		print('tp: ',tp)
		return

	if (st >= price_bid): 
		print('st return: ',price_bid)
		print('st: ',st)
		return

	print(symbol,': ','buy')
	request = {
		"action": mt5.TRADE_ACTION_DEAL,
    	"symbol": symbol,
    	"volume": lot,
    	"type": mt5.ORDER_TYPE_BUY,
    	"price": price,
    	"sl": st,
    	"tp": tp,
    	"deviation": deviation,
    	"magic": magic,
    	"comment": comment,
    	"type_time": mt5.ORDER_TIME_GTC,
    	"type_filling": mt5.ORDER_FILLING_FOK
   		 }

	result = mt5.order_send(request)
	# check the execution result
	print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));

	try:
		if result.retcode != mt5.TRADE_RETCODE_DONE:
			print("2. order_send failed, retcode={}".format(result.retcode))
			# request the result as a dictionary and display it element by element
			result_dict=result._asdict()
			for field in result_dict.keys():
				print("field   {}={}".format(field,result_dict[field]))
        		# if this is a trading request structure, display it element by element as well
				if field=="request":
					traderequest_dict=result_dict[field]._asdict()
					for tradereq_filed in traderequest_dict:
						print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
				else:
					print('send Done ',comment)
	except:
		print('some thing wrong send ',comment)

	return

def carrier_sell(symbol,lot,st,tp,comment,magic):

	price_ask = mt5.symbol_info_tick(symbol).ask
	price = mt5.symbol_info_tick(symbol).bid
	price_bid = mt5.symbol_info_tick(symbol).bid
	spred = ((abs(price_ask-price_bid)/price_ask) * 100)
	deviation = 5

	print('==== SELL =======> ',symbol)
	print('spred: ',spred)
	

	if (spred > 0.045): 
		print('spred return: ',spred)
		return

	tp = tp + abs(price_ask-price_bid)
	st = st + abs(price_ask-price_bid)

	if (st <= price_ask): 
		print('st return: ',price_ask)
		print('st: ',st)
		return

	if (tp >= (price_bid)): 
		print('tp return: ',price_bid)
		print('tp: ',tp)
		return

	print('================================')

	print(symbol,': ','sell')
	request = {
		"action": mt5.TRADE_ACTION_DEAL,
    	"symbol": symbol,
    	"volume": lot,
    	"type": mt5.ORDER_TYPE_SELL,
    	"price": price,
    	"sl": st,
    	"tp": tp,
    	"deviation": deviation,
    	"magic": magic,
    	"comment": comment,
    	"type_time": mt5.ORDER_TIME_GTC,
    	"type_filling": mt5.ORDER_FILLING_FOK
    	}

	result = mt5.order_send(request)
	# check the execution result
	print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));

	try:
		if result.retcode != mt5.TRADE_RETCODE_DONE:
			print("2. order_send failed, retcode={}".format(result.retcode))
			# request the result as a dictionary and display it element by element
			result_dict=result._asdict()
			for field in result_dict.keys():
				print("   {}={}".format(field,result_dict[field]))
        	# if this is a trading request structure, display it element by element as well
				if field=="request":
					traderequest_dict=result_dict[field]._asdict()
					for tradereq_filed in traderequest_dict:
						print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
				else:
					print('send Done ',comment)
	except:
		print('some thing wrong send ',comment)

	return

