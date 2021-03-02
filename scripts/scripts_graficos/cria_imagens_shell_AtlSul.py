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
# resultsDir = os.environ["resultsdir"]
# simulationName = os.environ["simulation_name"]
# startingDate = os.environ["starting_date"]
# startingTime = os.environ["starting_time"]
# endingDate = os.environ["ending_date"]
# endingTime = os.environ["ending_time"]
# timeResolution = os.environ["time_resolution"]

# save path and user input user dates variables
resultsDir = '/storage/oceano/rafael/wavewatch3_results/hindcast/teste_1'

startingDate = raw_input("Starting date (YYYYMMDD):")
startingTime = raw_input("Starting time (hhmmss):")
endingDate = raw_input("Ending date (YYYYMMDD):")
endingTime = raw_input("Starting date (YYYYMMDD):")
time_resolution = input("Time resolution (in seconds):")

# open files in folder and add names in specifics lists
hsNamesList = []
dirNamesList = []

# *WARNING* --> in "roda_sistema_hindcast.sh" the script do 'cd' to "vento_gelo_gfs" directory to run this 
# **FIX IT!!!**    script (extrai_datas.py). The netCDF4.Dataset is not working outside this folder!!!

# adding filename in lists
for file in os.listdir('.'):
    if "_dir" in file:
        dirNamesList.append(file)
    elif "_hs" in file:
        hsNamesList.append(file)
    else:
        continue


# define datespan function
def datespan(startDate, endDate, delta=timedelta(days=1)):
    startingDate = startDate
    while startingDate < endDate:
        yield startingDate
        startingDate += delta


# dates list used in "for" loop
listField = []
for j in datespan(datetime(int(startingDate[0:4]), int(startingDate[4:6]), int(startingDate[6:8]), int(startingTime[0:2])), \
        datetime(int(endingDate[0:4]), int(endingDate[4:6]), int(endingDate[6:8]), int(endingTime[0:2])), \
        delta=timedelta(hours=3)):
        listField.append(j)


for i, filename in enumerate(hsNamesList):
    # Pastas e arquivo
    datasetHsRegional = Dataset(resultsDir + '/south_atlantic/' + filename)
    datasetDirRegional = Dataset(resultsDir + '/south_atlantic/' + dirNamesList[i])
    pathSaveRegional = (resultsDir + '/south_atlantic/imagens')
    waveHsRegional = datasetHsRegional['hs']
    waveDirRegional = datasetDirRegional['dir'][:]
    time = datasetHsRegional['time']
    lats = datasetDirRegional['latitude'][:]
    lons = datasetDirRegional['longitude'][:]
    lon, lat = np.meshgrid(lons, lats)
    lonCorr = lon - 360
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



