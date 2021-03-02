import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np




dataset201801 = Dataset('swan.201804_transp_energy.nc')

uComp = dataset201801['u_component_energy_transp']
vComp = dataset201801['v_component_energy_transp']
time = dataset201801['time']

for i in range(time.size):
	u = uComp[i,:,:]
	v = vComp[i,:,:]
	Pe = np.hypot(u, v)
	plt.contourf(Pe)
	#plt.colorbar()
	plt.savefig(os.path.join('/home/piatam8/ww3/ww3_shell/modelo_hindcast/resultados/teste_1/swan-BG/arquivos_netCDF/check_images', 'imagem_' + str(i)), bbox_inches='tight', dpi=300)
