import os
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
import collections
import scipy.io as sio
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import seaborn as sns
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patheffects as path_effects

# env. variable from shell
simulationName = 'teste_18'
#simulationName = os.environ["simulation_name"]

# data and path
datasetHs = Dataset('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_hs.nc')
datasetTp = Dataset('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_tp.nc')
pathSaveBg = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/imagens/simulacao_geral/diagramas'

hs = datasetHs['hs']
tp = datasetTp['tp']
time = datasetHs['time']


# *** annual lists ***

sumWaveEnergy2017 = 0
sumWaveEnergy2018 = 0
fields2017 = 0
fields2018 = 0

initialDateVariable = datetime(1990, 1, 1, 0)

initialDate2017 = datetime(2017, 1, 1, 0)
finalDate2017 = datetime(2017, 12, 31, 22)

initialDate2018 = datetime(2018, 1, 1, 0)
finalDate2018 = datetime(2018, 12, 31, 22)

hsPoint2017List = []
tpPoint2017List = []

hsPoint2018List = []
tpPoint2018List = []


pointAnl = 'R6' # ---> define point name here!

for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if initialDate2017 <= dates <= finalDate2017: # *** 2017 ***
        #hsField = hs[index,:,:]
        #tpField = tp[index,:,:]
        hsPoint2017 = hs[index, 98, 308].data # ----------------> edit point here!
        tpPoint2017 = tp[index, 98, 308].data # ----------------> edit point here!
        hsPoint2017Float = float(hsPoint2017)
        tpPoint2017Float = float(tpPoint2017)
        hsPoint2017List.append(hsPoint2017Float)
        tpPoint2017List.append(tpPoint2017Float)
        fields2017 = fields2017 + 1
    elif initialDate2018 <= dates <= finalDate2018:
        #hsField = hs[index,:,:]
        #tpField = tp[index,:,:]
        hsPoint2018 = hs[index, 98, 308].data # ----------------> edit point here!
        tpPoint2018 = tp[index, 98, 308].data # ----------------> edit point here!
        hsPoint2018Float = float(hsPoint2018)
        tpPoint2018Float = float(tpPoint2018)
        hsPoint2018List.append(hsPoint2018Float)
        tpPoint2018List.append(tpPoint2018Float)
        fields2018 = fields2018 + 1
    else:
        continue


# **** wave power isolines ****

# lists 2017
hsIso12017 = []
hsIso52017 = []
hsIso152017 = []
hsIso302017 = []
hsIso602017 = []
hsIso902017 = []
hsIso1202017 = []
hsIso1502017 = []


# lists 2018
hsIso12018 = []
hsIso52018 = []
hsIso152018 = []
hsIso302018 = []
hsIso602018 = []
hsIso902018 = []
hsIso1202018 = []
hsIso1502018 = []

# constants
rho = 1025
g = 9.8

# formulas
#Pw = ((rho * (g ** 2)) / (64 * math.pi)) * tpPoint2018List * (hsPoint2018List ** 2)
#Hs = math.sqrt(Pw * ((64 * math.pi)/(rho * (g ** 2))) * Te)
#Te = Pw * ((64 * math.pi)/(rho * (g ** 2))) * (Hs ** 2)


# ******* 2017 ********
# isoline of Pw = 1kW/m
Pw = 1000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso12017.append(Hs)


# isoline of Pw = 5kW/m
Pw = 5000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso52017.append(Hs)


# isoline of Pw = 15kW/m 
Pw = 15000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso152017.append(Hs)


# isoline of Pw = 30kW/m 
Pw = 30000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso302017.append(Hs)


# isoline of Pw = 60kW/m 
Pw = 60000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso602017.append(Hs)


# isoline of Pw = 90kW/m 
Pw = 90000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso902017.append(Hs)


# isoline of Pw = 120kW/m 
Pw = 120000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso1202017.append(Hs)


# isoline of Pw = 200000kW/m 
Pw = 150000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso1502017.append(Hs)



# ******* 2018 ********
# isoline of Pw = 1kW/m
Pw = 1000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso12018.append(Hs)


# isoline of Pw = 5kW/m
Pw = 5000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso52018.append(Hs)


# isoline of Pw = 15kW/m 
Pw = 15000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso152018.append(Hs)


# isoline of Pw = 30kW/m 
Pw = 30000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso302018.append(Hs)


# isoline of Pw = 60kW/m 
Pw = 60000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso602018.append(Hs)


# isoline of Pw = 90kW/m 
Pw = 90000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso902018.append(Hs)


# isoline of Pw = 120kW/m 
Pw = 120000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso1202018.append(Hs)


# isoline of Pw = 200000kW/m 
Pw = 150000

for i in tpPoint2018List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso1502018.append(Hs)


# creating plot 

