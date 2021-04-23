# -*- coding: utf-8 -*-
"""
Status polling QThread
"""

# Standard lib imports:
import time
# Third party imports:
from PyQt5.QtCore import QThread, pyqtSignal
# Package imports:
from traverser.ui_functions.status_functions import update_status

class PollStatus(QThread):
    """
    Qthread class used for polling traverse / VixIM status
    """
    # Define signals used to emit instructions to update status and program
    # plots:
    plot_status = pyqtSignal()
    plot_program = pyqtSignal()

    def __init__(self, ui, poll_int=1.0):
        # Qthread init:
        QThread.__init__(self)
        # Store self properties ... ui:
        self.ui = ui
        # Polling interval:
        self.poll_int = poll_int
        # X and Y position, used to determine if plot needs updating:
        self.x_pos = None
        self.y_pos = None

    def run(self):
        """
        The run method loops forever, updating information at the requested
        interval.
        """
        while True:
            # Update status and get current position:
            x_pos, y_pos, status = update_status(self.ui)
            # If status is returned:
            if status is True:
                # If x or y position have changed, update plot:
                if x_pos != self.x_pos or y_pos != self.y_pos:
                    self.x_pos = x_pos
                    self.y_pos = y_pos
                    self.plot_status.emit()
                # Check if program plot needs updating ... Get the program
                # information:
                program = self.ui.program
                # If program x and y values are set:
                if program['x'] is not None and program['y'] is not None:
                    # Get status area:
                    status_area = self.ui.ui_components['status_area']
                    # Try to get program chart:
                    try:
                        chart_program = status_area.properties['chart_program']
                    except KeyError:
                        chart_program = None
                    # If program has update or program chart does not exist,
                    # emit program plotting signal:
                    if program['updated'] is True or chart_program is None:
                        self.plot_program.emit()
                        self.plot_status.emit()
                        self.ui.log_message('Program updated', True)
            time.sleep(self.poll_int)
