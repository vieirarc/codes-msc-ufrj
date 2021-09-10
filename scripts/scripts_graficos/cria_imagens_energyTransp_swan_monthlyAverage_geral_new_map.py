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
pathSaveBg = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy/monthly_average')



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
sumWaveEnergyJan2017 = 0
fieldsJan2017 = 0

sumWaveEnergyFeb2017 = 0
fieldsFeb2017 = 0

sumWaveEnergyMar2017 = 0
fieldsMar2017 = 0

sumWaveEnergyApr2017 = 0
fieldsApr2017 = 0

sumWaveEnergyMay2017 = 0
fieldsMay2017 = 0

sumWaveEnergyJun2017 = 0
fieldsJun2017 = 0

sumWaveEnergyJul2017 = 0
fieldsJul2017 = 0

sumWaveEnergyAug2017 = 0
fieldsAug2017 = 0

sumWaveEnergySep2017 = 0
fieldsSep2017 = 0

sumWaveEnergyOct2017 = 0
fieldsOct2017 = 0

sumWaveEnergyNov2017 = 0
fieldsNov2017 = 0

sumWaveEnergyDec2017 = 0
fieldsDec2017 = 0

# 2018 *****************
sumWaveEnergyJan2018 = 0
fieldsJan2018 = 0

sumWaveEnergyFeb2018 = 0
fieldsFeb2018 = 0

sumWaveEnergyMar2018 = 0
fieldsMar2018 = 0

sumWaveEnergyApr2018 = 0
fieldsApr2018 = 0

sumWaveEnergyMay2018 = 0
fieldsMay2018 = 0

sumWaveEnergyJun2018 = 0
fieldsJun2018 = 0

sumWaveEnergyJul2018 = 0
fieldsJul2018 = 0

sumWaveEnergyAug2018 = 0
fieldsAug2018 = 0

sumWaveEnergySep2018 = 0
fieldsSep2018 = 0

sumWaveEnergyOct2018 = 0
fieldsOct2018 = 0

sumWaveEnergyNov2018 = 0
fieldsNov2018 = 0

sumWaveEnergyDec2018 = 0
fieldsDec2018 = 0
 
# defining dates
# initial date according ww3 results
initialDateVariable = datetime(1990, 1, 1, 0)

# 2017
jan2017 = datetime(2017, 1, 1, 0)
feb2017 = datetime(2017, 2, 1, 0)
mar2017 = datetime(2017, 3, 1, 0)
apr2017 = datetime(2017, 4, 1, 0)
may2017 = datetime(2017, 5, 1, 0)
jun2017 = datetime(2017, 6, 1, 0)
jul2017 = datetime(2017, 7, 1, 0)
aug2017 = datetime(2017, 8, 1, 0)
sep2017 = datetime(2017, 9, 1, 0)
oct2017 = datetime(2017, 10, 1, 0)
nov2017 = datetime(2017, 11, 1, 0)
dec2017 = datetime(2017, 12, 1, 0)

# 2018
jan2018 = datetime(2018, 1, 1, 0)
feb2018 = datetime(2018, 2, 1, 0)
mar2018 = datetime(2018, 3, 1, 0)
apr2018 = datetime(2018, 4, 1, 0)
may2018 = datetime(2018, 5, 1, 0)
jun2018 = datetime(2018, 6, 1, 0)
jul2018 = datetime(2018, 7, 1, 0)
aug2018 = datetime(2018, 8, 1, 0)
sep2018 = datetime(2018, 9, 1, 0)
oct2018 = datetime(2018, 10, 1, 0)
nov2018 = datetime(2018, 11, 1, 0)
dec2018 = datetime(2018, 12, 1, 0)

