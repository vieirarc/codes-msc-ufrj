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

averageDict = {}
fig = plt.figure(figsize=(8, 12))

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
        dates = initialDate + timedelta(days=j)
        datesString = dates.strftime("%Y%m%d_%H%M%S")
        listField.append(datesString)
    # sort lists elements in crescent order
    listField.sort()
    sumPowerDensity = 0
    averagePowerDensity = 0
    # **** Cria imagens ****
    for index, name in enumerate(listField): # monthly block
        waveFieldHsRegional = waveHsRegional[index,:,:]
        waveFieldTpRegional = waveTpRegional[index,:,:]
        powerDensity = [(rho*(g**2))/(64*math.pi)] * (waveFieldHsRegional**2) * waveFieldTpRegional
        sumPowerDensity = sumPowerDensity + powerDensity 
    averageMonthly = sumPowerDensity / len(listField)
    # ************************* fields plot ****************************************
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
    cf = m.contour(x, y, averageMonthly, levels, colors='white', linestyles='solid')
    isobaths_labels = plt.clabel( cf, fmt='%i', colors='white', fontsize=5)
    plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
    im = m.pcolormesh(x, y, averageMonthly, vmin=0, vmax=18100, shading='gouraud')  
    #m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
    #    scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
    cbar = m.colorbar(im, pad="10%")
    cbar.set_label(u'Wave power (W/m²)', size=5)
    cbar.set_ticks([np.arange(0, 18100, 2000)], update_ticks=True)
    cbar.ax.tick_params(labelsize=5)
    hour = str(name)[9:11]
    day = str(name)[6:8]
    month = str(name)[4:6]
    year = str(name)[0:4]
    plt.title('Monthly average of Wave Power Density ' + year + '/' + month, fontsize=12)
    plt.savefig(os.path.join(pathSaveRegional, year + month), bbox_inches='tight', dpi=300)
    i = i + 1
    #plt.figure(figsize=(16,8))
    if i <= 12: # *********************** subplots ************************
        a = plt.subplot(4, 3, i)
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
        cf = m.contour(x, y, averageMonthly, levels, colors='white', linestyles='solid')
        isobaths_labels = plt.clabel( cf, fmt='%i', colors='white', fontsize=5)
        plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
        im = m.pcolormesh(x, y, averageMonthly, vmin=0, vmax=18100, shading='gouraud')  
        #m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
        #    scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
        cbar = m.colorbar(im, pad="10%")
        cbar.set_label(u'Wave power (W/m²)', size=5)
        cbar.set_ticks([np.arange(0, 18100, 2000)], update_ticks=True)
        cbar.ax.tick_params(labelsize=5)
        #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        hour = str(name)[9:11]
        day = str(name)[6:8]
        month = str(name)[4:6]
        year = str(name)[0:4]
        plt.title(year + '/' + month, fontsize=5)
        plt.savefig(os.path.join(pathSaveRegional, 'wave_power_subplots_' + year), bbox_inches='tight', dpi=300)
    else:
        b = plt.subplot(4, 3, i-12)
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
        cf = m.contour(x, y, averageMonthly, levels, colors='white', linestyles='solid')
        isobaths_labels = plt.clabel( cf, fmt='%i', colors='white', fontsize=7)
        plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
        im = m.pcolormesh(x, y, averageMonthly, vmin=0, vmax=18100, shading='gouraud')  
        #m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
        #    scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
        cbar = m.colorbar(im, pad="10%")
        cbar.set_label(u'Wave power (W/m²)', size=5)
        cbar.set_ticks([np.arange(0, 18100, 2000)], update_ticks=True)
        cbar.ax.tick_params(labelsize=5)
        hour = str(name)[9:11]
        day = str(name)[6:8]
        month = str(name)[4:6]
        year = str(name)[0:4]
        plt.title(year + '/' + month, fontsize=5)
        plt.savefig(os.path.join(pathSaveRegional, 'wave_power_subplots_' + year), bbox_inches='tight', dpi=300)


