# -*- coding: UTF-8 -*-

import collections
import os
import numpy as np
import scipy.io as sio
from intdir2uv import intdir2uv
from netCDF4 import Dataset
from datetime import datetime, timedelta


# get a list with file names
filenamesList = []
for filename in os.listdir('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG'):
	if '_per' in filename:
		filenamesList.append(filename)

filenamesList.sort() # sort list in rising order

for i in filenamesList:
	datasetTp = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/' + i)
	lon_lat = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
	lons = lon_lat['lon_bg_laje']
	lats = lon_lat['lat_bg_laje']
	la = lats[:,0]
	lo = lons[0,:]
	# get time variable from ww3 result
	tpWW3 = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/bg/ww3.' + i[5:12] + 't02.nc')
	tempo = tpWW3['time']

	tpOrdered = collections.OrderedDict(sorted(datasetTp.items()))

	fistKey = list(tpOrdered)[0]
	del tpOrdered[fistKey],\
							tpOrdered['__globals__'], tpOrdered['__header__'], tpOrdered['__version__']


	tpDict = {}


	for k, v in tpOrdered.items():
		tpMasked = np.ma.masked_invalid(v)
		tpDict["hs_{0}".format(k)] = v


	tpNewOrdered = collections.OrderedDict(sorted(tpDict.items()))
	tpConcat = np.stack(tpNewOrdered.values(), axis=0)

	# ******** netCDF file ********

	# create netcdf file
	waveDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/' + i[0:-4] + '.nc', \
							'w', format='NETCDF3_CLASSIC')


	# create dimensions
	waveDataset.createDimension('latitude', int(la.size))
	waveDataset.createDimension('longitude', int(lo.size))
	waveDataset.createDimension('time', int(tempo.size))

	# create variables
	latitudesW = waveDataset.createVariable('latitude', "f8", ('latitude',))
	longitudesW = waveDataset.createVariable('longitude', "f8", ('longitude',))
	timeW = waveDataset.createVariable('time', "f8", ('time',))

	# create 3D U and V variables
	tpWave = waveDataset.createVariable('t02', "f8", ('time', 'latitude', 'longitude'))


	# global attributes     
	waveDataset.description = 'Swan simulation results'

	# variable attributes
	latitudesW.units = 'degree_north'
	longitudesW.units = 'degree_east'
	timeW.units = 'days since 1990-01-01 00:00:00.0'
	timeW.calendar = 'gregorian'
	tpWave.units = 's'

	# add data into variables
	latitudesW[:] = la[:]
	longitudesW[:] = lo[:]
	tpWave[:] = tpConcat[:]
	timeW[:] = tempo

	waveDataset.close()
	del tpConcat
	del tpOrdered

