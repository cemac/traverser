# -*- coding: utf-8 -*-
"""
Traverser instrument base class
"""

class Instrument():
    """
    Traverser instrument

    Bas class for traverser instruments
    """
    def __init__(self):
        # Class properties:
        self.properties = {}
        # Instrument name:
        self.name = None
        # Connected state:
        self.connected = False

    def __repr__(self):
        """
        Representation of the instrument
        """
        rep = '<Traverser instrument: {0}>'.format(self.name)
        return rep

    def __str__(self):
        """
        Printable representation of the instrument
        """
        if self.connected:
            connect_status = 'CONNECTED'
        else:
            connect_status = 'DISCONNECTED'
        rep = 'Traverser {0}, properties : {1}, {2}'.format(
            self.name, self.properties, connect_status
        )
        return rep

    def get_name(self):
        """
        Return the instrument name
        """
        return self.name

    def connect(self):
        """
        connect should perform the connection to the instrument
        """
        pass

    def disconnect(self):
        """
        disconnect should disconnect from the instrument
        """
        pass

    def status(self):
        """
        status should return connection status (True / False)
        """
        pass

    def acquire(self):
        """
        acquire should acquire a reading and return a dict of values, where:
          * 'ids' is a list of value names / ids (e.g. 'temperature',
            'humidity')
          * 'values' is a list of returned values
          * 'units' is a list of the units for the values
          * 'error' return False if all good, else return error message
        """
        return {}
