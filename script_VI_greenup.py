# -*- coding: utf-8 -*-
"""
Relate the VIs to the greenup data

@author: hdysheng
"""
import os
import pandas as pd

path_all     = r'T:\AnalysisDroneData\ReflectanceCube\indices\CLMB STND 2019 Flight Data'
path_VI      = r'{}\100081_2019_06_11_17_57_06'.format(path_all)
path_greenup = r'{}\greenup_related'.format(path_all)
name_VI      = 'VI_summary.csv'
name_greenup = 'CLMB_STND_2019_Master Data_Working.xlsx'

df_VI = pd.read_csv(os.path.join(path_VI, name_VI), encoding = 'Latin-1', index_col = 0)
df_VI = df_VI.reset_index()
df_VI = df_VI.rename(columns = {'index': 'PLOT_GL'})
df_greenup = pd.read_excel(open(os.path.join(path_greenup, name_greenup), 'rb'),
                           sheet_name = 'Sheet1', index_col = 0, encoding = 'Latin-1')

df_final = df_VI.merge(df_greenup, on = 'PLOT_GL', how = 'right')
#df_final = pd.merge(df_VI.assign(x=df_VI.PLOT_GL.astype(str)),
#                    df_greenup.assign(x=df_greenup.PLOT_GL.astype(str)),
#                    how = 'inner', on = 'x')

df_final.to_csv(os.path.join(path_VI, 'VI_summary_greenup.csv'), index = False, encoding = 'Latin-1')
