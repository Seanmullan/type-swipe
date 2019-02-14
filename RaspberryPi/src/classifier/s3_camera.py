"""
Camera state when non-metallic object is in sensor zone
"""
import data

class CameraState(object):
    """
    This class takes a photo of the object
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Camera State'
        if self.check_conditions():
            return "Preprocessing"
        return "Camera"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        return True
