from random import seed
from random import randint
from log_get_data import *
from MetaTrader5 import *
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ind
import csv
import os
from cross_TsKs_Buy_signal import *
from progress.bar import Bar


def initilize_values():
    #************************** initialize Values ******************************************************

    #ichi = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
        #tenkan=9,kijun=28,snkou=52)

        #SPANA_5M = ichi[0][ichi[0].columns[0]]
        #SPANB_5M = ichi[0][ichi[0].columns[1]]
        #tenkan_5M = ichi[0][ichi[0].columns[2]]
        #kijun_5M = ichi[0][ichi[0].columns[3]]
        #chikospan_5M = ichi[0][ichi[0].columns[4]]

        #TK_KS_signal = cross_TsKs_Buy_signal(tenkan,kijun,sym.name)

        #TK_KS_signal_exit = exit_signal_TsKs(tenkan,kijun,sym.name)

    Chromosome_5M = {}
    Chromosome_30M = {}
    Chromosome_1H = {}


    range(1)
    value = randint(50, 100)
    Chromosome_5M[0] = {
    'tp': 0,
    'tenkan': 9,
    'kijun': 26,
    'snkou': 52
    }
    Chromosome_30M[0] = {
    'tp': (randint(0,1)/100),
    'tenkan': 9,
    'kijun': 26,
    'snkou': 52
    }
    Chromosome_1H[0] = {
    'tp': (randint(0,1)/100),
    'tenkan': 9,
    'kijun': 26,
    'snkou': 52
    }
    i = 1
    while i < 8:
        Chromosome_5M[i] = {
            #'sl': '',
            #'tp': '',
            #'diff_min_max': '',
            ##'apply_to': apply_to[randint(0, 7)],
            'tp': (randint(0,1)/100),
            'tenkan': randint(3, 20),
            'kijun': randint(20, 40),
            'snkou': randint(45, 80)
        }
        Chromosome_30M[i] = {
            #'sl': '',
            #'tp': '',
            #'diff_min_max': '',
            'tp': (randint(0,1)/100),
            'tenkan': randint(3, 20),
            'kijun': randint(20, 40),
            'snkou': randint(45, 80)
        }
        Chromosome_1H[i] = {
            #'sl': '',
            #'tp': '',
            #'diff_min_max': '',
            'tp': (randint(0,1)/100),
            'tenkan': randint(3, 20),
            'kijun': randint(20, 40),
            'snkou': randint(45, 80)
        }
        res = list(Chromosome_5M[i].keys()) 
        #print(res[1])
        #print(Chromosome_5M[i][res[1]])
        i += 1

    #***********************************************************************************
    return Chromosome_5M, Chromosome_30M, Chromosome_1H

def gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H):


    Chromosome_Cutter_5M = randint(0, 3)
    Chromosome_Cutter_30M = randint(0, 3)
    Chromosome_Cutter_1H = randint(0, 3)

    Chromosome_selector_5M = randint(0, 7)
    Chromosome_selector_30M = randint(0, 7)
    Chromosome_selector_1H = randint(0, 7)

    baby_5M = {}
    baby_30M = {}
    baby_1H = {}
    #print('Generate Baby')
    chrom_creator_counter = 0
    baby_counter_5M = 0
    baby_counter_30M = 0
    baby_counter_1H = 0

    baby_counter_create = 0

    while (baby_counter_create < (len(Chromosome_30M) * 2)):
        baby_1H[baby_counter_create] = {
        #'apply_to': 0,
        'tp': 0,
        'tenkan': 0,
        'kijun': 0,
        'snkou': 0
        }
        baby_30M[baby_counter_create] = {
        #'apply_to': 0,
        'tp': 0,
        'tenkan': 0,
        'kijun': 0,
        'snkou': 0
        }
        baby_5M[baby_counter_create] = {
        #'apply_to': 0,
        'tp': 0,
        'tenkan': 0,
        'kijun': 0,
        'snkou': 0
        }

        baby_counter_create += 1
    while chrom_creator_counter < len(Chromosome_30M):

        #********************************************* 5M Baby ************************************************************
        Chromosome_selector_5M_1 = randint(0, 7)
        Chromosome_selector_5M_2 = randint(0, 7)

        res_5M_1 = list(Chromosome_5M[Chromosome_selector_5M_1].keys())
        res_5M_2 = list(Chromosome_5M[Chromosome_selector_5M_2].keys())

                

        #print(type(res_5M_1[0]))

        Chromosome_Cutter_5M = randint(0, 3)
        change_chrom_counter = 0
                    
        #print('counter',chrom_creator_counter)

        while change_chrom_counter < Chromosome_Cutter_5M:
                        #print(change_chrom_counter)
            baby_5M[baby_counter_5M].update({res_5M_1[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_1][res_5M_1[change_chrom_counter]]})
            baby_5M[baby_counter_5M + 1].update({res_5M_2[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_2][res_5M_2[change_chrom_counter]]})

            change_chrom_counter += 1

        change_chrom_counter = Chromosome_Cutter_5M

        while change_chrom_counter < 4:
            baby_5M[baby_counter_5M].update({res_5M_2[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_2][res_5M_2[change_chrom_counter]]})
            baby_5M[baby_counter_5M + 1].update({res_5M_1[change_chrom_counter]: Chromosome_5M[Chromosome_selector_5M_1][res_5M_1[change_chrom_counter]]})
            change_chrom_counter += 1

                    #print(Chromosome_5M)
                    #print('baby = ',baby_5M)


        baby_counter_5M = baby_counter_5M + 2

                    #********************************************///////***************************************************************************

                    #****************************************** 30M Baby **************************************************************************
        Chromosome_selector_30M_1 = randint(0, 7)
        Chromosome_selector_30M_2 = randint(0, 7)

        res_30M_1 = list(Chromosome_30M[Chromosome_selector_30M_1].keys())
        res_30M_2 = list(Chromosome_30M[Chromosome_selector_30M_2].keys())

                    #print(type(res_30M_1[0]))

        Chromosome_Cutter_30M = randint(0, 3)
        change_chrom_counter = 0
                    
                    #print('counter',chrom_creator_counter)

        while change_chrom_counter < Chromosome_Cutter_30M:
                        #print(change_chrom_counter)
            baby_30M[baby_counter_30M].update({res_30M_1[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_1][res_30M_1[change_chrom_counter]]})
            baby_30M[baby_counter_30M + 1].update({res_30M_2[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_2][res_30M_2[change_chrom_counter]]})

            change_chrom_counter += 1

        change_chrom_counter = Chromosome_Cutter_30M

        while change_chrom_counter < 4:
            baby_30M[baby_counter_30M].update({res_30M_2[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_2][res_30M_2[change_chrom_counter]]})
            baby_30M[baby_counter_30M + 1].update({res_30M_1[change_chrom_counter]: Chromosome_30M[Chromosome_selector_30M_1][res_30M_1[change_chrom_counter]]})
            change_chrom_counter += 1

                    
                    #print(Chromosome_30M)
                    #print('baby = ',baby_30M)
        baby_counter_30M = baby_counter_30M + 2

        #*********************************************************////****************************************************

        #********************************************************* 1H Baby ***************************************************
        Chromosome_selector_1H_1 = randint(0, 7)
        Chromosome_selector_1H_2 = randint(0, 7)

        res_1H_1 = list(Chromosome_1H[Chromosome_selector_1H_1].keys())
        res_1H_2 = list(Chromosome_1H[Chromosome_selector_1H_2].keys())

                    #print(type(res_1H_1[0]))

        Chromosome_Cutter_1H = randint(0, 3)
        change_chrom_counter = 0
                    
                    #print('counter',chrom_creator_counter)

        while change_chrom_counter < Chromosome_Cutter_1H:
                        #print(change_chrom_counter)
            baby_1H[baby_counter_1H].update({res_1H_1[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_1][res_1H_1[change_chrom_counter]]})
            baby_1H[baby_counter_1H + 1].update({res_1H_2[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_2][res_1H_2[change_chrom_counter]]})

            change_chrom_counter += 1

        change_chrom_counter = Chromosome_Cutter_1H

        while change_chrom_counter < 4:
            baby_1H[baby_counter_1H].update({res_1H_2[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_2][res_1H_2[change_chrom_counter]]})
            baby_1H[baby_counter_1H + 1].update({res_1H_1[change_chrom_counter]: Chromosome_1H[Chromosome_selector_1H_1][res_1H_1[change_chrom_counter]]})
            change_chrom_counter += 1

                    #print(Chromosome_1H)
                    #print('baby = ',baby_1H)
                    

        baby_counter_1H = baby_counter_1H + 2

    #************************************************///////*************************************************************************



        chrom_creator_counter += 1

    i = 0
    limit_counter = len(Chromosome_5M) * 2 
    while i < (limit_counter):
        Chromosome_5M[i] = {
        #'sl': '',
        #'tp': '',
        #'diff_min_max': '',
        #'apply_to': apply_to[randint(0, 7)],
        'tp': (randint(0,1)/100),
        'tenkan': randint(3, 20),
        'kijun': randint(20, 40),
        'snkou': randint(45, 80)
        }
        Chromosome_30M[i] = {
        #'sl': '',
        #'tp': '',
        #'diff_min_max': '',
        #'apply_to': apply_to[randint(0, 7)],
        'tp': (randint(0,1)/100),
        'tenkan': randint(3, 20),
        'kijun': randint(20, 40),
        'snkou': randint(45, 80)
        }
        Chromosome_1H[i] = {
        #'sl': '',
        #'tp': '',
        #'diff_min_max': '',
        #'apply_to': apply_to[randint(0, 7)],
        'tp': (randint(0,1)/100),
        'tenkan': randint(3, 20),
        'kijun': randint(20, 40),
        'snkou': randint(45, 80)
        }
        i += 1

    re_counter = 0
    while (re_counter < limit_counter):
        Chromosome_5M[re_counter]['tp'] = baby_5M[re_counter]['tp']
        Chromosome_5M[re_counter]['tenkan'] = baby_5M[re_counter]['tenkan']
        Chromosome_5M[re_counter]['kijun'] = baby_5M[re_counter]['kijun']
        Chromosome_5M[re_counter]['snkou'] = baby_5M[re_counter]['snkou']
        re_counter += 1
        #print(Chromosome_5M[6])

    re_counter = 0
    while (re_counter < limit_counter):
        Chromosome_30M[re_counter]['tp'] = baby_30M[re_counter]['tp']
        Chromosome_30M[re_counter]['tenkan'] = baby_30M[re_counter]['tenkan']
        Chromosome_30M[re_counter]['kijun'] = baby_30M[re_counter]['kijun']
        Chromosome_30M[re_counter]['snkou'] = baby_30M[re_counter]['snkou']
        re_counter += 1


    re_counter = 0
    while (re_counter < limit_counter):
        Chromosome_1H[re_counter]['tp'] = baby_1H[re_counter]['tp']
        Chromosome_1H[re_counter]['tenkan'] = baby_1H[re_counter]['tenkan']
        Chromosome_1H[re_counter]['kijun'] = baby_1H[re_counter]['kijun']
        Chromosome_1H[re_counter]['snkou'] = baby_1H[re_counter]['snkou']
        re_counter += 1

    return Chromosome_5M,Chromosome_30M,Chromosome_1H
                


#***********///////////********************************** BUY ALGO 30M *********///////////////////******************************************


