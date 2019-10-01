# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:01:27 2019
The code is used to generate summary of number of pixels belong to 6 classes of the switchgrass, for every image
@author: hdysheng
"""
import os
import scipy.io as sio
import numpy as np
import pandas as pd
import re
import funcs
import pdb

#def transfer(numID):
#    letter_ = numID%6
#    if letter_ == 0:
#        letter_ = 6
#        num = int((numID-6)/6)+1
#    else:
#        num     = int(numID/6)+1
#    
##    print(letter_)
#    if letter_ == 1:
#        letter = 'A'
#    elif letter_ == 2:
#        letter = 'B'
#    elif letter_ == 3:
#        letter = 'C'
#    elif letter_ == 4:
#        letter = 'D'
#    elif letter_ == 5:
#        letter = 'E'
#    elif letter_ == 6:
#        letter = 'F'
#    ID = str(num) + letter
#    return ID

id_path = r'T:\AnalysisDroneData\groundTruth\CLMB STND 2019 Flight Data\100085_2019_07_18_15_54_58\id_processed'
filelist = [f for f in os.listdir(os.path.join(id_path)) if f.endswith('.mat')]

# get the correct order of files
list_frame_idx_hyper = []
for f in filelist:
    hyper_cube_name = re.findall('\d+', f)[0]
    list_frame_idx_hyper.append(int(hyper_cube_name))
index_temp = np.argsort(list_frame_idx_hyper)
file_list = [filelist[i] for i in index_temp]

plot_list = [funcs.transfer(i) for i in range(1,37)]
col = [re.findall('\d+', f)[0] for f in file_list]
row = plot_list

#col = ['class {}'.format(i) for i in range(0,7)]
#row = [re.findall('\d+', f)[0] for f in file_list]
df_summary = pd.DataFrame(columns = col, index = row)

class_names = np.arange(1,37)
for f in file_list:
    count_final = np.zeros(36)
    hyper_cube_name = re.findall('\d+', f)[0]
    loaded = sio.loadmat(os.path.join(id_path, f), squeeze_me = True)
    plotID     = loaded['id']
    
    [plot_name, counts] = np.unique(plotID, return_counts = True)
    counts = counts[plot_name!=0]
    plot_name = plot_name[plot_name!=0]
    
    for idx, i_name in enumerate(plot_name):
        plt_id = funcs.transfer(i_name)
        df_summary.loc[plt_id, re.findall('\d+', f)[0]] = counts[idx]
       
df_summary.to_csv(os.path.join(id_path, 'summary.csv'), index = True, encoding = 'latin-1')
