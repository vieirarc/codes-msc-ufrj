import os
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
import collections
import scipy.io as sio 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


rj4 = np.genfromtxt('/home/piatam8/ww3/ww3_shell/modelo_hindcast/validation/buoy_data/SIMCOSTA_RJ-4_OCEAN_2017-08-27_2019-10-19.dat')
datasetTp = Dataset('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_tp.nc')

lats = datasetTp['latitude'][:]
lons = datasetTp['longitude'][:]
lon, lat = np.meshgrid(lons, lats)

coastline = sio.loadmat('/home/piatam8/ww3/ww3_shell/modelo_hindcast/swan/coastline_bg.mat')
costaLat = coastline['lat']
costaLon = coastline['lon']


# *********** BUOY RJ4 *********** #
tpBuoyDictInit = {}

for i in rj4[1::]:
	if i[4] == 55 or i[4] == 53: # selecting only the fields of 55' and 53'
		yearInt = int(i[0])
		monthInt = int(i[1])
		dayInt = int(i[2])
		hourInt = int(i[3])
		minuteInt = int(i[4])
		tp = i[7]
		tpRound = round(tp,2)
		dateKeys = datetime(yearInt, monthInt, dayInt, hourInt, minuteInt)
		dateKeyNames = dateKeys.strftime('%Y%m%d_%H%M')
		tpBuoyDictInit["{0}".format(dateKeyNames)] = tpRound  # dictionary
		
tpBuoyDict = collections.OrderedDict(sorted(tpBuoyDictInit.items()))



# *********** SWAN RESULTS *********** #

# ***** TP *****
# create a list of months	
tempo = datasetTp['time']
datesList = []
initialDate = datetime(1990, 01, 01, 00, 00)
for i in tempo:
        dates = initialDate + timedelta(days=i)
        datesString = dates.strftime('%Y%m%d_%H%M')
        datesList.append(datesString)


# exracting info from an specific point (buoy location) 
tpResults = datasetTp['tp']
tpPointResultsDict = {}

for index, name in enumerate(datesList):
	tpField = tpResults[index,:,:]
	#tpFieldFlip = tpField[::-1]
	tpPointResults = tpField[131, 181]
	tpPointResultsRound = round(tpPointResults,2)
	tpPointResultsDict["{0}".format(name)] = tpPointResultsRound  # dictionary

tpSwanDict = collections.OrderedDict(sorted(tpPointResultsDict.items()))


# *********** applying a filter to the swan results ************
tpBuoyFinalDict = {}
tpSwanFinalDict = {}

for k, v in tpBuoyDict.items():
	keyDateBuoy = datetime.strptime(k, '%Y%m%d_%H%M')
	if keyDateBuoy.minute == 53:
		newDate = keyDateBuoy + timedelta(minutes=7)
	else:
		newDate = keyDateBuoy + timedelta(minutes=5)
	for k2, v2 in tpSwanDict.items():
		keyDateSwan = datetime.strptime(k2, '%Y%m%d_%H%M')
		if newDate == keyDateSwan:
			tpSwanFinalDict["{0}".format(k2)] = v2
			newDateString = newDate.strftime('%Y%m%d_%H%M')
			tpBuoyFinalDict["{0}".format(newDateString)] = v
			print '*** Field in concordance: ' + newDateString
		else:
			continue
	print '*** ### ***'

tpBuoyFinalDictOrdered = collections.OrderedDict(sorted(tpBuoyFinalDict.items()))
tpSwanFinalDictOrdered = collections.OrderedDict(sorted(tpSwanFinalDict.items()))

# removing 'nan' values
# TP
for k3, v3 in tpBuoyFinalDictOrdered.items():
	if np.isnan(v3) == True:
		del tpBuoyFinalDictOrdered[k3]
		del tpSwanFinalDictOrdered[k3]


# defining the seasons

# 2017
Summer2017 = datetime(2017, 1, 1, 00)
Autumn2017 = datetime(2017, 3, 21, 00)
Winter2017 = datetime(2017, 6, 21, 00)
Spring2017 = datetime(2017, 9, 21, 00)

# 2018
Summer2018 = datetime(2017, 12, 21, 00)
Autumn2018 = datetime(2018, 3, 21, 00)
Winter2018 = datetime(2018, 6, 21, 00)
Spring2018 = datetime(2018, 9, 21, 00)
Spring2018Final = datetime(2018, 12, 20, 00)

Summer2017Buoy = {} 
Autumn2017Buoy = {}
Winter2017Buoy = {}
Spring2017Buoy = {}
Spring2017Buoy = {}

Summer2017Swan = {} 
Autumn2017Swan = {}
Winter2017Swan = {}
Spring2017Swan = {}
Spring2017Swan = {}

