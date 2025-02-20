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

def get_ascent_rate(altitude): 
    """ Finds the ascent rate based on the current altitude of the balloon.

    Args:
        altitude (float): The altitude the balloon is at. (m)

    Returns:
        float: The ascent rate of the balloon (m/s)
    """


    # TODO This is only at STP, so we can change it later for more accuracy
    balloon_air_density = 0.178 # grams per liter

    # This is from one paper
    # numerator = np.pi * get_diameter(altitude) ** 3 * (balloon_air_density - atm.getAirDensity(altitude)) * get_g(altitude) / 6
    # numerator = numerator - (total_mass) * get_g(altitude)

    # denominator = balloon_drag_coefficient * balloon_air_density * np.pi * get_diameter(altitude)**2/8

    # This is from another paper
    numerator = 4 * get_diameter(altitude) * (balloon_air_density - atm.getAirDensity(altitude)) * get_g(altitude)
    denominator = 3 * balloon_drag_coefficient * atm.getAirDensity(altitude)

    return np.sqrt(numerator/denominator)



def get_g(altitude):
    """ Returns the acceleration due to gravity based on altitude

    Args:
        altitude (float): The altitude at which the g is to be found (m)
    
    Returns:
        float: The acceleration due to gravity at altitude
    """

    # I'm assuming that the mass of Earth isn't going to change
    mass_of_earth = 5.972 * 10**24
    gravitational_constant = 6.6743 * 10 ** 11
    radius_of_earth = 66378137

    return (gravitational_constant * mass_of_earth) / (altitude + radius_of_earth)

# ! This does not work right now, the problem is in what I said in the Notes for Config.py
# ! I think the problem is garbage in garbage out, so update the other bit first
def get_diameter(altitude):
    """ Returns the diameter of the balloon based on the altitude
    
    Uses the functions from Atmosphere.py to calculate the diameter of the ballon.
    This includes functions like pressure and temperature

    Args:
        altitude (float): The altitude to do the calculations for. (m)

    Returns:
        float: The diameter of the balloon. (m)

    """

    # Finding the volume (Can be updated; this assumes constant temperature)
    volume = initial_volume * launch_pressure / atm.getAirPressure(altitude)

    print(f"The volume is {volume} m^3 at {altitude} meters")

    # Finding diameter from volume
    return 2 * np.power(3 * volume/4/np.pi, 1/3)










