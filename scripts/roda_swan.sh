#!/bin/bash

export PY_dir=/home/oceano/anaconda2
export PATH="$PATH:$PY_dir/bin"
export swan_dir=/home/oceano/SWAN/swan4131/
export PATH="$PATH:$swan_dir"

# variavel "simulation_name" eh criada no script principal (hindcast_ondas.sh)
export workdir=/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast
export resultsdir=/storage/oceano/rafael/wavewatch3_results/hindcast
ww3_grid_bg='bg'
read -p "Simulation Name (with no space between words!): " simulation_name
export $simulation_name

# define function "ordinal" for masseges
function ordinal () {
  case "$1" in
    *1[0-9] | *[04-9]) echo "$1"th;;
    *1) echo "$1"st;;
    *2) echo "$1"nd;;
    *3) echo "$1"rd;;
  esac
}


# loop through files in folder
for filename in /storage/oceano/rafael/wavewatch3_results/hindcast/teste_1/$ww3_grid_bg/*_hs.nc;
do
	export filename=${filename:62:17}
	cd $resultsdir/teste_1/bg/
	# atualiza input file swan
	ipython /home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/scripts/atualiza_info_input_swan.py
	echo "Swan input file updated!"
	# Gera arquivos TPAR
	ipython /home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/swan/escreve_TPAR_mered_leste.py
	ipython /home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/swan/escreve_TPAR_mered_oeste.py
	ipython /home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast/swan/escreve_TPAR_zonal.py
	echo "TPAR files created!"
	# roda SWAN
	cd $workdir/swan
	swanrun -input $workdir/swan/swan_input_hindcast.swn
	echo "SWAN simulation for ${filename:4:6} is finished!"
	mv swan_input_hindcast.prt $resultsdir/$simulation_name/swan-BG/swan_prt_${filename:4:6}.prt
	mv swan.${filename:4:6}_hs.mat $resultsdir/$simulation_name/swan-BG
	mv swan.${filename:4:6}_dir.mat $resultsdir/$simulation_name/swan-BG
	mv swan.${filename:4:6}_per.mat $resultsdir/$simulation_name/swan-BG
	mv swan.${filename:4:6}_total_energy.mat $resultsdir/$simulation_name/swan-BG
	mv swan.${filename:4:6}_transp_energy.mat $resultsdir/$simulation_name/swan-BG
done
