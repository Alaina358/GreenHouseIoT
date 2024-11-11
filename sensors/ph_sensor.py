import random

"""
    Generates a simulated pH value for water.
    Typical pH values for water range from around 6.5 to 8.5.
    Returns a float representing the pH level.
"""

def generate_ph_data():
    return round(random.uniform(6.5, 8.5), 2)