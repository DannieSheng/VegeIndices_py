# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 14:24:47 2019
A script to calculate major hyperspectral vegetation indices
% Reference: Hyperspectral Remote Sensing of Vegetation (Second Edition, Volumne II)
@author: hdysheng
hdysheng@ufl.edu
University of Florida
"""
import os 
import re
import numpy as np
import scipy.io as sio
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt 
import pickle
import funcs
import pandas as pd
import pdb

plt.close('all')

viPath = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB STND 2019 Flight Data\100084_2019_06_25_16_39_57'
idPath = viPath.replace(r'ReflectanceCube\indices', 'groundTruth')
idPath = idPath + r'\id_processed'

## Get the summary file: with information of images correspond to plotIDs
plotID_info = pd.read_csv(os.path.join(idPath, 'summary.csv'), encoding = 'Latin-1', index_col = 0)
pixelsum    = plotID_info.sum(axis=1)

# Define the final result dataframe
list_plotIDs = plotID_info.index.values.tolist()
list_VIs     = ['ACI', 'ARI', 'CARI', 'CI_red_edge', 'EVI', 'MARI', 'MCARI', 'MTCI', 'NDVI', 
                'PRI', 'RGRI', 'RVSI', 'SIPI', 'SR','VARI', 'VI_green', 'WBI']
df_summary = pd.DataFrame(columns = list_VIs, index = list_plotIDs)

## Get the list of all files
list_file_temp = [f for f in os.listdir(idPath) if f.startswith('ID_') and f.endswith('.mat')]

    # get the correct order of the files
list_file = []
for f in list_file_temp:
    cube_name = re.findall('\d+', f)[0]
    list_file.append(int(cube_name))
index_temp = np.argsort(list_file)
list_file  = [list_file_temp[i] for i in index_temp]

## loop over all images
for idx, f in enumerate(list_file):
    f_idx = f.replace('.mat', '')
    f_idx = f_idx.replace('ID_', '')
    
    # find the indexes of plot_IDs this image includes
    idxID  = plotID_info[plotID_info[f_idx]>0].index.tolist()
    idxID_ = [funcs.reverse_transfer(i) for i in idxID]
    plot_id = sio.loadmat(os.path.join(idPath, f))['id']
    
    f_VI = f.replace('ID', 'raw')
    f_VI = f_VI.replace('.mat', '_VI.pkl')
     
    vis = pickle.load(open(os.path.join(viPath, f_VI), 'rb'))

    for id_idx, id_idx_ in zip(idxID, idxID_):
        id_map = np.zeros_like(plot_id)
        id_map[np.where(plot_id == id_idx_)] = 1
        for vi in list_VIs:
            vi_mat = vis[vi]
            vi_mat_ = vi_mat*id_map
            
            if pd.isna(df_summary.loc[id_idx, vi]):
                df_summary.loc[id_idx, vi] = sum(sum(vi_mat_))/pixelsum[id_idx]
            else:
#                pdb.set_trace()
                df_summary.loc[id_idx, vi] += sum(sum(vi_mat_))/pixelsum[id_idx]
df_summary.to_csv(os.path.join(viPath, 'VI_summary.csv'), index = True, encoding = 'Latin-1')
       