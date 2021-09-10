# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker
from netCDF4 import Dataset
import numpy as np
import scipy.io as sio
from datetime import date, datetime, timedelta
import collections
from windrose import WindroseAxes
import math



# original windrose plot


# As variáveis dirPointSummer2017 e energyPointSummer2017
# sao vetores unidimensionais


# creating plot
ax = WindroseAxes.from_ax()
ax.bar(dirPointSummer2017, energyPointSummer2017, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
la = np.arange(0, max(energyPointSummer2017), 4000)

# getting labels as strig
laList = []
laFinalList = []

for i in la:
    nLa = int(i / 1000)
    nLaStr = str(nLa)
    laList.append(nLaStr)

for index, name in enumerate(laList):
    if index < 5:
        laNsum = name + ' - ' + laList[index + 1]
        laFinalList.append(laNsum)
    else:
        laNsum = name + ' +'
        laFinalList.append(laNsum)



obs = 'Frequency in % of time'
ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                             prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
plt.gcf().text(0.701, 0.611111111111, obs, fontsize=11)
ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
ax.set_yticks(numpy.arange(5, 35.1, 5))
ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
ax.set_rlabel_position(45)  # get radial labels away from plotted line
ax.set_title('Wave energy transport', fontsize=16)
