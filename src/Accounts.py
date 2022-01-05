from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
#import matplotlib.pyplot as plt
import numpy as np

def log_multi_account(num):
	accounts ={}
	accounts[1] = {
	'user': 50823100,
	'pass': 'cws5bwbe',
	'type': 'demo'
	}
	accounts[2] = {
	'user': 50825064,
	'pass':'v2hmkibt',
	'type': 'demo'
	}
	accounts[3] = {
	'user': 50825103,
	'pass':'8tfarxvn',
	'type': 'demo'
	}
	accounts[4] = {
	'user': 50825951,
	'pass':'3zsvqxje',
	'type': 'demo'
	}
	accounts[5] = {
	'user': 50826350,
	'pass':'lbea6nhe',
	'type': 'demo'
	}
	accounts[6] = {
	'user': 50827127,
	'pass':'gismp7kw',
	'type': 'demo'
	}
	
	accounts[7] = {
	'user': 17070454,
	'pass':'TautuiKashu1369',
	'type': 'demo'
	}

	accounts[1000] = {
	'user': 51029334,
	'pass':'q5r5S4z6j',
	'type': 'demo'
	}

	accounts[996] = {
	'user': 50893660,
	'pass':'5sxeyhbh',
	'type': 'demo'
	}
	
	accounts[997] = {
	'user': 50890640,
	'pass':'jkovf2hr',
	'type': 'demo'
	}
	
	accounts[998] = {
	'user': 50884146,
	'pass':'nvd7gzyk',
	'type': 'demo'
	}

	accounts[999] = {
	'user': 50875916,
	'pass':'5ovdijjh',
	'type': 'demo'
	}

	accounts[1001] = {
	'user': 50871893,
	'pass':'teuyft8y',
	'type': 'demo'
	}

	accounts[1002] = {
	'user': 50859731,
	'pass':'tp5bwcmj',
	'type': 'demo'
	}

	accounts[14] = {
	'user': 50853218,
	'pass':'awzd5kme',
	'type': 'demo'
	}

	accounts[13] = {
	'user': 50852837,
	'pass':'qnx2qrrz',
	'type': 'demo'
	}
	
	accounts[8] = {
	'user': 50827750,
	'pass':'npbl1lnd',
	'type': 'demo'
	}
	accounts[9] = {
	'user': 50829690,
	'pass':'j6twroqc',
	'type': 'demo'
	}
	accounts[10] = {
	'user': 50830365,
	'pass':'vriq7otv',
	'type': 'demo'
	}
	accounts[11] = {
	'user': 50832513,
	'pass':'oexfwjz6',
	'type': 'demo'
	}
	accounts[12] = {
	'user': 50833621,
	'pass':'jezdnq5t',
	'type': 'demo'
	}

	
	
	accounts['real'] = {
	'user': 17070454,
	'pass':'TautuiKashu1369',
	'type': 'real'
	}
	
	if not mt5.initialize():
		print("initialize() failed, error code =",mt5.last_error())
		quit()

	account_info_dict = ''
	authorized=mt5.login(accounts[num]['user'], password=accounts[num]['pass'])
	if authorized:
		account_info=mt5.account_info()
		if account_info!=None:
			account_info_dict = mt5.account_info()._asdict()
	else:
		print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())

	return account_info_dict["balance"]

#print(log_multi_account(1000))