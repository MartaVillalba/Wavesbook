#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def energy_spectrum(hs, tp, gamma, duration):
    '''
    spec: Dataset with vars for the whole partitions
    S(f,dir) = S(f) * D(dir)
    S(f) ----- D(dir)
    Meshgrid de x freqs - dir - z energy
    '''

    # Defining frequency series - tend length
    freqs = np.linspace(0.02, 1, duration)

    S = []
    fp = 1/tp

    for f in freqs:
        if f <= fp:
            sigma = 0.07
        if f > fp:
            sigma = 0.09

        Beta = (0.06238/(0.23+0.0336*gamma-0.185*(1.9+gamma)**-1))*(1.094-0.01915*np.log(gamma))
        Sf = Beta * (hs**2) * (tp**-4) * (f**-5)*np.exp(-1.25*(tp*f)**-4)*gamma**(np.exp((-(tp*f-1)**2)/(2*sigma**2)))
        S.append(Sf)

    return (S, freqs)

def series_Jonswap(H, T, duration, deltat, gamma):
    '''
    Generate surface elevation from PSD df = 1/tendc

    waves - dictionary
              T       - Period (s)
              H       - Height (m)
              gamma   - Jonswap spectrum  peak parammeter
              deltat  - delta time (s)
              tendc   - simulation period (s)

    returns 2D numpy array with series time and elevation
    '''

    # series duration
    time = np.arange(0, duration, deltat)

    # series frequency
    freqs = np.linspace(0.02, 1, duration)
    delta_f = freqs[1] - freqs[0]

    # calculate energy spectrum
    S, freq = energy_spectrum(H, T, gamma, duration)

    # series elevation
    teta = np.zeros((len(time)))

    # calculate aij
    for f in range(len(freqs)):
        ai = np.sqrt(S[f] * 2 * delta_f)
        eps = np.random.rand() * (2*np.pi)

        # calculate elevation
        teta = teta + ai * np.cos(2*np.pi*freqs[f] * time + eps)

    # generate series dataframe
    series = np.zeros((len(time), 2))
    series[:, 0] = time
    series[:, 1] = teta

    return series, S, freq

def series_regular_monochromatic(H, T, duration, deltat):
    '''
    Generates monochromatic regular waves series

    waves - dictionary
              T      - Period (s)
              H      - Height (m)
              WL     - Water level (m)
              warmup - spin up time (s)
              deltat - delta time (s)
              tendc  - simulation period (s)

    returns 2D numpy array with series time and elevation
    '''

    # series duration
    time = np.arange(0, duration, deltat)

    # series elevation
    teta = (H/2) * np.cos((2*np.pi/T)*time)

    # generate series dataframe
    series = np.zeros((len(time), 2))
    series[:, 0] = time
    series[:, 1] = teta

    return series

def series_regular_bichromatic(H, T, duration, deltat, T2):
    '''
    Generates bichromatic regular waves series

    waves - dictionary
              T1     - Period component 1 (s)
              T2     - Period component 2 (s)
              H      - Height (m)
              WL     - Water level (m)
              warmup - spin up time (s)
              deltat - delta time (s)
              tendc  - simulation period (s)
    '''

    # series duration
    time = np.arange(0, duration, deltat)

    # series elevation
    teta = (H/2) * np.cos((2*np.pi/T)*time) + (H/2) * np.cos((2*np.pi/T2)*time)

    # generate series dataframe
    series = np.zeros((len(time), 2))
    series[:,0] = time
    series[:,1] = teta

    return series

def waves_dispersion(T, h):
    'Solve the wave dispersion relation'

    L1 = 1
    L2 = ((9.81*T**2)/2*np.pi) * np.tanh(h*2*np.pi/L1)
    umbral = 1

    while umbral > 0.1:
        L2 = ((9.81*T**2)/(2*np.pi)) * np.tanh((h*2*np.pi)/L1)
        umbral = np.abs(L2-L1)
        L1 = L2

    L = L2
    k = (2*np.pi)/L
    c = np.sqrt(9.8*np.tanh(k*h)/k)

    return(L, k, c)

def plot_waves(wave, H, T, duration, deltat, T2=None, gamma=None):
    '''
    Plot wave series

    waves:   waves parameters
    series:  waves series
    '''
    
    # plot series, group envelope
    fig = plt.figure(figsize=(17,3), constrained_layout=True)
    spec = gridspec.GridSpec(ncols=6, nrows=1, figure=fig)
    
    ax1 = fig.add_subplot(spec[0,5])
    # make waves series dataset
    if wave == 'monochromatic':
        series = series_regular_monochromatic(H, T, duration, deltat)
        ax1.vlines([1/T], 0, [0.5*(H/2)**2], color='b', linewidth=1)
        ax1.scatter([1/T], [0.5*(H/2)**2], c='b', s=12)
        ax1.set_ylabel('$S(f)$ $(m^{2})$')
        
    elif wave == 'bichromatic':
        series = series_regular_bichromatic(H, T, duration, deltat, T2)
        ax1.vlines([1/T, 1/T2], [0,0], [0.5*(H/2)**2, 0.5*(H/2)**2], color='b',  linewidth=1)
        ax1.scatter([1/T, 1/T2], [0.5*(H/2)**2, 0.5*(H/2)**2], c='b', s=12)
        ax1.set_ylabel('$S(f)$ $(m^{2})$')
        
    else:
        series, S, f = series_Jonswap(H, T, duration, deltat, gamma)
        ax1.plot(f, S, c='b')
        ax1.set_ylabel('$S(f)$ $(m^{2}/Hz)$')
        
    ax1.set_xlabel('$f$ (Hz)')
    ax1.set_xlim([0,1])
    
    
    # waves series 
    time = series[:,0]
    elevation = series[:,1]
    envelope = np.abs(hilbert(elevation))  # hilbert transformation
    
    ax = fig.add_subplot(spec[0, 0:5])
    ax.plot(time, elevation, c='k')
    ax.fill_between(
        time, -envelope, envelope,
        facecolor = 'dodgerblue',
        alpha = 0.3,
        label = 'Group envelope',
    )
    ax.plot(time, envelope, '--', c='k')
    ax.plot(time, -envelope, '--', c='k')
    ax.set_xlim(0, time[-1])
    ax.set_xlabel('$Time$ $(s)$')
    ax.set_ylabel('$Elevation$ $(m)$')
    ax.legend(loc = 'lower right')
    
    plt.close()
    
    return(fig)
    