import os

my_path = "Genetic_TsKs_output_sell_onebyone/1H/"

for sym in os.listdir(my_path):
	print(sym.split('.')[0])
	print(os.path.exists(my_path+sym))
	os.rename(my_path+sym , 'rename/' + sym.split('.')[0]+'_i'+'.csv')