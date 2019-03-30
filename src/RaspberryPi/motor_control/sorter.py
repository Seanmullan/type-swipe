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
    been sorted before moving to the next object in the classified queue. Note: Metal is
    ANTI_CLOCKWISE, plastic is CLOCKWISE.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = data.Data()
        self.vertical_motor = 3
        self.rotational_motor = 5
        self.vertical_pos = Vertical.UP
        self.rotational_pos = Rotation.ANTI_CLOCKWISE

        self.current_class = -1
        self.bin_threshold = 200

        self.glass_index = 0
        self.plastic_index = 1
        self.metal_index = 2

        bins = self.data.get_bin_weights()
        self.plastic_bin = bins[self.plastic_index]
        self.metal_bin = bins[self.metal_index]
        self.glass_bin = bins[self.glass_index]

        self.vertical_speed = -100
        self.rotational_speed = 100
        self.vertical_clicks_thresh = 40000
        self.rotational_clicks_thresh = 500

        self.thread_encoder = threading.Thread(name="get_encoder", target=self.get_encoders)
        self.thread_encoder_event = threading.Event()
        self.thread_encoder.start()

        # Timeout for motors. Might not neeed this.
        self.timeout = 2

    def run(self):
        """
        If the run_system flag is set, get the next item from the classified queue, sort it by
        moving sorter to correct position, then wait until it falls into the bin before getting
        the next item.
        """
        while not self.data.get_shut_down():
            while self.data.get_run_system():
                if not self.data.classification_queue_empty():
                    self.current_class = self.data.dequeue_classified_queue()
                    print "Sorting ", str(self.current_class)
                    self.sort_object(self.current_class)
                    
                    #Check weight sensors before continuing
                    #self.check_bin_weights()
                    time.sleep(0.1)
                time.sleep(0.2)
            time.sleep(0.2)
        
        
        print "Exiting sorter"
        self.set_idle_pos()

    def set_idle_pos(self):
        """
        Set the sorting plane to the default position (UP and ANTI_CLOCKWISE)
        """
        self.move_swiper(Vertical.UP, Rotation.ANTI_CLOCKWISE)
        self.thread_encoder_event.set()

    def sort_object(self, current_class):
        """
        Moves sorter into the correct position based on the object classification
        """
        if current_class == object_type.ObjectType.glass:
            self.move_swiper(Vertical.UP, None)

        elif current_class == object_type.ObjectType.plastic:
            self.move_swiper(Vertical.DOWN, Rotation.CLOCKWISE)

        elif current_class == object_type.ObjectType.metal:
            self.move_swiper(Vertical.DOWN, Rotation.ANTI_CLOCKWISE)

    def move_swiper(self, vertical_direction, rotation_direction):
        """
        Sets each of the vertical and rotational motors. Each motor spins until the click thresholds
        for each motor are surpassed.
        """
        vertical_moving = True
        rotation_moving = True

        vertical_clicks = 0
        rotational_clicks = 0

        # TIMEOUT
        initial_time = time.time()

        # VERTICAL MOTOR
        if vertical_direction == Vertical.UP:
            if self.vertical_pos == Vertical.DOWN:
                try:
                    motor.motor_move(self.vertical_motor, self.vertical_speed)
                except:
                    print "I2C Error"
            else:
                vertical_moving = False
        elif vertical_direction == Vertical.DOWN:
            if self.vertical_pos == Vertical.UP:
                try:
                    motor.motor_move(self.vertical_motor, -self.vertical_speed)
                except:
                    print "I2C Error"
            else:
                vertical_moving = False
        else:
            vertical_moving = False

        # ROTATIONAL MOTOR
        if rotation_direction == Rotation.ANTI_CLOCKWISE:
            if self.rotational_pos == Rotation.CLOCKWISE:
                try:
                    motor.motor_move(self.rotational_motor, self.rotational_speed)
                except:
                    print "I2C Error"
            else:
                rotation_moving = False
        elif rotation_direction == Rotation.CLOCKWISE:
            if self.rotational_pos == Rotation.ANTI_CLOCKWISE:
                try:
                    motor.motor_move(self.rotational_motor, -self.rotational_speed)
                except:
                    print "I2C Error"
            else:
                rotation_moving = False
        else:
            rotation_moving = False

        # COUNT CLICKS
        while (vertical_moving or rotation_moving):
            if (vertical_clicks < self.vertical_clicks_thresh):
                vertical_clicks += self.data.get_vertical_position()
            else:
                vertical_moving = False
                try:
                    motor.stop_motor(self.vertical_motor)
                except:
                    print "I2C Error"

            if (rotational_clicks < self.rotational_clicks_thresh):
                rotational_clicks += self.data.get_rotation_position()
            else:
                rotation_moving = False
                try:
                    motor.stop_motor(self.rotational_motor)
                except:
                    print "I2C Error"

            if time.time() - initial_time > self.timeout:
                print "Sorter timeout exceeded"
                break

            print "Vertical clicks: ", vertical_clicks
            print "Rotation clicks: ", rotational_clicks 

        # Shouldnt need these
        motor.stop_motor(self.vertical_motor)
        motor.stop_motor(self.rotational_motor)

        # Set motor positions
        self.vertical_pos = Vertical.UP if vertical_direction == Vertical.UP else Vertical.DOWN
        self.rotational_pos = Rotation.ANTI_CLOCKWISE if rotation_direction == Rotation.ANTI_CLOCKWISE else Rotation.CLOCKWISE

    def get_encoders(self):
        """
        Reads vertical and rotational motor positions from encoder board
        """
        while not self.thread_encoder_event.is_set():
            self.data.set_vertical_position(motor.get_motor_position(self.vertical_motor))
            self.data.set_rotation_position(motor.get_motor_position(self.rotational_motor))
            time.sleep(0.02)

    def check_bin_weights(self):
        """
        Checks the bins weight sensors and checks for 
        correct classification and bin type
        """
        initial_bin_weights = self.data.get_bin_weights()

        glass_bin   = initial_bin_weights[self.glass_index]
        plastic_bin = initial_bin_weights[self.plastic_index]
        metal_bin   = initial_bin_weights[self.metal_bin]

        weight_changed = False

        while not weight_changed:
            new_bin_weights = self.data.get_bin_weights()
            
            if abs(glass_bin - new_bin_weights[self.glass_index]) > self.bin_threshold:
                if self.current_class != object_type.ObjectType.glass:
                    print "Incorrectly sorted as glass. Expected: ", self.current_class
                    # sound buzzer
                else:
                    print "Item sorted as glass"
                weight_changed = True
            
            elif abs(plastic_bin - new_bin_weights[self.plastic_index]) > self.bin_threshold:
                if self.current_class != object_type.ObjectType.plastic:
                    print "Incorrectly sorted as plastic. Expected: ", self.current_class
                    # sound buzzer
                else:
                    print "Item sorted as plastic"
                weight_changed = True
            
            elif abs(metal_bin - new_bin_weights[self.metal_index]) > self.bin_threshold:
                if self.current_class != object_type.ObjectType.metal:
                    print "Incorrectly sorted as metal. Expected: ", self.current_class
                    # sound buzzer
                else:
                    print "Item sorted as metal"
                weight_changed = True
            else:
                time.sleep(0.05)

class Vertical(object):
    """
    Defines positions for the vertical motor
    """
    UP = 0
    DOWN = 1

class Rotation(object):
    """
    Defines positions for the rotational motor
    """
    ANTI_CLOCKWISE = 0
    CLOCKWISE = 1
