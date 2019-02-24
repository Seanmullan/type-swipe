"""
Entry point for the program, which is called by Sandbox
"""

import sys
sys.path.append('data/')
#pylint: disable=wrong-import-position
import threading
import json
import data
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

        def check_run_system():
            """
            Continuously checks the system control file, which will be written to by the
            server. This includes setting the speed of the conveyor belt and stopping the
            whole system.
            """
            while True:
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

        self.thread_check_run_system = threading.Thread(target=check_run_system)

        # Start system threads
        self.thread_check_run_system.start()
        self.preprocessor.start()


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
                continue

        elif proximity < 15 and inductive >= 900:
            self.data.enqueue_metal_queue(0)
            print 'Non-metal object detected'
            while self.get_sensors()[0] < 15:
                continue

        elif proximity < 15 and inductive < 900:
            self.data.enqueue_metal_queue(1)
            print 'Metallic object detected'
            while self.get_sensors()[0] < 15:
                continue


    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        image = self.camera.getFrame()
        self.data.set_image_raw(image)
        self.camera.imshow('Camera', image)