# ************* 2017
fig, ax = plt.subplots(figsize =(10, 7))

hsPoint2017List_min = np.min(hsPoint2017List)
hsPoint2017List_max = np.max(hsPoint2017List)
tpPoint2017List_min = np.min(tpPoint2017List)
tpPoint2017List_max = np.max(tpPoint2017List)
hs_bins = np.linspace(0, 6, 13)
tp_bins = np.linspace(4, 14, 21)


# creating cmap
newCmap = cm.get_cmap('jet', 256)
newcolors = newCmap(np.linspace(0, 1, 256))
white = np.array([1, 1., 1, 1])
newcolors[0,:] = white
newcmp = ListedColormap(newcolors)

# plotting
hist, xbins, ybins, im = ax.hist2d(tpPoint2017List, hsPoint2017List, bins=(tp_bins,hs_bins), cmap=newcmp, vmin=0, vmax=151)

# writing numbers inside each bin
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        if hist.T[i,j] > 0:
                histInt = int(hist.T[i,j])
                txt = ax.text(xbins[j]+0.26,ybins[i], histInt,
                color="w", ha="center", va="bottom", fontsize=9.0)
                txt.set_path_effects([path_effects.Stroke(linewidth=1.0, foreground='black'),
                       path_effects.Normal()])
        else:
                continue

# colorbar
cbar = fig.colorbar(im, shrink=0.65)
cbar.set_label(u'Number of occurrences', size=10, rotation=90, labelpad=4)
#cbar.set_ticks([range(1, 151, 25)])
#cbar.set_ticklabels(['0', '25', '50', '75', '100', '125', '150']) # vertically oriented colorbar)
cbar.ax.tick_params(labelsize=10)


# axis
ax.set(xlim=(4, 14.5), ylim=(0, 6.1))
plt.grid(color='dimgrey', linestyle='--', linewidth=0.1)


# x
ax.set_xlabel('Energetic Period (s)', fontsize=10)
ax.set_xticks(np.arange(4, 14.5, 0.5))
x_ticks = [ '4' , ' ',  '5 ', ' ',  '6' , ' ',  '7' , ' ',  '8' , ' ',  '9' , ' ', '10' , ' ', '11' , ' ', '12' , ' ', '13' , ' ', '14' ]
ax.set_xticklabels(x_ticks, fontsize=8)

# y
ax.set_ylabel('Significant Wave Height (m)', fontsize=10)
ax.set_yticks(np.arange(0, 6.1, 0.5))
y_ticks = ['0', ' ', '1', ' ', '2', ' ', '3', ' ', '4' , ' ',  '5 ', ' ',  '6']
ax.set_yticklabels(y_ticks, fontsize=8)

# plotting isolines


plt.plot(tpPoint2017List, hsIso12017, '.', markersize=3, color='dimgrey')
plt.text(13.6, 0.2, "1 kW/m", fontsize=8, fontweight="bold")

plt.plot(tpPoint2017List, hsIso52017, '.', markersize=3, color='dimgrey')
plt.text(4.1, 1.48, "5 kW/m", fontsize=8, rotation=-11, fontweight="bold")

plt.plot(tpPoint2017List, hsIso152017, '.', markersize=3, color='dimgrey')
plt.text(5.1, 2.3, "15 kW/m", fontsize=8, rotation=-13.7, fontweight="bold")

plt.plot(tpPoint2017List, hsIso302017, '.', markersize=3, color='dimgrey')
plt.text(5.5, 3.15, "30 kW/m", fontsize=8, rotation=-15, fontweight="bold")

plt.plot(tpPoint2017List, hsIso602017, '.', markersize=3, color='dimgrey')
plt.text(5.85, 4.35, "60 kW/m", fontsize=8, rotation=-17.5, fontweight="bold")

plt.plot(tpPoint2017List, hsIso902017, '.', markersize=3, color='dimgrey')
plt.text(6.4, 5.15, "90 kW/m", fontsize=8, rotation=-16.59, fontweight="bold")

plt.plot(tpPoint2017List, hsIso1202017, '.', markersize=3, color='dimgrey')
plt.text(7.5, 5.46, "120 kW/m", fontsize=8, rotation=-17, fontweight="bold")

plt.plot(tpPoint2017List, hsIso1502017, '.', markersize=3, color='dimgrey')
plt.text(8.94, 5.62, "150 kW/m", fontsize=8, rotation=-17, fontweight="bold")


plt.title('Scatter diagram Hs-Te Point ' + pointAnl + ' - 2017', fontsize=10 )
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig(os.path.join(pathSaveBg, 'bivariate_dist_2017_' + pointAnl), bbox_inches='tight', dpi=100)



# ************* 2018
fig, ax = plt.subplots(figsize =(10, 7))

