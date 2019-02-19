"""
Acts as a fake IO class for Sandbox simulator. Used to test logic flow of program
"""

#pylint: disable=invalid-name
#pylint: disable=no-self-use
#pylint: disable=unused-argument
#pylint: disable=too-few-public-methods
import numpy as np

class IOTools(object):
    """
    Initialises fake drivers
    """
    def __init__(self):
        self.camera = Camera()
        self.interface_kit = InterfaceKitHelper()
        self.motor_control = MotorControl()

class Camera(object):
    """
    Fake Camera object
    """
    def __init__(self):
        pass

    def initCamera(self, camera='pi', resolution='low'):
        """
        Return fake Camera object
        """
        return self

    def getFrame(self):
        """
        Return dummy image
        """
        return np.zeros(500)

    def imshow(self, name, image):
        """
        Dummy function for image display
        """
        pass

class InterfaceKitHelper(object):
    """
    Fake sensor driver class
    """
    __inputs = np.zeros(8)
    __sensors = np.zeros(8)

    def __init__(self):
        pass

    def getInputs(self):
        """
        Return dummy readings
        """
        return InterfaceKitHelper.__inputs[:]

    def getSensors(self):
        """
        Return dummy readings
        """
        return InterfaceKitHelper.__sensors[:]

class MotorControl(object):
    """
    Fake motor driver class
    """
    def __init__(self):
        pass

    def setMotor(self, motor_id, speed):
        """
        Set dummy motors
        """
        pass

    def stopMotor(self, motor_id):
        """
        Set dummy motor by id
        """
        pass

    def stopMotors(self):
        """
        Set all dummy motors
        """
        pass

    def __write(self, value):
        """
        Write to dummy motor
        """
        pass
