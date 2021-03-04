from __future__ import division
import os
import collections
import math
import numpy as np
import scipy.io as sio
from netCDF4 import Dataset
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt



rj4 = np.genfromtxt('/home/piatam8/ww3/ww3_shell/modelo_hindcast/validation/buoy_data/SIMCOSTA_RJ-4_OCEAN_2017-08-27_2019-10-19.dat')
datasetHs = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_hs.nc')
datasetTp = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_tp.nc')



lats = datasetHs['latitude'][:]
lons = datasetHs['longitude'][:]
lon, lat = np.meshgrid(lons, lats)

coastline = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/coastline_bg.mat')
costaLat = coastline['lat']
costaLon = coastline['lon']


# *********** BUOY RJ4 *********** #
hsBuoyDictInit = {}
tpBuoyDictInit = {}

for i in rj4[1::]:
	if i[4] == 55 or i[4] == 53: # selecting only the fields of 55' and 53'
		yearInt = int(i[0])
		monthInt = int(i[1])
		dayInt = int(i[2])
		hourInt = int(i[3])
		minuteInt = int(i[4])
		hs = i[6]
		tp = i[7]
		hsRound = round(hs, 2)
		tpRound = round(tp, 2)
		dateKeys = datetime(yearInt, monthInt, dayInt, hourInt, minuteInt)
		dateKeyNames = dateKeys.strftime('%Y%m%d_%H%M')
		hsBuoyDictInit["{0}".format(dateKeyNames)] = hsRound  # dictionary
		tpBuoyDictInit["{0}".format(dateKeyNames)] = tpRound  # dictionary

		
hsBuoyDict = collections.OrderedDict(sorted(hsBuoyDictInit.items()))
tpBuoyDict = collections.OrderedDict(sorted(tpBuoyDictInit.items()))


# *********** SWAN RESULTS *********** #

# ***** HS and TP *****
# create a list of months	
tempo = datasetHs['time']
datesList = []
initialDate = datetime(1990, 01, 01, 00, 00)
for i in tempo:
        dates = initialDate + timedelta(days=i)
        datesString = dates.strftime('%Y%m%d_%H%M')
        datesList.append(datesString)


# exracting info from an specific grid point (buoy location) 
hsResults = datasetHs['hs']
tpResults = datasetTp['tp']
hsPointResultsDict = {}
tpPointResultsDict = {}

for index, name in enumerate(datesList):
	hsField = hsResults[index,:,:]
	tpField = tpResults[index,:,:]
	hsPointResults = hsField[131, 181]
	tpPointResults = tpField[131, 181]
	hsPointResultsRound = round(hsPointResults, 2)
	tpPointResultsRound = round(tpPointResults, 2)
	hsPointResultsDict["{0}".format(name)] = hsPointResultsRound  # dictionary
	tpPointResultsDict["{0}".format(name)] = tpPointResultsRound  # dictionary

hsSwanDict = collections.OrderedDict(sorted(hsPointResultsDict.items()))
tpSwanDict = collections.OrderedDict(sorted(tpPointResultsDict.items()))


# *********** applying a filter in the swan results ************
hsBuoyFinalDict = {}
hsSwanFinalDict = {}

tpBuoyFinalDict = {}
tpSwanFinalDict = {}

for (k, v), (k4, v4) in zip(hsBuoyDict.items(), tpBuoyDict.items()):
	keyDateBuoy = datetime.strptime(k, '%Y%m%d_%H%M')
	if keyDateBuoy.minute == 53:
		newDate = keyDateBuoy + timedelta(minutes=7)
	else:
		newDate = keyDateBuoy + timedelta(minutes=5)
	for (k2, v2), (k3, v3) in zip(hsSwanDict.items(), tpSwanDict.items()):
		keyDateSwanHs = datetime.strptime(k2, '%Y%m%d_%H%M')
		keyDateSwanTp = datetime.strptime(k3, '%Y%m%d_%H%M')
		if newDate == keyDateSwanHs == keyDateSwanTp:
			hsSwanFinalDict["{0}".format(k2)] = v2
			tpSwanFinalDict["{0}".format(k3)] = v3
			newDateString = newDate.strftime('%Y%m%d_%H%M')
			hsBuoyFinalDict["{0}".format(newDateString)] = v
			tpBuoyFinalDict["{0}".format(newDateString)] = v4
			print '*** Field in concordance: ' + newDateString
		else:
			continue
	print '*** End of loop interaction ***'

