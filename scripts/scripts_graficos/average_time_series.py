# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
#plt.switch_backend('Qt4Agg')
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


# save path and user input user dates variables
resultsDir = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1'

# open files in folder and add names in specifics lists
hsNamesList = []
tpNamesList = []
dirNamesList = []
g = 9.8
rho = 1025 # sea water average density

# *WARNING* --> in "roda_sistema_hindcast.sh" the script do 'cd' to "vento_gelo_gfs" directory to run this 
# **FIX IT!!!**    script (extrai_datas.py). The netCDF4.Dataset is not working outside this folder!!!

# adding filename in lists
for file in os.listdir(resultsDir + '/swan-BG/arquivos_netCDF'):
    if "_dir" in file:
        dirNamesList.append(file)
    elif "_hs" in file:
        hsNamesList.append(file)
    elif "_per" in file:
        tpNamesList.append(file)
    else:
        continue

# sort lists elements in crescent order
hsNamesList.sort()
del hsNamesList[0] # delete december file
tpNamesList.sort()
del tpNamesList[0]
dirNamesList.sort()
del dirNamesList[0]

averageDict = {}
averagePointList = []
averageMonthlyList = []
# ***** looping through files in folder *****
for i, filename in enumerate(hsNamesList):
    # Pastas e arquivo
    datasetHsRegional = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/' + filename)
    datasetTpRegional = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/' + tpNamesList[i])
    datasetDirRegional = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/' + dirNamesList[i])
    pathSaveRegional = (resultsDir + '/swan-BG/imagens/wave_energy')
    waveHsRegional = datasetHsRegional['hs']
    waveTpRegional = datasetTpRegional['t02']
    #waveDirRegional = datasetDirRegional['dir'][:]
    time = datasetHsRegional['time']
    lats = datasetDirRegional['latitude'][:]
    lons = datasetDirRegional['longitude'][:]
    lon, lat = np.meshgrid(lons, lats)
    lonCorr = lon - 360
    # create listField related to time variable
    # inicial date according to file results
    listField = []
    initialDate = datetime(1990, 01, 01, 00)
    for j in time:
        d = initialDate + timedelta(days=j)
        datesString = d.strftime("%Y%m%d_%H%M%S")
        listField.append(datesString)
    # sort lists elements in crescent order
    listField.sort()
    sumPowerDensity = 0
    averagePowerDensity = 0
    # **** Cria imagens ****
    for index, name in enumerate(listField):
        waveFieldHsRegional = waveHsRegional[index,:,:]
        waveFieldTpRegional = waveTpRegional[index,:,:]
        powerDensity = [(rho*(g**2))/(64*math.pi)] * (waveFieldHsRegional**2) * waveFieldTpRegional
        sumPowerDensity = sumPowerDensity + powerDensity
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
ax.set_title(u'Monthly average of Wave Power Density (W/m²)')

locator = mdates.MonthLocator()  # every month
dfmt = mdates.DateFormatter('%b %y')

plt.plot(monthList ,averagePointList, linewidth=1.6)
plt.xticks(rotation=45)
X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)


