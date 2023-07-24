# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:44:33 2023

@author: Maria
"""
import numpy as np
from typing import Tuple


# Extract frequency bins function definition
def extract_frequency_bins(spiketimes: np.ndarray, bin_size: float, start: float, stop: float, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Parameters
    ----------
    bin_time, spike_count = extract_frequency_bins(spiketimes, bin_size, start, stop, **kwargs)
    
    bin_size: bin size in seconds
    start: the point in the recording where the function starts binning in seconds
    stop: the point in the recording where the function stops binning in seconds
    **kwargs: TYPE
        - smooth_method: by default, no smoothing is performed, but 'moving_average' or 'gaussian' smoothing can be performed
        - smooth_window: if smoothing is performed, provide a smoothing window (number of bins) as an integer. Default is 5 bins.
        - smooth_sigma: if gaussian smoothing is performed, provide a sigma value, denoting the narrowness of the filter
    
    Returns
    -------
    bin_time: numpy array of time bins (center of bins) in seconds
    spike_count: numpy array of spike frequency in each time bin, if several templates are selected this will be a 2D array
    '''
    smooth_method = kwargs.get('smooth_method', 'none')
    smooth_window = kwargs.get('smooth_window', 5)
    n_bins = int((stop - start)/bin_size)
    bin_time = np.arange(0,(stop-start), bin_size) + bin_size/2
    
    spiketimes = spiketimes
    spike_count = np.histogram(spiketimes, n_bins, (start, stop))[0] 
    spike_count = spike_count / bin_size

    
    return bin_time, spike_count