import pandas as pd
import pandas_ta as ta
from log_get_data import *

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()
# Help about this, 'ta', extension
#help(df.ta)

# List of all indicators
#df.ta.indicators()

# Help about an indicator such as bbands
#help(ta.sma)
symbol_data_5M,money,sym = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,20)
help(ta.cdl_pattern)
hammer = ta.cdl_pattern(open_=symbol_data_5M['AUDCAD_i']['open'],close=symbol_data_5M['AUDCAD_i']['close'],low=symbol_data_5M['AUDCAD_i']['low'],high=symbol_data_5M['AUDCAD_i']['high'],name="hammer",fillna=1)

print(symbol_data_5M['AUDCAD_i']['time'][(hammer == 10)])

#**************************************************** Hammer Strategy *******************************************************

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////