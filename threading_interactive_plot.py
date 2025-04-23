#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:18:33 2024

@author: romas
"""

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading
import sys

n = 0
def userin(threadnum):
    while True:
       instr = input("Please enter an integer: ")
       try:
          global n
          n = int(instr)
       except ValueError:
          print("Your input was not an integer.  Try again.\n", file=sys.stderr)
       else:
           break
     

class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = np.array([])
        self.ydata = np.array([])
        self.t0 = time.perf_counter()
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-50,50)
        self.ax.set_xlim(0, self.maxt)
        self.ax.title.set_text('enter an integer between -50 and 50')


    def update(self, data):
        t,y = data
        self.tdata = np.append(self.tdata, t)
        self.ydata = np.append(self.ydata, y)
        self.ydata = self.ydata[self.tdata > (t-self.maxt)]
        self.tdata = self.tdata[self.tdata > (t-self.maxt)]
        self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        self.ax.figure.canvas.draw()
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

    def func(self):
        while True:
            t = time.perf_counter() - self.t0
            y = n
            yield t , y



for j in range(3):
   thr = threading.Thread(target = userin, args = (j,))
   thr.start()
   
   
   
if __name__ == '__main__':
    dt = 0.01
    fig, ax = plt.subplots()
    scope = Scope(ax, maxt=10, dt=dt)
    ani = animation.FuncAnimation(fig, scope.update, scope.func, interval=dt*1000., blit=True)

    plt.show()
   