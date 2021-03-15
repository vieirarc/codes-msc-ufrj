# -*- coding: UTF-8 -*-
from __future__ import division
import os
import collections
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


# defining some diretories
resultsDir = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1'
pathSave = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy')



averageDict = {}

# open files and get variables
datasetEnergy = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_transp_energy.nc')
time = datasetEnergy['time']
uWaveEnergy = datasetEnergy['u_component_energy_transp']
vWaveEnergy = datasetEnergy['v_component_energy_transp']
time = datasetEnergy['time']
lats = datasetEnergy['latitude'][:]
lons = datasetEnergy['longitude'][:]
lon, lat = np.meshgrid(lons, lats)
coastline = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/coastline_bg.mat')
costaLat = coastline['lat']
costaLon = coastline['lon']

# counters
# 2017
sumWaveEnergySummer2017 = 0
fieldsSummer2017 = 0

sumWaveEnergyAutumn2017 = 0
fieldsAutumn2017 = 0

sumWaveEnergyWinter2017 = 0
fieldsWinter2017 = 0

sumWaveEnergySpring2017 = 0
fieldsSpring2017 = 0


# 2018 *****************
sumWaveEnergySummer2018 = 0
fieldsSummer2018 = 0

sumWaveEnergyAutumn2018 = 0
fieldsAutumn2018 = 0

sumWaveEnergyWinter2018 = 0
fieldsWinter2018 = 0

sumWaveEnergySpring2018 = 0
fieldsSpring2018 = 0


# defining dates
# initial date according ww3 results
initialDateVariable = datetime(1990, 01, 01, 00)

# 2017
Summer2017 = datetime(2016, 12, 21, 00)
Autumn2017 = datetime(2017, 3, 21, 00)
Winter2017 = datetime(2017, 6, 21, 00)
Spring2017 = datetime(2017, 9, 21, 00)

# 2018
Summer2018 = datetime(2017, 12, 21, 00)
Autumn2018 = datetime(2018, 3, 21, 00)
Winter2018 = datetime(2018, 6, 21, 00)
Spring2018 = datetime(2018, 9, 21, 00)
Spring2018Final = datetime(2018, 12, 20, 00)

# calculating wave power for each month
for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if Summer2017 <= dates < Autumn2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSummer2017 = fieldsSummer2017 + 1
        waveEnergySummer2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySummer2017 = sumWaveEnergySummer2017 + waveEnergySummer2017
    elif Autumn2017 <= dates < Winter2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsAutumn2017 = fieldsAutumn2017 + 1
        waveEnergyAutumn2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyAutumn2017 = sumWaveEnergyAutumn2017 + waveEnergyAutumn2017
    elif Winter2017 <= dates < Spring2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsWinter2017 = fieldsWinter2017 + 1
        waveEnergyWinter2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyWinter2017 = sumWaveEnergyWinter2017 + waveEnergyWinter2017
    elif Spring2017 <= dates < Summer2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSpring2017 = fieldsSpring2017 + 1
        waveEnergySpring2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySpring2017 = sumWaveEnergySpring2017 + waveEnergySpring2017
    elif Summer2018 <= dates < Autumn2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSummer2018 = fieldsSummer2018 + 1
        waveEnergySummer2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySummer2018 = sumWaveEnergySummer2018 + waveEnergySummer2018
    elif Autumn2018 <= dates < Winter2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsAutumn2018 = fieldsAutumn2018 + 1
        waveEnergyAutumn2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyAutumn2018 = sumWaveEnergyAutumn2018 + waveEnergyAutumn2018
    elif Winter2018 <= dates < Spring2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsWinter2018 = fieldsWinter2018 + 1
        waveEnergyWinter2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyWinter2018 = sumWaveEnergyWinter2018 + waveEnergyWinter2018
    elif Spring2018 <= dates < Spring2018Final:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSpring2018 = fieldsSpring2018 + 1
        waveEnergySpring2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySpring2018 = sumWaveEnergySpring2018 + waveEnergySpring2018
    else:
        continue

# calculating average for each month
# 2017

averageSazonalDict = {}

