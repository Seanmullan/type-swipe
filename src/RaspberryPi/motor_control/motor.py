'''
- script used to test individual motors
- used for debugging
- author ****
'''

import smbus2

BUS = smbus2.SMBus(1)
MOTOR_ADDRESS = 0x04
ENCODER_ADDRESS = 0x05
MOVEMENT = ''
#---------------------------------------------------------------------------
#                              Useful functions
#---------------------------------------------------------------------------

# Writing to motorboard
def motor_move(motor_id, power):
    """
    Smooth control of the motors
    Mode 2 is Forward.
    Mode 3 is Backwards.
    """
    mode = 2 if power >= 0 else 3
    cmd_byte = motor_id << 5 | 24 | mode << 1
    pwr = int(abs(power) * 2.55)
    BUS.write_i2c_block_data(MOTOR_ADDRESS, 0, [cmd_byte, pwr])

def get_motor_position(motor_id):
    msg = smbus2.i2c_msg.read(ENCODER_ADDRESS, 6)
    BUS.i2c_rdwr(msg)
    position = list(msg)[motor_id]
    if position >= 128:
        position -= 256
    return abs(position)

def write(value):
    """
    Write data to bus
    """
    BUS.write_byte_data(MOTOR_ADDRESS, 0x00, value)


def stop_motor(motor_id):
    """
    Mode 0 floats the motor.
    """
    direction = 0
    byte1 = motor_id << 5 | 16 | direction << 1
    write(byte1)


def stop_motors():
    """
    The motor board stops all motors if bit 0 is high.
    """
    write(0x01)