# calculating wave power for each month
for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if jan2017 <= dates < feb2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJan2017 = fieldsJan2017 + 1
        waveEnegyJan2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJan2017 = sumWaveEnergyJan2017 + waveEnegyJan2017
    elif feb2017 <= dates < mar2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsFeb2017 = fieldsFeb2017 + 1
        waveEnegyfeb2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyFeb2017 = sumWaveEnergyFeb2017 + waveEnegyfeb2017
    elif mar2017 <= dates < apr2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsMar2017 = fieldsMar2017 + 1
        waveEnegymar2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyMar2017 = sumWaveEnergyMar2017 + waveEnegymar2017
    elif apr2017 <= dates < may2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsApr2017 = fieldsApr2017 + 1
        waveEnegyapr2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyApr2017 = sumWaveEnergyApr2017 + waveEnegyapr2017
    elif may2017 <= dates < jun2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsMay2017 = fieldsMay2017 + 1
        waveEnegymay2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyMay2017 = sumWaveEnergyMay2017 + waveEnegymay2017
    elif jun2017 <= dates < jul2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJun2017 = fieldsJun2017 + 1
        waveEnegyjun2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJun2017 = sumWaveEnergyJun2017 + waveEnegyjun2017
    elif jul2017 <= dates < aug2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJul2017 = fieldsJul2017 + 1
        waveEnegyjul2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJul2017 = sumWaveEnergyJul2017 + waveEnegyjul2017
    elif aug2017 <= dates < sep2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsAug2017 = fieldsAug2017 + 1
        waveEnegyaug2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyAug2017 = sumWaveEnergyAug2017 + waveEnegyaug2017
    elif sep2017 <= dates < oct2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSep2017 = fieldsSep2017 + 1
        waveEnegysep2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySep2017 = sumWaveEnergySep2017 + waveEnegysep2017
    elif oct2017 <= dates < nov2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsOct2017 = fieldsOct2017 + 1
        waveEnegyoct2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyOct2017 = sumWaveEnergyOct2017 + waveEnegyoct2017
    elif nov2017 <= dates < dec2017:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsNov2017 = fieldsNov2017 + 1
        waveEnegynov2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyNov2017 = sumWaveEnergyNov2017 + waveEnegynov2017
    elif dec2017 <= dates < jan2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsDec2017 = fieldsDec2017 + 1
        waveEnegydec2017 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyDec2017 = sumWaveEnergyDec2017 + waveEnegydec2017
    elif jan2018 <= dates < feb2018: # *************************************************************
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJan2018 = fieldsJan2018 + 1
        waveEnegyJan2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJan2018 = sumWaveEnergyJan2018 + waveEnegyJan2018
    elif feb2018 <= dates < mar2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsFeb2018 = fieldsFeb2018 + 1
        waveEnegyfeb2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyFeb2018 = sumWaveEnergyFeb2018 + waveEnegyfeb2018
    elif mar2018 <= dates < apr2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsMar2018 = fieldsMar2018 + 1
        waveEnegymar2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyMar2018 = sumWaveEnergyMar2018 + waveEnegymar2018
    elif apr2018 <= dates < may2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsApr2018 = fieldsApr2018 + 1
        waveEnegyapr2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyApr2018 = sumWaveEnergyApr2018 + waveEnegyapr2018
    elif may2018 <= dates < jun2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsMay2018 = fieldsMay2018 + 1
        waveEnegymay2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyMay2018 = sumWaveEnergyMay2018 + waveEnegymay2018
    elif jun2018 <= dates < jul2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJun2018 = fieldsJun2018 + 1
        waveEnegyjun2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJun2018 = sumWaveEnergyJun2018 + waveEnegyjun2018
    elif jul2018 <= dates < aug2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsJul2018 = fieldsJul2018 + 1
        waveEnegyjul2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyJul2018 = sumWaveEnergyJul2018 + waveEnegyjul2018
    elif aug2018 <= dates < sep2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsAug2018 = fieldsAug2018 + 1
        waveEnegyaug2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyAug2018 = sumWaveEnergyAug2018 + waveEnegyaug2018
    elif sep2018 <= dates < oct2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsSep2018 = fieldsSep2018 + 1
        waveEnegysep2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergySep2018 = sumWaveEnergySep2018 + waveEnegysep2018
    elif oct2018 <= dates < nov2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsOct2018 = fieldsOct2018 + 1
        waveEnegyoct2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyOct2018 = sumWaveEnergyOct2018 + waveEnegyoct2018
    elif nov2018 <= dates < dec2018:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsNov2018 = fieldsNov2018 + 1
        waveEnegynov2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyNov2018 = sumWaveEnergyNov2018 + waveEnegynov2018
    elif dec2018 <= dates:
        uEnergyField = uWaveEnergy[index,:,:]
        vEnergyField = vWaveEnergy[index,:,:]
        fieldsDec2018 = fieldsDec2018 + 1
        waveEnegydec2018 = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
        sumWaveEnergyDec2018 = sumWaveEnergyDec2018 + waveEnegydec2018
    else:
        continue

