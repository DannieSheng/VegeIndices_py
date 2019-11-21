# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:22:27 2019
A script to save the VI and the greenup data into a same table, and append as a new sheet to the 'VI_indices_all.xlsx' file
@author: hdysheng
"""

import os
import pandas as pd
#import re
import pdb

path_greenup = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\greenup_related'
name_greenup = 'CLMB_GWAS_2019_Greenup Data.xlsx'
df_greenup   = pd.read_excel(os.path.join(path_greenup, name_greenup))
path_indices  = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB GWAS 2019 Flight Data\100083_2019_06_25_15_59_59'
name_indices  = 'VI_indices_all.xlsx'
xl_indices    = pd.ExcelFile(os.path.join(path_indices, name_indices))
output_writer = pd.ExcelWriter(os.path.join(path_indices, name_indices), engine="openpyxl", mode = 'a')
count        = 0
for sheetname in xl_indices.sheet_names:
    df_ind = pd.read_excel(xl_indices, sheetname)
    
    df_ind = df_ind.rename(columns = {"index": "location"})    

    if count == 0:
        df_merged = df_ind
    else:
        df_merged = df_merged.append(df_ind, ignore_index = True)
    count += 1
df_merged = df_merged.sort_values(by = ['location'])
df_merged.to_excel(output_writer, sheet_name = 'all')
output_writer.save()
