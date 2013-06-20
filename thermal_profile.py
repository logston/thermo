""" 2013 Paul Logston
This class defines several temperature profiles that model the heating and 
cooling of different substances
"""


class TemperatureProfile:
    """A class that defines different temperature profiles"""
    
    def constant(c):
        return lambda x: c

    def linear(m, b):
        return lambda x: m*x+b