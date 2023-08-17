# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:37:11 2023

@author: Maria
"""

import numpy as np
from scipy.signal import  gaussian



def movingaverage(values: np.ndarray, window: int) -> np.ndarray:
    """    
    Parameters
    ----------
    values : Values representing the data to be smoothed using the moving average method.
    window : size of the moving average window. 

    Returns
    -------
    smas : Result of the moving average smoothing operation.
    """
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'same')

    return smas  

def gaussian_smooth(values: np.ndarray, window: int, sigma: float) -> np.ndarray:
    """    
    Parameters
    ----------
    values : Values representing the data to be smoothed using the Gaussian smoothing method.
    window : Size of the Gaussian window. 
    sigma : Standard deviation (spread or width) of the Gaussian distribution.

    Returns
    -------
    smoothed_array : Result of the Gaussian smoothing operation.
    """
    norm_sigma = (window/10)*sigma
    print('norm sigma is ' + str(norm_sigma))
    weights = gaussian(window, sigma)
    weights = weights / np.sum(weights)
    smoothed_array = np.convolve(values, weights, 'same')
    
    return smoothed_array