"""
Proximity state when conveyor belt is moving but no object is in
the sensor zone
"""

class ProximityState():
    """
    This class checks if an object enters the sensor zone
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print("Transitioned to Proximity State")
        if self.check_conditions():
            return "Inductive"
        return "Proximity"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
