#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:38:22 2024

@author: romas
"""


import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import board
import busio
import adafruit_mcp9808
##############################################################################


def cel2far(T):
   """Convert T from Celsius to Fahrenheit
   """
   return(1.8*T + 32.0)


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
        self.ax.set_ylim(-10, 120)
        self.ax.set_xlim(0, self.maxt)
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Temperature (F)')
        self.ax.title.set_text('Continuous Temperature Sensor Data')

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



    def temp(self):
    
    
        while True:
            with board.I2C() as i2c:
                sensor = adafruit_mcp9808.MCP9808(i2c)
                Tc = sensor.temperature  # float
                Tf = cel2far(Tc)
                t = time.perf_counter() - self.t0
                yield t , Tf
            

if __name__ == '__main__':
    dt = 0.01
    fig, ax = plt.subplots()
    scope = Scope(ax, maxt=10, dt=dt)
    ani = animation.FuncAnimation(fig, scope.update, scope.temp, interval=dt*1000., blit=True)

    plt.show()
