#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:33:42 2024

@author: romas
"""


import numpy as np
import random
import matplotlib.pyplot as plt

number = int(input('input number of random points under 2000: '))

nvalue = []
errorval = []
for n in range(1,number):
    count = 0
    
    for i in range(n):
        x = random.uniform(0,2)
        y = random.uniform(0,2)
        radius = x**2 + y**2
        if radius <= 1:
            count += 1
    
    picalc = (count/n)*4**2
    error = np.abs(picalc-np.pi)/np.pi
   
    nvalue.append(n)
    errorval.append(error)


plt.plot(nvalue,errorval)
plt.title("Fractional Error in pi Calculation for increasing N value")
plt.xlabel('Number of random data points')
plt.ylabel('Fractional error')
plt.show()
