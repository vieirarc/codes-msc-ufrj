#!/bin/bash


# ******************************* MAKE NETCDF RESULTS ****************************** #
#																					 #
# This script runs all the python routines responsible for converting results        #
# from ".mat" to "netCDF"   														 #
# ********************************************************************************** #


export workdir=/home/piatam8/ww3/ww3_shell/modelo_hindcast

cd $workdir/scripts

ipython cria_netCDF_dir_geral.py
echo " *** NetCDF Wdir file is done! ***"

ipython cria_netCDF_energyTransp_geral.py
echo " *** NetCDF energyTransp file is done! ***"

ipython cria_netCDF_hs_geral.py
echo " *** NetCDF Hs file is done! ***"

ipython cria_netCDF_tp_geral.py
echo " *** NetCDF Tp file is done! ***"

echo " ************* End of Program *************"

