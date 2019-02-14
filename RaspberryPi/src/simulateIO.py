import numpy as np

class IOTools:
    def __init__(self):
        self.camera = Camera()
        self.interface_kit = InterfaceKitHelper()
        self.motor_control = MotorControl()

    def destroy(self):
        self.camera.destroy()
        self.interface_kit.destroy()
        self.motor_control.stopMotors()

class Camera:
    def __init__(self):
        pass
    
    def initCamera(self, camera='pi', resolution='low'):
        return self

    def getFrame(self):
        return np.zeros(500)

    def imshow(self, name, image):
        pass

class InterfaceKitHelper:
    __inputs = np.zeros(8)
    __sensors = np.zeros(8)

    def __init__(self):
        pass
    
    def getInputs(self):
        return InterfaceKitHelper.__inputs[:]

    def getSensors(self):
        return InterfaceKitHelper.__sensors[:]

class MotorControl:
    def __init__(self):
        pass
    
    def setMotor(self, id, speed):
        pass

    def stopMotor(self, id):
        pass

    def stopMotors(self):
        pass
    
    def __write(self, value):
        pass

