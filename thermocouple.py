""" 2013 Paul Logston
This module declares a Thermocouple class and a Temperature Profile
that can mimic the output of an Adafruit Thermocouple Amplifier (MAX31855).
"""

"""TODO
Format output strings to two digs after decimal place.
Format tc output to only be fourths of a whole
add more TemperatureProfile

Add ability to set TP from outside object

"""


import random

class TemperatureProfile:
    """A Temperature Profile class that produces a profile of different
    shapes.
    """

    def constant(self, c):
        """Return a constant function"""
        c = float(c)
        return lambda x: c + random.gauss(0, 0.01*c)

    def linear(self, m, b):
        """Return a linear function"""
        return lambda x: m*x + b + random.gauss(0, 1)


class Thermocouple:
    """A Thermocouple class to model an Adafruit Thermocouple Amplifier (MAX31855)."""

    def __init__(self):
        """Build Thermocouple"""
        self.tgen = self.time_point_generator()
        self.TPc = TemperatureProfile()
        self.set_in_profile(self.TPc.constant(23))
        self.set_tc_profile(self.TPc.linear(3,4))

    def set_in_profile(self, fn):
        """Set internal temperature profile to given function and reset."""
        self.in_profile = fn

    def get_in_profile(self):
        """Return internal temperature profile function."""
        return self.in_profile

    def set_tc_profile(self, fn):
        """Set thermocouple temperature profile to given function and reset."""
        self.tc_profile = fn

    def get_tc_profile(self):
        """Return thermocouple temperature profile function."""
        return self.tc_profile

    def read(self):
        """Return a formatted reading from the Thermocouple"""
        t = self.tgen.next()
        return self._fmt_in_output(t) + ',' + self._fmt_tc_output(t) + '\n'

    def _fmt_in_output(self, t):
        """Return string value representing internal temperature"""
        return str(round(self.in_profile(t), 2))

    def _fmt_tc_output(self, t):
        """Return string value representing temperature"""
        return str(round(self.tc_profile(t), 2))

    def time_point_generator(self):
        """Return a time generator. Each time next is called on the generator,
        it returns a unitless time incremented by one time step.
        """
        t = 0
        while True:
            yield t
            t += 1



