"""
Processes images as they pass beneath the camera. Detects when object is in centre of the frame,
and if the object is non-metallic (as determined by the metal queue), it further preprocesses the
image and starts a thread for the Model to classify the object as glass or plastic.
"""

import threading
import math
import numpy as np
import cv2
import data
import model

class Preprocessor(threading.Thread):
    """
    See module description for this class
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.raw_image = np.ndarray((128, 160, 3))
        self.prev_raw_image = np.ndarray((128, 160, 3))
        self.frame_centre = np.array((50, 50))
        self.prev_dist = 0
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        If the run_system flag is set, execute object detection
        """
        while True:
            if self.stopped():
                break

            if self.data.get_run_system():
                if not self.data.metal_queue_empty():
                    raw_image = self.data.get_image_raw()
                    self.detect_object(raw_image)

        print("preprocessor exiting")

    def detect_object(self, raw_image):
        """
        This algorithm finds the frame where the distance between the centre of the frame
        and the centroid of the object is minimised (i.e. the object is closest to the centre
        of the frame). If the incoming object is metal, add metal to the classifified queue.
        Otherwise, start a thread for the Model and pass the image in.
        """
        centroid = detect_centroid(raw_image)
        dist = distance(centroid, self.frame_centre)

        # If the distance between the centroids have increased, then the object is moving away
        # from the centre of the frame, so we use the previous frame.
        if dist > self.prev_dist:
            image = self.prev_raw_image
            metal = self.data.dequeue_metal_queue()
            if metal:
                self.data.enqueue_classified_queue("Metal")
            else:
                thread_model = model.Model(image)
                thread_model.start()
        # Otherwise, the object is still moving closer to the centre of the frame.
        else:
            self.prev_raw_image = raw_image
            self.prev_dist = dist

def detect_centroid(raw_image):
    """
    Finds the (x,y) coordinates of the centroid of the object
    """
    # # find center of mass to track whether the object is located
    # gray_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(raw_image, 127, 255, 1)
    # M = cv2.moments(thresh)

    # #there may be bugs here.... M["m00"]
    # cX = int(M["m10"] / M["m00"])
    # cY = int(M["m01"] / M["m00"])

    # return np.array((cX,cY))
    return np.zeros(2)

def distance(centroid_1, centroid_2):
    """
    Calculates Euclidean distance between two centroid points.
    """
    return math.sqrt((centroid_2[0] - centroid_1[0])**2 + (centroid_2[1] - centroid_2[1])**2)
