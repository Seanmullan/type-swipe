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
    BUZZER         = 0
    ENTRANCE_MOTOR = 1
    INDUCTIVE_PWR  = 2
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
        self.__image_raw = np.ndarray((128, 160, 3))
        self.__shut_down = False
        self.__run_system = False

        # FIFO queues are syncronized
        self.__classified_queue = queue.Queue()
        self.__metal_queue = queue.Queue()

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
    
    def get_image_raw(self):
        """
        Return image take by Pi
        """
        image = np.ndarray((128, 160, 3))
        with self.__lock_image_raw:
            image = self.__image_raw
        return image

    def set_image_raw(self, image):
        """
        Set image take by Pi
        """
        with self.__lock_image_raw:
            self.__image_raw = image

    def enqueue_metal_queue(self, metallic):
        """
        Enqueues metal (1) or non-metal (0)
        """
        self.__metal_queue.put(metallic)

    def dequeue_metal_queue(self):
        """
        Dequeue and returns 1 or 0 for metallic
        """
        return self.__metal_queue.get()

    def metal_queue_empty(self):
        return self.__metal_queue.empty()

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

    def insert_classified_to_database(classification):
         """
         Inserts classification of an object into database
         """
         sql = """INSERT INTO collected_data(object_classified)
                 VALUES(%s) RETURNING object_classified;"""
         conn = None
         vendor_id = None
         try:
             # Read database configuration
             conn = psycopg2.connect(dbname='s1764997', user='s1764997', password='password', host='pgteach', port='5432', sslmode='disable')
             # Create a new cursor
             cur = conn.cursor()
             # Execute the INSERT statement
             cur.execute(sql, (classification,))
             # Commit the changes to the database
             conn.commit()
             # Close communication with the database
             cur.close()
         except (Exception, psycopg2.DatabaseError) as error:
             print(error)
         finally:
             if conn is not None:
                 conn.close()

    def insert_data_to_database(obj_id, classification, obj_bin):
         """
         Inserts into database object's id, classification and bin where it fell
         """
         sql = """INSERT INTO collected_data(object_id, object_classified, object_bin)
                 VALUES(%s, %s, %s) RETURNING object_classified;"""
         conn = None
         vendor_id = None
         try:
             # Read database configuration
             conn = psycopg2.connect(dbname='s1764997', user='s1764997', password='password', host='pgteach', port='5432', sslmode='disable')
             # Create a new cursor
             cur = conn.cursor()
             # Execute the INSERT statement
             cur.execute(sql, (obj_id, classification, obj_bin))
             # Commit the changes to the database
             conn.commit()
             # Close communication with the database
             cur.close()
         except (Exception, psycopg2.DatabaseError) as error:
             print(error)
         finally:
             if conn is not None:
                 conn.close()

    def upload_image_to_cloud(bucket_name, source_file_name, destination_blob_name):
        """
        Uploads an image to the bucket.
        bucket_name - name of bucket to upload image into
        source_file_name - path to and name of a file to upload
        destination_blob_name - destination on the bucket where the file will be uploaded
        """
        # Use credentials json file to authenticate for uploading the image
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../credentials.json"

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
