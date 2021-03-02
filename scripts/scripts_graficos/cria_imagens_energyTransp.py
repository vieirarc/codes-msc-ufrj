

from netCDF4 import Dataset
import numpy as np
import math



resultsDir = '/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1'
pathSave = (resultsDir + '/swan-BG/imagens/wave_energy')




energyDataset = Dataset('swan.201612_transp_energy.nc')
uEnergy = energyDataset['u_component_energy_transp']
vEnergy = energyDataset['v_component_energy_transp']
time = energyDataset['time']
lats = energyDataset['latitude'][:]
lons = energyDataset['longitude'][:]
lon, lat = np.meshgrid(lons, lats)
lonCorr = lon - 360


uEnergy10 = uEnergy[10,:,:]
vEnergy10 = vEnergy[10,:,:]
	
wavePower = np.hypot(uEnergy10, vEnergy10)

wavePowerMasked = np.ma.masked_where(wavePower == 0, wavePower)

