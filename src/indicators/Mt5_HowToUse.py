from Mt5_LoginGetData import LoginGetData as getdata

loging = getdata()


loging.account_name = 'mehrshadpc'
loging.initilizer()
loging.login()

# for sym in loging.get_symbols():
#  	print(sym.name)

# print(loging.get_balance())
# data = loging.getone(timeframe = '5M', number = 500, symbol = 'XAUUSD_i')
# print(data['XAUUSD_i'])

# data = loging.getall(timeframe = '1H', number = 500)
# print(data['XAUUSD_i'])

#loging.Update(symbol = 'ETHUSD_i', timeframe = '1H', number = 200)

data_5M, data_1H = loging.readall(symbol = 'XAUUSD_i', number_5M = 'all', number_1H = 'all')
print(data_1H['XAUUSD_i'])

# data_5M = loging.readone(symbol = 'XAUUSD_i', number = 500, timeframe = '5M')
# print(data_5M)