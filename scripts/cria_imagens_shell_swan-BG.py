# -*- coding: UTF-8 -*-

import os
import collections
import scipy.io as sio
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from mpl_toolkits.basemap import Basemap, cm
from intdir2uv import intdir2uv
from datetime import date, datetime, timedelta
import numpy as np

# reading user input and variables from "roda_sistema_shell.sh" shell script
resultsDir = os.environ["resultsdir"]
simulationName = os.environ["simulation_name"]
startingDate = os.environ["starting_date"]
startingTime = os.environ["starting_time"]
endingDate = os.environ["ending_date"]
endingTime = os.environ["ending_time"]
timeResolution = os.environ["time_resolution"]

# datas
currentDate = date.today().strftime("%Y%m%d")
yesterday = date.today() - timedelta(1)

# caminhos e variáveis
hs = sio.loadmat(resultsDir + simulationName + '/swan-BG/swan.' + startingDate[0:6] + '_hs.mat')
direct = sio.loadmat(resultsDir + simulationName + '/swan-BG/swan.' + startingDate[0:6] + '_dir.mat')
pathSaveBg = (resultsDir + simulationName + '/swan-BG/imagens')
lon_lat = sio.loadmat('/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
coastline = sio.loadmat('/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/swan/coastline_bg.mat')
lon = lon_lat['lon_bg_laje']
lat = lon_lat['lat_bg_laje']
costaLat = coastline['lat']
costaLon = coastline['lon']

del hs['HS_' + yesterday.strftime("%Y%m%d") + '_210000'],hs['__globals__'], hs['__header__'], hs['__version__']
del direct['DIR_' + yesterday.strftime("%Y%m%d") + '_210000'],direct['__globals__'], direct['__header__'], direct['__version__']

hsOrdered = collections.OrderedDict(sorted(hs.items()))
dirOrdered = collections.OrderedDict(sorted(direct.items()))

font = {'size':5}

# gera e salva imagens
for (k, v), (k2, v2) in zip(hsOrdered.items(), dirOrdered.items()):
	hsMasked = np.ma.masked_invalid(v)
	#hsMaskedInvert = hsMasked[::-1]
	dirMasked = np.ma.masked_invalid(v2)
	uWave, vWave = intdir2uv(1, dirMasked)
	ut = -uWave
	vt = -vWave
	#utInvert = ut[::-1] # v[::-1] gira a matriz de cima pra baixo (= flipud do matlab!)
	#vtInvert = vt[::-1]
	fig = plt.figure()
	plt.plot(costaLon, costaLat, 'k')
	lvl = np.arange(0, 3.6, 0.25)
	cf = plt.contourf(lon, lat, hsMasked, levels=lvl, vmin=0, vmax=3.6, cmap=plt.cm.get_cmap('jet'))
	plt.quiver(lon[::10,::10], lat[::10,::10], ut[::10,::10], vt[::10,::10], scale = 100, \
					width = 0.0009, headwidth = 6, headlength = 5, headaxislength = 4, minlength = 0.1)
	# plt.plot(-43.200, -22.940, 'ro',markersize=1.6, color='k')
	# plt.text(-43.218, -22.936, 'Rio de Janeiro', fontsize=8)
	# plt.plot(-43.175, -22.964, 'ro',markersize=1.6, color='k')
	# plt.text(-43.205, -22.965, 'Copacabana', fontsize=6.4)
	# plt.plot(-43.103, -22.945, 'ro',markersize=1.6, color='k')
	# plt.text(-43.0999999, -22.945, u'Niterói', fontsize=8)
	cbar = fig.colorbar(cf, ticks=[-1, 0, 1], orientation='vertical')
	cbar.set_label('Altura Significativa de Ondas (m)', size=9, rotation=270, labelpad=20)
	cbar.set_ticks([np.arange(0, 3.6, 0.25)], update_ticks=True)
	cbar.ax.tick_params(labelsize=6)
	hour = str(k)[12:14]
	day = str(k)[9:11]
	month = str(k)[7:9]
	year = str(k)[3:7]
	plt.title(k[9:11] + '/' + k[7:9] + '/' + k[3:7] + ' - ' + k[12:14] + 'H', fontsize=10)
	plt.rc('font', **font)
	plt.savefig(os.path.join(pathSaveBg, year + month + day + hour), bbox_inches='tight', dpi=300) 
	plt.close()

