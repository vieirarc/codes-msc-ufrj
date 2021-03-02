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

# Pastas e arquivo
datasetHsRegional = Dataset(resultsDir + simulationName + '/south_atlantic/ww3.' + startingDate[0:6] + '_hs.nc')
datasetDirRegional = Dataset(resultsDir + simulationName + '/south_atlantic/ww3.' + startingDate[0:6] + '_dir.nc')
pathSaveRegional = (resultsDir + simulationName + '/south_atlantic/imagens')
waveHsRegional = datasetHsRegional['hs']
waveDirRegional = datasetDirRegional['dir'][:]
time = datasetHsRegional['time']
lats = datasetDirRegional['latitude'][:]
lons = datasetDirRegional['longitude'][:]
lon, lat = np.meshgrid(lons, lats)
lonCorr = lon - 360


# define funcao datespan
def datespan(startDate, endDate, delta=timedelta(days=1)):
    startingDate = startDate
    while startingDate < endDate:
        yield startingDate
        startingDate += delta


# lista de datas
listField = []
for j in datespan(datetime(startingDate[0:4], startingDate[4:6], startingDate[6:8], startingTime[0:2]), \
        datetime(endingDate[0:4], endingDate[4:6], endingDate[6:8], endingTime[0:2]), \
        delta=timedelta(seconds=time_resolution)):
        listField.append(j)


'''
# **** think about a new solution here!!! --> using time variable to fix it right ****
for j in time:
    datespan(datetime(startingDate[0:4], startingDate[4:6], startingDate[6:8], startingTime[0:2]), \
        datetime(endingDate[0:4], endingDate[4:6], endingDate[6:8], endingTime[0:2]), \
        delta=timedelta(seconds=time_resolution)):
        listField.append(j)

'''

# Cria imagens
for index, name in enumerate(listField):
    m = Basemap(llcrnrlon=-69.0, llcrnrlat=-57.6, urcrnrlon=-2.0, urcrnrlat=-6.0, resolution='l', projection='merc') # **** parei aqui! *****
    m.drawcoastlines(linewidth=0.8)
    m.drawstates(linewidth=0.1)
    m.drawcountries(linewidth=0.6)
    m.fillcontinents(color='0.8', lake_color=None)
    m.drawparallels(np.arange(-90,90,10), fontsize=7, linewidth=0.03, labels=[1,0,0,0])
    m.drawmeridians(np.arange(m.lonmin,m.lonmax, 10), fontsize=7, linewidth=0.03, labels=[0,0,0,1])
    waveFieldHsRegional = waveHsRegional[index,:,:]
    u, v = intdir2uv(1, waveDirRegional[index,:,:])
    ut = -u
    vt = -v
    x, y = m(lonCorr,lat)
    im = m.pcolormesh(x, y,waveFieldHsRegional, vmin=0, vmax=8, shading='gouraud')  
    m.quiver(x[::4,::4], y[::4,::4] ,ut[::4,::4], vt[::4,::4], \
        scale = 60, width = 0.0009, headwidth = 9, headlength = 5, headaxislength = 5, minlength = 0.1)
    cbar = m.colorbar(im, pad="10%")
    cbar.set_label('metros', size=7)
    cbar.set_ticks([np.arange(0, 8, 1)], update_ticks=True)
    cbar.ax.tick_params(labelsize=6)
    hour = str(name)[11:13]
    day = str(name)[8:10]
    month = str(name)[5:7]
    year = str(name)[0:4]
    plt.title(day + '/' + month + '/' + year + ' - ' + hour + 'H', fontsize=10)
    plt.savefig(os.path.join(pathSaveRegional, year + month + day + hour), bbox_inches='tight', dpi=300)
    plt.close()