Summer2018Buoy = {}
Autumn2018Buoy = {}
Winter2018Buoy = {}
Spring2018Buoy = {}
Spring2018Buoy = {}

Summer2018Swan = {}
Autumn2018Swan = {}
Winter2018Swan = {}
Spring2018Swan = {}
Spring2018Swan = {}


# creating season dictionaries
for (k, v), (k2, v2) in zip(tpBuoyFinalDictOrdered.items(), tpSwanFinalDictOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	if Summer2017 <= keyDate < Autumn2017:
		Summer2017Buoy["{0}".format(k)] = v
		Summer2017Swan["{0}".format(k2)] = v2
	elif Autumn2017 <= keyDate < Winter2017:
		Autumn2017Buoy["{0}".format(k)] = v
		Autumn2017Swan["{0}".format(k2)] = v2
	elif Winter2017 <= keyDate < Spring2017:
		Winter2017Buoy["{0}".format(k)] = v
		Winter2017Swan["{0}".format(k2)] = v2
	elif Spring2017 <= keyDate < Summer2018:
		Spring2017Buoy["{0}".format(k)] = v
		Spring2017Swan["{0}".format(k2)] = v2
	elif Summer2018 <= keyDate < Autumn2018:
		Summer2018Buoy["{0}".format(k)] = v
		Summer2018Swan["{0}".format(k2)] = v2
	elif Autumn2018 <= keyDate < Winter2018:
		Autumn2018Buoy["{0}".format(k)] = v
		Autumn2018Swan["{0}".format(k2)] = v2
	elif Winter2018 <= keyDate < Spring2018:
		Winter2018Buoy["{0}".format(k)] = v
		Winter2018Swan["{0}".format(k2)] = v2
	elif Spring2018 <= keyDate < Spring2018Final:
		Spring2018Buoy["{0}".format(k)] = v
		Spring2018Swan["{0}".format(k2)] = v2
	else:
		continue


# ordered dicts
Summer2017BuoyOrdered = collections.OrderedDict(sorted(Summer2017Buoy.items()))
Autumn2017BuoyOrdered = collections.OrderedDict(sorted(Autumn2017Buoy.items()))
Winter2017BuoyOrdered = collections.OrderedDict(sorted(Winter2017Buoy.items()))
Spring2017BuoyOrdered = collections.OrderedDict(sorted(Spring2017Buoy.items()))

Summer2017SwanOrdered = collections.OrderedDict(sorted(Summer2017Swan.items()))
Autumn2017SwanOrdered = collections.OrderedDict(sorted(Autumn2017Swan.items()))
Winter2017SwanOrdered = collections.OrderedDict(sorted(Winter2017Swan.items()))
Spring2017SwanOrdered = collections.OrderedDict(sorted(Spring2017Swan.items()))

Summer2018BuoyOrdered = collections.OrderedDict(sorted(Summer2018Buoy.items()))
Autumn2018BuoyOrdered = collections.OrderedDict(sorted(Autumn2018Buoy.items()))
Winter2018BuoyOrdered = collections.OrderedDict(sorted(Winter2018Buoy.items()))
Spring2018BuoyOrdered = collections.OrderedDict(sorted(Spring2018Buoy.items()))

Summer2018SwanOrdered = collections.OrderedDict(sorted(Summer2018Swan.items()))
Autumn2018SwanOrdered = collections.OrderedDict(sorted(Autumn2018Swan.items()))
Winter2018SwanOrdered = collections.OrderedDict(sorted(Winter2018Swan.items()))
Spring2018SwanOrdered = collections.OrderedDict(sorted(Spring2018Swan.items()))


# creating a time series for buoy and swan infos

# creating the lists
Summer2017DateList = []
Autumn2017DateList = []
Winter2017DateList = []
Spring2017DateList = []
Summer2018DateList = []
Autumn2018DateList = []
Winter2018DateList = []
Spring2018DateList = []


Summer2017BuoyList = []
Autumn2017BuoyList = []
Winter2017BuoyList = []
Spring2017BuoyList = []

Summer2018BuoyList = []
Autumn2018BuoyList = []
Winter2018BuoyList = []
Spring2018BuoyList = []

Summer2017SwanList = []
Autumn2017SwanList = []
Winter2017SwanList = []
Spring2017SwanList = []

Summer2018SwanList = []
Autumn2018SwanList = []
Winter2018SwanList = []
Spring2018SwanList = []


# Summer 2017
for (k, v), (k2, v2) in zip(Summer2017BuoyOrdered.items(), Summer2017SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Summer2017DateList.append(keyDate)
	Summer2017BuoyList.append(v)
	Summer2017SwanList.append(v2)

# Autumn 2017
for (k, v), (k2, v2) in zip(Autumn2017BuoyOrdered.items(), Autumn2017SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Autumn2017DateList.append(keyDate)
	Autumn2017BuoyList.append(v)
	Autumn2017SwanList.append(v2)

# Winter 2017
for (k, v), (k2, v2) in zip(Winter2017BuoyOrdered.items(), Winter2017SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Winter2017DateList.append(keyDate)
	Winter2017BuoyList.append(v)
	Winter2017SwanList.append(v2)

# Spring 2017
for (k, v), (k2, v2) in zip(Spring2017BuoyOrdered.items(), Spring2017SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Spring2017DateList.append(keyDate)
	Spring2017BuoyList.append(v)
	Spring2017SwanList.append(v2)

# Summer 2018
for (k, v), (k2, v2) in zip(Summer2018BuoyOrdered.items(), Summer2018SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Summer2018DateList.append(keyDate)
	Summer2018BuoyList.append(v)
	Summer2018SwanList.append(v2)

# Autumn 2018
for (k, v), (k2, v2) in zip(Autumn2018BuoyOrdered.items(), Autumn2018SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Autumn2018DateList.append(keyDate)
	Autumn2018BuoyList.append(v)
	Autumn2018SwanList.append(v2)

# Winter 2018
for (k, v), (k2, v2) in zip(Winter2018BuoyOrdered.items(), Winter2018SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Winter2018DateList.append(keyDate)
	Winter2018BuoyList.append(v)
	Winter2018SwanList.append(v2)

# Spring 2018
for (k, v), (k2, v2) in zip(Spring2018BuoyOrdered.items(), Spring2018SwanOrdered.items()):
	keyDate = datetime.strptime(k, '%Y%m%d_%H%M')
	Spring2018DateList.append(keyDate)
	Spring2018BuoyList.append(v)
	Spring2018SwanList.append(v2)



# creating graphs
pathSave = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/imagens/simulacao_geral/validacao/RJ-4/tp'

# Summer 2017
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Summer 2017', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Summer2017DateList ,Summer2017BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Summer2017DateList, Summer2017SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '1_time_series_tp_valid_Summer2017'), bbox_inches='tight', dpi=200)
plt.close()

# Autumn 2017
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Autumn 2017', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Autumn2017DateList, Autumn2017BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Autumn2017DateList, Autumn2017SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '2_time_series_tp_valid_Autumn2017'), bbox_inches='tight', dpi=200)
plt.close()

# Winter 2017
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Winter 2017', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Winter2017DateList, Winter2017BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Winter2017DateList, Winter2017SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '3_time_series_tp_valid_Winter2017'), bbox_inches='tight', dpi=200)
plt.close()

# Spring 2017
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Spring 2017', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Spring2017DateList, Spring2017BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Spring2017DateList, Spring2017SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '4_time_series_tp_valid_Spring2017'), bbox_inches='tight', dpi=200)
plt.close()

# Summer 2018
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Summer 2018', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Summer2018DateList, Summer2018BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Summer2018DateList, Summer2018SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '5_time_series_tp_valid_Summer2018'), bbox_inches='tight', dpi=200)
plt.close()

# Autumn 2018
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Autumn 2018', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Autumn2018DateList, Autumn2018BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Autumn2018DateList, Autumn2018SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '6_time_series_tp_valid_Autumn2018'), bbox_inches='tight', dpi=200)
plt.close()


# Winter 2018
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Winter 2018', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Winter2018DateList, Winter2018BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Winter2018DateList, Winter2018SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='best')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '7_time_series_tp_valid_Winter2018'), bbox_inches='tight', dpi=200)
plt.close()

# Spring 2018
fig = plt.gcf()
fig.set_size_inches(23.5, 9.5)
ax = plt.subplot()
ax.grid(True)
ax.set_title(u'Time Series Tp - RJ-4 Buoy - Spring 2018', fontsize=20)
font = {'size':16}
locator = mdates.HourLocator(interval=72)  # every month
dfmt = mdates.DateFormatter('%d%b')

plt.plot(Spring2018DateList, Spring2018BuoyList, color='black', linewidth=2.2, label='RJ-4 Buoy')
plt.plot(Spring2018DateList, Spring2018SwanList, color='green', linewidth=2.2, label='SWAN Simulation')
plt.legend(loc='upper right')

plt.xticks(rotation=45)
plt.ylabel('Peak period (s)', size=16, rotation=90, labelpad=9)

X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(dfmt)
plt.rc('font', **font)
plt.savefig(os.path.join(pathSave, '8_time_series_tp_valid_Spring2018'), bbox_inches='tight', dpi=200)
plt.close()
