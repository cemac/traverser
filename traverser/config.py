# -*- coding: utf-8 -*-
"""
Traverser configuration class
"""

# Standard lib imports:
import os

class Config(object):
    """
    Traverser configuration
    """
    def __init__(self):
        """
        Init configuration
        """
        # Config values:
        self.values = {
            # Serial port / device:
            'serial_port': '/dev/ttyUSB0',
            # Baud rate:
            'baud_rate': 9600,
            # Serial timeout:
            'timeout': 0.5,
            # Velocity and acceleration values:
            'vel': 2,
            'accel': 10,
            'decel': 10,
            # Assign motor 1 and motor 2 to x and y:
            'x_motor': 1,
            'y_motor': 2,
            # Max X distance:
            'max_x': 2046658,
            # Max Y distance:
            'max_y': 2364810,
            # X distance in x_units:
            'x_dist': 2400,
            # y distance in y_units:
            'y_dist': 2750,
            # X distance units:
            'x_units': 'mm',
            # Y distance units:
            'y_units': 'mm',
            # Instrument poll interval (in seconds):
            'poll_instrument': 1.0
        }
        # Default configuration file location:
        self.default_config = os.sep.join([os.path.expanduser('~'),
                                           '.traverser.ini'])
        # Values which can be set in configuration:
        self.config_values = list(self.values.keys())
