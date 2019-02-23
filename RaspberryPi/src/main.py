"""
Acts as a Sandbox simulator. Used to test logic flow of program
"""

import threading
import simulate_io
import toddler
import data
import time

class Main(object):
    """
    This class initialises a fake IO class and starts threads to call Toddler methods
    """

    def __init__(self):
        self.__io = simulate_io.IOTools()
        self.__toddler = toddler.Toddler(self.__io)
        self.__data = data.Data()

        def toddler_control():
            """
            Invokes Toddler control method
            """
            # Allow time for sensor data to initialise
            time.sleep(1)
            while 1:
                self.__toddler.control()

        def toddler_vision():
            """
            Invokes Toddler vision method
            """
            while 1:
                self.__toddler.vision()

        def self_test():
            self.__data.set_proximity(15)
            self.__data.set_inductive(1000)
            time.sleep(2)
            self.__data.set_proximity(10)
            self.__data.set_inductive(100)
            time.sleep(2)
            self.__data.set_proximity(15)
            self.__data.set_inductive(1000)
            time.sleep(2)
            self.__data.set_proximity(10)
            self.__data.set_inductive(1000)
            time.sleep(2)

        self.__toddler_control = threading.Thread(target=toddler_control)
        self.__toddler_vision = threading.Thread(target=toddler_vision)
        self.__self_test = threading.Thread(target=self_test)
        self.start_threads()

    def start_threads(self):
        """
        Start control and vision threads
        """
        self.__toddler_control.start()
        self.__toddler_vision.start()
        self.__self_test.start()

    def destroy(self):
        """
        Join threads
        """
        self.__toddler_control.join()
        self.__toddler_vision.join()
        self.__self_test.join()

if __name__ == '__main__':
    MAIN = Main()
