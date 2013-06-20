""" 
2013 Paul Logston

This class defines funcitons that generate temperatures along a thermal
profile. 

"""

class ThermalProfile:
    """A wrapper for several thermal profiles"""

    def root(self, time, power=0.5):
        return pow(time, power)