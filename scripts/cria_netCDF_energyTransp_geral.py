# -*- coding: UTF-8 -*-

import collections
import os
import numpy as np
import scipy.io as sio
from intdir2uv import intdir2uv
from netCDF4 import Dataset
from datetime import datetime, timedelta


# env. variable from shell
simulationName = os.environ["simulation_name"]

# get a list with file names
filenamesList = []
for filename in os.listdir('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/' + simulationName + '/swan-BG/simulacao_geral'):
	if '_transp_energy' in filename:
		filenamesList.append(filename)

filenamesList.sort() # sort list in rising order


for i in filenamesList:
	# accessing data
	energyTransp = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/' + simulationName + '/swan-BG/simulacao_geral/' + i)
	lon_lat = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/lon_lat_bg_laje.mat')
	lons = lon_lat['lon_bg_laje']
	lats = lon_lat['lat_bg_laje']
	la = lats[:,0]
	lo = lons[0,:]
	
	# creating time variable based in ww3 results
	tempo = np.arange(9831.0, 10591.876, .125)	

	# sorting elements inside dict
	energyTranspOrdered = collections.OrderedDict(sorted(energyTransp.items()))
	
	# deleting unecessary elements
	xFirstKey = list(energyTranspOrdered)[0]
	yFirstKey = xFirstKey[0:7] + 'y' + xFirstKey[8::]
	print xFirstKey
	print yFirstKey

	# TRANSP_x_20181130_210000
	del energyTranspOrdered[xFirstKey], energyTranspOrdered[yFirstKey],\
							energyTranspOrdered['__globals__'], energyTranspOrdered['__header__'], energyTranspOrdered['__version__']

	# separating U and V in differents dicts
	uDictEnergy = {}
	vDictEnergy = {}
	for k, v in energyTranspOrdered.items():
		if 'TRANSP_x' in k:
			uDictEnergy["u_transp_energy_{0}".format(k[9::])] = v
		else:
			vDictEnergy["v_transp_energy_{0}".format(k[9::])] = v


	uEnergyOrdered = collections.OrderedDict(sorted(uDictEnergy.items()))
	uEnergyConcat = np.stack(uEnergyOrdered.values(), axis=0)

	vEnergyOrdered = collections.OrderedDict(sorted(vDictEnergy.items()))
	vEnergyConcat = np.stack(vEnergyOrdered.values(), axis=0)

	# ******** netCDF file ********

	# create netcdf file
	energyDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/' + simulationName + '/swan-BG/arquivos_netCDF/simulacao_geral/' + i[0:-4] + '.nc',\
						 'w', format='NETCDF3_64BIT_OFFSET')

	# create dimensions
	energyDataset.createDimension('latitude', int(la.size))
	energyDataset.createDimension('longitude', int(lo.size))
	energyDataset.createDimension('time', int(tempo.size))

	# create variables
	latitudesW = energyDataset.createVariable('latitude', "f4", ('latitude',))
	longitudesW = energyDataset.createVariable('longitude', "f4", ('longitude',))
	timeW = energyDataset.createVariable('time', "f4", ('time',))

	# create 3D U and V variables
	u_energy_component = energyDataset.createVariable('u_component_energy_transp', "f4", ('time', 'latitude', 'longitude'),fill_value='1e+20')
	v_energy_component = energyDataset.createVariable('v_component_energy_transp', "f4", ('time', 'latitude', 'longitude'),fill_value='1e+20')

	# global attributes     
	energyDataset.description = 'Swan simulation results'

	# variable attributes
	latitudesW.units = 'degree_north'
	longitudesW.units = 'degree_east'
	timeW.units = 'days since 1990-01-01 00:00:00.0'
	timeW.calendar = 'gregorian'
	u_energy_component.units = 'm s**-1'
	v_energy_component.units = 'm s**-1'

	# add data into variables
	latitudesW[:] = la[:]
	longitudesW[:] = lo[:]
	u_energy_component[:] = uEnergyConcat[:]
	v_energy_component[:] = vEnergyConcat[:]
	timeW[:] = tempo

	energyDataset.close()

