"""
Inductive state when object enters the sensor zone
"""

import data

class InductiveState(object):
    """
    This class checks if the object is metallic
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Inductive State'
        if self.check_conditions():
            return "Preprocessing"
        return "Inductive"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        if self.data.get_inductive() > 900:
            return True
        return False
