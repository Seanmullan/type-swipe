'''
Controls the conveyor belt
'''

import motor
import data

class Conveyor(object):
    '''
    Contains methods to set the speed and stop the conveyor belt
    '''

    def __init__(self):
        self.id_motor_front = data.Data.ENTRANCE_MOTOR
        self.id_motor_back = data.Data.EXIT_MOTOR

    def set_belt_speed(self, speed):
        '''
        Sets the speed of the front and back motors of the conveyor belt
        '''
        motor.motor_move(self.id_motor_front, speed)
        motor.motor_move(self.id_motor_back, speed)

    def stop_belt(self):
        '''
        Stops the front and back motors of the conveyor belt
        '''
        motor.stop_motors()
