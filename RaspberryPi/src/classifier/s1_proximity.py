"""
Proximity state when conveyor belt is moving but no object is in
the sensor zone
"""

import data

class ProximityState(object):
    """
    This class checks if an object enters the sensor zone
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Proximity State'
        if self.check_conditions():
            return "Inductive"
        return "Proximity"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        if self.data.get_proximity() < 20:
            return True
        return False
