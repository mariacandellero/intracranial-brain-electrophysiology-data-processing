# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:53:47 2023

@author: Maria
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import  gaussian
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from typing import Tuple, List




avg_spike_rate_list = []


for a in range(16):
    in_file_path = rf'C:\Users\Maria\Documents\Hippocampal_recordings\Rec_0202\tetrode{a+1}.npy'
    data_in = np.load(in_file_path)
    n_channels = 4
    srate = 30000

    for j in range(data_in.shape[1]):
        chan_1 = data_in[int(1e7):int(4e7), j]  # select parts of data you want, don't take noise parts

        t_tot = chan_1.size / srate
        dt = 1 / srate
        t1 = np.arange(0, t_tot, dt)

        # High-pass filtering
        low_cutoff = 500
        high_cutoff = 4000

        filt_data = butter_bandpass_filter(chan_1, low_cutoff, high_cutoff, srate)

        # Spike detection
        mean_signal = np.mean(filt_data)
        abs_distance = np.abs(filt_data - mean_signal)
        median_distance = np.median(abs_distance)
        threshold = median_distance * 20

        peaks = find_peaks(filt_data, height=threshold, distance=srate * 0.005)
        peaks_x = peaks[0] / srate
        peaks_y = peaks[1]['peak_heights']

        # Spike rate calculation
        spike_rate = extract_frequency_bins(peaks_x, bin_size=1, start=np.min(t1), stop=np.max(t1))
        avg_spike_rate = np.mean(spike_rate[1])
        avg_spike_rate_list.append(avg_spike_rate)
        avg_spike_rate_array = np.array(avg_spike_rate_list)


        # Windows around spikes extraction 
        window_size = 0.001
        windows = spike_windows_extraction(filt_data, peaks_x, window_size)

        

