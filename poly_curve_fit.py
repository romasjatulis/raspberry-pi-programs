#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:29:43 2024

@author: romas
"""

import numpy as np
import random
import matplotlib.pyplot as plt

number = int(input('input number of random points less than 100: '))

x = []
y = []

for i in range(number):
    x.append(random.uniform(0,100))
    y.append(random.uniform(0,100))


xfit = np.linspace(0,100,10000)
line = np.poly1d(np.polyfit(x,y,1))
n3 = np.poly1d(np.polyfit(x,y,number-3))
n1 = np.poly1d(np.polyfit(x,y,number-1))


plt.xlim(-5,105)
plt.ylim(-5,105)
plt.scatter(x, y)
plt.plot(xfit, line(xfit) , color = 'red' , label = "1 degree")
plt.plot(xfit, n3(xfit) , color = 'orange' , label = "N-3 degree")
plt.plot(xfit, n1(xfit) , color = 'green' , label = 'N-1 degree')
plt.title("Plot for " + str(number) + " points")
plt.legend()
plt.show()
