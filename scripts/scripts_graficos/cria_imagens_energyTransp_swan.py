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
fig = plt.figure(figsize=(8, 12))



# ***** looping through files in folder *****
for i, filename in enumerate(energyNamesList):
    # Pastas e arquivo
    datasetEnergy = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/' + filename)
    pathSave = (resultsDir + '/swan-BG/imagens/wave_energy')
    uWaveEnergy = datasetEnergy['u_component_energy_transp']
    vWaveEnergy = datasetEnergy['v_component_energy_transp']
    time = datasetEnergy['time']
    lats = datasetEnergy['latitude'][:]
    lons = datasetEnergy['longitude'][:]
    lon, lat = np.meshgrid(lons, lats)
    # create listField related to time variable
    # inicial date according to file results
    listField = []
    initialDate = datetime(1990, 01, 01, 00)
    for j in time:
        dates = initialDate + timedelta(days=np.float64(j))
        datesString = dates.strftime("%Y%m%d_%H%M%S")
        listField.append(datesString)
    # sort lists elements in crescent order
    listField.sort()
    sumWaveEnergy = 0
    # calculating wave power and monthly average
    for index, name in enumerate(listField): # monthly block
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        waveEnegy = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergy = sumWaveEnergy + waveEnegy 
    averageMonthly = sumWaveEnergy / len(listField)
    averageMonthlyMasked = np.ma.masked_where(averageMonthly == 0, averageMonthly)
    # ************************* creating imagens ****************************************
    fig, ax = plt.subplots()
    plt.plot(costaLon, costaLat, 'k')
    lvl = np.arange(0, 12100, 1000)
    levels= [1000, 2000,4000, 5000, 7000, 8000, 9000, 10000, 12000]
    # levels= [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    cf = plt.contourf(lon, lat, averageMonthlyMasked, lvl, vmin=0, vmax=12100, shading='gouraud')
    im = plt.contour(lon, lat, averageMonthlyMasked, levels, colors='white', linestyles='solid')
    isobaths_labels = plt.clabel(im, fmt='%i', colors='white', fontsize=7)
    plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
    plt.plot(-43.185, -22.950, 'ro',markersize=1.9, color='k')
    plt.text(-43.208, -22.960, 'Rio de Janeiro', fontsize=7)
    plt.plot(-43.095, -22.940, 'ro',markersize=1.9, color='k')
    plt.text(-43.090, -22.945, u'Niterói', fontsize=7)
    plt.text(-43.135, -23.070, u'Ilha Rasa', fontsize=7, color='black')
    cbar = fig.colorbar(cf, orientation='vertical')
    cbar.set_label(u'Wave power (W/m)', size=10, rotation=90, labelpad=4)
    cbar.set_ticks([np.arange(0, 12100, 1000)], update_ticks=True)
    cbar.ax.tick_params(labelsize=8)
    plt.rcParams.update({'font.size': 7})
    hour = str(name)[9:11]
    day = str(name)[6:8]
    month = str(name)[4:6]
    year = str(name)[0:4]
    plt.title('Monthly average of Wave Power ' + year + '/' + month, fontsize=10)
    plt.savefig(os.path.join(pathSave, year + month), bbox_inches='tight', dpi=400)


