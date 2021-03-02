#!/bin/bash
export PY_dir=/home/oceano/anaconda2
export PATH="$PATH:$PY_dir/bin"
export swan_dir=/home/oceano/SWAN/swan4131
export PATH="$PATH:$swan_dir"

# future input by user
export workdir=/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast
export resultsdir="/storage/oceano/rafael/wavewatch3_results/hindcast"


# input by user
read -p "Simulation Name (with no space between words!): " simulation_name
echo ' '
echo ' '

export simulation_name

# generates the variables shell file  *** FIX IT! *** --> it's not working outside the 'vento_gelo_gfs'
cd $workdir/vento_gelo_gfs # it goes to 'vento_gelo_gfs' and then the script works...
ipython $workdir/scripts/cria_listas_filenames.py
cd $workdir/scripts # it gets back to 'scripts'...
chmod 777 listas_nomes.sh
source listas_nomes.sh # source it to be able of reading in python (in cria_imagens_shell....py)!


# generating grids
./cria_grades_ww3.sh >& log_grades.txt

# create necessary directories
./cria_diretorios.sh >& log_diretorios.txt


# define function "ordinal" for masseges
function ordinal () {
  case "$1" in
    *1[0-9] | *[04-9]) echo "$1"th;;
    *1) echo "$1"st;;
    *2) echo "$1"nd;;
    *3) echo "$1"rd;;
  esac
}

# moving the "work" directory to results directory. It will be back to "workdir" when the "for" loop
# is will be ended. It's to generate the larger outputs in another disk!
mv $workdir/work $resultsdir

# *********** starting "for" interaction ********************

