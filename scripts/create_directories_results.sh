#!/bin/bash

export resultsdir=/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados

# input by user
simulation_name = raw_input('Simulation Name: ')
export simulation_name

# creating directories
mkdir $resultsdir/$simulation_name
mkdir $resultsdir/$simulation_name/swan-BG
mkdir $resultsdir/$simulation_name/swan-BG/arquivos_netCDF
mkdir $resultsdir/$simulation_name/swan-BG/imagens
mkdir $resultsdir/$simulation_name/swan-BG/simulacao_geral
mkdir $resultsdir/$simulation_name/swan-BG/arquivos_netCDF/simulacao_geral
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/time_series
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/wave_energy
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/wave_energy/annual_average
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/wave_energy/montly_average
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/wave_energy/seasonal_average
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-3
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-3/dir
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-3/hs
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-3/tp
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-3/statistics_table
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-4
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-4/dir
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-4/hs
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-4/tp
mkdir $resultsdir/$simulation_name/swan-BG/imagens/simulacao_geral/validacao/RJ-4/statistics_table

