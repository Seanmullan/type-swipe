"""
Entry point for the program, which is called by Sandbox
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
import serial
import preprocessor
import sorter
import object_type
import sensor_manager
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
        self.inductive_thresh = 300
        self.weight_thresh = 200

        # Initialise sensor values
        self.proximity = 20
        self.inductive = 100

        # Initialise buffers for weight and inductive sensors
        self.weight_buffer = []
        self.inductive_buffer = []

        # Initialise system objects and driver functions
        self.conveyor = conveyor.Conveyor()
        self.data = data.Data()
        self.preprocessor = preprocessor.Preprocessor()
        self.sorter = sorter.Sorter()
        self.sensor_manager = sensor_manager.SensorManager(io)
        #self.camera = io.camera.initCamera('pi', 'low')

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
        #self.preprocessor.start()
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
            with open('data/system_control.json') as json_file:
                try:
                    sys_data = json.load(json_file)
                    run_system = sys_data['system']['run']
                    self.data.set_run_system(run_system)

                    if run_system:
                        if initialised_running == False:
                            try:
                                self.conveyor.set_belt_speed(70)
                                initialised_running = True
                            except:
                                print "Failed to write to motor board"
                        time.sleep(0.2)
                    else:
                        initialised_running = False
                        self.conveyor.stop_belt()
                except:
                    print "Failed to decode JSON"
        self.conveyor.stop_belt()

    def stop_control(self):
        """
        Sets the stop flag for the toddler control thread
        """
        self.control_event.set()

    def stopped_control(self):
        """
        Returns true if the control stop flag is set
        """
        return self.control_event.is_set()

    def control(self):
        """
        Called by Sandbox thread. Determines if an object is present in the sensor zone, and if so,
        whether it is metallic or non-metallic. A '1' is added to the metal queue if metallic, and
        a 0 is added otherwise. While the current object is present, the function will spin until
        the object leaves the sensor zone.
        """
        
        # No object present in sensor zone
        if self.data.get_proximity() >= self.proximity_thresh:
            time.sleep(0.15)

        else:
            inductive_buffer = []
            weight_buffer = []
            initial_time = time.time()

            while time.time() - initial_time < 0.75:
                inductive_buffer.append(self.data.get_inductive())
                weight_buffer.append(self.data.get_conveyor_weight())
                time.sleep(0.05)

            # Non-metallic object present in sensor zone
            if max(inductive_buffer) <= self.inductive_thresh:
                self.data.enqueue_metal_queue(0)
                print 'Non-metal object detected'
                
                if max(weight_buffer) < self.weight_thresh:
                    print "Plastic object"
                    self.data.enqueue_classified_queue(object_type.ObjectType.plastic)
                else:
                    print "Glass object"
                    self.data.enqueue_classified_queue(object_type.ObjectType.glass)

            # Metallic object present in sensor zone
            else:
                self.data.enqueue_metal_queue(1)
                print 'Metallic object detected'
                self.data.enqueue_classified_queue(object_type.ObjectType.metal)

            weight_buffer = []
            inductive_buffer = []
            time.sleep(2)
 
    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        #image = self.camera.getFrame()
        #self.data.set_image_raw(image)
        #self.camera.imshow('Camera', image)
        # cap0 = cv2.VideoCapture(1)
        # ret0, frame0 = cap0.read()
        # object_name = 'tester'
        # cv2.imwrite('/home/student/images/' + object_name + str(self.counter) + '.png', frame0)
        # self.counter += 1
        # print(frame0.shape)
        time.sleep(1)

    def destroy(self):
        """
        Shuts down system threads safely.
        """
        print "Shutting down system"
        self.stop_control()
        self.stop_check_run_system()
        self.thread_check_run_system.join()
        self.data.set_run_system(False)
        self.data.set_shut_down(True)
        self.conveyor.stop_belt()