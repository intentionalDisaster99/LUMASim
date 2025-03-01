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

# Deprecated and doesn't work
def old_et_ascent_rate(altitude): 
    """ Finds the ascent rate based on the current altitude of the balloon.

    Args:
        altitude (float): The altitude the balloon is at. (m)

    Returns:
        float: The ascent rate of the balloon (m/s)
    """

    # TODO This is only at STP, so we can change it later for more accuracy
    balloon_air_density = balloon_gas_mass / initial_gas_volume /1000 #0.1786 # kg per m^3

    # This is from one paper
    # numerator = np.pi * (get_diameter(altitude) ** 3) * (balloon_air_density - atm.getAirDensity(altitude)) * get_g(altitude) / 6
    # numerator = numerator - (total_mass / 1000) * get_g(altitude)

    # denominator = balloon_drag_coefficient * balloon_air_density * np.pi * get_diameter(altitude)**2 /8

    # This is from another paper
    numerator = 4 * get_diameter(altitude) * (balloon_air_density - atm.getAirDensity(altitude)) * get_g(altitude)
    denominator = 3 * balloon_drag_coefficient * atm.getAirDensity(altitude)

    # print(f"Ascent Rate: {np.sqrt(numerator/denominator)} m/s Altitude: {altitude} m Diameter: {get_diameter(altitude)} m g: {get_g(altitude)} kg Air Density: {atm.getAirDensity(altitude)} km/m^3 Drag Coefficient: {balloon_drag_coefficient} Gas Density: {balloon_air_density} kg/m^3")

    # Checking for a negative
    if (numerator/denominator) <= 0:
        return -1

    return np.sqrt(numerator/denominator)

def get_ascent_rate(altitude):
    """ Finds the ascent rate based on the current altitude of the balloon.

    Args:
        altitude (float): The altitude the balloon is at. (m)

    Returns:
        float: The ascent rate of the balloon (m/s)
    """

    return np.sqrt(get_free_lift(altitude) * 2/(balloon_drag_coefficient * np.pi * (get_diameter(altitude)/2) ** 2 * atm.getAirDensity(altitude)))

def get_gross_lift(altitude):
    """ Calculates the gross lift for the balloon.

    NOTE: This is the total amount that the gas in the balloon can lift.

    Args:
        altitude (float): The altitude to calculate for. (m)
    Returns:
        float: The gross lift (N)
    """
    return initial_gas_volume * (atm.getAirDensity(altitude) - get_internal_density(altitude))
    print(f"Calculated gross lift was: {initial_gas_volume * (atm.getAirDensity(altitude)) * get_g(altitude)}")
    print(f"g: {get_g(altitude)}")
    return initial_gas_volume * (atm.getAirDensity(altitude)) * get_g(altitude) - balloon_mass / 1000

#! Might be an issue point here, math isn't mathing
def get_neck_lift(altitude):
    """ Calculates the neck lift for the balloon at any altitude.

    NOTE: This is the lifting force of the balloon alone, so the upwards buoyancy force minus the force of gravity

    Args:
        altitude (float): The altitude to calculate for (m).
    Returns:
        float: The neck lift (N)
    """
    return get_gross_lift(altitude) - (balloon_mass / 1000)

def get_free_lift(altitude):
    """ Calculates the free lift for the balloon at any altitude.

    NOTE: This is the left over lift that is actually used to go up. It accounts for the mass of the balloon and payload.

    Args:
        altitude (float): The altitude to calculate for (m).
    Returns:
        float: The free lift (N)
    """
    return get_gross_lift(altitude) - (total_mass/1000) * (-get_g(altitude))

def get_internal_density(altitude):
    """ Calculates the density of the gas inside the balloon at a certain altitude.

    Args:
        altitude (float): The altitude to calculate for (m)
    Returns:
        float: The internal density (kg/m^3)
    """
    return (balloon_gas_mass / 1000)/get_volume(altitude)


def get_g(altitude):
    """ Returns the magnitude of the acceleration due to gravity based on altitude

    Args:
        altitude (float): The altitude at which the g is to be found (m)
    
    Returns:
        float: The acceleration due to gravity at altitude (m/ss)
    """

    # I'm assuming that the mass of Earth isn't going to change
    mass_of_earth = 5.9736  * 10**24
    gravitational_constant = 6.6743 * 10 ** -11
    radius_of_earth = 6.378137 * 10 ** 6

    return (gravitational_constant * mass_of_earth) / (altitude + radius_of_earth) ** 2

# TODO Adjust this to use the get_volume function
def get_diameter(altitude):
    """ Returns the diameter of the balloon based on the altitude
    
    Uses the functions from Atmosphere.py to calculate the diameter of the ballon.
    This includes functions like pressure

    Args:
        altitude (float): The altitude to do the calculations for. (m)

    Returns:
        float: The diameter of the balloon. (m)

    """

    # Finding the volume (Can be updated; this assumes constant temperature)
    volume = initial_gas_volume * launch_pressure / atm.getAirPressure(altitude)

    # Finding diameter from volume
    return np.power(6 * volume/(np.pi), 1/3)

def get_volume(altitude):
    """ Finds the volume of the balloon at any altitude.

    Args:
        altitude (float): The altitude at which to find the volume (m)

    Returns:
        float: The volume (m)
    """

    k = R * moles_of_gas
    return k * atm.getAirTemperature(altitude) / atm.getAirPressure(altitude)


def get_burst_altitude(allowed_error = 1):
    """ Iteratively finds the altitude the balloon will burst at

    Args:
        allowed_error (float): How much error is allowed in the calculation.
                               Defaults to 1 meter. (m) 
    
    Returns:
        float: The altitude the balloon will burst at (m)
    """

    altitude = 0

    while (get_diameter(altitude) < burst_diameter):
        altitude += allowed_error

    return altitude

def get_descent_rate(altitude, velocity):
    """ Calculates the descent rate at a given altitude

    Args:
        altitude (float): The altitude to calculate for (m).
        velocity (float): The last velocity recorded (m/s).
    Returns:
        float: The new calculated ascent rate (m/s).
    """
    # ! This isn't working right now, but I think the issue is that it is getting huge velocities from the ascent
    # print(f"8*{payload_mass} * {get_g(altitude)}/(np.pi*{atm.getAirDensity(altitude)}*{velocity}^2)")

    if 8 * payload_mass * get_g(altitude)/(np.pi * atm.getAirDensity(altitude) * velocity ** 2) < 0: 
        print("Invalid value in descent rate")
        # return 0
    return np.sqrt(8 * payload_mass * get_g(altitude)/(np.pi * atm.getAirDensity(altitude) * velocity ** 2))









