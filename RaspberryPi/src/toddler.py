"""
Entry point for the program, which is called by Sandbox
"""

import sys
sys.path.append('classifier/')
sys.path.append('data/')
#pylint: disable=wrong-import-position
import state_machine
import data

class Toddler(object):
    """
    This class initialises all the threads, and updates the Data class with sensor
    and image data
    """

    def __init__(self, io):

        self.state = state_machine.StateMachine(0)
        self.state.start()

        self.data = data.Data()

        self.camera = io.camera.initCamera('pi', 'low')
        self.get_inputs = io.interface_kit.getInputs
        self.get_sensors = io.interface_kit.getSensors
        self.m_c = io.motor_control

    def control(self):
        """
        Called by Sandbox thread. Updates sensor data in Data class.
        """
        print '{}\t{}'.format(self.get_sensors(), self.get_inputs())
        self.data.set_inductive(100)

    def vision(self):
        """
        Called by Sandbox thread. Updates image data in Data class.
        """
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
