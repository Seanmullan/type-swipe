from __future__ import with_statement
import time
import csv

class Item(object):
    """
    This class contains all data collected about an item as it is classified and sorted
    """

    def __init__(self, item_id, final_classification, sensor_classification, vision_classification, 
                weight, classification_time, inductive_reading, proximity_reading, image_path,
                image_name, bin_class=None, bin_weight_change=None, time_to_bin=None):

        self.__item_id               = item_id
        self.__final_classification  = final_classification
        self.__sensor_classification = sensor_classification
        self.__vision_classification = vision_classification
        self.__weight                = weight
        self.__classification_time   = classification_time
        self.__inductive_reading     = inductive_reading
        self.__proximity_reading     = proximity_reading
        self.__image_path            = image_path
        self.__image_name            = image_name
        self.__bin_class             = bin_class
        self.__bin_weight_change     = bin_weight_change
        self.__time_to_bin           = time_to_bin
        
    """
    Setters
    """
    def set_item_id(self, id):
        self.__item_id = id

    def set_final_classification(self, final_classification):
        self.__final_classification = final_classification
    
    def set_sensor_classification(self, sensor_classification):
        self.__sensor_classification = sensor_classification

    def set_vision_classification(self, vision_classification):
        self.__vision_classification = vision_classification

    def set_item_weight(self,weight):
        self.__weight = weight

    def set_classification_time(self, classification_time):
        self.__classification_time = classification_time

    def set_inductive_reading(self, inductive):
        self.__inductive_reading = inductive

    def set_proximity_reading(self, proximity):
        self.__proximity_reading = proximity_reading

    def set_image_path(self, path):
        self.__image_path = path

    def set_image_name(self, name):
        self.__image_name = name

    def set_bin_class(self, bin):
        self.__bin_class = bin

    def set_bin_weight_change(self, weight_change):
        self.__bin_weight_change = weight_change

    def set_time_to_bin(self, time):
        self.__time_to_bin = time

    """
    Getters
    """
    def get_item_id(self):
        return self.__item_id

    def get_final_classification(self):
        return self.__final_classification
    
    def get_sensor_classification(self):
        return self.__sensor_classification

    def get_vision_classification(self):
        return self.__vision_classification

    def get_item_weight(self):
        return self.__weight

    def get_classification_time(self):
        return self.__classification_time

    def get_inductive_reading(self):
        return self.__inductive_reading

    def get_proximity_reading(self):
        return self.__proximity_reading

    def get_image_path(self):
        return self.__image_path

    def get_image_name(self):
        return self.__image_name

    def get_bin_class(self):
        return self.__bin_class

    def get_bin_weight_change(self):
        return self.__bin_weight_change

    def get_time_to_bin(self):
        return self.__time_to_bin


    def save_data_to_file(self):
        """
        Saves all item data to CSV file.
        """
        with open("Quantative_Data.csv", "a") as text_file:
            text_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                                            str(self.__item_id),
                                            str(self.__final_classification),
                                            str(self.__sensor_classification),
                                            str(self.__vision_classification),
                                            str(self.__weight),
                                            str(self.__classification_time),
                                            str(self.__inductive_reading),
                                            str(self.__proximity_reading),
                                            str(self.__image_path),
                                            str(self.__image_name),
                                            str(self.__bin_class),
                                            str(self.__bin_weight_change),
                                            str(self.__time_to_bin)))

    def toString(self):
        """
        Prints all data collected from item
        """
        string = "[ITEM] Item ID: {}\nFinal Classification: {}\nSensor Classification: {}\nVision Classification: {}\nItem Weight: {}\nTime To Classify: {}\nInductive Reading: {}\nProximity Reading: {}\nImage Path: {}\nImage Name: {}\n Bin Class: {}\nBin Weight Change {}\nTime To Bin {}\n".format(
                                            str(self.__item_id),
                                            str(self.__final_classification),
                                            str(self.__sensor_classification),
                                            str(self.__vision_classification),
                                            str(self.__weight),
                                            str(self.__classification_time),
                                            str(self.__inductive_reading),
                                            str(self.__proximity_reading),
                                            str(self.__image_path),
                                            str(self.__image_name),
                                            str(self.__bin_class),
                                            str(self.__bin_weight_change),
                                            str(self.__time_to_bin))
