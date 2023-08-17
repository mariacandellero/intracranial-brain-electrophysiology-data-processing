# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:47:55 2023

@author: Maria
"""

import numpy as np
from typing import List


def spike_windows_extraction(data: np.ndarray, spike_times: np.ndarray, window_size: float) -> List[np.ndarray]:
    '''
    Parameters
    ----------
    data : Continuous data from which windows around spikes are to be extracted.
    spike_times : Spike times (timestamps) at which the spike windows will be centered.
    window_size : Size of the spike windows in seconds.

    Returns
    -------
    spike_windows : Windows of data around each spike time.
    '''
    srate = 30000  # Change this to your actual sampling rate if available
    spike_windows = []
    for t in spike_times:
        start_idx = int((t - window_size) * srate)
        end_idx = int((t + window_size) * srate)
        s_w = data[start_idx:end_idx]
        spike_windows.append(s_w)
    return spike_windows