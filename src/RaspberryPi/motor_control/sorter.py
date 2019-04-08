"""
Moves the sorter to the correct position based on the classification of the incoming object.
"""

import threading
import time
import data
import motor
import item_type
import item
import json
import conveyor

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
        self.vertical_motor = self.data.VERTICAL_MOTOR
        self.rotational_motor = self.data.ROTATION_MOTOR
        self.vertical_pos = Vertical.UP
        self.rotational_pos = Rotation.ANTI_CLOCKWISE
        self.current_class = -1

        # Define weight change thresholds for bin weight sensors
        self.glass_bin_threshold = 300
        self.plastic_bin_threshold = 100
        self.metal_bin_threshold = 250

        # Indexes for bin sensor readings array
        self.glass_index = 0
        self.plastic_index = 1
        self.metal_index = 2

        # Define speeds for sorter motors and thresholds for rotary encoders
        self.vertical_speed = -80
        self.rotational_speed = 80
        self.vertical_clicks_thresh = 80000
        self.rotational_clicks_thresh = 40000

        # Start thread for rotary encoders
        self.thread_encoder = threading.Thread(name="get_encoder", target=self.get_encoders)
        self.thread_encoder_event = threading.Event()
        self.thread_encoder.start()

        # Timeout for motors and bins
        self.timeout_vertical = 2
        self.timeout_rotation = 1.5
        self.timeout_bins = 10

    def run(self):
        """
        If the run_system flag is set, get the next item from the classified queue, sort it by
        moving sorter to correct position, then wait until it falls into the bin before getting
        the next item.
        """
        while not self.data.get_shut_down():
            while self.data.get_run_system():
                if not self.data.classification_queue_empty():
                    
                    # Retrieve item data
                    item_data      = self.data.dequeue_classified_queue()
                    object_id      = item_data.get_item_id()
                    current_class  = item_data.get_final_classification()
                    image_path     = item_data.get_image_path()
                    image_name     = item_data.get_image_name()
                    weight_reading = item_data.get_item_weight() 
                    
                    print "[SORTER] Sorting ", str(current_class)
                    self.sort_object(current_class)
                    
                    #Check weight sensors before continuing
                    self.check_bin_weights()

                    # Save item data to CSV and upload item data to database
                    item_data.save_data_to_file()
                    self.upload_to_database(object_id, current_class, image_path, image_name, weight_reading)
                    time.sleep(5)
                time.sleep(0.2)
            time.sleep(0.2)
        
        print "[SORTER] Exiting sorter"
        self.set_idle_pos()

    def set_idle_pos(self):
        """
        Set the sorting plane to the default position (UP and ANTI_CLOCKWISE)
        """
        self.move_sorter(Vertical.UP, Rotation.ANTI_CLOCKWISE)
        self.thread_encoder_event.set()

    def sort_object(self, current_class):
        """
        Moves sorter into the correct position based on the object classification
        """
        if current_class == item_type.ItemType.glass:
            self.move_sorter(Vertical.UP, None)

        elif current_class == item_type.ItemType.plastic:
            self.move_sorter(Vertical.DOWN, Rotation.CLOCKWISE)

        elif current_class == item_type.ItemType.metal:
            self.move_sorter(Vertical.DOWN, Rotation.ANTI_CLOCKWISE)

    def move_sorter(self, vertical_direction, rotation_direction):
        """
        Sets each of the vertical and rotational motors. Each motor spins until the click thresholds
        for each motor are surpassed. If I2C error occurs, reset the sorting arm. 
        Allow motors to move until either rotary encoder clicks threshold is exceeded or motor
        motor timeouts are exceeded.
        """
        vertical_clicks = 0
        rotational_clicks = 0
        initial_time = time.time()
        vertical_moving = self.move_vertical(vertical_direction)
        rotation_moving = self.move_rotational(rotation_direction)

        while (vertical_moving or rotation_moving):
            if (vertical_clicks < self.vertical_clicks_thresh and vertical_moving == True):
                vertical_clicks += self.data.get_vertical_position()
            else:
                vertical_moving = False
                try:
                    motor.stop_motor(self.vertical_motor)
                except:
                    print "[SORTER] I2C Error: Stop vertical motor"
                    self.reset_sorter()

            if (rotational_clicks < self.rotational_clicks_thresh and rotation_moving == True):
                rotational_clicks += self.data.get_rotation_position()
            else:
                rotation_moving = False
                try:
                    motor.stop_motor(self.rotational_motor)
                except:
                    print "[SORTER] I2C Error: Stop rotational motor"
                    self.reset_sorter()

            if time.time() - initial_time > self.timeout_vertical:
                vertical_moving = False
                try:
                    motor.stop_motor(self.vertical_motor)
                except:
                    print "[SORTER] I2C Error: Stop vertical motor"
                    self.reset_sorter()

            if time.time() - initial_time > self.timeout_rotation:
                rotation_moving = False
                try:
                    motor.stop_motor(self.rotational_motor)
                except:
                    print "[SORTER] I2C Error: Stop rotational motor"
                    self.reset_sorter()

        motor.stop_motor(self.vertical_motor)
        motor.stop_motor(self.rotational_motor)

        self.set_motor_positions(vertical_direction, rotation_direction)

    def move_vertical(self, vertical_direction):
        """
        Determine if vertical motor should move, and if so engage motor in appropriate direction.
        Return True if motor is engaged, false otherwise.
        """
        if vertical_direction == Vertical.UP:
            if self.vertical_pos == Vertical.DOWN:
                try:
                    print "[SORTER] Moving vertical up"
                    motor.motor_move(self.vertical_motor, self.vertical_speed)
                    return True
                except:
                    print "[SORTER] I2C Error: Vertical up"
            else:
                return False

        elif vertical_direction == Vertical.DOWN:
            if self.vertical_pos == Vertical.UP:
                try:
                    print "[SORTER] Moving vertical down"
                    motor.motor_move(self.vertical_motor, -self.vertical_speed)
                    return True
                except:
                    print "[SORTER] I2C Error: Vertical down"
            else:
                return False

        else:
            return False

    def move_rotational(self, rotation_direction):
        """
        Determine if rotational motor should move, and if so engage motor in appropriate direction.
        Return True if motor is engaged, false otherwise.
        """
        if rotation_direction == Rotation.ANTI_CLOCKWISE:
            if self.rotational_pos == Rotation.CLOCKWISE:
                try:
                    print "[SORTER] Moving rotational anti-clockwise"
                    motor.motor_move(self.rotational_motor, self.rotational_speed)
                    return True
                except:
                    print "[SORTER] I2C Error: Rotation anti-clockwise"
            else:
                return False

        elif rotation_direction == Rotation.CLOCKWISE:
            if self.rotational_pos == Rotation.ANTI_CLOCKWISE:
                try:
                    print "[SORTER] Moving rotational clockwise"
                    motor.motor_move(self.rotational_motor, -self.rotational_speed)
                    return True
                except:
                    print "[SORTER] I2C Error: Rotation clockwise"
            else:
                return False

        else:
            return False

    def set_motor_positions(self, vertical_direction, rotation_direction):
        """
        Sets current positions of vertical and rotational motors.
        """
        if vertical_direction == Vertical.UP:
            self.vertical_pos = Vertical.UP
        elif vertical_direction == Vertical.DOWN:
            self.vertical_pos = Vertical.DOWN
        else:
            pass

        if rotation_direction == Rotation.ANTI_CLOCKWISE:
            self.rotational_pos = Rotation.ANTI_CLOCKWISE
        elif rotation_direction == Rotation.CLOCKWISE:
            self.rotational_pos = Rotation.CLOCKWISE
        else:
            pass

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
        Continually computes the change in the bin weight sensors until one of the weight sensors
        changes by more than its weight change threshold. This informs the system which bin the
        object fell in to. If the timeout is exceed, then it is likely that the item is stuck.
        In this case, sound the buzzer and reset the sorting arm.
        """
        initial_time = time.time()
        initial_bin_weights = self.data.get_bin_weights()
        glass_bin   = initial_bin_weights[self.glass_index]
        plastic_bin = initial_bin_weights[self.plastic_index]
        metal_bin   = initial_bin_weights[self.metal_bin]
        weight_changed = False

        while not weight_changed:
            if time.time() - initial_time > self.timeout_bins:
                print "[SORTER] Bin timeout exceeded"
                self.sound_buzzer()
                self.data.set_shut_down(True)
                break
        
            new_bin_weights = self.data.get_bin_weights()
            bin = ""

            if abs(glass_bin - new_bin_weights[self.glass_index]) > self.glass_bin_threshold:
                if self.current_class != item_type.ItemType.glass:
                    print "[SORTER] Incorrectly sorted as glass. Expected: ", self.current_class
                    self.sound_buzzer()
                    self.reset_sorter()
                else:
                    print "[SORTER] Item sorted as glass"
                weight_changed = True
                bin = "glass"
            
            elif abs(plastic_bin - new_bin_weights[self.plastic_index]) > self.plastic_bin_threshold:
                if self.current_class != item_type.ItemType.plastic:
                    print "[SORTER] Incorrectly sorted as plastic. Expected: ", self.current_class
                    self.sound_buzzer()
                    self.reset_sorter()
                else:
                    print "[SORTER] Item sorted as plastic"
                weight_changed = True
                bin = "plastic"
    
            elif abs(metal_bin - new_bin_weights[self.metal_index]) > self.metal_bin_threshold:
                if self.current_class != item_type.ItemType.metal:
                    print "[SORTER] Incorrectly sorted as metal. Expected: ", self.current_class
                    self.sound_buzzer()
                    self.reset_sorter()
                else:
                    print "[SORTER] Item sorted as metal"
                weight_changed = True
                bin = "metal"

            else:
                time.sleep(0.05)

    def upload_to_database(self, object_id, current_class, image_path, image_name, weight_reading):
        """
        Starts threads to upload item data to the database, including the object ID,
        its classification, and the photo of the item.
        """
        thread_upload_data = threading.Thread(
            name="upload_data", 
            target=self.data.insert_data_to_database,
            args=[object_id, current_class, weight_reading]
        )
        thread_upload_image = threading.Thread(
            name="upload_image",
            target=self.data.upload_image_to_cloud,
            args=["collecteddataset", image_path, "images/"+image_name]
        )
        thread_upload_data.start()
        thread_upload_image.start()

    def reset_sorter(self):
        """
        In the case of an I2C error or an item getting stuck, this function temporarily
        stops the conveyor belt and resets the sorting arm to its original position.
        """
        # Stop conveyor belt
        motor.stop_motor(self.data.ENTRANCE_MOTOR_INDUCTIVE_PWR)
        motor.stop_motor(self.data.EXIT_MOTOR)

        # Force sorting arm to original position by ignoring current position
        motor.motor_move(self.rotational_motor, self.rotational_speed)
        motor.motor_move(self.vertical_motor, self.vertical_speed)
        time.sleep(2)
        motor.stop_motor(self.vertical_motor)
        motor.stop_motor(self.rotational_motor)
        self.vertical_pos = Vertical.UP
        self.rotational_pos = Rotation.ANTI_CLOCKWISE

        # Restart conveyor belt
        motor.motor_move(self.data.ENTRANCE_MOTOR_INDUCTIVE_PWR, 70)
        motor.motor_move(self.data.EXIT_MOTOR, 70)

    def sound_buzzer(self):
        """
        Starts a thread to sound the buzzer.
        """
        print "[SORTER] Sounding buzzer"
        buzzer = threading.Thread(name="buzzer", target=self.thread_buzzer)
        buzzer.start()
    
    def thread_buzzer(self):
        """
        Engages motor board to sound buzzer for 2 seconds.
        """
        motor.motor_move(self.data.BUZZER, 100)
        time.sleep(2)
        motor.stop_motor(self.data.BUZZER)

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
