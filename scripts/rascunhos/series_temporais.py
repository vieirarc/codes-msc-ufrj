# -*- coding: UTF-8 -*-
import os
from netCDF4 import Dataset
import numpy as np
from datetime import date, datetime, timedelta
from matplotlib import dates
import matplotlib.pyplot as plt
import collections
plt.switch_backend('agg')

# Datas
todayString = date.today().strftime("%Y%m%d")
today = date.today()
finalDate = date.today() + timedelta(days=4)


# diretorios para salvar as imagens
path_save = '/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/series_temporais/series/' +  todayString + '/'
path_save_tp = '/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/series_temporais/series_TP/' +  todayString + '/'

# le os arquivos netcdf's
datasetHs = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/atlantico_sul/' +  todayString + '/ww3.' + todayString[0:4] + '_hs.nc') # altura significativa
datasetTp = Dataset('/home/piatam8/ww3/ww3_shell/modelo_operacional_v1.3/resultados/atlantico_sul/' +  todayString + '/ww3.' + todayString[0:4] + '_t02.nc')# periodo
	
HS = datasetHs['hs']
TP = datasetTp['t02']
      
# ****** HS ******
# gera as series de Hs
serieHsP1_SC = []
serieHsP2_RJ = []
serieHsP3_BA = []
serieHsP4_PE = []

dicSeriesHs = {}

for i in range(0,40):
	ponto1 = HS[i, 84, 43] # OK! SC
	serieHsP1_SC.append(ponto1)
	ponto2 = HS[i, 93, 55] # OK! BG
	serieHsP2_RJ.append(ponto2)
	ponto3 = HS[i, 105, 62] # OK! BAHIA
	serieHsP3_BA.append(ponto3)
	ponto4 = HS[i, 123, 71] # OK! PE
	serieHsP4_PE.append(ponto4)


dicSeriesHs['serieHsP1_SC'] = serieHsP1_SC
dicSeriesHs['serieHsP2_RJ'] = serieHsP2_RJ
dicSeriesHs['serieHsP3_BA'] = serieHsP3_BA
dicSeriesHs['serieHsP4_PE'] = serieHsP4_PE

dicSeriesHsOrdered = collections.OrderedDict(sorted(dicSeriesHs.items()))

# ****** TP ******
serieTpP1_SC = []
serieTpP2_RJ = []
serieTpP3_BA = []
serieTpP4_PE = []
# serieTpP5 = []
# serieTpP6 = []
dicSeriesTp = {}

for i in range(0,40):
	ponto1 = TP[i, 84, 43] # OK! SC
	serieTpP1_SC.append(ponto1)
	ponto2 = TP[i, 93, 55] # OK! BG - RJ
	serieTpP2_RJ.append(ponto2)
	ponto3 = TP[i, 105, 62] # OK! BA
	serieTpP3_BA.append(ponto3)
	ponto4 = TP[i, 123, 71] # OK! PE
	serieTpP4_PE.append(ponto4)


dicSeriesTp['serieTpP1_SC'] = serieTpP1_SC
dicSeriesTp['serieTpP2_RJ'] = serieTpP2_RJ
dicSeriesTp['serieTpP3_BA'] = serieTpP3_BA
dicSeriesTp['serieTpP4_PE'] = serieTpP4_PE

dicSeriesTpOrdered = collections.OrderedDict(sorted(dicSeriesTp.items()))

# lista de datas para formatar o eixo x
def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

listField = []
for j in datespan(datetime(today.year, today.month, today.day, 00), datetime(finalDate.year, finalDate.month, finalDate.day, 22),\
								 delta=timedelta(hours=3)):
	listField.append(j)

days = dates.DayLocator()
hours = dates.HourLocator()
dfmt = dates.DateFormatter('                                           %b %d')

# limites do eixo x
datemin = datetime(today.year, today.month, today.day, 0, 0)
datemax = datetime(finalDate.year, finalDate.month, finalDate.day, 21, 00)


