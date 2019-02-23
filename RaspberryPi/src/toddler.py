"""
Entry point for the program, which is called by Sandbox
"""

import sys
sys.path.append('data/')
#pylint: disable=wrong-import-position
import threading
import data
import preprocessor
import json
if len(sys.argv) == 2:
    import fake_conveyor as conveyor
else:
    import conveyor as conveyor

class Toddler(object):
    """
    This class initialises all the threads, and updates the Data class with sensor
    and image data
    """

    def __init__(self, io):

        self.preprocessor = preprocessor.Preprocessor()
        self.conveyor = conveyor.Conveyor()

        self.data = data.Data()

        self.camera = io.camera.initCamera('pi', 'low')
        self.get_inputs = io.interface_kit.getInputs
        self.get_sensors = io.interface_kit.getSensors
        self.m_c = io.motor_control

        def check_run_system():
            while True:
                with open('system_control.json') as json_file:
                    data = json.load(json_file)
                    run_system = data['system']['run']
                    conveyor_speed = data['system']['speed']

                    if run_system:
                        self.conveyor.set_belt_speed(conveyor_speed)
                    else:
                        self.conveyor.stop_belt()
        
                    self.data.set_run_system(run_system)

        self.thread_check_run_system = threading.Thread(target=check_run_system)
        self.thread_check_run_system.start()

        self.preprocessor.start()


    def control(self):
        """
        Called by Sandbox thread. Updates sensor data in Data class.
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
