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
import pandas as pd
from netCDF4 import Dataset
import datetime
import scipy.signal as sg
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
import datetime

def moment(n, f, E):   
    if n<0:
        f = f[1:]
        E = E[1:]
    return np.trapz(E * f**n, x = f)

def highestN_stats(series, N):
    series = sorted(series, reverse=True)
    lim = int(len(series)/N)
    return(np.nanmean(series[0:lim]))

def rmsV(values):
    
    return(np.sqrt(np.sum([i**2 for i in values])/len(values)))

def assess_jonwsap(f, E):
    'Evaluate the JONSWAP-gamma parameter of the wave spectrum defined by PSD=f(f, E)'
    
    fp = f[np.argmax(E)]
    tp = 1/fp

    gammas = range(7)
    Sf = np.zeros((len(gammas) + 1, len(f) - 1))
    error = np.zeros((len(gammas) + 1, len(f) - 1))
    
    # Calculate spectral shape
    for i in gammas:
        Sf1 = (0.0624/(0.230 + 0.0336*i - 0.185 * (1.9 + i)**(-1))) * (4.004 * np.sqrt(moment(0, f, E)))**2 * tp**(-4) * f[1:]**(-5)
        Sf2 = np.exp(-1.25 * (tp * f[1:])**(-4)) * i**(np.exp((-(tp*f[1:] - 1)**2)/(2 * moment(0, f, E))))
        Sf[i, :] = Sf1 * Sf2
    
    # Evaluate errors
    for i in gammas:
        error[i, :] = Sf[i, :] - E[1:]
        error = abs(error)
        vals = np.sum(error, axis = 1)

    bf = np.argmin(vals[0:len(vals)-1]) + 1
    Ef = Sf[bf]
    
    return(bf, Ef)


def DispersionLonda(T,h):
    L1 = 1
    L2 = ((9.81*T**2)/2*np.pi)*np.tanh(h*2*np.pi/L1)
    umbral = 1
        
    while umbral>0.1:
        L2 = ((9.81*T**2)/(2*np.pi))*np.tanh((h*2*np.pi)/L1)
        umbral = np.abs(L2-L1)
        L1=L2
        
    L = L2
    k = (2*np.pi)/L
    c = np.sqrt(9.8*np.tanh(k*h)/k)
    return(L,k,c)

def upcrossing(watlev, fs):
       
        time = np.arange(0, len(watlev), 1) * fs
        watlev = watlev - np.mean(watlev)
        neg = np.where(watlev < 0)[0]

        neg1 = []
        r = []
        H = []

        for i in range(len(neg)-1):
            if neg[i+1] != neg[i] + 1:
                neg1.append(neg[i])
        
        for i in range(len(neg1)-1):
            if neg1[0] == 0: neg1[0]=1
            p = np.polyfit(time[slice(neg1[i],neg1[i]+1)], watlev[slice(neg1[i], neg1[i]+1)], 1)
            r.append(np.roots(p))
            
        r = [item for sublist in r for item in sublist]
        r = np.abs(r)
        for i in np.arange(2, len(r), 1):
            H.append(max(watlev[np.where((time < r[i]) & (time > r[i-1]))]) - min(watlev[np.where((time < r[i]) & (time > r[i-1]))]))

        T = np.diff(r)
        
        return(T, H)

def bursting(ds):
    
    burst_length = ds.burst_length.values
    samples_per_burst = ds.samples_per_burst.values
    sample = ds.sample.values
    sample_interval = ds.sample_interval.values

    # Converting seconds to datetime
    dates = []
    watlev = []
    for t in ds.time.values:

        burst_date = np.arange(np.datetime64(t), 
                     np.datetime64(t) + pd.Timedelta(np.float(samples_per_burst * sample_interval), unit='s'), 
                     datetime.timedelta(seconds=np.float(sample_interval)))
        
        surf = ds.sel(time=t).P_1.values

        watlev.append(surf)
        dates.append(burst_date)


    H, T = [], []
    for row in range(np.shape(dates)[0]):
        
        series = np.array(watlev[row])
        
        series[np.isnan(series)] = 0
        
        # Estimate power spectral density using Welch’s method.        
        f, E = sg.welch(series, fs = 1/sample_interval)   
        m0 = np.trapz(E, x=f)
        m2 = np.trapz(E*f**2, x=f)
        
        Hs = 4 * np.sqrt(m0)
        Tm = np.sqrt(m0/m2)
    
        H.append(Hs)
        T.append(Tm)
        
    return(ds.time.values, H, T)


