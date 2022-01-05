				#****************************** Data_Buy 5M TsKs *******************************************************************
		try:
			with open("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M_buy = line
					data_TsKs_5M_buy['tp'] = float(data_TsKs_5M_buy['tp'])
					#data_TsKs_5M_buy['tp'] = (data_TsKs_5M_buy['tp']/3)*2

					data_TsKs_5M_buy['st'] = float(data_TsKs_5M_buy['st'])
					data_TsKs_5M_buy['kijun'] = float(data_TsKs_5M_buy['kijun'])
					data_TsKs_5M_buy['tenkan'] = float(data_TsKs_5M_buy['tenkan'])
					data_TsKs_5M_buy['snkou'] = float(data_TsKs_5M_buy['snkou'])
					data_TsKs_5M_buy['score'] = float(data_TsKs_5M_buy['score'])

		except:
			#continue
			data_TsKs_5M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}

		#**************************************************////////////////////***************************************************

		#****************************** Data_Sell 5M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M_sell = line
					data_TsKs_5M_sell['tp'] = float(data_TsKs_5M_sell['tp'])
					#data_TsKs_5M_sell['tp'] = (data_TsKs_5M_sell['tp']/3)*2

					data_TsKs_5M_sell['st'] = float(data_TsKs_5M_sell['st'])
					data_TsKs_5M_sell['kijun'] = float(data_TsKs_5M_sell['kijun'])
					data_TsKs_5M_sell['tenkan'] = float(data_TsKs_5M_sell['tenkan'])
					data_TsKs_5M_sell['snkou'] = float(data_TsKs_5M_sell['snkou'])
					data_TsKs_5M_sell['score'] = float(data_TsKs_5M_sell['score'])

		except:
			#continue
			data_TsKs_5M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************
		
		#****************************** Data_Buy 30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_30M_buy = line
					data_TsKs_30M_buy['tp'] = float(data_TsKs_30M_buy['tp'])
					#data_TsKs_30M_buy['tp'] = (data_TsKs_30M_buy['tp']/3)*2

					data_TsKs_30M_buy['st'] = float(data_TsKs_30M_buy['st'])
					data_TsKs_30M_buy['kijun'] = float(data_TsKs_30M_buy['kijun'])
					data_TsKs_30M_buy['tenkan'] = float(data_TsKs_30M_buy['tenkan'])
					data_TsKs_30M_buy['snkou'] = float(data_TsKs_30M_buy['snkou'])
					data_TsKs_30M_buy['score'] = float(data_TsKs_30M_buy['score'])
		except:
			#continue
			data_TsKs_30M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************

		#****************************** Data_Sell 30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_30M_sell = line
					data_TsKs_30M_sell['tp'] = float(data_TsKs_30M_sell['tp'])
					#data_TsKs_30M_sell['tp'] = (data_TsKs_30M_sell['tp']/3)*2

					data_TsKs_30M_sell['st'] = float(data_TsKs_30M_sell['st'])
					data_TsKs_30M_sell['kijun'] = float(data_TsKs_30M_sell['kijun'])
					data_TsKs_30M_sell['tenkan'] = float(data_TsKs_30M_sell['tenkan'])
					data_TsKs_30M_sell['snkou'] = float(data_TsKs_30M_sell['snkou'])
					data_TsKs_30M_sell['score'] = float(data_TsKs_30M_sell['score'])
		except:
			#continue
			data_TsKs_30M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}



		#******************************//////////////////////***********************************************************

		#****************************** Data_Buy 1H TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_1H_buy = line
					data_TsKs_1H_buy['tp'] = float(data_TsKs_1H_buy['tp'])
					#data_TsKs_1H_buy['tp'] = (data_TsKs_1H_buy['tp']/3)*2

					data_TsKs_1H_buy['st'] = float(data_TsKs_1H_buy['st'])
					data_TsKs_1H_buy['kijun'] = float(data_TsKs_1H_buy['kijun'])
					data_TsKs_1H_buy['tenkan'] = float(data_TsKs_1H_buy['tenkan'])
					data_TsKs_1H_buy['snkou'] = float(data_TsKs_1H_buy['snkou'])
					data_TsKs_1H_buy['score'] = float(data_TsKs_1H_buy['score'])


		except:
			#continue
			data_TsKs_1H_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 1H TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_1H_sell = line
					data_TsKs_1H_sell['tp'] = float(data_TsKs_1H_sell['tp'])
					#data_TsKs_1H_sell['tp'] = (data_TsKs_1H_sell['tp']/3)*2

					data_TsKs_1H_sell['st'] = float(data_TsKs_1H_sell['st'])
					data_TsKs_1H_sell['kijun'] = float(data_TsKs_1H_sell['kijun'])
					data_TsKs_1H_sell['tenkan'] = float(data_TsKs_1H_sell['tenkan'])
					data_TsKs_1H_sell['snkou'] = float(data_TsKs_1H_sell['snkou'])
					data_TsKs_1H_sell['score'] = float(data_TsKs_1H_sell['score'])


		except:
			#continue
			data_TsKs_1H_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun': 26 , 'tenkan': 9, 'snkou': 52
			,'score': 0}


		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy 5M30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M30M_buy = line
					data_TsKs_5M30M_buy['tp'] = float(data_TsKs_5M30M_buy['tp'])
					#data_TsKs_5M30M_buy['tp'] = (data_TsKs_5M30M_buy['tp']/3)*2

					data_TsKs_5M30M_buy['st'] = float(data_TsKs_5M30M_buy['st'])
					data_TsKs_5M30M_buy['kijun5M'] = float(data_TsKs_5M30M_buy['kijun5M'])
					data_TsKs_5M30M_buy['tenkan5M'] = float(data_TsKs_5M30M_buy['tenkan5M'])
					data_TsKs_5M30M_buy['snkou5M'] = float(data_TsKs_5M30M_buy['snkou5M'])
					data_TsKs_5M30M_buy['kijun30M'] = float(data_TsKs_5M30M_buy['kijun30M'])
					data_TsKs_5M30M_buy['tenkan30M'] = float(data_TsKs_5M30M_buy['tenkan30M'])
					data_TsKs_5M30M_buy['snkou30M'] = float(data_TsKs_5M30M_buy['snkou30M'])
					data_TsKs_5M30M_buy['score'] = float(data_TsKs_5M30M_buy['score'])

					if(data_TsKs_5M30M_buy['score'] < 90):
						data_TsKs_5M30M_buy['score'] = data_TsKs_5M30M_buy['score']/10

		except:
			#continue
			data_TsKs_5M30M_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 26 , 'tenkan5M': 9, 'snkou5M': 52,'kijun30M': 26 , 'tenkan30M': 9, 'snkou30M': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell 5M30M TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_5M30M_sell = line
					data_TsKs_5M30M_sell['tp'] = float(data_TsKs_5M30M_sell['tp'])
					#data_TsKs_5M30M_sell['tp'] = (data_TsKs_5M30M_sell['tp']/3)*2

					data_TsKs_5M30M_sell['st'] = float(data_TsKs_5M30M_sell['st'])
					data_TsKs_5M30M_sell['kijun5M'] = float(data_TsKs_5M30M_sell['kijun5M'])
					data_TsKs_5M30M_sell['tenkan5M'] = float(data_TsKs_5M30M_sell['tenkan5M'])
					data_TsKs_5M30M_sell['snkou5M'] = float(data_TsKs_5M30M_sell['snkou5M'])
					data_TsKs_5M30M_sell['kijun30M'] = float(data_TsKs_5M30M_sell['kijun30M'])
					data_TsKs_5M30M_sell['tenkan30M'] = float(data_TsKs_5M30M_sell['tenkan30M'])
					data_TsKs_5M30M_sell['snkou30M'] = float(data_TsKs_5M30M_sell['snkou30M'])
					data_TsKs_5M30M_sell['score'] = float(data_TsKs_5M30M_sell['score'])

					if(data_TsKs_5M30M_sell['score'] < 90):
						data_TsKs_5M30M_sell['score'] = data_TsKs_5M30M_sell['score']/10

		except:
			#continue
			data_TsKs_5M30M_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 26 , 'tenkan5M': 9, 'snkou5M': 52,'kijun30M': 26 , 'tenkan30M': 9, 'snkou30M': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Buy porro TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_porro_buy = line
					data_TsKs_porro_buy['tp'] = float(data_TsKs_porro_buy['tp'])
					#data_TsKs_porro_buy['tp'] = (data_TsKs_porro_buy['tp']/3)*2

					data_TsKs_porro_buy['st'] = float(data_TsKs_porro_buy['st'])
					data_TsKs_porro_buy['kijun5M'] = float(data_TsKs_porro_buy['kijun5M'])
					data_TsKs_porro_buy['tenkan5M'] = float(data_TsKs_porro_buy['tenkan5M'])
					data_TsKs_porro_buy['snkou5M'] = float(data_TsKs_porro_buy['snkou5M'])
					data_TsKs_porro_buy['kijun30M'] = float(data_TsKs_porro_buy['kijun30M'])
					data_TsKs_porro_buy['tenkan30M'] = float(data_TsKs_porro_buy['tenkan30M'])
					data_TsKs_porro_buy['snkou30M'] = float(data_TsKs_porro_buy['snkou30M'])
					data_TsKs_porro_buy['kijun1H'] = float(data_TsKs_porro_buy['kijun1H'])
					data_TsKs_porro_buy['tenkan1H'] = float(data_TsKs_porro_buy['tenkan1H'])
					data_TsKs_porro_buy['snkou1H'] = float(data_TsKs_porro_buy['snkou1H'])
					data_TsKs_porro_buy['score'] = float(data_TsKs_porro_buy['score'])

					if(data_TsKs_porro_buy['score'] < 90):
						data_TsKs_porro_buy['score'] = data_TsKs_porro_buy['score']/10

		except:
			#continue
			data_TsKs_porro_buy = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 26 , 'tenkan5M': 9, 'snkou5M': 52,'kijun30M': 26 , 'tenkan30M': 9, 'snkou30M': 52,'kijun1H': 26 , 'tenkan1H': 9, 'snkou1H': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************


		#****************************** Data_Sell porro TsKs *******************************************************************

		try:
			with open("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
				for line in csv.DictReader(myfile):
					data_TsKs_porro_sell = line
					data_TsKs_porro_sell['tp'] = float(data_TsKs_porro_sell['tp'])
					#data_TsKs_porro_sell['tp'] = (data_TsKs_porro_sell['tp']/3)*2
					
					data_TsKs_porro_sell['st'] = float(data_TsKs_porro_sell['st'])
					data_TsKs_porro_sell['kijun5M'] = float(data_TsKs_porro_sell['kijun5M'])
					data_TsKs_porro_sell['tenkan5M'] = float(data_TsKs_porro_sell['tenkan5M'])
					data_TsKs_porro_sell['snkou5M'] = float(data_TsKs_porro_sell['snkou5M'])
					data_TsKs_porro_sell['kijun30M'] = float(data_TsKs_porro_sell['kijun30M'])
					data_TsKs_porro_sell['tenkan30M'] = float(data_TsKs_porro_sell['tenkan30M'])
					data_TsKs_porro_sell['snkou30M'] = float(data_TsKs_porro_sell['snkou30M'])
					data_TsKs_porro_sell['kijun1H'] = float(data_TsKs_porro_sell['kijun1H'])
					data_TsKs_porro_sell['tenkan1H'] = float(data_TsKs_porro_sell['tenkan1H'])
					data_TsKs_porro_sell['snkou1H'] = float(data_TsKs_porro_sell['snkou1H'])
					data_TsKs_porro_sell['score'] = float(data_TsKs_porro_sell['score'])

					if(data_TsKs_porro_sell['score'] < 90):
						data_TsKs_porro_sell['score'] = data_TsKs_porro_sell['score']/10

		except:
			#continue
			data_TsKs_porro_sell = {'tp' : 0.02, 'st' : 0.3,
			'kijun5M': 26 , 'tenkan5M': 9, 'snkou5M': 52,'kijun30M': 26 , 'tenkan30M': 9, 'snkou30M': 52,'kijun1H': 26 , 'tenkan1H': 9, 'snkou1H': 52
			,'score': 0}

		#******************************//////////////////////***********************************************************

		


		#***************************************** ichimokou ******************************************************************************
		try:
			# *******************++++++++++++ TSKS Buy 30M************************************************************
			ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_30M_buy['tenkan'],kijun=data_TsKs_30M_buy['kijun'],snkou=data_TsKs_30M_buy['snkou'])
			SPANA_30M_buy = ichi_30M[0][ichi_30M[0].columns[0]]
			SPANB_30M_buy = ichi_30M[0][ichi_30M[0].columns[1]]
			tenkan_30M_buy = ichi_30M[0][ichi_30M[0].columns[2]]
			kijun_30M_buy = ichi_30M[0][ichi_30M[0].columns[3]]
			chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

			TsKs_signal_cross_30M_buy = {}
			TsKs_signal_cross_30M_buy = cross_TsKs_Buy_signal(tenkan_30M_buy,kijun_30M_buy,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('30M Buy TsKs Wrong!!')

		try:

			# *******************++++++++++++ TSKS Sell 30M************************************************************

			ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=data_TsKs_30M_sell['tenkan'],kijun=data_TsKs_30M_sell['kijun'],snkou=data_TsKs_30M_sell['snkou'])
			SPANA_30M_sell = ichi_30M[0][ichi_30M[0].columns[0]]
			SPANB_30M_sell = ichi_30M[0][ichi_30M[0].columns[1]]
			tenkan_30M_sell = ichi_30M[0][ichi_30M[0].columns[2]]
			kijun_30M_sell = ichi_30M[0][ichi_30M[0].columns[3]]
			chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

			TsKs_signal_cross_30M_sell = {}
			TsKs_signal_cross_30M_sell = cross_TsKs_Buy_signal(tenkan_30M_sell,kijun_30M_sell,sym.name)

			#*********************---------------------*************/////////////*************************************************
		except:
			print('30M Sell TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************

			ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M_buy['tenkan'],kijun=data_TsKs_5M_buy['kijun'],snkou=data_TsKs_5M_buy['snkou'])
			SPANA_5M_buy = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M_buy = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M_buy = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M_buy = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			TsKs_signal_cross_5M_buy = {}
			TsKs_signal_cross_5M_buy = cross_TsKs_Buy_signal(tenkan_5M_buy,kijun_5M_buy,sym.name)


			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Sell 5M************************************************************

			ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M_sell['tenkan'],kijun=data_TsKs_5M_sell['kijun'],snkou=data_TsKs_5M_sell['snkou'])
			SPANA_5M_sell = ichi_5M[0][ichi_5M[0].columns[0]]
			SPANB_5M_sell = ichi_5M[0][ichi_5M[0].columns[1]]
			tenkan_5M_sell = ichi_5M[0][ichi_5M[0].columns[2]]
			kijun_5M_sell = ichi_5M[0][ichi_5M[0].columns[3]]
			chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

			TsKs_signal_cross_5M_sell = {}
			TsKs_signal_cross_5M_sell = cross_TsKs_Buy_signal(tenkan_5M_sell,kijun_5M_sell,sym.name)

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M Sell TsKs Wrong!!')
			

		try:
			# *******************++++++++++++ TSKS Buy 1H************************************************************

			ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_1H_buy['tenkan'],kijun=data_TsKs_1H_buy['kijun'],snkou=data_TsKs_1H_buy['snkou'])
			SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
			SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
			tenkan_1H_buy = ichi_1H[0][ichi_1H[0].columns[2]]
			kijun_1H_buy = ichi_1H[0][ichi_1H[0].columns[3]]
			chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

			TsKs_signal_cross_1H_buy = {}
			TsKs_signal_cross_1H_buy = cross_TsKs_Buy_signal(tenkan_1H_buy,kijun_1H_buy,sym.name)


			#*********************---------------------*************/////////////*************************************************

		except:
			print('1H Buy TsKs Wrong!!')



		try:
			# *******************++++++++++++ TSKS Sell 1H************************************************************

			ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=data_TsKs_1H_sell['tenkan'],kijun=data_TsKs_1H_sell['kijun'],snkou=data_TsKs_1H_sell['snkou'])
			SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
			SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
			tenkan_1H_sell = ichi_1H[0][ichi_1H[0].columns[2]]
			kijun_1H_sell = ichi_1H[0][ichi_1H[0].columns[3]]
			chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

			TsKs_signal_cross_1H_sell = {}
			TsKs_signal_cross_1H_sell = cross_TsKs_Buy_signal(tenkan_1H_sell,kijun_1H_sell,sym.name)


			#*********************---------------------*************/////////////*************************************************
			#print(macd_5M)
			#print(len(macd_5M))
		except:
			print('1H Sell TsKs Wrong!!')


		#************************************** 5M30M ichimokou ************************************************************************
		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************

			ichi_5M30M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_buy['tenkan5M'],kijun=data_TsKs_5M30M_buy['kijun5M'],snkou=data_TsKs_5M30M_buy['snkou5M'])
			SPANA_5M30M_buy = ichi_5M30M[0][ichi_5M30M[0].columns[0]]
			SPANB_5M30M_buy = ichi_5M30M[0][ichi_5M30M[0].columns[1]]
			tenkan_5M30M_buy = ichi_5M30M[0][ichi_5M30M[0].columns[2]]
			kijun_5M30M_buy = ichi_5M30M[0][ichi_5M30M[0].columns[3]]
			chikospan_5M30M = ichi_5M30M[0][ichi_5M30M[0].columns[4]]


			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M30M Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Sell 5M************************************************************

			ichi_5M30M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_5M30M_sell['tenkan5M'],kijun=data_TsKs_5M30M_sell['kijun5M'],snkou=data_TsKs_5M30M_sell['snkou5M'])
			SPANA_5M30M_sell = ichi_5M30M[0][ichi_5M30M[0].columns[0]]
			SPANB_5M30M_sell = ichi_5M30M[0][ichi_5M30M[0].columns[1]]
			tenkan_5M30M_sell = ichi_5M30M[0][ichi_5M30M[0].columns[2]]
			kijun_5M30M_sell = ichi_5M30M[0][ichi_5M30M[0].columns[3]]
			chikospan_5M30M = ichi_5M30M[0][ichi_5M30M[0].columns[4]]

			#*********************---------------------*************/////////////*************************************************

		except:
			print('5M30M Sell TsKs Wrong!!')

		#**************************************************************************************************************************************************

		#************************************** porro ichimokou ************************************************************************
		try:

			# *******************++++++++++++ TSKS Buy 5M************************************************************

			ichi_porro = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_porro_buy['tenkan5M'],kijun=data_TsKs_porro_buy['kijun5M'],snkou=data_TsKs_porro_buy['snkou5M'])
			SPANA_porro_buy = ichi_porro[0][ichi_porro[0].columns[0]]
			SPANB_porro_buy = ichi_porro[0][ichi_porro[0].columns[1]]
			tenkan_porro_buy = ichi_porro[0][ichi_porro[0].columns[2]]
			kijun_porro_buy = ichi_porro[0][ichi_porro[0].columns[3]]
			chikospan_porro = ichi_porro[0][ichi_porro[0].columns[4]]


			#*********************---------------------*************/////////////*************************************************

		except:
			print('porro Buy TsKs Wrong!!')


		try:

			# *******************++++++++++++ TSKS Sell 5M************************************************************

			ichi_porro = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=data_TsKs_porro_sell['tenkan5M'],kijun=data_TsKs_porro_sell['kijun5M'],snkou=data_TsKs_porro_sell['snkou5M'])
			SPANA_porro_sell = ichi_porro[0][ichi_porro[0].columns[0]]
			SPANB_porro_sell = ichi_porro[0][ichi_porro[0].columns[1]]
			tenkan_porro_sell = ichi_porro[0][ichi_porro[0].columns[2]]
			kijun_porro_sell = ichi_porro[0][ichi_porro[0].columns[3]]
			chikospan_porro = ichi_porro[0][ichi_porro[0].columns[4]]

			#*********************---------------------*************/////////////*************************************************

		except:
			print('porro Sell TsKs Wrong!!')

		#**************************************************************************************************************************************************