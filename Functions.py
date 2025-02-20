""" Supplies many of the functions to the main flight simulation files.

Supplies many functions to the main flight files. Cannot be run standalone.


File Details

File Name:    Function.py
Author(s):    Sam Whitlock
Status:       In progress
Notes:
    None

"""

import numpy as np
import Atmosphere as atm
from Config import *

def get_ascent_rate(diameter, altitude): 
    """ Finds the ascent rate based on the current altitude of the balloon.

    Args:
        altitude (float): The altitude the balloon is at.

    Returns:
        float: The ascent rate of the balloon (m/s)
    """


    # TODO This is only at STP, so we can change it later for more accuracy
    balloon_air_density = 0.178 # grams per liter


    numerator = np.pi * diameter ** 3 * (balloon_air_density - atm.getAirDensity(altitude)) * get_g(altitude) / 6
    numerator = numerator - (total_mass) * get_g(altitude)

    denominator = balloon_drag_coefficient * balloon_air_density * np.pi * diameter**2/8

    return np.sqrt(numerator/denominator)



def get_g(altitude):
    """ Returns the acceleration due to gravity based on altitude

    Args:
        altitude (float): The altitude at which the g is to be found
    
    Returns:
        float: The acceleration due to gravity at altitude
    """

    # I'm assuming that the mass of Earth isn't going to change
    mass_of_earth = 5.972 * 10**24
    gravitational_constant = 6.6743 * 10 ** 11
    radius_of_earth = 66378137

    return (gravitational_constant * mass_of_earth) / (altitude + radius_of_earth)

def get_diameter(altitude):

    pass









