from __future__ import division
from os import listdir
from pydap.client import open_url
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np
import collections

print '  ' 
print '  '
print '  The computation will take a while! Dude, you can work in another issue for now...'
print '  '
print '  '
print '  Processing ice files...'
print '  '
print '  '


# "for" interaction through files in folder
for file in listdir('/home/oceano/rafael_vieira/era5/arquivos'):
	dataset = Dataset(file)
	if 'ice' in file:
		iceConc = dataset['siconc']
		lats = dataset['latitude']
		lons = dataset['longitude']
		tempo = dataset['time']

		# invert lat lon
		lons2D, lats2D = np.meshgrid(lons, lats)
		lats2DInv = lats2D[::-1]
		lons2DInv = lons2D[::-1]

		lats1DInv = lats2DInv[:,1]
		lons1DInv = lons2DInv[1,:]

		del dataset
		del lons2D
		del lats2D
		del lats2DInv
		del lons2DInv
		# lista de datas em string
		datesList = []
		initialDate = datetime(1900, 01, 01, 00)
		for i in tempo:
		        i = int(i)
		        dates = initialDate + timedelta(hours=i)
		        datesString = dates.strftime("%Y%m%d_%H%S")
		        datesList.append(datesString)

		del initialDate
		del i
		del dates
		del datesString
		# inverte u, v , ice
		iceDict = {}
		# inverting wind fields
		for index, name in enumerate(datesList):
			iceNormal = iceConc[index,:,:]
			iceInverted = iceNormal[::-1]
			iceDict["ice_{0}".format(name)] = iceInverted  # dictionary


		del datesList
		del index
		del name
		del iceNormal
		del iceInverted
		# sort and concatenate dicts
		iceDictOrdered = collections.OrderedDict(sorted(iceDict.items()))

		del iceDict
		iceConcat = np.stack(iceDictOrdered.values(), axis=0) # necessary variable to add in netcdf file

		del iceDictOrdered
		# create NETCDF file *****************************************
		iceDataset = Dataset('/home/oceano/rafael_vieira/era5/arquivos_teste_geral/' + file,\
							 'w', format='NETCDF4_CLASSIC')

		# create dimensions
		 # ice
		latI = iceDataset.createDimension('latitude', int(lats.size))
		lonI = iceDataset.createDimension('longitude', int(lons.size))
		timeI = iceDataset.createDimension('time', int(tempo.size))

		# create variables
		 # ice
		latitudesIce = iceDataset.createVariable('latitude', "f8", ('latitude',))
		longitudesIce = iceDataset.createVariable('longitude', "f8", ('longitude',))
		timesIce = iceDataset.createVariable('time', "f8", ('time',))

		# create 3D U and V variables
		ice_surface_extent = iceDataset.createVariable('ice_surface_extent', "f4", \
								('time', 'latitude', 'longitude'),fill_value='9.999000260554009e+20')

		# global attributes     
		iceDataset.description = 'COPERNICUS - ERA5 REANALISYS WIND COMPONENTS'

		# variable attributes
		 # ice
		latitudesIce.units = 'degrees_north'
		longitudesIce.units = 'degree_east'
		timesIce.units = 'hours since 1900-01-01 00:00:00.0'
		timesIce.calendar = 'gregorian'
		ice_surface_extent.units = '(0 - 1)'

		# add data into variables
		 # ice
		latitudesIce[:] = lats1DInv[:]
		longitudesIce[:] = lons1DInv[:]
		ice_surface_extent[:] = iceConcat[:]
		timesIce[:] = tempo[:]
		iceDataset.close()
		del iceConcat
		print '---> File ' + file + ' is done!'
		print ' '
print "  Computation is finished!"