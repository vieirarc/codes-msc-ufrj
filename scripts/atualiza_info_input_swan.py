# -*- coding: UTF-8 -*-
import os
from netCDF4 import Dataset
from datetime import datetime, timedelta


# reading user input and variables from "roda_sistema_shell.sh" shell script
workDir = os.environ["workdir"]
resultsDir = os.environ["resultsdir"]
simulationName = os.environ["simulation_name"]
filename = os.environ["filename"]

# get 'time' variable in file
datasetWave = Dataset(resultsDir + '/' + simulationName + '/bg/' + filename)
time = datasetWave['time']

# create a list filled with dates
datesList = []
initialDate = datetime(1990, 01, 01, 00)
for i in time:
	i = float(i.data)
	dates = initialDate + timedelta(days=i)
	datesString = dates.strftime("%Y%m%d_%H%M%S")
	datesList.append(datesString)

# getting one field before the starting date
# and dates variables
startingDate = initialDate + timedelta(days=int(time[0].data))
timeResolution = time[2] - time[1] 
timeResolutionSec = 60*60*24*timeResolution # in seconds
firstFieldDateNotString = startingDate - timedelta(seconds=timeResolutionSec) 

# variables
firstFieldDate = firstFieldDateNotString.strftime("%Y%m%d")
firstFieldTime = firstFieldDateNotString.strftime("%H%M%S")
startingDate = datesList[0][0:8]
startingTime = datesList[0][9:13]
endingDate = datesList[-1][0:8] # last field (or element) of this list
endingTime = datesList[-1][9:15] # last field (or element) of this list
finalField = time.size
timeResolutionSec = timeResolutionSec # just to organize all the variables block! 


with open(workDir + '/swan/swan_input_hindcast.swn', 'r') as file:
	data = file.readlines()



data[63] = 'BLO \'COMPGRID\' NOHEADER \'swan.' + startingDate[0:6] + '_hs.mat\' LAY 4 HS 1 OUTPUT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec\n'

data[64] = 'BLO \'COMPGRID\' NOHEADER \'swan.' + startingDate[0:6] + '_dir.mat\' LAY 4 DIR 1 OUTPUT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec\n'

data[65] = 'BLO \'COMPGRID\' NOHEADER \'swan.' + startingDate[0:6] + '_per.mat\' LAY 4 PER 1 OUTPUT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec\n'

data[66] = 'BLO \'COMPGRID\' NOHEADER \'swan.' + startingDate[0:6] + '_total_energy.mat\' LAY 4 GENERAT 1 OUTPUT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec\n'

data[67] = 'BLO \'COMPGRID\' NOHEADER \'swan.' + startingDate[0:6] + '_transp_energy.mat\' LAY 4 TRANSP 1 OUTPUT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec\n'


data[69] = 'COMP NONSTAT ' + firstFieldDate + '.' + firstFieldTime + ' ' + str(timeResolutionSec) + ' Sec ' + endingDate + '.' + endingTime + '\n'





with open(workDir + '/swan/swan_input_hindcast.swn', 'w') as file:
	file.writelines(data)

