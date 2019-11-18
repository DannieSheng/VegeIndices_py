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

def rotate_mat(cube_name, list_rotate, mat):
    if cube_name in list_rotate:
        mat = np.rot90(mat)
    else:
        mat = np.rot90(mat, k = 3)
    return mat
    

path_VI = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\100083_2019_06_25_15_59_59'
path_gt = path_VI.replace(r'ReflectanceCube\indices', 'groundTruth')

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
    temp_gt  = sio.loadmat(os.path.join(path_gt, f), squeeze_me = True)
    gt       = temp_gt['gt']
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
    list_loc = np.unique(gt)
    df_summary = pd.DataFrame(columns = list_VI_, index = list_loc)
    for VI in list_VI:
        if VI == 'CRI':
            for i in range(0,len(indices['CRI'])):
                VI_ind = indices[VI][i]
                VI_ind = rotate_mat(cube_name, list_rotate, VI_ind)
                for loca in list_loc:
                    idx = np.where(gt == loca)
                    df_summary.loc[loca, 'CRI_' + str(i+1)] = np.average(VI_ind[np.where(gt == loca)])
        elif VI == 'PSND':
            for key in indices['PSND'].keys():
                VI_ind = indices[VI][key]
                VI_ind = rotate_mat(cube_name, list_rotate, VI_ind)
                for loca in list_loc:
                    idx = np.where(gt == loca)
                    df_summary.loc[loca, 'PSND_' + key] = np.average(VI_ind[np.where(gt == loca)])
        else:
            VI_ind = indices[VI]
            if cube_name in list_rotate:
                VI_ind = np.rot90(VI_ind)
            else:
                VI_ind = np.rot90(VI_ind, k = 3)
            for loca in list_loc:
                idx = np.where(gt == loca)
                df_summary.loc[loca, VI] = np.average(VI_ind[np.where(gt == loca)])
    df_summary.to_excel(output_writer, sheet_name = cube_name)
#    pdb.set_trace()
output_writer.save()
        