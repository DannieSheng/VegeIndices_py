# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:44:27 2019
A script to plot the green up data on top of the original image
@author: hdysheng
"""

import os
import pandas as pd
import scipy.io as sio
import numpy as np
import re
import matplotlib.pyplot as plt
import pickle
import pdb

# path of VI and greenup data (saved in the same file already)
path           = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\100083_2019_06_25_15_59_59'
name           = 'VI_indices_all.xlsx'

path_gt        = r'T:\AnalysisDroneData\groundTruth\CLMB GWAS 2019 Flight Data\100083_2019_06_25_15_59_59'
path_detected  = path_gt + r'\gt_map'

path_GR        = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\greenup_related'

excel_file     = pd.ExcelFile(os.path.join(path, name))
# list_sheetname = excel_file.sheet_names

    # get the list of all files with ground truth
list_file_temp = [f for f in os.listdir(path_gt) if f.endswith('.mat')]

    # get the correct order of the files
list_file = []
for f in list_file_temp:
    cube_name = re.findall('\d+', f)[0]
    list_file.append(int(cube_name))
index_temp = np.argsort(list_file)
list_file = [list_file_temp[i] for i in index_temp]

list_GR_cols = ['GR1', 'GR50', 'GR100']

# for cube in list_sheetname:
    # df_VI         = excel_file.parse(cube) 
    # name_gt       = 'gt_' + cube + '.mat'
    # name_detected = 'gt_map_' + cube + '_temp.mat'
    # loaded = sio.loadmat(os.path.join(path_gt, name_gt), squeeze_me = True)
for f in list_file:
    cube_name = re.findall('\d+', f)[0]
    name_detected = 'gt_map_' + cube_name + '_temp.mat'
    loaded = sio.loadmat(os.path.join(path_gt, f), squeeze_me = True)
    gt     = loaded['gt']
    list_loc = list(np.unique(gt))
    list_loc.remove(0)
    gt_map = np.zeros(np.shape(gt))
    gt_map[np.where(gt>0)] = 1

#    loaded   = sio.loadmat(os.path.join(path_detected, name_detected), squeeze_me = True)
#    detected = loaded['detected']
#
#    added    = gt_map - detected
#    added_gt = added*gt

    df_info   = excel_file.parse(sheet_name = cube_name)
    # get rid of 'nan's
    for col in list_GR_cols:
        df_info.loc[df_info[col].isnull(), col] = 1
        
    GR = dict()
    for col in list_GR_cols:
        GR[col] = np.zeros(np.shape(gt))
        for loc in list_loc:
            GR[col][np.where(gt == loc)] = df_info.loc[df_info[df_info['index'] == 'C{}'.format(loc)].index.tolist(), str(col)]
        fig, axs = plt.subplots(1,1)
        im = axs.imshow(GR[col])
        axs.set_title(col)
        plt.axis('off')
        plt.savefig(os.path.join(path_GR, '{}_{}.png'.format(cube_name, col)))
    with open(os.path.join(path_GR, '{}.pkl'.format(cube_name)), 'wb') as f:
        pickle.dump(GR, f)
    plt.close('all')
#    pdb.set_trace()
