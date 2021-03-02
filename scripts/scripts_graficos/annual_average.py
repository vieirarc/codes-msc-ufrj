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

fig = plt.figure(figsize=(8, 12))

totalFields2017 = 0
totalFields2018 = 0
sumPowerDensity2017 = 0
sumPowerDensity2018 = 0

# ***** looping through files in folder *****
for i, filename in enumerate(hsNamesList):
    if '2017' in filename:
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
            dates = initialDate + timedelta(days=j)
            datesString = dates.strftime("%Y%m%d_%H%M%S")
            listField.append(datesString)
        # sort lists elements in crescent order
        listField.sort()
        # **** Cria imagens ****
        for index, name in enumerate(listField): # monthly block
            waveFieldHsRegional = waveHsRegional[index,:,:]
            waveFieldTpRegional = waveTpRegional[index,:,:]
            powerDensity = [(rho*(g**2))/(64*math.pi)] * (waveFieldHsRegional**2) * waveFieldTpRegional
            sumPowerDensity2017 = sumPowerDensity2017 + powerDensity 
        totalFields2017 = totalFields2017 + len(listField)
    else:
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
            dates = initialDate + timedelta(days=j)
            datesString = dates.strftime("%Y%m%d_%H%M%S")
            listField.append(datesString)
        # sort lists elements in crescent order
        listField.sort()
        # **** Cria imagens ****
        for index, name in enumerate(listField): # monthly block
            waveFieldHsRegional = waveHsRegional[index,:,:]
            waveFieldTpRegional = waveTpRegional[index,:,:]
            powerDensity = [(rho*(g**2))/(64*math.pi)] * (waveFieldHsRegional**2) * waveFieldTpRegional
            sumPowerDensity2018 = sumPowerDensity2018 + powerDensity 
        totalFields2018 = totalFields2018 + len(listField)

averageAnnual2017 = sumPowerDensity2017 / totalFields2017
averageAnnual2018 = sumPowerDensity2018 / totalFields2018


fig = plt.figure()
m = Basemap(llcrnrlon=-43.7, llcrnrlat=-23.6, urcrnrlon=-42.4, urcrnrlat=-22.0,\
                                 resolution='h', projection='merc')
m.drawcoastlines(linewidth=0.8)
m.drawstates(linewidth=0.1)
m.drawcountries(linewidth=0.6)
m.fillcontinents(color='0.8', lake_color='None')
m.drawparallels(np.arange(-23.9, -21.9 ,0.5), fontsize=7, linewidth=0.03, labels=[1,0,0,0])
m.drawmeridians(np.arange(m.lonmin,m.lonmax, 0.5), fontsize=7, linewidth=0.03, labels=[0,0,0,1])
#u, v = intdir2uv(1, waveDirRegional[index,:,:])
#ut = -u
#vt = -v
x, y = m(lonCorr,lat)
levels= [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000]
cf = m.contour(x, y, averageAnnual2017, levels, colors='white', linestyles='solid')
isobaths_labels = plt.clabel( cf, fmt='%i', colors='white', fontsize=6)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
im = m.pcolormesh(x, y, averageAnnual2017, vmin=0, vmax=12100, shading='gouraud')  
#m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
#    scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
cbar = m.colorbar(im, pad="10%")
cbar.set_label(u'Wave power (W/m²)', size=7)
cbar.set_ticks([np.arange(0, 12100, 1000)], update_ticks=True)
cbar.ax.tick_params(labelsize=7)
hour = str(name)[9:11]
day = str(name)[6:8]
month = str(name)[4:6]
year = str(name)[0:4]
plt.title('Annual average of Wave Power Density - 2017', fontsize=10)
plt.savefig(os.path.join(pathSaveRegional + '/annual_average_wave_power_density', 'annual_2017'), bbox_inches='tight', dpi=300)

# *************** 2018 ************

fig = plt.figure()
m = Basemap(llcrnrlon=-43.7, llcrnrlat=-23.6, urcrnrlon=-42.4, urcrnrlat=-22.0,\
                                 resolution='h', projection='merc')
m.drawcoastlines(linewidth=0.8)
m.drawstates(linewidth=0.1)
m.drawcountries(linewidth=0.6)
m.fillcontinents(color='0.8', lake_color='None')
m.drawparallels(np.arange(-23.9, -21.9 ,0.5), fontsize=7, linewidth=0.03, labels=[1,0,0,0])
m.drawmeridians(np.arange(m.lonmin,m.lonmax, 0.5), fontsize=7, linewidth=0.03, labels=[0,0,0,1])
#u, v = intdir2uv(1, waveDirRegional[index,:,:])
#ut = -u
#vt = -v
x, y = m(lonCorr,lat)
levels= [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000]
cf = m.contour(x, y, averageAnnual2018, levels, colors='white', linestyles='solid')
isobaths_labels = plt.clabel( cf, fmt='%i', colors='white', fontsize=6)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
im = m.pcolormesh(x, y, averageAnnual2018, vmin=0, vmax=12100, shading='gouraud')  
#m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
#    scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
cbar = m.colorbar(im, pad="10%")
cbar.set_label(u'Wave power (W/m²)', size=7)
cbar.set_ticks([np.arange(0, 12100, 1000)], update_ticks=True)
cbar.ax.tick_params(labelsize=7)
hour = str(name)[9:11]
day = str(name)[6:8]
month = str(name)[4:6]
year = str(name)[0:4]
plt.title('Annual average of Wave Power Density - 2018', fontsize=10)
plt.savefig(os.path.join(pathSaveRegional + '/annual_average_wave_power_density', 'annual_2018'), bbox_inches='tight', dpi=300)
