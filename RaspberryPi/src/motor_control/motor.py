'''
- script used to test individual motors
- used for debugging
- author ****
'''

import smbus

BUS = smbus.SMBus(1)
ADDRESS = 0x04
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
    BUS.write_i2c_block_data(ADDRESS, 0, [cmd_byte, pwr])

def write(value):
    """
    Write data to bus
    """
    BUS.write_byte_data(ADDRESS, 0x00, value)

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
