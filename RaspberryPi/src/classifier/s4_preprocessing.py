"""
Preprocessing state when photo of object is taken
"""
import data

class PreprocessingState(object):
    """
    This class preprocesses the image
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Preprocessing State'
        if self.check_conditions():
            return "Model"
        return "Preprocessing"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        return True
