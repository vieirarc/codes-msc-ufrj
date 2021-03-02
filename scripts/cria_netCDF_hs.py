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
	if '_hs' in filename:
		filenamesList.append(filename)

filenamesList.sort() # sort list in rising order

for i in filenamesList:
	datasetHs = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/' + i)
	lon_lat = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
	lons = lon_lat['lon_bg_laje']
	lats = lon_lat['lat_bg_laje']
	la = lats[:,0]
	lo = lons[0,:]
	# get time variable from ww3 result
	hsWW3 = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/bg/ww3.' + i[5:14] + '.nc')
	tempo = hsWW3['time']

	hsOrdered = collections.OrderedDict(sorted(datasetHs.items()))

	fistKey = list(hsOrdered)[0]
	del hsOrdered[fistKey],\
							hsOrdered['__globals__'], hsOrdered['__header__'], hsOrdered['__version__']


	hsDict = {}


	for k, v in hsOrdered.items():
		hsMasked = np.ma.masked_invalid(v)
		hsDict["hs_{0}".format(k)] = v


	hsNewOrdered = collections.OrderedDict(sorted(hsDict.items()))
	hsConcat = np.stack(hsNewOrdered.values(), axis=0)

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
	hsWave = waveDataset.createVariable('hs', "f8", ('time', 'latitude', 'longitude'))


	# global attributes     
	waveDataset.description = 'Swan simulation results'

	# variable attributes
	latitudesW.units = 'degree_north'
	longitudesW.units = 'degree_east'
	timeW.units = 'days since 1990-01-01 00:00:00.0'
	timeW.calendar = 'gregorian'
	hsWave.units = 'm'

	# add data into variables
	latitudesW[:] = la[:]
	longitudesW[:] = lo[:]
	hsWave[:] = hsConcat[:]
	timeW[:] = tempo

	waveDataset.close()
	del hsConcat
	del hsOrdered