# calculating average for each month
# 2017

averageMonthlyDict = {}

averageJan2017 = sumWaveEnergyJan2017 / fieldsJan2017
averageJan2017Masked = np.ma.masked_where(averageJan2017 == 0, averageJan2017)
averageMonthlyDict["Jan_01_2017"] = averageJan2017Masked

averageFeb2017 = sumWaveEnergyFeb2017 / fieldsFeb2017
averageFeb2017Masked = np.ma.masked_where(averageFeb2017 == 0, averageFeb2017)
averageMonthlyDict["Feb_02_2017"] = averageFeb2017Masked

averageMar2017 = sumWaveEnergyMar2017 / fieldsMar2017
averageMar2017Masked = np.ma.masked_where(averageMar2017 == 0, averageMar2017)
averageMonthlyDict["Mar_03_2017"] = averageMar2017Masked

averageApr2017 = sumWaveEnergyApr2017 / fieldsApr2017
averageApr2017Masked = np.ma.masked_where(averageApr2017 == 0, averageApr2017)
averageMonthlyDict["Apr_04_2017"] = averageApr2017Masked

averageMay2017 = sumWaveEnergyMay2017 / fieldsMay2017
averageMay2017Masked = np.ma.masked_where(averageMay2017 == 0, averageMay2017)
averageMonthlyDict["May_05_2017"] = averageMay2017Masked

averageJun2017 = sumWaveEnergyJun2017 / fieldsJun2017
averageJun2017Masked = np.ma.masked_where(averageJun2017 == 0, averageJun2017)
averageMonthlyDict["Jun_06_2017"] = averageJun2017Masked

averageJul2017 = sumWaveEnergyJul2017 / fieldsJul2017
averageJul2017Masked = np.ma.masked_where(averageJul2017 == 0, averageJul2017)
averageMonthlyDict["Jul_07_2017"] = averageJul2017Masked

averageAug2017 = sumWaveEnergyAug2017 / fieldsAug2017
averageAug2017Masked = np.ma.masked_where(averageAug2017 == 0, averageAug2017)
averageMonthlyDict["Aug_08_2017"] = averageAug2017Masked

averageSep2017 = sumWaveEnergySep2017 / fieldsSep2017
averageSep2017Masked = np.ma.masked_where(averageSep2017 == 0, averageSep2017)
averageMonthlyDict["Sep_09_2017"] = averageSep2017Masked

averageOct2017 = sumWaveEnergyOct2017 / fieldsOct2017
averageOct2017Masked = np.ma.masked_where(averageOct2017 == 0, averageOct2017)
averageMonthlyDict["Oct_10_2017"] = averageOct2017Masked

averageNov2017 = sumWaveEnergyNov2017 / fieldsNov2017
averageNov2017Masked = np.ma.masked_where(averageNov2017 == 0, averageNov2017)
averageMonthlyDict["Nov_11_2017"] = averageNov2017Masked

averageDec2017 = sumWaveEnergyDec2017 / fieldsDec2017
averageDec2017Masked = np.ma.masked_where(averageDec2017 == 0, averageDec2017)
averageMonthlyDict["Dec_12_2017"] = averageDec2017Masked

# 2018 ***********************************************************************
averageJan2018 = sumWaveEnergyJan2018 / fieldsJan2018
averageJan2018Masked = np.ma.masked_where(averageJan2018 == 0, averageJan2018)
averageMonthlyDict["Jan_01_2018"] = averageJan2018Masked

averageFeb2018 = sumWaveEnergyFeb2018 / fieldsFeb2018
averageFeb2018Masked = np.ma.masked_where(averageFeb2018 == 0, averageFeb2018)
averageMonthlyDict["Feb_02_2018"] = averageFeb2018Masked

averageMar2018 = sumWaveEnergyMar2018 / fieldsMar2018
averageMar2018Masked = np.ma.masked_where(averageMar2018 == 0, averageMar2018)
averageMonthlyDict["Mar_03_2018"] = averageMar2018Masked

