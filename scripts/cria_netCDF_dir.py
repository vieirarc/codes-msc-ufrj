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
	if '_dir' in filename:
		filenamesList.append(filename)

filenamesList.sort() # sort list in rising order


for i in filenamesList:
	direct = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/' + i)
	lon_lat = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
	lons = lon_lat['lon_bg_laje']
	lats = lon_lat['lat_bg_laje']
	la = lats[:,0]
	lo = lons[0,:]
		# get time variable from ww3 result
	directWW3 = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/bg/ww3.' + i[5:15] + '.nc')
	tempo = directWW3['time']

	directOrdered = collections.OrderedDict(sorted(direct.items()))

	fistKey = list(directOrdered)[0]
	del directOrdered[fistKey],\
							directOrdered['__globals__'], directOrdered['__header__'], directOrdered['__version__']

	
	uDictDir = {}
	vDictDir = {}

	for k, v in directOrdered.items():
		dirMasked = np.ma.masked_invalid(v)
		uDir, vDir = intdir2uv(1, v)
		uTrans = -uDir
		vTrans = -vDir
		uDictDir["u_dir_{0}".format(k)] = uTrans
		vDictDir["v_dir_{0}".format(k)] = vTrans


	udirOrdered = collections.OrderedDict(sorted(uDictDir.items()))
	uWaveConcat = np.stack(udirOrdered.values(), axis=0)

	vdirOrdered = collections.OrderedDict(sorted(vDictDir.items()))
	vWaveConcat = np.stack(vdirOrdered.values(), axis=0)

	# ******** netCDF file ********

	# create netcdf file
	waveDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/' + i[0:-4] + '.nc',\
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
	u_dirWave_component = waveDataset.createVariable('u_component_wave', "f8", ('time', 'latitude', 'longitude'),fill_value='1e+20')
	v_dirWave_component = waveDataset.createVariable('v_component_wave', "f8", ('time', 'latitude', 'longitude'),fill_value='1e+20')

	# global attributes     
	waveDataset.description = 'Swan simulation results'

	# variable attributes
	latitudesW.units = 'degree_north'
	longitudesW.units = 'degree_east'
	timeW.units = 'days since 1990-01-01 00:00:00.0'
	timeW.calendar = 'gregorian'
	u_dirWave_component.units = 'm s**-1'
	v_dirWave_component.units = 'm s**-1'

	# add data into variables
	latitudesW[:] = la[:]
	longitudesW[:] = lo[:]
	u_dirWave_component[:] = uWaveConcat[:]
	v_dirWave_component[:] = vWaveConcat[:]
	timeW[:] = tempo

	waveDataset.close()

