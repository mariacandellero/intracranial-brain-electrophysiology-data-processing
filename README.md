# intracranial-brain-electrophysiology-data-processing
Written by Maria Candellero, 2023, Ghent University

# Overview
This analysis represents the different steps implemented with the aim of studying the activity of local field potentials (LFPs), spikes, and the computation of their synchrony on the basis of high-density electrophysiology recordings acquired with the ONIX system.

# Data separation into tetrodes
By running tetrode_extraction.py, the input data is separated into 16 tetrodes, adding up to a total of 64 channels.

# LFPs analysis
By running the files in lfp, local field potentials are investigated, mainly from a spectral point of view. To do so, it is necessary to run: 
- lfp_analysis.py, which contains the main script
- filter.py, a function to be used within the main script to Butterworth band-pass filter the signal
- find_highest_peak.py, a function to be used within the main script to detect the highest frequency peak, associated frequency band, and power in the power spectrum
- amplitude_spectrum_plot.py, a function to plot the amplitude spectrogram

# Spikes analysis
By running the files in spike, spikes are investigated, mainly from a spiking rate point of view. To do so, it is necessary to run: 
- spike_analysis.py, which contains the main script
- frequency_bins_extraction.py, a function to be used within the main script to extract the time bins together with the spike frequency in each
- smoothing, an optional function to be used within frequency_bins_extraction.py to select the preferred noise reduction technique
- spike_windows_extraction, a function to be used within the main script to visualize windows of data around each spike time

# LFPs and Spikes coupling
By running the files in coupling, the coherence between LFPs and spikes is computed. To do so, it is necessary to run:
- coupling analysis.py, which contains the main script
- lfp_spike_phases.py, a function to be used within the main script to extract the phase of the LFPs at the time of each spike
- polar_plot.py, a function to be used within the main script to create a polar plot to visualize the distribution of phases
