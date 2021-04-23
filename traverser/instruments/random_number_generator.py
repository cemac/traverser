# -*- coding: utf-8 -*-
"""
random_number_gerator test instrument
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
        self.name = 'Random Number Generator'

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
        val_ids = ['random_number']
        val_units = ['']
        # If not connected:
        if not self.connected:
            # No values and an error message:
            val_values = [None]
            err_msg = ['Device not connected']
        else:
            # Get values:
            val_values = [random.randint(0, 1000)]
            err_msg = [False]
        # Return the result:
        return {
            'ids': val_ids,
            'values': val_values,
            'units': val_units,
            'error': err_msg
        }
