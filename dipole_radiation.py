#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 17:16:45 2024

@author: romas
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



#List of Constants used to calculate the fields and poynting vecor:

 # Permeability of free space   
mu0 = 4 * np.pi * 1e-7 
 # Speed of light
c = 3e8 
# Frequency
frequency = 10e8  
# Wavelengt
wavelength = c / frequency
# Wave number
k = 2 * np.pi / wavelength  
# Dipole moment
p = 10e-5
#Period
period = 1 / frequency

#starts program with no figure
fig = None

#First plot is a surface plot of the poynging vector
#I tried many different plots to display the vector field, this is a hard one to show since the field goes out everywhere
#arrows and a quiver plot of the vector did not look too good
#I noticed when doing research radiation is often dispayled by intensity and countours
#this is much more visually pleasing and easier to extract meaning from

#This plot is known as the intensity profile of the dipole and it shows how the radiation expands from the origin
#It is plotted for a constant radius because in 3 dimensions the plot gets messy and it is difficult to see
#direction and magnitude of radiation
#the next animated plots address these two values much more clearly

#When characterizing antenne and radiation, the intensity is often the value of interest
#Intensity is found from the magnitude of the poynting vector
#The poynting vector is the cross product of the E and B fields and radiates outward as shown by the surface

#This approach uses the far field approximation for an electric dipole taken from Griffiths chapter 11
#In real world and engineering applications the far field is important

def surface():
    global fig
    # Spherical coordinates
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Calculating the Poynting vector's magnitude in spherical coordinates
    r = 5* wavelength 
    S_magnitude = (mu0 * p**2 * (2*np.pi*frequency)**4) / (32 * np.pi**2 * c**2 * r**2) * np.sin(theta)**2
    
    # Converting spherical coordinates to Cartesian coordinates for the plot
    # The radial distance is modulated by the Poynting vector's magnitude for visualization
    X = S_magnitude * np.sin(theta) * np.cos(phi)
    Y = S_magnitude * np.sin(theta) * np.sin(phi)
    Z = S_magnitude * np.cos(theta)
    
    # Set up the figure and subplots
    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    ax.plot_surface(X, Y, Z, color = 'red', alpha=0.6, linewidth=0)
    
    #this is a kind of general view to see the shape of the radiation in 3d
    #It didn't make sense to show actual distances since we put r constant and
    #the full solution would have many of these shapes for different r, but visually wouldnt tell us much more information
    
    plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Intensity Profile for a Radiating Diple Pointing in the Z-axis (Poyting Vector Surface plot)')
    plt.show()





#Here I am setting the axes for the poynting vector contour plots
#The region of interest here is within 5 wavelengths
#The r depencence of the poynting vector means that it dies out very fast
#This region is close enough to be interesting and also gives a good idea of were the radiation is going
x = np.linspace(-5 * wavelength, 5 * wavelength, 300)
y = np.linspace(-5 * wavelength, 5 * wavelength, 300)
z = np.linspace(-5 * wavelength, 5 * wavelength, 300)

X_xz, Z_xz = np.meshgrid(x, z)

X_xy, Y_xy = np.meshgrid(x, y)

# Function to calculate Poynting vector magnitude for the xz plane
def S_xz(t):
    #radius
    r = np.sqrt(X_xz**2 + Z_xz**2)
    #theta
    theta = np.arctan2(X_xz, Z_xz)
    #this is what creates the time depencence of the field which depends on the frquency of oscillation and position
    phi = k * r - 2*np.pi*frequency * t
    
    #we cannot divide by zero so we must set a bottom limit for r
    #We are more interested in the far field so it is fine to cut out a bit in the middle anyway
    r[r < wavelength / 2] = wavelength / 2

    #radial component of the Poynting Vector
    Sr = (c * p**2 * k**4 / (8 * np.pi * r**2)) * (np.sin(theta))**2 * (1 + ((1 - (2 / ((k * r)**2))) * np.cos(2 * phi)) - ((2 / (k * r)) - (1 / (k * r))**3) * np.sin(2 * phi))
    #theta component of hte Poynting vector
    S_theta = (c * p**2 * k**3 / (4 * np.pi * r**3)) * np.sin(theta) * np.cos(theta) * ((1 - (1 / (k * r))**2) * np.sin(2 * phi) + (2 / k * r) * np.cos(2 * phi))
    #magnitude is the combination of both
    #This parameter is interesting to adjsut becuase it determines how fast the field dies off
    #instead of taking the square root, this is to the power of 1/5 to see more of the field 
    S_mag_xz = (Sr**2 + S_theta**2)**(1/5)
   
    return S_mag_xz


