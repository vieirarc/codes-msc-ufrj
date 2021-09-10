# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.patches import Polygon, Path

#plt.switch_backend('Qt4Agg')
plt.switch_backend('agg')

from netCDF4 import Dataset
import numpy as np
import pytz
import scipy.io as sio
from matplotlib.collections import PatchCollection
#from mpl_toolkits.basemap import Basemap, cm
from datetime import date, datetime, timedelta
from intdir2uv import intdir2uv
from tzlocal import get_localzone
import math


# defining some diretories
resultsDir = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/teste_18'
pathSaveBg = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy/annual_average')



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
costaLon = np.genfromtxt('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/swan/lon_bg_mun.txt')
costaLat = np.genfromtxt('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/swan/lat_bg_mun.txt')


sumWaveEnergy2017 = 0
sumWaveEnergy2018 = 0
fields2017 = 0
fields2018 = 0

initialDateVariable = datetime(1990, 1, 1, 0)

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

font = {'size':8}


# **************** ************************* *************
# **************** gera e salva imagens 2017 *************

fig, ax = plt.subplots(figsize=(5.2, 4))

coastline = np.array([costaLon, costaLat])
coastline = np.squeeze(coastline)
coastline = coastline.transpose()

patches  = []

polygon = Polygon(coastline, closed=True)
patches.append(polygon)

collection = PatchCollection(patches, alpha=0.4)

collection.set_color('silver')

ax.add_collection(collection)
collection.set_zorder(3)

name = '20170102_0000'

day = name[6:8]
day = int(day)
month = name[4:6]
month = int(month)
year = name[0:4]
year = int(year)
hour = name[9:11]
hour = int(hour)

infodata=datetime(int(year),int(month),int(day),int(hour), tzinfo=pytz.utc)
print('###############################')
print('Horário UTC  : {0}'.format(infodata.strftime('%Y-%m-%d %H:%M')))
## One of the two lines below could be used if Brazilian Daylight Saving Time
## (dst/Horario de Verao) was not interruped. By the way until python
## libraries are not update I suggest to remove 3 hours from UTC datetime and
## force to localize it

#infodata=infodata.astimezone(get_localzone())
#infodata=infodata.astimezone(pytz.timezone('America/Sao_Paulo'))

infodata = infodata - timedelta(hours=3)
infodata = datetime(infodata.year,
            infodata.month,
            infodata.day,
            infodata.hour,
            tzinfo=pytz.timezone('America/Sao_Paulo'))  

print('Horário Local: {0}'.format(infodata.strftime('%Y-%m-%d %H:%M')))

year=infodata.strftime('%Y')
month=infodata.strftime('%m')
day=infodata.strftime('%d')
hour=infodata.strftime('%H')
#print(year,month,day,hour)
#uEnergyField = uWaveEnergy[index,:,:]
#vEnergyField = vWaveEnergy[index,:,:]
#waveEnegy = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
plt.plot(costaLon, costaLat, 'k', linewidth=0.2, zorder=4)
lvl = np.arange(0, 9100, 500)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0,9100, 1000)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, average2017Masked, lvl, vmin=0, vmax=9100)
im = plt.contour(lon, lat, average2017Masked, levels, linewidths=0.5, colors='white', linestyles='solid')
fmt = {}
for l, s in zip(im.levels, strs):
    fmt[l] = s
isobaths_labels = plt.clabel(im, inline=1, inline_spacing=-2.5, fmt=fmt, colors='white', fontsize=4.7)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=0.8, foreground="k")])
plt.axis([np.min(lon), np.max(lon), np.min(lat), np.max(lat)])

#xF, yF  = (-43.20,  -22.93)
#xB, yB  = (-43.20,  -22.95)
#xC, yC  = (-43.215, -22.97)
xN,  yN  = (-43.08,  -22.90)
xRJ, yRJ = (-43.24,  -22.93)
xDC, yDC = (-43.26,  -22.715)
xMg, yMg = (-43.155, -22.685)
xSG, ySG = (-43.05,  -22.83)
xG,  yG  = (-43.075, -22.672)
xI,  yI  = (-43.035, -22.77)
xMr, yMr = (-43.05,  -22.945)

