# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:00:59 2023

@author: Maria
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def amplitude_spectrum_plot(freqs: np.ndarray, chan_1_epoched_fft: np.ndarray) -> Tuple[plt.Figure, plt.Axes]:
    """    
    Parameters
    ----------
    freqs : array of frequency values in Hz, representing the frequency axis of the amplitude spectrum.
    chan_1_epoched_fft : FFT (Fast Fourier Transform) of the epoched EEG data for a specific channel.

    Returns
    -------
    fig : figure containing the amplitude spectrum plot.
    ax : the plot's axes.
    """
    
    fig, ax = plt.subplots(figsize=(16, 10))
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    time = np.arange(0.5, int(np.shape(chan_1_epoched_fft)[1]/2 + 1), 0.5)

    levels = np.linspace(np.min(np.sqrt(chan_1_epoched_fft)), np.max(np.sqrt(chan_1_epoched_fft)) / 4, 100)
    plt.contourf(time, freqs, np.sqrt(chan_1_epoched_fft), cmap="jet", levels=levels)

    plt.ylim(0, 80)
    plt.title('Spectrum', fontsize=25, fontweight='bold')
    plt.xlabel('Time [s]', fontsize=20, fontweight='bold')
    plt.ylabel('Frequency [Hz]', fontsize=20, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)

    return fig, ax