hsBuoyFinalDictOrdered = collections.OrderedDict(sorted(hsBuoyFinalDict.items()))
hsSwanFinalDictOrdered = collections.OrderedDict(sorted(hsSwanFinalDict.items()))

tpBuoyFinalDictOrdered = collections.OrderedDict(sorted(tpBuoyFinalDict.items()))
tpSwanFinalDictOrdered = collections.OrderedDict(sorted(tpSwanFinalDict.items()))

# removing 'nan' values
# HS
for k, v in hsBuoyFinalDictOrdered.items():
	if np.isnan(v) == True:
		del hsBuoyFinalDictOrdered[k]
		del hsSwanFinalDictOrdered[k]

# TP
for k3, v3 in tpBuoyFinalDictOrdered.items():
	if np.isnan(v3) == True:
		del tpBuoyFinalDictOrdered[k3]
		del tpSwanFinalDictOrdered[k3]

# ***** Statistics ***** #

# Mean HS  of RJ-3 buoy
sumHsXi = 0

for k, v in hsBuoyFinalDictOrdered.items():
	sumHsXi = sumHsXi + v
Rj4HsXm = (1/len(hsBuoyFinalDictOrdered))*sumHsXi


# Mean TP  of RJ-3 buoy
sumTpXi = 0

for k, v in tpBuoyFinalDictOrdered.items():
	sumTpXi = sumTpXi + v
Rj4TpXm = (1/len(tpBuoyFinalDictOrdered))*sumTpXi


# Mean of HS SWAN simulation
sumHsYi = 0

for k2, v2 in hsSwanFinalDictOrdered.items():
	sumHsYi = sumHsYi + v2
SwanHsYm = (1/len(hsSwanFinalDictOrdered))*sumHsYi


# Mean of TP SWAN simulation
sumTpYi = 0

for k3, v3 in tpSwanFinalDictOrdered.items():
	sumTpYi = sumTpYi + v3
SwanTpYm = (1/len(tpSwanFinalDictOrdered))*sumTpYi


# BiasHs (SWAN_Hs - BUOY) of RJ-3 Buoy
sumHsXiYi = 0

for (k, v), (k2, v2) in zip(hsBuoyFinalDictOrdered.items(), hsSwanFinalDictOrdered.items()):
	XiYi = (v2 - v)
	sumHsXiYi = sumHsXiYi + XiYi
biasHs = (1/len(hsBuoyFinalDictOrdered))*sumHsXiYi


# BiasTp (SWAN_Tp - BUOY) of RJ-3 Buoy
sumTpXiYi = 0

for (k, v), (k2, v2) in zip(tpBuoyFinalDictOrdered.items(), tpSwanFinalDictOrdered.items()):
	XiYi = (v2 - v)
	sumTpXiYi = sumTpXiYi + XiYi
biasTp = (1/len(tpBuoyFinalDictOrdered))*sumTpXiYi


# RMSE HS
sumHsXiYiB = 0

for (k, v), (k2, v2) in zip(hsBuoyFinalDictOrdered.items(), hsSwanFinalDictOrdered.items()):
	XiYiB = (v2 - v - biasHs)**2
	sumHsXiYiB = sumHsXiYiB + XiYiB
RMSE_Hs = math.sqrt((1/(len(hsBuoyFinalDictOrdered) - 1))*sumHsXiYiB)


# RMSE TP
sumTpXiYiB = 0

for (k, v), (k2, v2) in zip(tpBuoyFinalDictOrdered.items(), tpSwanFinalDictOrdered.items()):
	XiYiB = (v2 - v - biasTp)**2
	sumTpXiYiB = sumTpXiYiB + XiYiB
RMSE_Tp = math.sqrt((1/(len(tpBuoyFinalDictOrdered) - 1))*sumTpXiYiB)


# Scatter Index HS
SI_Hs = RMSE_Hs/Rj4HsXm

# Scatter Index TP
SI_Tp = RMSE_Tp/Rj4TpXm


# Symmetric Slope HS 

sumHsXiSqrt = 0
sumHsYiSqrt = 0