xlG, ylG   = ([-43.02, -43.04], [-22.69, -22.674])
xlI, ylI   = ([-43.0175, -43.035], [-22.732, -22.765])
xlMr, ylMr = ([-43.015, -43.03], [-22.965, -22.945])

ax.plot(xlG, ylG, 'k', linewidth=0.4, zorder=4)
ax.plot(xlI, ylI, 'k', linewidth=0.4, zorder=4)
ax.plot(xlMr, ylMr, 'k', linewidth=0.4, zorder=4)
   
#ax.text(xF, yF, 'Flamengo', fontsize=6, ha='center', va='center')
#ax.text(xB, yB, 'Botafogo', fontsize=6, ha='center', va='center')
#ax.text(xC, yC, 'Copacabana', fontsize=6, ha='center', va='center')
ax.text(xN, yN, u'Niterói', fontsize=6, ha='center', va='center')
ax.text(xRJ, yRJ, u'Rio de Janeiro', fontsize=6, ha='center', va='center')
ax.text(xDC, yDC, u'Duque\nde\nCaxias', fontsize=6, ha='center', va='center')
ax.text(xMg, yMg, u'Magé', fontsize=6, ha='center', va='center')
ax.text(xSG, ySG, u'São Gonçalo', fontsize=6, ha='center', va='center')
ax.text(xG, yG, u'Guapimirim', fontsize=6, ha='center', va='center')
ax.text(xI, yI, u'Itaboraí', fontsize=6, ha='center', va='center')
ax.text(xMr, yMr, u'Maricá', fontsize=6, ha='center', va='center')

x_labels = np.round(np.arange(-43.3,-42.95, 0.07), 2)
y_labels = np.round(np.arange(-23.09, -22.64, 0.07), 2)
ax.set_xticks(x_labels)
ax.set_xticklabels(x_labels, fontsize=6)
ax.set_yticks(y_labels)
ax.set_yticklabels(y_labels, fontsize=6)
cbar = fig.colorbar(cf, orientation='vertical')
cbar.set_ticks([np.arange(0, 9100, 500)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
cbar.set_label(u'Wave energy (kW/m)', size=6, rotation=90, labelpad=4)
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('Average Wave Energy - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'average_wave_energy_' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 



# **************** gera e salva imagens 2018 **************

fig, ax = plt.subplots(figsize=(5.2, 4))

coastline = np.array([costaLon, costaLat])
coastline = np.squeeze(coastline)
coastline = coastline.transpose()

patches  = []

polygon = Polygon(coastline, closed=True)
patches.append(polygon)

collection = PatchCollection(patches, alpha=0.4)

collection.set_color('silver')

ax.add_collection(collection)
collection.set_zorder(3)

name = '20180102_0000'

day = name[6:8]
day = int(day)
month = name[4:6]
month = int(month)
year = name[0:4]
year = int(year)
hour = name[9:11]
hour = int(hour)

infodata=datetime(int(year),int(month),int(day),int(hour), tzinfo=pytz.utc)
print('###############################')
print('Horário UTC  : {0}'.format(infodata.strftime('%Y-%m-%d %H:%M')))
## One of the two lines below could be used if Brazilian Daylight Saving Time
## (dst/Horario de Verao) was not interruped. By the way until python
## libraries are not update I suggest to remove 3 hours from UTC datetime and
## force to localize it

#infodata=infodata.astimezone(get_localzone())
#infodata=infodata.astimezone(pytz.timezone('America/Sao_Paulo'))

infodata = infodata - timedelta(hours=3)
infodata = datetime(infodata.year,
            infodata.month,
            infodata.day,
            infodata.hour,
            tzinfo=pytz.timezone('America/Sao_Paulo'))  

print('Horário Local: {0}'.format(infodata.strftime('%Y-%m-%d %H:%M')))

year=infodata.strftime('%Y')
month=infodata.strftime('%m')
day=infodata.strftime('%d')
hour=infodata.strftime('%H')
#print(year,month,day,hour)
#uEnergyField = uWaveEnergy[index,:,:]
#vEnergyField = vWaveEnergy[index,:,:]
#waveEnegy = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
plt.plot(costaLon, costaLat, 'k', linewidth=0.2, zorder=4)
lvl = np.arange(0, 9100, 500)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0, 9100, 1000)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, average2018Masked, lvl, vmin=0, vmax=9100)
im = plt.contour(lon, lat, average2018Masked, levels, linewidths=0.5, colors='white', linestyles='solid')
fmt = {}
for l, s in zip(im.levels, strs):
    fmt[l] = s
isobaths_labels = plt.clabel(im, inline=1, inline_spacing=-2.5, fmt=fmt, colors='white', fontsize=4.0)
plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=0.8, foreground="k")])
plt.axis([np.min(lon), np.max(lon), np.min(lat), np.max(lat)])

