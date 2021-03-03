#!/bin/bash


# ********************************* MAKE VALIDATION ******************************** #
#																					 #
# This script runs all the python routines responsible for the model's validation    #
# process.																			 #
# ********************************************************************************** #



export workdir=/home/piatam8/ww3/ww3_shell/modelo_hindcast/validation/scripts-validation


# python scripts validation

# **** RJ-3 Buoy **** #
echo " *** RJ-3 Buoy *** "
echo "."
echo "."
echo "."

ipython $workdir/validation_hs_rj-3.py
echo "Hs time series RJ-3 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_tp_rj-3.py
echo "Tp time series RJ-3 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_dir_rj-3.py
echo "Wdir time series RJ-3 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_statistics_rj-3.py
echo "Statistics table RJ-3 done!"
echo "."
echo "."
echo "."

# **** RJ-4 Buoy**** #
echo " *** RJ-4 Buoy *** "
echo "."
echo "."
echo "."

ipython $workdir/validation_hs_rj-4.py
echo "Hs time series RJ-4 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_tp_rj-4.py
echo "Hs time series RJ-4 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_dir_rj-4.py
echo "Wdir time series RJ-4 done!"
echo "."
echo "."
echo "."

ipython $workdir/validation_statistics_rj-4.py
echo "Statistics table RJ-4 done!"
echo "."
echo "."
echo "."

echo " ______ End of Program ______ "