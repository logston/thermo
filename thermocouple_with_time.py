""" 2013 Paul Logston
This module declares a Thermocouple class that can mimic the output 
of a Adafruit Thermocouple Amplifier (MAX31855).
"""

import datetime
import pytz

import thermal_profile as tpm

class Thermocouple:
    """A Thermocouple class to model a real Thermocouple."""

    def __init__(self):
        """Build Thermocouple"""
        self.init_datetime = datetime.datetime.now(pytz.utc) 
        self.UNIX_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        self.init_ts = (self.init_datetime-self.UNIX_EPOCH).total_seconds()
        self.tp = tpm.ThermalProfile()

    def _current_timestamp(self):
        """Return current UTC timestamp in seconds"""
        return (datetime.datetime.now(pytz.utc)-self.UNIX_EPOCH).total_seconds()

    def _running_timestamp(self):
        """Return time since initialization in seconds"""
        return (datetime.datetime.now(pytz.utc)-self.init_datetime).total_seconds()

    def read(self):
        """Return a formatted reading from the Thermocouple"""
        internal = self._internal_func(self._running_timestamp())
        thermocouple = self._thermocouple_func(self._running_timestamp())
        return str(round(internal, 2)) + ',' + str(round(thermocouple, 2)) + '\n'

    def _internal_func(self, timestamp):
        """A function to simulate the internal temperature fluctuation of 
        the thermocouple.

        """
        return self.tp.root(timestamp)

    def _thermocouple_func(self, timestamp):
        """A function to simulate the thermocouple temperature fluctuation"""
        return self.tp.root(timestamp, power=-1)

