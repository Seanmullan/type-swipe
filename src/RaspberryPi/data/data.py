"""
This Singleton data class provides thread safe getters and setters for shared resources
"""

from __future__ import with_statement
import threading
import Queue as queue
import numpy as np
from google.cloud import storage
import os
import psycopg2
import json
import time
import item_type

# pylint: disable=too-many-instance-attributes

class Singleton(type):
    """
    Creates Singleton instances of Data
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Data(object):
    """
    Thread safe getters and setters of shared resources
    """
    __metaclass__ = Singleton
    # Define motor board indices
    ENTRANCE_MOTOR_INDUCTIVE_PWR = 1
    BUZZER  = 2
    VERTICAL_MOTOR = 3
    EXIT_MOTOR     = 4
    ROTATION_MOTOR = 5

    # Define phidget board indices
    LIGHT           = 0
    INDUCTIVE_DATA  = 1
    GLASS_BIN       = 3
    PLASTIC_BIN     = 4
    METAL_BIN       = 5
    CONVEYOR_WEIGHT = 7

    def __init__(self):
        self.__proximity = 20
        self.__inductive = 0
        self.__vertical_position = 0
        self.__rotation_position = 0
        self.__bin_weights = [0,0,0]
        self.__conveyor_weight = 0
        self.__shut_down = False
        self.__run_system = False
        self.__classified_queue = queue.Queue()
        self.next_object_id = self.get_highest_object_id()

        self.__lock_proximity = threading.RLock()
        self.__lock_inductive = threading.RLock()
        self.__lock_vertical_position = threading.RLock()
        self.__lock_rotation_position = threading.RLock()
        self.__lock_bins = threading.RLock()
        self.__lock_conveyor = threading.RLock()
        self.__lock_image_raw = threading.RLock()
        self.__lock_run_system = threading.RLock()
        self.__lock_shut_down = threading.RLock()

    def get_proximity(self):
        """
        Return proximity value
        """
        proximity = 0
        with self.__lock_proximity:
            proximity = self.__proximity
        return proximity

    def set_proximity(self, reading):
        """
        Set proximity value
        """
        with self.__lock_proximity:
            self.__proximity = reading

    def get_inductive(self):
        """
        Return inductive sensor value
        """
        inductive_data = 0
        with self.__lock_inductive:
            inductive_data = self.__inductive
        return inductive_data

    def set_inductive(self, reading):
        """
        Set inductive sensor value
        """
        with self.__lock_inductive:
            self.__inductive = reading

    def get_vertical_position(self):
        """
        Return vertical motor position value
        """
        vertical_pos = 0
        with self.__lock_vertical_position:
            vertical_pos = self.__vertical_position
        return vertical_pos

    def set_vertical_position(self, position):
        """
        Set vertical motor position value
        """
        with self.__lock_vertical_position:
            self.__vertical_position = position

    def get_rotation_position(self):
        """
        Return rotation motor position value
        """
        rotation_pos = 0
        with self.__lock_rotation_position:
            rotation_pos = self.__rotation_position
        return rotation_pos

    def set_rotation_position(self, position):
        """
        Set rotation motor position value
        """
        with self.__lock_rotation_position:
            self.__rotation_position = position

    def get_bin_weights(self):
        """
        Return bin weights
        """
        weights = [0, 0, 0]
        with self.__lock_bins:
            weights = self.__bin_weights
        return weights

    def set_bin_weights(self, weights):
        """
        Set bin weights
        """
        with self.__lock_bins:
            self.__bin_weights = weights

    def get_conveyor_weight(self):
        """
        Return conveyor belt weight sensor
        """
        weight = 0
        with self.__lock_conveyor:
            weight = self.__conveyor_weight
        return weight

    def set_conveyor_weight(self, weight):
        """
        Set conveyor sensor weight
        """
        with self.__lock_conveyor:
            self.__conveyor_weight = weight

    def enqueue_classified_queue(self, classification):
        """
        Enqueues classification
        """
        self.__classified_queue.put(classification)

    def dequeue_classified_queue(self):
        """
        Dequeue and returns classification
        """
        return self.__classified_queue.get()

    def classification_queue_empty(self):
        """
        Returns true if queue is empty
        """
        return self.__classified_queue.empty()

    def get_run_system(self):
        """
        Return TRUE if unpaused (set by web app), FALSE otherwise
        """
        run = False
        with self.__lock_run_system:
            run = self.__run_system
        return run

    def set_run_system(self, run):
        """
        Set flag for pausing and unpausing system
        """
        with self.__lock_run_system:
            self.__run_system = run

    def get_shut_down(self):
        """
        Return flag for shutting down system
        """
        shut_down = False
        with self.__lock_shut_down:
            shut_down = self.__shut_down
        return shut_down

    def set_shut_down(self, shut_down):
        """
        Set flag for shutting down system
        """
        with self.__lock_shut_down:
            self.__shut_down = shut_down

    def insert_data_to_database(self, obj_id, classification, obj_weight):
        """
        Inserts into database object's id, classification and bin where it fell
        """
        if classification == item_type.ItemType.glass:
            object_class = "glass"
        elif classification == item_type.ItemType.plastic:
            object_class = "plastic"
        else:
            object_class = "metal"

        print("Inserting object ID: " + str(obj_id) + " Classification: " + object_class)
        sql = """INSERT INTO collected_data(object_id, object_classified, object_weight)
                VALUES(%s, %s, %s) RETURNING object_id, object_classified, object_weight;"""
        conn = None
        vendor_id = None
        try:
            # Read database configuration
            conn = psycopg2.connect(dbname='s1764997', user='s1764997', password='password', host='pgteach', port='5432', sslmode='disable')
            # Create a new cursor
            cur = conn.cursor()
            # Execute the INSERT statement
            cur.execute(sql, (obj_id, object_class, obj_weight))
            # Commit the changes to the database
            conn.commit()
            # Close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        
        self.update_next_object_id()

    def upload_image_to_cloud(self, bucket_name, source_file_name, destination_blob_name):
        """
        Uploads an image to the bucket.
        bucket_name - name of bucket to upload image into
        source_file_name - path to and name of a file to upload
        destination_blob_name - destination on the bucket where the file will be uploaded
        """
        initial_time = time.time()
        # Use credentials json file to authenticate for uploading the image
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

        print "Upload time elapsed: ", time.time() - initial_time

    def get_highest_object_id(self):
        """
        Reads from file system_control.json which stores id of an object to be classified
        """
        with open('data/id.json') as json_file:  
            data = json.load(json_file)
            highest_id = data['item']['next_id']
        return highest_id

    def update_next_object_id(self):
        """
        Updates id of a next object to be classified into the file
        """
        data = ""
        with open('data/id.json', 'r') as json_file:  
            data = json.load(json_file)
            data['item']['next_id'] += 1

        if data != "":
            with open('data/id.json', 'w') as json_file:
                json.dump(data, json_file)
