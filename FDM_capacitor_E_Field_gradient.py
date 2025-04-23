#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:09:31 2024

@author: romas
"""
import numpy as np
import matplotlib.pyplot as plt

#grid dimension
gdim = 100

#plate separation
fracsep = 0.6
sep = fracsep*gdim

#plate width
fracwidth = 0.2
width = fracwidth*gdim

#plate thickness
fracthick = 0.01
thick = fracthick*gdim

#potential
V = 1

#maximum iteration
maxit = 1000



initialgrid = np.zeros((gdim,gdim), dtype='uint')

def setbound(grid):
    
    #Top plate
    grid[int(gdim/2 - width/2):int(gdim/2 + width/2),int(gdim/2 + sep/2 - thick/2):int(gdim/2 + sep/2 + thick/2)] = V
    
    #bottom plate
    grid[int(gdim/2 - width/2):int(gdim/2 + width/2),int(gdim/2 - sep/2 - thick/2):int(gdim/2 - sep/2 + thick/2)] = -V
    
    #border
    grid[0,0:gdim-1] = 0
    grid[gdim-1,0:gdim] = 0
    grid[0:gdim-1,0] = 0
    grid[0:gdim-1,gdim-1] = 0
    return grid

def average(grid):
    new_grid = 0.25*(np.roll(grid,-1,axis=0) + np.roll(grid,1,axis=0) + np.roll(grid,-1,axis=1) + np.roll(grid,1,axis = 1))
    return new_grid


a = initialgrid
for i in range(maxit):
    sum1 = np.sum(np.abs(a))
    av = average(a)
    b = setbound(av)
    sum2 = np.sum(np.abs(b))
    print(np.abs(sum1-sum2))
    a = b


plotarr = np.flipud(a.transpose())
f1, ax1 = plt.subplots()

picture = ax1.imshow(plotarr, interpolation='none', cmap='jet')

#
# turn off axis labels
#
ax1.axis('off')
#ax1.set_title('Grid = '  + str(gdim) + ', ' + 'Thickness = '  + str(thick) + ', ' +'Gap = '  + str(sep) + ', ' + 'Width = '  + str(width) + ', ' 'V = '  + str(V) + ', ' + 'Iterations = '  + str(maxit))
print('Grid = '  + str(gdim) + ', ' + 'Thickness = '  + str(thick) + ', ' +'Gap = '  + str(sep) + ', ' + 'Width = '  + str(width) + ', ' 'V = '  + str(V) + ', ' + 'Iterations = '  + str(maxit))
#
# draw figure
#
f1.show()


