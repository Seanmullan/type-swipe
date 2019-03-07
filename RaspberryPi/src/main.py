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

        self.__toddler_control = threading.Thread(name="control", target=self.toddler_control)
        self.__toddler_vision = threading.Thread(name="vision", target=self.toddler_vision)
        self.__self_test = threading.Thread(name="test", target=self.self_test)
        self.start_threads()

    def toddler_control(self):
        """
        Invokes Toddler control method
        """
        while not self.stopped_control():
            self.__toddler.control()

    def stop_control(self):
        """
        Sets the stop flag for the toddler control thread
        """
        self.__control_stop_event.set()
        self.__toddler.stop_control()

    def stopped_control(self):
        """
        Returns true if the control stop flag is set
        """
        return self.__control_stop_event.is_set()


    def toddler_vision(self):
        """
        Invokes Toddler vision method
        """
        while not self.stopped_vision():
            self.__toddler.vision()

    def stop_vision(self):
        """
        Sets the stop flag for the toddler vision thread
        """
        self.__vision_stop_event.set()

    def stopped_vision(self):
        """
        Returns true if the vision stop flag is set
        """
        return self.__vision_stop_event.is_set()


    def self_test(self):
        """
        Simulates objects passing through proximity and inductive sensors
        """
        import example_test
        import second_test

        self.destroy()

    def start_threads(self):
        """
        Start control and vision threads
        """
        self.__toddler_control.start()
        self.__toddler_vision.start()
        self.__self_test.start()

    def destroy(self):
        """
        Stop threads
        """

        self.__toddler.preprocessor.stop()
        self.stop_vision()
        self.stop_control()
        self.__io.stop_read_data()
        self.__toddler.stop_check_run_system()
        self.__toddler.thread_check_run_system.join()

if __name__ == '__main__':
    MAIN = Main()
