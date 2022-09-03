from fastai.tabular.all import *
from Mt5_LoginGetData import LoginGetData as getdata
from indicator_Divergence import Divergence
from indicator_Tester import Tester
from macd_Parameters import Parameters
from macd_Config import Config
from macd_MACD import MACD
import pandas as pd
from indicator_Parameters import Parameters as indicator_parameters
from indicator_Config import Config as indicator_config

from pr_Parameters import Parameters as pr_Parameters
from pr_Config import Config as pr_Config

import pandas_ta as ind

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from random import randint


loging = getdata()


parameters = Parameters()
config = Config()

ind_params = indicator_parameters()
ind_config = indicator_config()



data_5M, data_1H = loging.readall(symbol = 'ETHUSD_i', number_5M = 1000, number_1H = 10)

signal_out = data_5M['ETHUSD_i'].copy(deep = True)

# Ready for ploting :

plt.style.use("seaborn-whitegrid")
plt.rc("figure", autolayout=True, figsize=(11, 5))
plt.rc(
	    "axes",
	    labelweight="bold",
	    labelsize="large",
	    titleweight="bold",
	    titlesize=14,
	    titlepad=10,
	)

plot_params = dict(
				    color="0.75",
				    style=".-",
				    markeredgecolor="0.25",
				    markerfacecolor="0.25",
				    legend=False,
				)
#/////////////////////////////////////////////

# Load Tunnel Traffic dataset

signal_out = signal_out.set_index('time').to_period('D')

moving_average = signal_out.rolling(
									    window=365,       # 365-day window
									    center=True,      # puts the average at the center of the window
									    min_periods=183,  # choose about half the window size
									).mean()              # compute the mean (could also do median, std, min, max, ...)

# ax = signal_out.plot(style=".", color="0.5")
# moving_average.plot(
# 					    ax=ax, linewidth=3, title="Prices - 365-Day Moving Average", legend=False,
# 					)
#plt.show()

from statsmodels.tsa.deterministic import DeterministicProcess

dp = DeterministicProcess(
						    index=signal_out.index,  # dates from the training data
						    constant=True,       # dummy feature for the bias (y_intercept)
						    order=5,             # the time dummy (trend)
						    drop=True,           # drop terms if necessary to avoid collinearity
						    #seasonal=True,
						)
# `in_sample` creates features for the dates given in the `index` argument
X = dp.in_sample()

# print('X = ',X.head())

from sklearn.linear_model import LinearRegression

y = signal_out["close"]  # the target

# The intercept is the same as the `const` feature from
# DeterministicProcess. LinearRegression behaves badly with duplicated
# features, so we need to be sure to exclude it here.
model = LinearRegression(fit_intercept=False)
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)

# ax = signal_out.plot(style=".", color="0.5", title="Prices - Linear Trend")
# _ = y_pred.plot(ax=ax, linewidth=3, label="Trend")
#plt.show()

X = dp.out_of_sample(steps=10)

y_fore = pd.Series(model.predict(X), index=X.index)

# print('Y_fore = ',y_fore)

# ax = signal_out["2021-03-19 20:30:00":].plot(title="Prices - Linear Trend Forecast", **plot_params)
# ax = y_pred["2021-03-19 20:30:00":].plot(ax=ax, linewidth=3, label="Trend")
# ax = y_fore.plot(ax=ax, linewidth=3, label="Trend Forecast", color="C3")
# _ = ax.legend()

#plt.show()

def fourier_features(index, freq, order):
    time = np.arange(len(index), dtype=np.float32)
    k = 2 * np.pi * (1 / freq) * time
    features = {}
    for i in range(1, order + 1):
        features.update({
            f"sin_{freq}_{i}": np.sin(i * k),
            f"cos_{freq}_{i}": np.cos(i * k),
        })
    return pd.DataFrame(features, index=index)


# Compute Fourier features to the 4th order (8 new features) for a
# series y with daily observations and annual seasonality:
#
# fourier_features(y, freq=365.25, order=4)


from pathlib import Path
from warnings import simplefilter
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

simplefilter("ignore")

# Set Matplotlib defaults
plt.style.use("seaborn-whitegrid")
plt.rc("figure", autolayout=True, figsize=(11, 5))
plt.rc(
	    "axes",
	    labelweight="bold",
	    labelsize="large",
	    titleweight="bold",
	    titlesize=16,
	    titlepad=10,
	)
plot_params = dict(
	    color="0.75",
	    style=".-",
	    markeredgecolor="0.25",
	    markerfacecolor="0.25",
	    legend=False,
	)

# annotations: https://stackoverflow.com/a/49238256/5769929
def seasonal_plot(X, y, period, freq, ax=None):
    if ax is None:
        _, ax = plt.subplots()
    palette = sns.color_palette("husl", n_colors=X[period].nunique(),)
    ax = sns.lineplot(
        x=freq,
        y=y,
        hue=period,
        data=X,
        ci=False,
        ax=ax,
        palette=palette,
        legend=False,
    )
    ax.set_title(f"Seasonal Plot ({period}/{freq})")
    for line, name in zip(ax.lines, X[period].unique()):
        y_ = line.get_ydata()[-1]
        ax.annotate(
            name,
            xy=(1, y_),
            xytext=(6, 0),
            color=line.get_color(),
            xycoords=ax.get_yaxis_transform(),
            textcoords="offset points",
            size=14,
            va="center",
        )
    return ax


def plot_periodogram(ts, detrend='linear', ax=None):
    from scipy.signal import periodogram
    fs = pd.Timedelta("1H") / pd.Timedelta("5T")
    freqencies, spectrum = periodogram(
								        ts,
								        fs=fs,
								        detrend=detrend,
								        window="boxcar",
								        scaling='spectrum',
								    )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(
				        [
				            "Annual (1)",
				            "Semiannual (2)",
				            "Quarterly (4)",
				            "Bimonthly (6)",
				            "Monthly (12)",
				            "Biweekly (26)",
				            "Weekly (52)",
				            "Semiweekly (104)",
				        ],
				        rotation=30,
				    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    return ax

X = signal_out.copy()
print(X.columns)

# days within a week
X["day"] = X.index.dayofweek  # the x-axis (freq)
X["week"] = X.index.week  # the seasonal period (period)

# days within a year
X["dayofyear"] = X.index.dayofyear
X["year"] = X.index.year
# fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(11, 6))
# seasonal_plot(X, y="close", period="week", freq="day", ax=ax0)
# seasonal_plot(X, y="close", period="year", freq="dayofyear", ax=ax1)

plot_periodogram(signal_out.close)

plt.show()

fourier = CalendarFourier(freq="A", order=10)  # 10 sin/cos pairs for "A"nnual seasonality

dp = DeterministicProcess(
						    index=signal_out.index,
						    constant=True,               # dummy feature for bias (y-intercept)
						    order=1,                     # trend (order 1 means linear)
						    seasonal=True,               # weekly seasonality (indicators)
						    additional_terms=[fourier],  # annual seasonality (fourier)
						    drop=True,                   # drop terms to avoid collinearity
						)

X = dp.in_sample()  # create features for dates in tunnel.index

print(X)

y = signal_out["close"]

model = LinearRegression(fit_intercept=False)
_ = model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=y.index)
X_fore = dp.out_of_sample(steps=2)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

ax = y.plot(color='0.25', style='.', title="Tunnel Traffic - Seasonal Forecast")
ax = y_pred.plot(ax=ax, label="Seasonal")
ax = y_fore.plot(ax=ax, label="Seasonal Forecast", color='C3')
_ = ax.legend()
plt.show()
