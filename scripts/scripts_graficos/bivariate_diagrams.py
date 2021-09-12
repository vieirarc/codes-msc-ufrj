import os
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
import collections
import scipy.io as sio
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
#plt.switch_backend('Agg')
import seaborn as sns
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patheffects as path_effects

# env. variable from shell
simulationName = 'teste_18'
#simulationName = os.environ["simulation_name"]

# data and path
datasetHs = Dataset('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_hs.nc')
datasetTp = Dataset('/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/arquivos_netCDF/simulacao_geral/swan.geral_tp.nc')
pathSave = '/scratch/90081c/vieirarc/ww3-projects/modelo_hindcast/resultados/' + simulationName + '/swan-BG/imagens/simulacao_geral/diagramas'

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


pointAnl = 'XX' # ---> define point name here!

for index in range(time.size):
    dates = initialDateVariable + timedelta(days=np.float64(time[index]))
    if initialDate2017 <= dates <= finalDate2017: # *** 2017 ***
        #hsField = hs[index,:,:]
        #tpField = tp[index,:,:]
        hsPoint2017 = hs[index, 24, 188].data # ----------------> edit point here!
        tpPoint2017 = tp[index, 24, 188].data # ----------------> edit point here!
        hsPoint2017Float = float(hsPoint2017)
        tpPoint2017Float = float(tpPoint2017)
        hsPoint2017List.append(hsPoint2017Float)
        tpPoint2017List.append(tpPoint2017Float)
        fields2017 = fields2017 + 1
    elif initialDate2018 <= dates <= finalDate2018:
        #hsField = hs[index,:,:]
        #tpField = tp[index,:,:]
        hsPoint2018 = hs[index, 24, 188].data # ----------------> edit point here!
        tpPoint2018 = tp[index, 24, 188].data # ----------------> edit point here!
        hsPoint2018Float = float(hsPoint2018)
        tpPoint2018Float = float(tpPoint2018)
        hsPoint2018List.append(hsPoint2018Float)
        tpPoint2018List.append(tpPoint2018Float)
        fields2018 = fields2018 + 1
    else:
        continue


# wave power isolines

# lists
hsIso1 = []
hsIso5 = []
hsIso15 = []
hsIso30 = []
hsIso60 = []
hsIso90 = []
hsIso120 = []
hsIso150 = []

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
    hsIso1.append(Hs)


# isoline of Pw = 5kW/m
Pw = 5000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso5.append(Hs)


# isoline of Pw = 15kW/m 
Pw = 15000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso15.append(Hs)


# isoline of Pw = 30kW/m 
Pw = 30000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso30.append(Hs)


# isoline of Pw = 60kW/m 
Pw = 60000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso60.append(Hs)


# isoline of Pw = 90kW/m 
Pw = 90000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso90.append(Hs)


# isoline of Pw = 120kW/m 
Pw = 120000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso120.append(Hs)


# isoline of Pw = 200000kW/m 
Pw = 150000

for i in tpPoint2017List:
    Hs = math.sqrt((Pw * 64 * math.pi)/(rho * (g ** 2) * i))
    hsIso150.append(Hs)


plt.plot(tpPoint2017List, hsIso4)


# creating plot 

# ************* 2017
fig, ax = plt.subplots(figsize =(10, 7))

hsPoint2017List_min = np.min(hsPoint2017List)
hsPoint2017List_max = np.max(hsPoint2017List)
tpPoint2017List_min = np.min(tpPoint2017List)
tpPoint2017List_max = np.max(tpPoint2017List)
hs_bins = np.linspace(0, 6, 13)
tp_bins = np.linspace(4, 14, 21)

plt.title('Bivariate distribution Hs and Te - Point ' + pointAnl + ' 2017' )
ax.set_xlabel('Energetic Period (s)')
ax.set_ylabel('Significant Wave Height (m)')

