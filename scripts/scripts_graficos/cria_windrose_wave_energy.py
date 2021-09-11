# -*- coding: UTF-8 -*-
from __future__ import division
import os
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker
from netCDF4 import Dataset
import numpy as np
import scipy.io as sio
from datetime import date, datetime, timedelta
import collections
from windrose import WindroseAxes
import math


# defining some diretories
resultsDir = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/teste_18'
pathSaveBg = (resultsDir + '/swan-BG/imagens/simulacao_geral/wave_energy/direction')


# open files and get variables
datasetEnergy = Dataset(resultsDir + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_transp_energy.nc')
time = datasetEnergy['time']
uWaveEnergy = datasetEnergy['u_component_energy_transp']
vWaveEnergy = datasetEnergy['v_component_energy_transp']
time = datasetEnergy['time']
lats = datasetEnergy['latitude'][:]
lons = datasetEnergy['longitude'][:]
lon, lat = np.meshgrid(lons, lats)


# counters
# 2017

# wave power
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


# U V ***************
sumUcompSummer2017 = 0
sumVcompSummer2017 = 0
fieldsSummer2017 = 0

sumUcompAutumn2017 = 0
sumVcompAutumn2017 = 0
fieldsAutumn2017 = 0

sumUcompWinter2017 = 0
sumVcompWinter2017 = 0
fieldsWinter2017 = 0

sumUcompSpring2017 = 0
sumVcompSpring2017 = 0
fieldsSpring2017 = 0


# 2018 *****************
sumUcompSummer2018 = 0
sumVcompSummer2018 = 0
fieldsSummer2018 = 0

sumUcompAutumn2018 = 0
sumVcompAutumn2018 = 0
fieldsAutumn2018 = 0

sumUcompWinter2018 = 0
sumVcompWinter2018 = 0
fieldsWinter2018 = 0

sumUcompSpring2018 = 0
sumVcompSpring2018 = 0
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


# converting U V to degrees
# empty lists and dicts

energyPointSummer2017 = []
energyPointAutumn2017 = []
energyPointWinter2017 = []
energyPointSpring2017 = []
energyPointSummer2018 = []
energyPointAutumn2018 = []
energyPointWinter2018 = []
energyPointSpring2018 = []


dirPointSummer2017 = []
dirPointAutumn2017 = []
dirPointWinter2017 = []
dirPointSpring2017 = []
dirPointSummer2018 = []
dirPointAutumn2018 = []
dirPointWinter2018 = []
dirPointSpring2018 = []


energyDict = {}
dirDict = {}

# ***** choosing the point for analysis ******

pAnl = 'XX ' # define here the point name

for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if Summer2017 <= dates < Autumn2017:    
        uEnergyFieldSummer2017 = uWaveEnergy[index,:,:]
        vEnergyFieldSummer2017 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldSummer2017[25, 15]
        vPoint1 = vEnergyFieldSummer2017[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergySummer2017 = np.hypot(uEnergyFieldSummer2017, vEnergyFieldSummer2017)
        energyPoint = waveEnergySummer2017[25, 15]
        dirPointSummer2017.append(testeDirdegree)
        energyPointSummer2017.append(energyPoint)
    elif Autumn2017 <= dates < Winter2017:
        uEnergyFieldAutumn2017 = uWaveEnergy[index,:,:]
        vEnergyFieldAutumn2017 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldAutumn2017[25, 15]
        vPoint1 = vEnergyFieldAutumn2017[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergyAutumn2017 = np.hypot(uEnergyFieldAutumn2017, vEnergyFieldAutumn2017) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergyAutumn2017[25, 15]
        dirPointAutumn2017.append(testeDirdegree)
        energyPointAutumn2017.append(energyPoint)
    elif Winter2017 <= dates < Spring2017:
        uEnergyFieldWinter2017 = uWaveEnergy[index,:,:]
        vEnergyFieldWinter2017 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldWinter2017[25, 15]
        vPoint1 = vEnergyFieldWinter2017[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergyWinter2017 = np.hypot(uEnergyFieldWinter2017, vEnergyFieldWinter2017) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergyWinter2017[25, 15]
        dirPointWinter2017.append(testeDirdegree)
        energyPointWinter2017.append(energyPoint)
    elif Spring2017 <= dates < Summer2018:
        uEnergyFieldSpring2017 = uWaveEnergy[index,:,:]
        vEnergyFieldSpring2017 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldSpring2017[25, 15]
        vPoint1 = vEnergyFieldSpring2017[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergySpring2017 = np.hypot(uEnergyFieldSpring2017, vEnergyFieldSpring2017) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergySpring2017[25, 15]
        dirPointSpring2017.append(testeDirdegree)
        energyPointSpring2017.append(energyPoint)
    elif Summer2018 <= dates < Autumn2018:
        uEnergyFieldSummer2018 = uWaveEnergy[index,:,:]
        vEnergyFieldSummer2018 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldSummer2018[25, 15]
        vPoint1 = vEnergyFieldSummer2018[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergySummer2018 = np.hypot(uEnergyFieldSummer2018, vEnergyFieldSummer2018) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergySummer2018[25, 15]
        dirPointSummer2018.append(testeDirdegree)
        energyPointSummer2018.append(energyPoint)
    elif Autumn2018 <= dates < Winter2018:
        uEnergyFieldAutumn2018 = uWaveEnergy[index,:,:]
        vEnergyFieldAutumn2018 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldAutumn2018[25, 15]
        vPoint1 = vEnergyFieldAutumn2018[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergyAutumn2018 = np.hypot(uEnergyFieldAutumn2018, vEnergyFieldAutumn2018) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergyAutumn2018[25, 15]
        dirPointAutumn2018.append(testeDirdegree)
        energyPointAutumn2018.append(energyPoint)
    elif Winter2018 <= dates < Spring2018:
        uEnergyFieldWinter2018 = uWaveEnergy[index,:,:]
        vEnergyFieldWinter2018 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldWinter2018[25, 15]
        vPoint1 = vEnergyFieldWinter2018[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergyWinter2018 = np.hypot(uEnergyFieldWinter2018, vEnergyFieldWinter2018) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergyWinter2018[25, 15]
        dirPointWinter2018.append(testeDirdegree)
        energyPointWinter2018.append(energyPoint)
    elif Spring2018 <= dates < Spring2018Final:
        uEnergyFieldSpring2018 = uWaveEnergy[index,:,:]
        vEnergyFieldSpring2018 = vWaveEnergy[index,:,:]
        uPoint1 = uEnergyFieldSpring2018[25, 15]
        vPoint1 = vEnergyFieldSpring2018[25, 15]
        radDirct = math.atan2(uPoint1, vPoint1)
        degDirect = math.degrees(radDirct)
        testeDirdegree = math.fmod(180 + (180/math.pi) * math.atan2(uPoint1,vPoint1),360)
        waveEnergySpring2018 = np.hypot(uEnergyFieldSpring2018, vEnergyFieldSpring2018) # equivalent to "sqrt(u**2 + v**2)"
        energyPoint = waveEnergySpring2018[25, 15]
        dirPointSpring2018.append(testeDirdegree)
        energyPointSpring2018.append(energyPoint)
    else:
        continue


# adding lists to dicts

# 2017
energyDict["energy_Summer2017"] = energyPointSummer2017
dirDict["dir_Summer2017"] = dirPointSummer2017

energyDict["energy_Autumn2017"] = energyPointAutumn2017
dirDict["dir_Autumn2017"] = dirPointAutumn2017

energyDict["energy_Winter2017"] = energyPointWinter2017
dirDict["dir_Winter2017"] = dirPointWinter2017

energyDict["energy_Spring2017"] = energyPointSpring2017
dirDict["dir_Spring2017"] = dirPointSpring2017

# 2018
energyDict["energy_Summer2018"] = energyPointSummer2018
dirDict["dir_Summer2018"] = dirPointSummer2018

energyDict["energy_Autumn2018"] = energyPointAutumn2018
dirDict["dir_Autumn2018"] = dirPointAutumn2018

energyDict["energy_Winter2018"] = energyPointWinter2018
dirDict["dir_Winter2018"] = dirPointWinter2018

energyDict["energy_Spring2018"] = energyPointSpring2018
dirDict["dir_Spring2018"] = dirPointSpring2018


# *********** plotting windrose ************

for (k1, v1), (k2, v2) in zip(dirDict.items(), energyDict.items()):
    if k1[-10::]==k2[-10::]=='Summer2017':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '1_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Autumn2017':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '2_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Winter2017':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '3_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Spring2017':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '4_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Summer2018':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '5_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Autumn2018':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '6_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Winter2018':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '7_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    elif k1[-10::]==k2[-10::]=='Spring2018':
        ax = WindroseAxes.from_ax()
        ax.bar(v1, v2, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                        normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
        la = np.arange(0, max(energyPointSummer2017), 4000)

        # getting labels in strig
        laList = []
        laFinalList = []

        for i in la:
            nLa = int(i / 1000)
            nLaStr = str(nLa)
            laList.append(nLaStr)

        for index, name in enumerate(laList):
            if index < 5:
                laNsum = name + ' - ' + laList[index + 1]
                laFinalList.append(laNsum)
            else:
                laNsum = name + ' +'
                laFinalList.append(laNsum)



        obs = 'Frequency in % of time'
        ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                                     prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
        plt.gcf().text(0.907, 0.6, obs, fontsize=11)
        ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
        ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
        ax.set_yticks(numpy.arange(5, 35.1, 5))
        ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax.set_rlabel_position(45)  # get radial labels away from plotted line
        ax.set_title('Wave energy transport - Point ' + pAnl + k1[4:10] + ' ' + k1[10::], fontsize=16)
        plt.savefig(os.path.join(pathSaveBg, '8_windrose_waves_' + k1[-10::]), bbox_inches='tight', dpi=300, transparent=False)
    else:
        continue




# *****************************

# original windrose plot


# As variáveis dirPointSummer2017 e energyPointSummer2017
# sao vetores unidimensionais

# creating plot
ax = WindroseAxes.from_ax()
ax.bar(dirPointSummer2017, energyPointSummer2017, bins=np.arange(0, max(energyPointSummer2017), 4000), \
                                                normed=True, opening=0.8, cmap=mpl.cm.jet, edgecolor='white')
la = np.arange(0, max(energyPointSummer2017), 4000)

# getting labels as strig
laList = []
laFinalList = []

for i in la:
    nLa = int(i / 1000)
    nLaStr = str(nLa)
    laList.append(nLaStr)

for index, name in enumerate(laList):
    if index < 5:
        laNsum = name + ' - ' + laList[index + 1]
        laFinalList.append(laNsum)
    else:
        laNsum = name + ' +'
        laFinalList.append(laNsum)



obs = 'Frequency in % of time'
ax.legend(labels=laFinalList, title="Wave Energy (kW/m)", fontsize=10, \
                             prop={'size':10}, loc='best', shadow=True, bbox_to_anchor=(0.63, 0.45, 0.63, 0.45))
plt.gcf().text(0.701, 0.611111111111, obs, fontsize=11)
ax.set_xticklabels((90, 45, 0, 315, 270, 225, 180, 135))
ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW','S', 'SE'], fontsize=14)
ax.set_yticks(numpy.arange(5, 35.1, 5))
ax.set_yticklabels(numpy.arange(5, 35.1, 5), fontsize=12, verticalalignment='top', horizontalalignment='right')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
ax.set_rlabel_position(45)  # get radial labels away from plotted line
ax.set_title('Wave energy transport', fontsize=16)
