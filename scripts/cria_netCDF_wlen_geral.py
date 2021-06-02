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
for filename in os.listdir('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_2/swan-BG/simulacao_geral'):
	if '_wlen' in filename:
		filenamesList.append(filename)

filenamesList.sort() # sort list in rising order


for i in filenamesList:
	# accessing data
	wlen = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_2/swan-BG//simulacao_geral/' + i)
	lon_lat = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
	lons = lon_lat['lon_bg_laje']
	lats = lon_lat['lat_bg_laje']
	la = lats[:,0]
	lo = lons[0,:]
	
	# creating time variable based in ww3 results 
	tempo = np.arange(9831.0, 10591.876, .125)


	# sorting elements inside dict
	wlenOrdered = collections.OrderedDict(sorted(wlen.items()))
	
	# deleting unecessary elements
	fistKey = list(wlenOrdered)[0]
	del wlenOrdered[fistKey],\
							wlenOrdered['__globals__'], wlenOrdered['__header__'], wlenOrdered['__version__']


	wlenDict = {}


	for k, v in wlenOrdered.items():
		wlenMasked = np.ma.masked_invalid(v)
		wlenDict["wlen_{0}".format(k)] = v


	wlenNewOrdered = collections.OrderedDict(sorted(wlenDict.items()))
	wlenConcat = np.stack(wlenNewOrdered.values(), axis=0)

	# ******** netCDF file ********

	# create netcdf file
	waveDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_2/swan-BG/arquivos_netCDF/simulacao_geral/' + i[0:-4] + '.nc', \
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
	wlenWave = waveDataset.createVariable('wlen', "f8", ('time', 'latitude', 'longitude'))


	# global attributes     
	waveDataset.description = 'Swan simulation results'

	# variable attributes
	latitudesW.units = 'degree_north'
	longitudesW.units = 'degree_east'
	timeW.units = 'days since 1990-01-01 00:00:00.0'
	timeW.calendar = 'gregorian'
	wlenWave.units = 'm'

	# add data into variables
	latitudesW[:] = la[:]
	longitudesW[:] = lo[:]
	wlenWave[:] = wlenConcat[:]
	timeW[:] = tempo

	waveDataset.close()
	del wlenConcat
	del wlenOrdered