averageSummer2017 = sumWaveEnergySummer2017 / fieldsSummer2017
averageSummer2017Masked = np.ma.masked_where(averageSummer2017 == 0, averageSummer2017)
averageSazonalDict["01_Summer_2017"] = averageSummer2017Masked

averageAutumn2017 = sumWaveEnergyAutumn2017 / fieldsAutumn2017
averageAutumn2017Masked = np.ma.masked_where(averageAutumn2017 == 0, averageAutumn2017)
averageSazonalDict["02_Autumn_2017"] = averageAutumn2017Masked

averageWinter2017 = sumWaveEnergyWinter2017 / fieldsWinter2017
averageWinter2017Masked = np.ma.masked_where(averageWinter2017 == 0, averageWinter2017)
averageSazonalDict["03_Winter_2017"] = averageWinter2017Masked

averageSpring2017 = sumWaveEnergySpring2017 / fieldsSpring2017
averageSpring2017Masked = np.ma.masked_where(averageSpring2017 == 0, averageSpring2017)
averageSazonalDict["04_Spring_2017"] = averageSpring2017Masked

averageSummer2018 = sumWaveEnergySummer2018 / fieldsSummer2018
averageSummer2018Masked = np.ma.masked_where(averageSummer2018 == 0, averageSummer2018)
averageSazonalDict["05_Summer_2018"] = averageSummer2018Masked

averageAutumn2018 = sumWaveEnergyAutumn2018 / fieldsAutumn2018
averageAutumn2018Masked = np.ma.masked_where(averageAutumn2018 == 0, averageAutumn2018)
averageSazonalDict["06_Autumn_2018"] = averageAutumn2018Masked

averageWinter2018 = sumWaveEnergyWinter2018 / fieldsWinter2018
averageWinter2018Masked = np.ma.masked_where(averageWinter2018 == 0, averageWinter2018)
averageSazonalDict["07_Winter_2018"] = averageWinter2018Masked

averageSpring2018 = sumWaveEnergySpring2018 / fieldsSpring2018
averageSpring2018Masked = np.ma.masked_where(averageSpring2018 == 0, averageSpring2018)
averageSazonalDict["08_Spring_2018"] = averageSpring2018Masked


averageSazonalOrderedDict = collections.OrderedDict(sorted(averageSazonalDict.items()))


    # ************************* creating imagens ****************************************
for k, v in averageSazonalOrderedDict.items():
    fig, ax = plt.subplots()
    plt.plot(costaLon, costaLat, 'k')
    lvl = np.arange(0, 9100, 1000)
    levels= [1000, 2000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000]
    # levels= [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    cf = plt.contourf(lon, lat, v, lvl, vmin=0, vmax=9100, shading='gouraud')
    im = plt.contour(lon, lat, v, levels, colors='white', linestyles='solid')
    isobaths_labels = plt.clabel(im, fmt='%i', colors='white', fontsize=7)
    plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
    plt.plot(-43.185, -22.950, 'ro',markersize=1.9, color='k')
    plt.text(-43.208, -22.960, 'Rio de Janeiro', fontsize=7)
    plt.plot(-43.095, -22.940, 'ro',markersize=1.9, color='k')
    plt.text(-43.090, -22.945, u'Niterói', fontsize=7)
    plt.text(-43.135, -23.070, u'Ilha Rasa', fontsize=7)
    cbar = fig.colorbar(cf, orientation='vertical')
    cbar.set_label(u'Wave Power (W/m)', size=10, rotation=90, labelpad=4)
    cbar.set_ticks([np.arange(0, 9100, 1000)], update_ticks=True)
    cbar.ax.tick_params(labelsize=8)
    plt.rcParams.update({'font.size': 7})
    #hour = str(k)[9:11]
    #day = str(k)[6:8]
    month = str(k)[0:3]
    monthNumber = str(k)[0:2]
    year = str(k)[10::]
    season = str(k)[3:9]
    plt.title('Sazonal average of Wave Power - ' + season + ' ' + year, fontsize=10)
    plt.savefig(os.path.join(pathSave, monthNumber + '_' + season + year), bbox_inches='tight', dpi=400)


