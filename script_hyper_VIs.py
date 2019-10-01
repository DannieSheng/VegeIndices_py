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
import hdf5storage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt 
import pickle
import pdb

plt.close('all')

window_size = 5
dataPath  = r'T:\Box2\Drone Flight Data and Reference Files\Flight Data - All Sites\CLMB STND 2019 Flight Data\100085_2019_07_18_15_54_58'
hdrPath   = dataPath.replace(r'T:\Box2\Drone Flight Data and Reference Files\Flight Data - All Sites', r'T:\AnalysisDroneData\ReflectanceCube\ReadableHDR')
hyperPath = dataPath.replace(r'T:\Box2\Drone Flight Data and Reference Files\Flight Data - All Sites', r'T:\AnalysisDroneData\ReflectanceCube\MATdataCube')

## Get the list of all files
list_file_temp = [f for f in os.listdir(hyperPath) if f.startswith('raw_') and f.endswith('.mat')]

    # get the correct order of the files
list_file = []
for f in list_file_temp:
    cube_name = re.findall('\d+', f)[0]
    list_file.append(int(cube_name))
index_temp = np.argsort(list_file)
list_file  = [list_file_temp[i] for i in index_temp]

## Set the indices result saving path, if not exist, create on
indexPath = dataPath.replace(r'T:\Box2\Drone Flight Data and Reference Files\Flight Data - All Sites', r'T:\AnalysisDroneData\ReflectanceCube\indices')
if not os.path.exists(indexPath):
    os.makedirs(indexPath)

## load wavelengths indormation
temp = sio.loadmat(os.path.join(hdrPath, list_file[0]), squeeze_me = True)
parameters, wavelength = temp['parameters'], temp['wavelength']

## list of interested wavelengths which are used in calculation of the vege indices
list_wv = [445, 500, 510, 531, 550, 570, 650, 670, 675, 680, 681.25, 700, 708.75, 714, 733, 752, 753.75, 800, 900, 970]
idx_wv  = {}
for wv in list_wv:
    sorted_wv  = [wavelength[i] for i in np.argsort(abs(wavelength-wv))]
    id_temp    = np.where(wavelength == sorted_wv[0])[0]
    idx_wv[wv] = np.arange(id_temp-int(window_size/2), id_temp+int(window_size/2)+1)
    
## starting and ending indices of wavelengths of specific colors
list_wv_color = {'green': [540, 560],
                 'red_edge': [690, 710],
                 'blue': [450, 490],
                 'nir': [760, 800]}
idx_colors = dict()
for color in list_wv_color.keys():
    idx_temp = []
    for idx, wvl in enumerate(list_wv_color[color]):
        idx_temp.append(np.argsort(abs(wavelength-wvl))[0])
    idx_colors.update({color: idx_temp})
    
## filter to deal with some 0 reflectances
h = np.ones((3,3))
h[1,1] = 0

## loop over all images
for f in list_file:
    pdb.set_trace()
    indices = dict()
    R = dict()
    data = hdf5storage.loadmat(os.path.join(hyperPath, f))['data']
    f_ = f.replace('_rd_rf.mat', '')
    for color in list_wv_color.keys():
        R.update({color: np.average(data[:,:,idx_colors[color][0]:idx_colors[color][1]+1], axis = 2)})
    
