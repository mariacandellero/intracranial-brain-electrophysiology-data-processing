# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:03:12 2023

@author: Maria
"""

import numpy as np
import matplotlib.pyplot as plt


def polar_plot(phases: np.ndarray) -> plt.Figure:
    """
    Creation of a polar plot to visualize the distribution of phases.

    Parameters
    ----------
    phases : Phases to be visualized in the polar plot.

    Returns
    -------
    fig : Figure containing the polar plot.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    plt.rcParams["font.weight"] = "bold"

    phase_diff = (phases - np.pi) % (2*np.pi) - np.pi
    bins = np.linspace(-np.pi, np.pi, 21)
    counts, _ = np.histogram(phase_diff, bins=bins)
    widths = np.diff(bins)
    centers = (bins[:-1] + bins[1:]) / 2

    # Calculation of corresponding bin radius
    area = counts / phase_diff.size
    radius = (area / np.pi)**.5

    # Creation of polar plot
    bars = ax.bar(centers, radius, width=widths, bottom=0.0, edgecolor='black', linewidth=1.5)
    label = ['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$',
             r'$\pi$', r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$']
    ax.set_xticklabels(label, fontweight='bold')
    ax.set_yticks([])
    ax.set_title('Phases distribution', fontsize=20, fontweight='bold')

    return fig