import threading
import serial
import data

class Proximity(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def run(self):
        """
        Reads proximity value over USB port.
        """
        while not self.data.get_shut_down():
            if self.ser.readline() != None:
                try:
                    proxi = int(float(self.ser.readline()))
                    self.data.set_proximity(proxi)
                except ValueError:
                    print "Failed to convert proxi string to int"