# I made a separate function to calculate the poytning vector in the xy plane
# Theta is zero in the xy plane so the theta component goes away and the radial component is simplified
# Having this separate equation allows for less calculations and better performace
def S_xy(t):

    # Radius in the xy-plane
    r = np.sqrt(X_xy**2 + Y_xy**2)  
    phi = k * r - 2 * np.pi * frequency * t
    #again, we cannot divide by zero
    r[r < wavelength / 2] = wavelength / 2
    Sr = (c * p**2 * k**4 / (8 * np.pi * r**2)) *  (1 + ((1 - (2 / ((k * r)**2))) * np.cos(2 * phi)) - ((2 / (k * r)) - (1 / (k * r))**3) * np.sin(2 * phi))
    
    S_mag_xy = Sr**(2/5)
    
    
    #I included this to take care of the non values that would occur so that I could still keep the full equation and range that I wanted to see
    S_mag_xy = np.nan_to_num(S_mag_xy, nan=0.0)

    return S_mag_xy



#This is the fuction tha creates the countour plots of the poytning vector in the xy and xz planes
def S_animate(plane):
    #global variable which allows communication with the other function that is responsible for animating
    global contour
    #the fig variable is jsut there to let the program know if a plot is open
    #if a plot is open, it needs to close it before showing the next one
    global fig
    
    #initial contour at t = 0
    t = 0
    
    #This sets the number of levels that are shown on the contour
    #setting the levels high smooths out the contour and looks like a gradient
    #setting the levels too high also slowed down the program alot, especially on the raspberry pi
    levels = 20
    
    fig, ax = plt.subplots(figsize=(10, 8))
    #this sets up the plot for the desired plane of view
    
    if plane == 'xy':
        Ax1 = X_xy
        Ax2 = Y_xy
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title('Radiation from a Dipole along the Z-axis (Poynting Vector Magnitude)')
        S_mag = S_xy(t)
    else:
        Ax1 = X_xz
        Ax2 = Z_xz
        ax.set_xlabel('x (m)')
        ax.set_ylabel('z (m)')
        ax.set_title('Radiation from a Dipole along the Z-axis (Poynting Vector Magnitude)')
        S_mag = S_xz(t)
        
        
    #this calculates the initial contour and sets the colorbar
    #this is out of the update function becuase I do not want it reset every time    
    contour = ax.contourf(Ax1, Ax2, S_mag, levels = levels, cmap='inferno' )
    fig.colorbar(contour, ax=ax, label='Magnitude of Poynting Vector')

    #this is responsible for the animation
    #it removes the previous contour
    def update(frame):
        global contour
        #the for loop removes th previous contours
        for c in contour.collections:
            c.remove()  # Remove old contours
            
        #calculates the poynting vector magnitude in terms of the frame given by the update function
        if plane == 'xy':
            S_mag = S_xy(frame)
        else:
            S_mag = S_xz(frame)
        #finds countours plots
        contour = ax.contourf(Ax1,Ax2, S_mag,levels = levels, cmap='inferno' )
    #animates
    #the frames go from zero to one period and then repeat so that the animation is continuous
    #The loop runs for half a second
    #doing a real time animation would be hard to see becuase the period is tiny for RF
    figure = FuncAnimation(fig, update, frames=np.linspace(0, period, 50), interval=10, repeat=True)
    
    plt.show()
    

#This lets you switch between the plots
def plots():
    print("Select View:")
    print("1 - 3D Intensity Profile")
    print("2 - XZ Radiation Animation")
    print("3 - XY Radiation Animation")
    print("4 - Exit")
    choice = input("Enter your choice: ")
    return choice



while True:
    user_choice = plots()
    if fig is not None:
        plt.close(fig)
    if user_choice == '1':
        surface()
    elif user_choice == '2':
        S_animate('xy')
    elif user_choice == '3':
        S_animate('xz')
    elif user_choice == '4':
        plt.close()
        break
    else:
        print("Invalid choice. Please try again.")


