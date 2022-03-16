from scipy.stats import foldnorm, dweibull, rayleigh, expon, nakagami, norm
from scipy.signal import argrelextrema
from sklearn.cluster import KMeans
from fitter import Fitter
import pandas_ta as ind
import pandas as pd
import numpy as np
import time


def extremePoints(high, low, number_min, number_max):
    extremes = pd.DataFrame(low, columns=['low'])
    extremes['high'] = high

    # Finding Extreme Points
    extremes['min'] = extremes.iloc[
            argrelextrema(
                extremes.low.values, comparator=np.less,
                order=number_max)[0]]['low']
    extremes['max'] = extremes.iloc[
            argrelextrema(
                extremes.high.values, comparator=np.greater,
                order=number_max)[0]]['high']
    exterm_point = pd.DataFrame(
            np.concatenate(
                (extremes['max'].dropna().to_numpy(),
                 extremes['min'].dropna().to_numpy()), axis=None),
            columns=['extremes'])

    return exterm_point


def extremePointsIchimoko(
        high, low, close, tenkan=9, kijun=26, senkou=52, n_clusters=15):

    ichi = ind.ichimoku(
            high=high, low=low, close=close,
            tenkan=tenkan, kijun=kijun, senkou=senkou)

    column = ichi[0].columns[0]
    SPANA = pd.DataFrame(ichi[0], columns=[column])
    column = ichi[0].columns[1]
    SPANB = pd.DataFrame(ichi[0], columns=[column])
    column = ichi[0].columns[2]
    Tenkan = pd.DataFrame(ichi[0], columns=[column])
    column = ichi[0].columns[3]
    Kijun = pd.DataFrame(ichi[0], columns=[column])

    Tenkan_train = pd.DataFrame()
    Tenkan_train['extreme'] = Tenkan.dropna()
    Tenkan_train['power'] = np.ones(len(Tenkan_train))*1

    Kijun_train = pd.DataFrame()
    Kijun_train['extreme'] = Kijun.dropna()
    Kijun_train['power'] = np.ones(len(Kijun_train))*1

    SPANA_train = pd.DataFrame()
    SPANA_train['extreme'] = SPANA.dropna()
    SPANA_train['power'] = np.ones(len(SPANA_train))*2

    SPANB_train = pd.DataFrame()
    SPANB_train['extreme'] = SPANB.dropna()
    SPANB_train['power'] = np.ones(len(SPANB_train))*2

    Three_train_1 = pd.DataFrame(
            np.concatenate(
                (Kijun_train['extreme'].to_numpy(),
                 SPANA_train['extreme'].to_numpy(),
                 SPANB_train['extreme'].to_numpy()), axis=None),
            columns=['extreme'])
    Three_train_1['power'] = np.ones(len(Three_train_1)) * 3

    Three_train_2 = pd.DataFrame(
            np.concatenate(
                (Tenkan_train['extreme'].to_numpy(),
                 SPANA_train['extreme'].to_numpy(),
                 SPANB_train['extreme'].to_numpy()), axis=None),
            columns=['extreme'])
    Three_train_2['power'] = np.ones(len(Three_train_2))*3

    Four_train = pd.DataFrame(
            np.concatenate(
                (Tenkan_train['extreme'].to_numpy(),
                 Kijun_train['extreme'].to_numpy(),
                 SPANA_train['extreme'].to_numpy(),
                 SPANB_train['extreme'].to_numpy()), axis=None),
            columns=['extreme'])
    Four_train['power'] = np.ones(len(Four_train))*4

    exterm_point = pd.DataFrame(
            np.concatenate(
                (
                    Tenkan_train['extreme'].to_numpy(),
                    Kijun_train['extreme'].to_numpy(),
                    SPANA_train['extreme'].to_numpy(),
                    SPANB_train['extreme'].to_numpy(),
                    Three_train_1['extreme'].to_numpy(),
                    Three_train_2['extreme'].to_numpy(),
                    Four_train['extreme'].to_numpy()
                ), axis=None), columns=['extremes'])

    exterm_point['power'] = np.concatenate(
            (
                Tenkan_train['power'].to_numpy(),
                Kijun_train['power'].to_numpy(),
                SPANA_train['power'].to_numpy(),
                SPANB_train['power'].to_numpy(),
                Three_train_1['power'].to_numpy(),
                Three_train_2['power'].to_numpy(),
                Four_train['power'].to_numpy()
            ), axis=None)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    # fitting
    kmeans = kmeans.fit(
            exterm_point['extremes'].to_numpy().reshape(-1, 1),
            sample_weight=exterm_point['power'].to_numpy())

    X_pred = kmeans.cluster_centers_
    Power = np.bincount(kmeans.fit_predict(y1.to_numpy().reshape(-1, 1)))
    Y_pred = kmeans.labels_

    exterm_point_pred = pd.DataFrame(X_pred, columns=['extremes'])
    exterm_point_pred['power'] = Power

    return exterm_point_pred


