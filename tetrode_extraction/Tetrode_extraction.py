# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 17:32:20 2023

@author: Maria
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_path = r'C:\Users\Maria\Documents\Hippocampal_recordings\Raw_recordings'
savepath_directory = r'C:\Users\Maria\Documents\Hippocampal_recordings\Rec_2411'

# Loading of all the data from Headstage64 workflow
suffix = '2022-11-24T12_40_02'; # Change to match file names' suffix

# RHD2164 64-Channel Bioamplfier Chip
rhd2164 = {}
rhd2164['ephys'] = np.fromfile(data_path + '\\' + 'rhd2164-ephys_' + suffix + '.raw', dtype=np.uint16)

# Reading of drive3-plate file into a DataFrame
df_plate = pd.read_csv(r'C:\Users\Maria\Documents\Hippocampal_recordings\drive3plate4.txt', delimiter='\t', decimal=',', header=None)
# Drop of the 7th column
df_plate = df_plate.drop(df_plate.columns[6], axis=1)
# Column names setting
column_plate_names = ['Site', '350,1 Hz|Mag (MOhm)', '350,1 Hz|Phase(°)', 'uA;(hh:mm:ss)', '350,1 Hz|Mag (MOhm)', '350,1 Hz|Phase(°)']
df_plate.columns = column_plate_names
# Add 3 rows of 0s to the bottom of the dataframe
for j in range(3):
    df_plate.loc[len(df_plate)] = [30]*len(df_plate.columns)
# Extraction of just the impedance magnitude column
df_plate = df_plate.iloc[:, 1]

n_chans = 64
n_tetrodes = int(n_chans/4)
srate = 30000
n_samples = int(np.shape(rhd2164['ephys'])[0]/64)
length_trace = n_samples / srate
dt = 1/srate
# 16 bits to cover +-6.4 mV, *1000 to convert mV to microV
scaler = (6.4*2 / 2**16) * 1000 

## Reshape and scale of the data with scaler
rhd2164['ephys'] = rhd2164['ephys'].reshape(n_samples, n_chans).astype('float64') * scaler 

chans_list = []
# Inspection of whether the impedance is ok
for h in range(63):
        if df_plate.iloc[h] < 10:
            chans = h
            chans_list.append(chans)
        else:
            chans = np.nan
chans_array = np.array(chans_list)

# Median calculation and substraction            
median = np.median(rhd2164['ephys'][:,chans_array] , axis=1)

for i in range(64):
    rhd2164['ephys'][:,i] = rhd2164['ephys'][:,i] - median

for i in range(n_tetrodes):
    start_chan = int(i*4)
    stop_chan = int(start_chan + 4)
    
    
    data = rhd2164['ephys'][:,start_chan:stop_chan]
    
    savepath_file = savepath_directory + '\\' + 'tetrode' + str(int(i+1)) + '.npy'
    np.save(savepath_file, data)
    
    print(start_chan + 1, stop_chan)