"""
Model state when preprocessed image is passed to machine learning model
"""

class ModelState(object):
    """
    This class passes the preprocessed image to the machine learning model
    """

    def __init__(self):
        pass

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Model State'
        if self.check_conditions():
            return "Proximity"
        return "Model"

    @staticmethod
    def check_conditions():
        """
        Check condition for state transition
        """
        return True
