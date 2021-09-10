# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.patches import Polygon, Path

#plt.switch_backend('Qt4Agg')
#plt.switch_backend('agg')

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
import collections



# defining some diretories
resultsDir = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/teste_18'
pathSaveBg = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy/metrics')



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
initialDateVariable = datetime(1990, 1, 1, 0)

# 2017
Summer2017 = datetime(2016, 12, 21, 0)
Autumn2017 = datetime(2017, 3, 21, 0)
Winter2017 = datetime(2017, 6, 21, 0)
Spring2017 = datetime(2017, 9, 21, 0)

# 2018
Summer2018 = datetime(2017, 12, 21, 0)
Autumn2018 = datetime(2018, 3, 21, 0)
Winter2018 = datetime(2018, 6, 21, 0)
Spring2018 = datetime(2018, 9, 21, 0)
Spring2018Final = datetime(2018, 12, 20, 0)

# calculating wave power for each season
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

# calculating average for each season
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

# annual average for 2017 and 2018

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


# Metrics **********************************************************

# **** seasonal variability ****
# ******************************

# 2017 *******
SV_2017 = [averageSazonalOrderedDict["02_Autumn_2017"] - \
                        averageSazonalOrderedDict["01_Summer_2017"]] / average2017Masked

SV_2017_2D = SV_2017[0,:,:]


# 2018 *******
SV_2018 = [averageSazonalOrderedDict["07_Winter_2018"] - \
                        averageSazonalOrderedDict["05_Summer_2018"]] / average2018Masked

SV_2018_2D = SV_2018[0,:,:]


# **** coefficient of variation ****
# **********************************

# 2017
sumPPmTotal2017 = 0
sumPPmTotal2018 = 0
fields2017 = 0
fields2018 = 0

for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if initialDate2017 <= dates <= finalDate2017: # *** all 2017 fields ***
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fields2017 = fields2017 + 1
        waveEnegy2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        numerator2017 = waveEnegy2017.data - average2017Masked.data
        numerator2017Sqrt = numerator2017 ** 2
        sumPPmTotal2017 = sumPPmTotal2017 + numerator2017Sqrt
    elif initialDate2018 <= dates <= finalDate2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fields2018 = fields2018 + 1
        waveEnegy2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        numerator2018 = waveEnegy2018.data - average2018Masked.data
        numerator2018Sqrt = numerator2018 ** 2
        sumPPmTotal2018 = sumPPmTotal2018 + numerator2018Sqrt
    else:
        continue




# 2017
nMinus12017 = fields2017 - 1
divisionSd2017 = np.divide(sumPPmTotal2017.data, nMinus12017)
Sd2017 = np.sqrt(divisionSd2017)
COV2017 = np.divide(Sd2017.data, average2017Masked.data)

# 2018
nMinus12018 = fields2018 - 1
divisionSd2018 = np.divide(sumPPmTotal2018.data, nMinus12018)
Sd2018 = np.sqrt(divisionSd2018)
COV2018 = np.divide(Sd2018.data, average2018Masked.data)





# **************** ************************* *************
# **************** gera e salva imagens SV-2017 *************

font = {'size':8}


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
lvl = np.arange(0.0, 1.62, 0.1)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0, 3)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0',  '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'] #['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, SV_2017_2D, lvl, vmin=0, vmax=1.62)
#im = plt.contour(lon, lat, SV_2017_2D, levels, linewidths=0.5, colors='white', linestyles='solid')
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
cbar.set_ticks([np.arange(0, 1.62, 0.1)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6'])#['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
#cbar.set_label(u'SV index', size=6, rotation=90, labelpad=4) # colorbar label
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('SV index - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'SV_index' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 


# **************** ************************* *************
# **************** gera e salva imagens SV-2018 *************

font = {'size':8}


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
lvl = np.arange(0.0, 1.62, 0.1)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0, 1)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0',  '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'] #['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, SV_2018_2D, lvl, vmin=0, vmax=1.62)
#im = plt.contour(lon, lat, SV_2018_2D, levels, linewidths=0.5, colors='white', linestyles='solid')
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
cbar.set_ticks([np.arange(0, 1.62, 0.1)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6'])#['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
#cbar.set_label(u'SV index', size=6, rotation=90, labelpad=4) # colobar label
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('SV index - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'SV_index' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 



# **************** ************************* *************
# **************** gera e salva imagens COV-2017 *************

font = {'size':8}


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
lvl = np.arange(0.0, 2.1, 0.1)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0, 3)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'] #['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, COV2017, lvl, vmin=0, vmax=2.1)
#im = plt.contour(lon, lat, COV2017, levels, linewidths=0.5, colors='white', linestyles='solid')
fmt = {}
for l, s in zip(im.levels, strs):
    fmt[l] = s
#isobaths_labels = plt.clabel(im, inline=1, inline_spacing=-2.5, fmt=fmt, colors='white', fontsize=4.7)
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
cbar.set_ticks([np.arange(0, 2.1, 0.1)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'])#['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
#cbar.set_label(u'COV index', size=6, rotation=90, labelpad=4) # colorbar label
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('COV - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'COV_' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 



# **************** ************************* *****************
# **************** gera e salva imagens COV-2018 *************

font = {'size':8}


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
lvl = np.arange(0.0, 2.1, 0.1)
#levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
levels = range(0, 3)
#strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
strs = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0',  '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'] #['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
cf = plt.contourf(lon, lat, COV2018, lvl, vmin=0, vmax=2.1)
#im = plt.contour(lon, lat, COV2018, levels, linewidths=0.5, colors='white', linestyles='solid')
fmt = {}
for l, s in zip(im.levels, strs):
    fmt[l] = s
#isobaths_labels = plt.clabel(im, inline=1, inline_spacing=-2.5, fmt=fmt, colors='white', fontsize=4.7)
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
cbar.set_ticks([np.arange(0, 2.1, 0.1)])# update_ticks=True
#cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
cbar.set_ticklabels(['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'])#['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0']) #, '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
#cbar.set_label(u'COV index', size=6, rotation=90, labelpad=4) # colorbar label
cbar.ax.tick_params(labelsize=6)
#plt.rcParams.update({'font.size':4})
plt.gca().set_aspect('equal', adjustable='box')
#plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
plt.title('COV - ' + year, fontsize=6)
plt.rc('font', **font)
ax.set_axisbelow(False) 
plt.savefig(os.path.join(pathSaveBg, 'COV_' + year), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
plt.close() 

