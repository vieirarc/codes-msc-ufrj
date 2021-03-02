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

# reading user input and variables from "roda_sistema_shell.sh" shell script
resultsDir = os.environ["resultsdir"]
simulationName = os.environ["simulation_name"]
startingDate = os.environ["starting_date"]
startingTime = os.environ["starting_time"]
endingDate = os.environ["ending_date"]
endingTime = os.environ["ending_time"]
timeResolution = os.environ["time_resolution"]

# Datas
todayString = date.today().strftime("%Y%m%d")
today = date.today()
finalDate = date.today() + timedelta(days=4)


# Pastas e arquivos
datasetHsGlobal = Dataset(resultsDir + simulationName + '/global/ww3.' + startingDate[0:6] + '_hs.nc')
datasetDirGlobal = Dataset(resultsDir + simulationName + '/global/ww3.' + startingDate[0:6] + '_dir.nc')
pathSaveGlobal = (resultsDir + simulationName + '/global/imagens')
waveHsGlobal = datasetHsGlobal['hs']
waveDirGlobal = datasetDirGlobal['dir']
lats = datasetDirGlobal['latitude'][:]
lons = datasetDirGlobal['longitude'][:]
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
    m = Basemap(projection='mill', llcrnrlat=-70, llcrnrlon=-360, urcrnrlat=70, urcrnrlon=0, resolution='l')
    m.drawcoastlines(linewidth=1.0)
    m.drawstates(linewidth=0.05)
    m.drawcountries(linewidth=0.1)
    m.fillcontinents(color='0.8', lake_color=None)
    m.drawparallels(np.arange(-90,90,30), fontsize=7, linewidth=0.03, labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180, 180, 60), fontsize=7, linewidth=0.03, labels=[0,0,0,1])
    waveFieldHsGlobal = waveHsGlobal[index,:,:]
    u, v = intdir2uv(1, waveDirGlobal[index,:,:])
    ut = -u
    vt = -v
    x, y = m(lonCorr,lat)
    im = m.imshow(waveFieldHsGlobal, vmin=0, vmax=7)
    m.quiver(x[::2,::2], y[::2,::2] ,ut[::2,::2], vt[::2,::2], \
        scale = 80, width = 0.0009, headwidth = 5, headlength = 5, headaxislength = 5, minlength = 0.1)
    cbar = m.colorbar(im, pad="10%")
    cbar.set_label('metros', size=7)
    cbar.set_ticks([np.arange(0, 8, 1)], update_ticks=True)
    cbar.ax.tick_params(labelsize=6)
    hour = str(name)[11:13]
    day = str(name)[8:10]
    month = str(name)[5:7]
    year = str(name)[0:4]
    plt.title(day + '/' + month + '/' + year + ' - ' + hour + 'H', fontsize=10)
    plt.savefig(os.path.join(pathSaveGlobal, year + month + day + hour), bbox_inches='tight', dpi=300)
    plt.close()


