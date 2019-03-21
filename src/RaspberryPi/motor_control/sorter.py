"""
Moves the sorter to the correct position based on the classification of the incoming object.
"""

import threading
import time
import data
import motor
import object_type

class Sorter(threading.Thread):
    """
    Dequeue's the next object from the classified queue, and moves the sorter to the correct
    position based on the classification. The sorter will wait until the current object has
    been sorted before moving to the next object in the classified queue.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.vertical_motor = 3
        self.rotational_motor = 5
        self.vertical_pos = Vertical.up
        self.rotational_pos = Rotation.left
        # Plastic is right, metal is left

        self.vertical_speed = 100
        self.rotational_speed = 100
        self.vertical_clicks_thresh = 500
        self.rotational_clicks_thresh = 500

    def run(self):
        """
        If the run_system flag is set, get the next item from the classified queue, sort it by
        moving sorter to correct position, then wait until it falls into the bin before getting
        the next item.
        """
        while self.data.get_run_system():
            if not self.data.classification_queue_empty():
                current_class = self.data.dequeue_classified_queue()
                print "Sorting ", str(current_class)
                self.sort_object(current_class)
                # Wait for time period or check weight sensors before continuing
                time.sleep(0.1)
        
        self.set_idle_pos()

    def set_idle_pos(self):
        """
        Set the sorting plane to the default position (Up and left)
        """
        self.move_swiper(Vertical.up, Rotation.left)

    def sort_object(self, current_class):
        """
        Moves sorter into the correct position based on the object classification
        """
        if current_class == object_type.ObjectType.glass:
            self.move_swiper(Vertical.up, None)

        elif current_class == object_type.ObjectType.plastic:
            self.move_swiper(Vertical.down, Rotation.right)

        elif current_class == object_type.ObjectType.metal:
            self.move_swiper(Vertical.down, Rotation.left)

    def move_swiper(self, vertical_direction, rotation_direction):
        """
        Sets each of the vertical and rotational motors. Each motor spins until the click thresholds
        for each motor are surpassed.
        """
        vertical_clicks = 0
        rotational_clicks = 0

        vertical_reading_count = 0
        rotational_reading_count = 0

        while (vertical_clicks < self.vertical_clicks_thresh and rotational_clicks < self.rotational_clicks_thresh):
            
            # If there is a vertical movement
            if not vertical_direction == None:
                self.vertical_move(vertical_direction)
                if (vertical_clicks < self.vertical_clicks_thresh):
                    # Ignore first two readings
                    if vertical_reading_count > 2:
                        vertical_clicks += motor.get_motor_position(self.vertical_motor)
                    vertical_reading_count += 1
                    time.sleep(0.1)
                else:
                    motor.stop_motor(self.vertical_motor)
            else:
                vertical_clicks = self.vertical_clicks_thresh

            # If there is a rotational movement
            if not rotation_direction == None:
                self.rotational_move(rotation_direction)
                if (rotational_clicks < self.rotational_clicks_thresh):
                    # Ignore first two readings
                    if rotational_reading_count > 2:
                        rotational_clicks += motor.get_motor_position(self.rotational_motor)
                    rotational_reading_count += 1
                    time.sleep(0.1)
                else:
                    motor.stop_motor(self.rotational_motor)
            else:
                rotational_clicks = self.rotational_clicks_thresh

        motor.stop_motor(self.vertical_motor)
        motor.stop_motor(self.rotational_motor)

        # Set motor positions
        self.vertical_pos = Vertical.up if vertical_direction == Vertical.up else Vertical.down
        self.rotational_pos = Rotation.left if rotation_direction == Rotation.left else Rotation.right
        
    def vertical_move(self, direction):
        """
        Moves vertical motor
        """
        if direction == Vertical.up:
            if self.vertical_pos == Vertical.down:
                motor.motor_move(self.vertical_motor, self.vertical_speed)
        else:
            if self.vertical_pos == Vertical.up:
                motor.motor_move(self.vertical_motor, -self.vertical_speed)
    
    def rotational_move(self, direction):
        """
        Moves rotational motor
        """
        if direction == Rotation.left:
            if self.rotational_pos == Rotation.right:
                motor.motor_move(self.rotational_motor, self.rotational_speed)
        else:
            if self.rotational_pos == Rotation.left:
                motor.motor_move(self.rotational_motor, -self.rotational_speed)


class Vertical(object):
    up = 0
    down = 1

class Rotation(object):
    left = 0
    right = 1