# creating cmap
viridis = cm.get_cmap('jet', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([1, 1., 1, 1])
newcolors[0,:] = white
newcmp = ListedColormap(newcolors)

# plotting
hist, xbins, ybins, im = ax.hist2d(tpPoint2017List, hsPoint2017List, bins=(tp_bins,hs_bins), cmap=newcmp, vmin=0, vmax=151)

# colorbar
cbar = fig.colorbar(im)
cbar.set_label(u'Number of occurrences', size=10, rotation=90, labelpad=4)
#cbar.set_ticks([range(1, 151, 25)])
#cbar.set_ticklabels(['0', '25', '50', '75', '100', '125', '150']) # vertically oriented colorbar)
cbar.ax.tick_params(labelsize=9)

# writing numbers inside each bin
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        if hist.T[i,j] > 0:
                histInt = int(hist.T[i,j])
                txt = ax.text(xbins[j]+0.3,ybins[i], histInt,
                color="w", ha="center", va="bottom", fontsize=9, fontweight="bold")
                txt.set_path_effects([path_effects.Stroke(linewidth=0.7, foreground='black'),
                       path_effects.Normal()])
        else:
                continue


# axis
ax.set(xlim=(4,max(tpPoint2017List)), ylim=(0, max(hsPoint2017List)))
plt.xticks(np.arange(4, max(tpPoint2017List), 0.5))
plt.yticks(np.arange(0, max(hsPoint2017List), 0.5))
plt.grid(color='k', linestyle='--', linewidth=0.4)
plt.plot(tpPoint2017List, hsIso1, 'k')
plt.plot(tpPoint2017List, hsIso5, 'k')
plt.plot(tpPoint2017List, hsIso15, 'k')
plt.plot(tpPoint2017List, hsIso30, 'k')
plt.plot(tpPoint2017List, hsIso60, 'k')
plt.plot(tpPoint2017List, hsIso90, 'k')
plt.plot(tpPoint2017List, hsIso120, 'k')
plt.plot(tpPoint2017List, hsIso150, 'k')
plt.gca().set_aspect('equal', adjustable='box')
    

#plt.savefig(os.path.join(pathSave, 'bivariate_dist'), bbox_inches='tight', dpi=400)



# ************* 2018
fig, ax = plt.subplots(figsize =(10, 7))

hsPoint2018List_min = np.min(hsPoint2018List)
hsPoint2018List_max = np.max(hsPoint2018List)
tpPoint2018List_min = np.min(tpPoint2018List)
tpPoint2018List_max = np.max(tpPoint2018List)
hs_bins = np.linspace(hsPoint2018List_min, hsPoint2018List_max, 20)
tp_bins = np.linspace(tpPoint2018List_min, tpPoint2018List_max, 15)

plt.title('Bivariate distribution Hs and Te - Point ' + pointAnl + ' 2018' )
ax.set_xlabel('Energetic Period (s)')
ax.set_ylabel('Significant Wave Height (m)')

# creating cmap
viridis = cm.get_cmap('jet', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([1, 1., 1, 1])
newcolors[0,:] = white
newcmp = ListedColormap(newcolors)

# plotting
hist, xbins, ybins, im = ax.hist2d(tpPoint2018List, hsPoint2018List, bins=[tp_bins, hs_bins], cmap=newcmp, vmin=0, vmax=113)
cbar = fig.colorbar(im)
cbar.set_label(u'Number of occurrences', size=10, rotation=90, labelpad=4)

# writing numbers inside each bin
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        if hist.T[i,j] > 0:
                histInt = int(hist.T[i,j])
                txt = ax.text(xbins[j]+0.3,ybins[i], histInt,
                color="w", ha="center", va="bottom", fontsize=9, fontweight="bold")
                txt.set_path_effects([path_effects.Stroke(linewidth=0.7, foreground='black'),
                       path_effects.Normal()])
        else:
                continue

# axis
ax.set(xlim=(0,17.1), ylim=(0,6.1))
plt.xticks(np.arange(0, 17.1, 1))
plt.yticks(np.arange(0, 6.1, 1))
plt.grid(color='k', linestyle='--', linewidth=0.4)

#plt.savefig(os.path.join(pathSave, 'bivariate_dist'), bbox_inches='tight', dpi=400)
