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
        image = self.data.get_image_raw()
        image_processed = self.preprocess(image)
        self.data.set_image_processed(image_processed)
        return "Model"

    def preprocess(self, image):
        """
        Preprocesses image
        """
        #pylint: disable=no-self-use
        return image
