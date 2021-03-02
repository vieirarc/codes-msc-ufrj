from netCDF4 import Dataset

from __future__ import division
import datetime
import numpy as np
import collections

# arquivos
u2016Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/uwnd.10m.gauss.2016.nc')
lat = u2016Dataset['lat']
lon = u2016Dataset['lon']
time = u2016Dataset['time']
uWind = u2016Dataset['uwnd'] parei aqui! ****


u2017Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/uwnd.10m.gauss.2017.nc')
u2018Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/uwnd.10m.gauss.2018.nc')

v2016Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/vwnd.10m.gauss.2016.nc')
v2017Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/vwnd.10m.gauss.2017.nc')
v2018Dataset = Dataset('/home/rafael/Desktop/dissertacao/noaa-reanalysis/vwnd.10m.gauss.2018.nc')





# create netcdf file
wndDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/vento_gelo_gfs/wind_ww3.nc', 'w', format='NETCDF3_CLASSIC')
iceDataset = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/vento_gelo_gfs/ice_ww3.nc', 'w', format='NETCDF3_CLASSIC')

# create dimensions
 # wind 
latW = wndDataset.createDimension('latitude', int(lats.attributes['grads_size']))
lonW = wndDataset.createDimension('longitude', int(lons.attributes['grads_size']))
timeW = wndDataset.createDimension('time', int(tempo.attributes['grads_size']))
 # ice
latI = iceDataset.createDimension('latitude', int(lats.attributes['grads_size']))
lonI = iceDataset.createDimension('longitude', int(lons.attributes['grads_size']))
timeI = iceDataset.createDimension('time', int(tempo.attributes['grads_size']))

# create variables
 # wind
latitudesWnd = wndDataset.createVariable('latitude', "f8", ('latitude',))
longitudesWnd = wndDataset.createVariable('longitude', "f8", ('longitude',))
timesWnd = wndDataset.createVariable('time', "f8", ('time',))
 # ice
latitudesIce = iceDataset.createVariable('latitude', "f8", ('latitude',))
longitudesIce = iceDataset.createVariable('longitude', "f8", ('longitude',))
timesIce = iceDataset.createVariable('time', "f8", ('time',))

# create 3D U and V variables
u_wnd10m_component = wndDataset.createVariable('u_wnd10m_component', "f4", ('time', 'latitude', 'longitude'))
v_wnd10m_component = wndDataset.createVariable('v_wnd10m_component', "f4", ('time', 'latitude', 'longitude'))
ice_surface_extent = iceDataset.createVariable('ice_surface_extent', "f4", ('time', 'latitude', 'longitude'))

# global attributes     
wndDataset.description = 'NCEP/NOAA - GFS WIND'
iceDataset.description = 'NCEP/NOAA - Ice Extent'

# variable attributes
 # wind
latitudesWnd.units = 'degree_north'
longitudesWnd.units = 'degree_east'
timesWnd.units = 'days since 0001-01-01 00:00:0.0'
u_wnd10m_component.units = 'm/s'
v_wnd10m_component.units = 'm/s'
 # ice
latitudesIce.units = 'degrees_north'
longitudesIce.units = 'degree_east'
timesIce.units = 'days since 0001-01-01 00:00:0.0'
ice_surface_extent.units = 'Proportion'

# add data into variables
 # wind
latitudesWnd[:] = lats
longitudesWnd[:] = lons
u_wnd10m_component[:] = uComp
v_wnd10m_component[:] = vComp
timesWnd[:] = tempo
wndDataset.close()
 # icecsfc
latitudesIce[:] = lats
longitudesIce[:] = lons
ice_surface_extent[:] = iceCfsr
timesIce[:] = tempo
iceDataset.close()
