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
path_greenup = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB STND 2019 Flight Data\greenup_related'
name_greenup = 'CLMB_STND_2019_Master Data_Working.xlsx'
df_greenup   = pd.read_excel(os.path.join(path_greenup, name_greenup),sheet_name='Sheet1')

list_geno = df_greenup['GENO'].unique()
greenup_rate = ['first green tiller', '50% crown green up', '100% crown green up']
#fig, axs = plt.subplots(2,3)
#axs = axs.ravel()
for (idx, geno) in enumerate(list_geno):
    cond = df_greenup['GENO'] == geno
    df_geno = df_greenup.loc[cond,:]
    list_loc = df_geno['PLOT_LC']
#    fig= plt.figure(figsize=(12,8))
    fig, ax = plt.subplots(figsize=(13,10))
    for loc in list_loc:
        cond1 = df_geno['PLOT_LC'] == loc
#        gr = df_geno.loc[cond1, ['GREEN1', 'GREEN50', 'GREEN100']].values.tolist()[0]
        gr = df_geno.loc[cond1, ['Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']].astype(datetime).values.tolist()[0]
        plt.plot(gr, greenup_rate, '^-', label = loc)
#        axs[idx].plot(gr, greenup_rate, '^-', label = loc)
    ax.tick_params(labelsize=12)
    plt.title('Green up information for {}'.format(geno), fontsize = 20)
    plt.legend(loc = 'best')
    pl.xticks(rotation=40)
    pl.yticks(rotation=55)
    
    plt.savefig(os.path.join(path_greenup, '{}.png'.format(geno)))
#    pdb.set_trace()
#    