#initilize_values()
def TsKs_genetic_buy_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):
    #*************************** Algorithm *************************************************//
    
    #symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    window_end = 2000
    window_start = 0
    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)

    
    sym_counter = 0

    bar = Bar('Processing 30M BUY TSKS = ', max=73)
    print('\n')

    print('**************************** START TSKS 30M BUY *********************************************')

    for sym in symbols:

        chorm_save_counter_30M = 0

        data_save_30M = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_30M[7] = line

                    Chromosome_30M[7]['kijun'] = float(Chromosome_30M[7]['kijun'])
                    Chromosome_30M[7]['tenkan'] = float(Chromosome_30M[7]['tenkan'])
                    Chromosome_30M[7]['snkou'] = float(Chromosome_30M[7]['snkou'])
            continue

        chrom_counter = 0


        chrom_faild = 0
        chrom_faild_30M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_30M):
            window_end = 2000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs 30M BUY sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY 30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_30M = 0
            tp_counter_30M = 0
            percentage_buy_tp_save_30M = {}
            percentage_buy_st_save_30M = {}
            percentage_sell_tp_save_30M = {}
            percentage_sell_st_save_30M = {}

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_buy = {}

                TK_KS_signal_30M_buy = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_30M_buy['signal'] == 'buy')):

                    TK_KS_signal_30M_buy['index'] += 3

                    counter_i = TK_KS_signal_30M_buy['index']
                    final_index = (len(tenkan_30M)-1)

                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_30M)-1)):
                            final_index = (len(tenkan_30M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']])/symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 50): break

                    try:
                        percentage_buy_tp_save_30M[tp_counter_30M] = max(percentage_buy_tp.values())
                        percentage_buy_st_save_30M[tp_counter_30M] = max(percentage_buy_st.values())
                    except:
                        percentage_buy_tp_save_30M[tp_counter_30M] = 0
                        percentage_buy_st_save_30M[tp_counter_30M] = 0

                    if (percentage_buy_st_save_30M[tp_counter_30M] < 0): 
                        percentage_buy_st_save_30M[tp_counter_30M] = 0
                        score_30M += 0

                    if (percentage_buy_st_save_30M[tp_counter_30M] > (spred+0.02)):
                        score_30M -= 0

                    if (percentage_buy_tp_save_30M[tp_counter_30M] > (spred+tp_limit)): 
                        score_30M += 1
                        if (abs(percentage_buy_st_save_30M[tp_counter_30M]) >= abs(percentage_buy_tp_save_30M[tp_counter_30M])):
                            score_30M -= 1
                        else:
                            score_30M += 1

                    if (percentage_buy_tp_save_30M[tp_counter_30M] <= (spred+tp_limit)): 
                        score_30M -= 1
                        percentage_buy_tp_save_30M[tp_counter_30M] = -1000
                    

                    num_trade += 1


                    tp_counter_30M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_30M_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_30M = (score_30M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_30M = -10
            #print('*************************************** score_30M = ',score_30M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 30M ************************************************************************

            if (score_30M < max_score_30M):
                chrom_faild_30M += 1
                chrom_faild += 1

                Chromosome_30M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                ##print('new baby 30M')
                while (Chromosome_30M[chrom_counter]['tenkan'] >= Chromosome_30M[chrom_counter]['kijun']):
                    Chromosome_30M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(5, 120),
                        'kijun': randint(5, 120),
                        'snkou': randint(30, 260)
                        }
                    
                chrom_faild_30M = 0
                score_30M = 0

                #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_30M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_30M)
                else:
                    continue
                

            if (score_30M >= max_score_30M):
                chrom_faild_30M = 0
                try:
                    max_score_30M = score_30M

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_30M.items()}

                    percentage_buy_tp_save_30M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_30M.items()}

                    percentage_buy_st_save_30M = max(res.values())

                    if percentage_buy_tp_save_30M != 0:
                        data_save_30M[chorm_save_counter_30M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_30M[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_30M,
                        'st': percentage_buy_st_save_30M,
                        'signal': 'buy',
                        'score': score_30M,
                        'kijun': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_30M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_30M += 1

                        if (score_30M >= 195): faild_flag = num_turn + 1
                    score_30M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0


                chrom_faild_30M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************



        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_30M.values()])
            max_find_30M = {}
            min_find_30M = {}
            max_find_tp_30M = {}
            counter_find = 0
            for i in data_save_30M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_30M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_30M.values()])

            counter_find = 0
            for i in max_find_30M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_30M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_30M.values()])

            counter_find = 0
            for i in max_find_tp_30M.values():
                if abs(i['st']) == min_st:
                    min_find_30M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
            'kijun': min_find_30M[0]['kijun'] , 'tenkan': min_find_30M[0]['tenkan'], 'snkou': min_find_30M[0]['snkou']
            ,'score': min_find_30M[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 30M BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 30M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 30M *********///////////////////******************************************

def TsKs_genetic_sell_algo_30M(tp_limit,max_num_trade,num_turn,max_score_30M):


    

    #*************************** Algorithm *************************************************//
    
    #symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    window_end = 2000
    window_start = 0

    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)

    
    sym_counter = 0

    print('**************************** START TSKS 30M SELL *********************************************')

    bar = Bar('Processing 30M SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_30M = 0

        data_save_30M = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_30M[7] = line

                    Chromosome_30M[7]['kijun'] = float(Chromosome_30M[7]['kijun'])
                    Chromosome_30M[7]['tenkan'] = float(Chromosome_30M[7]['tenkan'])
                    Chromosome_30M[7]['snkou'] = float(Chromosome_30M[7]['snkou'])
            continue


        chrom_faild = 0
        chrom_faild_30M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_30M):
            window_end = 2000
            window_start = 0
            

            window_length = 10

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL 30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_30M = 0
            tp_counter_30M = 0
            percentage_buy_tp_save_30M = {}
            percentage_buy_st_save_30M = {}
            percentage_sell_tp_save_30M = {}
            percentage_sell_st_save_30M = {}

            num_trade = 0


            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_sell = {}

                TK_KS_signal_30M_sell = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_30M_sell['signal'] == 'sell')):

                    TK_KS_signal_30M_sell['index'] += 3

                    counter_i = TK_KS_signal_30M_sell['index']
                    final_index = (len(tenkan_30M)-1)
                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_30M)-1)):
                            final_index = (len(tenkan_30M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']])/symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']] - symbol_data_30M[sym.name]['high'][counter_i])/symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 50): break

                    try:
                        percentage_sell_tp_save_30M[tp_counter_30M] = min(percentage_sell_tp.values())
                        percentage_sell_st_save_30M[tp_counter_30M] = min(percentage_sell_st.values())
                    except:
                        percentage_sell_tp_save_30M[tp_counter_30M] = 0
                        percentage_sell_st_save_30M[tp_counter_30M] = 0


                    if (percentage_sell_st_save_30M[tp_counter_30M] > 0): 
                        percentage_sell_st_save_30M[tp_counter_30M] = 0
                        score_30M += 0

                    if (percentage_sell_st_save_30M[tp_counter_30M] < (-1 * (spred+0.02))): 
                        score_30M -= 0

                    if (percentage_sell_tp_save_30M[tp_counter_30M] < (-1 * (spred+tp_limit))): 
                        score_30M += 1
                        if (abs(percentage_sell_st_save_30M[tp_counter_30M]) >= abs(percentage_sell_tp_save_30M[tp_counter_30M])):
                            score_30M -= 1
                        else:
                            score_30M += 1

                    if (percentage_sell_tp_save_30M[tp_counter_30M] >= (-1 * (spred+tp_limit))): 
                        score_30M -= 1
                        percentage_sell_tp_save_30M[tp_counter_30M] = 1000


                    num_trade += 1


                    tp_counter_30M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_30M_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_30M = (score_30M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_30M = -10

            ##print('*************************************** score_30M = ',score_30M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************

            


            #************************************************* Check save recreate 30M ************************************************************************

            if (score_30M < max_score_30M):
                chrom_faild_30M += 1
                chrom_faild += 1

                Chromosome_30M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_30M > (len(Chromosome_30M)/4)):
                    ##print('new baby 30M')
                    while (Chromosome_30M[chrom_counter]['tenkan'] >= Chromosome_30M[chrom_counter]['kijun']):
                        Chromosome_30M[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_30M = 0
                    score_30M = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_30M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_30M)
                else:
                    continue

            if (score_30M >= max_score_30M):
                chrom_faild_30M = 0
                try:
                    max_score_30M = score_30M

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_30M.items()}

                    percentage_sell_tp_save_30M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_30M.items()}

                    percentage_sell_st_save_30M = max(res.values())

                    if percentage_sell_tp_save_30M != 0:
                        data_save_30M[chorm_save_counter_30M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_30M[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_30M,
                        'st': percentage_sell_st_save_30M,
                        'signal': 'sell',
                        'score': score_30M,
                        'kijun': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_30M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_30M += 1

                        if (score_30M >= 195): faild_flag = num_turn + 1
                    score_30M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1
            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0

                chrom_faild = 0
                chrom_faild_30M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_30M.values()])
            max_find_30M = {}
            min_find_30M = {}
            max_find_tp_30M = {}
            counter_find = 0
            for i in data_save_30M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_30M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_30M.values()])

            counter_find = 0
            for i in max_find_30M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_30M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_30M.values()])

            counter_find = 0
            for i in max_find_tp_30M.values():
                if abs(i['st']) == min_st:
                    min_find_30M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_30M[0]['tp'], 'st' : min_find_30M[0]['st'],
            'kijun': min_find_30M[0]['kijun'] , 'tenkan': min_find_30M[0]['tenkan'], 'snkou': min_find_30M[0]['snkou']
            ,'score': min_find_30M[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/30M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 30M SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 30M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** BUY ALGO 5M *********///////////////////******************************************

#initilize_values()
def TsKs_genetic_buy_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

    #*************************** Algorithm *************************************************//
    
    #symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

    window_end = 2000
    window_start = 0

    symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

    
    sym_counter = 0

    print('**************************** START TSKS 5M BUY *********************************************')

    bar = Bar('Processing 5M BUY TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_5M = 0

        data_save_5M = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_5M[7] = line

                    Chromosome_5M[7]['kijun'] = float(Chromosome_5M[7]['kijun'])
                    Chromosome_5M[7]['tenkan'] = float(Chromosome_5M[7]['tenkan'])
                    Chromosome_5M[7]['snkou'] = float(Chromosome_5M[7]['snkou'])
            continue


        chrom_faild = 0
        chrom_faild_5M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_5M):
            window_end = 2000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_5M = 0
            tp_counter_5M = 0
            percentage_buy_tp_save_5M = {}
            percentage_buy_st_save_5M = {}
            percentage_sell_tp_save_5M = {}
            percentage_sell_st_save_5M = {}

            num_trade = 0

            while window_counter > window_start:
                #print('////////////////////////TsKs window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 5M Chorme *********************************************************************

                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_buy = {}

                #print('tenkan = ',tenkan_5M)

                TK_KS_signal_5M_buy = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_5M_buy['signal'] == 'buy')):

                    TK_KS_signal_5M_buy['index'] += 3

                    counter_i = TK_KS_signal_5M_buy['index']
                    final_index = (len(tenkan_5M)-1)

                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_5M)-1)):
                            final_index = (len(tenkan_5M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']])/symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 300): break

                    try:
                        percentage_buy_tp_save_5M[tp_counter_5M] = max(percentage_buy_tp.values())
                        percentage_buy_st_save_5M[tp_counter_5M] = max(percentage_buy_st.values())
                    except:
                        percentage_buy_tp_save_5M[tp_counter_5M] = 0
                        percentage_buy_st_save_5M[tp_counter_5M] = 0


                    if (percentage_buy_st_save_5M[tp_counter_5M] < 0): 
                        percentage_buy_st_save_5M[tp_counter_5M] = 0
                        score_5M += 0

                    if (percentage_buy_st_save_5M[tp_counter_5M] > (spred+0.02)):
                        score_5M -= 0

                    if (percentage_buy_tp_save_5M[tp_counter_5M] > (spred+tp_limit)): 
                        score_5M += 1
                        if (abs(percentage_buy_st_save_5M[tp_counter_5M]) >= abs(percentage_buy_tp_save_5M[tp_counter_5M])):
                            score_5M -= 1
                        else:
                            score_5M += 1

                    if (percentage_buy_tp_save_5M[tp_counter_5M] <= (spred+tp_limit)): 
                        score_5M -= 1
                        percentage_buy_tp_save_5M[tp_counter_5M] = -1000


                    num_trade += 1


                    tp_counter_5M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_5M_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_5M = (score_5M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_5M = -10

            #print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_5M) + 1
                break
            #******************************************************* ////////// ********************************************************



            #************************************************* Check save recreate 5M ************************************************************************

            if (score_5M < max_score_5M):
                chrom_faild_5M += 1
                chrom_faild += 1

                Chromosome_5M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_5M > (len(Chromosome_5M)/4)):
                    ##print('new baby 5M')
                    while (Chromosome_5M[chrom_counter]['tenkan'] >= Chromosome_5M[chrom_counter]['kijun']):
                        Chromosome_5M[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_5M = 0
                    score_5M = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_5M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_5M)
                else:
                    continue

            if (score_5M >= max_score_5M):
                chrom_faild_5M = 0
                try:
                    max_score_5M = score_5M

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_5M.items()}

                    percentage_buy_tp_save_5M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_5M.items()}

                    percentage_buy_st_save_5M = max(res.values())

                    if percentage_buy_tp_save_5M != 0:
                        data_save_5M[chorm_save_counter_5M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_5M[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_5M,
                        'st': percentage_buy_st_save_5M,
                        'signal': 'buy',
                        'score': score_5M,
                        'kijun': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_5M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_5M += 1

                        if (score_5M >= 195): faild_flag = num_turn + 1
                    score_5M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_5M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0


                chrom_faild_5M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_5M.values()])
            max_find_5M = {}
            min_find_5M = {}
            max_find_tp_5M = {}
            counter_find = 0
            for i in data_save_5M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_5M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_5M.values()])

            counter_find = 0
            for i in max_find_5M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_5M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_5M.values()])

            counter_find = 0
            for i in max_find_tp_5M.values():
                if abs(i['st']) == min_st:
                    min_find_5M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
            'kijun': min_find_5M[0]['kijun'] , 'tenkan': min_find_5M[0]['tenkan'], 'snkou': min_find_5M[0]['snkou']
            ,'score': min_find_5M[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 5M BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 5M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 5M *********///////////////////******************************************

def TsKs_genetic_sell_algo_5M(tp_limit,max_num_trade,num_turn,max_score_5M):

    #*************************** Algorithm *************************************************//
    
    #symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

    window_end = 2000
    window_start = 0

    symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

    sym_counter = 0

    print('**************************** START TSKS 5M SELL *********************************************')

    bar = Bar('Processing 5M SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_5M = 0

        data_save_5M = {}

        Chromosome_5M,Chromosome_30M,Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_5M[7] = line

                    Chromosome_5M[7]['kijun'] = float(Chromosome_5M[7]['kijun'])
                    Chromosome_5M[7]['tenkan'] = float(Chromosome_5M[7]['tenkan'])
                    Chromosome_5M[7]['snkou'] = float(Chromosome_5M[7]['snkou'])
            continue

        chrom_faild = 0
        chrom_faild_5M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_5M):
            window_end = 2000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_5M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_5M = 0
            tp_counter_5M = 0
            percentage_buy_tp_save_5M = {}
            percentage_buy_st_save_5M = {}
            percentage_sell_tp_save_5M = {}
            percentage_sell_st_save_5M = {}

            num_trade = 0


            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 5M Chorme *********************************************************************
                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_sell = {}

                TK_KS_signal_5M_sell = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_5M_sell['signal'] == 'sell')):

                    TK_KS_signal_5M_sell['index'] += 3

                    counter_i = TK_KS_signal_5M_sell['index']
                    final_index = (len(tenkan_5M)-1)
                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_5M)-1)):
                            final_index = (len(tenkan_5M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']])/symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 300): break

                    try:
                        percentage_sell_tp_save_5M[tp_counter_5M] = min(percentage_sell_tp.values())
                        percentage_sell_st_save_5M[tp_counter_5M] = min(percentage_sell_st.values())
                    except:
                        percentage_sell_tp_save_5M[tp_counter_5M] = 0
                        percentage_sell_st_save_5M[tp_counter_5M] = 0

                    if (percentage_sell_st_save_5M[tp_counter_5M] > 0): 
                        percentage_sell_st_save_5M[tp_counter_5M] = 0
                        score_5M += 0

                    if (percentage_sell_st_save_5M[tp_counter_5M] < (-1 * (spred+0.02))): 
                        score_5M -= 0

                    if (percentage_sell_tp_save_5M[tp_counter_5M] < (-1 * (spred+tp_limit))): 
                        score_5M += 1
                        if (abs(percentage_sell_st_save_5M[tp_counter_5M]) >= abs(percentage_sell_tp_save_5M[tp_counter_5M])):
                            score_5M -= 1
                        else:
                            score_5M += 1

                    if (percentage_sell_tp_save_5M[tp_counter_5M] >= (-1 * (spred+tp_limit))): 
                        score_5M -= 1
                        percentage_sell_tp_save_5M[tp_counter_5M] = 1000
                    

                    num_trade += 1


                    tp_counter_5M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_5M_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_5M = (score_5M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_5M = -10

            #print('*************************************** score_5M = ',score_5M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_5M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 5M ************************************************************************

            if (score_5M < max_score_5M):
                chrom_faild_5M += 1
                chrom_faild += 1

                Chromosome_5M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_5M > (len(Chromosome_5M)/4)):
                    ##print('new baby 5M')
                    while (Chromosome_5M[chrom_counter]['tenkan'] >= Chromosome_5M[chrom_counter]['kijun']):
                        Chromosome_5M[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_5M = 0
                    score_5M = 0

                    chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_5M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_5M)
                else:
                    continue

            if (score_5M >= max_score_5M):
                chrom_faild_5M = 0
                try:
                    max_score_5M = score_5M

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_5M.items()}

                    percentage_sell_tp_save_5M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_5M.items()}

                    percentage_sell_st_save_5M = max(res.values())

                    if percentage_sell_tp_save_5M != 0:
                        data_save_5M[chorm_save_counter_5M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_5M[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_5M,
                        'st': percentage_sell_st_save_5M,
                        'signal': 'sell',
                        'score': score_5M,
                        'kijun': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_5M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_5M += 1

                        if (score_5M >= 195): faild_flag = num_turn + 1
                    score_5M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_5M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                #chrom_counter = 0

                chrom_faild = 0
                chrom_faild_5M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_5M.values()])
            max_find_5M = {}
            min_find_5M = {}
            max_find_tp_5M = {}
            counter_find = 0
            for i in data_save_5M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_5M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_5M.values()])

            counter_find = 0
            for i in max_find_5M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_5M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_5M.values()])

            counter_find = 0
            for i in max_find_tp_5M.values():
                if abs(i['st']) == min_st:
                    min_find_5M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_5M[0]['tp'], 'st' : min_find_5M[0]['st'],
            'kijun': min_find_5M[0]['kijun'] , 'tenkan': min_find_5M[0]['tenkan'], 'snkou': min_find_5M[0]['snkou']
            ,'score': min_find_5M[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/5M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 5M SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 5M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** BUY ALGO 1H *********///////////////////******************************************

#initilize_values()
def TsKs_genetic_buy_algo_1H(tp_limit,max_num_trade,num_turn,max_score_1H):
    

    #*************************** Algorithm *************************************************//
    
    #symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,10)

    window_end = 1000
    window_start = 0

    symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)

    sym_counter = 0

    print('**************************** START TSKS 1H BUY *********************************************')

    bar = Bar('Processing 1H BUY TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_1H = 0

        data_save_1H = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_1H[7] = line

                    Chromosome_1H[7]['kijun'] = float(Chromosome_1H[7]['kijun'])
                    Chromosome_1H[7]['tenkan'] = float(Chromosome_1H[7]['tenkan'])
                    Chromosome_1H[7]['snkou'] = float(Chromosome_1H[7]['snkou'])
            continue


        chrom_faild = 0
        chrom_faild_1H = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_1H):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_1H),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY 1H ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_1H = 0
            tp_counter_1H = 0
            percentage_buy_tp_save_1H = {}
            percentage_buy_st_save_1H = {}
            percentage_sell_tp_save_1H = {}
            percentage_sell_st_save_1H = {}

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 1H Chorme *********************************************************************
                ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=Chromosome_1H[chrom_counter]['tenkan'],kijun=Chromosome_1H[chrom_counter]['kijun'],snkou=Chromosome_1H[chrom_counter]['snkou'])[0:window_counter]

                SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
                SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
                tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]][0:window_counter]
                kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]][0:window_counter]
                chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

                TK_KS_signal_1H_buy = {}

                TK_KS_signal_1H_buy = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_1H_buy['signal'] == 'buy')):

                    TK_KS_signal_1H_buy['index'] += 3

                    counter_i = TK_KS_signal_1H_buy['index']
                    final_index = (len(tenkan_1H)-1)

                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_1H)-1)):
                            final_index = (len(tenkan_1H)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['high'][TK_KS_signal_1H_buy['index']])/symbol_data_1H[sym.name]['high'][TK_KS_signal_1H_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_1H[sym.name]['high'][TK_KS_signal_1H_buy['index']] - symbol_data_1H[sym.name]['low'][counter_i])/symbol_data_1H[sym.name]['high'][TK_KS_signal_1H_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 30): break

                    try:
                        percentage_buy_tp_save_1H[tp_counter_1H] = max(percentage_buy_tp.values())
                        percentage_buy_st_save_1H[tp_counter_1H] = max(percentage_buy_st.values())
                    except:
                        percentage_buy_tp_save_1H[tp_counter_1H] = 0
                        percentage_buy_st_save_1H[tp_counter_1H] = 0

                    if (percentage_buy_st_save_1H[tp_counter_1H] < 0): 
                        percentage_buy_st_save_1H[tp_counter_1H] = 0
                        score_1H += 0

                    if (percentage_buy_st_save_1H[tp_counter_1H] > (spred+0.02)):
                        score_1H -= 0

                    if (percentage_buy_tp_save_1H[tp_counter_1H] > (spred+tp_limit)): 
                        score_1H += 1
                        if (abs(percentage_buy_st_save_1H[tp_counter_1H]) >= abs(percentage_buy_tp_save_1H[tp_counter_1H])):
                            score_1H -= 1
                        else:
                            score_1H += 1

                    if (percentage_buy_tp_save_1H[tp_counter_1H] <= (spred+tp_limit)): 
                        score_1H -= 1
                        percentage_buy_tp_save_1H[tp_counter_1H] = -1000


                    num_trade += 1


                    tp_counter_1H += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_1H_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_1H = (score_1H/num_trade) * 100

            if (num_trade < max_num_trade):
                score_1H = -10

            #print('*************************************** score_1H = ',score_1H,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_1H) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 1H ************************************************************************

            if (score_1H < max_score_1H):
                chrom_faild_1H += 1
                chrom_faild += 1

                Chromosome_1H[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_1H > (len(Chromosome_1H)/4)):
                    ##print('new baby 1H')
                    while (Chromosome_1H[chrom_counter]['tenkan'] >= Chromosome_1H[chrom_counter]['kijun']):
                        Chromosome_1H[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_1H = 0
                    score_1H = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_1H)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_1H)
                else:
                    continue

            if (score_1H >= max_score_1H):
                chrom_faild_1H = 0
                try:
                    max_score_1H = score_1H

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_1H.items()}

                    percentage_buy_tp_save_1H = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_1H.items()}

                    percentage_buy_st_save_1H = max(res.values())

                    if percentage_buy_tp_save_1H != 0:
                        data_save_1H[chorm_save_counter_1H] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_1H[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_1H,
                        'st': percentage_buy_st_save_1H,
                        'signal': 'buy',
                        'score': score_1H,
                        'kijun': Chromosome_1H[chrom_counter]['kijun'],
                        'tenkan': Chromosome_1H[chrom_counter]['tenkan'],
                        'snkou': Chromosome_1H[chrom_counter]['snkou']
                        }
                        chorm_save_counter_1H += 1

                        if (score_1H >= 195): faild_flag = num_turn + 1
                    score_1H = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_1H)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0


                chrom_faild_1H = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_1H.values()])
            max_find_1H = {}
            min_find_1H = {}
            max_find_tp_1H = {}
            counter_find = 0
            for i in data_save_1H.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_1H[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_1H.values()])

            counter_find = 0
            for i in max_find_1H.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_1H[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_1H.values()])

            counter_find = 0
            for i in max_find_tp_1H.values():
                if abs(i['st']) == min_st:
                    min_find_1H[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv')

            add_row = {'tp' : min_find_1H[0]['tp'], 'st' : min_find_1H[0]['st'],
            'kijun': min_find_1H[0]['kijun'] , 'tenkan': min_find_1H[0]['tenkan'], 'snkou': min_find_1H[0]['snkou']
            ,'score': min_find_1H[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/1H/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 1H BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 1H BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 1H *********///////////////////******************************************

def TsKs_genetic_sell_algo_1H(tp_limit,max_num_trade,num_turn,max_score_1H):   

    #*************************** Algorithm *************************************************//
    
    #symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,0,10)

    window_end = 1000
    window_start = 0

    symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)

    sym_counter = 0

    print('**************************** START TSKS 1H SELL *********************************************')

    bar = Bar('Processing 1H SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_1H = 0

        data_save_1H = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_1H[7] = line

                    Chromosome_1H[7]['kijun'] = float(Chromosome_1H[7]['kijun'])
                    Chromosome_1H[7]['tenkan'] = float(Chromosome_1H[7]['tenkan'])
                    Chromosome_1H[7]['snkou'] = float(Chromosome_1H[7]['snkou'])
            continue

        chrom_faild = 0
        chrom_faild_1H = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_1H):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_1H),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL 1H ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_1H = 0
            tp_counter_1H = 0
            percentage_buy_tp_save_1H = {}
            percentage_buy_st_save_1H = {}
            percentage_sell_tp_save_1H = {}
            percentage_sell_st_save_1H = {}

            num_trade = 0


            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 1H Chorme *********************************************************************
                ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=Chromosome_1H[chrom_counter]['tenkan'],kijun=Chromosome_1H[chrom_counter]['kijun'],snkou=Chromosome_1H[chrom_counter]['snkou'])[0:window_counter]

                SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
                SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
                tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]][0:window_counter]
                kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]][0:window_counter]
                chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

                TK_KS_signal_1H_sell = {}

                TK_KS_signal_1H_sell = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_1H_sell['signal'] == 'sell')):

                    TK_KS_signal_1H_sell['index'] += 3

                    counter_i = TK_KS_signal_1H_sell['index']
                    final_index = (len(tenkan_1H)-1)
                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_1H)-1)):
                            final_index = (len(tenkan_1H)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_1H[sym.name]['close'][counter_i] - symbol_data_1H[sym.name]['low'][TK_KS_signal_1H_sell['index']])/symbol_data_1H[sym.name]['low'][TK_KS_signal_1H_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_1H[sym.name]['low'][TK_KS_signal_1H_sell['index']] - symbol_data_1H[sym.name]['high'][counter_i])/symbol_data_1H[sym.name]['low'][TK_KS_signal_1H_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 30): break

                    try:
                        percentage_sell_tp_save_1H[tp_counter_1H] = min(percentage_sell_tp.values())
                        percentage_sell_st_save_1H[tp_counter_1H] = min(percentage_sell_st.values())
                    except:
                        percentage_sell_tp_save_1H[tp_counter_1H] = 0
                        percentage_sell_st_save_1H[tp_counter_1H] = 0

                    if (percentage_sell_st_save_1H[tp_counter_1H] > 0): 
                        percentage_sell_st_save_1H[tp_counter_1H] = 0
                        score_1H += 0

                    if (percentage_sell_st_save_1H[tp_counter_1H] < (-1 * (spred+0.02))): 
                        score_1H -= 0

                    if (percentage_sell_tp_save_1H[tp_counter_1H] < (-1 * (spred+tp_limit))): 
                        score_1H += 1
                        if (abs(percentage_sell_st_save_1H[tp_counter_1H]) >= abs(percentage_sell_tp_save_1H[tp_counter_1H])):
                            score_1H -= 1
                        else:
                            score_1H += 1

                    if (percentage_sell_tp_save_1H[tp_counter_1H] >= (-1 * (spred+tp_limit))): 
                        score_1H -= 1
                        percentage_sell_tp_save_1H[tp_counter_1H] = 1000
                    

                    num_trade += 1


                    tp_counter_1H += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_1H_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_1H = (score_1H/num_trade) * 100

            if (num_trade < max_num_trade):
                score_1H = -10

            #print('*************************************** score_1H = ',score_1H,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_1H) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 1H ************************************************************************

            if (score_1H < max_score_1H):
                chrom_faild_1H += 1
                chrom_faild += 1

                Chromosome_1H[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_1H > (len(Chromosome_1H)/4)):
                    ##print('new baby 1H')
                    while (Chromosome_1H[chrom_counter]['tenkan'] >= Chromosome_1H[chrom_counter]['kijun']):
                        Chromosome_1H[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_1H = 0
                    score_1H = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_1H)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_1H)
                else:
                    continue

            if (score_1H >= max_score_1H):
                chrom_faild_1H = 0
                try:
                    max_score_1H = score_1H

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_1H.items()}

                    percentage_sell_tp_save_1H = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_1H.items()}

                    percentage_sell_st_save_1H = max(res.values())

                    if percentage_sell_tp_save_1H != 0:
                        data_save_1H[chorm_save_counter_1H] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_1H[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_1H,
                        'st': percentage_sell_st_save_1H,
                        'signal': 'sell',
                        'score': score_1H,
                        'kijun': Chromosome_1H[chrom_counter]['kijun'],
                        'tenkan': Chromosome_1H[chrom_counter]['tenkan'],
                        'snkou': Chromosome_1H[chrom_counter]['snkou']
                        }
                        chorm_save_counter_1H += 1

                        if (score_1H >= 195): faild_flag = num_turn + 1
                    score_1H = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_1H)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0

                chrom_faild = 0
                chrom_faild_1H = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_1H.values()])
            max_find_1H = {}
            min_find_1H = {}
            max_find_tp_1H = {}
            counter_find = 0
            for i in data_save_1H.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_1H[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_1H.values()])

            counter_find = 0
            for i in max_find_1H.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_1H[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_1H.values()])

            counter_find = 0
            for i in max_find_tp_1H.values():
                if abs(i['st']) == min_st:
                    min_find_1H[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv')

            add_row = {'tp' : min_find_1H[0]['tp'], 'st' : min_find_1H[0]['st'],
            'kijun': min_find_1H[0]['kijun'] , 'tenkan': min_find_1H[0]['tenkan'], 'snkou': min_find_1H[0]['snkou']
            ,'score': min_find_1H[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/1H/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 1H SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 1H SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************



#***********///////////********************************** BUY ALGO 5M30M *********///////////////////******************************************

#initilize_values()
def TsKs_genetic_buy_algo_5M30M(tp_limit,max_num_trade,num_turn,max_score_5M30M):

    #*************************** Algorithm *************************************************//
    
    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    sym_counter = 0

    print('**************************** START TSKS 5M30M BUY *********************************************')

    bar = Bar('Processing 5M30M BUY TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_5M30M = 0

        data_save_5M30M = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    data_TsKs_5M30M_buy = line

                    Chromosome_5M[7]['kijun'] = float(data_TsKs_5M30M_buy['kijun5M'])
                    Chromosome_5M[7]['tenkan'] = float(data_TsKs_5M30M_buy['tenkan5M'])
                    Chromosome_5M[7]['snkou'] = float(data_TsKs_5M30M_buy['snkou5M'])

                    Chromosome_30M[7]['kijun'] = float(data_TsKs_5M30M_buy['kijun30M'])
                    Chromosome_30M[7]['tenkan'] = float(data_TsKs_5M30M_buy['tenkan30M'])
                    Chromosome_30M[7]['snkou'] = float(data_TsKs_5M30M_buy['snkou30M'])
            continue


        chrom_faild = 0

        chrom_faild_5M30M = 0

        faild_flag = 0

        window_end = 1000
        window_start = 0

        symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
        symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

        while chrom_counter < len(Chromosome_30M):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY 5M30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end


            score_5M30M = 0
            tp_counter_5M30M = 0
            percentage_buy_tp_save_5M30M = {}
            percentage_buy_st_save_5M30M = {}
            percentage_sell_tp_save_5M30M = {}
            percentage_sell_st_save_5M30M = {}

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_buy = {}

                TK_KS_signal_30M_buy = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

                #******************************************* 5M Chorme *********************************************************************
                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_buy = {}

                TK_KS_signal_5M_buy = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

                #******************************************* 5M30M Chorme *********************************************************************

                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = abs(price_ask-price_bid)

                if ((TK_KS_signal_30M_buy['signal'] == 'buy') & (TK_KS_signal_5M_buy['signal'] == 'buy') & (TK_KS_signal_30M_buy['index'] == TK_KS_signal_5M_buy['index'])):

                    counter_i = TK_KS_signal_30M_buy['index']
                    final_index = (len(tenkan_30M)-1)

                    if (final_index - counter_i) >= 20:
                        final_index = counter_i + 20
                        if (final_index > (len(tenkan_30M)-1)):
                            final_index = (len(tenkan_30M)-1)

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']])/symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']] - symbol_data_30M[sym.name]['low'][counter_i])/symbol_data_30M[sym.name]['high'][TK_KS_signal_30M_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                    percentage_buy_tp_save_5M30M[tp_counter_5M30M] = max(percentage_buy_tp.values())
                    percentage_buy_st_save_5M30M[tp_counter_5M30M] = max(percentage_buy_st.values())

                    if (percentage_buy_st_save_5M30M[tp_counter_5M30M] < 0): 
                        percentage_buy_st_save_5M30M[tp_counter_5M30M] = 0
                        score_5M30M += 0

                    if (percentage_buy_st_save_5M30M[tp_counter_5M30M] > (spred+0.02)):
                        score_5M30M -= 0

                    if (percentage_buy_tp_save_5M30M[tp_counter_5M30M] > (spred+tp_limit)): 
                        score_5M30M += 1
                        if (abs(percentage_buy_st_save_5M30M[tp_counter_5M30M]) >= abs(percentage_buy_tp_save_5M30M[tp_counter_5M30M])):
                            score_5M30M -= 1
                        else:
                            score_5M30M += 1

                    if (percentage_buy_tp_save_5M30M[tp_counter_5M30M] <= (spred+tp_limit)): 
                        score_5M30M -= 1
                        percentage_buy_tp_save_5M30M[tp_counter_5M30M] = -1000

                    

                    num_trade += 1


                    tp_counter_5M30M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_30M_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_5M30M = (score_5M30M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_5M30M = -10

            #print('*************************************** score_5M30M = ',score_5M30M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************

            #************************************************* Check save recreate 5M30M ************************************************************************

            if (score_5M30M < max_score_5M30M):
                chrom_faild_5M30M += 1
                chrom_faild += 1
                if True:#(chrom_faild_5M30M > (len(Chromosome_30M)/4)):
                    ##print('new baby 5M30M')
                    Chromosome_5M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_30M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    chrom_faild_5M30M = 0
                    score_5M30M = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_5M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_5M)
                else:
                    continue

            if (score_5M30M >= max_score_5M30M):
                chrom_faild_5M30M = 0
                try:
                    max_score_5M30M = score_5M30M

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_5M30M.items()}

                    percentage_buy_tp_save_5M30M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_5M30M.items()}

                    percentage_buy_st_save_5M30M = max(res.values())

                    if percentage_buy_tp_save_5M30M != 0:
                        data_save_5M30M[chorm_save_counter_5M30M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_30M[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_5M30M,
                        'st': percentage_buy_st_save_5M30M,
                        'signal': 'buy',
                        'score': score_5M30M,
                        'kijun30M': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan30M': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou30M': Chromosome_30M[chrom_counter]['snkou'],
                        'kijun5M': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan5M': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou5M': Chromosome_5M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_5M30M += 1

                        if (score_5M30M >= 195): faild_flag = num_turn + 1
                    score_5M30M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0


                chrom_faild_5M30M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************
        
        try:
            max_score = max([abs(i['score']) for i in data_save_5M30M.values()])
            max_find_5M30M = {}
            min_find_5M30M = {}
            max_find_tp_5M30M = {}
            counter_find = 0
            for i in data_save_5M30M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_5M30M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_5M30M.values()])

            counter_find = 0
            for i in max_find_5M30M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_5M30M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_5M30M.values()])

            counter_find = 0
            for i in max_find_tp_5M30M.values():
                if abs(i['st']) == min_st:
                    min_find_5M30M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')


        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv')
            add_row = {'tp' : min_find_5M30M[0]['tp'], 'st' : min_find_5M30M[0]['st'],
            'kijun30M': min_find_5M30M[0]['kijun30M'] , 'tenkan30M': min_find_5M30M[0]['tenkan30M'], 'snkou30M': min_find_5M30M[0]['snkou30M'],
            'kijun5M': min_find_5M30M[0]['kijun5M'] , 'tenkan5M': min_find_5M30M[0]['tenkan5M'], 'snkou5M': min_find_5M30M[0]['snkou5M']
            ,'score': min_find_5M30M[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/5M30M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun30M','tenkan30M','snkou30M','kijun5M','tenkan5M','snkou5M','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 5M30M BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 5M30M BUY *********************************************')

        #*****************************////////////******************************************************************

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 5M30M *********///////////////////******************************************

def TsKs_genetic_sell_algo_5M30M(tp_limit,max_num_trade,num_turn,max_score_5M30M):   

    #*************************** Algorithm *************************************************//
    
    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    sym_counter = 0

    print('**************************** START TSKS 5M30M SELL *********************************************')
    bar = Bar('Processing 5M30M SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_5M30M = 0

        data_save_5M30M = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    data_TsKs_5M30M_sell = line

                    Chromosome_5M[7]['kijun'] = float(data_TsKs_5M30M_sell['kijun5M'])
                    Chromosome_5M[7]['tenkan'] = float(data_TsKs_5M30M_sell['tenkan5M'])
                    Chromosome_5M[7]['snkou'] = float(data_TsKs_5M30M_sell['snkou5M'])

                    Chromosome_30M[7]['kijun'] = float(data_TsKs_5M30M_sell['kijun30M'])
                    Chromosome_30M[7]['tenkan'] = float(data_TsKs_5M30M_sell['tenkan30M'])
                    Chromosome_30M[7]['snkou'] = float(data_TsKs_5M30M_sell['snkou30M'])
            continue


        chrom_faild = 0

        chrom_faild_5M30M = 0

        faild_flag = 0

        window_end = 1000
        window_start = 0

        symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
        symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

        while chrom_counter < len(Chromosome_30M):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL 5M30M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_5M30M = 0
            tp_counter_5M30M = 0
            percentage_buy_tp_save_5M30M = {}
            percentage_buy_st_save_5M30M = {}
            percentage_sell_tp_save_5M30M = {}
            percentage_sell_st_save_5M30M = {}

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_sell = {}

                TK_KS_signal_30M_sell = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

                #******************************************* 5M Chorme *********************************************************************
                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_sell = {}

                TK_KS_signal_5M_sell = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

                #******************************************************///////*****************************************************************************

                #******************************************* 5M30M Chorme *********************************************************************

                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = abs(price_ask-price_bid)


                if ((TK_KS_signal_30M_sell['signal'] == 'sell') & (TK_KS_signal_5M_sell['signal'] == 'sell') & (TK_KS_signal_30M_sell['index'] == TK_KS_signal_5M_sell['index'])):
                    counter_i = TK_KS_signal_30M_sell['index']
                    final_index = (len(tenkan_30M)-1)
                    if (final_index - counter_i) >= 20:
                        final_index = counter_i + 20
                        if (final_index > (len(tenkan_30M)-1)):
                            final_index = (len(tenkan_30M)-1)

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_30M[sym.name]['close'][counter_i] - symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']])/symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']] - symbol_data_30M[sym.name]['high'][counter_i])/symbol_data_30M[sym.name]['low'][TK_KS_signal_30M_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1
                    percentage_sell_tp_save_5M30M[tp_counter_5M30M] = min(percentage_sell_tp.values())
                    percentage_sell_st_save_5M30M[tp_counter_5M30M] = min(percentage_sell_st.values())

                    if (percentage_sell_st_save_5M30M[tp_counter_5M30M] > 0): 
                        percentage_sell_st_save_5M30M[tp_counter_5M30M] = 0
                        score_5M30M += 0

                    if (percentage_sell_st_save_5M30M[tp_counter_5M30M] < (-1 * (spred+0.02))): 
                        score_5M30M -= 0

                    if (percentage_sell_tp_save_5M30M[tp_counter_5M30M] < (-1 * (spred+0.04))): 
                        score_5M30M += 1
                        if (abs(percentage_sell_st_save_5M30M[tp_counter_5M30M]) >= abs(percentage_sell_tp_save_5M30M[tp_counter_5M30M])):
                            score_5M30M -= 1
                        else:
                            score_5M30M += 1

                    if (percentage_sell_tp_save_5M30M[tp_counter_5M30M] >= (-1 * (spred+0.04))): 
                        score_5M30M -= 1
                        percentage_sell_tp_save_5M30M[tp_counter_5M30M] = 1000
                    

                    num_trade += 1


                    tp_counter_5M30M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_30M_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_5M30M = (score_5M30M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_5M30M = -10

            #print('*************************************** score_5M30M = ',score_5M30M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 5M30M ************************************************************************

            if (score_5M30M < max_score_5M30M):
                chrom_faild_5M30M += 1
                chrom_faild += 1
                if True:#(chrom_faild_5M30M > (len(Chromosome_30M)/4)):
                    ##print('new baby 5M30M')
                    Chromosome_5M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_30M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    chrom_faild_5M30M = 0
                    score_5M30M = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_5M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_5M)
                else:
                    continue

            if (score_5M30M >= max_score_5M30M):
                chrom_faild_5M30M = 0
                print('5M30M save')
                try:
                    max_score_5M30M = score_5M30M

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_5M30M.items()}

                    percentage_sell_tp_save_5M30M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_5M30M.items()}

                    percentage_sell_st_save_5M30M = max(res.values())

                    if percentage_sell_tp_save_5M30M != 0:
                        data_save_5M30M[chorm_save_counter_5M30M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_30M[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_5M30M,
                        'st': percentage_sell_st_save_5M30M,
                        'signal': 'sell',
                        'score': score_5M30M,
                        'kijun30M': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan30M': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou30M': Chromosome_30M[chrom_counter]['snkou'],
                        'kijun5M': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan5M': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou5M': Chromosome_5M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_5M30M += 1

                        if (score_5M30M >= 195): faild_flag = num_turn + 1
                    score_5M30M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0

                chrom_faild = 0

                chrom_faild_5M30M = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_5M30M.values()])
            max_find_5M30M = {}
            min_find_5M30M = {}
            max_find_tp_5M30M = {}
            counter_find = 0
            for i in data_save_5M30M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_5M30M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_5M30M.values()])

            counter_find = 0
            for i in max_find_5M30M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_5M30M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_5M30M.values()])

            counter_find = 0
            for i in max_find_tp_5M30M.values():
                if abs(i['st']) == min_st:
                    min_find_5M30M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_5M30M[0]['tp'], 'st' : min_find_5M30M[0]['st'],
            'kijun30M': min_find_5M30M[0]['kijun30M'] , 'tenkan30M': min_find_5M30M[0]['tenkan30M'], 'snkou30M': min_find_5M30M[0]['snkou30M'],
            'kijun5M': min_find_5M30M[0]['kijun5M'] , 'tenkan5M': min_find_5M30M[0]['tenkan5M'], 'snkou5M': min_find_5M30M[0]['snkou5M']
            ,'score': min_find_5M30M[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/5M30M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun30M','tenkan30M','snkou30M','kijun5M','tenkan5M','snkou5M','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 5M30M SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 5M30M SELL *********************************************')
        #*****************************////////////******************************************************************


#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** BUY ALGO porro *********///////////////////******************************************

#initilize_values()
def TsKs_genetic_buy_algo_porro(tp_limit,max_num_trade,num_turn,max_score_porro):

    #*************************** Algorithm *************************************************//
    
    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    sym_counter = 0

    print('**************************** START TSKS poroo BUY *********************************************')

    bar = Bar('Processing Porro BUY TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_porro = 0

        data_save_porro = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    data_TsKs_porro_buy = line

                    Chromosome_5M[7]['kijun'] = float(data_TsKs_porro_buy['kijun5M'])
                    Chromosome_5M[7]['tenkan'] = float(data_TsKs_porro_buy['tenkan5M'])
                    Chromosome_5M[7]['snkou'] = float(data_TsKs_porro_buy['snkou5M'])

                    Chromosome_30M[7]['kijun'] = float(data_TsKs_porro_buy['kijun30M'])
                    Chromosome_30M[7]['tenkan'] = float(data_TsKs_porro_buy['tenkan30M'])
                    Chromosome_30M[7]['snkou'] = float(data_TsKs_porro_buy['snkou30M'])

                    Chromosome_1H[7]['kijun'] = float(data_TsKs_porro_buy['kijun1H'])
                    Chromosome_1H[7]['tenkan'] = float(data_TsKs_porro_buy['tenkan1H'])
                    Chromosome_1H[7]['snkou'] = float(data_TsKs_porro_buy['snkou1H'])
            continue


        chrom_faild = 0

        chrom_faild_porro = 0

        faild_flag = 0

        window_end = 1000
        window_start = 0

        symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
        symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)
        symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

        while chrom_counter < len(Chromosome_30M):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY PORRO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_porro = 0
            tp_counter_porro = 0
            percentage_buy_tp_save_porro = {}
            percentage_buy_st_save_porro = {}
            percentage_sell_tp_save_porro = {}
            percentage_sell_st_save_porro = {}

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_buy = {}

                TK_KS_signal_30M_buy = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

                #******************************************* 5M Chorme *********************************************************************
                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_buy = {}

                TK_KS_signal_5M_buy = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

                #******************************************* 1H Chorme *********************************************************************
                ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=Chromosome_1H[chrom_counter]['tenkan'],kijun=Chromosome_1H[chrom_counter]['kijun'],snkou=Chromosome_1H[chrom_counter]['snkou'])[0:window_counter]

                SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
                SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
                tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]][0:window_counter]
                kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]][0:window_counter]
                chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

                TK_KS_signal_1H_buy = {}

                TK_KS_signal_1H_buy = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

                #******************************************************///////*****************************************************************************

                #******************************************* porro Chorme *********************************************************************

                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = abs(price_ask-price_bid)

                if ((TK_KS_signal_1H_buy['signal'] == 'buy') & (TK_KS_signal_30M_buy['signal'] == 'buy') & (TK_KS_signal_5M_buy['signal'] == 'buy') & (TK_KS_signal_30M_buy['index'] <= TK_KS_signal_5M_buy['index']) & (TK_KS_signal_1H_buy['index'] <= TK_KS_signal_5M_buy['index'])):

                    counter_i = TK_KS_signal_5M_buy['index']
                    final_index = (len(tenkan_5M)-1)

                    if (final_index - counter_i) >= 20:
                        final_index = counter_i + 20
                        if (final_index > (len(tenkan_5M)-1)):
                            final_index = (len(tenkan_5M)-1)

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']])/symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']] - symbol_data_5M[sym.name]['low'][counter_i])/symbol_data_5M[sym.name]['high'][TK_KS_signal_5M_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                    percentage_buy_tp_save_porro[tp_counter_porro] = max(percentage_buy_tp.values())
                    percentage_buy_st_save_porro[tp_counter_porro] = max(percentage_buy_st.values())

                    if (percentage_buy_st_save_porro[tp_counter_porro] < 0): 
                        percentage_buy_st_save_porro[tp_counter_porro] = 0
                        score_porro += 0

                    if (percentage_buy_st_save_porro[tp_counter_porro] > (spred+0.02)):
                        score_porro -= 0

                    if (percentage_buy_tp_save_porro[tp_counter_porro] > (spred+tp_limit)): 
                        score_porro += 1
                        if (abs(percentage_buy_st_save_porro[tp_counter_porro]) >= abs(percentage_buy_tp_save_porro[tp_counter_porro])):
                            score_porro -= 1
                        else:
                            score_porro += 1

                    if (percentage_buy_tp_save_porro[tp_counter_porro] <= (spred+tp_limit)): 
                        score_porro -= 1
                        percentage_buy_tp_save_porro[tp_counter_porro] = -1000
                    

                    num_trade += 1


                    tp_counter_porro += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_5M_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_porro = (score_porro/num_trade) * 100

            if (num_trade < max_num_trade):
                score_porro = -10

            #print('*************************************** score_porro = ',score_porro,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate porro ************************************************************************

            if (score_porro < max_score_porro):
                chrom_faild_porro += 1
                chrom_faild += 1
                if True:#(chrom_faild_porro > (len(Chromosome_30M)/4)):
                    ##print('new baby porro')
                    Chromosome_5M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_30M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_1H[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    chrom_faild_porro = 0
                    score_porro = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_30M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_30M)
                else:
                    continue

            if (score_porro >= max_score_porro):
                chrom_faild_porro = 0
                try:
                    max_score_porro = score_porro

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_porro.items()}

                    percentage_buy_tp_save_porro = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_porro.items()}

                    percentage_buy_st_save_porro = max(res.values())

                    if percentage_buy_tp_save_porro != 0:
                        data_save_porro[chorm_save_counter_porro] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_5M[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_porro,
                        'st': percentage_buy_st_save_porro,
                        'signal': 'buy',
                        'score': score_porro,
                        'kijun5M': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan5M': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou5M': Chromosome_5M[chrom_counter]['snkou'],
                        'kijun30M': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan30M': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou30M': Chromosome_30M[chrom_counter]['snkou'],
                        'kijun1H': Chromosome_1H[chrom_counter]['kijun'],
                        'tenkan1H': Chromosome_1H[chrom_counter]['tenkan'],
                        'snkou1H': Chromosome_1H[chrom_counter]['snkou']
                        }
                        chorm_save_counter_porro += 1

                        if (score_porro >= 195): faild_flag = num_turn + 1
                    score_porro = 0
                except:
                    print('fault')


            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0

                chrom_faild_porro = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************
        
        try:
            max_score = max([abs(i['score']) for i in data_save_porro.values()])
            max_find_porro = {}
            min_find_porro = {}
            max_find_tp_porro = {}
            counter_find = 0
            for i in data_save_porro.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_porro[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_porro.values()])

            counter_find = 0
            for i in max_find_porro.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_porro[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_porro.values()])

            counter_find = 0
            for i in max_find_tp_porro.values():
                if abs(i['st']) == min_st:
                    min_find_porro[counter_find] = i
                    counter_find += 1       
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************
        
        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv')

            add_row = {'tp' : min_find_porro[0]['tp'], 'st' : min_find_porro[0]['st']
            ,'kijun5M': min_find_porro[0]['kijun5M'] , 'tenkan5M': min_find_porro[0]['tenkan5M'], 'snkou5M': min_find_porro[0]['snkou5M']
            ,'kijun30M': min_find_porro[0]['kijun30M'] , 'tenkan30M': min_find_porro[0]['tenkan30M'], 'snkou30M': min_find_porro[0]['snkou30M']
            ,'kijun1H': min_find_porro[0]['kijun1H'] , 'tenkan1H': min_find_porro[0]['tenkan1H'], 'snkou1H': min_find_porro[0]['snkou1H']
            ,'score': min_find_porro[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/porro/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun5M','tenkan5M','snkou5M','kijun30M','tenkan30M','snkou30M','kijun1H','tenkan1H','snkou1H','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS porro BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS poroo BUY *********************************************')
        #*****************************////////////******************************************************************

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO porro *********///////////////////******************************************

def TsKs_genetic_sell_algo_porro(tp_limit,max_num_trade,num_turn,max_score_porro):
    
    #*************************** Algorithm *************************************************//
    
    symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,0,10)

    sym_counter = 0

    print('**************************** START TSKS poroo SELL *********************************************')

    bar = Bar('Processing Porro SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_porro = 0

        data_save_porro = {}

        Chromosome_5M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    data_TsKs_porro_sell = line

                    Chromosome_5M[7]['kijun'] = float(data_TsKs_porro_sell['kijun5M'])
                    Chromosome_5M[7]['tenkan'] = float(data_TsKs_porro_sell['tenkan5M'])
                    Chromosome_5M[7]['snkou'] = float(data_TsKs_porro_sell['snkou5M'])

                    Chromosome_30M[7]['kijun'] = float(data_TsKs_porro_sell['kijun30M'])
                    Chromosome_30M[7]['tenkan'] = float(data_TsKs_porro_sell['tenkan30M'])
                    Chromosome_30M[7]['snkou'] = float(data_TsKs_porro_sell['snkou30M'])

                    Chromosome_1H[7]['kijun'] = float(data_TsKs_porro_sell['kijun1H'])
                    Chromosome_1H[7]['tenkan'] = float(data_TsKs_porro_sell['tenkan1H'])
                    Chromosome_1H[7]['snkou'] = float(data_TsKs_porro_sell['snkou1H'])
            continue

        chrom_faild = 0

        chrom_faild_porro = 0

        faild_flag = 0

        window_end = 1000
        window_start = 0

        symbol_data_30M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M30,window_start,window_end)
        symbol_data_1H,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_H1,window_start,window_end)
        symbol_data_5M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,window_start,window_end)

        while chrom_counter < len(Chromosome_30M):
            window_end = 1000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_30M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL PORRO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_porro = 0
            tp_counter_porro = 0
            percentage_sell_tp_save_porro = {}
            percentage_sell_st_save_porro = {}
            diff_minus_porro = 0
            diff_plus_porro = 0

            num_trade = 0

            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 30M Chorme *********************************************************************
                ichi_30M = ind.ichimoku(high=symbol_data_30M[sym.name]['high'],low=symbol_data_30M[sym.name]['low'],close=symbol_data_30M[sym.name]['close'],
                    tenkan=Chromosome_30M[chrom_counter]['tenkan'],kijun=Chromosome_30M[chrom_counter]['kijun'],snkou=Chromosome_30M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_30M = ichi_30M[0][ichi_30M[0].columns[0]]
                SPANB_30M = ichi_30M[0][ichi_30M[0].columns[1]]
                tenkan_30M = ichi_30M[0][ichi_30M[0].columns[2]][0:window_counter]
                kijun_30M = ichi_30M[0][ichi_30M[0].columns[3]][0:window_counter]
                chikospan_30M = ichi_30M[0][ichi_30M[0].columns[4]]

                TK_KS_signal_30M_sell = {}

                TK_KS_signal_30M_sell = cross_TsKs_Buy_signal(tenkan_30M,kijun_30M,sym.name)

                #******************************************* 5M Chorme *********************************************************************
                ichi_5M = ind.ichimoku(high=symbol_data_5M[sym.name]['high'],low=symbol_data_5M[sym.name]['low'],close=symbol_data_5M[sym.name]['close'],
                    tenkan=Chromosome_5M[chrom_counter]['tenkan'],kijun=Chromosome_5M[chrom_counter]['kijun'],snkou=Chromosome_5M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_5M = ichi_5M[0][ichi_5M[0].columns[0]]
                SPANB_5M = ichi_5M[0][ichi_5M[0].columns[1]]
                tenkan_5M = ichi_5M[0][ichi_5M[0].columns[2]][0:window_counter]
                kijun_5M = ichi_5M[0][ichi_5M[0].columns[3]][0:window_counter]
                chikospan_5M = ichi_5M[0][ichi_5M[0].columns[4]]

                TK_KS_signal_5M_sell = {}

                TK_KS_signal_5M_sell = cross_TsKs_Buy_signal(tenkan_5M,kijun_5M,sym.name)

                #******************************************* 1H Chorme *********************************************************************
                ichi_1H = ind.ichimoku(high=symbol_data_1H[sym.name]['high'],low=symbol_data_1H[sym.name]['low'],close=symbol_data_1H[sym.name]['close'],
                    tenkan=Chromosome_1H[chrom_counter]['tenkan'],kijun=Chromosome_1H[chrom_counter]['kijun'],snkou=Chromosome_1H[chrom_counter]['snkou'])[0:window_counter]

                SPANA_1H = ichi_1H[0][ichi_1H[0].columns[0]]
                SPANB_1H = ichi_1H[0][ichi_1H[0].columns[1]]
                tenkan_1H = ichi_1H[0][ichi_1H[0].columns[2]][0:window_counter]
                kijun_1H = ichi_1H[0][ichi_1H[0].columns[3]][0:window_counter]
                chikospan_1H = ichi_1H[0][ichi_1H[0].columns[4]]

                TK_KS_signal_1H_sell = {}

                TK_KS_signal_1H_sell = cross_TsKs_Buy_signal(tenkan_1H,kijun_1H,sym.name)

                #******************************************************///////*****************************************************************************

                #******************************************* porro Chorme *********************************************************************

                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = abs(price_ask-price_bid)

                if ((TK_KS_signal_1H_sell['signal'] == 'sell') & (TK_KS_signal_30M_sell['signal'] == 'sell') & (TK_KS_signal_5M_sell['signal'] == 'sell') & (TK_KS_signal_30M_sell['index'] <= TK_KS_signal_5M_sell['index']) & (TK_KS_signal_1H_sell['index'] <= TK_KS_signal_5M_sell['index'])):
                    counter_i = TK_KS_signal_5M_sell['index']
                    final_index = (len(tenkan_5M)-1)
                    if (final_index - counter_i) >= 20:
                        final_index = counter_i + 20
                        if (final_index > (len(tenkan_5M)-1)):
                            final_index = (len(tenkan_5M)-1)

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_5M[sym.name]['close'][counter_i] - symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']])/symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']] - symbol_data_5M[sym.name]['high'][counter_i])/symbol_data_5M[sym.name]['low'][TK_KS_signal_5M_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1
                    percentage_sell_tp_save_porro[tp_counter_porro] = min(percentage_sell_tp.values())
                    percentage_sell_st_save_porro[tp_counter_porro] = min(percentage_sell_st.values())

                    if (percentage_sell_st_save_porro[tp_counter_porro] > 0): 
                        percentage_sell_st_save_porro[tp_counter_porro] = 0
                        score_porro += 0

                    if (percentage_sell_st_save_porro[tp_counter_porro] < (-1 * (spred+0.02))): 
                        score_porro -= 0

                    if (percentage_sell_tp_save_porro[tp_counter_porro] < (-1 * (spred+0.04))): 
                        score_porro += 1
                        if (abs(percentage_sell_st_save_porro[tp_counter_porro]) >= abs(percentage_sell_tp_save_porro[tp_counter_porro])):
                            score_porro -= 1
                        else:
                            score_porro += 1

                    if (percentage_sell_tp_save_porro[tp_counter_porro] >= (-1 * (spred+0.04))): 
                        score_porro -= 1
                        percentage_sell_tp_save_porro[tp_counter_porro] = 1000


                    num_trade += 1


                    tp_counter_porro += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_5M_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_porro = (score_porro/num_trade) * 100

            if (num_trade < max_num_trade):
                score_porro = -10

            #print('*************************************** score_porro = ',score_porro,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_30M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate porro ************************************************************************

            if (score_porro < max_score_porro):
                chrom_faild_porro += 1
                chrom_faild += 1
                if True:#(chrom_faild_porro > (len(Chromosome_30M)/4)):
                    ##print('new baby porro')
                    Chromosome_5M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_30M[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    Chromosome_1H[chrom_counter] = {
                        #'apply_to': apply_to[randint(0, 7)],
                        'tp': (randint(0,1)/100),
                        'tenkan': randint(3, 20),
                        'kijun': randint(20, 40),
                        'snkou': randint(45, 80)
                        }
                    chrom_faild_porro = 0
                    score_porro = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_30M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_30M)
                else:
                    continue

            if (score_porro >= max_score_porro):
                chrom_faild_porro = 0
                print('porro save')
                try:
                    max_score_porro = score_porro

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_porro.items()}

                    percentage_sell_tp_save_porro = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_porro.items()}

                    percentage_sell_st_save_porro = max(res.values())

                    if percentage_sell_tp_save_porro != 0:
                        data_save_porro[chorm_save_counter_porro] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_5M[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_porro,
                        'st': percentage_sell_st_save_porro,
                        'signal': 'sell',
                        'score': score_porro,
                        'kijun5M': Chromosome_5M[chrom_counter]['kijun'],
                        'tenkan5M': Chromosome_5M[chrom_counter]['tenkan'],
                        'snkou5M': Chromosome_5M[chrom_counter]['snkou'],
                        'kijun30M': Chromosome_30M[chrom_counter]['kijun'],
                        'tenkan30M': Chromosome_30M[chrom_counter]['tenkan'],
                        'snkou30M': Chromosome_30M[chrom_counter]['snkou'],
                        'kijun1H': Chromosome_1H[chrom_counter]['kijun'],
                        'tenkan1H': Chromosome_1H[chrom_counter]['tenkan'],
                        'snkou1H': Chromosome_1H[chrom_counter]['snkou']
                        }
                        chorm_save_counter_porro += 1

                        if (score_porro >= 195): faild_flag = num_turn + 1
                    score_porro = 0
                except:
                    print('fault')


            
            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_30M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0

                chrom_faild_porro = 0

                Chromosome_5M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_5M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_porro.values()])
            max_find_porro = {}
            min_find_porro = {}
            max_find_tp_porro = {}
            counter_find = 0
            for i in data_save_porro.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_porro[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_porro.values()])

            counter_find = 0
            for i in max_find_porro.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_porro[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_porro.values()])

            counter_find = 0
            for i in max_find_tp_porro.values():
                if abs(i['st']) == min_st:
                    min_find_porro[counter_find] = i
                    counter_find += 1       
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv')

            add_row = {'tp' : min_find_porro[0]['tp'], 'st' : min_find_porro[0]['st']
            ,'kijun5M': min_find_porro[0]['kijun5M'] , 'tenkan5M': min_find_porro[0]['tenkan5M'], 'snkou5M': min_find_porro[0]['snkou5M']
            ,'kijun30M': min_find_porro[0]['kijun30M'] , 'tenkan30M': min_find_porro[0]['tenkan30M'], 'snkou30M': min_find_porro[0]['snkou30M']
            ,'kijun1H': min_find_porro[0]['kijun1H'] , 'tenkan1H': min_find_porro[0]['tenkan1H'], 'snkou1H': min_find_porro[0]['snkou1H']
            ,'score': min_find_porro[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/porro/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun5M','tenkan5M','snkou5M','kijun30M','tenkan30M','snkou30M','kijun1H','tenkan1H','snkou1H','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS porro SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS poroo SELL *********************************************')
        #*****************************////////////******************************************************************


#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** BUY ALGO 1M *********///////////////////******************************************

#initilize_values()
def TsKs_genetic_buy_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

    #*************************** Algorithm *************************************************//
    
    #symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

    window_end = 5000
    window_start = 0

    symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

    
    sym_counter = 0

    print('**************************** START TSKS 1M BUY *********************************************')

    bar = Bar('Processing 1M BUY TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_1M = 0

        data_save_1M = {}

        Chromosome_1M, Chromosome_30M, Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_buy_onebyone/1M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_buy_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_1M[7] = line

                    Chromosome_1M[7]['kijun'] = float(Chromosome_1M[7]['kijun'])
                    Chromosome_1M[7]['tenkan'] = float(Chromosome_1M[7]['tenkan'])
                    Chromosome_1M[7]['snkou'] = float(Chromosome_1M[7]['snkou'])
            continue


        chrom_faild = 0
        chrom_faild_1M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_1M):
            window_end = 5000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_1M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ BUY 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_1M = 0
            tp_counter_1M = 0
            percentage_buy_tp_save_1M = {}
            percentage_buy_st_save_1M = {}
            percentage_sell_tp_save_1M = {}
            percentage_sell_st_save_1M = {}

            num_trade = 0

            while window_counter > window_start:
                #print('////////////////////////TsKs window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 5M Chorme *********************************************************************

                ichi_1M = ind.ichimoku(high=symbol_data_1M[sym.name]['high'],low=symbol_data_1M[sym.name]['low'],close=symbol_data_1M[sym.name]['close'],
                    tenkan=Chromosome_1M[chrom_counter]['tenkan'],kijun=Chromosome_1M[chrom_counter]['kijun'],snkou=Chromosome_1M[chrom_counter]['snkou'])

                SPANA_1M = ichi_1M[0][ichi_1M[0].columns[0]]
                SPANB_1M = ichi_1M[0][ichi_1M[0].columns[1]]
                tenkan_1M = ichi_1M[0][ichi_1M[0].columns[2]][0:window_counter]
                kijun_1M = ichi_1M[0][ichi_1M[0].columns[3]][0:window_counter]
                chikospan_1M = ichi_1M[0][ichi_1M[0].columns[4]]

                TK_KS_signal_1M_buy = {}

                #print('tenkan = ',tenkan_1M)

                TK_KS_signal_1M_buy = cross_TsKs_Buy_signal(tenkan_1M,kijun_1M,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_1M_buy['signal'] == 'buy')):

                    TK_KS_signal_1M_buy['index'] += 3

                    counter_i = TK_KS_signal_1M_buy['index']
                    final_index = (len(tenkan_1M)-1)

                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_1M)-1)):
                            final_index = (len(tenkan_1M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_buy_tp = {}
                    percentage_buy_st = {}


                    while (counter_i <= final_index):
                        percentage_buy_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['high'][TK_KS_signal_1M_buy['index']])/symbol_data_1M[sym.name]['high'][TK_KS_signal_1M_buy['index']]) * 100
                        percentage_buy_st[counter_j] = ((symbol_data_1M[sym.name]['high'][TK_KS_signal_1M_buy['index']] - symbol_data_1M[sym.name]['low'][counter_i])/symbol_data_1M[sym.name]['high'][TK_KS_signal_1M_buy['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 600): break

                    try:
                        percentage_buy_tp_save_1M[tp_counter_1M] = max(percentage_buy_tp.values())
                        percentage_buy_st_save_1M[tp_counter_1M] = max(percentage_buy_st.values())
                    except:
                        percentage_buy_tp_save_1M[tp_counter_1M] = 0
                        percentage_buy_st_save_1M[tp_counter_1M] = 0

                    if (percentage_buy_st_save_1M[tp_counter_1M] < 0): 
                        percentage_buy_st_save_1M[tp_counter_1M] = 0
                        score_1M += 0

                    if (percentage_buy_st_save_1M[tp_counter_1M] > (spred+0.02)):
                        score_1M -= 0

                    if (percentage_buy_tp_save_1M[tp_counter_1M] > (spred+tp_limit)): 
                        score_1M += 1
                        if (abs(percentage_buy_st_save_1M[tp_counter_1M]) >= abs(percentage_buy_tp_save_1M[tp_counter_1M])):
                            score_1M -= 1
                        else:
                            score_1M += 1

                    if (percentage_buy_tp_save_1M[tp_counter_1M] <= (spred+tp_limit)): 
                        score_1M -= 1
                        percentage_buy_tp_save_1M[tp_counter_1M] = -1000


                    num_trade += 1


                    tp_counter_1M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_1M_buy['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_1M = (score_1M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_1M = -10

            #print('*************************************** score_1M = ',score_1M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_1M) + 1
                break
            #******************************************************* ////////// ********************************************************



            #************************************************* Check save recreate 5M ************************************************************************

            if (score_1M < max_score_1M):
                chrom_faild_1M += 1
                chrom_faild += 1

                Chromosome_1M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_1M > (len(Chromosome_1M)/4)):
                    ##print('new baby 5M')
                    while (Chromosome_1M[chrom_counter]['tenkan'] >= Chromosome_1M[chrom_counter]['kijun']):
                        Chromosome_1M[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_1M = 0
                    score_1M = 0

                    #chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_1M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_1M)
                else:
                    continue

            if (score_1M >= max_score_1M):
                chrom_faild_1M = 0
                try:
                    max_score_1M = score_1M

                    res = {key : abs(val) for key, val in percentage_buy_tp_save_1M.items()}

                    percentage_buy_tp_save_1M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_buy_st_save_1M.items()}

                    percentage_buy_st_save_1M = max(res.values())

                    if percentage_buy_tp_save_1M != 0:
                        data_save_1M[chorm_save_counter_1M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_1M[chrom_counter][#'apply_to'],
                        'tp': percentage_buy_tp_save_1M,
                        'st': percentage_buy_st_save_1M,
                        'signal': 'buy',
                        'score': score_1M,
                        'kijun': Chromosome_1M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_1M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_1M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_1M += 1

                        if (score_1M >= 195): faild_flag = num_turn + 1
                    score_1M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_1M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                chrom_counter = 0


                chrom_faild_1M = 0

                Chromosome_1M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_1M.values()])
            max_find_1M = {}
            min_find_1M = {}
            max_find_tp_1M = {}
            counter_find = 0
            for i in data_save_1M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_1M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_1M.values()])

            counter_find = 0
            for i in max_find_1M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_1M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_1M.values()])

            counter_find = 0
            for i in max_find_tp_1M.values():
                if abs(i['st']) == min_st:
                    min_find_1M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_buy_onebyone/1M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_buy_onebyone/1M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
            'kijun': min_find_1M[0]['kijun'] , 'tenkan': min_find_1M[0]['tenkan'], 'snkou': min_find_1M[0]['snkou']
            ,'score': min_find_1M[0]['score']}

            with open("Genetic_TsKs_output_buy_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 1M BUY sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 1M BUY *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#***********///////////********************************** SELL ALGO 1M *********///////////////////******************************************

def TsKs_genetic_sell_algo_1M(tp_limit,max_num_trade,num_turn,max_score_1M):

    #*************************** Algorithm *************************************************//
    
    #symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M5,0,10)

    window_end = 5000
    window_start = 0

    symbol_data_1M,my_money,symbols = log_get_data_Genetic(mt5.TIMEFRAME_M1,window_start,window_end)

    sym_counter = 0

    print('**************************** START TSKS 1M SELL *********************************************')

    bar = Bar('Processing 1M SELL TSKS = ', max=73)
    print('\n')

    for sym in symbols:

        chorm_save_counter_1M = 0

        data_save_1M = {}

        Chromosome_1M,Chromosome_30M,Chromosome_1H = initilize_values()

        chrom_counter = 0

        if os.path.exists("Genetic_TsKs_output_sell_onebyone/1M/"+sym.name+'.csv'):
            with open("Genetic_TsKs_output_sell_onebyone/1M/"+sym.name+'.csv', 'r', newline='') as myfile:
                for line in csv.DictReader(myfile):
                    Chromosome_1M[7] = line

                    Chromosome_1M[7]['kijun'] = float(Chromosome_1M[7]['kijun'])
                    Chromosome_1M[7]['tenkan'] = float(Chromosome_1M[7]['tenkan'])
                    Chromosome_1M[7]['snkou'] = float(Chromosome_1M[7]['snkou'])
            continue

        chrom_faild = 0
        chrom_faild_1M = 0

        faild_flag = 0

        

        while chrom_counter < len(Chromosome_1M):
            window_end = 5000
            window_start = 0

            window_length = 10

            

            #print('+++++++++++++++Number of babys = ',len(Chromosome_1M),'+++++++++++++++++++++++++++++')
            #print('************************TsKs sym number = ',sym_counter,' ******************************************')
            #print('+++++++++++++++++++++++++++ SELL 5M ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            window_counter = window_end

            score_1M = 0
            tp_counter_1M = 0
            percentage_buy_tp_save_1M = {}
            percentage_buy_st_save_1M = {}
            percentage_sell_tp_save_1M = {}
            percentage_sell_st_save_1M = {}

            num_trade = 0


            while window_counter > window_start:
                #print('//////////////////////// window = ',window_counter,'///////////////////////////////////////')

                #******************************************* 1M Chorme *********************************************************************
                ichi_1M = ind.ichimoku(high=symbol_data_1M[sym.name]['high'],low=symbol_data_1M[sym.name]['low'],close=symbol_data_1M[sym.name]['close'],
                    tenkan=Chromosome_1M[chrom_counter]['tenkan'],kijun=Chromosome_1M[chrom_counter]['kijun'],snkou=Chromosome_1M[chrom_counter]['snkou'])[0:window_counter]

                SPANA_1M = ichi_1M[0][ichi_1M[0].columns[0]]
                SPANB_1M = ichi_1M[0][ichi_1M[0].columns[1]]
                tenkan_1M = ichi_1M[0][ichi_1M[0].columns[2]][0:window_counter]
                kijun_1M = ichi_1M[0][ichi_1M[0].columns[3]][0:window_counter]
                chikospan_1M = ichi_1M[0][ichi_1M[0].columns[4]]

                TK_KS_signal_1M_sell = {}

                TK_KS_signal_1M_sell = cross_TsKs_Buy_signal(tenkan_1M,kijun_1M,sym.name)


                price_ask = mt5.symbol_info_tick(sym.name).ask
                price_bid = mt5.symbol_info_tick(sym.name).bid
                spred = ((abs(price_ask-price_bid)/price_ask) * 100)

                if ((TK_KS_signal_1M_sell['signal'] == 'sell')):

                    TK_KS_signal_1M_sell['index'] += 3

                    counter_i = TK_KS_signal_1M_sell['index']
                    final_index = (len(tenkan_1M)-1)
                    if (final_index - counter_i) >= 20:
                        #final_index = counter_i + 20
                        if (final_index > (len(tenkan_1M)-1)):
                            final_index = (len(tenkan_1M)-1)

                    final_index = window_end - 1

                    counter_j = 0

                    percentage_sell_tp = {}
                    percentage_sell_st = {}

                    while (counter_i <= final_index):
                        percentage_sell_tp[counter_j] = ((symbol_data_1M[sym.name]['close'][counter_i] - symbol_data_1M[sym.name]['low'][TK_KS_signal_1M_sell['index']])/symbol_data_1M[sym.name]['low'][TK_KS_signal_1M_sell['index']]) * 100
                        percentage_sell_st[counter_j] = ((symbol_data_1M[sym.name]['low'][TK_KS_signal_1M_sell['index']] - symbol_data_1M[sym.name]['high'][counter_i])/symbol_data_1M[sym.name]['low'][TK_KS_signal_1M_sell['index']]) * 100

                        counter_i += 1
                        counter_j += 1

                        if (counter_j > 600): break

                    try:
                        percentage_sell_tp_save_1M[tp_counter_1M] = min(percentage_sell_tp.values())
                        percentage_sell_st_save_1M[tp_counter_1M] = min(percentage_sell_st.values())
                    except:
                        percentage_sell_tp_save_1M[tp_counter_1M] = 0
                        percentage_sell_st_save_1M[tp_counter_1M] = 0

                    if (percentage_sell_st_save_1M[tp_counter_1M] > 0): 
                        percentage_sell_st_save_1M[tp_counter_1M] = 0
                        score_1M += 0

                    if (percentage_sell_st_save_1M[tp_counter_1M] < (-1 * (spred+0.02))): 
                        score_1M -= 0

                    if (percentage_sell_tp_save_1M[tp_counter_1M] < (-1 * (spred+tp_limit))): 
                        score_1M += 1
                        if (abs(percentage_sell_st_save_1M[tp_counter_1M]) >= abs(percentage_sell_tp_save_1M[tp_counter_1M])):
                            score_1M -= 1
                        else:
                            score_1M += 1

                    if (percentage_sell_tp_save_1M[tp_counter_1M] >= (-1 * (spred+tp_limit))): 
                        score_1M -= 1
                        percentage_sell_tp_save_1M[tp_counter_1M] = 1000
                    

                    num_trade += 1


                    tp_counter_1M += 1

                    #******************************************************///////*****************************************************************************
                window_counter = TK_KS_signal_1M_sell['index'] - 1

            if (num_trade == 0): num_trade = 1000
            score_1M = (score_1M/num_trade) * 100

            if (num_trade < max_num_trade):
                score_1M = -10

            #print('*************************************** score_1M = ',score_1M,'  *****************************************************************')

            #******************************************************** faild break ***************************************************
            if (faild_flag >= num_turn):
                #print('faild flag')
                chrom_counter = len(Chromosome_1M) + 1
                break
            #******************************************************* ////////// ********************************************************


            #************************************************* Check save recreate 5M ************************************************************************

            if (score_1M < max_score_1M):
                chrom_faild_1M += 1
                chrom_faild += 1

                Chromosome_1M[chrom_counter] = {
                    #'apply_to': apply_to[randint(0, 7)],
                    'tp': (randint(0,1)/100),
                    'tenkan': randint(5, 120),
                    'kijun': randint(5, 120),
                    'snkou': randint(30, 260)
                    }

                if True:#(chrom_faild_1M > (len(Chromosome_1M)/4)):
                    ##print('new baby 5M')
                    while (Chromosome_1M[chrom_counter]['tenkan'] >= Chromosome_1M[chrom_counter]['kijun']):
                        Chromosome_1M[chrom_counter] = {
                            #'apply_to': apply_to[randint(0, 7)],
                            'tp': (randint(0,1)/100),
                            'tenkan': randint(5, 120),
                            'kijun': randint(5, 120),
                            'snkou': randint(30, 260)
                            }
                    chrom_faild_1M = 0
                    score_1M = 0

                    chrom_counter = 0

                if (chrom_faild >= ((len(Chromosome_1M)))):
                    chrom_faild = 0
                    chrom_counter = len(Chromosome_1M)
                else:
                    continue

            if (score_1M >= max_score_1M):
                chrom_faild_1M = 0
                try:
                    max_score_1M = score_1M

                    res = {key : abs(val) for key, val in percentage_sell_tp_save_1M.items()}

                    percentage_sell_tp_save_1M = min(res.values())

                    res = {key : abs(val) for key, val in percentage_sell_st_save_1M.items()}

                    percentage_sell_st_save_1M = max(res.values())

                    if percentage_sell_tp_save_1M != 0:
                        data_save_1M[chorm_save_counter_1M] = {
                        'symbol': sym.name,
                        #'apply_to': Chromosome_1M[chrom_counter][#'apply_to'],
                        'tp': percentage_sell_tp_save_1M,
                        'st': percentage_sell_st_save_1M,
                        'signal': 'sell',
                        'score': score_1M,
                        'kijun': Chromosome_1M[chrom_counter]['kijun'],
                        'tenkan': Chromosome_1M[chrom_counter]['tenkan'],
                        'snkou': Chromosome_1M[chrom_counter]['snkou']
                        }
                        chorm_save_counter_1M += 1

                        if (score_1M >= 195): faild_flag = num_turn + 1
                    score_1M = 0
                except:
                    print('fault')

            

            #******************************************************/////////////////////************************************************************************

            chrom_counter += 1

            #************************************* Create Gen ***********************************************************************
            if (chrom_counter >= ((len(Chromosome_1M)))):
                chrom_faild = 0
                faild_flag += 1
                #print('Gen Create')

                #chrom_counter = 0

                chrom_faild = 0
                chrom_faild_1M = 0

                Chromosome_1M,Chromosome_30M,Chromosome_1H = gen_creator(Chromosome_1M,Chromosome_30M,Chromosome_1H)
                continue
            #************************************ /////////// ************************************************************************

        #**************************** Calc Max tp & Min st *********************************************************

        try:
            max_score = max([abs(i['score']) for i in data_save_1M.values()])
            max_find_1M = {}
            min_find_1M = {}
            max_find_tp_1M = {}
            counter_find = 0
            for i in data_save_1M.values():
                if ((abs((i['score'])) == max_score) & (max_score != 0)):
                    max_find_1M[counter_find] = i
                    counter_find += 1

            max_tp = max([abs(i['tp']) for i in max_find_1M.values()])

            counter_find = 0
            for i in max_find_1M.values():
                if abs(i['tp']) == max_tp:
                    max_find_tp_1M[counter_find] = i
                    counter_find += 1

            min_st = min([abs(i['st']) for i in max_find_tp_1M.values()])

            counter_find = 0
            for i in max_find_tp_1M.values():
                if abs(i['st']) == min_st:
                    min_find_1M[counter_find] = i
                    counter_find += 1
        except:
            print('Empty')

        #********************************///////////////****************************************************************

        #*************************** Save to TXT File ***************************************************************

        try:
            if os.path.exists("Genetic_TsKs_output_sell_onebyone/1M/"+sym.name+'.csv'):
                os.remove("Genetic_TsKs_output_sell_onebyone/1M/"+sym.name+'.csv')

            add_row = {'tp' : min_find_1M[0]['tp'], 'st' : min_find_1M[0]['st'],
            'kijun': min_find_1M[0]['kijun'] , 'tenkan': min_find_1M[0]['tenkan'], 'snkou': min_find_1M[0]['snkou']
            ,'score': min_find_1M[0]['score']}

            with open("Genetic_TsKs_output_sell_onebyone/1M/"+sym.name+'.csv', 'w', newline='') as myfile:
                   fields=['tp','st','kijun','tenkan','snkou','score']
                   writer=csv.DictWriter(myfile,fieldnames=fields)
                   writer.writeheader()
                   writer.writerow(add_row)
        except:
            print('some thing wrong')

        print('************************ TSKS 1M SELL sym number = = ',sym_counter,' ******************************************')
        sym_counter += 1
        bar.next()

    print('**************************** Finish TSKS 1M SELL *********************************************')

#********************************//////////////-----------+++++++++++++//////////////***************************************************************


#TsKs_genetic_sell_algo_1M(0.02,3,5,50)       
#TsKs_genetic_buy_algo_1M(0.02,3,5,50)    