# formata e gera os graficos (figuras separadas)
for (k, v), (k2, v2) in zip(dicSeriesHsOrdered.iteritems(), dicSeriesTpOrdered.iteritems()):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax1 = ax.twinx()
	ax.xaxis.set_major_locator(days)
	ax.xaxis.set_minor_locator(hours)
	ax.xaxis.set_major_formatter(dfmt)
	ax.set_xlim(datemin, datemax)
	ax.set_ylim(0, 8)
	ax1.set_ylim(0, 10)
	ax.grid(True)
	ax.set_title(u'Altura Significativa e Período Médio de Ondas - Ponto {0}'.format(k[8:9]))
	ax.plot(listField, v, linewidth=3)
	ax1.plot(listField, v2, 'r', linewidth=3)
	ax.set_ylabel('Altura (m)', color='b')
	ax1.set_ylabel(u'Período (s)', color='r')
	ax.set_xlabel('Tempo (horas)')
	fig.set_size_inches(15, 6)
	plt.legend(loc=2)
	plt.savefig(os.path.join(path_save, todayString + '_ponto{0}'.format(k2[8:9])))


'''
# formata e gera graficos juntos
# ponto 1
fig = plt.figure()
ax = plt.subplot(4,1,1)
ax1 = ax.twinx()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_minor_locator(hours)	
ax.xaxis.set_major_formatter(dfmt)
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 8)
ax1.set_ylim(0, 10)
ax.grid(True)
ax.set_title(u'Altura Significativa e Período Médio de Ondas - Ponto {0}'.format(dicSeriesHsOrdered.keys()[0][8:9]))
ax.plot(listField, dicSeriesHsOrdered.values()[0], linewidth=3)	
ax1.plot(listField, dicSeriesTpOrdered.values()[0], 'r', linewidth=3)
ax.set_ylabel('Altura (m)', color='b')
ax1.set_ylabel(u'Período (s)', color='r')
ax.set_xlabel('Tempo (horas)')

# ponto 2
ax = plt.subplot(4,1,2)
ax1 = ax.twinx()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_minor_locator(hours)	
ax.xaxis.set_major_formatter(dfmt)
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 8)
ax1.set_ylim(0, 10)
ax.grid(True)
ax.set_title(u'Altura Significativa e Período Médio de Ondas - Ponto {0}'.format(dicSeriesHsOrdered.keys()[1][8:9]))
ax.plot(listField, dicSeriesHsOrdered.values()[1], linewidth=3)	
ax1.plot(listField, dicSeriesTpOrdered.values()[1], 'r', linewidth=3)
ax.set_ylabel('Altura (m)', color='b')
ax1.set_ylabel(u'Período (s)', color='r')
ax.set_xlabel('Tempo (horas)')

# ponto 3
ax = plt.subplot(4,1,3)
ax1 = ax.twinx()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_minor_locator(hours)	
ax.xaxis.set_major_formatter(dfmt)
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 8)
ax1.set_ylim(0, 10)
ax.grid(True)
ax.set_title(u'Altura Significativa e Período Médio de Ondas - Ponto {0}'.format(dicSeriesHsOrdered.keys()[2][8:9]))
ax.plot(listField, dicSeriesHsOrdered.values()[2], linewidth=3)
ax1.plot(listField, dicSeriesTpOrdered.values()[2], 'r', linewidth=3)
ax.set_ylabel('Altura (m)', color='b')
ax1.set_ylabel(u'Período (s)', color='r')
ax.set_xlabel('Tempo (horas)')

# ponto 4
ax = plt.subplot(4,1,4)
ax1 = ax.twinx()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_minor_locator(hours)	
ax.xaxis.set_major_formatter(dfmt)
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 8)
ax1.set_ylim(0, 10)
ax.grid(True)
ax.set_title(u'Altura Significativa e Período Médio de Ondas - Ponto {0}'.format(dicSeriesHsOrdered.keys()[3][8:9]))
ax.plot(listField, dicSeriesHsOrdered.values()[3], linewidth=3)
ax1.plot(listField, dicSeriesTpOrdered.values()[3], 'r', linewidth=3)
ax.set_ylabel('Altura (m)', color='b')
ax1.set_ylabel(u'Período (s)', color='r')
ax.set_xlabel('Tempo (horas)')
plt.subplots_adjust(hspace=1.2)
fig.set_size_inches(20, 11)
plt.savefig(os.path.join(path_save, 'series_hs_tp'))


'''