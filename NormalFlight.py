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
import matplotlib as plt

# Initialization
altitude = pd.zeros(simulation_steps)
time = np.arange(0, simulation_length_seconds, delta_time)







# Plotting 
plt.plot(time * 3600, altitude)
plt.xlabel("Mission Time (h)")
plt.ylabel("Altitude (m)")




