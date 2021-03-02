#!/bin/bash

export workdir=/home/oceano/WW3-v6.07/model/ww3_shell/modelo_hindcast
export resultsdir=/storage/oceano/rafael/wavewatch3_results/hindcast

mkdir $resultsdir/$simulation_name

mkdir $resultsdir/$simulation_name/global
mkdir $resultsdir/$simulation_name/global/imagens

mkdir $resultsdir/$simulation_name/south_atlantic
mkdir $resultsdir/$simulation_name/south_atlantic/imagens

mkdir $resultsdir/$simulation_name/rj
mkdir $resultsdir/$simulation_name/rj/imagens

mkdir $resultsdir/$simulation_name/bg
mkdir $resultsdir/$simulation_name/bg/imagens

mkdir $resultsdir/$simulation_name/swan-BG
mkdir $resultsdir/$simulation_name/swan-BG/imagens

mkdir $resultsdir/$simulation_name/restart
