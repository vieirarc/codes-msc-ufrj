# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import matplotlib.patheffects as PathEffects
import matplotlib.dates as mdates
from netCDF4 import Dataset
import numpy as np
import scipy.io as sio
from mpl_toolkits.basemap import Basemap, cm
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from intdir2uv import intdir2uv
import math


# defining some diretories
resultsDir = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1'
pathSave = (resultsDir + '/swan-BG/imagens/time_series')

coastline = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/coastline_bg.mat')
costaLat = coastline['lat']
costaLon = coastline['lon']

# open files in folder and add names in specifics lists
energyNamesList = []

# adding filename in lists
for filename in os.listdir(resultsDir + '/swan-BG/arquivos_netCDF'):
    if "_transp_energy" in filename:
        energyNamesList.append(filename)
    else:
        continue


# sort lists elements in crescent order
energyNamesList.sort()
del energyNamesList[0] # delete december file


averageDict = {}
averagePointList = []
averageMonthlyList = []
# ***** looping through files in folder *****
for i, filename in enumerate(energyNamesList):
    # Pastas e arquivo
    datasetEnergy = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/' + filename)
    uWaveEnergy = datasetEnergy['u_component_energy_transp']
    vWaveEnergy = datasetEnergy['v_component_energy_transp']
    time = datasetEnergy['time']
    # create listField related to time variable
    # inicial date according to file results
    listField = []
    initialDate = datetime(1990, 01, 01, 00)
    for j in time:
        d = initialDate + timedelta(days=np.float64(j))
        datesString = d.strftime("%Y%m%d_%H%M%S")
        listField.append(datesString)
    # sort lists elements in crescent order
    listField.sort()
    sumPowerDensity = 0
    averagePowerDensity = 0
    # calculate wave power and average
    for index, name in enumerate(listField):
        uEnergyField = uWaveEnergy[i,:,:]
        vEnergyField = vWaveEnergy[i,:,:]
        waveEnegy = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumPowerDensity = sumPowerDensity + waveEnegy
    averageMonthly = sumPowerDensity / len(listField)
    averageMonthlyList.append(averageMonthly)
    #average = average.data
for index, name in enumerate(averageMonthlyList):
    averagePoint = averageMonthlyList[index][24, 188]
    averagePointList.append(averagePoint)


# create a list of months
monthList = []
initialDate = datetime(2017, 01, 01, 00)
for j in range(24):
    d = initialDate + relativedelta(months=j)
    monthList.append(d)


# creating graph
fig = plt.figure()
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series of Wave Power Monthly Average')

locator = mdates.MonthLocator()  # every month
dfmt = mdates.DateFormatter('%b %y')

plt.plot(monthList ,averagePointList, linewidth=1.6)
plt.xticks(rotation=45)
plt.ylabel('Wave Power (W/m)', size=12, rotation=90, labelpad=4)
X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)

#plt.savefig(os.path.join(pathSave, 'annual_average_timeSeries'), bbox_inches='tight', dpi=400)


