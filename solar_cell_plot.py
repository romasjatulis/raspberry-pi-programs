#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:21:31 2024

@author: romas
"""

ACQTIME = 1.0  # seconds of data acquisition

#    samples per second
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
SPS = 920

#    full-scale range in mV
#    options: 16:256, 8:512, 4:1024, 2:2048, 1:4096, 2/3:6144.
VGAIN = 1

nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
###############################################################################

print()
print('Initializing ADC...')
print()

i2c = busio.I2C(board.SCL, board.SDA)

#
# ADS1015 parameters with defaults
#    preamp gain: 1.0
#       options: 2/3, 1, 2, 4, 8, 16
#          corresponding full-scale ranges (mV)
#                +/- 6144, 4096, 2048, 1024, 512, 256
#                Note: input must not exceed VDD + 0.3
#    data_rate (samples per second): 1600
#       options: 128, 250, 490, 920, 1600, 2400, 3300.
#    mode: ADS.Mode.Single
#       options: ADS.Mode.Single, ADS.Mode.CONTINUOUS
#    address: 0x48
#
adc = ADS.ADS1015(i2c, gain=VGAIN, data_rate=SPS, mode=ADS.Mode.CONTINUOUS)

# Second and third arguments are the ADC channel pins
channel = AnalogIn(adc, ADS.P2, ADS.P3)

indata = np.zeros(nsamples,'float')
vin = AnalogIn(adc, 2, 3)

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()

for i in range(nsamples):
   st = time.perf_counter()
   indata[i] = vin.voltage
   while (time.perf_counter() - st) <= sinterval:
      pass

t = time.perf_counter() - t0

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t)
print()
###############################################################################

f1, ax1 = plt.subplots()

#
# Default plotting style connects points with lines
#
ax1.plot(xpoints, indata)
ax1.set_xlabel('Time(s)')
ax1.set_ylabel('Voltage(V)')
ax1.title.set_text('Solar Cell Voltage Data')

#
# Plotting with steps is better for visualizing sampling
#
# ax1.plot(xpoints, indata,'-',drawstyle='steps-post')

f1.show()

input("\nPress <Enter> to exit...\n")




file = open("p5_hw7_data.txt", "w")
strdat = ["%.4f" % x for x in indata]
tempdata = "\n".join(strdat)
file.write(tempdata)
