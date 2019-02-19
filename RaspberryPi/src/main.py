"""
Acts as a Sandbox simulator. Used to test logic flow of program
"""

import threading
import simulate_io
import toddler

class Main(object):
    """
    This class initialises a fake IO class and starts threads to call Toddler methods
    """

    def __init__(self):
        self.__io = simulate_io.IOTools()
        self.__toddler = toddler.Toddler(self.__io)

        def toddler_control():
            """
            Invokes Toddler control method
            """
            while 1:
                self.__toddler.control()

        def toddler_vision():
            """
            Invokes Toddler vision method
            """
            while 1:
                self.__toddler.vision()

        self.__toddler_control = threading.Thread(target=toddler_control)
        self.__toddler_vision = threading.Thread(target=toddler_vision)
        self.start_threads()

    def start_threads(self):
        """
        Start control and vision threads
        """
        self.__toddler_control.start()
        self.__toddler_vision.start()

    def destroy(self):
        """
        Join threads
        """
        self.__toddler_control.join()
        self.__toddler_vision.join()

if __name__ == '__main__':
    MAIN = Main()
