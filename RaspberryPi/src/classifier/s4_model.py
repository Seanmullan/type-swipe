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
        image = self.data.get_image_processed()
        classification = self.classify(image)
        self.data.set_classification(classification)
        return "Proximity"

    def classify(self, image):
        """
        Classifies image
        """
        #pylint: disable=unused-argument
        #pylint: disable=no-self-use
        return -1