#xF, yF  = (-43.20,  -22.93)
#xB, yB  = (-43.20,  -22.95)
#xC, yC  = (-43.215, -22.97)
xN,  yN  = (-43.08,  -22.90)
xRJ, yRJ = (-43.24,  -22.93)
xDC, yDC = (-43.26,  -22.715)
xMg, yMg = (-43.155, -22.685)
xSG, ySG = (-43.05,  -22.83)
xG,  yG  = (-43.075, -22.672)
xI,  yI  = (-43.035, -22.77)
xMr, yMr = (-43.05,  -22.945)

xlG, ylG   = ([-43.02, -43.04], [-22.69, -22.674])
xlI, ylI   = ([-43.0175, -43.035], [-22.732, -22.765])
xlMr, ylMr = ([-43.015, -43.03], [-22.965, -22.945])

ax.plot(xlG, ylG, 'k', linewidth=0.4, zorder=4)
ax.plot(xlI, ylI, 'k', linewidth=0.4, zorder=4)
ax.plot(xlMr, ylMr, 'k', linewidth=0.4, zorder=4)
   
#ax.text(xF, yF, 'Flamengo', fontsize=6, ha='center', va='center')
#ax.text(xB, yB, 'Botafogo', fontsize=6, ha='center', va='center')
#ax.text(xC, yC, 'Copacabana', fontsize=6, ha='center', va='center')
ax.text(xN, yN, u'Niterói', fontsize=6, ha='center', va='center')
ax.text(xRJ, yRJ, u'Rio de Janeiro', fontsize=6, ha='center', va='center')
ax.text(xDC, yDC, u'Duque\nde\nCaxias', fontsize=6, ha='center', va='center')
ax.text(xMg, yMg, u'Magé', fontsize=6, ha='center', va='center')
ax.text(xSG, ySG, u'São Gonçalo', fontsize=6, ha='center', va='center')
ax.text(xG, yG, u'Guapimirim', fontsize=6, ha='center', va='center')
ax.text(xI, yI, u'Itaboraí', fontsize=6, ha='center', va='center')
ax.text(xMr, yMr, u'Maricá', fontsize=6, ha='center', va='center')

x_labels = np.round(np.arange(-43.3,-42.95, 0.07), 2)
y_labels = np.round(np.arange(-23.09, -22.64, 0.07), 2)
ax.set_xticks(x_labels)
ax.set_xticklabels(x_labels, fontsize=6)
ax.set_yticks(y_labels)
ax.set_yticklabels(y_labels, fontsize=6)
cbar = fig.colorbar(cf, orientation='vertical')
cbar.set_ticks([np.arange(0, 9100, 500)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
cbar.set_label(u'Wave energy (kW/m)', size=6, rotation=90, labelpad=4)
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('Average Wave Energy - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'average_wave_energy_' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 


