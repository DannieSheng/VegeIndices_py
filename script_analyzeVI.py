#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script to examine the VIs and the relationship between VIs and the greenup data (correlation)

@author: hudanyunsheng
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb

path    = '/Users/hudanyunsheng/Google Drive'
name    = 'VI_indices_all.xlsx'
list_VI = ['ACI', 'ARI', 'CARI', 'CI_red_edge', 'CRI_1', 'CRI_2',
       'EVI', 'MARI', 'MCARI', 'MTCI', 'NDVI', 'PRI', 'PSND_chl_a',
       'PSND_chl_b', 'PSND_car', 'RGRI', 'RVSI', 'SIPI', 'SR', 'VARI',
       'VI_green', 'WBI']
list_GR = ['GR1', 'GR50', 'GR100']
list_color = ['r', 'g', 'b']

df   = pd.read_excel(os.path.join(path, name), sheet_name = 'all', usecols = "B:AG", encoding = 'Latin-1')

    # drop the column 'Unnamed: 0.1' if needed
df   = df.drop(columns = 'Unnamed: 0.1')

    # get rid of invalid rows (for those with no 'WINTER_SURVIVAL' values, they are invalid)
row_loc = df[df['WINTER_SURVIVAL'].isnull()].index
df      = df.drop(index = row_loc)

    # get the summary of the switchgrass field: alive, dead or weak
#df_summary = df[['WINTER_SURVIVAL', 'location']].groupby('WINTER_SURVIVAL').agg({
#                'location': 'count'})
#df_summary = df_summary.reset_index(drop=False)

df_summary = df[['WINTER_SURVIVAL']].groupby('WINTER_SURVIVAL').agg({
                'WINTER_SURVIVAL': ['count']})
df_summary.columns = df_summary.columns.droplevel(0)
df_summary = df_summary.reset_index(drop=False)
df_summary['ratio'] = df_summary['count']/sum(df_summary['count'])

    # examine the distribution of VIs for dead and survive plots
output_writer1 = pd.ExcelWriter(os.path.join(path, 'VI_distri.xlsx'))
#loc_dead      = df[df['WINTER_SURVIVAL'] == 'N'].index
loc_survive   = df[df['WINTER_SURVIVAL'] == 'Y'].index
#fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
for VI in list_VI:
#    df_dead    = df.loc[loc_dead, VI]
#    df_survive = df.loc[loc_survive, VI]
    df_temp = df[[VI, 'WINTER_SURVIVAL']]
    df_temp_summary = df_temp.groupby('WINTER_SURVIVAL').agg({
            VI: ['min', 'max', 'mean', 'std']})
    df_temp_summary.columns = df_temp_summary.columns.droplevel(0)
#    ax1.plot(VI, df_temp_summary.loc['N','min'], 'r.-', label = 'dead')
#    ax1.plot(VI, df_temp_summary.loc['Y','min'], 'b.-', label = 'survived')
#    ax2.plot(VI, df_temp_summary.loc['N','max'], 'r.-', label = 'dead')
#    ax2.plot(VI, df_temp_summary.loc['Y','max'], 'b.-', label = 'survived')
#    ax3.plot(VI, df_temp_summary.loc['N','mean'], 'r.-', label = 'dead')
#    ax3.plot(VI, df_temp_summary.loc['Y','mean'], 'b.-', label = 'survived')
    fig, ax1 = plt.subplots(1,1)
    ax1.plot('dead', df_temp_summary.loc['N','min'], 'r*')
    ax1.plot('dead', df_temp_summary.loc['N','max'], 'g*')
    ax1.plot('dead', df_temp_summary.loc['N','mean'], 'b*')
    ax1.plot('survive', df_temp_summary.loc['N','min'], 'r*')
    ax1.plot('survive', df_temp_summary.loc['N','max'], 'g*')
    ax1.plot('survive', df_temp_summary.loc['N','mean'], 'b*')
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.tight_layout()
    plt.savefig(os.path.join(path, VI+'dist.png'))
    df_temp_summary.to_excel(output_writer1, sheet_name = VI)
    plt.close('all')
#output_writer1.save()
pdb.set_trace()
    # examine the correlation of VIs and greenup data (3) for survived plots
corr_all   = dict()
count      = 0
fig, axs   = plt.subplots(1,1)
for GR in list_GR:
    corr_all[GR] = dict()
    for VI in list_VI:
        df_temp = df.loc[loc_survive, [VI, GR]]
        corr_all[GR][VI] = np.corrcoef(df_temp[VI], df_temp[GR])[0,1]
    list_temp = [corr_all[GR][k] for k in corr_all[GR].keys()]
#    plt.figure(figsize=(50,100))
    axs.plot(list_VI, list_temp, list_color[count] + '.-', label = GR)
    count += 1
axs.legend()
plt.xticks(fontsize = 14, rotation=80)
plt.yticks(fontsize = 14)
plt.tight_layout()
plt.savefig(os.path.join(path, 'correlation.png'))
    