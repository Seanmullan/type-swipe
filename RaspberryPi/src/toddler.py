"""
Entry point for the program, which is called by Sandbox
"""

import sys
sys.path.append('data/')
sys.path.append('motor_control/')
#pylint: disable=wrong-import-position
import threading
import json
import data
sys.path.append('vision/')
import preprocessor
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

        # Initialise system objects and driver functions
        self.preprocessor = preprocessor.Preprocessor()
        self.conveyor = conveyor.Conveyor()
        self.data = data.Data()
        self.camera = io.camera.initCamera('pi', 'low')
        self.get_inputs = io.interface_kit.getInputs
        self.get_sensors = io.interface_kit.getSensors
        self.__control_stop_event = threading.Event()   #Needed for getting stuck in while loops
        self.__thread_check_run_system_stop_event = threading.Event()

        self.thread_check_run_system = threading.Thread(name="check_run_system", target=self.check_run_system)

        # Start system threads
        self.thread_check_run_system.start()
        self.preprocessor.start()

    def stop_check_run_system(self):
        """
        Sets the stop flag for the check_run_system thread
        """
        self.__thread_check_run_system_stop_event.set()

    def stopped_check_run_system(self):
        """
        Returns true if the check_run_system flag has been set
        """
        return self.__thread_check_run_system_stop_event.is_set()

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
                else:
                    self.conveyor.stop_belt()

                # Set system wide flag for start/stop
                self.data.set_run_system(run_system)


    """
    We need a thread stopper event inside the toddler due to
    The thread getting stuck in the while loops for when an object is passing through
    As of now we can stop the thread but perhaps it would be useful to improve the
    control algorithm so that it doesn't get stuck like this
    """

    def stop_control(self):
        """
        Sets the stop flag for the toddler control thread
        """
        self.__control_stop_event.set()

    def stopped_control(self):
        """
        Returns true if the control stop flag is set
        """
        return self.__control_stop_event.is_set()

    def control(self):
        """
        Called by Sandbox thread. Determines if an object is present in the sensor zone, and if so,
        whether it is metallic or non-metallic. A '1' is added to the metal queue if metallic, and
        a 0 is added otherwise. While the current object is present, the function will spin until
        the object leaves the sensor zone.
        TODO: Figure out sensor thresholds
        """
        #print '{}\t{}'.format(self.get_sensors(), self.get_inputs())
        sensor_data = self.get_sensors()
        proximity = sensor_data[0]
        inductive = sensor_data[1]

        if proximity >= 15:
            print 'No object present'
            while self.get_sensors()[0] >= 15:
                if self.stopped_control():
                    break
                else:
                    continue

        elif proximity < 15 and inductive >= 900:
            self.data.enqueue_metal_queue(0)
            print 'Non-metal object detected'
            while self.get_sensors()[0] < 15:
                if self.stopped_control():
                    break
                else:
                    continue

        elif proximity < 15 and inductive < 900:
            self.data.enqueue_metal_queue(1)
            print 'Metallic object detected'
            while self.get_sensors()[0] < 15:
                if self.stopped_control():
                    break
                else:
                    continue


    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        # image = self.camera.getFrame()
        # self.data.set_image_raw(image)
        # self.camera.imshow('Camera', image)
