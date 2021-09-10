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
#from mpl_toolkits.basemap import Basemap, cm
from datetime import date, datetime, timedelta
from intdir2uv import intdir2uv
from matplotlib.collections import PatchCollection
from tzlocal import get_localzone # $ pip install tzlocal
import math

todayString = date.today().strftime("%Y%m%d")
#todayString = "20200917"

resultsDir = '/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.4/resultados'
pathSaveBg = (resultsDir + '/swan-BG/' + todayString +'/imagens/wave_energy')

datasetEnergy = Dataset(resultsDir + '/swan-BG/' + todayString +'/netCDF/swan.transp_energy_bg.nc')
uWaveEnergy = datasetEnergy['u_component_energy_transp']
vWaveEnergy = datasetEnergy['v_component_energy_transp']
time = datasetEnergy['time']
lats = datasetEnergy['latitude'][:]
lons = datasetEnergy['longitude'][:]
lon, lat = np.meshgrid(lons, lats)

coastline = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.4/swan/coastline_bg.mat')
#costaLat = coastline['lat']
#costaLon = coastline['lon']
costaLon = np.genfromtxt('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.4/swan/lon_bg_mun.txt')
costaLat = np.genfromtxt('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.4/swan/lat_bg_mun.txt')


listField = []
initialDate = datetime(1990, 1, 1, 00)
for j in time:
	dates = initialDate + timedelta(days=np.float64(j))
	datesString = dates.strftime("%Y%m%d_%H%M%S")
	listField.append(datesString)


font = {'size':8}

#levels = np.arange(0, 3.1, 0.10)
#ian_rgb = np.array([[160.6486,223.6486,255],[144.9730,207.9730,255],[114.1622,194.4595,255],[10.7027,191.3243,255],[0,214.7838,255],[8.3784,231.6486,246.3514],[31.8649,255,222.1351],[44.4054,255,209.5946],[56.9459,255,197.0541],[82.0270,255,171.9730],[94.5676,255,159.4324],[107.1081,255,146.8919],[119.6486,255,134.3514],[132.1892,255,121.8108],[185.8108,255,68.1892],[201.8108,255,52.1892],[214.3514,255,39.6486],[226.8919,255,27.1081],[239.4324,255,14.5946],[255,245.4865,0],[255,232.9459,0],[255,220.4054,0],[255,207.8649,0],[255,195.3243,0],[255,170.2432,0],[255,157.7027,0],[255,145.1622,0],[255,111.8649,0],[255,88.0811,0],[255,31,0]], np.float64) / 255.0
levels = np.arange(0, 2.6, 0.10)
ian_rgb = np.array([[160.6486,223.6486,255],[144.9730,207.9730,255],[114.1622,194.4595,255],[0,214.7838,255],[8.3784,231.6486,246.3514],[31.8649,255,222.1351],[44.4054,255,209.5946],[56.9459,255,197.0541],[82.0270,255,171.9730],[107.1081,255,146.8919],[119.6486,255,134.3514],[132.1892,255,121.8108],[185.8108,255,68.1892],[214.3514,255,39.6486],[226.8919,255,27.1081],[239.4324,255,14.5946],[255,245.4865,0],[255,220.4054,0],[255,207.8649,0],[255,195.3243,0],[255,170.2432,0],[255,145.1622,0],[255,111.8649,0],[255,88.0811,0],[255,31,0],[180,10,0]], np.float64) / 255.0

    
# gera e salva imagens
for index, name in enumerate(listField[1::]):
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
    uEnergyField = uWaveEnergy[index,:,:]
    vEnergyField = vWaveEnergy[index,:,:]
    waveEnegy = np.hypot(uEnergyField, vEnergyField) # equivalent to "sqrt(u**2 + v**2)"
    plt.plot(costaLon, costaLat, 'k', linewidth=0.2, zorder=4)
    lvl = np.arange(0, 20100, 1000)
    #levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000]
    levels = range(1000,20100,500)
    strs = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0','16.5','17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
    #strs = ['1.0', '2.0', '3.0', '4.0']
    cf = plt.contourf(lon, lat, waveEnegy, lvl, vmin=0, vmax=20100)
    im = plt.contour(lon, lat, waveEnegy, levels, linewidths=0.5, colors='white', linestyles='solid')
    fmt = {}
    for l, s in zip(im.levels, strs):
        fmt[l] = s
    isobaths_labels = plt.clabel(im, inline=1, inline_spacing=-2.5, fmt=fmt, colors='white', fontsize=4.7)
    plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=1.0, foreground="k")])
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
    cbar.set_ticks([np.arange(0, 20100, 1000)])# update_ticks=True
    #cbar.set_yticks([0, 4.1, 0.2])[#0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.1])
    cbar.set_ticklabels(['0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']) # vertically oriented colorbar)
    cbar.set_label(u'Energia de Onda (kW/m)', size=6, rotation=90, labelpad=4)
    cbar.ax.tick_params(labelsize=6)
    #plt.rcParams.update({'font.size':4})
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
    plt.title('Energia de Ondas ' + day + '/' + month + '/' + year + ' - ' + hour[0:2] + 'H', fontsize=6)
    plt.rc('font', **font)
    ax.set_axisbelow(False) 
    plt.savefig(os.path.join(pathSaveBg, 'wavePower_bg_' + year + month + day + '_' + hour), bbox_inches='tight', dpi=300, transparent=False) # onda_bg_aaaammdd_hhmmss.png
    plt.close()      