averageApr2018 = sumWaveEnergyApr2018 / fieldsApr2018
averageApr2018Masked = np.ma.masked_where(averageApr2018 == 0, averageApr2018)
averageMonthlyDict["Apr_04_2018"] = averageApr2018Masked

averageMay2018 = sumWaveEnergyMay2018 / fieldsMay2018
averageMay2018Masked = np.ma.masked_where(averageMay2018 == 0, averageMay2018)
averageMonthlyDict["May_05_2018"] = averageMay2018Masked

averageJun2018 = sumWaveEnergyJun2018 / fieldsJun2018
averageJun2018Masked = np.ma.masked_where(averageJun2018 == 0, averageJun2018)
averageMonthlyDict["Jun_06_2018"] = averageJun2018Masked

averageJul2018 = sumWaveEnergyJul2018 / fieldsJul2018
averageJul2018Masked = np.ma.masked_where(averageJul2018 == 0, averageJul2018)
averageMonthlyDict["Jul_07_2018"] = averageJul2018Masked

averageAug2018 = sumWaveEnergyAug2018 / fieldsAug2018
averageAug2018Masked = np.ma.masked_where(averageAug2018 == 0, averageAug2018)
averageMonthlyDict["Aug_08_2018"] = averageAug2018Masked

averageSep2018 = sumWaveEnergySep2018 / fieldsSep2018
averageSep2018Masked = np.ma.masked_where(averageSep2018 == 0, averageSep2018)
averageMonthlyDict["Sep_09_2018"] = averageSep2018Masked

averageOct2018 = sumWaveEnergyOct2018 / fieldsOct2018
averageOct2018Masked = np.ma.masked_where(averageOct2018 == 0, averageOct2018)
averageMonthlyDict["Oct_10_2018"] = averageOct2018Masked

averageNov2018 = sumWaveEnergyNov2018 / fieldsNov2018
averageNov2018Masked = np.ma.masked_where(averageNov2018 == 0, averageNov2018)
averageMonthlyDict["Nov_11_2018"] = averageNov2018Masked

averageDec2018 = sumWaveEnergyDec2018 / fieldsDec2018
averageDec2018Masked = np.ma.masked_where(averageDec2018 == 0, averageDec2018)
averageMonthlyDict["Dec_12_2018"] = averageDec2018Masked


# **************** ************************* *************
# **************** gera e salva imagens **** *************


font = {'size':8}

for k, v in averageMonthlyDict.items():
    fig, ax = plt.subplots(figsize=(5.2, 4))

    coastline = np.array([costaLon, costaLat])
    coastline = np.squeeze(coastline)
    coastline = coastline.transpose()

    patches  = []

    polygon = Polygon(coastline, closed=True)
    patches.append(polygon)

    collection = PatchCollection(patches)

    collection.set_color('silver')

    ax.add_collection(collection)
    collection.set_zorder(3)


    day = '02' # whatever!
    day = int(day)
    month = k[4:6]
    month = int(month)
    year = k[7::]
    year = int(year)
    hour = '00'
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
    lvl = np.arange(0, 14100, 1000)
    #levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
    levels = range(0,14100, 1000)
    #strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0'] #, '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
    strs = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0']
    cf = plt.contourf(lon, lat, v, lvl, vmin=0, vmax=13100)
    im = plt.contour(lon, lat, v, levels, linewidths=0.5, colors='white', linestyles='solid')
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
    cbar.set_ticks([np.arange(0, 14100, 1000)])# update_ticks=True
    #cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
    cbar.set_ticklabels(['0.0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0']) #, '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
    cbar.set_label(u'Wave energy (kW/m)', size=6, rotation=90, labelpad=4)
    cbar.ax.tick_params(labelsize=6)
    #plt.rcParams.update({'font.size':4})
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
    monthStr = k[0:3]
    plt.title('Average Wave Energy - ' + monthStr + ' ' + year, fontsize=6)
    plt.rc('font', **font)
    ax.set_axisbelow(False)
    if year == '2018':
        month2018 = int(month) + 12
        plt.savefig(os.path.join(pathSaveBg, str(month2018) + '_monthly_average_wave_energy_' + year + month), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
        plt.close()
    else:
        plt.savefig(os.path.join(pathSaveBg, month + '_monthly_average_wave_energy_' + year + month), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
        plt.close()



