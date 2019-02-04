"""
Idle state when conveyor belt isn't moving
"""

class IdleState(object):
    """
    This class checks if the Start command has been issued
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Idle State'
        if self.check_conditions():
            return "Proximity"
        return "Idle"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
