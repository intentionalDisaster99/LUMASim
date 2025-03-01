""" Supplies the atmospheric functions to the simulation files.

Supplies the functions to the other simulation files when imported. 
When run from this file, displays the atmosphere as 3 graphs against altitude.


File Details

File Name:    Atmosphere.py
Author(s):    Sam Whitlock
Status:       Functional
Notes:
    None

"""

import matplotlib.pyplot as plt
import numpy as np


# Function definitions

def toGeopotentialAltitude(altitude):
    """Converts altitude to geopotential altitude.

    Args:
        altitude (float): The altitude to be converted in meters.

    Returns:
        float: The converted altitude in meters.
    """
    earthRadius = 6369000
    return (altitude * earthRadius) / (altitude + earthRadius)

def getAirTemperature(altitude):
    """Gets the temperature of the air at a certain altitude.

    Args:
        altitude (float): The altitude at which the temperature should be found in meters.

    Returns:
        float: The temperature of the air at a specific altitude in kelvin.
    """
    altitude = toGeopotentialAltitude(altitude)

    if altitude < 11000:
        temp = 288.15 - 6.5 / 1000 * altitude
    elif altitude < 20000:
        temp = 216.65
    elif altitude < 32000:
        temp = 216.65 + 1 / 1000 * (altitude - toGeopotentialAltitude(20000))
    elif altitude < 47000:
        temp = 228.65 + 2.8 / 1000 * (altitude - toGeopotentialAltitude(32000))
    elif altitude < 51000:
        temp = 270.65
    elif altitude < 71000:
        temp = 270.65 - 2.8 / 1000 * (altitude - toGeopotentialAltitude(51000))
    elif altitude < 84850:
        temp = 214.65 - 2 / 1000 * (altitude - toGeopotentialAltitude(71000))
    else:
        temp = 186.95
    
    return temp

def getAirDensity(altitude):
    """Returns the density of the air at a certain altitude.

    Args:
        altitude (float): The altitude at which the density should be found in meters.

    Returns:
        float: The density calculated in kg/m^3.
    """
    # We need the pressure at this altitude and temperature, so 
    pressure = getAirPressure(altitude)  # Pa
    temp = getAirTemperature(altitude)  # K

    # The specific gas constant for dry air
    gasConstant = 8.31446261815324 / 0.0289652  # J/(K kg)

    return (pressure) / (gasConstant * temp)
    
def getAirPressure(altitude):
    """Returns the pressure of the air at a certain altitude.

    Args:
        altitude (float): The altitude at which the pressure should be found in meters.

    Returns:
        float: The pressure calculated in Pa.
    """
    altitude = toGeopotentialAltitude(altitude)

    standardSeaLevelPressure = 101325  # Pa
    seaLevelStandardTemp = 288.15  # K
    g = 9.80665  # m/ss
    molarMassOfDryAir = 0.02896968  # kg/mol
    gasConstant = 8.314462618  # J/(molK)
    
    return standardSeaLevelPressure * np.exp(-(g * altitude * molarMassOfDryAir) / (seaLevelStandardTemp * gasConstant))

if __name__ == "__main__":

    # We want 3 graphs, one for density, pressure, and temperature
    figure, axis = plt.subplots(1, 3)

    # Altitude, what is going to be the y in each graph
    altitude = np.arange(0, 80000, 250)  # Meters of course  

    # Temperature
    temp = np.empty(altitude.size)
    for i in range(len(altitude)):
        temp[i] = getAirTemperature(altitude[i])
    axis[0].plot(temp, altitude / 1000)

    # Density
    den = np.empty(altitude.size)
    for i in range(len(altitude)):
        den[i] = getAirDensity(altitude[i])
    axis[1].plot(den, altitude / 1000)

    # Pressure
    pressure = np.empty(altitude.size)
    for i in range(len(altitude)):
        pressure[i] = getAirPressure(altitude[i])
    axis[2].plot(pressure / 1000, altitude / 1000)

    axis[0].set(xlabel='Temperature (k)', ylabel='Altitude (km)')
    axis[1].set(xlabel='Density (kg/m^2)', title="Atmospheric Testing")
    axis[2].set(xlabel='Pressure (kPa)')

    # Saving and showing the plot
    figure.savefig("test.png")
    plt.show()
