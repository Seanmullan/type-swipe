"""
This pre-trained machine learning model classifies objects in images as either
glass or plastic.
"""

import threading

class Model(threading.Thread):
    """
    Thread is alive while the image is being classified, and subseqeuntly destroyed.
    """

    def __init__(self, image):
        threading.Thread.__init__(self)
        self.image = image

    def run(self):
        """
        Classify object here
        """
        pass
