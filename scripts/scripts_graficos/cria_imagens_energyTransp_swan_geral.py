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
initialDateVariable = datetime(1990, 01, 01, 00)

# 2017
jan2017 = datetime(2017, 1, 01, 00)
feb2017 = datetime(2017, 2, 01, 00)
mar2017 = datetime(2017, 3, 01, 00)
apr2017 = datetime(2017, 4, 01, 00)
may2017 = datetime(2017, 5, 01, 00)
jun2017 = datetime(2017, 6, 01, 00)
jul2017 = datetime(2017, 7, 01, 00)
aug2017 = datetime(2017, 8, 01, 00)
sep2017 = datetime(2017, 9, 01, 00)
oct2017 = datetime(2017, 10, 01, 00)
nov2017 = datetime(2017, 11, 01, 00)
dec2017 = datetime(2017, 12, 01, 00)

# 2018
jan2018 = datetime(2018, 1, 01, 00)
feb2018 = datetime(2018, 2, 01, 00)
mar2018 = datetime(2018, 3, 01, 00)
apr2018 = datetime(2018, 4, 01, 00)
may2018 = datetime(2018, 5, 01, 00)
jun2018 = datetime(2018, 6, 01, 00)
jul2018 = datetime(2018, 7, 01, 00)
aug2018 = datetime(2018, 8, 01, 00)
sep2018 = datetime(2018, 9, 01, 00)
oct2018 = datetime(2018, 10, 01, 00)
nov2018 = datetime(2018, 11, 01, 00)
dec2018 = datetime(2018, 12, 01, 00)

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


    # ************************* creating imagens ****************************************
for k, v in averageMonthlyDict.items():
    fig, ax = plt.subplots()
    plt.plot(costaLon, costaLat, 'k')
    lvl = np.arange(0, 12100, 1000)
    levels= [1000, 2000,5000, 6000, 7000, 8000, 9000, 10000, 12000]
    # levels= [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    cf = plt.contourf(lon, lat, v, lvl, vmin=0, vmax=12100, shading='gouraud')
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
    cbar.set_ticks([np.arange(0, 12100, 1000)], update_ticks=True)
    cbar.ax.tick_params(labelsize=8)
    plt.rcParams.update({'font.size': 7})
    #hour = str(k)[9:11]
    #day = str(k)[6:8]
    month = str(k)[0:3]
    monthNumber = str(k)[4:6]
    year = str(k)[7::]
    plt.title('Monthly average of Wave Power ' + month + '/' + year, fontsize=10)
    plt.savefig(os.path.join(pathSave, year + monthNumber), bbox_inches='tight', dpi=400)



