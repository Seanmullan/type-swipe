import threading
import time
import data
import motor

class Inductive(threading.Thread):

    def __init__(self, io):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.get_sensors = io.interface_kit.getSensors
        
        # Inductive sensor is powered from the motor board output
        motor.motor_move(self.data.INDUCTIVE_PWR, 100)

    def run(self):
        """
        Reads inductive sensor data from phidget board and updates
        data class.
        """
        while not self.data.get_shut_down():
            sensor_data = self.get_sensors()

            inductive = sensor_data[self.data.INDUCTIVE_DATA]
            self.data.set_inductive(inductive)
            time.sleep(0.05)
