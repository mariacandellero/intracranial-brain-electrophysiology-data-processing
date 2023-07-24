# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:05:46 2023

@author: Maria
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, hilbert, gaussian, find_peaks
from scipy import signal
from numpy.fft import fft
import scipy
import csv
from astropy.stats import rayleightest
from fooof import FOOOF
from fooof.bands import Bands


plv_arrays = []  
pval_arrays = [] 

for a in range(16):
    in_file_path = rf'C:\Users\Maria\Documents\Hippocampal_recordings\Rec_0802\tetrode{a+1}.npy'
    data_in = np.load(in_file_path)
    n_channels = 4
    srate = 30000
    dt = 1/srate

    for j in range(data_in.shape[1]):
        plv_list = []  # Initialize plv_list for each channel
        pval_list = []  # Initialize pval_list for each channel
        chan_1 = data_in[int(1e7):int(4e7), j] # select parts of data you want, don't take noise parts

        t1 = np.arange(0,chan_1.size/srate,dt)
        t_tot = chan_1.size/srate
           
        data = chan_1
        fs = srate # sample rate, Hz
        cutoff_low = 2  # desired cutoff frequency of the filter, Hz
        cutoff_high = 250  # desired cutoff frequency of the filter, Hz

        # Band-pass filtering
        chan_1_filt = butter_bandpass_filter(chan_1, cutoff_low, cutoff_high, fs, order=2)

        # Resampling the data 
        srate_new = 1000
        dt_new = 1/srate_new
        samples_new = round(srate_new*chan_1.size/srate)

        chan_1_down = signal.resample(chan_1_filt,(samples_new))

        tnew = np.arange(0,samples_new/srate_new,dt_new)
        tnew_max = samples_new/srate_new

        # Epoching
        n_epochs = int((len(chan_1_down) / (1*srate_new)) * 2 - 1)  # 50% overlap
        len_epoch = 1*srate_new
        
        
        # Isolation of a certain frequency band with a Butterworth band-pass filter
        fNQ = 1 / dt_new / 2 #Nyquist frequency
        df = 1 / tnew_max  #Frequency resolution
        
        # Definition of the frequency bands of interest
        frequency_bands = {'delta': [1, 4], 'theta': [4, 7], 'alpha': [8, 12], 'beta': [13, 30], 'gamma': [30, 150]}

        for band_name, band_range in frequency_bands.items():
            # Filter the data for the specific frequency band
            b, c = scipy.signal.butter(2, [band_range[0]/fNQ, band_range[1]/fNQ], 'band')
            filteredBandPass = scipy.signal.lfilter(b, c, chan_1_down)
            
            
            # spike rate definition
            spikesrate = 30000
            
            t_tot = chan_1.size/spikesrate
            dt = 1/spikesrate
            time = np.arange(0, t_tot, dt)


            # High-pass filtering
            low_cutoff = 500
            high_cutoff = 4000

            filt_data = butter_bandpass_filter(chan_1, low_cutoff, high_cutoff, spikesrate)


            # Spike detection
            mean_signal = np.mean(filt_data)
            abs_distance = np.abs(filt_data - mean_signal)
            median_distance = np.median(abs_distance)
            threshold = median_distance * 20

            peaks = find_peaks(filt_data, height=threshold, distance=spikesrate*0.005)
            peaks_x = peaks[0] / spikesrate
            peaks_y = peaks[1]['peak_heights']
            
            # Phases computation
            phases = lfp_spike_phases(filteredBandPass, srate_new, peaks_x)
            phase_diff = phases - np.pi

            # Roseplot of radians       
            polar_plot(phases)
            
            # Computaion of Phase-locking value        
            plv = abs(np.mean(np.exp(1j*phases)))

            # Computation of Rayleigh test
            pval = rayleightest(phases)
            
            plv_list.append(plv)
            pval_list.append(pval)

        plv_array_j = np.array(plv_list)
        pval_array_j = np.array(pval_list)
        plv_arrays.append(plv_array_j)
        pval_arrays.append(pval_array_j)

# Concatenation of the arrays for all channels
plv_array = np.concatenate(plv_arrays, axis=0)
pval_array = np.concatenate(pval_arrays, axis=0)