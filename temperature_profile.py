""" 2013 Paul Logston

This module defines several temperature profiles that model the heating and 
cooling of different substances
"""

import random

class TemperatureProfile:

    def constant(self, c):
        return lambda x: c

    def linear(self, m, b):
        return lambda x: m*x+b