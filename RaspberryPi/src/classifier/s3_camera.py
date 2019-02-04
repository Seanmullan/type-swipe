"""
Camera state when non-metallic object is in sensor zone
"""

class CameraState(object):
    """
    This class takes a photo of the object
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Camera State'
        if self.check_conditions():
            return "Preprocessing"
        return "Camera"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
