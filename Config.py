""" Provides a simple place to update the details to the simulations.

Holds the constants required behind the scenes for the simulations that change how the simulation performs.
This is where you should generally change the inputs to the simulation.


File Details

File Name:    Config.py
Author(s):    Sam Whitlock
Status:       In progress
Notes:
    None

"""

# Balloon details 
# Burst diameters in meters
burst_diameters = {
    "k50": 0.88,
    "k100": 1.96,
    "k150": 2.52,
    "k200": 3.00,
    "k300": 3.78,
    "k350": 4.12,
    # "k450": 4.72, 
    # "k500": 4.99,
    "k600": 6.02,
    # "k700": 6.53, 
    "k800": 7.00,
    "k1000": 7.86,
    "k1200": 8.63,
    "k1500": 9.44,
    "k1600": 9.71,
    "k1800": 9.98,
    "k2000": 10.54,
    "k3000": 13.00,
    "k4000": 15.06,
    # 100g Hwoyee Data from http://www.hwoyee.com/images.aspx?fatherId=11010101&msId=1101010101&title=0
    "h100": 2.00,
    # Hwoyee data from http://www.hwoyee.com/base.asp?ScClassid=521&id=521102
    # Updated 2024-11 from https://www.hwoyee.com/weather-balloon-meteorological-balloon-for-weather-sounding-wind-or-cloud-detection-near-space-researchesgiant-round-balloons-huge-balloons-product/
    "h200": 2.97,
    "h300": 4.30,
    "h350": 4.80,
    "h500": 5.80,
    "h600": 6.50,
    "h750": 6.90,
    "h800": 7.00,
    "h1000": 8.00,
    "h1200": 9.10,
    "h1600": 10.00,
    # These two are fudged a little
    "h2000": 11.00,
    "h3000": 12.00,
    # PAWAN data from
    # http://randomaerospace.com/Random_Aerospace/Balloons.html
    "p100": 1.6,
    "p350": 4.0,
    "p600": 5.8,
    "p800": 6.6,
    "p900": 7.0,
    "p1200": 8.0,
    "p1600": 9.5,
    "p2000": 10.2,
}

# Coefficient of Drag
drag_coefficients = {
    "k50": 0.25,
    "k100": 0.25,
    "k150": 0.25,
    "k200": 0.25,
    "k300": 0.25,
    "k350": 0.25,
    "k450": 0.25,
    "k500": 0.25,
    "k600": 0.30,
    "k700": 0.30,
    "k800": 0.30,
    "k1000": 0.30,
    "k1200": 0.25,
    "k1500": 0.25,
    "k1600": 0.25,
    "k1800": 0.25,
    "k2000": 0.25,
    "k3000": 0.25,
    "k4000": 0.25,
    # Hwoyee data just guesswork
    "h100": 0.25,
    "h200": 0.25,
    "h300": 0.25,
    "h350": 0.25,
    "h400": 0.25,
    "h500": 0.25,
    "h600": 0.30,
    "h750": 0.30,
    "h800": 0.30,
    "h950": 0.30,
    "h1000": 0.30,
    "h1200": 0.25,
    "h1500": 0.25,
    "h1600": 0.25,
    "h2000": 0.25,
    "h3000": 0.25,
    # PAWAN data also guesswork
    "p100": 0.25,
    "p350": 0.25,
    "p600": 0.30,
    "p800": 0.30,
    "p900": 0.30,
    "p1200": 0.25,
    "p1600": 0.25,
    "p2000": 0.25,
}

# Masses in grams
balloon_masses = {
    "k50": 50,
    "k100": 100,
    "k150": 150,
    "k200": 200,
    "k300": 300,
    "k350": 350,
    "k600": 600,
    "k800": 800,
    "k1000": 1000,
    "k1200": 1200,
    "k1500": 1500,
    "k1600": 1600,
    "k1800": 1800,
    "k2000": 2000,
    "k3000": 3000,
    "k4000": 4000,
    "h100": 100,
    "h200": 200,
    "h300": 300,
    "h350": 350,
    "h500": 500,
    "h600": 600,
    "h750": 750,
    "h800": 800,
    "h1000": 1000,
    "h1200": 1200,
    "h1600": 1600,
    "h2000": 2000,
    "h3000": 3000,
    "p100": 100,
    "p350": 350,
    "p600": 600,
    "p800": 800,
    "p900": 900,
    "p1200": 1200,
    "p1600": 1600,
    "p2000": 2000,
}



# Direct inputs
simulation_length = 3 # Hours
balloon_type = "k1000" # String name; check dict below for more
helium_mass = 100 # grams
payload_mass = 3000 # grams

# Constants
simulation_steps = 10000


# Calculated
simulation_length_seconds = simulation_length * 3600 # Seconds
delta_time = simulation_length_seconds / simulation_steps # Seconds / step
burst_diameter = burst_diameters[balloon_type] # Meters
balloon_mass = balloon_masses[balloon_type] # Grams
balloon_drag_coefficient = drag_coefficients[balloon_type]
total_mass = payload_mass + helium_mass + balloon_mass


