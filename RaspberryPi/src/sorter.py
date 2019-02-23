import threading
import data

class Sorter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.current_classification = ""

    def run(self):
        while True:
            if self.data.get_run_system():
                current_class = self.data.dequeue_classified_queue()
                self.sort_object(current_class)
                # TODO: Wait for some period of time or check weight/light sensors
                # before getting next class

    def sort_object(self, current_class):
        # Do stuff with motors
        pass