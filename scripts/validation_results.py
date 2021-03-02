#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:21:55 2020

# Script: valid_rafinha.py

# Author: Yuri Brasil

# e-mail: yuri.brasil@oceanica.ufrj.br

# Modification: July 7th 2020

# Objective: Plot a series of plots showing comparison 
between different sets of wave data.

"""

import pandas as pd
import numpy as np
import datetime as date
import matplotlib.pyplot as plt
import scipy.io as sio

from datetime import timedelta
from matplotlib import style
from scipy import stats

# my_path =  '/home/piatam8/Desktop/Kingston_Prata/Modelos_numericos/SWAN/Validacao_Rafinha/results_mat/'
# my_path2 = '/home/piatam8/Desktop/Kingston_Prata/Modelos_numericos/SWAN/Validacao_Rafinha/'

my_path = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/simulacao_geral/'
my_path2 = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/validation/'

#d10 = my_path + '10_dir_bg_swan.mat'
#h10 = my_path + '10_hs_bg_swan.mat'

#d10 = my_path + '2019_10_19_dir_bg_swan.mat'
#h10 = my_path + '2019_10_19_hs_bg_swan.mat'

#d10 = my_path + '2019_11_19_dir_bg_swan.mat'
#h10 = my_path + '2019_11_19_hs_bg_swan.mat'

d10 = my_path + 'swan.geral_hs.mat'
h10 = my_path + 'swan.geral_dir.mat'

dir10 = sio.loadmat(d10)#, squeeze_me=True)
hs10 = sio.loadmat(h10)

del d10, h10

obs = '_'
#obs = '_raf_op4'

################### Creating arrays of lon and lat ############################

lon_init = -43.3140
lat_init = -23.0900

d_lon = 0.00082
d_lat = 0.00089

rows = 473 # Lat
cols = 338 # Lon

lon_ar = np.arange(lon_init,cols*d_lon + lon_init,d_lon)[0:-1]
lat_ar = np.arange(lat_init,rows*d_lat + lat_init,d_lat)[0:-1]

# Coordinates of SiMCosta RJ-4 (-43.152167, -22.971550)
# lon_ar[197] and lat_ar[133]

# Hs[133,197]

################## Loading files into dataframe format ########################

#csv_file = 'SIMCOSTA_RJ-4_OCEAN_2020-01-01_2020-01-21.csv'
#csv_file = 'SIMCOSTA_RJ-4_OCEAN_2019-10-18_2019-10-24.csv'
#csv_file = 'SIMCOSTA_RJ-4_OCEAN_2019-11-18_2019-11-24.csv'
csv_file = 'SIMCOSTA_RJ-3_OCEAN_2016-07-14_2019-01-05.csv'

# Creating the column names
column_names = ['Hs', 'Tp', 'Dir']

# Creating a dataframe for the spreadsheet from SiMCosta
sim_df = pd.read_csv(my_path2 + csv_file, 
                  error_bad_lines=False, 
                  encoding = 'UTF-8', 
                  sep = ',', 
                  header = 16,
                  parse_dates={'datetime': [0,1,2,3,4,5]})

# Putting everything in the datetime format
sim_df.datetime = sim_df.apply(lambda x: pd.to_datetime(x.datetime, 
                                                  dayfirst=True, 
                                                  format="%Y %m %d %H %M %S"), axis=1)
# Imposing that the datetime is the index
sim_df.index = sim_df.datetime

# deleting a few columns
sim_df = sim_df.drop(['Avg_Wv_Dir', 'M_Decl', 'datetime'], axis=1)

# Setting the column names
sim_df.columns = column_names

# Getting only the times with 55min and changing its datetime to 5 minutes later
# to get the round hour. i.e 4:00 instead of 3:55 as SiMCosta shows
sim_df = sim_df.resample('30min', base=25, loffset=timedelta(minutes=5)).asfreq()

# Getting only the data that ends at 00min
sim_df = sim_df[sim_df.index.minute == 00]

################ Getting the SWAN parameters data #############################
 
# Getting the time data from SWAN file

# Getting the year data      
SWAN_year = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_year.append(int(i[3:7]))

# Getting the month data      
SWAN_month = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_month.append(int(i[7:9]))
    
# Getting the day data   
SWAN_day = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_day.append(int(i[9:11]))

# Getting the hour data   
SWAN_hour = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_hour.append(int(i[12:14]))
   
# Getting the hour data   
SWAN_minute = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_minute.append(int(i[14:16]))

swan_datetime = []

for i in range(0,len(SWAN_year)):
    swan_datetime.append(date.datetime(SWAN_year[i], 
                                       SWAN_month[i],
                                       SWAN_day[i],
                                       SWAN_hour[i],
                                       SWAN_minute[i]))

#swan_datetime = np.array(swan_datetime)

del SWAN_year, SWAN_month, SWAN_day, SWAN_hour, SWAN_minute

###############################################################################

SWAN_hs = []

for i in hs10.keys():
    if i[0:2] == 'HS':
        SWAN_hs.append(hs10[i][133,197])

SWAN_dir = []

for i in dir10.keys():
    if i[0:3] == 'DIR':
        SWAN_dir.append(dir10[i][133,197])


# Creating the SWAN dataframe
swan_df = pd.DataFrame(data={'Hs': SWAN_hs, 'Dir': SWAN_dir},
                       index=swan_datetime)

del SWAN_hs, SWAN_dir 

# Getting the dataframe at which the datetime matches with the swan dataframe
sim_df = sim_df[swan_df.index[3]:swan_df.index[-1]]
 
################ Adapting the SWAN data to validate it ########################

# Getting only the values at the same interval of swan_df
new_sim_df = sim_df[swan_df.index[1]:swan_df.index[-1]]

# Dropping the nan values
new_sim_df = new_sim_df.dropna()

# Transforming the values at which sim_df has nan in nan
nan_swan_df = swan_df[new_sim_df.notna()]

#  Dropping the nans
new_swan_df = nan_swan_df.dropna()

# Resampling the new_sim_df dataframe to get samples every 3 hours, without 0h
new_sim_df = new_sim_df.resample('3H').asfreq().dropna()

################################ Validation ###################################

keys = ['Hs', 'Dir']

#Bias

vals_bias = [np.nansum(swan_df['Hs'] - sim_df['Hs'])/len(sim_df['Hs']),
              np.nansum(swan_df['Dir'] - sim_df['Dir'])/len(sim_df['Dir'])]
             
bias = dict(zip(keys, vals_bias))

#RMSE

vals_rmse = [np.sqrt((np.nansum(swan_df['Hs'] - sim_df['Hs']))**2 /len(sim_df['Hs'])),
             np.sqrt((np.nansum(swan_df['Dir'] - sim_df['Dir']))**2 /len(sim_df['Dir']))]           
                          
rmse = dict(zip(keys, vals_rmse))

#Scatter Index

vals_scat_index = [rmse['Hs']/np.nanmean(sim_df['Hs']),
                   rmse['Dir']/np.nanmean(sim_df['Dir'])]
                                                    
scat_index = dict(zip(keys, vals_scat_index))


validation = {'rmse':rmse, 'bias':bias, 'scatter_index':scat_index}

del bias, rmse, scat_index, vals_bias, vals_rmse, vals_scat_index


############################# Visual Inspection ###############################
        
################################# Hs Plot #####################################

style.use('ggplot')
#style.use('ggplot2')

my_gray = (0.898, 0.898, 0.898, 1.0)


fig1 = plt.figure(figsize=(14, 10))

#plt.plot(sim_df.index, sim_df['Hs'], 
#         '-', linewidth=1.0, color='b', 
#         label = 'SiMCosta', marker = 'o', markersize=4)

#plt.plot(nan_swan_df.index, nan_swan_df['Hs'],
#         '-', linewidth=1.0, color='deepskyblue',
#         label = 'SWAN', marker = 's', markersize=4)


plt.plot(new_sim_df.index, new_sim_df['Hs'], 
         '-', linewidth=1.0, color='b', 
         label = 'SiMCosta', marker = 'o', markersize=4)

plt.plot(new_swan_df.index, new_swan_df['Hs'],
         '-', linewidth=1.0, color='deepskyblue',
         label = 'SWAN', marker = 's', markersize=4)

plt.ylabel('(m)', fontsize=14)
plt.xlabel('Date', fontsize=14)

# Ploting the mean lines and their values
plt.axhline(y=np.mean(sim_df['Hs']),
            linewidth=1, linestyle='--', color='b',
            label = 'SiMCosta Mean')

plt.text(sim_df.index[0],
         np.mean(sim_df['Hs']) + 0.02,
         str(np.round(np.mean(sim_df['Hs']),decimals = 2)), 
         fontsize=14, color = 'b')

plt.axhline(y=np.mean(nan_swan_df['Hs']),
            linewidth=1, linestyle='-.', color='deepskyblue',
            label = 'SWAN Mean')

plt.text(new_swan_df.index[-1],
         np.mean(nan_swan_df['Hs']) + 0.02,
         str(np.round(np.mean(nan_swan_df['Hs']),decimals = 2)),
         fontsize=14, color = 'deepskyblue')

# Ploting the text box
side_text = plt.figtext(0.135, 0.791,                        
                        'N = ' + str(len(new_sim_df['Hs'])) + '\n'
                        'RMSE = ' + str(round(validation['rmse']['Hs'],3)) + 'm' + '\n'
                        'Bias = ' + str(round(validation['bias']['Hs'],3)) + 'm' + '\n'                        
                        'Scatter Index = ' + str(round(validation['scatter_index']['Hs'],3)),
                        fontsize = 12, bbox=dict(facecolor = 'none'))


plt.title('Significant Wave Height - SWAN X SiMCosta', fontsize=16, pad=15)

plt.legend(loc='upper right', fontsize = 'x-large', facecolor = 'none')
plt.grid(linestyle='--', linewidth=0.5)
plt.show()

file_name = 'SWAN_simcosta_Hs_' + str(sim_df.index.year[0]) + str(sim_df.index.month[0]) + str(sim_df.index.day[0]) + '_' + \
            str(sim_df.index.year[-1]) + str(sim_df.index.year[-1]) + str(sim_df.index.year[-1])  + obs
            
fig1.savefig(file_name, dpi=300)


################################# Dir Plot #####################################

fig2 = plt.figure(figsize=(14, 10))

#plt.plot(sim_df.index, sim_df['Dir'],
#         '-', linewidth=1.4, color='g',
#         label = 'SiMCosta', marker = 'o', markersize=4)
#
#plt.plot(nan_swan_df.index, nan_swan_df['Dir'],
#         '-', linewidth=1.4, color='lightgreen',
#         label = 'SWAN', marker = 's', markersize=4)

plt.plot(new_sim_df.index, new_sim_df['Dir'],
         '-', linewidth=1.4, color='g',
         label = 'SiMCosta', marker = 'o', markersize=4)

plt.plot(new_swan_df.index, new_swan_df['Dir'],
         '-', linewidth=1.4, color='lightgreen',
         label = 'SWAN', marker = 's', markersize=4)


plt.ylabel('(º)', fontsize=14)
plt.xlabel('Date', fontsize=14)

# Ploting the mean lines and their values
plt.axhline(y=np.mean(sim_df['Dir']),
            linewidth=1, linestyle='--', color='g',
            label = 'SiMCosta Mean')

plt.text(sim_df.index[0],
         np.mean(sim_df['Dir']) + 0.8,
         str(np.round(np.mean(sim_df['Dir']), decimals = 2)),
         fontsize=14, color = 'g')

plt.axhline(y=np.mean(nan_swan_df['Dir']),
            linewidth=1, linestyle='-.', color='lightgreen',
            label = 'SiMCosta Mean')

plt.text(nan_swan_df.index[-3],
         np.mean(nan_swan_df['Dir']) + 0.8,
         str(np.round(np.mean(nan_swan_df['Dir']), decimals = 2)),
         fontsize=14, color = 'lightgreen')

# Ploting the text box
side_text = plt.figtext(0.135, 0.79,                        
                        'N = ' + str(len(new_sim_df['Dir'])) + '\n'
                        'RMSE = ' + str(round(validation['rmse']['Dir'],3)) + 'º' + '\n'
                        'Bias = ' + str(round(validation['bias']['Dir'],3)) + 'º' + '\n'                        
                        'Scatter Index = ' + str(round(validation['scatter_index']['Dir'],3)),
                        fontsize = 12, bbox=dict(facecolor = 'none'))

plt.title('Mean Wave Direction - SWAN X SiMCosta', fontsize=16, pad=15)
plt.grid(linestyle='--', linewidth=0.5)
plt.legend(loc='upper right', fontsize = 'x-large', facecolor = 'none')
plt.show()

file_name2 = 'SWAN_simcosta_Dir_' + str(sim_df.index.year[0]) + str(sim_df.index.month[0]) + str(sim_df.index.day[0]) + '_' + \
            str(sim_df.index.year[-1]) + str(sim_df.index.year[-1]) + str(sim_df.index.year[-1])  + obs
            
fig2.savefig(file_name2, dpi=300)

#################### Correlation and other stats ##############################

################################## Hs #########################################

tendency_line = []

slope, intercept, rvalue, pvalue, stderr = stats.linregress(new_sim_df['Hs'], new_swan_df['Hs'])

corr_hs = {'slope':slope, 'intercept':intercept, 'rvalue':rvalue, 'pvalue':pvalue, 'stderr':stderr}

for i in range(0,len(new_sim_df['Hs'])):
    tendency_line.append(intercept + (slope * new_sim_df['Hs'][i]))

############################ Hs Correlation Plot ##############################

fig3 = plt.figure(figsize=(14, 10))

#plt.figure(), plt.plot((5,10), (5,10), '-o')

#plt.plot(new_sim_df['Hs'],new_sim_df['Hs'], linestyle= '--', 
#         color = 'k', alpha = 0.5, linewidth = 0.4)

plt.plot( (plt.xlim()[0],plt.xlim()[1]), (plt.xlim()[0],plt.xlim()[1]) , linestyle= '--', 
         color = 'k', alpha = 0.5, linewidth = 1)

plt.scatter(new_sim_df['Hs'], new_swan_df['Hs'], alpha = 0.5, marker = 'o', color = 'blue')

ax = plt.plot(new_sim_df['Hs'], tendency_line, color='deepskyblue',
                linewidth = 0.4, label = 'Tendency line')

plt.ylabel('SWAN Values (m)', fontsize=14)
plt.xlabel('SiMCosta Values (m)', fontsize=14)  

# Ploting the text box
side_text = plt.figtext(0.14, 0.785,                        
                        'N = ' + str(len(new_sim_df['Hs'])) + '\n'
                        'p < ' + str(round(corr_hs['pvalue'],3)) + '\n' \
                        'R = ' + str(round(corr_hs['rvalue'],3)) + '\n' \
                        'y = ' + str(round(corr_hs['slope'],3)) +  'x' + \
                        ' + ' + str(round(corr_hs['intercept'],3)), 
                        fontsize = 12, bbox=dict(facecolor = 'none'))

plt.title('Significant Wave Height - SWAN X SiMCosta', fontsize=16, pad=15)
plt.grid(linestyle='--', linewidth=0.5)
plt.legend(loc='upper right', fontsize = 'x-large', facecolor = 'none')
plt.show()

file_name3 = 'Corr_SWAN_simcosta_Hs_' + str(sim_df.index.year[0]) + str(sim_df.index.month[0]) + str(sim_df.index.day[0]) + '_' + \
            str(sim_df.index.year[-1]) + str(sim_df.index.year[-1]) + str(sim_df.index.year[-1])  + obs
            
fig3.savefig(file_name3, dpi=300)


################################## Dir ########################################

tendency_line = []

slope, intercept, rvalue, pvalue, stderr = stats.linregress(new_sim_df['Dir'], new_swan_df['Dir'])

corr_dir = {'slope':slope, 'intercept':intercept, 'rvalue':rvalue, 'pvalue':pvalue, 'stderr':stderr}

for i in range(0,len(new_sim_df['Dir'])):
    tendency_line.append(intercept + (slope * new_sim_df['Dir'][i]))

############################ Dir Correlation Plot #############################

fig4 = plt.figure(figsize=(14, 10))

#plt.plot(new_sim_df['Dir'],new_sim_df['Dir'], linestyle= '--', 
#         color = 'k', alpha = 0.5, linewidth = 1)

#plt.plot( (plt.xlim()[0],plt.xlim()[1]), (plt.xlim()[0],plt.xlim()[1]) , linestyle= '--', 
#         color = 'k', alpha = 0.5, linewidth = 1)

plt.plot( (150,200), (150,200) , linestyle= '--', 
         color = 'k', alpha = 0.5, linewidth = 1)

plt.scatter(new_sim_df['Dir'], new_swan_df['Dir'], alpha = 0.5, marker = 'o', color = 'green')

ax = plot = plt.plot(new_sim_df['Dir'], tendency_line, color='lightgreen',
                linewidth = 0.4, label = 'Tendency line')

plt.ylabel('SWAN Values (º)', fontsize=14)
plt.xlabel('SiMCosta Values (º)', fontsize=14)  

# Ploting the text box
side_text = plt.figtext(0.14, 0.785,                        
                        'N = ' + str(len(new_sim_df['Dir'])) + '\n'
                        'p < ' + str(round(corr_hs['pvalue'],3)) + '\n' \
                        'R = ' + str(round(corr_hs['rvalue'],3)) + '\n' \
                        'y = ' + str(round(corr_hs['slope'],3)) +  'x' + \
                        ' + ' + str(round(corr_hs['intercept'],3)), 
                        fontsize = 12, bbox=dict(facecolor = 'none'))


plt.title('Mean Direction  - SWAN X SiMCosta', fontsize=16, pad=15)
plt.grid(linestyle='--', linewidth=0.5)
plt.legend(loc='upper right', fontsize = 'x-large', facecolor = 'none')
plt.show()

file_name4 = 'Corr_SWAN_simcosta_Dir_' + str(sim_df.index.year[0]) + str(sim_df.index.month[0]) + str(sim_df.index.day[0]) + '_' + \
            str(sim_df.index.year[-1]) + str(sim_df.index.year[-1]) + str(sim_df.index.year[-1])  + obs
            
fig4.savefig(file_name4, dpi=300)


#plt.close('all')


############################################################################


#fig5 = plt.figure(figsize=(14, 10))
#
#st = 'HS_20200114_150000'
#
#plt.contourf(hs10[st])
#plt.title('Hs 2020-01-14 15h', fontsize=16, pad=15)
#plt.colorbar()
#
#file_name5 = st     
#fig5.savefig(file_name5, dpi=300)
#
#fig6 = plt.figure(figsize=(14, 10))
#
#st2 = 'HS_20200114_180000'
#
#plt.contourf(hs10[st2])
#plt.title('Hs 2020-01-14 18h', fontsize=16, pad=15)
#plt.colorbar()
#
#file_name6 = st2   
#fig6.savefig(file_name6, dpi=300)
#
#fig7 = plt.figure(figsize=(14, 10))
#
#st3 = 'HS_20200114_210000'
#
#plt.contourf(hs10[st3])
#plt.title('Hs 2020-01-14 21h', fontsize=16, pad=15)
#plt.colorbar()
#
#file_name7 = st3   
#fig7.savefig(file_name7, dpi=300)

