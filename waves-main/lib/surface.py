#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 13:11:46 2020

"""

import os.path as op
import sys
sys.path.insert(0, op.join(op.dirname(__file__), '..'))

import numpy as np
import xarray as xr 
import matplotlib.pyplot as plt

# maths
from math import gamma as gmfunc

# these are the default partitions
default_partitions = {
    'sea': (1.2, 10, None, 70, 20, None), # hs, tp, dir, spr, gamma
    'swell1': (3.2, 16, None, 300, 10, None),
    'swell2': (0.8, 14, None, 180, 12, None)
    # 'swell3': [...] ; add extra partitions as required...
}

def calculate_spectrum(freqs_recon, dirs_recon, partitions: dict = default_partitions):
    
    """
    This function calculates a "syntetic" spectrum given the partitions...
    The number of partitions that can be given to the funtion is NOT limited,
    but the example contains just one sea and two swells

    Args:
        partitions (python-dict): These are the partitions, containing hs, tp,
            tm02, dir, spr and gamma, where tm02 and gamma ara optional

    Returns:
        [xr.Dataset]: The function returns an xarray Dataset with variable name
            "efth" and the energy calculated for each frequency and direction
            available in spectra_examples.nc, which is saved in the parent folder
            
    """

    # and iterate for all the partitions
    for partition in partitions.keys():
        
        # extract hs, tp, dir, spr and gamma
        hs, tp, dirr, spr, gamma = partitions[partition] # this is a tuple
        #if not gamma:
        #    gamma = 3.3 if not tm02 else np.exp((np.log(tp/(1.411*tm02)))/-0.07972)
        
        # calculate sigma value
        sigma = np.where(
            freqs_recon<(1/tp),
            np.ones(len(freqs_recon))*0.07,
            np.ones(len(freqs_recon))*0.09
        ) 
        
        # calculate alpha parameter
        alpha = (0.06238 / (0.23+0.0336*gamma-0.185*(1.9+gamma)**(-1))) * \
            (1.094-0.01915*np.log(gamma))

        # energy in frequencies
        S = alpha * (hs**2) * (tp**(-4)) * (freqs_recon**(-5)) * \
            np.exp(-1.25*(tp*freqs_recon)**(-4)) * \
            gamma**(np.exp((-(tp*freqs_recon-1)**2)/(2*sigma**2)))
        
        # energy in directions
        s = (2/(spr*np.pi/180)**2) - 1 # spectral shape parameter
        D = ((2**(2*s-1))/np.pi)*(gmfunc(s+1)**2/gmfunc(2*s+1)) * \
            np.abs(np.cos(
                (np.deg2rad(dirs_recon)-np.deg2rad(dirr))/2
            ))**(2*s)
        
        # total spectrum
        if partition=='sea':
            spectrum = S * D * (np.pi/180)
        else:
            spectrum += S * D * (np.pi/180)
            
    return spectrum.to_dataset(name='efth')

def calculate_surface(freqs_recon, dirs_recon, spectrum,
    x_y_dist: int = 1000, x_y_nodes: int = 200, 
    time: tuple = (1,1)):
    
    """
    This function calculates the free surface elevation given the spectrum...
    By default, one previously loaded spectrum is plotted, but a "syntetic"
    spectrum can be passed and will be plotted too. More than one time can be also
    plotted to see the waves moving...

    Args:
        spectrum (xr.Dataset): This is the spectrum in an xarray Dataset with
            variable name "efth"
        x_y_dist (int): Distance in meters to be covered by the surface in the 
            x and y axis. Defaults to 1000.
        x_y_nodes (int): Number of pixels in x and y axis.
        time (tuple): This is the time frames, been the first item the total number
            of seconds to cover, and the second one the time step
        
        *** Be careful when adding large number of nodes, as the computation might
            take several time, or even not compute the matrices multiplications...

    Returns:
        [xr.Dataset]: The function returns an xarray Dataset with the elevation
            in meters, and coordinates the x and y values, but also the time if
            it is passed in time parameter
            
    """

    # we first calculate the deltas in freqs and dirs
    delta_freq = (
        (max(freqs_recon)-min(freqs_recon))/len(freqs_recon)
    ).values # difference in the frequencies
    delta_dir = (360.0/len(dirs_recon)) * np.pi/180
    
    # we now construct the real x and y spaces (xr.DataArrays)
    x = xr.Dataset(
        {'x_space': (('x'), np.linspace(
            1000,1000+x_y_dist,x_y_nodes
        ))}, coords = {'x': np.arange(x_y_nodes)}
    ).x_space
    y = xr.Dataset(
        {'y_space': (('y'), np.linspace(
            1000,1000+x_y_dist,x_y_nodes
        ))}, coords = {'y': np.arange(x_y_nodes)}
    ).y_space
    
    # and now create the w, k and th (theta) xr.DataArrays
    w = 2 * np.pi * freqs_recon
    k = w**2 / 9.806
    th = xr.Dataset(
        {'math_dir': (('dir'), dirs_recon.values)#trans_geosdeg2mathdeg(dirs_recon,correct=True) # +180
        }, coords={'dir': dirs_recon}
    ).math_dir * np.pi/180 # math-understandable directions
    
    # then we calculate the amplitudes
    amplitude = np.sqrt(
        spectrum.efth * 2 * delta_dir * delta_freq
    )
    
    # and add the random phase term
    spectrum = spectrum.assign(
        {'alpha':(('freq','dir'),np.random.rand(*amplitude.shape)*2*np.pi-np.pi)}
    )
    
    # create the time-surface
    if time[0]==1:
        return (amplitude*np.cos(
            w*1-k*x*np.cos(th)-k*y*np.sin(th)-spectrum.alpha
        )).sum(dim='freq').sum(dim='dir')
    else:
        surfaces = []
        for t in progressbar.progressbar(np.arange(1,time[0],time[1])):
            surfaces.append(
                (amplitude*np.cos(
                    w*t-k*x*np.cos(th)-k*y*np.sin(th)-spectrum.alpha)
                ).sum(dim='freq').sum(dim='dir').expand_dims(
                    {'surface_time':[t]} # append time to concat
                )
            )
        return xr.concat(surfaces,dim='surface_time')

