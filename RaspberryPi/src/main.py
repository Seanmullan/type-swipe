"""
Acts as a Sandbox simulator. Used to test logic flow of program. To run the self-test,
use 'python main.py --test'.
"""

import threading
import time
import simulate_io
import toddler
import data
import sys
sys.path.append('tests/')
import traceback

class Main(object):
    """
    This class initialises a fake IO class and starts threads to call Toddler methods
    """

    def __init__(self):
        self.__io = simulate_io.IOTools()
        self.__toddler = toddler.Toddler(self.__io)
        self.__data = data.Data()
        self.__control_stop_event = threading.Event()
        self.__vision_stop_event = threading.Event()

        def toddler_control():
            """
            Invokes Toddler control method
            """
            # Allow time for sensor data to initialise
            #time.sleep(0.5)
            while 1:
                #print("running toddler_control in main")
                self.__toddler.control()

        def toddler_vision():
            """
            Invokes Toddler vision method
            """
            while 1:
                #print("running toddler vision in main")
                self.__toddler.vision()

        def self_test():
            """
            Simulates objects passing through proximity and inductive sensors
            """
            import example_test

            import second_test

            self.destroy()

        self.__toddler_control = threading.Thread(name="control", target=toddler_control)
        self.__toddler_vision = threading.Thread(target=toddler_vision)
        self.__self_test = threading.Thread(name="test",target=self_test)
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
        print(threading.enumerate())
        self.__toddler.preprocessor.stop()
        self.__toddler.preprocessor.join()
        print(threading.enumerate())

        

if __name__ == '__main__':
    MAIN = Main()
