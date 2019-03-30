import threading
import time
import data

class Weight(threading.Thread):

    def __init__(self, io):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.get_sensors = io.interface_kit.getSensors

    def run(self):
        """
        Reads weight sensor data from phidget board and updates
        data class.
        """
        while not self.data.get_shut_down():
            sensor_data = self.get_sensors()

            # Get bin weight sensors
            glass   = float(sensor_data[self.data.GLASS_BIN])
            plastic = float(sensor_data[self.data.PLASTIC_BIN])
            metal   = float(sensor_data[self.data.METAL_BIN])
            bins    = [glass, plastic, metal]
            
            # Get conveyor belt weight
            conveyor = float(sensor_data[self.data.CONVEYOR_WEIGHT])

            # Update data class
            self.data.set_bin_weights(bins)
            self.data.set_conveyor_weight(conveyor)
            time.sleep(0.05)
