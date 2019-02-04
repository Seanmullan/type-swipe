"""
Preprocessing state when photo of object is taken
"""

class PreprocessingState(object):
    """
    This class preprocesses the image
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Preprocessing State'
        if self.check_conditions():
            return "Model"
        return "Preprocessing"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
