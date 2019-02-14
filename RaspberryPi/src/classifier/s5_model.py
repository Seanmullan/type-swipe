"""
Model state when preprocessed image is passed to machine learning model
"""
import data
class ModelState(object):
    """
    This class passes the preprocessed image to the machine learning model
    """

    def __init__(self):
        self.data = data.Data()

    def handle(self):
        """
        Returns state based on transition criteria
        """
        print 'Transitioned to Model State'
        if self.check_conditions():
            return "Proximity"
        return "Model"

    def check_conditions(self):
        """
        Check condition for state transition
        """
        return True
