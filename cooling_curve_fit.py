#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 14:05:24 2024

@author: romas
"""


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

data = np.loadtxt("p6_hw7_data.txt")

#exponential funtion to fit to
def exponential(t, tau, amplitude, const):
    return amplitude * np.exp(-t/tau) + const


x_data = np.linspace(0,120,120*4)
y_data = data

#fitting with scipy
try:
    params, covariance = curve_fit(exponential, x_data, y_data, maxfev=50)
except RuntimeError as e:
    print("Error:", e)
    exit()


tau, amplitude, const = params


x_fit = np.linspace(min(x_data), max(x_data), 1000)
y_fit = exponential(x_fit, tau, amplitude, const)

print('amplitude: ' + str(amplitude))
print('time constant: ' + str(tau))
print('offset: ' + str(const)) 


plt.scatter(x_data, y_data, s = 4 , label='Data')
plt.plot(x_fit, y_fit, color='red', label='Fitted curve')
plt.legend()
plt.xlabel('Time(s)')
plt.ylabel('Temp(F)')
plt.title('Exponential Fitting with time constant:' + str(tau))
plt.show()



