import pygrib 
import numpy as np
from netCDF4 import Dataset
from os import listdir

# acessa os arquivos 
grbs2016 = pygrib.open('era5_2016_december.grib')
grbs2017 = pygrib.open('era5_2017.grib')
grbs2018 = pygrib.open('era5_2018.grib')

# lista com grib messages
uGrd10m2016 = grbs2016.select(name='10 metre U wind component')

# criando dicionarios com valores
uDict = {}
vDict = {}
iceDict = {}

for i in np.arange(0, 743):
	uGrd10m2016Fild = grbs2016.select(name='10 metre U wind component')[i]
	print 'Feito index ', i
	uGrd10m2016Values = uGrd10m2016Fild.values
	print 'Feito values ', i
	uGrd10m2016Names = uGrd10m2016[i]
	uGrd10m2016Names = str(uGrd10m2016Names) # *****[94:106]
	print 'Feito Name ', i
	uDict["u_{0}".format(uGrd10m2016Names[94:106])] = uGrd10m2016Values[::-1] # inverse U array
	print 'Feito Dict u ', i


	vDict["v_grd10m_{0}".format(uGrd10m2016Names[94:106])]= vGrd10m2016_field[::-1] # inverse V array
	iceDict["ice_cover_{0}".format(uGrd10m2016Names[94:106])]= seaIce2016_field[::-1] # inverse V array




***************************************************************************************



vGrd10m2016 = grbs2016.select(name='10 metre V wind component')[0]
seaIce2016 = grbs2016.select(name='Sea-ice cover')[0]

uGrd10m2016Values = uGrd10m2016.values
vGrd10m2016Values = vGrd10m2016.values
seaIce2016Values = seaIce2016.values

uDict = {}
vDict = {}
iceDict = {}

uDict["u_grd10m_{0}".format(file[22:24])] = uGrd10m2016_field[::-1] # inverse U array 
vDict["v_grd10m_{0}".format(file[22:24])]= vGrd10m2016_field[::-1] # inverse V array
iceDict["ice_cover_{0}".format(file[22:24])]= seaIce2016_field[::-1] # inverse V array





# ***********************************************************
grbs2017 = pygrib.open('era5_2017.grib')




grbs2018 = pygrib.open('era5_2018.grib')


