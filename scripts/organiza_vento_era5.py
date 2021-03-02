from __future__ import division
from pydap.client import open_url
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np
import collections

# accessing data
dataset = Dataset('201807_uv_wind_era5.nc')

uComp = dataset['u10']
vComp = dataset['v10']
lats = dataset['latitude']
lons = dataset['longitude']
tempo = dataset['time']

# invert lat lon
lons2D, lats2D = np.meshgrid(lons, lats)
lats2DInv = lats2D[::-1]
lons2DInv = lons2D[::-1]

lats1DInv = lats2DInv[:,1]
lons1DInv = lons2DInv[1,:]

# lista de datas em string
datesList = []
initialDate = datetime(1900, 01, 01, 00)
for i in tempo:
        i = int(i)
        dates = initialDate + timedelta(hours=i)
        datesString = dates.strftime("%Y%m%d_%H%S")
        datesList.append(datesString)


print ('****Inicio Concatenacao****')
# inverte u, v , ice
uWndDict = {}
vWndDict = {}

# inverting wind fields
for index, name in enumerate(datesList):
	uWndNormal = uComp[index,:,:]
	vWndNormal = vComp[index,:,:]
	uWndInverted = uWndNormal[::-1]
	vWndInverted = vWndNormal[::-1]
	uWndDict["uWnd_{0}".format(name)] = uWndInverted  # dictionary
	vWndDict["vWnd_{0}".format(name)] = vWndInverted  # dictionary


# sort and concatenate dicts
uWndDictOrdered = collections.OrderedDict(sorted(uWndDict.items()))
uWndConcat = np.stack(uWndDictOrdered.values(), axis=0)

vWndDictOrdered = collections.OrderedDict(sorted(vWndDict.items()))
vWndConcat = np.stack(vWndDictOrdered.values(), axis=0)


# create netcdf file
wndDataset = Dataset('/home/oceano/rafael_vieira/era5/arquivos_editados/201807_uv_wind_era5.nc',\
					 'w', format='NETCDF4_CLASSIC')

# create dimensions
 # wind 
latW = wndDataset.createDimension('latitude', int(lats.size))
lonW = wndDataset.createDimension('longitude', int(lons.size))
timeW = wndDataset.createDimension('time', int(tempo.size))

# create variables
 # wind
latitudesWnd = wndDataset.createVariable('latitude', "f8", ('latitude',))
longitudesWnd = wndDataset.createVariable('longitude', "f8", ('longitude',))
timesWnd = wndDataset.createVariable('time', "f8", ('time',))

# create 3D U and V variables
u_wnd10m_component = wndDataset.createVariable('u_wnd10m_component', "f4", ('time', 'latitude', 'longitude'),fill_value='9.999000260554009e+20')
v_wnd10m_component = wndDataset.createVariable('v_wnd10m_component', "f4", ('time', 'latitude', 'longitude'),fill_value='9.999000260554009e+20')

# global attributes     
wndDataset.description = 'COPERNICUS - ERA5 REANALISYS WIND COMPONENTS'

# variable attributes
 # wind
latitudesWnd.units = 'degree_north'
longitudesWnd.units = 'degree_east'
timesWnd.units = 'hours since 1900-01-01 00:00:00.0'
timesWnd.calendar = 'gregorian'
u_wnd10m_component.units = 'm s**-1'
v_wnd10m_component.units = 'm s**-1'

# add data into variables
 # wind
latitudesWnd[:] = lats1DInv[:]
longitudesWnd[:] = lons1DInv[:]
u_wnd10m_component[:] = uWndConcat[:]
v_wnd10m_component[:] = vWndConcat[:]
timesWnd[:] = tempo[:]
wndDataset.close()