hsPoint2018List_min = np.min(hsPoint2018List)
hsPoint2018List_max = np.max(hsPoint2018List)
tpPoint2018List_min = np.min(tpPoint2018List)
tpPoint2018List_max = np.max(tpPoint2018List)
hs_bins = np.linspace(0, 6, 13)
tp_bins = np.linspace(4, 14, 21)


# creating cmap
newCmap = cm.get_cmap('jet', 256)
newcolors = newCmap(np.linspace(0, 1, 256))
white = np.array([1, 1., 1, 1])
newcolors[0,:] = white
newcmp = ListedColormap(newcolors)

# plotting
hist, xbins, ybins, im = ax.hist2d(tpPoint2018List, hsPoint2018List, bins=(tp_bins,hs_bins), cmap=newcmp, vmin=0, vmax=151)

# writing numbers inside each bin
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        if hist.T[i,j] > 0:
                histInt = int(hist.T[i,j])
                txt = ax.text(xbins[j]+0.26,ybins[i], histInt,
                color="w", ha="center", va="bottom", fontsize=9.0)
                txt.set_path_effects([path_effects.Stroke(linewidth=1.0, foreground='black'),
                       path_effects.Normal()])
        else:
                continue

# colorbar
cbar = fig.colorbar(im, shrink=0.65)
cbar.set_label(u'Number of occurrences', size=10, rotation=90, labelpad=4)
#cbar.set_ticks([range(1, 151, 25)])
#cbar.set_ticklabels(['0', '25', '50', '75', '100', '125', '150']) # vertically oriented colorbar)
cbar.ax.tick_params(labelsize=10)


# axis
ax.set(xlim=(4, 14.5), ylim=(0, 6.1))
plt.grid(color='dimgrey', linestyle='--', linewidth=0.1)


# x
ax.set_xlabel('Energetic Period (s)', fontsize=10)
ax.set_xticks(np.arange(4, 14.5, 0.5))
x_ticks = [ '4' , ' ',  '5 ', ' ',  '6' , ' ',  '7' , ' ',  '8' , ' ',  '9' , ' ', '10' , ' ', '11' , ' ', '12' , ' ', '13' , ' ', '14' ]
ax.set_xticklabels(x_ticks, fontsize=8)

# y
ax.set_ylabel('Significant Wave Height (m)', fontsize=10)
ax.set_yticks(np.arange(0, 6.1, 0.5))
y_ticks = ['0', ' ', '1', ' ', '2', ' ', '3', ' ', '4' , ' ',  '5 ', ' ',  '6']
ax.set_yticklabels(y_ticks, fontsize=8)

# plotting isolines


plt.plot(tpPoint2018List, hsIso12018, '.', markersize=3, color='dimgrey')
plt.text(13.6, 0.2, "1 kW/m", fontsize=8, fontweight="bold")

plt.plot(tpPoint2018List, hsIso52018, '.', markersize=3, color='dimgrey')
plt.text(4.1, 1.48, "5 kW/m", fontsize=8, rotation=-11, fontweight="bold")

plt.plot(tpPoint2018List, hsIso152018, '.', markersize=3, color='dimgrey')
plt.text(5.1, 2.3, "15 kW/m", fontsize=8, rotation=-13.7, fontweight="bold")

plt.plot(tpPoint2018List, hsIso302018, '.', markersize=3, color='dimgrey')
plt.text(5.5, 3.15, "30 kW/m", fontsize=8, rotation=-15, fontweight="bold")

plt.plot(tpPoint2018List, hsIso602018, '.', markersize=3, color='dimgrey')
plt.text(5.85, 4.35, "60 kW/m", fontsize=8, rotation=-17.5, fontweight="bold")

plt.plot(tpPoint2018List, hsIso902018, '.', markersize=3, color='dimgrey')
plt.text(6.4, 5.15, "90 kW/m", fontsize=8, rotation=-16.59, fontweight="bold")

plt.plot(tpPoint2018List, hsIso1202018, '.', markersize=3, color='dimgrey')
plt.text(7.5, 5.46, "120 kW/m", fontsize=8, rotation=-17, fontweight="bold")

plt.plot(tpPoint2018List, hsIso1502018, '.', markersize=3, color='dimgrey')
plt.text(8.94, 5.62, "150 kW/m", fontsize=8, rotation=-17, fontweight="bold")


plt.title('Scatter diagram Hs-Te Point ' + pointAnl + ' - 2018', fontsize=10 )
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig(os.path.join(pathSaveBg, 'bivariate_dist_2018_' + pointAnl), bbox_inches='tight', dpi=100)


# *******************************************

# pointsDict = {}

# R1x, R1y = (39, 65)
# R2x, R2y = (83, 20)
# R3x, R3y = (128, 15)
# R4x, R4y = (188, 24)
# R5x, R5y = (266, 44)
# R6x, R6y = (308, 98)


