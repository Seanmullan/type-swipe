"""
Moves the sorter to the correct position based on the classification of the incoming object.
"""

import threading
import data

class Sorter(threading.Thread):
    """
    Dequeue's the next object from the classified queue, and moves the sorter to the correct
    position based on the classification. The sorter will wait until the current object has
    been sorted before moving to the next object in the classified queue.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()

    def run(self):
        """
        If the run_system flag is set, get the next item from the classified queue, sort it by
        moving sorter to correct position, then wait until it falls into the bin before getting
        the next item.
        """
        while True:
            if self.data.get_run_system():
                current_class = self.data.dequeue_classified_queue()
                self.sort_object(current_class)
                # Wait for time perioud or check weight/light sensors before continuing

    def sort_object(self, current_class):
        """
        Moves sorter into the correct position based on the object classification
        """
        pass
