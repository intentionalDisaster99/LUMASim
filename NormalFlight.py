""" Runs a simple simulation of a balloon flight with normal parameters.

This is a very simple simulation that runs and displays a balloon flight with matplotlib using pandas.


File Details

File Name:    NormalFlight.py
Author(s):    Sam Whitlock
Status:       In progress
Notes:
    None

"""

from Config import *
from Functions import *
import Atmosphere as atm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialization
altitude = np.zeros(simulation_steps)
time = np.arange(0, simulation_length_seconds, delta_time)
velocity = 0

# Flight loop
for step in range(1, simulation_steps):



    if (get_diameter(altitude[step - 1]) < burst_diameter):
        print("up")
        velocity = get_ascent_rate(altitude[step - 1])

        if velocity == -1: 
            print("FLOATER I THINK")
            break

        altitude[step] = altitude[step - 1] + velocity * delta_time
        # print(f"Ascent rate: {velocity} m/s Altitude: {altitude[step]}")


    else:
        print("down")
        velocity = get_descent_rate(altitude[step-1], velocity)

        altitude[step] = altitude[step - 1] + velocity * delta_time

        if altitude[step] <= 0:
            print("Hit the ground")
            break






# Plotting 
plt.plot(time / 3600, altitude/1000)
plt.xlabel("Mission Time (h)")
plt.ylabel("Altitude (km)")
plt.show()



