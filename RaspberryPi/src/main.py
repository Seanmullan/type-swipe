import simulateIO
import threading
import toddler

class Main:

    def __init__(self):
        self.__IO = simulateIO.IOTools()
        self.__toddler = toddler.Toddler(self.__IO)
 
        def toddler_control():
            while 1:
                print("toddlercontrol")
                self.__toddler.control()
            
        def toddler_vision():
            while 1:
                print("toddlervision")
                self.__toddler.vision()
 
        self.__toddler_control = threading.Thread(target = toddler_control )
        self.__toddler_vision = threading.Thread(target = toddler_vision)

        self.start_threads()

    def start_threads(self):
        print("Starting threads")
        self.__toddler_control.start()
        self.__toddler_vision.start()

    def destroy(self):
        self.__done = True
        self.__toddler_control.join()
        self.__toddler_vision.join()
        self.__IO.destroy()

if __name__ == '__main__':
    main = Main()
