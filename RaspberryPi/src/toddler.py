import time
import numpy
import cv2
import threading
import sys
sys.path.append('/home/student/classifier/')
import state_machine

class Toddler:

    def __init__(self, IO):

        state = state_machine.StateMachine(1)
        state.start()

        self.camera = IO.camera.initCamera('pi', 'low')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.sc = IO.servo_control
        print(sys.path)

    def control(self):
        print('{}\t{}'.format(self.getSensors(), self.getInputs()))
        time.sleep(0.05)

    def vision(self):
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
        time.sleep(0.05)
        