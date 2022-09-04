from src.utils import extremePoints, bestExtremeFinder
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def sikimi(
        y3, y4, symbol_data_5M, symbol_data_15M, symbol_data_1D,
        symbol_data_1H, symbol_data_4H, exterm_point_pred):

    i = len(y3) - 1
    while True:
        end = i
        i += 100

        local_extreme_5M = pd.DataFrame()
        local_extreme_5M['extreme'] = pd.DataFrame(
                extremePoints(
                    high=symbol_data_5M['AUDCAD_i']['high'][0:end],
                    low=symbol_data_5M['AUDCAD_i']['low'][0:end],
                    number_min=5, number_max=5))
        local_extreme_5M['power'] = np.ones(len(local_extreme_5M))*1

        local_extreme_15M = pd.DataFrame()
        local_extreme_15M['extreme'] = pd.DataFrame(
                extremePoints(
                    high=symbol_data_15M['AUDCAD_i']['high'],
                    low=symbol_data_15M['AUDCAD_i']['low'],
                    number_min=5, number_max=5))
        local_extreme_15M['power'] = np.ones(len(local_extreme_15M))*3

        local_extreme_1H = pd.DataFrame()
        local_extreme_1H['extreme'] = pd.DataFrame(
                extremePoints(
                    high=symbol_data_1H['AUDCAD_i']['high'],
                    low=symbol_data_1H['AUDCAD_i']['low'],
                    number_min=5, number_max=5))
        local_extreme_1H['power'] = np.ones(len(local_extreme_1H))*12

        local_extreme_4H = pd.DataFrame()
        local_extreme_4H['extreme'] = pd.DataFrame(
                extremePoints(
                    high=symbol_data_4H['AUDCAD_i']['high'],
                    low=symbol_data_4H['AUDCAD_i']['low'],
                    number_min=2, number_max=2))
        local_extreme_4H['power'] = np.ones(len(local_extreme_4H))*48

        local_extreme_1D = pd.DataFrame()
        local_extreme_1D['extreme'] = pd.DataFrame(
                extremePoints(
                    high=symbol_data_1D['AUDCAD_i']['high'],
                    low=symbol_data_1D['AUDCAD_i']['low'],
                    number_min=2, number_max=2))
        local_extreme_1D['power'] = np.ones(len(local_extreme_1D))*288

        exterm_point = pd.DataFrame(
                np.concatenate(
                    (local_extreme_5M['extreme'].to_numpy(),
                     local_extreme_15M['extreme'].to_numpy(),
                     local_extreme_1H['extreme'].to_numpy(),
                     local_extreme_4H['extreme'].to_numpy(),
                     local_extreme_1D['extreme'].to_numpy(),
                     exterm_point_pred['extremes'].to_numpy()), axis=None),
                columns=['extremes'])

        exterm_point['power'] = np.concatenate(
                (local_extreme_5M['power'].to_numpy(),
                 local_extreme_15M['power'].to_numpy(),
                 local_extreme_1H['power'].to_numpy(),
                 local_extreme_4H['power'].to_numpy(),
                 local_extreme_1D['power'].to_numpy(),
                 exterm_point_pred['power'].to_numpy()), axis=None)

        extereme = bestExtremeFinder(
                exterm_point=exterm_point,
                high=y3[0:end], low=y4[0:end],
                n_clusters_low=5, n_clusters_high=5,
                alpha_low=0.1, alpha_high=0.05, timeout_break=1)

        fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 6))
        ax0.axhline(y=extereme['high'][0], color='r', linestyle='-')
        ax0.axhline(y=extereme['high'][1], color='g', linestyle='-')
        ax0.axhline(y=extereme['high'][2], color='r', linestyle='-')

        ax0.axhline(y=extereme['low'][0], color='g', linestyle='-')
        ax0.axhline(y=extereme['low'][1], color='b', linestyle='-')
        ax0.axhline(y=extereme['low'][2], color='g', linestyle='-')

        ax0.axvline(x=end, color='r', linestyle='-')
        ax1.axvline(x=end, color='r', linestyle='-')

        ax0.plot(y3.index[end-100:end], y3[end-100:end], 'b')
        ax1.plot(y3.index[end-10:end+300], y3[end-10:end+300], 'b')
        plt.show()
