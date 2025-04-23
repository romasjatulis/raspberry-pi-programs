#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:51:30 2024

@author: romas
"""

FTIME = 1       # function range in seconds
FS = 920         # samples per second
npts = FTIME*FS  # number of sample points


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd



data = [] 
  
file = open('p5_hw7_data.txt','r') 
for voltage in file: 
    data.append(float(voltage.strip()))



t = np.linspace(0, FTIME, npts)
y = data
f1, ax1 = plt.subplots()
ax1.plot(t,y)
ax1.set_xlabel('Time(s)')
ax1.set_ylabel('Voltage(V)')
ax1.title.set_text('Plot of Voltage data for My iPhone screen dimming')
f1.show()

#subrtacted mean from voltage data to center about the axis (remove offset)
y = y - np.mean(y)

ft = np.fft.fft(y, n=16*npts)
ftnorm = abs(ft)
ps = ftnorm**2
xvals = np.fft.fftfreq(len(ps), 1.0/FS)
f2, ax2 = plt.subplots()
ax2.plot(xvals,ps)
ax2.set_xlim(1,200)
ax2.set_xlabel('Frequency(Hz)')
ax2.set_ylabel('Power')
ax2.title.set_text('PSD plot with fundamental frequency of the iPhone screen at 120Hz')
f2.show()

input("\nPress <Enter> to exit...\n")
