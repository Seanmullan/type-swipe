# Data required:
# Inductive sensor data
# Images
# {Classification, ID}

from __future__ import with_statement
import numpy as np
import threading

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Data(object):
    __metaclass__ = Singleton

    def __init__(self):

        self.__inductive      = 0
        self.__image          = np.zeros(500) # TODO: Find size of image array
        self.__classification = [0,0]

        self.__lock_inductive      = threading.RLock()
        self.__lock_image          = threading.RLock()
        self.__lock_classification = threading.RLock()

    def get_inductive(self):
        inductive_data = 0
        with self.__lock_inductive:
            inductive_data = self.__inductive
        return inductive_data

    def set_inductive(self, reading):
        with self.__lock_inductive:
            self.__inductive = reading
    
    def get_image(self):
        image = np.zeros(500)
        with self.__lock_image:
            image = self.__image
        return self.__image

    
    def set_image(self, image):
        with self.__lock_image:
            self.__image = image

    
    def get_classification(self):
        classification = 0
        with self.__lock_classification:
            classification = self.__classification
        return classification

    
    def set_classification(self, classification):
        with self.__lock_classification:
            self.__classification = classification