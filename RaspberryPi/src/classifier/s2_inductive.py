"""
Inductive state when object enters the sensor zone
"""

class InductiveState(object):
    """
    This class checks if the object is metallic
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Inductive State'
        if self.check_conditions():
            return "Camera"
        return "Inductive"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
