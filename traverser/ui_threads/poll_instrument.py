# -*- coding: utf-8 -*-
"""
Instrument polling QThread
"""

# Standard lib imports:
import time
# Third party imports:
from PyQt5.QtCore import QThread
# Package imports:
from traverser.ui_functions.instrument_functions import update_instrument

class PollInstrument(QThread):
    """
    Qthread class used for polling instrument
    """
    def __init__(self, ui, config, config_value, poll_int=1.0):
        # Qthread init:
        QThread.__init__(self)
        # Store self properties ... ui:
        self.ui = ui
        # Polling interval:
        self.poll_int = poll_int
        # Config and value which might change during run time:
        self.config = config
        self.config_value = config_value

    def run(self):
        """
        The run method loops forever, updating information at the requested
        interval.
        """
        while True:
            # Check polling interval for changes:
            config_int = self.config.values[self.config_value]
            if config_int != self.poll_int:
                self.poll_int = config_int
            update_instrument(self.ui)
            time.sleep(self.poll_int)
