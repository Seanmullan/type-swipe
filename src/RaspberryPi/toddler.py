"""
Entry point for the program, which is called by Sandbox.
"""

import sys
sys.path.append('data/')
sys.path.append('motor_control/')
sys.path.append('vision/')
sys.path.append('sensors/')
import threading
import time
import json
import data
import motor
import cv2
import serial
import preprocessor
import sorter
import item_type
import sensor_manager
import model
import numpy as np
import item

# If the self test is running, import fake conveyor class
if len(sys.argv) == 2:
    if sys.argv[1] == '--test':
        import fake_conveyor as conveyor
else:
    import conveyor as conveyor

class Toddler(object):
    """
    Initialises all the threads, and updates the Data class with sensor
    and image data
    """

    def __init__(self, io):

        # Define sensor thresholds
        self.proximity_thresh = 15
        self.inductive_thresh = 450
        self.weight_thresh = 200
        self.weight_interval = 100

        # Initialise system objects and driver functions
        self.conveyor = conveyor.Conveyor()
        self.data = data.Data()
        self.model = model.VisionModel()
        self.sorter = sorter.Sorter()
        self.sensor_manager = sensor_manager.SensorManager(io)
        self.camera = io.camera.initCamera('pi', 'low')
        self.next_object_id = self.data.get_highest_object_id()

        # Initial frame view
        self.initial_frame = self.camera.getFrame()[30:130, 42:106, :]
        initial_frames = []
        for i in range(100):
            initial_frames.append(np.sum(cv2.absdiff(self.initial_frame, self.camera.getFrame()[30:130, 42:106, :])))

        # Compute camera detection threshold
        initial_frames.sort()
        self.detection_threshold = initial_frames[80]
        print "[TODDLER] Detection threshold: ", self.detection_threshold

        # Initialise thread to check Json file
        self.thread_check_run_system = threading.Thread(
            name="check_run_system",
            target=self.check_run_system
        )
        self.control_event = threading.Event()
        self.check_run_system_event = threading.Event()

        # Start system threads
        time.sleep(2)
        self.thread_check_run_system.start()
        self.sensor_manager.start_sensors()
        self.sorter.start()

    def stop_check_run_system(self):
        """
        Sets the stop flag for the check_run_system thread
        """
        self.check_run_system_event.set()

    def stopped_check_run_system(self):
        """
        Returns true if the check_run_system flag has been set
        """
        return self.check_run_system_event.is_set()

    def check_run_system(self):
        """
        Continuously checks the system control file, which will be written to by the
        server. This includes setting the speed of the conveyor belt and stopping the
        whole system.
        """
        initialised_running = False

        while not self.stopped_check_run_system():

            if self.data.get_shut_down():
                self.destroy()
                break

            with open('data/system_control.json') as json_file:
                try:
                    sys_data = json.load(json_file)
                    run_system = sys_data['system']['run']
                    self.data.set_run_system(run_system)

                    if run_system:
                        if initialised_running == False:
                            try:
                                # Sound buzzer 3 times
                                for i in range(3):
                                    motor.motor_move(self.data.BUZZER, 100)
                                    time.sleep(0.4)
                                    motor.stop_motor(self.data.BUZZER)
                                    time.sleep(0.5)
                                
                                self.conveyor.set_belt_speed(100)
                                initialised_running = True
                            except:
                                print "[TODDLER] Failed to write to motor board"
                        time.sleep(0.2)
                    else:
                        initialised_running = False
                        self.conveyor.stop_belt()
                except:
                    print "[TODDLER] Failed to decode JSON"
        self.conveyor.stop_belt()

    def stop_control(self):
        """
        Sets the stop flag for the toddler controensor data - Using computer vision"
                    
        """
        self.control_event.set()

    def stopped_control(self):
        """
        Returns true if the control stop flag is ensor data - Using computer vision"
                    
        """
        return self.control_event.is_set()

    def control(self):
        """
        Called by Sandbox thread. First determines if an object is present in the sensor zone.
        Then, it collects data from inductive and weight sensors and a photo is taken. If the 
        inductive sensor indicates that the object is metallic, then it is immediately classified.
        Otherwise, the weight of the object is analysed. If it is close to the weight threshold,
        the machine learning model is ran with the photo taken. Otherwise, if the object is 
        greater than the weight threshold + weight interval, it is classified as glass, and if it
        is less than the weight threshold - weight interval, it is classified as plastic.
        """

        # No object present in sensor zone
        if self.data.get_proximity() >= self.proximity_thresh:
            time.sleep(0.15)

        else:
            inductive_buffer = []
            weight_buffer = []
            initial_time = time.time()

            # Collect sensor data
            while time.time() - initial_time < 0.75:
                inductive_buffer.append(self.data.get_inductive())
                weight_buffer.append(self.data.get_conveyor_weight())
                time.sleep(0.05)

            max_weight = max(weight_buffer)
            max_inductive = max(inductive_buffer)
            proximity = self.data.get_proximity()

            # Get frame and save image
            time.sleep(0.3)
            image = self.camera.getFrame()[30:130, 42:106, :]
            image_path = '/home/student/images/object_' + str(self.next_object_id) + '.png'
            image_name = 'image_' + str(self.next_object_id) + ".png"
            cv2.imwrite(image_path, image)
            
            final_classification = -1
            sensor_classification = -1
            vision_classification = -1

            # Non-metallic object present in sensor zone
            if max_inductive <= self.inductive_thresh:
                
                if max_weight < self.weight_thresh:
                    # Verify item is present by checking if difference between image and intial
                    # frame is less than the detection threshold.
                    if np.sum(cv2.absdiff(self.initial_frame, image)) < self.detection_threshold:
                        print "[TODDLER] Falsely detected object"
                    else:
                        sensor_classification = item_type.ItemType.plastic

                        # If weight is close to threshold, use computer vision
                        if max_weight > self.weight_thresh - self.weight_interval:
                            print "[TODDLER] Weak sensor data - Using computer vision"
                            self.conveyor.stop_belt()
                            vision_classification = self.classify_vision(image)
                            self.conveyor.set_belt_speed(100)
 
                            if vision_classification == item_type.ItemType.metal:
                                final_classification = sensor_classification
                            else:
                                final_classification = vision_classification
                        else:
                            final_classification = sensor_classification
                
                # If weight is close to threshold, use computer vision
                elif max_weight < self.weight_thresh + self.weight_interval:
                    sensor_classification = item_type.ItemType.glass

                    print "[TODDLER] Weak sensor data - Using computer vision"
                    self.conveyor.stop_belt()
                    vision_classification = self.classify_vision(image)
                    self.conveyor.set_belt_speed(100)

                    if vision_classification == item_type.ItemType.metal:
                        final_classification = sensor_classification
                    else:
                        final_classification = vision_classification

                else:
                    sensor_classification = item_type.ItemType.glass
                    final_classification = sensor_classification

            # Metallic object present in sensor zone
            else:
                sensor_classification = item_type.ItemType.metal
                final_classification = sensor_classification

            # Insert item onto queue
            if final_classification != -1:
                print "[TODDLER] Sensor Classification: ", str(sensor_classification)
                print "[TODDLER] Vision Classification: ", str(vision_classification)
                print "[TODDLER] Final Classification: ", str(final_classification)
                time_to_classify = time.time() - initial_time
                item_data = item.Item(self.next_object_id, final_classification, sensor_classification, vision_classification,
                max_weight, time_to_classify, max_inductive, proximity, 
                image_path, image_name)

                self.data.enqueue_classified_queue(item_data)
                self.next_object_id += 1

            weight_buffer = []
            inductive_buffer = []
            time.sleep(2)

    def classify_vision(self, img):
        """
        Runs machine learning classification.
        """
        prediction = self.model.predict(img)
        if prediction == 0:
            classification = item_type.ItemType.glass
        elif prediction == 1:
            classification = item_type.ItemType.metal
        else:
            classification = item_type.ItemType.plastic
        
        return classification

    def destroy(self):
        """
        Shuts down system threads safely.
        """
        print "[TODDLER] Shutting down system"
        self.stop_control()
        self.stop_check_run_system()
        self.thread_check_run_system.join(timeout=15)
        self.data.set_run_system(False)
        self.data.set_shut_down(True)
        self.conveyor.stop_belt()

    def vision(self):
        """
        Called by Sandbox thread. Unused.
        """
        time.sleep(0.5)
