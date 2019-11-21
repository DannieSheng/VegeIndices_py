# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:19:01 2019
A script to assign VI to plots of the GWAS field based on the ground truth
@author: hdysheng
"""

import os
import re
import numpy as np
import scipy.io as sio
import pandas as pd
import copy
import pickle
import matplotlib.pyplot as plt
import pdb

def rotate_mat(cube_name, list_rotate, mat):
    if cube_name in list_rotate:
        mat = np.rot90(mat)
    else:
        mat = np.rot90(mat, k = 3)
    return mat
    

path_VI        = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\100083_2019_06_25_15_59_59'
path_gt        = path_VI.replace(r'ReflectanceCube\indices', 'groundTruth')
path_detected  = path_gt + r'\gt_map'

path_greenup = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\greenup_related'
name_greenup = 'CLMB_GWAS_2019_Greenup Data.xlsx'
df_greenup   = pd.read_excel(os.path.join(path_greenup, name_greenup), sheet_name = 'CLMB GWAS 2019 Greenup Data')

# list of all files with ground truth
list_file_temp = [f for f in os.listdir(path_gt) if f.endswith('.mat')]

list_rotate = ['612', '2612', '4612', '10336', '12336', '14336', '19975', '21975', '23975', '29393', '31393', '33393', '39100', '41100', '43100', '48433', '50433', '52433']

    # get the correct order of all files
list_file = []
for f in list_file_temp:
    cube_name = re.findall('\d+', f)[0]
    list_file.append(int(cube_name))
index_temp    = np.argsort(list_file)
list_file     = [list_file_temp[i] for i in index_temp]
output_writer = pd.ExcelWriter(os.path.join(path_VI, 'VI_indices_all.xlsx'))
count = 0
for f in list_file:
    count += 1
    cube_name = re.findall('\d+', f)[0]            
    loaded   = sio.loadmat(os.path.join(path_gt, f), squeeze_me = True)
    gt       = loaded['gt']
    gt_map = np.zeros(np.shape(gt))
    gt_map[np.where(gt>0)] = 1
    
    name_detected = 'gt_map_' + cube_name + '_temp.mat'
    loaded        = sio.loadmat(os.path.join(path_detected, name_detected), squeeze_me = True)
    detected      = loaded['detected']
    
    added      = gt_map - detected
    added_gt   = added*gt
    list_added = [str(int(i)) for i in np.unique(added_gt)]
    list_added.remove('0')
#    pdb.set_trace()
    f_VI     = 'raw_' + cube_name + '_VI.pkl'
    indices  = pickle.load(open(os.path.join(path_VI, f_VI), 'rb'))
    list_VI  = list(indices.keys())
    list_VI_ = copy.deepcopy(list_VI)
    list_VI_.remove('CRI')
    list_VI_.remove('PSND')
    list_VI_.append('CRI_1')
    list_VI_.append('CRI_2')
    for key in indices['PSND'].keys():
        list_VI_.append('PSND_' + key)
    list_loc  = np.unique(gt)
    list_loc_ = ['C'+str(loc) for loc in list_loc]
    df_summary = pd.DataFrame(columns = list_VI_.append('added?'), index = list_loc_)
    
    ##
    for loca in list_loc:
        idx = np.where(gt == loca)
        
        # indicate whether added by hand
        if str(loca) in list_added:
            df_summary.loc['C'+str(loca), 'added?'] = 1
        else:
            df_summary.loc['C'+str(loca), 'added?'] = 0
        
        # indicate the location in the ground truth matrix
        idx = np.where(gt == loca)
        
        # go over every VI
        for VI in list_VI:
            if VI == 'CRI':
                for i in range(0,len(indices['CRI'])):
                    VI_ind = indices[VI][i]
                    VI_ind = rotate_mat(cube_name, list_rotate, VI_ind)
                    df_summary.loc['C' + str(loca), 'CRI_' + str(i+1)] = np.average(VI_ind[np.where(gt == loca)])
            elif VI == 'PSND':
                for key in indices['PSND'].keys():
                    VI_ind = indices[VI][key]
                    VI_ind = rotate_mat(cube_name, list_rotate, VI_ind)
                    df_summary.loc['C' + str(loca), 'PSND_' + key] = np.average(VI_ind[np.where(gt == loca)])
            else:
                VI_ind = indices[VI]
                VI_ind = rotate_mat(cube_name, list_rotate, VI_ind)
                df_summary.loc['C' + str(loca), VI] = np.average(VI_ind[np.where(gt == loca)])
    
    df_summary = df_summary.reset_index()
    df_summary = df_summary.merge(df_greenup, left_on = 'index', right_on = 'PLOT_GL', how = 'left')
    df_summary.to_excel(output_writer, sheet_name = cube_name)
output_writer.save()
        