#    R_wv = {}
    for wv in list_wv:
        R[wv] = np.average(data[:,:,idx_wv[wv]], axis = 2)
    pdb.set_trace()
        
    # getting rid of the "divided by zero" issue
    for key in R.keys():
        id_temp = np.where(R[key] == 0)[0]
        while id_temp.size>0:
           R_temp          = filters.correlate(R[key], h)
           R[key][id_temp] = R_temp[id_temp]
           id_temp         = np.where(R[key] == 0)[0]
    pdb.set_trace()
           
    # ACI
    indices['ACI'] = R['green']/R['nir']
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['ACI'])
    axs.set_title('Anthocyanin Content Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_aci.png'.format(f_)))
    
    # ARI
    indices['ARI'] = 1/R[550] - 1/R[700]
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['ARI'])
    axs.set_title('Anthocyanin Reflectance Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_ari.png'.format(f_)))
    
    # CARI
    indices['CARI'] = R[700] - R[670] -0.2*R[700]-R[550]
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['CARI'])
    axs.set_title('Chlorophyll Absorption in Reflectance Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_cari.png'.format(f_)))    

    # CI_red_edge
    indices['CI_red_edge'] = R['nir']/R['red_edge']
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['CI_red_edge'])
    axs.set_title('Chlorophyll Index Red Edge')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_ci_rededge.png'.format(f_)))
    
    # CRI
    indices['CRI'] = []
    indices['CRI'].append(1/R[510]-1/R[550])
    indices['CRI'].append(1/R[510]-1/R[700])
    fig, axs = plt.subplots(1,2)
    axs.ravel()
    im0 = axs[0].imshow(indices['CRI'][0])
    axs[0].set_title('Carotenoid Reflectance Index I')
    axs[0].axis('off')
    im1 = axs[1].imshow(indices['CRI'][1])
    axs[1].set_title('Carotenoid Reflectance Index II')
    axs[1].axis('off')
    plt.savefig(os.path.join(indexPath, '{}_cri.png'.format(f_)))    
    
    # EVI
    indices['EVI'] = 2.5*(R['nir']-R['red_edge'])/(R['nir']+6*R['red_edge']-7.5*R['blue']+1)
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['EVI'])
    axs.set_title('Enhanced Vegetation Index')
    plt.axis('off')    
    plt.savefig(os.path.join(indexPath, '{}_evi.png'.format(f_)))    
    
    # MARI
    indices['MARI'] = (1/R[550]-1/R[700])*R['nir']
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['MARI'])
    axs.set_title('Modified Anthocyanin Reflectance Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_mari.png'.format(f_)))   
    
    # MCARI
    indices['MCARI'] = ((R[700]-R[670])-0.2*(R[700]-R[550]))*(R[700]/R[670])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['MCARI'])
    axs.set_title('Modified Chlorophyll Absorption in Reflectance Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_mcari.png'.format(f_)))      
    
    # MTCI
    indices['MTCI'] = (R[753.75]-R[708.75])/(R[708.75]-R[681.25])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['MTCI'])
    axs.set_title('MERIS Terrestrial Chloroophyll Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_mtci.png'.format(f_)))      
    
    # NDVI
    indices['NDVI'] = (R['nir']-R['red_edge'])/(R['nir']+R['red_edge'])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['NDVI'])
    axs.set_title('Normalized Difference Vegetation Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_ndvi.png'.format(f_)))       
    
    # PRI
    indices['PRI'] = (R[531]-R[570])/(R[531]+R[570])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['PRI'])
    axs.set_title('Photochemical Reflectance Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_pri.png'.format(f_)))      
    
    # PSND
    indices['PSND'] = {}
    indices['PSND']['chl_a'] = (R[800]-R[675])/(R[800]+R[675])
    indices['PSND']['chl_b'] = (R[800]-R[650])/(R[800]+R[650])
    indices['PSND']['car']   = (R[800]-R[500])/(R[800]+R[500])
    
    fig, axs = plt.subplots(1,3)
    axs.ravel()
    im0 = axs[0].imshow(indices['PSND']['chl_a'])
    axs[0].set_title('Pigment Sensitive Normalized Difference for chl_a')
    axs[0].axis('off')
    im1 = axs[1].imshow(indices['PSND']['chl_b'])
    axs[1].set_title('Pigment Sensitive Normalized Difference for chl_b')
    axs[2].axis('off')
    im1 = axs[2].imshow(indices['PSND']['car'])
    axs[2].set_title('Pigment Sensitive Normalized Difference for car')
    axs[2].axis('off')
    plt.savefig(os.path.join(indexPath, '{}_psnd.png'.format(f_)))   
    
    # RGRI
    indices['RGRI'] = R['red_edge']/R['green']
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['RGRI'])
    axs.set_title('Red/Green Ration Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_rgri.png'.format(f_)))    
    
    # RVSI
    indices['RVSI'] = (R[714]+R[752])/2-R[733]
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['RVSI'])
    axs.set_title('Red-edge Vegetation Stress Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_rvsi.png'.format(f_))) 
    
    # SIPI
    indices['SIPI'] = (R[800]-R[445])/(R[800]-R[680])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['SIPI'])
    axs.set_title('Structure-Insensitive Pigment Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_sipi.png'.format(f_))) 
    
    # SR
    indices['SR'] = R[800]/R[675]
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['SR'])
    axs.set_title('Simple Ratio')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_sr.png'.format(f_))) 
    
    # VARI
    indices['VARI'] = (R['green']-R['red_edge'])/(R['green']+R['red_edge']-R['blue'])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['VARI'])
    axs.set_title('Visible Atmospherically Resistant Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_vari.png'.format(f_)))   
        
    # VI_green
    indices['VI_green'] = (R['green']-R['red_edge'])/(R['green']+R['red_edge'])
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['VI_green'])
    axs.set_title('Vegetation Index using Green band')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_vi_green.png'.format(f_)))  
    
    # WBI
    indices['WBI'] = R[900]/R[970]
    fig, axs = plt.subplots(1,1)
    im = axs.imshow(indices['WBI'])
    axs.set_title('Water Band Index')
    plt.axis('off')
    plt.savefig(os.path.join(indexPath, '{}_wbi.png'.format(f_))) 
    
    pickle.dump(indices, open(os.path.join(indexPath, '{}_VI.pkl'.format(f_)), 'wb'))
    
    plt.close('all')
    