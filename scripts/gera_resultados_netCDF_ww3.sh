#!/bin/bash

# the "simulation_name" variable is created in the main script (roda_sistema_hindcast)

export workdir=/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast

# create necessary links for global grid
cd $resultsdir/$simulation_name/restart
rm -f mod_def.ww3 out_grd.ww3
ln -s $workdir/fix/mod_def.global mod_def.ww3
ln -s out_grd.global out_grd.ww3
ln -s $resultsdir/work/ww3_ounf.inp ww3_ounf.inp

# gera netcdf's grade global
/home/oceano/WW3-v6.07/model/exe/ww3_ounf
mv -f *.nc $resultsdir/$simulation_name/global/

# cria links necessarios para grade atlSul
rm -f mod_def.ww3 out_grd.ww3 out_pnt.ww3 ww3_ounp.inp
ln -s $workdir/fix/mod_def.southatl mod_def.ww3
ln -s out_grd.southatl out_grd.ww3
ln -s out_pnt.southatl out_pnt.ww3
ln -s $resultsdir/work/ww3_ounp.inp ww3_ounp.inp

# gera netcdf's grade atlSul
/home/oceano/WW3-v6.07/model/exe/ww3_ounf
/home/oceano/WW3-v6.07/model/exe/ww3_ounp  # ***** Gera resultados dos pontos especificos! *****
mv -f *.nc $resultsdir/$simulation_name/south_atlantic

# cria links necessarios para grade RJ
rm -f mod_def.ww3 out_grd.ww3
ln -s $workdir/fix/mod_def.grade_rj mod_def.ww3
ln -s out_grd.grade_rj out_grd.ww3
#ln -s out_pnt.grade_rj out_pnt.ww3
#ln -s $resultsdir/work/ww3_ounp.inp ww3_ounp.inp

# gera netcdf's grade RJ
/home/oceano/WW3-v6.07/model/exe/ww3_ounf
#/home/oceano/WW3-v6.07/model/exe/ww3_ounp  # ***** Gera resultados dos pontos especificos! *****
mv -f *.nc $resultsdir/$simulation_name/rj

# cria links necessarios para grade BG
rm -f mod_def.ww3 out_grd.ww3
ln -s $workdir/fix/mod_def.grade_bg mod_def.ww3
ln -s out_grd.grade_bg out_grd.ww3
#ln -s out_pnt.grade_bg out_pnt.ww3
#ln -s $resultsdir/work/ww3_ounp.inp ww3_ounp.inp

# gera netcdf's grade BG
/home/oceano/WW3-v6.07/model/exe/ww3_ounf
#/home/oceano/WW3-v6.07/model/exe/ww3_ounp  # ***** Gera resultados dos pontos especificos! *****
mv -f *.nc $resultsdir/$simulation_name/bg
