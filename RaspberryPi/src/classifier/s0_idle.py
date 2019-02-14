"""
Idle state when conveyor belt isn't moving
"""
import data

class IdleState(object):
    """
    This class checks if the Start command has been issued
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Idle State'
        if self.check_conditions():
            return "Proximity"
        return "Idle"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        return True
