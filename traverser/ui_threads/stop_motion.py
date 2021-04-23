# -*- coding: utf-8 -*-
"""
Motion stopping QThread
"""

# Third party imports:
from PyQt5.QtCore import QThread, pyqtSignal
# Package imports:
from traverser.ui_functions.motion_control_functions import stop_it

class StopMotion(QThread):
    """
    Qthread class used for stopping VixIM motion
    """
    # Define signals used to stop and start other threads:
    stop_thread = pyqtSignal(str, bool)
    start_thread = pyqtSignal(str)

    def __init__(self, ui):
        # Qthread init:
        QThread.__init__(self)
        # Store self properties ... ui:
        self.ui = ui

    def stop_it(self):
        """
        Run function just stops the ViXIM motors
        """
        # Stop it:
        stop_it(self, self.ui)
