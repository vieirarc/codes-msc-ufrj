# -*- coding: UTF-8 -*-

from os import listdir
from netCDF4 import Dataset
import numpy as numpy
from datetime import datetime, timedelta


# open files in folder and add names in specifics lists
windNamesList = []
iceNamesList = []

# *WARNING* --> in "roda_sistema_hindcast.sh" the script do 'cd' to "vento_gelo_gfs" directory to run this 
# **FIX IT!!!**    script (extrai_datas.py). The netCDF4.Dataset is not working outside this folder!!!

for file in listdir('.'):
	if "ice" in file:
		iceNamesList.append(file)
	else:
		windNamesList.append(file)


# turn lists to tuple
windNamesList = tuple(windNamesList)
iceNamesList = tuple(iceNamesList)
windNamesList = " ".join(windNamesList)
iceNamesList = " ".join(iceNamesList)


# create a shell script with the names lists
# writing in file
infoFile = open("/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/scripts/listas_nomes.sh", "w")
infoFile.write("#!/bin/bash")
infoFile.write("\n")
infoFile.write("\n")
infoFile.write("#      *** Infromation file from wind fields ***    ")
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("wind_files=(%s) " % (windNamesList))
infoFile.write("\n")
infoFile.write("\n")

infoFile.write("ice_files=(%s) " % (iceNamesList))
infoFile.write("\n")
infoFile.write("\n")
