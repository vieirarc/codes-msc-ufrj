# -*- coding: UTF-8 -*-

import os
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from netCDF4 import Dataset
import numpy as np
import scipy.io as sio
from mpl_toolkits.basemap import Basemap, cm
from datetime import date, datetime, timedelta
from intdir2uv import intdir2uv


simulationName = raw_input('Simulation Name: ')

# Datas
todayString = date.today().strftime("%Y%m%d")
today = date.today()
finalDate = date.today() + timedelta(days=4)
yesterday = date.today() - timedelta(1)

# Pastas e arquivo
datasetHsRegional = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/grade_bg/' +  simulationName + '/ww3.' + todayString[0:4] + '_hs.nc')
datasetDirRegional = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/grade_bg/' + simulationName + '/ww3.' + todayString[0:4] + '_dir.nc')
pathSaveRegional = ('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/grade_bg/' +  simulationName + '/imagens')
waveHsRegional = datasetHsRegional['hs']
waveDirRegional = datasetDirRegional['dir'][:]
lats = datasetDirRegional['latitude'][:]
lons = datasetDirRegional['longitude'][:]
lon, lat = np.meshgrid(lons, lats)
lonCorr = lon - 360


# define funcao datespan
def datespan(startDate, endDate, delta=timedelta(days=1)):
    todayString = startDate
    while todayString < endDate:
        yield todayString
        todayString += delta


# lista de datas
listField = []
for j in datespan(datetime(today.year, today.month, today.day, 00), \
        datetime(finalDate.year, finalDate.month, finalDate.day, 22), delta=timedelta(hours=3)):
        listField.append(j)


# Cria imagens
for index, name in enumerate(listField):
    m = Basemap(llcrnrlon=-43.7, llcrnrlat=-23.6, urcrnrlon=-42.4, urcrnrlat=-22.0,\
                                     resolution='h', projection='merc')
    m.drawcoastlines(linewidth=0.8)
    m.drawstates(linewidth=0.1)
    m.drawcountries(linewidth=0.6)
    m.fillcontinents(color='0.8', lake_color='None')
    m.drawparallels(np.arange(-23.9, -21.9 ,0.5), fontsize=7, linewidth=0.03, labels=[1,0,0,0])
    m.drawmeridians(np.arange(m.lonmin,m.lonmax, 0.5), fontsize=7, linewidth=0.03, labels=[0,0,0,1])
    waveFieldHsRegional = waveHsRegional[index,:,:]
    u, v = intdir2uv(1, waveDirRegional[index,:,:])
    ut = -u
    vt = -v
    x, y = m(lonCorr,lat)
    im = m.pcolormesh(x, y,waveFieldHsRegional, vmin=0, vmax=2.5, shading='gouraud')  
    m.quiver(x[::1,::1], y[::1,::1] ,ut[::1,::1], vt[::1,::1], \
        scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
    cbar = m.colorbar(im, pad="10%")
    cbar.set_label('metros', size=7)
    cbar.set_ticks([np.arange(0, 2.5, 0.5)], update_ticks=True)
    cbar.ax.tick_params(labelsize=6)
    hour = str(name)[11:13]
    day = str(name)[8:10]
    month = str(name)[5:7]
    year = str(name)[0:4]
    plt.title(day + '/' + month + '/' + year + ' - ' + hour + 'H', fontsize=8)
    plt.savefig(os.path.join(pathSaveRegional, year + month + day + hour), bbox_inches='tight', dpi=300)
    plt.close()