for i in ${!wind_files[@]}
do
	filename=${wind_files[$i]}
	export filename
	# *****************
	# generates the variables shell file  *** FIX IT! ***
	cd $workdir/vento_gelo_gfs # it goes to 'vento_gelo_gfs' and then the script works...
	ipython $workdir/scripts/extrai_datas.py
	cd $workdir/scripts # it gets back to 'scripts'...
	chmod 777 info_vento_gelo.sh
	source info_vento_gelo.sh # source it to be able of reading in python (in cria_imagens_shell....py)!
	# *****************
	# update dates in WaveWatch III **ww3_multi.inp.hindcast** file
	# ---> setting variables
	line_11_hindcast="   $first_field_date $first_field_time $ending_date $ending_time"
	line_15_hindcast="   $first_field_date $first_field_time   $time_resolution  $ending_date $ending_time"
	line_30_hindcast="   $first_field_date $first_field_time       0   $ending_date $ending_time"
	line_31_hindcast="   $first_field_date $first_field_time       $time_resolution   $ending_date $ending_time"
	# ---> updating lines
	sed -i "11s/.*/$line_11_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "15s/.*/$line_15_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "19s/.*/$line_15_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "30s/.*/$line_30_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "31s/.*/$line_31_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "32s/.*/$line_30_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	sed -i "33s/.*/$line_30_hindcast/" $resultsdir/work/ww3_multi.inp.hindcast
	# update dates in WaveWatch III **ww3_ounf.inp** , **ww3_ounp.inp** , **ww3_prnc.inp.wndcfsr** and **ww3_prnc.inp.icecfsr** files
	# ---> setting variables
	line_3_ounf="  $starting_date 000000 $time_resolution 9999"
	line_3_ounp="  $starting_date 000000 $time_resolution $final_field"
	line_5_wndcfsr="  '${wind_files[$i]}'"
	line_5_icecfsr="  '${ice_files[$i]}'"
	# ---> updating lines 
	sed -i "3s/.*/$line_3_ounf/" $resultsdir/work/ww3_ounf.inp
	sed -i "3s/.*/$line_3_ounp/" $resultsdir/work/ww3_ounp.inp
	sed -i "5s/.*/$line_5_wndcfsr/" $workdir/fix/ww3_prnc.inp.wndcfsr
	sed -i "5s/.*/$line_5_icecfsr/" $workdir/fix/ww3_prnc.inp.icecfsr
	# update dates in SWAN **swan_input_hindcast.swn** files
	# ---> setting variables
	line_60_swan="BLO 'COMPGRID' NOHEADER 'swan.${starting_date:0:6}_hs.mat' LAY 4 HS 1 OUTPUT $first_field_date.$first_field_time $time_resolution Sec"
	line_61_swan="BLO 'COMPGRID' NOHEADER 'swan.${starting_date:0:6}_dir.mat' LAY 4 DIR 1 OUTPUT $first_field_date.$first_field_time $time_resolution Sec"
	line_64_swan="COMP NONSTAT $first_field_date.$first_field_time $time_resolution Sec $ending_date.$ending_time"
	# ---> updating lines
	sed -i "60s/.*/$line_60_swan/" $workdir/swan/swan_input_hindcast.swn
	sed -i "61s/.*/$line_61_swan/" $workdir/swan/swan_input_hindcast.swn
	sed -i "64s/.*/$line_64_swan/" $workdir/swan/swan_input_hindcast.swn
	# forcing's fields
	cd $workdir/cfsr/
	# processing forcing fields
	# wind
	rm -f mod_def.ww3 ww3_prnc.inp *.nc wind.cfsr
	ln -s $workdir/vento_gelo_gfs/${wind_files[$i]} 
	ln -s $workdir/fix/ww3_prnc.inp.wndcfsr ww3_prnc.inp
	ln -s $workdir/fix/mod_def.cfsr mod_def.ww3
	/home/oceano/WW3-v6.07/model/exe/ww3_prnc
	mv -f "wind.ww3" "wind.cfsr"
	# ice
	rm -f ww3_prnc.inp ice.cfsr
	ln -s $workdir/vento_gelo_gfs/${ice_files[$i]}
	ln -s $workdir/fix/ww3_prnc.inp.icecfsr ww3_prnc.inp
	/home/oceano/WW3-v6.07/model/exe/ww3_prnc
	mv -f "ice.ww3" "ice.cfsr"
	# final steps to running WW3 simulation
	cd $resultsdir/work/
	rm -f mod_def.cfsr mod_def.global mod_def.southatl mod_def.grade_rj mod_def.grade_bg ww3_multi.inp wind.cfsr ice.cfsr
	ln -s ww3_multi.inp.hindcast ww3_multi.inp
	ln -s $workdir/fix/mod_def.cfsr mod_def.cfsr
	ln -s $workdir/fix/mod_def.global mod_def.global
	ln -s $workdir/fix/mod_def.southatl mod_def.southatl
	ln -s $workdir/fix/mod_def.grade_rj mod_def.grade_rj
	ln -s $workdir/fix/mod_def.grade_bg mod_def.grade_bg
	ln -s $workdir/cfsr/wind.cfsr wind.cfsr
	ln -s $workdir/cfsr/ice.cfsr ice.cfsr
	# running the WW3 model
	echo "STARTING $(ordinal $(($i+1))) WW3 simulation at: $(date)"
	echo ' '
	echo ' '
	/home/oceano/WW3-v6.07/model/exe/ww3_multi
	echo "--> $(ordinal $(($i+1))) WW3 simulation is DONE at: $(date)" # a list of ordinal numbers created in line 57 is used here!
	echo ' '
	# move restart files
	cd $resultsdir/work
	mv -f out_* $resultsdir/$simulation_name/restart   
	mv -f log.* $resultsdir/$simulation_name/restart
	cp -f restart* $resultsdir/$simulation_name/restart
	rm $resultsdir/work/restart*
	cp $resultsdir/$simulation_name/restart/restart$final_field.global $resultsdir/work
	cp $resultsdir/$simulation_name/restart/restart$final_field.southatl $resultsdir/work
	cp $resultsdir/$simulation_name/restart/restart$final_field.grade_rj $resultsdir/work
	cp $resultsdir/$simulation_name/restart/restart$final_field.grade_bg $resultsdir/work
	mv $resultsdir/work/restart$final_field.global restart.global
	mv $resultsdir/work/restart$final_field.southatl restart.southatl
	mv $resultsdir/work/restart$final_field.grade_rj restart.grade_rj
	mv $resultsdir/work/restart$final_field.grade_bg restart.grade_bg
	#rm -f $resultsdir/$simulation_name/restart/restart*  # remove all restart files from restart results folder
	# generating results
	cd $workdir/scripts
	echo "Generating netCDF file results..."
	echo ' '
	echo ' '
	./gera_resultados_netCDF_ww3.sh >& log_gera_resultados.txt
	# running SWAN wave model
	echo "Running SWAN simulation..."
	echo ' '
	echo ' '
	#./roda_swan.sh >& log_swan.txt
	# creating images
	echo "Creating images..."
	echo ' '
	echo ' '
	cd $workdir/scripts
	#ipython $workdir/scripts/cria_imagens_shell_global.py
	ipython $workdir/scripts/cria_imagens_shell_AtlSul.py >& log_Atlsul.txt
	#ipython $workdir/scripts/cria_imagens_shell_rj.py
	#ipython $workdir/scripts/cria_imagens_shell_bg.py
	#ipython $workdir/scripts/cria_imagens_shell_swan-BG.py
done

cd $resultsdir/work/
rm -f mod_def.cfsr mod_def.global mod_def.southatl mod_def.grade_rj mod_def.grade_bg ww3_multi.inp wind.cfsr ice.cfsr

cd $workdir/scripts
mv $resultsdir/work/ $workdir

echo ' '
echo "    *** Hindcast simulation is finished! ***"



