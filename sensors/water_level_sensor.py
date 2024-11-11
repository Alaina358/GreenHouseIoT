import random

'''
Generates a simulated water level reading in centimeters.
Returns a float representing the water level in centimeters.
Assumed levels are between 0% and 100%
'''

def generate_water_level_data():
    return round(random.uniform(0, 100), 2)