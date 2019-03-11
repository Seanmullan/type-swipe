"""
Entry point for the program, which is called by Sandbox
"""

import sys
sys.path.append('data/')
sys.path.append('motor_control/')
sys.path.append('vision/')
sys.path.append('motor_control/')
import threading
import time
import json
import data
import motor
import serial
import preprocessor
import sorter
import object_type
# If the self test is running, import fake conveyor class
if len(sys.argv) == 2:
    if sys.argv[1] == '--test':
        import fake_conveyor as conveyor
else:
    import conveyor as conveyor

class Toddler(object):
    """
    This class initialises all the threads, and updates the Data class with sensor
    and image data
    """

    def __init__(self, io):

        # Define sensor thresholds
        self.proximity_thresh = 13
        self.inductive_thresh = 300
        self.weight_thresh = 100

        # Initialise sensor values
        self.proximity = 15
        self.inductive = 100

        # Initialise buffer for weight sensor values
        self.weight_buffer = []

        # Initialise system objects and driver functions
        self.conveyor = conveyor.Conveyor()
        self.data = data.Data()
        self.preprocessor = preprocessor.Preprocessor()
        self.sorter = sorter.Sorter()
        self.camera = io.camera.initCamera('pi', 'low')
        self.get_inputs = io.interface_kit.getInputs
        self.get_sensors = io.interface_kit.getSensors

        # Initialise helper threads
        self.thread_proxi = threading.Thread(name="get_proxi", target=self.get_proxi)
        self.thread_check_run_system = threading.Thread(
            name="check_run_system",
            target=self.check_run_system
        )

        # Initialise thread stop flags
        self.control_event = threading.Event()
        self.check_run_system_event = threading.Event()

        # Start system threads
        self.thread_check_run_system.start()
        self.thread_proxi.start()
        self.preprocessor.start()
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
        while not self.stopped_check_run_system():
            with open('data/system_control.json') as json_file:
                sys_data = json.load(json_file)
                run_system = sys_data['system']['run']
                conveyor_speed = sys_data['system']['speed']

                # If system is running, update conveyor belt speed
                if run_system:
                    self.conveyor.set_belt_speed(conveyor_speed)
                    motor.motor_move(2, 100)
                    time.sleep(0.2)
                else:
                    self.conveyor.stop_belt()

                # Set system wide flag for start/stop
                self.data.set_run_system(run_system)

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
        print '{}\t{}'.format(self.get_sensors(), self.get_inputs())
        proximity = self.data.get_proximity()
        inductive = float(self.get_sensors()[2])
        weight = float(self.get_sensors()[3])
        self.weight_buffer.append(weight)

        # No object present in sensor zone
        if proximity >= self.proximity_thresh:
            print 'No object present'
            self.wait(False)

        # Non-metallic object present in sensor zone
        elif proximity < self.proximity_thresh and inductive <= self.inductive_thresh:
            self.data.enqueue_metal_queue(0)
            print 'Non-metal object detected'
            max_weight = max(self.weight_array)
            if max_weight < self.weight_threshold:
                print "Plastic object"
                self.data.enqueue_classified_queue(ObjectType.plastic)
            else:
                print "Glass object"
                self.data.enqueue_classified_queue(ObjectType.glass)
            self.weight_array = []
            self.wait(True)

        # Metallic object present in sensor zone
        elif proximity < self.proximity_thresh and inductive > self.inductive_thresh:
            self.data.enqueue_metal_queue(1)
            print 'Metallic object detected'
            self.data.enqueue_classified_queue(ObjectType.metal)
            self.wait(True)

    def wait(self, object_present):
        """
        If no object is present, the thread spins until an object is present. If an
        object is present, the thread spins until the object leaves the sensor zone.
        """
        if not object_present:
            while self.data.get_proximity() >= self.proximity_thresh:
                #print '{}\t{}'.format(self.get_sensors(), self.get_inputs())
                weight = float(self.get_sensors()[3])
                self.weight_buffer.append(weight)
                if self.stopped_control():
                    break
                else:
                    time.sleep(0.1)
        else:
            while self.data.get_proximity() < self.proximity_thresh:
                weight = float(self.get_sensors()[3])
                self.weight_buffer.append(weight)
                if self.stopped_control():
                    break
                else:
                    time.sleep(0.1)
        time.sleep(0.2)

    def get_proxi(self):
        """
        Reads proximity value from USB port.
        """
        ser = serial.Serial('/dev/ttyACM0', 9600)
        while self.data.get_run_system():
            if ser.readline() != None:
                try:
                    proxi = int(float(ser.readline()))
                    self.data.set_proximity(proxi)
                except ValueError:
                    print "Failed to convert proxi string to int"

    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        image = self.camera.getFrame()
        self.data.set_image_raw(image)
        self.camera.imshow('Camera', image)
        # cap0 = cv2.VideoCapture(1)
        # ret0, frame0 = cap0.read()
        # object_name = 'tester'
        # cv2.imwrite('/home/student/images/' + object_name + str(self.counter) + '.png', frame0)
        # self.counter += 1
        # print(frame0.shape)
        time.sleep(0.05)

    def destroy(self):
        """
        Shuts down system threads safely.
        """
        print "Shutting down system"
        self.data.set_run_system(False)
        self.stop_control()
        self.stop_check_run_system()
        self.conveyor.stop_belt()
