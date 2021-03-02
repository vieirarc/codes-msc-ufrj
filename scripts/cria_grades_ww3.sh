#!/bin/bash

# comentarios
export workdir=/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast

cd $workdir/fix/

# prepara grade global   **** a grade não muda em funcao dos dias!
rm -f ww3_grid.inp
ln -s ww3_grid.inp.global ww3_grid.inp
/home/oceano/WW3-v6.07/model/exe/ww3_grid
mv -f "mod_def.ww3" "mod_def.global"

# prepara grade Atlantico Sul    **** a grade não muda em funcao dos dias!
rm -f ww3_grid.inp
ln -s ww3_grid.inp.southatl ww3_grid.inp
/home/oceano/WW3-v6.07/model/exe/ww3_grid
mv -f "mod_def.ww3" "mod_def.southatl"

# prepara grade RJ
rm -f ww3_grid.inp
ln -s ww3_grid.inp.grade_rj ww3_grid.inp
/home/oceano/WW3-v6.07/model/exe/ww3_grid
mv -f "mod_def.ww3" "mod_def.grade_rj"

# prepara grade BG
rm -f ww3_grid.inp
ln -s ww3_grid.inp.grade_bg ww3_grid.inp
/home/oceano/WW3-v6.07/model/exe/ww3_grid
mv -f "mod_def.ww3" "mod_def.grade_bg"

# *** prepara as forcantes ***
# grades das forcantes      **** a grade não muda em funcao dos dias!
rm -f ww3_grid.inp
ln -s ww3_grid.inp.cfsr ww3_grid.inp
/home/oceano/WW3-v6.07/model/exe/ww3_grid 
mv -f "mod_def.ww3" "mod_def.cfsr"
