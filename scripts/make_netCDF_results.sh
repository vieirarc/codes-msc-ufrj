#!/bin/bash


# ******************************* MAKE NETCDF RESULTS ****************************** #
#																					 #
# This script runs all the python routines responsible for converting results        #
# from ".mat" to "netCDF"   														 #
# ********************************************************************************** #


# input by user
#simulation_n	ame = raw_input('Simulation Name: ')


export workdir=/home/piatam8/ww3/ww3_shell/modelo_hindcast


cd $workdir/scripts

ipython cria_netCDF_dir_geral.py
echo " "
echo " "
echo " *** NetCDF Wdir file is done! ***"

ipython cria_netCDF_energyTransp_geral.py
echo " "
echo " "
echo " *** NetCDF energyTransp file is done! ***"

ipython cria_netCDF_hs_geral.py
echo " "
echo " "
echo " *** NetCDF Hs file is done! ***"

ipython cria_netCDF_tp_geral.py
echo " "
echo " "
echo " *** NetCDF Tp file is done! ***"
echo " "
echo " "
echo " ************* End of Program *************"

