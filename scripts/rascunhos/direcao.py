import os
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import scipy.io as sio
from mpl_toolkits.basemap import Basemap
from datetime import date, datetime, timedelta
from intdir2uv import intdir2uv

# Datas
currentDate = date.today().strftime("%Y%m%d")
finalDate = date.today() + timedelta(days=4)
yesterday = date.today() - timedelta(1)

# Pastas e arquivo
datasetHsRegional = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional/resultados/regional/' +  currentDate + '/ww3.2018_hs.nc')
datasetDirRegional = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional/resultados/regional/' + currentDate + '/ww3.2018_dir.nc')
pathSaveRegional = ('/home/piatam8/ww3/ww3_shell/modelo_operacional/scripts/imagens_teste')
waveHsRegional = datasetHsRegional['hs']
waveDirRegional = datasetDirRegional['dir'][:]
lats = datasetDirRegional['latitude'][:]
lons = datasetDirRegional['longitude'][:]
lon, lat = np.meshgrid(lons, lats)
u, v = intdir2uv(4, waveDirRegional[10])
waveFieldHsRegional = waveHsRegional[10,:,:]

# Imagem
m = Basemap(llcrnrlon=-67.2, llcrnrlat=-40.60, urcrnrlon=-11.15, urcrnrlat=-6.99, resolution='l', projection='merc')
m.drawcoastlines(linewidth=1.0)
m.drawstates(linewidth=0.1)
m.drawcountries(linewidth=0.8)
m.drawparallels(np.arange(-90,90,10), fontsize=10, linewidth=0.03, labels=[1,0,0,0])
m.drawmeridians(np.arange(m.lonmin,m.lonmax, 10), fontsize=10, linewidth=0.03, labels=[0,0,0,1])

lonteste = lon - 360
x, y = m(lonteste,lat)

m.pcolor(x[58:125,5:115], y[58:125,5:115], waveFieldHsRegional[58:125,5:115], vmin=0, vmax=7)
m.quiver(x[58:125,5:115][::2,::2], y[58:125,5:115][::2,::2] ,u[58:125,5:115][::2,::2], v[58:125,5:115][::2,::2], \
	scale = 500, width = 0.0009, headwidth = 5, headlength = 3, headaxislength = 3, minlength = 0.1)
