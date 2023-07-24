# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:01:58 2023

@author: Maria
"""

import numpy as np
import scipy


# Extraction of array of LFPs phases at which spikes occurred
def lfp_spike_phases(lfp: np.ndarray, srate_lfp: float, spike_train: np.ndarray) -> np.ndarray:
    """
    Compute the phase of the LFP at the time of each spike.
    
    Parameters
    ----------
    lfp : LFP trace.
    srate_lfp : Sampling rate of LFP.
    spike_train : Times of spike occurrences.
    
    Returns
    -------
    lfp_phases : Array of LFP phases at each time point when a spike occurred.
    """
    
    # Application of Hilbert transform 
    analytic_signal = scipy.signal.hilbert(filteredBandPass)

    # Extraction of LFPs amplitude and phase 
    amplitude = np.abs(analytic_signal)
    instantaneous_phase = np.angle(analytic_signal)

    # Compution of spike indices
    spike_indices = np.round(spike_train * srate_lfp).astype(int)
    spike_indices = spike_indices[spike_indices < len(lfp)]

    # Extraction of phases 
    phases = instantaneous_phase[spike_indices]

    return phases