# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:44:21 2023

@author: Maria
"""

import numpy as np
from fooof import FOOOF
from fooof.plts.spectra import plot_spectra_shading
from typing import Tuple


def find_highest_peak(faxis: np.ndarray, average_spectrum: np.ndarray, freq_range: Tuple[int, int]) -> Tuple[str, float]:
    """    
    Parameters
    ----------
    faxis : array of frequency values in Hz, representing the frequency axis of the EEG power spectrum.
    average_spectrum : array representing the average power values corresponding to each frequency in `faxis`.
    freq_range : tuple containing the frequency range for fitting the aperiodic and periodic components using the FOOOF library.

    Returns
    -------
    associated_band : string representing the frequency band associated with the highest peak found in the power spectrum. The value will be one of the following: 'delta', 'theta', 'alpha', 'beta', or 'gamma'.
    highest_peak_power : power value of the highest peak found in the power spectrum.
    """
    
    # Frequency bands of interest
    frequency_bands = {'delta': [1, 4], 'theta': [4, 7], 'alpha': [8, 12], 'beta': [13, 30], 'gamma': [30, 150]}
    bands_list = [freq_range for _, freq_range in frequency_bands.items()]
    shade_cols = ['#e8dc35', '#46b870', '#1882d9', '#a218d9', '#e60026']
    

    # Calculation of the frequency peaks using fooof
    fm = FOOOF()
    fm.fit(faxis, average_spectrum, freq_range)
    fm.report(faxis, average_spectrum, freq_range)
    full_peak_fit = fm._peak_fit

    # Plot of the power spectrum with shading for frequency bands
    plot_spectra_shading(fm.freqs, [full_peak_fit], linewidth=3, shades=bands_list, shade_colors=shade_cols)

    # Extraction of the peak parameters
    peak_params = fm.get_params('peak_params')

    # Peak with the highest power
    highest_peak_idx = np.argmax(peak_params[:, 1])
    highest_peak_freq = peak_params[highest_peak_idx, 0]
    highest_peak_power = peak_params[highest_peak_idx, 1]

    # Highest peak corresponding frequency band  
    associated_band = None
    for band_name, band_range in frequency_bands.items():
        if band_range[0] <= int(highest_peak_freq) <= band_range[1]:
            associated_band = band_name
            break

    return associated_band, highest_peak_power