def bestExtremeFinder(
        exterm_point, high, low, n_clusters_low, n_clusters_high,
        alpha_low, alpha_high, timeout_break):
    """
    ************* Help ***************
    exterm_point: All Extreme Points From Protection Resistion Functions
    n_clusters: Number Of Mean Centers Of Extreme Points, **** Must Be
    Optimazing and save in Database ****
    high: the High Level Of Candles from that Time Frame You want
    low: the Low Level Of Candles from that Time Frame You want
    alpha: the Accuracy of Finding Best Protection Or Resistation,
    **** Must Be Optimazing and save in Database ****
    timeout_break: Maximum Time Out For Running this Optimizer
    """

    timeout = time.time() + timeout_break  # timeout_break Sec from now\
    while True:
        kmeans_low = KMeans(
                n_clusters=n_clusters_low, random_state=0,
                init='k-means++', n_init=10, max_iter=100)
        kmeans_high = KMeans(
                n_clusters=n_clusters_high, random_state=0,
                init='k-means++', n_init=10, max_iter=100)
        # Model Fitting
        kmeans_low = kmeans_low.fit(
                exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes'] <= high[len(high)-1])].reshape(-1, 1), sample_weight=exterm_point['power'].to_numpy()[np.where(exterm_point['extremes'] <= high[len(high)-1])])
        kmeans_high = kmeans_high.fit(exterm_point['extremes'].to_numpy()[np.where(exterm_point['extremes'] >= low[len(low)-1])].reshape(-1, 1), sample_weight=exterm_point['power'].to_numpy()[np.where(exterm_point['extremes'] >= low[len(low)-1])])

        Y_low = kmeans_low.cluster_centers_
        Y_high = kmeans_high.cluster_centers_

        Power_low = kmeans_low.fit_predict(low.to_numpy()[np.where(low <= high[len(high) - 1])].reshape(-1, 1))
        Power_high = kmeans_high.fit_predict(high.to_numpy()[np.where(high >= low[len(low) - 1])].reshape(-1, 1))

        X_low = kmeans_low.cluster_centers_
        X_high = kmeans_high.cluster_centers_

        Power_low = np.bincount(Power_low)
        Power_high = np.bincount(Power_high)

        if ((len(Y_low) != len(X_low)) | ((len(Y_high) != len(X_high)))):
            timeout = time.time() + timeout_break
            continue
        if ((len(Y_low) == len(X_low)) & ((len(Y_high) == len(X_high)))):
            break

    exterm_point_pred_final_low = pd.DataFrame(X_low, columns=['X'])
    exterm_point_pred_final_low['Y'] = Y_low
    exterm_point_pred_final_low['power'] = Power_low
    exterm_point_pred_final_low = exterm_point_pred_final_low.sort_values(
            by=['X'])

    exterm_point_pred_final_high = pd.DataFrame(X_high, columns=['X'])
    exterm_point_pred_final_high['Y'] = Y_high
    exterm_point_pred_final_high['power'] = Power_high
    exterm_point_pred_final_high = exterm_point_pred_final_high.sort_values(
            by=['X'])

    # Fitting Model Finding ****************************
    data_X_high = np.zeros(np.sum(exterm_point_pred_final_high['power']))
    data_X_low = np.zeros(np.sum(exterm_point_pred_final_low['power']))

    j = 0
    z = 0
    for elm in exterm_point_pred_final_low['X']:
        k = 0
        while k < exterm_point_pred_final_low['power'].to_numpy()[j]:
            data_X_low[z] = elm
            k += 1
            z += 1
        j += 1

    j = 0
    z = 0
    for elm in exterm_point_pred_final_high['X']:
        k = 0
        while k < exterm_point_pred_final_high['power'].to_numpy()[j]:
            data_X_high[z] = elm
            k += 1
            z += 1
        j += 1

    # data = np.sort(data)
    data_X_low = np.sort(data_X_low)
    data_X_high = np.sort(data_X_high)

    timeout = time.time() + timeout_break  # timeout_break Sec from now
    distributions_low = ['foldnorm', 'dweibull', 'rayleigh',
                         'expon', 'nakagami', 'norm']
    distributions_high = ['foldnorm', 'dweibull', 'rayleigh',
                          'expon', 'nakagami', 'norm']

    # ************************************ Finding Low ***********************

    while True:
        f_low = Fitter(
                data=data_X_low,
                xmin=np.min(data_X_low),
                xmax=np.max(data_X_low),
                bins=len(exterm_point_pred_final_low['X']),
                distributions=distributions_low, timeout=30,
                density=True)
        f_low.fit(amp=1, progress=False, n_jobs=-1)

        items_low = list(f_low.get_best(method='sumsquare_error').items())
        dist_name_low = items_low[0][0]
        dist_parameters = items_low[0][1]

        if dist_name_low == 'foldnorm':
            Y = f_low.fitted_pdf['foldnorm']
            Y = foldnorm.pdf(
                    x=data_X_low, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = foldnorm.interval(
                    alpha=alpha_low, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        elif dist_name_low == 'dweibull':
            Y = f_low.fitted_pdf['dweibull']
            Y = dweibull.pdf(
                    x=data_X_low, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = dweibull.interval(
                    alpha=alpha_low, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        elif dist_name_low == 'rayleigh':
            Y = f_low.fitted_pdf['rayleigh']
            Y = rayleigh.pdf(
                    x=data_X_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = rayleigh.interval(
                    alpha=alpha_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        elif dist_name_low == 'expon':
            Y = f_low.fitted_pdf['expon']
            Y = expon.pdf(
                    x=data_X_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = expon.interval(
                    alpha=alpha_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        elif dist_name_low == 'nakagami':
            Y = f_low.fitted_pdf['nakagami']
            Y = nakagami.pdf(
                    x=data_X_low, nu=dist_parameters['nu'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = nakagami.interval(
                    alpha=alpha_low, nu=dist_parameters['nu'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        elif dist_name_low == 'norm':
            Y = f_low.fitted_pdf['norm']
            Y = norm.pdf(
                    x=data_X_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = norm.interval(
                    alpha=alpha_low, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_low = Extereme[1]
            Lower_Line_low = Extereme[0]
            Mid_Line_low = np.array(dist_parameters['loc'])
            Power_Upper_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Upper_Line_low.reshape(1, -1))].to_numpy()
            Power_Lower_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Lower_Line_low.reshape(1, -1))].to_numpy()
            Power_Mid_Line_low = exterm_point_pred_final_low['power'][kmeans_low.predict(Mid_Line_low.reshape(1, -1))].to_numpy()

        if time.time() > timeout:
            if distributions_low is None:
                return 'timeout.error'

        if Mid_Line_low <= Upper_Line_low and Mid_Line_low >= Lower_Line_low:
            break
        else:
            distributions_low.remove(dist_name_low)
            if distributions_low is None:
                return 'timeout.error'

    timeout = time.time() + timeout_break  # timeout_break Sec from now
    # ************************ Finding High ************************
    while True:
        f_high = Fitter(
                data=data_X_high, xmin=np.min(data_X_high),
                xmax=np.max(data_X_high),
                bins=len(exterm_point_pred_final_high['X']),
                distributions=distributions_high, timeout=30,
                density=True)
        f_high.fit(amp=1, progress=False, n_jobs=-1)

        items_high = list(f_high.get_best(method='sumsquare_error').items())
        dist_name_high = items_high[0][0]
        dist_parameters = items_high[0][1]

        if dist_name_high == 'foldnorm':
            Y = f_high.fitted_pdf['foldnorm']
            Y = foldnorm.pdf(
                    x=data_X_high, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = foldnorm.interval(
                    alpha=alpha_high, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        elif dist_name_high == 'dweibull':
            Y = f_high.fitted_pdf['dweibull']
            Y = dweibull.pdf(
                    x=data_X_high, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = dweibull.interval(
                    alpha=alpha_high, c=dist_parameters['c'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        elif dist_name_high == 'rayleigh':
            Y = f_high.fitted_pdf['rayleigh']
            Y = rayleigh.pdf(
                    x=data_X_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = rayleigh.interval(
                    alpha=alpha_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        elif dist_name_high == 'expon':
            Y = f_high.fitted_pdf['expon']
            Y = expon.pdf(
                    x=data_X_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = expon.interval(
                    alpha=alpha_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        elif dist_name_high == 'nakagami':
            Y = f_high.fitted_pdf['nakagami']
            Y = nakagami.pdf(
                    x=data_X_high, nu=dist_parameters['nu'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Extereme = nakagami.interval(
                    alpha=alpha_high, nu=dist_parameters['nu'],
                    loc=dist_parameters['loc'], scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        elif dist_name_high == 'norm':
            Y = f_high.fitted_pdf['norm']
            Y = norm.pdf(
                    x=data_X_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Extereme = norm.interval(
                    alpha=alpha_high, loc=dist_parameters['loc'],
                    scale=dist_parameters['scale'])
            Upper_Line_high = Extereme[1]
            Lower_Line_high = Extereme[0]
            Mid_Line_high = np.array(dist_parameters['loc'])
            Power_Upper_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Upper_Line_high.reshape(1, -1))].to_numpy()
            Power_Lower_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Lower_Line_high.reshape(1, -1))].to_numpy()
            Power_Mid_Line_high = exterm_point_pred_final_high['power'][kmeans_high.predict(Mid_Line_high.reshape(1, -1))].to_numpy()

        if time.time() > timeout:
            if distributions_high is None:
                return 'timeout.error'

        if (
                Mid_Line_high <= Upper_Line_high and
                Mid_Line_high >= Lower_Line_high
                ):
            break
        else:
            distributions_high.remove(dist_name_high)
            if distributions_high is None:
                return 'timeout.error'

    best_extremes = pd.DataFrame()
    best_extremes['high'] = [Upper_Line_high, Mid_Line_high, Lower_Line_high]
    best_extremes['power_high'] = [Power_Upper_Line_high, Power_Mid_Line_high,
                                   Power_Lower_Line_high]
    best_extremes['low'] = [Upper_Line_low, Mid_Line_low, Lower_Line_low]
    best_extremes['power_low'] = [Power_Upper_Line_low, Power_Mid_Line_low,
                                  Power_Lower_Line_low]

    return best_extremes
