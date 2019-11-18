# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 16:50:08 2019

@author: hdysheng
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pylab as pl
import pdb

plt.close('all')
df_all = dict()
list_dates   = ['100081_2019_06_11_17_57_06', '100084_2019_06_25_16_39_57', '100085_2019_07_18_15_54_58']
list_dates_  = ['2019_06_11', '2019_06_25', '2019_07_18']
name_VI      = 'VI_summary_greenup.csv'
savepath     = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB STND 2019 Flight Data\greenup_related'

list_VI  = ['ACI', 'ARI', 'CARI', 'CI_red_edge', 'EVI', 'MARI', 'MCARI', 'MTCI', 'NDVI', 'PRI', 'RGRI', 'RVSI', 'SIPI', 'SR', 'VARI', 'VI_green', 'WBI']
for date in list_dates:
    path_VI      = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB STND 2019 Flight Data\{}'.format(date)
    df_VI        = pd.read_csv(os.path.join(path_VI, name_VI), encoding = 'Latin-1')
    df_all[date] = df_VI
list_geno = df_VI['GENO'].unique() 
for VI in list_VI:
    for (idx, date) in enumerate(list_dates):
        df_temp = df_all[date][['PLOT_GL', VI, 'PLOT_LC', 'GENO']]
        if idx == 0:
            df_VIdate = df_temp
            df_VIdate = df_VIdate.rename(columns = {VI: date})
#            pdb.set_trace()
        else:
            df_VIdate = df_VIdate.merge(df_temp, how = 'inner', on = ['PLOT_GL', 'PLOT_LC', 'GENO'])
            df_VIdate = df_VIdate.rename(columns = {VI: date})
    
    for (idx, geno) in enumerate(list_geno):
        cond = df_VIdate['GENO'] == geno
        df_geno = df_VIdate.loc[cond,:]  
        list_loc = df_geno['PLOT_LC']
        fig = plt.figure(figsize=(10,8))
        for loc in list_loc:
            cond1 = df_geno['PLOT_LC'] == loc
            VI_value = df_geno.loc[cond1, list_dates].astype(datetime).values.tolist()[0]
            
            plt.plot(list_dates_, VI_value, '^-', label = loc)
        plt.title('{} for {}'.format(VI, geno))
        plt.legend(loc = 'best')
        pl.xticks(rotation=45)
        pl.yticks(rotation=45)
#        pdb.set_trace()
        plt.savefig(os.path.join(savepath, '{}_{}.png'.format(VI, geno)))
    plt.close('all')
#        pdb.set_trace()
            
    


