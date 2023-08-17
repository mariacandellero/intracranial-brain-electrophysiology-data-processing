# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:32:07 2023

@author: Maria
"""


from scipy.signal import butter, filtfilt
import numpy as np
from typing import Tuple


def butter_bandpass(lowcut : int, highcut: int, fs: float, order=2) -> Tuple[np.ndarray, np.ndarray]:
    """    
    Parameters
    ----------
    lowcut : Lower cutoff frequency of the bandpass filter.
    highcut : Upper cutoff frequency of the bandpass filter.
    fs : Sampling frequency.
    order : Order of the Butterworth filter (default is 2).

    Returns
    -------
    b : Filter coefficient
    a : Filter coefficient
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a



def butter_bandpass_filter(data: np.ndarray, lowcut: int, highcut: int, fs: float, order = 2) -> np.ndarray:
    """
    Parameters
    ----------
    data : Input data to be filtered.
    lowcut : Lower cutoff frequency of the bandpass filter.
    highcut : Upper cutoff frequency of the bandpass filter.
    fs : Sampling frequency.
    order : Order of the Butterworth filter (default is 2).

    Returns
    -------
    y : Filtered data.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y