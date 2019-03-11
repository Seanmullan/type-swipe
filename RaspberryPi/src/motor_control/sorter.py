"""
Moves the sorter to the correct position based on the classification of the incoming object.
"""

import threading
import time
import data
import motor
import object_type
import enum as Enum

class Sorter(threading.Thread):
    """
    Dequeue's the next object from the classified queue, and moves the sorter to the correct
    position based on the classification. The sorter will wait until the current object has
    been sorted before moving to the next object in the classified queue.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.vertical_motor = 1
        self.rotational_motor = 2
        self.vertical_pos = Vertical.up
        self.rotational_pos = Rotation.left
        # Plastic is right, metal is left

    def run(self):
        """
        If the run_system flag is set, get the next item from the classified queue, sort it by
        moving sorter to correct position, then wait until it falls into the bin before getting
        the next item.
        """
        while self.data.get_run_system():
            if not self.classification_queue_empty():
                current_class = self.data.dequeue_classified_queue()
                self.sort_object(current_class)
                # Wait for time perioud or check weight/light sensors before continuing
                time.sleep(10)
        self.set_idle_pos()

    def set_idle_pos(self):
        t0 = threading.Thread(name="Vertical Motor", target=self.vertical_move(Vertical.up))
        t1 = threading.Thread(name="Rotational Motor", target=self.rotational_motor(Rotation.left))
        t0.start()
        t1.start()
        t0.join()
        t1.join()

    def sort_object(self, current_class):
        """
        Moves sorter into the correct position based on the object classification
        """
        if current_class == ObjectType.glass:
            if self.vertical_pos == Vertical.down:
                t0 = threading.Thread(name="Vertical Motor", target=self.vertical_move(Vertical.up))
                t0.start()

        elif current_class == ObjectType.plastic:
            if self.vertical_pos == Vertical.up:
                t0 = threading.Thread(name="Vertical Motor", target=self.vertical_move(Vertical.down))
                t0.start()
            if self.rotational_pos == Rotation.left:
                t1 = threading.Thread(name="Rotational Motor", target=self.rotational_motor(Rotation.right))
                t1.start()

        elif current_class == ObjectType.metal:
            if self.vertical_pos == Vertical.up:
                t0 = threading.Thread(name="Vertical Motor", target=self.vertical_move(Vertical.down))
                t0.start()
            if self.rotational_pos == Rotation.right:
                t1 = threading.Thread(name="Rotational Motor", target=self.rotational_motor(Rotation.left))
                t1.start()

    def vertical_move(self, direction):
        inital_time = time.time()
        if direction == Vertical.up:
            while time.time() - inital_time < 1:
                # Move motor up
                pass
            self.vertical_pos = Vertical.up
        else:
            while time.time() - inital_time < 1:
                # Move motor down
                pass
            self.vertical_pos = Vertical.down

    def rotational_move(self, direction):
        inital_time = time.time()
        if direction == Rotation.left:
            while time.time() - inital_time < 1:
                # Move motor left
                pass
            self.rotational_pos = Rotation.left
        else:
            while time.time() - inital_time < 1:
                # Move motor right
                pass
            self.rotational_pos = Rotation.right

class Vertical(Enum):
    up = 0
    down = 1

class Rotation(Enum):
    left = 0
    right = 1

    
        
