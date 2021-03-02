# -*- coding: UTF-8 -*-
import os
from os import listdir
from netCDF4 import Dataset
import numpy as numpy
from datetime import datetime, timedelta

# import shell variable used in "for" loop (i)
fileName = os.environ["filename"]


# open files in folder and add names in specifics lists
windNamesList = []
iceNamesList = []

# *WARNING* --> in "roda_sistema_hindcast.sh" the script do 'cd' to "vento_gelo_gfs" directory to run this 
# **FIX IT!!!**    script (extrai_datas.py). The netCDF4.Dataset is not working outside this folder!!!

for file in listdir('.'):
	dataset = Dataset(file)
	if "ice" in file:
		iceNamesList.append(file)
	else:
		windNamesList.append(file)


# turn lists to tuple
windNamesList = tuple(windNamesList)
iceNamesList = tuple(iceNamesList)
windNamesList = " ".join(windNamesList)
iceNamesList = " ".join(iceNamesList)


# get 'time' variable in file
datasetWind = Dataset('/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/vento_gelo_gfs/' + fileName)
time = datasetWind['time']


# create a list filled with dates
datesList = []
initialDate = datetime(1900, 01, 01, 00)
for i in time:
	i = int(i)
	dates = initialDate + timedelta(hours=i)
	datesString = dates.strftime("%Y%m%d_%H%M%S")
	datesList.append(datesString)

# getting one field before the starting date
# and dates variables
startingDate = initialDate + timedelta(hours=int(time[0].data))
timeResolution = time[2] - time[1] # in hours
timeResolution = int(timeResolution)
timeResolutionSec = 60*60*timeResolution # in seconds
firstFieldDateNotString = startingDate - timedelta(seconds=timeResolutionSec) 

# variables
firstFieldDate = firstFieldDateNotString.strftime("%Y%m%d")
firstFieldTime = firstFieldDateNotString.strftime("%H%M%S")
startingDate = datesList[0][0:8]
startingTime = datesList[0][9:13]
endingDate = datesList[-1][0:8] # last field (or element) of this list
endingTime = datesList[-1][9:15] # last field (or element) of this list
finalField = time.size
timeResolutionSec = timeResolutionSec # just to organize the variables block! 

# create a shell script .sh infofile
# writing in file
infoFile = open("/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/scripts/info_vento_gelo.sh", "w")
infoFile.write("#!/bin/bash")
infoFile.write("\n")
infoFile.write("\n")
infoFile.write("#      *** Infromation file from wind fields ***    ")
infoFile.write("\n")
infoFile.write("\n")

# infoFile.write("wind_files=(%s) " % (windNamesList))
# infoFile.write("\n")
# infoFile.write("\n")

# infoFile.write("ice_files=(%s) " % (iceNamesList))
# infoFile.write("\n")
# infoFile.write("\n")

infoFile.write("# First field date")
infoFile.write("\n")
infoFile.write("export first_field_date='%s' " % (firstFieldDate))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# First field time")
infoFile.write("\n")
infoFile.write("export first_field_time='%s' " % (firstFieldTime))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Starting date")
infoFile.write("\n")
infoFile.write("export starting_date='%s' " % (startingDate))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Starting time")
infoFile.write("\n")
infoFile.write("export starting_time='%s' " % (startingTime))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Ending date")
infoFile.write("\n")
infoFile.write("export ending_date='%s' " % (endingDate))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Ending time")
infoFile.write("\n")
infoFile.write("export ending_time='%s' " % (endingTime))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Time resolution (in seconds)")
infoFile.write("\n")
infoFile.write("export time_resolution='%s' " % (timeResolutionSec))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("# Final field (for restart file purposes!)")
infoFile.write("\n")
infoFile.write("export final_field='%s' " % (finalField))
infoFile.write("\n")
infoFile.write("\n")

