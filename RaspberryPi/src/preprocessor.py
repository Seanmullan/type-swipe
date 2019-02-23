import threading
import numpy as np
import data
import model
import math
import cv2

class Preprocessor(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.raw_image = np.ndarray((128,160,3))
        self.prev_raw_image = np.ndarray((128,160,3))
        self.frame_centre = np.array((50,50))
        self.prev_distance = 0

    def run(self):
        while True:
            if self.data.get_run_system():
                raw_image = self.data.get_image_raw()
                self.detect_object(raw_image)

    def detect_object(self, raw_image):
        centroid = self.detect_centroid(raw_image)
        distance = self.distance(centroid, self.frame_centre)

        if distance > self.prev_distance:
            image = self.prev_raw_image
            metal = self.data.dequeue_metal_queue()
            if metal:
                self.data.enqueue_classified_queue("Metal")
            else:
                self.model = model.Model(image)
                self.model.start()
        else:
            self.prev_raw_image = raw_image

    def detect_centroid(self, raw_image):
        # # find center of mass to track whether the object is located 
        # gray_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        # _, thresh = cv2.threshold(gray_image,127,255,1)
        # M = cv2.moments(thresh)
    
        # #there may be bugs here.... M["m00"]
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])

        # return np.array((cX,cY))
        return np.zeros(2)

    def distance(self, centroid_1, centroid_2):
        return math.sqrt( (centroid_2[0] - centroid_1[0])**2 + (centroid_2[1] - centroid_2[1])**2 )
