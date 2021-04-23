# -*- coding: utf-8 -*-
"""
random environment data generator test instrument
"""

# Standard lib imports:
import random
# Package imports:
from traverser.instruments.instrument import Instrument

class TraverserInstrument(Instrument):
    """
    Random number generator test instrument
    """
    def __init__(self):
        # Run parent init first:
        super().__init__()
        # Instrument name:
        self.name = 'Environment Sensor'

    def connect(self):
        """
        Connect to instrument
        """
        self.connected = True
        return True, 'Connected {0}'.format(self.name)

    def disconnect(self):
        """
        Disconnect from instrument
        """
        self.connected = False
        return True, 'Disconnected {0}'.format(self.name)

    def status(self):
        """
        Return current status
        """
        return True, None

    def acquire(self):
        """
        Return instrument values
        """
        # Return value ids and units:
        val_ids = ['temperature', 'humidity']
        val_units = ['C', '%']
        # If not connected:
        if not self.connected:
            # No values and an error message:
            val_values = [None, None]
            err_msg = ['Device not connected'] * 2
        else:
            # Get values:
            val_values = [random.randint(5, 35), random.randint(0, 100)]
            err_msg = [False] * 2
        # Return the result:
        return {
            'ids': val_ids,
            'values': val_values,
            'units': val_units,
            'error': err_msg
        }
