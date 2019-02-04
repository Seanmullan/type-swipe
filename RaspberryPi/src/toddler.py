"""
Entry point for the program, which is called by Sandbox
"""

import time
import sys
import state_machine
sys.path.append('/home/student/classifier/')

class Toddler(object):
    """
    This class initialises all the threads, and updates the Data class with sensor
    and image data
    """

    def __init__(self, io):

        state = state_machine.StateMachine(0)
        state.start()

        self.camera = io.camera.initCamera('pi', 'low')
        self.get_inputs = io.interface_kit.getInputs
        self.get_sensors = io.interface_kit.getSensors
        self.m_c = io.motor_control
        self.s_c = io.servo_control

    def control(self):
        """
        Called by Sandbox thread. Updates sensor data in Data class.
        """
        print '{}\t{}'.format(self.get_sensors(), self.get_inputs())
        time.sleep(0.05)

    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
        time.sleep(0.05)
