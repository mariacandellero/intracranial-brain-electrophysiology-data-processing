# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:53:52 2023

@author: Maria
"""

import numpy as np
from scipy import signal
from numpy.fft import fft
import scipy


theta_contribution_list = []
total_list = []
associated_band_list = [] 
highest_peak_power_list = []

for a in range(16):
    in_file_path = rf'C:\Users\Maria\Documents\Hippocampal_recordings\Rec_0811\tetrode{a+1}.npy'
    data_in = np.load(in_file_path)
    n_channels = 4
    srate = 30000
    dt = 1/srate


    for j in range(data_in.shape[1]):
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

        # Total power spectrum
        window = signal.blackmanharris(len_epoch)
        chan_1_epoched_fft = np.zeros((len_epoch, n_epochs))
        
        for i in range(n_epochs):
            start = int(i*(len_epoch/2)) #50% overlap
            stop = int(start + len_epoch)
            epoch = signal.detrend(chan_1_down[start:stop])
            chan_1_epoched_fft[:,i] = (np.abs(fft(epoch*window)) / len(epoch)) ** 2 
            
            
        average_spectrum = np.mean(chan_1_epoched_fft, axis=1)
        average_spectrum = average_spectrum[:int(len(average_spectrum) / 2)]
        total =  np.sum(average_spectrum)      
        total_list.append(total)
        total_array = np.array(total_list)
        
        fNQ = 1 / dt_new / 2 #Nyquist frequency
        df = (fNQ)/len(average_spectrum) #Frequency resolution
        faxis = np.arange(0,fNQ,df)
        freq_range = (3, 150)  # Definition of the frequency range of interest

        # Determination of frequency band and power of the highest peak in the spectrum
        associated_band, highest_peak_power = find_highest_peak(faxis, average_spectrum, freq_range)
        associated_band_list.append(associated_band)
        associated_band_array = np.array(associated_band_list)
        highest_peak_power_list.append(highest_peak_power)
        highest_peak_power_array = np.array(highest_peak_power_list)
        
        # Isolation of a certain frequency band with a Butterworth band-pass filter
        fNQ = 1 / dt_new / 2 #Nyquist frequency
        df = 1 / tnew_max  #Frequency resolution

        b, c = scipy.signal.butter(3, [4/fNQ, 7/fNQ], 'band')
        filteredBandPass = scipy.signal.lfilter(b, c, chan_1_down)
        
        # epoching
        n_epochs_t = int((len(filteredBandPass) / (1*srate_new)) * 2 - 1)  # 50% overlap
        len_epoch_t = 1*srate_new

        window_t = signal.blackmanharris(len_epoch_t)
        chan_1_epoched_fft_t = np.zeros((len_epoch_t, n_epochs_t))
        for k in range(n_epochs_t):
            start_t = int(k*(len_epoch_t/2)) #50% overlap
            stop_t = int(start_t + len_epoch_t)
            epoch_t = signal.detrend(filteredBandPass[start_t:stop_t])
            chan_1_epoched_fft_t[:,k] = (np.abs(fft(epoch_t*window_t)) / np.sum(window_t)) ** 2    
        
        
        average_spectrum_t = np.mean(chan_1_epoched_fft_t, axis=1)
        average_spectrum_t = average_spectrum_t[:int(len(average_spectrum_t) / 2)]
        average_spectrum_t = 10*np.log10(average_spectrum_t)
        
        theta_contribution =  np.sum(average_spectrum_t)       
        theta_contribution_list.append(theta_contribution)
        theta_contribution_array = np.array(theta_contribution_list)