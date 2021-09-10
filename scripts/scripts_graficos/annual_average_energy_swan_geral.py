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


# defining some diretories
resultsDir = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/teste_18'
pathSave = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy/annual_average/')



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
coastline = sio.loadmat('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/swan/coastline_bg.mat')
costaLat = coastline['lat']
costaLon = coastline['lon']


sumWaveEnergy2017 = 0
sumWaveEnergy2018 = 0
fields2017 = 0
fields2018 = 0

initialDateVariable = datetime(1990,1,1,0)

initialDate2017 = datetime(2017, 1, 1, 0)
finalDate2017 = datetime(2017, 12, 31, 22)

initialDate2018 = datetime(2018, 1, 1, 0)
finalDate2018 = datetime(2018, 12, 31, 22)

for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if initialDate2017 <= dates <= finalDate2017: # *** 2017 ***
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fields2017 = fields2017 + 1
        waveEnegy2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergy2017 = sumWaveEnergy2017 + waveEnegy2017
    elif initialDate2018 <= dates <= finalDate2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fields2018 = fields2018 + 1
        waveEnegy2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergy2018 = sumWaveEnergy2018 + waveEnegy2018
    else:
        continue


averageMonthly2017 = sumWaveEnergy2017 / fields2017
averageMonthly2018 = sumWaveEnergy2018 / fields2018

average2017Masked = np.ma.masked_where(averageMonthly2017 == 0, averageMonthly2017)
average2018Masked = np.ma.masked_where(averageMonthly2018 == 0, averageMonthly2018)

# *************** 2017 ************
fig, ax = plt.subplots()
plt.plot(costaLon, costaLat, 'k')
lvl = np.arange(0, 6600, 500)
#levels= [1000, 2000,4000, 8000, 9000, 10000, 12000]
levels= [1000, 2000, 3000, 4000, 5000, 6000]
cf = plt.contourf(lon, lat, average2017Masked, lvl, vmin=0, vmax=6600, shading='gouraud')
im = plt.contour(lon, lat, average2017Masked, levels, colors='white', linestyles='solid')
isobaths_labels = plt.clabel(im, fmt='%i', colors='white', fontsize=7)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
plt.plot(-43.185, -22.950, 'ro',markersize=1.9, color='k')
plt.text(-43.208, -22.960, 'Rio de Janeiro', fontsize=7)
plt.plot(-43.095, -22.940, 'ro',markersize=1.9, color='k')
plt.text(-43.090, -22.945, u'Niterói', fontsize=7)
plt.text(-43.135, -23.070, u'Ilha Rasa', fontsize=7)
cbar = fig.colorbar(cf, orientation='vertical')
cbar.set_label(u'Wave Power (W/m)', size=10, rotation=90, labelpad=4)
cbar.set_ticks([np.arange(0, 6600, 500)], update_ticks=True)
cbar.ax.tick_params(labelsize=8)
plt.rcParams.update({'font.size': 7})
hour = initialDate2017.hour
day = initialDate2017.day
month = initialDate2017.month
year = initialDate2017.year
plt.title('Annual average of Wave Power - 2017', fontsize=10)
plt.savefig(os.path.join(pathSave, 'annual_average_2017'), bbox_inches='tight', dpi=400)


# *************** 2018 ************
fig, ax = plt.subplots()
plt.plot(costaLon, costaLat, 'k')
lvl = np.arange(0, 6600, 500)
#levels= [1000, 2000,4000, 8000, 9000, 10000, 12000]
levels= [1000, 2000, 3000, 4000, 5000, 6000]
cf = plt.contourf(lon, lat, average2018Masked, lvl, vmin=0, vmax=6600, shading='gouraud')
im = plt.contour(lon, lat, average2018Masked, levels, colors='white', linestyles='solid')
isobaths_labels = plt.clabel(im, fmt='%i', colors='white', fontsize=7)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.4, foreground="k")])
plt.plot(-43.185, -22.950, 'ro',markersize=1.9, color='k')
plt.text(-43.208, -22.960, 'Rio de Janeiro', fontsize=7)
plt.plot(-43.095, -22.940, 'ro',markersize=1.9, color='k')
plt.text(-43.090, -22.945, u'Niterói', fontsize=7)
plt.text(-43.135, -23.070, u'Ilha Rasa', fontsize=7)
cbar = fig.colorbar(cf, orientation='vertical')
cbar.set_label(u'Wave Power (W/m)', size=10, rotation=90, labelpad=4)
cbar.set_ticks([np.arange(0, 6600, 500)], update_ticks=True)
cbar.ax.tick_params(labelsize=8)
plt.rcParams.update({'font.size': 7})
hour = initialDate2018.hour
day = initialDate2018.day
month = initialDate2018.month
year = initialDate2018.year
plt.title('Annual average of Wave Power - 2018', fontsize=10)
plt.savefig(os.path.join(pathSave, 'annual_average_2018'), bbox_inches='tight', dpi=400)