for (k, v), (k2, v2) in zip(hsBuoyFinalDictOrdered.items(), hsSwanFinalDictOrdered.items()):
	sumHsXiSqrt = sumHsXiSqrt + v**2    # Buoy data
	sumHsYiSqrt = sumHsYiSqrt + v2**2   # SWAN results
symR_Hs = math.sqrt(sumHsYiSqrt/sumHsXiSqrt)


# Symmetric Slope Tp

sumTpXiSqrt = 0
sumTpYiSqrt = 0

for (k, v), (k2, v2) in zip(tpBuoyFinalDictOrdered.items(), tpSwanFinalDictOrdered.items()):
	sumTpXiSqrt = sumTpXiSqrt + v**2
	sumTpYiSqrt = sumTpYiSqrt + v2**2
symR_Tp = math.sqrt(sumTpYiSqrt/sumTpXiSqrt)


# Correlation Coefficient HS
sumHsXYMult = 0
sumHsXiXmSqrt = 0
sumHsYiYmSqrt = 0

for (k, v), (k2, v2) in zip(hsBuoyFinalDictOrdered.items(), hsSwanFinalDictOrdered.items()):
	XiXm = v - Rj4HsXm
	YiYm = v2 - SwanHsYm
	XYMult = XiXm*YiYm
	sumHsXYMult = sumHsXYMult + XYMult # numerator
	XiXmSqrt = XiXm**2
	YiYmSqrt = YiYm**2
	sumHsXiXmSqrt = sumHsXiXmSqrt + XiXmSqrt
	sumHsYiYmSqrt = sumHsYiYmSqrt + YiYmSqrt
sqrtRootsumXiXmSqrt = math.sqrt(sumHsXiXmSqrt)
sqrtRootsumYiYmSqrt = math.sqrt(sumHsYiYmSqrt)
denominator = sqrtRootsumXiXmSqrt*sqrtRootsumYiYmSqrt
corrHs = sumHsXYMult/denominator


# Correlation Coefficient TP
sumTpXYMult = 0
sumTpXiXmSqrt = 0
sumTpYiYmSqrt = 0

for (k, v), (k2, v2) in zip(tpBuoyFinalDictOrdered.items(), tpSwanFinalDictOrdered.items()):
	XiXm = v - Rj4TpXm
	YiYm = v2 - SwanTpYm
	XYMult = XiXm*YiYm
	sumTpXYMult = sumTpXYMult + XYMult # numerator
	XiXmSqrt = XiXm**2
	YiYmSqrt = YiYm**2
	sumTpXiXmSqrt = sumTpXiXmSqrt + XiXmSqrt
	sumTpYiYmSqrt = sumTpYiYmSqrt + YiYmSqrt
sqrtRootsumXiXmSqrt = math.sqrt(sumTpXiXmSqrt)
sqrtRootsumYiYmSqrt = math.sqrt(sumTpYiYmSqrt)
denominator = sqrtRootsumXiXmSqrt*sqrtRootsumYiYmSqrt
corrTp = sumTpXYMult/denominator


# creating table
f = open("/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/imagens/simulacao_geral/validacao/RJ-4/statistics_table/statistics_table_RJ-4_buoy.txt", "w")

f.write('\n')
f.write('****** Statistics for RJ-4 Buoy - Hs and Tp ******')
f.write('\n')
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('Mean Hs Buoy: ', Rj4HsXm)
f.write('\n')
f.write('Mean Hs SWAN: ', SwanHsYm)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('Mean Tp Buoy: ', Rj4TpXm)
f.write('\n')
f.write('Mean Tp SWAN: ', SwanTpYm)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('Bias Hs: ', biasHs)
f.write('\n')
f.write('Bias Tp: ', biasTp)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('RMSE Hs: ', RMSE_Hs)
f.write('\n')
f.write('RMSE Tp: ', RMSE_Tp)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('SI Hs - Scatter Index: ', SI_Hs)
f.write('\n')
f.write('SI Tp - Scatter Index: ', SI_Tp)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('Sym r Hs - Symmetric Slope: ', symR_Hs)
f.write('\n')
f.write('Sym r Tp - Symmetric Slope: ', symR_Tp)
f.write('\n')
f.write('__________________________________________________')
f.write('\n')
f.write('Corr Hs - Correlation Coefficient: ', corrHs)
f.write('\n')
f.write('Corr Tp - Correlation Coefficient: ', corrTp)
f.write('\n')
f.write('__________________________________________________')
f.close()

